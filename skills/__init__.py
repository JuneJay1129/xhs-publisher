"""
Skills 注册表
根据项目元数据（topics、language、description）自动匹配最合适的 skill
"""

from .ai_model import SKILL as ai_model
from .ai_agent import SKILL as ai_agent
from .dev_tools import SKILL as dev_tools
from .web_frontend import SKILL as web_frontend
from .backend import SKILL as backend
from .devops import SKILL as devops
from .general import SKILL as general

# 所有已注册 skill，按优先级排序（越前面越优先匹配）
SKILLS = [ai_model, ai_agent, dev_tools, web_frontend, backend, devops]


def detect_skill(repo_info):
    """根据仓库信息自动匹配最佳 skill

    参数:
      repo_info - {"name", "description", "stars", "language", "url", "topics"}

    返回:
      (skill_dict, score, reason)
    """
    topics = {t.lower() for t in repo_info.get("topics", [])}
    lang = (repo_info.get("language") or "").lower()
    desc = (repo_info.get("description") or "").lower()
    name = (repo_info.get("name") or "").lower()

    best_skill = None
    best_score = 0
    best_reason = ""

    for skill in SKILLS:
        score = 0
        matched = []

        # topics 匹配（权重最高）
        topic_hits = topics & skill["topics"]
        if topic_hits:
            score += len(topic_hits) * 100
            matched.append(f"topics:{','.join(topic_hits)}")

        # language 匹配
        if lang in skill["languages"]:
            score += 50
            matched.append(f"lang:{lang}")

        # description 关键词匹配
        for kw in skill["keywords"]:
            if kw in desc or kw in name:
                score += 30
                matched.append(f"kw:{kw}")

        if score > best_score:
            best_score = score
            best_skill = skill
            best_reason = " | ".join(matched) if matched else "fallback"

    # 无匹配则用通用 skill
    if best_score == 0:
        return general, 0, "no match, using general"

    return best_skill, best_score, best_reason


def list_skills():
    """列出所有已注册 skill"""
    result = []
    for s in SKILLS:
        result.append({
            "id": s["id"],
            "name": s["name"],
            "description": s["description"],
            "keywords_sample": list(s["keywords"])[:5],
        })
    result.append({
        "id": general["id"],
        "name": general["name"],
        "description": general["description"],
        "keywords_sample": [],
    })
    return result
