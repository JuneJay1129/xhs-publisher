"""
Skill: 后端服务
覆盖：Web 框架、API、数据库、微服务、认证等
"""

SKILL = {
    "id": "backend",
    "name": "后端服务",
    "description": "Web 框架、API、数据库、微服务、认证",
    "topics": {
        "api", "rest", "graphql", "grpc", "microservice", "server",
        "backend", "database", "orm", "auth", "authentication",
        "authorization", "jwt", "oauth", "redis", "postgres", "mysql",
        "mongodb", "elasticsearch", "caching", "queue", "message-queue",
        "websocket", "http", "gin", "fastapi", "express", "nestjs",
        "spring-boot", "actix", "axum",
    },
    "languages": {"Go", "Rust", "Java", "Python", "TypeScript", "C#"},
    "keywords": {
        "api", "rest", "graphql", "grpc", "microservice", "server",
        "backend", "database", "orm", "auth", "jwt", "oauth", "redis",
        "postgres", "mysql", "cache", "queue", "websocket", "http",
        "framework", "gin", "fastapi", "express", "spring", "actix",
    },
    "gen_params": {
        "role": "backend_architect",
        "style": "calm",
        "structure": "technical",
        "style_hints": [
            "用数据说话（QPS、延迟、并发数等）",
            "提及与 Spring Boot、FastAPI、Gin 等主流框架对比",
        ],
        "required_tags": "#后端 #开源",
    },
    "cover_config": {
        "theme": "backend",
        "colors": {
            "gradient": "linear-gradient(135deg, #0c3483 0%, #a2b6df 100%)",
            "accent": "#0c3483",
            "text": "#ffffff",
            "subtitle": "rgba(255,255,255,0.85)",
        },
        "icon": "⚙️",
        "badge": "后端架构",
    },
}
