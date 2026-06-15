"""
GitHub 热门项目采集器
使用 GitHub Trending 页面 + 搜索获取 AI/开发工具热门项目
支持两种模式：
  1. 直接读取 nanobot 预采集的 data.json（推荐，避免 SSL 问题）
  2. 直接调用 GitHub API（备用）
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding="utf-8")

CONFIG_PATH = Path(__file__).parent / "config.json"
DATA_PATH = Path(__file__).parent / "data" / "trending.json"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_cached_repos():
    """读取 nanobot 预采集的热门项目数据"""
    if not DATA_PATH.exists():
        print("[scraper] 没有缓存数据，请先运行 nanobot 采集")
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"[scraper] 从缓存读取到 {len(data)} 个项目")
    return data


def save_repos(repos):
    """保存采集结果"""
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(repos, f, ensure_ascii=False, indent=2)
    print(f"[scraper] 已保存 {len(repos)} 个项目到 {DATA_PATH}")


def pick_best_repo(repos, used_names=None):
    """
    从列表中挑选最适合写小红书文案的仓库
    策略：优先选 AI/agent 相关 + 高 stars + 近期活跃
    排除已使用过的项目
    """
    if not repos:
        return None

    if used_names is None:
        used_names = set()

    # 关键词权重（AI/agent 相关加分）
    ai_keywords = {"ai", "agent", "llm", "gpt", "claude", "copilot", "autonomous",
                   "machine-learning", "deep-learning", "neural", "transformer",
                   "rag", "embedding", "fine-tune", "inference", "model"}

    scored = []
    for r in repos:
        if r["name"] in used_names:
            continue
        score = r["stars"] / 100  # 基础分
        # topic 加分
        topics_lower = {t.lower() for t in r.get("topics", [])}
        keyword_overlap = topics_lower & ai_keywords
        score += len(keyword_overlap) * 500
        # description 关键词加分
        desc_lower = (r.get("description") or "").lower()
        for kw in ai_keywords:
            if kw in desc_lower:
                score += 200
        scored.append((score, r))

    if not scored:
        return repos[0] if repos else None

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1]


def fetch_trending_api(config=None):
    """备用：直接调用 GitHub API（需要网络支持）"""
    import requests
    if config is None:
        config = load_config()

    gh_config = config["github"]
    since_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    query = f"topic:ai OR topic:agent OR topic:llm stars:>={gh_config['min_stars']} pushed:>={since_date}"
    url = "https://api.github.com/search/repositories"
    params = {"q": query, "sort": "stars", "order": "desc", "per_page": gh_config["max_results"]}
    headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "xhs-publisher/1.0"}

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=30)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        repos = [{
            "name": item["full_name"],
            "description": item.get("description") or "",
            "stars": item["stargazers_count"],
            "language": item.get("language") or "",
            "url": item["html_url"],
            "topics": item.get("topics", []),
        } for item in items]
        save_repos(repos)
        return repos
    except Exception as e:
        print(f"[scraper] API 请求失败: {e}")
        return []


def get_repos(config=None):
    """获取项目列表（优先缓存，缓存不存在则尝试 API）"""
    repos = load_cached_repos()
    if repos:
        return repos
    print("[scraper] 缓存为空，尝试 API...")
    return fetch_trending_api(config)


if __name__ == "__main__":
    repos = get_repos()
    for i, r in enumerate(repos[:10], 1):
        print(f"{i}. {r['name']} ⭐{r['stars']} - {r['description'][:60]}")
