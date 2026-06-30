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

    # 使用场景（支持 string 或 dict 格式）
    scenarios_html = ""
    if scenarios:
        scenarios_items = ""
        for s in scenarios[:4]:
            if isinstance(s, str):
                quote = s
                author = ""
                source = ""
            else:
                quote = s.get("quote", s.get("text", ""))
                author = s.get("author", "")
                source = s.get("source", "")
            source_html = f'  <div class="source">{source}</div>' if source else ""
            author_html = f'  <div class="author">— {author}</div>' if author else ""
            scenarios_items += f"""
            <div class="scenario">
              <div class="quote">"{quote}"</div>
              {author_html}
              {source_html}
            </div>"""
        label = slide.get("scenarios_label", "💬 使用场景")
        scenarios_html = f"""
        <div class="scenarios-section">
          <div class="section-title">{label}</div>
          <div class="scenarios-grid">{scenarios_items}</div>
        </div>"""

    # 使用前后对比（替代 scenarios，二选一）
    compare_html = ""
    compare = slide.get("compare", {})
    if compare and not scenarios_html:
        before = compare.get("before", {})
        after = compare.get("after", {})
        before_items = ""
        after_items = ""
        for it in before.get("items", [])[:3]:
            before_items += f'<div class="cmp-item bad"><span class="cmp-icon">✕</span><span>{it}</span></div>'
        for it in after.get("items", [])[:3]:
            after_items += f'<div class="cmp-item good"><span class="cmp-icon">✓</span><span>{it}</span></div>'
        compare_html = f"""
        <div class="compare-section">
          <div class="compare-col before">
            <div class="compare-label">{before.get('label', 'Before')}</div>
            {before_items}
          </div>
          <div class="compare-col after">
            <div class="compare-label">{after.get('label', 'After')}</div>
            {after_items}
          </div>
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
  gap: 14px;
  overflow: hidden;
}}
.metrics-row {{
  display: flex; gap: 20px;
  padding: 16px 0 0;
  flex-shrink: 0;
}}
.metric {{
  flex: 1;
  background: #fff;
  border-radius: 12px;
  padding: 14px;
  text-align: center;
  border: 1px solid {theme['card_border']};
}}
.metric-value {{
  font-size: 48px;
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
  flex: 1;
}}
.highlight-card {{
  display: flex;
  gap: 16px;
  padding: 16px 20px;
  background: #fff;
  border-radius: 14px;
  border: 1px solid {theme['card_border']};
  flex: 1;
  align-items: center;
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
  padding: 14px 0 0;
  border-top: 1.5px solid {theme['card_border']};
  flex-shrink: 0;
}}
.section-title {{
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 10px;
  color: {theme['text']};
}}
.scenarios-grid {{
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 0 4px;
}}
.scenario {{
  padding: 10px 14px;
  background: #fff;
  border-radius: 12px;
  border: 1px solid {theme['card_border']};
}}
.scenario:last-child {{
  border-bottom: none;
}}
.quote {{
  font-size: 22px;
  font-style: italic;
  color: {theme['text']};
  line-height: 1.5;
  margin-bottom: 4px;
}}
.author {{
  font-size: 17px;
  color: {theme['text_sub']};
  text-align: right;
}}
.source {{
  font-size: 14px;
  color: {theme['accent']};
  text-align: right;
  margin-top: 1px;
}}
/* ── 使用前后对比 ── */
.compare-section {{
  display: flex;
  gap: 0;
  padding: 14px 0 0;
}}
.compare-col {{
  flex: 1;
  padding: 16px 20px;
}}
.compare-col.before {{
  background: #fff0f0;
  border-radius: 14px 0 0 14px;
  border: 2px solid #f5c6c6;
  border-right: none;
}}
.compare-col.after {{
  background: #f0fff4;
  border-radius: 0 14px 14px 0;
  border: 2px solid {theme['accent']};
  border-left: 2px dashed #ccc;
}}
.compare-label {{
  font-size: 22px;
  font-weight: 900;
  margin-bottom: 10px;
  letter-spacing: 1px;
}}
.compare-col.before .compare-label {{ color: #c0392b; }}
.compare-col.after .compare-label {{ color: {theme['accent']}; }}
.cmp-item {{
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 0;
  font-size: 20px;
  font-weight: 500;
  line-height: 1.5;
}}
.cmp-item .cmp-icon {{
  flex-shrink: 0;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 15px;
  font-weight: 900;
  color: #fff;
}}
.cmp-item.bad .cmp-icon {{ background: #e74c3c; }}
.cmp-item.good .cmp-icon {{ background: {theme['accent']}; }}
.cmp-item.bad {{ color: #666; }}
.cmp-item.good {{ color: {theme['text']}; font-weight: 700; }}
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
   {compare_html}
</div>
<div class="footer">
  <span>WHY CHOOSE</span>
  <span>AI TOOLS DAILY</span>
</div>
</body></html>"""


# ── Slide 4: 技术架构 ─────────────────────────────────────

def _render_architecture(slide, theme):
    """技术架构：2×2 网格模块 + 全宽详细说明区 + 技术栈标签"""
    heading = slide.get("heading", "技术架构")
    intro = slide.get("intro", "")
    layers = slide.get("layers", [])
    tech_stack = slide.get("tech_stack", [])
    description = slide.get("description", "")

    # 2×2 架构卡片
    layers_html = ""
    default_icons = ["🏗", "🔀", "🩺", "🤖", "⚙️", "📦"]
    for idx, ly in enumerate(layers[:4]):
        name = ly.get("name", "")
        icon = ly.get("icon", default_icons[idx % len(default_icons)])
        desc = ly.get("desc", "")
        features = ly.get("features", [])
        feat_html = ""
        if features:
            feat_items = "".join(f'<span class="feat-tag">{f}</span>' for f in features[:4])
            feat_html = f'<div class="feat-row">{feat_items}</div>'
        layers_html += f"""
        <div class="layer">
          <div class="layer-header">
            <span class="layer-icon">{icon}</span>
            <span class="layer-name">{name}</span>
          </div>
          <div class="layer-desc">{desc}</div>
          {feat_html}
        </div>"""

    # 全宽详细说明区
    desc_block = ""
    if description:
        desc_block = f"""
        <div class="arch-description">
          <div class="desc-text">{description}</div>
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
  justify-content: center;
  padding: 20px 60px;
  gap: 18px;
  overflow: hidden;
}}
/* ── 2×2 架构网格 ── */
.arch-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}}
.layer {{
  background: #fff;
  border-radius: 16px;
  padding: 20px 24px;
  border: 1.5px solid {theme['card_border']};
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}}
.layer-header {{
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}}
.layer-icon {{
  font-size: 28px;
  line-height: 1;
}}
.layer-name {{
  font-size: 26px;
  font-weight: 900;
  letter-spacing: 0.5px;
}}
.layer-desc {{
  font-size: 19px;
  color: {theme['text_sub']};
  line-height: 1.5;
  margin-bottom: 12px;
}}
.feat-row {{
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}}
.feat-tag {{
  background: {theme['bg']};
  border-radius: 8px;
  padding: 5px 14px;
  font-size: 17px;
  color: {theme['text']};
  font-weight: 600;
}}
/* ── 全宽详细说明区 ── */
.arch-description {{
  background: {theme['bg']};
  border: 1.5px solid {theme['card_border']};
  border-radius: 16px;
  padding: 20px 28px;
}}
.desc-text {{
  font-size: 22px;
  color: {theme['text']};
  line-height: 1.7;
  font-weight: 400;
}}
/* ── 技术栈标签 ── */
.tags-row {{
  display: flex; flex-wrap: wrap; gap: 10px;
}}
.tag {{
  background: #fff; border: 1px solid {theme['card_border']};
  border-radius: 10px; padding: 8px 16px;
  font-size: 20px; color: {theme['text']}; font-weight: 600;
}}
.footer {{
  padding: 18px 60px;
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
  <div class="arch-grid">{layers_html}</div>
  {desc_block}
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
  flex: 1; padding: 14px 60px;
  display: flex; flex-direction: column; gap: 16px;
  overflow: hidden;
}}
/* ── 步骤合并卡片 ── */
.steps-box {{
  background: #fff;
  border-radius: 16px;
  border: 1.5px solid {theme['card_border']};
  padding: 8px 0;
  flex-shrink: 0;
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
  flex: 1;
  display: flex;
  flex-direction: column;
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
.terminal-body {{
  padding: 20px 24px;
  flex: 1;
  display: flex;
  align-items: center;
}}
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
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
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

    # ── 数据复查 ──
    review_issues = review_slides(slides_data, theme)
    if review_issues:
        print("[slide_gen] ⚠️  复查发现以下问题：")
        for ri in review_issues:
            print(f"  Slide {ri['index']+1} ({ri['type']}):")
            for issue in ri["issues"]:
                print(f"    - {issue}")
        print("[slide_gen] 将继续生成，但请检查上述问题。")
    else:
        print("[slide_gen] ✅ 数据复查通过")

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


# ── 复查机制：程序化检测 HTML 内容完整性和留白 ──────────────

def review_slides(slides_data: list, theme: dict) -> list[dict]:
    """检查每页幻灯片的数据完整性，返回不合格项列表。

    检查规则：
    1. 各区块文本是否为空或过短
    2. 列表类字段是否有足够条目
    3. 占位/默认文本检测

    Returns:
        list of {index, type, issues: [str]}
    """
    results = []
    MIN_TEXT_LEN = 8       # 最小有效文本长度
    MIN_ITEMS = 2           # 列表最少条目数
    MIN_FEATURE_DESC = 15   # 功能描述最少字符

    for i, slide in enumerate(slides_data):
        issues = []
        stype = slide.get("type", "unknown")

        # ── 通用检查 ──
        heading = slide.get("heading", "")
        if not heading or len(heading.strip()) < 2:
            issues.append("heading 为空或过短")

        intro = slide.get("intro", slide.get("subheading", ""))
        if not intro or len(intro.strip()) < MIN_TEXT_LEN:
            issues.append("intro/subheading 为空或过短")

        # ── 按类型检查 ──
        if stype == "cover":
            sub = slide.get("subheading", "")
            if not sub or len(sub.strip()) < MIN_TEXT_LEN:
                issues.append("封面 subheading 为空")

        elif stype == "features":
            items = slide.get("items", [])
            if len(items) < MIN_ITEMS:
                issues.append(f"features items 不足 ({len(items)}/{MIN_ITEMS})")
            for j, item in enumerate(items):
                desc = item.get("desc", "")
                if not desc or len(desc.strip()) < MIN_FEATURE_DESC:
                    issues.append(f"items[{j}] desc 过短: '{desc[:20]}'")
            stats = slide.get("stats", [])
            if len(stats) < 2:
                issues.append("stats 数据不足")

        elif stype == "highlights":
            items = slide.get("items", [])
            if len(items) < MIN_ITEMS:
                issues.append(f"highlights items 不足 ({len(items)}/{MIN_ITEMS})")
            # 检查 scenarios 或 compare 至少有一个有内容
            scenarios = slide.get("scenarios", [])
            compare = slide.get("compare", {})
            if not scenarios and not compare:
                issues.append("scenarios 和 compare 都为空，底部区域会留白")
            elif scenarios:
                for j, s in enumerate(scenarios):
                    if isinstance(s, str):
                        q = s
                    else:
                        q = s.get("quote", s.get("text", ""))
                    if not q or len(q.strip()) < MIN_TEXT_LEN:
                        issues.append(f"scenarios[{j}] 内容为空")
            elif compare:
                b_items = compare.get("before", {}).get("items", [])
                a_items = compare.get("after", {}).get("items", [])
                if len(b_items) < 2 or len(a_items) < 2:
                    issues.append("compare 对比项不足 (需各至少 2 项)")

        elif stype == "architecture":
            layers = slide.get("layers", [])
            if len(layers) < 2:
                issues.append(f"layers 不足 ({len(layers)}/2)")
            for j, ly in enumerate(layers):
                name = ly.get("name", ly.get("label", ""))
                desc = ly.get("desc", "")
                features = ly.get("features", [])
                if not name:
                    issues.append(f"layers[{j}] name 为空")
                if not desc or len(desc.strip()) < MIN_TEXT_LEN:
                    issues.append(f"layers[{j}] desc 过短")
                if len(features) < 2:
                    issues.append(f"layers[{j}] features 不足 ({len(features)}/2)，留白风险")
            description = slide.get("description", "")
            if not description or len(description.strip()) < 20:
                issues.append("description 详细说明区为空或过短")

        elif stype == "usage":
            steps = slide.get("steps", [])
            if len(steps) < 3:
                issues.append(f"steps 不足 ({len(steps)}/3)")
            tips = slide.get("tips", [])
            if len(tips) < 2:
                issues.append(f"tips 不足 ({len(tips)}/2)")

        if issues:
            results.append({"index": i, "type": stype, "issues": issues})

    return results
