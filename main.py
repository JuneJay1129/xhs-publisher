"""
小红书自动发布工具 - 主入口
GitHub 热门项目 → LLM 生成文案 → 半自动发布到小红书

用法：
  python main.py              # 完整流程（采集→生成→发布）
  python main.py --draft      # 仅生成文案草稿，不发布
  python main.py --pick N     # 指定第 N 个项目（从缓存列表选）
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Windows UTF-8 输出
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from scraper import get_repos, pick_best_repo
from generator import generate_post, save_draft
from cover_gen import generate_covers
from publisher import publish_post


def load_config():
    with open(Path(__file__).parent / "config.json", "r", encoding="utf-8") as f:
        return json.load(f)


def run(skip_publish=False, pick_index=None):
    """完整流程：采集 → 生成 → 发布"""
    config = load_config()
    date_str = datetime.now().strftime("%Y-%m-%d")

    print(f"{'='*50}")
    print(f"🚀 小红书自动发布 - {date_str}")
    print(f"{'='*50}\n")

    # Step 1: 获取热门项目
    print("📥 Step 1: 获取热门项目...")
    repos = get_repos(config)

    if not repos:
        print("❌ 没有找到项目，请先运行采集")
        return

    # 打印候选列表
    print(f"\n热门项目列表：")
    for i, r in enumerate(repos[:10], 1):
        print(f"  {i}. {r['name']} ⭐{r['stars']} - {r['description'][:50]}")

    # 选择项目
    if pick_index is not None and 0 < pick_index <= len(repos):
        repo = repos[pick_index - 1]
        print(f"\n👆 手动选择第 {pick_index} 个项目")
    else:
        # 读取已使用记录，避免重复
        used_path = Path(__file__).parent / "data" / "used.json"
        used_names = set()
        if used_path.exists():
            used_names = set(json.loads(used_path.read_text(encoding="utf-8")))

        repo = pick_best_repo(repos, used_names)

        # 记录已使用
        used_names.add(repo["name"])
        used_path.parent.mkdir(parents=True, exist_ok=True)
        used_path.write_text(json.dumps(list(used_names), ensure_ascii=False), encoding="utf-8")

    print(f"\n🎯 选中: {repo['name']} ⭐{repo['stars']}")
    print(f"   {repo['description'][:80]}")

    # 获取 README（从 GitHub API，失败则跳过）
    print("\n📖 尝试获取 README...")
    readme = ""
    try:
        import requests
        url = f"https://api.github.com/repos/{repo['name']}/readme"
        headers = {"Accept": "application/vnd.github.v3.raw", "User-Agent": "xhs-publisher/1.0"}
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.ok:
            readme = resp.text[:2000]
            print(f"   获取成功（{len(readme)} 字符）")
    except Exception:
        print("   获取失败，用 description 替代")
        readme = repo.get("description", "")

    # Step 2: 生成文案
    print("\n✍️  Step 2: 生成小红书文案...")
    post = generate_post(repo, readme, config)

    if not post:
        print("❌ 文案生成失败")
        return

    # 打印文案
    print(f"\n{'─'*40}")
    print(f"📝 {post['title']}")
    print(f"{'─'*40}")
    print(post["body"])
    print(f"\n{post['tags']}")
    print(f"{'─'*40}\n")

    # 保存草稿
    draft_path = save_draft(post, date_str)

    # Step 3: 生成封面图 HTML
    print("\n🎨 Step 3: 生成封面图...")
    cover_paths = generate_covers(post, repo, date_str)
    print(f"   共 {len(cover_paths)} 张，用浏览器打开后截图即可")

    if skip_publish:
        print("\n✅ 草稿 + 封面图已生成，跳过发布")
        return post, draft_path

    # Step 3: 发布
    print("📤 Step 3: 打开小红书发布页...")
    success = publish_post(post)
    print("✅ 完成！" if success else "⚠️  请手动检查发布状态")

    return post, draft_path


if __name__ == "__main__":
    args = sys.argv[1:]
    skip = "--draft" in args
    pick = None
    for a in args:
        if a.startswith("--pick"):
            idx = args.index(a)
            if idx + 1 < len(args):
                pick = int(args[idx + 1])
    run(skip_publish=skip, pick_index=pick)
