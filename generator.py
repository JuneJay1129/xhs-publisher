"""
小红书文案生成器
用 LLM 根据 GitHub 项目信息生成小红书风格文案
"""

import sys
import requests
import json
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

CONFIG_PATH = Path(__file__).parent / "config.json"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


SYSTEM_PROMPT = """你是一个小红书爆款文案写手，专门写科技/开源项目推荐类笔记。

## 写作要求

### 标题
- 吸引眼球，带 1-2 个 emoji
- 包含数字（如 star 数、性能提升百分比）或悬念
- 15-20 字以内
- 例如："⭐2.5w星！这个开源工具帮我省了95%的API费用"

### 正文（500-800 字，分 5-6 个段落）

**第一段 — 开头钩子**
用一个具体的痛点场景引入，让读者产生共鸣。比如"你是不是也遇到过xxx的问题？"

**第二段 — 项目介绍**
清楚说明：
- 项目全称（中英文都要提）
- 用一句话概括它是什么
- 目前的 GitHub Stars 数
- 主要技术栈/语言

**第三段 — 核心功能详解**
详细介绍 2-3 个核心功能或亮点，每个功能用一两句话解释清楚。要具体，不要泛泛而谈。

**第四段 — 使用方式**
简要说明怎么上手（安装方式、支持的平台等），让读者觉得"这个我也能用"。

**第五段 — 为什么推荐**
总结推荐理由，可以对比同类工具说明优势。

**第六段 — 项目地址 + 引导**
- 明确写出项目地址（GitHub 链接）
- 结尾引导互动："感兴趣的点赞收藏，有问题评论区见！"

### 标签
- 生成 8-10 个相关标签，用 # 开头
- 包含中英文标签混搭
- 必须包含：项目名相关标签、技术领域标签、通用标签如 #开源项目 #程序员

### 风格要求
- 口语化，轻松有趣，像朋友聊天
- 适当使用 emoji 但不要过度（每段 2-3 个）
- 不要用 markdown 格式（不要用 **加粗** 或 - 列表）
- 不要用"小红书"这个词
- 要有信息量，不要水话连篇

### 封面图提示词
- 生成一段英文的 AI 绘图提示词，用于生成小红书封面图
- 风格：现代科技感，扁平插画或 3D 渲染，色彩鲜明
- 要包含项目的视觉元素（如相关技术的图标、场景）
- 不要包含中文文字（AI 绘图中文会乱码）

## 输出格式（严格遵守，不要多输出其他内容）
---TITLE---
标题内容
---BODY---
正文内容
---TAGS---
标签用空格分隔
---COVER_PROMPT---
英文封面图提示词"""


def generate_post(repo_info, readme_summary="", config=None):
    """根据仓库信息生成小红书文案"""
    if config is None:
        config = load_config()

    llm_config = config["llm"]

    # 构建用户 prompt
    user_prompt = f"""请为以下 GitHub 项目写一篇小红书笔记：

项目名称：{repo_info['name']}
Stars：{repo_info['stars']}
语言：{repo_info['language']}
简介：{repo_info['description']}
Topics：{', '.join(repo_info.get('topics', []))}
项目地址：{repo_info['url']}

README 摘要：
{readme_summary[:1500]}

请生成小红书风格的文案。"""

    payload = {
        "model": llm_config["model"],
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": 2000,
        "temperature": 0.75,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {llm_config.get('api_key', '')}",
    }

    try:
        resp = requests.post(
            llm_config["api_url"],
            json=payload,
            headers=headers,
            timeout=60,
        )
        resp.raise_for_status()
        result = resp.json()
        content = result["choices"][0]["message"]["content"]
        print(f"[generator] LLM 返回 {len(content)} 字符")
        print(f"[generator] 原始响应前200字: {content[:200]}")
    except Exception as e:
        print(f"[generator] LLM 请求失败: {e}")
        return None

    return parse_response(content)


def parse_response(text):
    """解析 LLM 输出的文案"""
    post = {"title": "", "body": "", "tags": "", "cover_prompt": ""}

    try:
        # 按分隔符拆分
        parts = text.split("---")
        for i, part in enumerate(parts):
            part_clean = part.strip()
            if part_clean == "TITLE":
                post["title"] = parts[i + 1].strip()
            elif part_clean == "BODY":
                post["body"] = parts[i + 1].strip()
            elif part_clean == "TAGS":
                post["tags"] = parts[i + 1].strip()
            elif part_clean == "COVER_PROMPT":
                post["cover_prompt"] = parts[i + 1].strip()
    except (IndexError, ValueError):
        # 解析失败时用全文作为 body
        print(f"[generator] 解析失败，原始内容: {text[:200]}")
        post["body"] = text
        post["title"] = "🔥 今日推荐开源项目"

    if not post["title"]:
        print("[generator] 警告: 标题为空")
    if not post["body"]:
        print("[generator] 警告: 正文为空")

    return post


def save_draft(post, date_str=None):
    """保存文案草稿到本地"""
    if date_str is None:
        from datetime import datetime
        date_str = datetime.now().strftime("%Y-%m-%d")

    drafts_dir = Path(__file__).parent / "drafts"
    drafts_dir.mkdir(exist_ok=True)

    filepath = drafts_dir / f"{date_str}.md"

    content = f"""# {post['title']}

{post['body']}

{post['tags']}

## 封面图提示词
{post.get('cover_prompt', '无')}

---
> Generated at {date_str}
"""
    filepath.write_text(content, encoding="utf-8")
    print(f"[generator] 草稿已保存: {filepath}")
    return filepath


if __name__ == "__main__":
    # 测试用
    test_repo = {
        "name": "test/ai-tool",
        "description": "A cool AI developer tool",
        "stars": 1234,
        "language": "Python",
        "url": "https://github.com/test/ai-tool",
        "topics": ["ai", "developer-tools"],
    }
    post = generate_post(test_repo, "This is a test README summary.")
    print(f"标题: {post['title']}")
    print(f"正文:\n{post['body']}")
    print(f"标签: {post['tags']}")
