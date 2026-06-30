"""
LLM 文案生成器
支持通过 skill 系统自动适配不同项目类型的 prompt
支持 --style / --length / --extra 等运行时调整
"""

import sys
import requests
import json
from pathlib import Path
from prompts import build_system_prompt, STYLES, LENGTHS

sys.stdout.reconfigure(encoding="utf-8")


def load_config():
    config_path = Path(__file__).parent / "config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_post(repo_info, readme="", config=None, skill=None,
                  style_override=None, length_override=None, extra_instructions=None):
    """调用 LLM 生成小红书文案

    参数:
      repo_info          - 仓库信息 {"name", "description", "stars", "language", "url", "topics"}
      readme             - README 内容（截取前 2000 字符）
      config             - 配置字典
      skill              - 已匹配的 skill（由 main.py 传入）
      style_override     - 风格覆盖（excited/calm/funny/tutorial/comparison）
      length_override    - 长度覆盖（short/medium/long）
      extra_instructions - 附加指令（追加到 system prompt 末尾）

    返回:
      {"title", "body", "tags", "cover_prompt"}
    """
    if config is None:
        config = load_config()

    # 使用传入的 skill，或回退到通用
    if skill is None:
        from skills.general import SKILL as skill

    # 从 skill 的 gen_params 组装 system prompt
    gp = skill.get("gen_params", {})
    role = gp.get("role", "tech_blogger")
    style = style_override or gp.get("style", "excited")
    structure = gp.get("structure", "standard")
    length = length_override or "medium"

    # 合并 skill 自带的 style_hints + 用户 extra_instructions
    hints = gp.get("style_hints", [])
    user_extra = extra_instructions or ""
    all_extra = "\n".join(f"- {h}" for h in hints)
    if user_extra:
        all_extra += f"\n- {user_extra}"

    # 确保 required_tags 被包含
    required_tags = gp.get("required_tags", "")
    if required_tags:
        all_extra += f"\n- tags 字段必须包含 {required_tags}"

    system_prompt = build_system_prompt(
        role_key=role,
        style_key=style,
        structure_key=structure,
        length_key=length,
        extra_instructions=all_extra,
    )

    # 用户提示词（包含仓库信息）
    user_prompt = f"""请为以下 GitHub 项目生成一条小红书推广笔记。

项目信息：
- 名称：{repo_info['name']}
- 描述：{repo_info.get('description', '无')}
- Stars：{repo_info.get('stars', 0)}
- 语言：{repo_info.get('language', '未知')}
- 链接：{repo_info.get('url', '')}
- Topics：{', '.join(repo_info.get('topics', [])[:10])}
"""

    if readme:
        user_prompt += f"\nREADME 摘要：\n{readme[:2000]}"

    # 调用 LLM
    llm_config = config.get("llm", {})
    api_key = llm_config.get("api_key", "")
    api_url = llm_config.get("api_url", "").rstrip("/")
    model = llm_config.get("model", "")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.8,
        "max_tokens": 4096,
    }

    try:
        url = api_url
        style_name = STYLES.get(style, {}).get("name", style)
        length_name = LENGTHS.get(length, {}).get("desc", length)
        print(f"[generator] 调用 LLM ({skill['name']} | {style_name} | {length_name})...")
        resp = requests.post(url, headers=headers, json=body, timeout=120)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]

        # 尝试解析 JSON
        post = parse_json_response(content)
        if post:
            # 安全过滤：移除正文中的 URL 链接（小红书违规风险）
            import re
            body = post.get("body", "")
            body = re.sub(r'https?://\S+', '', body)
            body = re.sub(r'www\.\S+', '', body)
            body = re.sub(r'\s+', ' ', body).strip()
            post["body"] = body

            print(f"[generator] 文案生成成功：{post['title']}")
            return post
        else:
            print("[generator] LLM 返回内容无法解析为 JSON，尝试提取...")
            return extract_fallback(content)

    except requests.exceptions.HTTPError as e:
        print(f"[generator] HTTP 错误: {e}")
        print(f"  响应: {e.response.text[:500]}")
        return None
    except Exception as e:
        print(f"[generator] 调用失败: {e}")
        return None


def parse_json_response(content):
    """尝试从 LLM 输出中提取 JSON（容错多种格式）"""
    content = content.strip()

    # 策略1: 去除所有 ``` 包裹
    import re
    fenced = re.findall(r'```(?:json)?\s*\n?(.*?)```', content, re.DOTALL)
    for block in fenced:
        block = block.strip()
        try:
            data = json.loads(block)
            if all(k in data for k in ("title", "body", "tags")):
                return data
        except json.JSONDecodeError:
            pass

    # 策略2: 直接解析整个 content
    try:
        data = json.loads(content)
        if all(k in data for k in ("title", "body", "tags")):
            return data
    except json.JSONDecodeError:
        pass

    # 策略3: 贪婪匹配最外层 { ... }
    start = content.find("{")
    end = content.rfind("}") + 1
    if start >= 0 and end > start:
        try:
            data = json.loads(content[start:end])
            if all(k in data for k in ("title", "body", "tags")):
                return data
        except json.JSONDecodeError:
            pass

    # 策略4: 逐个 { 找起
    for i, ch in enumerate(content):
        if ch == "{":
            for j in range(len(content) - 1, i, -1):
                if content[j] == "}":
                    try:
                        data = json.loads(content[i:j + 1])
                        if all(k in data for k in ("title", "body", "tags")):
                            return data
                    except json.JSONDecodeError:
                        continue
                    break

    return None


def extract_fallback(content):
    """JSON 解析失败时的降级处理"""
    return {
        "title": "发现一个超棒的开源项目！",
        "body": content[:1000],
        "tags": "#开源 #程序员 #GitHub",
        "cover_prompt": "tech project highlight",
        "slides": [
            {"type": "cover", "heading": "开源项目", "subheading": "发现一个超棒的项目"},
            {"type": "features", "heading": "产品功能", "intro": "核心功能一览", "items": [
                {"icon": "⭐", "title": "高星项目", "desc": "GitHub 热门推荐"},
                {"icon": "🔧", "title": "实用工具", "desc": "开发者必备"},
                {"icon": "📖", "title": "开源免费", "desc": "MIT 协议开源"},
                {"icon": "🚀", "title": "快速上手", "desc": "简单易用"},
            ], "summary_text": "该项目是一款实用的开源工具，帮助开发者提升效率。", "stats": [
                {"value": "1000+", "label": "GitHub Stars"},
                {"value": "3+", "label": "核心功能"},
                {"value": "MIT", "label": "开源协议"},
                {"value": "24/7", "label": "随时可用"},
            ]},
            {"type": "highlights", "heading": "核心亮点", "intro": "为什么值得用", "items": [
                {"icon": "✦", "title": "简单易用", "desc": "上手快"},
                {"icon": "✦", "title": "性能优秀", "desc": "高效稳定"},
            ]},
            {"type": "architecture", "heading": "技术架构", "intro": "技术栈概览",
             "layers": [{"name": "核心层", "desc": "主要功能模块"}],
             "tech_stack": ["开源"]},
            {"type": "usage", "heading": "快速上手", "steps": [{"cmd": "clone & run", "desc": "克隆并运行"}],
             "github": {}},
        ],
    }


def save_draft(post, output_dir=None):
    """保存文案草稿到指定目录"""
    if output_dir is None:
        output_dir = Path(__file__).parent / "drafts"

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    filepath = output_dir / "draft.md"

    content = f"""# {post['title']}

{post['body']}

{post['tags']}

## 封面图提示词
{post.get('cover_prompt', '无')}

---
> Generated at {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    filepath.write_text(content, encoding="utf-8")
    print(f"[generator] 草稿已保存: {filepath}")
    return filepath
