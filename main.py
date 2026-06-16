"""
小红书自动发布工具
用法：
  python main.py list                  # 查看 GitHub 热门项目
  python main.py generate              # 生成文案（默认 1 篇）
  python main.py generate -n 3         # 生成 3 篇文案
  python main.py generate --style calm # 用沉稳风格生成
  python main.py generate --dry-run    # 只看标题不调 LLM
  python main.py publish               # 自动发布到小红书
  python main.py preview               # 预览生成的 HTML 封面

风格选项 (--style)：excited(默认) | calm | funny | tutorial | comparison
长度选项 (--length)：short(200-350字) | medium(默认300-600字) | long(500-800字)
附加指令 (--extra)："多用繁体字" / "跟xx对比" / "不要用网络用语" 等
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")


def get_output_dir():
    """基于当前时间的输出目录"""
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S")


def load_used(used_path):
    if used_path.exists():
        return set(json.loads(used_path.read_text(encoding="utf-8")))
    return set()


def save_used(used_path, used_set):
    used_path.write_text(json.dumps(list(used_set), ensure_ascii=False, indent=2), encoding="utf-8")


def cmd_list(args):
    """查看热门项目列表"""
    from scraper import get_repos, DATA_PATH
    repos = get_repos()
    print(f"\nGitHub 热门项目\n")
    for i, r in enumerate(repos, 1):
        topics = ", ".join(r.get("topics", [])[:5])
        print(f"  {i:2d}. {r['name']:<30s} ⭐ {r['stars']:>6,}  {r['language'] or '':<12s} {topics}")
        print(f"      {r.get('description', '')[:80]}")
    print(f"\n共 {len(repos)} 个项目（缓存于 {DATA_PATH}）")


def cmd_generate(args):
    """生成文案"""
    from scraper import get_repos
    from skills import detect_skill
    from generator import generate_post, save_draft

    config_path = Path(__file__).parent / "config.json"
    if not config_path.exists():
        print("[错误] config.json 不存在，请先创建配置文件。")
        print("  参考 config.example.json")
        return

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    used_path = Path(__file__).parent / "data" / "used.json"
    used = load_used(used_path)

    # 获取项目列表
    repos = get_repos()

    # 过滤已使用
    available = [r for r in repos if r["name"] not in used]
    if not available:
        print("[提示] 所有项目都已使用过，重置已用列表。")
        used.clear()
        available = repos

    # 选前 N 个（跳过已处理的）
    to_process = available[:args.n]

    if args.dry_run:
        print(f"\n[dry-run] 将处理 {len(to_process)} 个项目：\n")
        for r in to_process:
            skill, score, reason = detect_skill(r)
            print(f"  - {r['name']:<30s} ⭐ {r['stars']:>6,}  →  [{skill['id']}] {skill['name']} ({reason})")
        return

    # 创建时间戳输出目录
    timestamp_dir = Path(__file__).parent / "output" / get_output_dir()

    print(f"\n开始生成 {len(to_process)} 篇文案...\n")

    for i, r in enumerate(to_process, 1):
        print(f"━━━ [{i}/{len(to_process)}] {r['name']} ━━━")
        skill, score, reason = detect_skill(r)
        print(f"  匹配 skill: [{skill['id']}] {skill['name']} ({reason})")

        # 读取 README（缓存中没有 readme 字段，跳过）
        readme = ""

        # 生成文案
        post = generate_post(
            r, readme, config, skill,
            style_override=args.style,
            length_override=args.length,
            extra_instructions=args.extra,
        )
        if post:
            out_dir = timestamp_dir / r["name"]
            save_draft(post, out_dir)

            # 生成介绍图
            slides = post.get("slides", [])
            if slides:
                # 注入 GitHub 项目信息到各 slide
                owner = r["name"].split("/")[0] if "/" in r["name"] else ""
                for s in slides:
                    # 封面：注入 avatar
                    if s.get("type") == "cover" and owner:
                        s["avatar_url"] = f"https://github.com/{owner}.png"
                        if not s.get("star_text") and r.get("stars"):
                            s["star_text"] = f"{r['stars']:,}"
                        if not s.get("lang_text") and r.get("language"):
                            s["lang_text"] = r["language"]
                    # 使用页：注入 GitHub 信息
                    if s.get("type") == "usage":
                        gh = s.get("github", {})
                        if not gh.get("name"):
                            s["github"] = {
                                "name": r["name"],
                                "desc": (r.get("description") or "")[:50],
                                "stars": f"{r.get('stars', 0):,}",
                                "forks": f"{r.get('forks', 0):,}" if r.get("forks") else "—",
                                "url": r.get("url", ""),
                            }

                from slide_gen import generate_slides
                img_dir = out_dir / "images"
                saved = generate_slides(slides, img_dir)
                print(f"  📸 生成 {len(saved)} 张介绍图")

            used.add(r["name"])
            print()

    save_used(used_path, used)
    print(f"✅ 全部完成！文案保存在 output/{get_output_dir()}/")


def cmd_publish(args):
    """发布到小红书"""
    from publisher import publish_post
    publish_post()


def cmd_preview(args):
    """预览封面"""
    from cover_gen import generate_covers_from_draft
    generate_covers_from_draft()


def main():
    parser = argparse.ArgumentParser(
        description="小红书自动发布工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command")

    # list
    p_list = sub.add_parser("list", help="查看 GitHub 热门项目")
    p_list.add_argument("--lang", default="", help="编程语言筛选")
    p_list.add_argument("--since", default="daily", choices=["daily", "weekly", "monthly"])
    p_list.set_defaults(func=cmd_list)

    # generate
    p_gen = sub.add_parser("generate", help="生成文案")
    p_gen.add_argument("-n", type=int, default=1, help="生成数量（默认 1）")
    p_gen.add_argument("--style", default=None,
                       choices=["excited", "calm", "funny", "tutorial", "comparison"],
                       help="文案风格（默认根据 skill 自动选择）")
    p_gen.add_argument("--length", default=None,
                       choices=["short", "medium", "long"],
                       help="文案长度（默认 medium）")
    p_gen.add_argument("--extra", default=None,
                       help="附加指令，如 --extra '多用繁体字' --extra '跟XX对比'")
    p_gen.add_argument("--dry-run", action="store_true", help="只显示标题，不调用 LLM")
    p_gen.set_defaults(func=cmd_generate)

    # publish
    p_pub = sub.add_parser("publish", help="发布到小红书")
    p_pub.set_defaults(func=cmd_publish)

    # preview
    p_pre = sub.add_parser("preview", help="预览生成的 HTML 封面")
    p_pre.set_defaults(func=cmd_preview)

    args = parser.parse_args()
    if args.command:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
