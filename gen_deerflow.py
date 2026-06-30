"""单项目生成脚本 — bytedance/deer-flow
优化点：
1. 模板间距压缩 → 内容更饱满
2. 丰富文字描述 → 每页信息密度更高
3. 文案无 URL
"""

import sys, json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

from slide_gen import generate_slides

SLIDES_DATA = [
    # ── ① 封面 ──
    {
        "type": "cover",
        "heading": "DeerFlow",
        "subheading": "字节跳动开源 · 超级 Agent 运行时",
        "avatar_url": "https://github.com/bytedance.png",
        "star_text": "75K",
        "lang_text": "Python",
    },

    # ── ② 特性 ──
    {
        "type": "features",
        "heading": "DeerFlow 能做什么？",
        "intro": "从深度研究到全能 Agent，一个 Harness 搞定一切",
        "project_name": "DeerFlow",
        "items": [
            {
                "icon": "🧩",
                "title": "Skill 系统",
                "desc": "结构化能力模块，按需加载",
                "detail": "内置研究/报告/PPT/网页/图片/视频生成 Skill，支持自定义扩展，渐进式加载节省 Token",
            },
            {
                "icon": "🤖",
                "title": "子 Agent 调度",
                "desc": "主 Agent 自动拆解任务并分发",
                "detail": "复杂任务自动分解为多个子 Agent 并行执行，结果汇聚后统一输出，支持分钟级到小时级任务",
            },
            {
                "icon": "🗂️",
                "title": "沙盒文件系统",
                "desc": "每个任务独立执行环境",
                "detail": "Docker 容器隔离，Agent 可读写文件、执行命令、查看图片，上传/工作区/输出三目录分离",
            },
            {
                "icon": "🧠",
                "title": "长期记忆 + 上下文工程",
                "desc": "跨会话记住你的偏好和风格",
                "detail": "持久化记忆用户画像、技术栈和工作习惯；子 Agent 独立上下文，完成任务自动压缩摘要",
            },
        ],
        "summary_text": "DeerFlow 2.0 是字节跳动开源的超级 Agent 运行时，基于 LangGraph + LangChain，"
                        "内置 Skill / 子 Agent / 沙盒 / 记忆 / TUI 五大模块，从深度研究到复杂工作流一站搞定。",
        "stats": [
            {"value": "75K+", "label": "GitHub Stars"},
            {"value": "5", "label": "核心模块"},
            {"value": "20+", "label": "内置 Skill"},
            {"value": "10K+", "label": "Forks"},
        ],
    },

    # ── ③ 亮点 ──
    {
        "type": "highlights",
        "heading": "为什么选 DeerFlow？",
        "intro": "不只是 Deep Research 框架，更是全能 Agent 基础设施",
        "items": [
            {
                "icon": "🏗️",
                "title": "Harness 架构",
                "desc": "不是框架拼装，而是开箱即用的 Agent 运行时。内置文件系统、记忆、Skill、沙盒、子 Agent 规划，"
                       "无需手动集成。从社区反馈中迭代：用户把它用在数据管道、PPT 生成、仪表盘、内容自动化等场景，"
                       "远超最初的 Deep Research 定位。",
            },
            {
                "icon": "⚡",
                "title": "Python 嵌入式客户端",
                "desc": "无需启动 HTTP 服务，直接在 Python 中调用 DeerFlowClient 实现 chat / stream / "
                       "配置管理 / 文件上传。返回格式与 HTTP Gateway 完全一致，适合集成到现有 Python 工作流。",
            },
            {
                "icon": "🖥️",
                "title": "终端工作台 (TUI)",
                "desc": "键盘驱动的终端界面：Markdown 流式渲染、工具活动卡片、/ 命令面板、模型切换、"
                       "会话历史、Ctrl+C 中断。TUI 和 Web UI 共享线程存储，无缝切换。",
            },
        ],
        "metrics": [
            {"value": "0", "label": "框架依赖"},
            {"value": "1 行", "label": "启动命令"},
            {"value": "Docker", "label": "沙盒隔离"},
        ],
        "scenarios": [
            {"quote": "用 DeerFlow 跑了一个 2 小时的深度研究任务，自动拆成 12 个子 Agent 并行，最后汇总成 30 页报告", "author": "HN 用户"},
            {"quote": "把公司的数据管道从 Airflow 迁到 DeerFlow Skill，配置量减少 80%", "author": "Data Engineer"},
            {"quote": "TUI 是我用过最好的终端 AI 界面，比 Claude Code 更灵活", "author": "终端爱好者"},
        ],
    },

    # ── ④ 架构 ──
    {
        "type": "architecture",
        "heading": "技术架构",
        "intro": "LangGraph 驱动 · 模块化 · 可扩展",
        "layers": [
            {"icon": "🖥️", "name": "交互层", "desc": "Web UI / TUI / Python Client / Claude Code 集成，多入口统一 Gateway API"},
            {"icon": "⚙️", "name": "调度层", "desc": "LangGraph 状态机 + 子 Agent 规划器，任务拆解→并行执行→结果汇聚"},
            {"icon": "🧩", "name": "能力层", "desc": "Skill 系统（渐进式加载）+ 核心工具（搜索/抓取/文件/Shell）+ MCP 扩展"},
            {"icon": "💾", "name": "基础设施", "desc": "Docker 沙盒隔离 + 长期记忆持久化 + 上下文压缩 + Token 追踪"},
        ],
        "description": "DeerFlow 2.0 从 Deep Research 框架进化为超级 Agent 运行时。"
                       "基于 LangGraph 状态机管理 Agent 执行流，支持动态子 Agent 派发和并行执行。"
                       "Skill 系统采用渐进式加载（仅在需要时读取 SKILL.md），保持上下文窗口精简。"
                       "沙盒环境通过 AioSandboxProvider 实现 Docker 容器隔离，LocalSandboxProvider 支持本地开发。"
                       "长期记忆跨会话持久化，越用越懂你。支持 OpenAI 兼容 API，可接入任意 LLM 供应商。",
        "tech_stack": [
            "Python", "TypeScript", "LangGraph", "LangChain",
            "Next.js", "Docker", "OpenAI API",
        ],
    },

    # ── ⑤ 使用 ──
    {
        "type": "usage",
        "heading": "30 秒开始使用",
        "steps": [
            {"cmd": "克隆仓库", "desc": "git clone 并进入目录"},
            {"cmd": "一键启动", "desc": "python -m deerflow up，自动拉取镜像并启动"},
            {"cmd": "打开浏览器", "desc": "访问 localhost:2026 开始对话"},
            {"cmd": "或用 TUI", "desc": "pip install deerflow-harness[tui]，终端直接用"},
        ],
        "github": {
            "name": "bytedance/deer-flow",
            "desc": "Open-source long-horizon SuperAgent harness that researches, codes, and builds for you",
            "stars": "75,473",
            "forks": "10,187",
            "url": "https://github.com/bytedance/deer-flow",
        },
        "code_example": {"title": "嵌入式调用", "code": "from deerflow.client import DeerFlowClient\n\nclient = DeerFlowClient()\nresponse = client.chat(\"分析这篇论文\", thread_id=\"my-thread\")"},
        "tips": ["支持 OpenAI 兼容 API，可接任意 LLM", "Skill 可通过 Gateway 安装 .skill 包", "TUI 和 Web UI 共享会话"],
    },
]


def main():
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    out_dir = Path(__file__).parent / "output" / timestamp / "bytedance" / "deer-flow" / "images"
    out_dir.mkdir(parents=True, exist_ok=True)
    saved = generate_slides(SLIDES_DATA, out_dir)
    print(f"📸 生成 {len(saved)} 张介绍图 → {out_dir}")
    for p in saved:
        print(f"  {p}")


if __name__ == "__main__":
    main()
