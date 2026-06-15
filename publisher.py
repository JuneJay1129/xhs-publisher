"""
小红书半自动发布器
用 Playwright 打开小红书发布页，自动填入内容
用户确认后手动点击发布
"""

from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.json"


def publish_post(post):
    """打开浏览器，自动填入文案内容，等待用户确认发布"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[publisher] playwright 未安装，请运行: pip install playwright && playwright install chromium")
        return False

    import json
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    xhs_config = config["xhs"]
    creator_url = xhs_config["creator_url"]
    timeout = xhs_config.get("browser_timeout", 60000)

    # 检查是否有保存的登录状态
    storage_path = Path(__file__).parent / "browser_state.json"

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=xhs_config.get("headless", False),
            args=["--disable-blink-features=AutomationControlled"],
        )

        # 尝试恢复登录状态
        context_opts = {
            "viewport": {"width": 1280, "height": 900},
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }
        if storage_path.exists():
            context_opts["storage_state"] = str(storage_path)
            print("[publisher] 恢复上次登录状态...")

        context = browser.new_context(**context_opts)
        page = context.new_page()

        # 打开小红书发布页
        print(f"[publisher] 正在打开小红书创作中心...")
        page.goto(creator_url, wait_until="domcontentloaded", timeout=timeout)

        # 检查是否需要登录
        if "login" in page.url or page.locator('text="登录"').count() > 0:
            print("\n" + "=" * 50)
            print("⚠️  需要登录小红书！")
            print("请在弹出的浏览器中手动扫码/登录")
            print("登录成功后脚本会自动继续...")
            print("=" * 50 + "\n")

            # 等待登录完成（跳转到发布页）
            page.wait_for_url("**/publish/**", timeout=120000)
            # 保存登录状态
            context.storage_state(path=str(storage_path))
            print("[publisher] 登录状态已保存！")

        # 等待发布页加载
        page.wait_for_load_state("networkidle", timeout=30000)

        # 尝试定位标题输入框并填入内容
        try:
            # 小红书发布页的标题输入框
            title_input = page.locator('[placeholder*="标题"]').first
            if title_input.count() > 0:
                title_input.click()
                title_input.fill(post["title"])
                print(f"[publisher] 标题已填入: {post['title']}")
        except Exception as e:
            print(f"[publisher] 标题填入失败: {e}")

        # 尝试定位正文编辑区并填入内容
        try:
            # 小红书发布页的正文区域（contenteditable div）
            body_input = page.locator('[contenteditable="true"]').first
            if body_input.count() > 0:
                body_input.click()
                # 组合正文 + 标签
                full_text = post["body"] + "\n\n" + post["tags"]
                body_input.fill(full_text)
                print(f"[publisher] 正文已填入（{len(full_text)} 字）")
        except Exception as e:
            print(f"[publisher] 正文填入失败: {e}")

        print("\n" + "=" * 50)
        print("✅ 内容已自动填入！")
        print("请在浏览器中检查内容，选择封面图，然后点击发布")
        print("完成后按 Enter 关闭浏览器...")
        print("=" * 50)

        input()  # 等待用户确认

        # 保存登录状态
        context.storage_state(path=str(storage_path))
        browser.close()

    return True


if __name__ == "__main__":
    # 测试用
    test_post = {
        "title": "🔥 这个 AI 工具太强了！",
        "body": "测试正文内容",
        "tags": "#AI #开发者工具 #开源",
    }
    publish_post(test_post)
