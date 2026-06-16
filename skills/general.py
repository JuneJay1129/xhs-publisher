"""
Skill: 通用兜底
当无法匹配到特定 skill 时使用
"""

SKILL = {
    "id": "general",
    "name": "通用",
    "description": "无法匹配特定分类时的通用模板",
    "topics": set(),
    "languages": set(),
    "keywords": set(),
    "gen_params": {
        "role": "tech_blogger",
        "style": "excited",
        "structure": "standard",
        "style_hints": [
            "突出项目的实用性和'为什么值得试'",
            "避免过多技术术语，让非技术读者也能看懂",
        ],
        "required_tags": "#开源 #程序员",
    },
    "cover_config": {
        "theme": "general",
        "colors": {
            "gradient": "linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)",
            "accent": "#fcb69f",
            "text": "#2d3436",
            "subtitle": "rgba(45,52,54,0.7)",
        },
        "icon": "💡",
        "badge": "开源推荐",
    },
}
