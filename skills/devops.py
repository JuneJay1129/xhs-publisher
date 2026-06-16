"""
Skill: DevOps / 基础设施
覆盖：容器、CI/CD、监控、云原生、IaC、K8s 等
"""

SKILL = {
    "id": "devops",
    "name": "DevOps / 基础设施",
    "description": "容器、CI/CD、监控、云原生、IaC",
    "topics": {
        "docker", "kubernetes", "k8s", "container", "ci-cd", "github-actions",
        "terraform", "ansible", "pulumi", "infrastructure", "cloud-native",
        "monitoring", "observability", "logging", "tracing", "prometheus",
        "grafana", "devops", "sre", "deployment", "helm", "istio",
        "service-mesh", "load-balancer", "nginx", "traefik", "caddy",
    },
    "languages": {"Go", "Rust", "Shell", "Python", "TypeScript"},
    "keywords": {
        "docker", "kubernetes", "k8s", "container", "ci-cd", "deploy",
        "terraform", "ansible", "infra", "cloud", "aws", "gcp", "azure",
        "monitor", "log", "trace", "metric", "alert", "grafana",
        "prometheus", "nginx", "proxy", "load balance", "scale",
    },
    "gen_params": {
        "role": "devops_engineer",
        "style": "calm",
        "structure": "technical",
        "style_hints": [
            "用实际运维场景说明价值（'部署时间从30分钟→3分钟'）",
            "提及与 Docker、K8s、Terraform、Prometheus 等对比",
        ],
        "required_tags": "#DevOps #运维",
    },
    "cover_config": {
        "theme": "devops",
        "colors": {
            "gradient": "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)",
            "accent": "#11998e",
            "text": "#ffffff",
            "subtitle": "rgba(255,255,255,0.85)",
        },
        "icon": "🐳",
        "badge": "DevOps",
    },
}
