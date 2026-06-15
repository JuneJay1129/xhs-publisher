"""
小红书 HTML 封面图生成器
生成 1080x1440 竖版 HTML 页面，截图后作为小红书封面/配图
"""

import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

OUTPUT_DIR = Path(__file__).parent / "covers"


def ensure_output_dir():
    OUTPUT_DIR.mkdir(exist_ok=True)


# ── 通用 CSS 变量 ──────────────────────────────────────────

COMMON_CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  width: 1080px;
  height: 1440px;
  font-family: 'PingFang SC', 'Microsoft YaHei', 'Noto Sans SC', sans-serif;
  overflow: hidden;
  position: relative;
}

.page {
  width: 1080px;
  height: 1440px;
  padding: 80px 72px;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

/* 背景装饰圆 */
.deco-circle {
  position: absolute;
  border-radius: 50%;
  opacity: 0.12;
  z-index: 0;
}

/* 内容在装饰之上 */
.content { position: relative; z-index: 1; flex: 1; display: flex; flex-direction: column; }
"""


# ── 封面图 ─────────────────────────────────────────────────

def cover_html(post, repo_info):
    title = post["title"]
    stars = repo_info.get("stars", 0)
    stars_display = f"{stars // 1000}.{stars % 1000 // 100}w" if stars >= 10000 else f"{stars // 1000}k"
    lang = repo_info.get("language", "")
    name = repo_info.get("name", "")
    desc = repo_info.get("description", "")[:80]

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{COMMON_CSS}

body {{
  background: linear-gradient(155deg, #1a1a2e 0%, #16213e 40%, #0f3460 100%);
  color: #fff;
}}

.deco-circle.c1 {{ width: 400px; height: 400px; background: #e94560; top: -100px; right: -80px; }}
.deco-circle.c2 {{ width: 250px; height: 250px; background: #533483; bottom: 100px; left: -60px; }}
.deco-circle.c3 {{ width: 180px; height: 180px; background: #0f9b8e; bottom: -40px; right: 120px; }}

.badge {{
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: rgba(255,255,255,0.12);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.18);
  border-radius: 50px;
  padding: 14px 28px;
  font-size: 28px;
  color: #ffd700;
  margin-bottom: 48px;
  width: fit-content;
}}

.badge .star {{ font-size: 32px; }}

.cover-title {{
  font-size: 72px;
  font-weight: 900;
  line-height: 1.25;
  margin-bottom: 36px;
  background: linear-gradient(135deg, #fff 0%, #e0e0ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: 2px;
}}

.subtitle {{
  font-size: 32px;
  color: rgba(255,255,255,0.75);
  line-height: 1.6;
  margin-bottom: 48px;
}}

.stats-row {{
  display: flex;
  gap: 24px;
  margin-bottom: 48px;
}}

.stat-card {{
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 20px;
  padding: 24px 36px;
  text-align: center;
}}

.stat-card .num {{
  font-size: 42px;
  font-weight: 800;
  color: #ffd700;
}}

.stat-card .label {{
  font-size: 22px;
  color: rgba(255,255,255,0.6);
  margin-top: 4px;
}}

.bottom-bar {{
  margin-top: auto;
  display: flex;
  align-items: center;
  gap: 16px;
  padding-top: 36px;
  border-top: 1px solid rgba(255,255,255,0.1);
}}

.bottom-bar .gh-icon {{
  width: 48px; height: 48px;
  background: rgba(255,255,255,0.15);
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 26px;
}}

.bottom-bar .repo-name {{
  font-size: 28px;
  color: rgba(255,255,255,0.7);
}}
</style></head><body>
<div class="page">
  <div class="deco-circle c1"></div>
  <div class="deco-circle c2"></div>
  <div class="deco-circle c3"></div>

  <div class="content">
    <div class="badge">
      <span class="star">⭐</span>
      <span>{stars_display} Stars on GitHub</span>
    </div>

    <div class="cover-title">{title.replace('⭐2.5w星！', '').replace('🔥', '').replace('！', '').strip()}</div>

    <div class="subtitle">{desc}</div>

    <div class="stats-row">
      <div class="stat-card">
        <div class="num">{stars_display}</div>
        <div class="label">GitHub Stars</div>
      </div>
      <div class="stat-card">
        <div class="num">{lang}</div>
        <div class="label">Language</div>
      </div>
      <div class="stat-card">
        <div class="num">MIT</div>
        <div class="label">License</div>
      </div>
    </div>

    <div class="bottom-bar">
      <div class="gh-icon">📦</div>
      <div class="repo-name">{name}</div>
    </div>
  </div>
</div>
</body></html>"""


# ── 功能亮点页 ──────────────────────────────────────────────

def features_html(post, repo_info):
    name = repo_info.get("name", "").split("/")[-1]
    features = [
        {"icon": "🗜️", "title": "超高压缩率", "desc": "减少 60-95% 的 Token 消耗，直接省下真金白银的 API 费用"},
        {"icon": "⚡", "title": "确定性压缩", "desc": "同样输入永远同样输出，不依赖额外模型调用，零随机性"},
        {"icon": "🔌", "title": "多种接入方式", "desc": "支持 Python 库、Proxy 代理、MCP 协议，即插即用"},
    ]

    cards_html = ""
    for i, f in enumerate(features):
        cards_html += f"""
    <div class="feature-card">
      <div class="feature-icon">{f['icon']}</div>
      <div class="feature-content">
        <div class="feature-title">{f['title']}</div>
        <div class="feature-desc">{f['desc']}</div>
      </div>
      <div class="feature-num">{str(i+1).zfill(2)}</div>
    </div>"""

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{COMMON_CSS}

body {{
  background: linear-gradient(160deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
  color: #fff;
}}

.deco-circle.c1 {{ width: 300px; height: 300px; background: #ff6b6b; top: 60px; right: -80px; }}
.deco-circle.c2 {{ width: 200px; height: 200px; background: #4ecdc4; bottom: 200px; left: -50px; }}

.section-title {{
  font-size: 56px;
  font-weight: 800;
  margin-bottom: 16px;
  background: linear-gradient(90deg, #ff6b6b, #ffd93d);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}}

.section-sub {{
  font-size: 28px;
  color: rgba(255,255,255,0.5);
  margin-bottom: 56px;
}}

.feature-card {{
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 24px;
  padding: 40px 44px;
  margin-bottom: 32px;
  display: flex;
  align-items: center;
  gap: 32px;
  position: relative;
}}

.feature-icon {{
  font-size: 56px;
  width: 100px;
  height: 100px;
  background: rgba(255,255,255,0.08);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}}

.feature-content {{ flex: 1; }}

.feature-title {{
  font-size: 34px;
  font-weight: 700;
  margin-bottom: 12px;
}}

.feature-desc {{
  font-size: 24px;
  color: rgba(255,255,255,0.65);
  line-height: 1.5;
}}

.feature-num {{
  position: absolute;
  right: 36px;
  top: 32px;
  font-size: 64px;
  font-weight: 900;
  color: rgba(255,255,255,0.06);
}}

.bottom-note {{
  margin-top: auto;
  text-align: center;
  font-size: 24px;
  color: rgba(255,255,255,0.35);
  padding-top: 40px;
}}
</style></head><body>
<div class="page">
  <div class="deco-circle c1"></div>
  <div class="deco-circle c2"></div>

  <div class="content">
    <div class="section-title">核心亮点</div>
    <div class="section-sub">为什么选择 {name}？</div>

    {cards_html}

    <div class="bottom-note">GitHub: {repo_info.get('name', '')}</div>
  </div>
</div>
</body></html>"""


# ── 快速上手页 ──────────────────────────────────────────────

def quickstart_html(post, repo_info):
    name = repo_info.get("name", "").split("/")[-1]
    lang = repo_info.get("language", "Python")

    install_cmd = f"pip install {name}-ai" if lang == "Python" else f"npm install {name}"

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{COMMON_CSS}

body {{
  background: linear-gradient(155deg, #0a0a23 0%, #1b1464 40%, #0d1b3e 100%);
  color: #fff;
}}

.deco-circle.c1 {{ width: 350px; height: 350px; background: #6c5ce7; top: -80px; left: -100px; }}
.deco-circle.c2 {{ width: 220px; height: 220px; background: #00cec9; bottom: -60px; right: -40px; }}

.section-title {{
  font-size: 56px;
  font-weight: 800;
  margin-bottom: 16px;
  background: linear-gradient(90deg, #a29bfe, #6c5ce7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}}

.section-sub {{
  font-size: 28px;
  color: rgba(255,255,255,0.5);
  margin-bottom: 52px;
}}

.step {{
  display: flex;
  gap: 28px;
  margin-bottom: 40px;
  align-items: flex-start;
}}

.step-num {{
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6c5ce7, #a29bfe);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: 800;
  flex-shrink: 0;
}}

.step-body {{
  flex: 1;
  padding-top: 6px;
}}

.step-title {{
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 14px;
}}

.step-desc {{
  font-size: 24px;
  color: rgba(255,255,255,0.6);
  line-height: 1.6;
  margin-bottom: 18px;
}}

.code-block {{
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 16px;
  padding: 22px 30px;
  font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
  font-size: 26px;
  color: #a29bfe;
  display: inline-block;
}}

.tip-box {{
  background: rgba(78, 205, 196, 0.1);
  border: 1px solid rgba(78, 205, 196, 0.25);
  border-radius: 20px;
  padding: 32px 36px;
  margin-top: 20px;
  display: flex;
  gap: 16px;
  align-items: flex-start;
}}

.tip-box .tip-icon {{ font-size: 32px; }}

.tip-box .tip-text {{
  font-size: 24px;
  color: rgba(255,255,255,0.7);
  line-height: 1.6;
}}

.bottom-bar {{
  margin-top: auto;
  text-align: center;
  font-size: 26px;
  color: rgba(255,255,255,0.4);
  padding-top: 36px;
  border-top: 1px solid rgba(255,255,255,0.08);
}}
</style></head><body>
<div class="page">
  <div class="deco-circle c1"></div>
  <div class="deco-circle c2"></div>

  <div class="content">
    <div class="section-title">3 分钟上手</div>
    <div class="section-sub">从安装到跑通，只需三步</div>

    <div class="step">
      <div class="step-num">1</div>
      <div class="step-body">
        <div class="step-title">安装</div>
        <div class="code-block">{install_cmd}</div>
      </div>
    </div>

    <div class="step">
      <div class="step-num">2</div>
      <div class="step-body">
        <div class="step-title">接入你的项目</div>
        <div class="step-desc">支持三种模式：Python 库直接调用、HTTP Proxy 代理、MCP Server 协议接入。根据你的场景选择最合适的方式。</div>
        <div class="code-block">from {name.replace('-', '_')} import compress</div>
      </div>
    </div>

    <div class="step">
      <div class="step-num">3</div>
      <div class="step-body">
        <div class="step-title">享受压缩</div>
        <div class="step-desc">自动将冗长的工具输出、日志、RAG 检索结果压缩后再传给 LLM。Token 消耗立降 60-95%。</div>
      </div>
    </div>

    <div class="tip-box">
      <div class="tip-icon">💡</div>
      <div class="tip-text">本地运行，数据不出服务器。压缩过程确定性，不会引入额外的模型调用成本。</div>
    </div>

    <div class="bottom-bar">🔗 {repo_info.get('url', '')}</div>
  </div>
</div>
</body></html>"""


# ── 主函数 ──────────────────────────────────────────────────

def generate_covers(post, repo_info, date_str=None):
    """生成所有封面图 HTML"""
    if date_str is None:
        from datetime import datetime
        date_str = datetime.now().strftime("%Y-%m-%d")

    ensure_output_dir()

    pages = [
        ("01-cover", "封面图", cover_html(post, repo_info)),
        ("02-features", "功能亮点", features_html(post, repo_info)),
        ("03-quickstart", "快速上手", quickstart_html(post, repo_info)),
    ]

    paths = []
    for filename, label, html in pages:
        filepath = OUTPUT_DIR / f"{date_str}-{filename}.html"
        filepath.write_text(html, encoding="utf-8")
        print(f"[covers] {label}: {filepath}")
        paths.append(filepath)

    return paths


if __name__ == "__main__":
    # 测试
    test_post = {
        "title": "⭐2.5w星！这个开源工具让AI开发成本直降95%",
        "body": "test body",
        "tags": "#AI #开源",
    }
    test_repo = {
        "name": "chopratejas/headroom",
        "description": "Compression layer that shrinks tool outputs before they reach the model",
        "stars": 25900,
        "language": "Python",
        "url": "https://github.com/chopratejas/headroom",
    }
    generate_covers(test_post, test_repo)
