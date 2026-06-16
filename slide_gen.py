"""
小红书项目介绍图生成器 — Apple 简约风格
5 张竖版图（1080×1440）：封面 / 功能 / 亮点 / 架构 / 使用+GitHub
"""

import sys
import json
import base64
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# ── Apple 银灰 Silver 主题 ────────────────────────────────

THEME = {
    "name": "银灰 Silver",
    "bg": "#f5f5f7",
    "bg_sub": "#e8e8ed",
    "text": "#1d1d1f",
    "text_sub": "#86868b",
    "accent": "#0071e3",
    "card_bg": "#ffffff",
    "card_border": "#d2d2d7",
}

# ── Google Fonts ──────────────────────────────────────────

FONT_LINK = '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&family=Noto+Serif+SC:wght@400;700;900&display=swap" rel="stylesheet">'


def _fetch_avatar_data_uri(url, size=200):
    """下载 GitHub 头像转为 base64 data URI，避免外部图片加载失败"""
    try:
        req = urllib.request.Request(url + f"?size={size}", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = resp.read()
            b64 = base64.b64encode(data).decode()
            return f"data:image/png;base64,{b64}"
    except Exception as e:
        print(f"[slide_gen] 头像下载失败: {e}")
        return ""

BASE_CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  width: 1080px; height: 1440px;
  font-family: 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  display: flex; flex-direction: column;
  overflow: hidden; position: relative;
  -webkit-font-smoothing: antialiased;
}
"""


# ── Slide 1: 封面 ─────────────────────────────────────────

def _render_cover(slide, theme):
    """封面：刊头 + Logo + 项目名 + 一句话介绍 + 标签"""
    heading = slide.get("heading", "项目名称")
    sub = slide.get("subheading", "")
    avatar_url = slide.get("avatar_url", "")
    logo_emoji = slide.get("logo_emoji", "")
    star = slide.get("star_text", "")
    lang = slide.get("lang_text", "")

    # 优先级：截图 > emoji > 白底黑字项目名
    fallback_html = f'<div class="emoji-logo">{logo_emoji}</div>' if logo_emoji else f'<div class="initials">{heading[:2].upper()}</div>'
    if avatar_url:
        avatar_html = f'<img src="{avatar_url}?size=200" onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'flex\'" /><div style="display:none;">{fallback_html}</div>'
    elif logo_emoji:
        avatar_html = f'<div class="emoji-logo">{logo_emoji}</div>'
    else:
        avatar_html = f'<div class="initials">{heading[:2].upper()}</div>'

    badges_list = []
    if star:
        badges_list.append(f'<span class="badge">⭐ {star} Stars</span>')
    if lang:
        badges_list.append(f'<span class="badge">💻 {lang}</span>')
    # 只有 MIT License 时不显示
    # badges_list.append('<span class="badge">MIT License</span>')

    badges_html = ""
    if badges_list:
        badges_inner = "".join(badges_list)
        badges_html = f'<div class="badges">{badges_inner}</div>'

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">{FONT_LINK}<style>
{BASE_CSS}
body {{
  background: {theme['bg']}; color: {theme['text']};
  display: flex; flex-direction: column;
}}
.masthead {{
  display: flex; justify-content: space-between; align-items: center;
  padding: 40px 60px 20px;
  border-bottom: 1.5px solid {theme['card_border']};
}}
.masthead .issue {{ font-size: 14px; color: {theme['text_sub']}; letter-spacing: 4px; text-transform: uppercase; }}
.masthead .date {{ font-size: 14px; color: {theme['text_sub']}; letter-spacing: 2px; }}
.main {{
  flex: 1; display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  padding: 0 80px;
}}
.logo-wrapper {{
  width: 260px; height: 260px; border-radius: 60px;
  background: {theme['text']};
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 56px;
  box-shadow: 0 20px 80px rgba(0,0,0,0.12);
  overflow: hidden;
}}
.logo-wrapper img {{ width: 100%; height: 100%; object-fit: cover; }}
.logo-wrapper .initials {{ font-size: 96px; font-weight: 900; color: #fff; }}
.logo-wrapper .emoji-logo {{ font-size: 120px; line-height: 1; background: #fff; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; }}
.name {{
  font-family: 'Noto Serif SC', serif;
  font-size: 84px; font-weight: 900;
  letter-spacing: -2px; margin-bottom: 24px;
  text-align: center;
}}
.subtitle {{
  font-size: 28px; color: {theme['text_sub']};
  font-weight: 300; text-align: center;
  max-width: 720px; line-height: 1.6; margin-bottom: 52px;
}}
.divider {{ width: 60px; height: 3px; background: {theme['text']}; margin-bottom: 52px; }}
.badges {{ display: flex; gap: 14px; flex-wrap: wrap; justify-content: center; }}
.badge {{
  background: #fff; border: 1.5px solid {theme['card_border']};
  border-radius: 100px; padding: 14px 32px;
  font-size: 22px; color: {theme['text_sub']}; letter-spacing: 1px;
}}
.footer {{
  padding: 32px 60px;
  border-top: 1.5px solid {theme['card_border']};
  display: flex; justify-content: space-between;
  font-size: 13px; color: {theme['text_sub']}; letter-spacing: 2px;
}}
</style></head><body>
<div class="masthead">
  <div class="issue">AI TOOLS DAILY</div>
  <div class="date">NO. 001 · 每天认识一个 AI 工具</div>
</div>
<div class="main">
  <div class="logo-wrapper">{avatar_html}</div>
  <div class="name">{heading}</div>
   <div class="subtitle">{sub}</div>
  {badges_html}
</div>
<div class="footer">
  <span>COVER STORY</span>
  <span>1 / 5</span>
</div>
</body></html>"""


# ── Slide 2: 功能介绍 ─────────────────────────────────────

def _render_features(slide, theme):
    """功能介绍：双栏网格 + emoji + 总结区"""
    heading = slide.get("heading", "产品功能")
    intro = slide.get("intro", "")
    items = slide.get("items", [])
    project_name = slide.get("project_name", "")
    summary_text = slide.get("summary_text", "")
    stats = slide.get("stats", [])

    grid_items = ""
    for it in items[:4]:
        icon = it.get("icon", "🔹")
        title = it.get("title", "")
        desc = it.get("desc", "")
        detail = it.get("detail", "")
        detail_html = f'<br>{detail}' if detail else ''
        grid_items += f"""
        <div class="item">
          <span class="emoji-line">{icon}</span>
          <p><b>{title}</b> — {desc}{detail_html}</p>
        </div>"""

    stats_items = ""
    for st in stats[:4]:
        stats_items += f'<div class="stat"><span class="stat-num">{st.get("value","")}</span><span class="stat-label">{st.get("label","")}</span></div>'

    # 构建总结区 HTML
    project_html = f'<span class="project-name">{project_name}</span> ' if project_name else ''
    summary_html = f"{project_html}{summary_text}"

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">{FONT_LINK}<style>
{BASE_CSS}
body {{
  background: {theme['bg']}; color: {theme['text']};
}}
.top-bar {{
  display: flex; justify-content: space-between; align-items: center;
  padding: 40px 60px 16px;
  font-size: 13px; color: {theme['text_sub']}; letter-spacing: 3px; text-transform: uppercase;
  flex-shrink: 0;
}}
h2 {{
  font-family: 'Noto Serif SC', serif;
  font-size: 64px; font-weight: 900;
  letter-spacing: -2px;
  padding: 0 60px 8px;
  flex-shrink: 0;
}}
.lead {{
  font-size: 28px; color: {theme['text_sub']}; font-weight: 300;
  padding: 0 60px 24px; line-height: 1.6;
  border-bottom: 1.5px solid {theme['card_border']};
  margin: 0 60px;
  flex-shrink: 0;
}}
.grid {{
  flex: 1; padding: 28px 60px 16px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 36px 40px;
}}
.grid .item {{
  display: flex; flex-direction: column; justify-content: flex-start;
  font-size: 28px; line-height: 1.6;
}}
.grid .item .emoji-line {{ font-size: 24px; margin-bottom: 8px; display: block; }}
.grid .item b {{ font-weight: 700; }}
.grid .item p {{ margin: 0; }}
.summary {{
  padding: 24px 60px 20px;
  border-top: 1.5px solid {theme['card_border']};
  flex-shrink: 0;
}}
.summary-text {{
  font-size: 28px; line-height: 1.7; color: {theme['text']};
  margin-bottom: 20px;
}}
.summary-text .project-name {{
  font-size: 32px; font-weight: 900;
}}
.summary-stats {{
  display: flex; gap: 0;
}}
.summary-stats .stat {{
  flex: 1; text-align: center;
  border-right: 1.5px solid {theme['card_border']};
}}
.summary-stats .stat:last-child {{ border-right: none; }}
.summary-stats .stat-num {{
  display: block;
  font-size: 36px; font-weight: 900; color: {theme['text']};
  line-height: 1.2;
}}
.summary-stats .stat-label {{
  display: block;
  font-size: 13px; color: {theme['text_sub']};
  margin-top: 4px;
}}
.footer {{
  padding: 24px 60px;
  border-top: 1.5px solid {theme['card_border']};
  display: flex; justify-content: space-between;
  font-size: 13px; color: {theme['text_sub']}; letter-spacing: 2px;
  flex-shrink: 0;
}}
</style></head><body>
<div class="top-bar">
  <span>FEATURE</span>
  <span>2 / 5</span>
</div>
<h2>{heading}</h2>
<div class="lead">{intro}</div>
<div class="grid">{grid_items}</div>
<div class="summary">
  <div class="summary-text">{project_html}{summary_text}</div>
  <div class="summary-stats">
    {stats_items}
  </div>
</div>
<div class="footer">
  <span>FUNCTIONS</span>
  <span>AI TOOLS DAILY</span>
</div>
</body></html>"""


# ── Slide 3: 核心亮点 ─────────────────────────────────────

def _render_highlights(slide, theme):
    """核心亮点：数据指标 + 亮点卡片 + 使用场景"""
    heading = slide.get("heading", "核心亮点")
    intro = slide.get("intro", "")
    items = slide.get("items", [])
    metrics = slide.get("metrics", [])
    scenarios = slide.get("scenarios", [])

    # 数据指标卡片
    metrics_html = ""
    if metrics:
        metrics_items = ""
        for m in metrics[:4]:
            metrics_items += f"""
            <div class="metric">
              <div class="metric-value">{m['value']}</div>
              <div class="metric-label">{m['label']}</div>
            </div>"""
        metrics_html = f'<div class="metrics-row">{metrics_items}</div>'

    # 亮点卡片
    cards_html = ""
    for it in items[:4]:
        icon = it.get("icon", "✦")
        title = it.get("title", "")
        desc = it.get("desc", "")
        cards_html += f"""
        <div class="highlight-card">
          <div class="card-icon">{icon}</div>
          <div class="card-content">
            <div class="card-title">{title}</div>
            <div class="card-desc">{desc}</div>
          </div>
        </div>"""

    # 使用场景
    scenarios_html = ""
    if scenarios:
        scenarios_items = ""
        for s in scenarios[:2]:
            quote = s.get("quote", "")
            author = s.get("author", "")
            scenarios_items += f"""
            <div class="scenario">
              <div class="quote">"{quote}"</div>
              <div class="author">— {author}</div>
            </div>"""
        scenarios_html = f"""
        <div class="scenarios-section">
          <div class="section-title">💬 用户怎么说</div>
          <div class="scenarios-grid">{scenarios_items}</div>
        </div>"""

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">{FONT_LINK}<style>
{BASE_CSS}
body {{
  background: {theme['bg']}; color: {theme['text']};
  display: flex; flex-direction: column;
  overflow: hidden;
}}
.top-bar {{
  display: flex; justify-content: space-between; align-items: center;
  padding: 40px 60px 16px;
  font-size: 13px; color: {theme['text_sub']}; letter-spacing: 3px; text-transform: uppercase;
}}
h2 {{
  font-family: 'Noto Serif SC', serif;
  font-size: 64px; font-weight: 900;
  letter-spacing: -2px;
  padding: 0 60px 8px;
}}
.lead {{
  font-size: 26px; color: {theme['text_sub']}; font-weight: 300;
  padding: 0 60px 20px; line-height: 1.6;
  border-bottom: 1.5px solid {theme['card_border']};
  margin: 0 60px;
}}
.content {{
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 0 60px;
  overflow: hidden;
}}
.metrics-row {{
  display: flex; gap: 20px;
  padding: 20px 0 16px;
}}
.metric {{
  flex: 1;
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  text-align: center;
  border: 1px solid {theme['card_border']};
}}
.metric-value {{
  font-size: 52px;
  font-weight: 900;
  color: {theme['accent']};
  margin-bottom: 4px;
}}
.metric-label {{
  font-size: 18px;
  color: {theme['text_sub']};
}}
.cards-section {{
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}}
.highlight-card {{
  display: flex;
  gap: 16px;
  padding: 14px 20px;
  background: #fff;
  border-radius: 14px;
  border: 1px solid {theme['card_border']};
}}
.card-icon {{
  font-size: 28px;
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: {theme['bg']};
  border-radius: 12px;
}}
.card-content {{
  flex: 1;
}}
.card-title {{
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 4px;
}}
.card-desc {{
  font-size: 20px;
  color: {theme['text_sub']};
  line-height: 1.5;
}}
.scenarios-section {{
  padding: 16px 0 0;
  border-top: 1.5px solid {theme['card_border']};
}}
.section-title {{
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 12px;
  color: {theme['text']};
}}
.scenarios-grid {{
  display: flex;
  gap: 16px;
}}
.scenario {{
  flex: 1;
  background: #fff;
  border-radius: 12px;
  padding: 14px 16px;
  border-left: 3px solid {theme['accent']};
}}
.quote {{
  font-size: 20px;
  font-style: italic;
  color: {theme['text']};
  line-height: 1.5;
  margin-bottom: 6px;
}}
.author {{
  font-size: 18px;
  color: {theme['text_sub']};
  text-align: right;
}}
.footer {{
  padding: 20px 60px;
  border-top: 1.5px solid {theme['card_border']};
  display: flex; justify-content: space-between;
  font-size: 13px; color: {theme['text_sub']}; letter-spacing: 2px;
}}
</style></head><body>
<div class="top-bar">
  <span>HIGHLIGHTS</span>
  <span>3 / 5</span>
</div>
<h2>{heading}</h2>
<div class="lead">{intro}</div>
<div class="content">
  {metrics_html}
  <div class="cards-section">{cards_html}</div>
  {scenarios_html}
</div>
<div class="footer">
  <span>WHY CHOOSE</span>
  <span>AI TOOLS DAILY</span>
</div>
</body></html>"""


# ── Slide 4: 技术架构 ─────────────────────────────────────

def _render_architecture(slide, theme):
    """技术架构：两列对比 + 从上到下流程 + 冲击力"""
    heading = slide.get("heading", "技术架构")
    intro = slide.get("intro", "")
    layers = slide.get("layers", [])
    tech_stack = slide.get("tech_stack", [])
    flow_steps = slide.get("flow_steps", [])
    compare = slide.get("compare", {})

    # 流程图
    flow_html = ""
    if flow_steps:
        flow_items = ""
        for i, step in enumerate(flow_steps[:4]):
            flow_items += f'<div class="flow-step">{step}</div>'
            if i < len(flow_steps) - 1:
                flow_items += '<div class="flow-arrow"><span class="arrow-line"></span><span class="arrow-head">›</span></div>'
        flow_html = f'<div class="flow-section">{flow_items}</div>'

    # 两列对比数据
    before = compare.get("before", {})
    after = compare.get("after", {})
    before_items_html = ""
    after_items_html = ""
    for it in before.get("items", []):
        before_items_html += f'<div class="cmp-item bad"><span class="cmp-icon">✕</span><span>{it}</span></div>'
    for it in after.get("items", []):
        after_items_html += f'<div class="cmp-item good"><span class="cmp-icon">✓</span><span>{it}</span></div>'

    # 架构卡片（精简描述，突出名称）
    layers_html = ""
    for ly in layers[:4]:
        name = ly.get("name", "")
        desc = ly.get("desc", "")
        features = ly.get("features", [])
        feat_html = ""
        if features:
            feat_items = "".join(f'<span class="feat-tag">{f}</span>' for f in features[:4])
            feat_html = f'<div class="feat-row">{feat_items}</div>'
        layers_html += f"""
        <div class="layer">
          <div class="layer-name">{name}</div>
          <div class="layer-desc">{desc}</div>
          {feat_html}
        </div>"""

    # 技术栈标签
    tags = ""
    for t in tech_stack[:8]:
        tags += f'<span class="tag">{t}</span>'

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">{FONT_LINK}<style>
{BASE_CSS}
body {{
  background: {theme['bg']}; color: {theme['text']};
  display: flex; flex-direction: column;
  overflow: hidden;
}}
.top-bar {{
  display: flex; justify-content: space-between; align-items: center;
  padding: 40px 60px 16px;
  font-size: 13px; color: {theme['text_sub']}; letter-spacing: 3px; text-transform: uppercase;
}}
h2 {{
  font-family: 'Noto Serif SC', serif;
  font-size: 68px; font-weight: 900;
  letter-spacing: -2px;
  padding: 0 60px 6px;
}}
.lead {{
  font-size: 28px; color: {theme['text_sub']}; font-weight: 300;
  padding: 0 60px 18px; line-height: 1.6;
  border-bottom: 1.5px solid {theme['card_border']};
  margin: 0 60px;
}}
.content {{
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 0 60px;
  overflow: hidden;
}}
/* ── 流程图 ── */
.flow-section {{
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 18px 0 14px;
}}
.flow-step {{
  background: #fff;
  border-radius: 14px;
  padding: 14px 28px;
  font-weight: 800;
  font-size: 24px;
  border: 1.5px solid {theme['card_border']};
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}}
.flow-arrow {{
  display: flex;
  align-items: center;
  gap: 2px;
  color: {theme['accent']};
}}
.arrow-line {{
  display: inline-block;
  width: 28px;
  height: 2px;
  background: {theme['accent']};
}}
.arrow-head {{
  font-size: 30px;
  font-weight: 700;
  line-height: 1;
}}
/* ── 两列对比 ── */
.compare-section {{
  display: flex;
  gap: 0;
  padding: 0 0 14px;
}}
.compare-col {{
  flex: 1;
  padding: 20px 24px;
}}
.compare-col.before {{
  background: #fff0f0;
  border-radius: 16px 0 0 16px;
  border: 2px solid #f5c6c6;
  border-right: none;
}}
.compare-col.after {{
  background: #f0fff4;
  border-radius: 0 16px 16px 0;
  border: 2px solid {theme['accent']};
  border-left: 2px dashed #ccc;
}}
.compare-label {{
  font-size: 24px;
  font-weight: 900;
  margin-bottom: 12px;
  letter-spacing: 1px;
}}
.compare-col.before .compare-label {{ color: #c0392b; }}
.compare-col.after .compare-label {{ color: {theme['accent']}; }}
.cmp-item {{
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 0;
  font-size: 22px;
  font-weight: 500;
  line-height: 1.5;
}}
.cmp-item .cmp-icon {{
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 900;
  color: #fff;
}}
.cmp-item.bad .cmp-icon {{ background: #e74c3c; }}
.cmp-item.good .cmp-icon {{ background: {theme['accent']}; }}
.cmp-item.bad {{ color: #666; }}
.cmp-item.good {{ color: {theme['text']}; font-weight: 700; }}
/* ── 架构卡片 2×2 ── */
.arch-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}}
.layer {{
  background: #fff;
  border-radius: 14px;
  padding: 18px 22px;
  border: 1px solid {theme['card_border']};
}}
.layer-name {{
  font-size: 24px;
  font-weight: 800;
  margin-bottom: 6px;
}}
.layer-desc {{
  font-size: 20px;
  color: {theme['text_sub']};
  line-height: 1.5;
  margin-bottom: 10px;
}}
.feat-row {{
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}}
.feat-tag {{
  background: {theme['bg']};
  border-radius: 8px;
  padding: 5px 12px;
  font-size: 17px;
  color: {theme['text']};
  font-weight: 500;
}}
/* ── 技术栈 ── */
.tags-row {{
  display: flex; flex-wrap: wrap; gap: 10px;
  padding: 14px 0 0;
  border-top: 1.5px solid {theme['card_border']};
}}
.tag {{
  background: #fff; border: 1px solid {theme['card_border']};
  border-radius: 10px; padding: 8px 16px;
  font-size: 20px; color: {theme['text']}; font-weight: 600;
}}
.footer {{
  padding: 20px 60px;
  border-top: 1.5px solid {theme['card_border']};
  display: flex; justify-content: space-between;
  font-size: 13px; color: {theme['text_sub']}; letter-spacing: 2px;
}}
</style></head><body>
<div class="top-bar">
  <span>ARCHITECTURE</span>
  <span>4 / 5</span>
</div>
<h2>{heading}</h2>
<div class="lead">{intro}</div>
<div class="content">
  {flow_html}
  <div class="compare-section">
    <div class="compare-col before">
      <div class="compare-label">{before.get('label', 'Before')}</div>
      {before_items_html}
    </div>
    <div class="compare-col after">
      <div class="compare-label">{after.get('label', 'After')}</div>
      {after_items_html}
    </div>
  </div>
  <div class="arch-grid">{layers_html}</div>
  <div class="tags-row">{tags}</div>
</div>
<div class="footer">
  <span>HOW IT WORKS</span>
  <span>AI TOOLS DAILY</span>
</div>
</body></html>"""


# ── Slide 5: 使用方式 + GitHub ─────────────────────────────

def _render_usage(slide, theme):
    """使用方式 — 安装向导风格：终端窗口 + 进度条 + 步骤卡片"""
    heading = slide.get("heading", "快速上手")
    steps = slide.get("steps", [])
    github = slide.get("github", {})
    code_example = slide.get("code_example", {})
    tips = slide.get("tips", [])

    total = len(steps) if steps else 1

    # 步骤 — 合并为一个白色大卡片，内部用编号+分隔线
    steps_inner = ""
    for i, s in enumerate(steps[:4], 1):
        cmd = s.get("cmd", "") if isinstance(s, dict) else str(s)
        desc = s.get("desc", "") if isinstance(s, dict) else ""
        border = f'border-bottom:1.5px solid {theme["card_border"]};' if i < total else ''
        steps_inner += f"""
        <div class="step-row" style="{border}">
          <div class="step-num">{i}</div>
          <div class="step-content">
            <div class="step-desc">{desc}</div>
            <div class="step-cmd"><span class="prompt">$</span> {cmd}</div>
          </div>
        </div>"""
    steps_html = f'<div class="steps-box">{steps_inner}</div>'

    # 终端代码块 — 独立深色区块
    code_html = ""
    if code_example:
        title = code_example.get("title", "使用示例")
        code = code_example.get("code", "")
        code_html = f"""
        <div class="terminal">
          <div class="terminal-bar">
            <span class="t-dot red"></span><span class="t-dot yellow"></span><span class="t-dot green"></span>
            <span class="t-title">{title}</span>
          </div>
          <div class="terminal-body"><pre>{code}</pre></div>
        </div>"""

    # 最佳实践 + GitHub 合并为一个白色大卡片 — 项目名称在上
    bottom_inner = ""
    gh = github
    if gh.get("name"):
        bottom_inner += f"""
        <div class="gh-row">
          <span class="gh-icon">🐙</span>
          <span class="gh-name">{gh.get('name','')}</span>
          <span class="gh-stars">⭐ {gh.get('stars','')}</span>
          <span class="gh-stars">🍴 {gh.get('forks','')}</span>
        </div>
        <div class="gh-url">{gh.get('url','')}</div>"""
    if tips:
        for tip in tips[:3]:
            bottom_inner += f'<div class="tip-line">{tip}</div>'
    bottom_html = f'<div class="bottom-box">{bottom_inner}</div>' if bottom_inner else ""

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">{FONT_LINK}<style>
{BASE_CSS}
body {{
  background: {theme['bg']}; color: {theme['text']};
  display: flex; flex-direction: column;
  overflow: hidden;
}}
.top-bar {{
  display: flex; justify-content: space-between; align-items: center;
  padding: 40px 60px 12px;
  font-size: 14px; color: {theme['text_sub']}; letter-spacing: 3px; text-transform: uppercase;
}}
h2 {{
  font-family: 'Noto Serif SC', serif;
  font-size: 76px; font-weight: 900;
  letter-spacing: -2px;
  padding: 0 60px 20px;
}}
.content {{
  flex: 1; padding: 0 60px;
  display: flex; flex-direction: column; gap: 30px;
  overflow: hidden;
}}
/* ── 步骤合并卡片 ── */
.steps-box {{
  background: #fff;
  border-radius: 16px;
  border: 1.5px solid {theme['card_border']};
  padding: 8px 0;
}}
.step-row {{
  display: flex;
  align-items: flex-start;
  gap: 18px;
  padding: 18px 28px;
}}
.step-num {{
  width: 44px; height: 44px; border-radius: 50%;
  background: {theme['text']}; color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-size: 24px; font-weight: 900; flex-shrink: 0;
  margin-top: 2px;
}}
.step-content {{ flex: 1; }}
.step-desc {{
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 4px;
}}
.step-cmd {{
  font-family: 'SF Mono', 'Menlo', 'Courier New', monospace;
  font-size: 24px;
  color: {theme['text_sub']};
}}
.prompt {{
  color: {theme['accent']};
  font-weight: 900;
  margin-right: 4px;
}}
/* ── 终端 ── */
.terminal {{
  border-radius: 14px;
  overflow: hidden;
  background: #1e1e1e;
}}
.terminal-bar {{
  display: flex; align-items: center; gap: 8px;
  padding: 12px 18px; background: #2d2d2d;
}}
.t-dot {{ width: 14px; height: 14px; border-radius: 50%; }}
.t-dot.red {{ background: #ff5f57; }}
.t-dot.yellow {{ background: #febc2e; }}
.t-dot.green {{ background: #28c840; }}
.t-title {{ color: #888; font-size: 14px; margin-left: 8px; font-family: 'SF Mono', monospace; }}
.terminal-body {{ padding: 20px 24px; }}
.terminal-body pre {{
  margin: 0;
  font-family: 'SF Mono', 'Menlo', 'Courier New', monospace;
  font-size: 22px; color: #d4d4d4; line-height: 1.7; white-space: pre-wrap;
}}
/* ── 底部合并卡片 ── */
.bottom-box {{
  background: #fff;
  border-radius: 16px;
  border: 1.5px solid {theme['card_border']};
  padding: 20px 28px;
}}
.tip-line {{
  font-size: 26px;
  color: {theme['text']};
  font-weight: 500;
  padding: 10px 0;
  line-height: 1.5;
  border-bottom: 1px solid {theme['bg']};
}}
.tip-line:last-of-type {{ border-bottom: none; }}
.gh-row {{
  display: flex; align-items: center; gap: 14px;
  padding-top: 14px;
  border-top: 1.5px solid {theme['card_border']};
  margin-top: 6px;
}}
.gh-icon {{ font-size: 36px; }}
.gh-name {{ font-size: 28px; font-weight: 900; flex: 1; }}
.gh-stars {{ font-size: 26px; font-weight: 700; color: {theme['accent']}; }}
.gh-url {{
  font-size: 20px; color: {theme['text_sub']};
  font-family: 'SF Mono', monospace;
  padding-top: 8px;
}}
.footer {{
  padding: 18px 60px;
  border-top: 1.5px solid {theme['card_border']};
  display: flex; justify-content: space-between;
  font-size: 14px; color: {theme['text_sub']}; letter-spacing: 2px;
}}
</style></head><body>
<div class="top-bar">
  <span>GETTING STARTED</span>
  <span>5 / 5</span>
</div>
<h2>{heading}</h2>
<div class="content">
  {bottom_html}
  {steps_html}
  {code_html}
</div>
<div class="footer">
  <span>QUICK START</span>
  <span>AI TOOLS DAILY</span>
</div>
</body></html>"""


# ── 模板分发 ──────────────────────────────────────────────

TEMPLATES = {
    "cover": _render_cover,
    "features": _render_features,
    "highlights": _render_highlights,
    "architecture": _render_architecture,
    "usage": _render_usage,
}


def render_slide_html(slide, theme):
    slide_type = slide.get("type", "cover")
    renderer = TEMPLATES.get(slide_type, _render_cover)
    return renderer(slide, theme)


# ── 截图 ─────────────────────────────────────────────────

def screenshot_html(html_str, output_path):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1080, "height": 1440})
        page.set_content(html_str, wait_until="networkidle")
        page.screenshot(path=str(output_path))
        browser.close()


def generate_slides(slides_data, output_dir, **_ignored):
    """生成全部幻灯片图片"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    theme = THEME
    print(f"[slide_gen] 主题: {theme['name']}")

    # 预处理：将 GitHub 头像 URL 转为 base64 data URI
    for slide in slides_data:
        if slide.get("type") == "cover" and slide.get("avatar_url"):
            url = slide["avatar_url"]
            if not url.startswith("data:"):
                data_uri = _fetch_avatar_data_uri(url)
                if data_uri:
                    slide["avatar_url"] = data_uri

    saved = []
    for i, slide in enumerate(slides_data):
        slide_type = slide.get("type", "cover")
        html_str = render_slide_html(slide, theme)

        png_path = output_dir / f"slide_{i+1}_{slide_type}.png"
        try:
            screenshot_html(html_str, png_path)
            print(f"[slide_gen] 截图完成: {png_path.name}")
            saved.append(png_path)
        except Exception as e:
            html_path = output_dir / f"slide_{i+1}_{slide_type}.html"
            html_path.write_text(html_str, encoding="utf-8")
            print(f"[slide_gen] 截图失败({e})，已保存 HTML: {html_path.name}")
            saved.append(html_path)

    return saved
