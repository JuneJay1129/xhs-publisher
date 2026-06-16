"""
Skill: AI Agent / 自动化
覆盖：AI Agent 框架、自动化工具、工作流编排、Copilot 等
"""

SKILL = {
    "id": "ai_agent",
    "name": "AI Agent / 自动化",
    "description": "AI Agent 框架、自动化工具、工作流编排",
    "topics": {
        "agent", "autonomous-agent", "multi-agent", "automation",
        "workflow", "orchestration", "copilot", "assistant",
        "chatbot-framework", "tool-use", "function-calling",
        "browser-agent", "coding-agent", "task-automation",
    },
    "languages": {"Python", "TypeScript", "JavaScript"},
    "keywords": {
        "agent", "autonomous", "automation", "workflow", "orchestrat",
        "copilot", "assistant", "multi-agent", "task", "pipeline",
        "browser", "scrape", "crawl", "rpa", "no-code", "low-code",
        "scheduler", "cron", "monitor", "deploy",
    },
    "gen_params": {
        "role": "efficiency_guru",
        "style": "excited",
        "structure": "standard",
        "style_hints": [
            "强调'自动化''解放双手''效率翻倍'等关键词",
            "用具体场景说明价值（'每天省2小时''自动帮你xxx'）",
            "适当提及竞品对比（Cursor、Copilot、AutoGPT 等）",
        ],
        "required_tags": "#AI #效率工具",
    },
    "cover_config": {
        "theme": "agent",
        "colors": {
            "gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
            "accent": "#f5576c",
            "text": "#ffffff",
            "subtitle": "rgba(255,255,255,0.85)",
        },
        "icon": "⚡",
        "badge": "效率神器",
    },
}
