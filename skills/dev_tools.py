"""
Skill: 开发工具
覆盖：CLI 工具、编辑器、代码生成、测试框架、包管理等
"""

SKILL = {
    "id": "dev_tools",
    "name": "开发工具",
    "description": "CLI 工具、编辑器、代码生成、测试框架",
    "topics": {
        "cli", "terminal", "editor", "ide", "linter", "formatter",
        "bundler", "package-manager", "testing", "debugging", "devtools",
        "code-generation", "scaffolding", "boilerplate", "template",
        "developer-tools", "developer-experience", "dx",
    },
    "languages": {"Rust", "Go", "Python", "TypeScript", "JavaScript", "Zig", "C", "C++"},
    "keywords": {
        "cli", "terminal", "command-line", "editor", "vscode", "neovim",
        "linter", "formatter", "bundler", "webpack", "vite", "esbuild",
        "test", "debug", "profil", "benchmark", "lint", "format",
        "codegen", "scaffold", "template", "boilerplate", "npm", "cargo",
        "brew", "package", "install", "tool",
    },
    "gen_params": {
        "role": "dev_friend",
        "style": "comparison",
        "structure": "standard",
        "style_hints": [
            "强调'简洁''轻量''好用'等开发者关心的点",
            "用 before/after 对比说明工具价值",
            "提及同类工具对比（对比主流方案）",
        ],
        "required_tags": "#开发工具 #程序员",
    },
    "cover_config": {
        "theme": "dev",
        "colors": {
            "gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
            "accent": "#4facfe",
            "text": "#ffffff",
            "subtitle": "rgba(255,255,255,0.85)",
        },
        "icon": "🛠️",
        "badge": "开发利器",
    },
}
