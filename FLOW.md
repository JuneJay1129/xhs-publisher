# xhs-publisher 项目架构 & 流程文档

> 最后更新：2026-06-16

---

## 一、今日需求变更汇总

### 图片生成
1. **银灰主题**（Silver）— 替代原来的5种亮色主题，银灰渐变背景 + 黑色文字 + 翡翠绿强调色
2. **5页结构固定**：Cover → Features → Highlights → Architecture → Usage
3. **内容必须饱满** — 留白不够时宁可加大字体、加粗内容，不留大面积空白
4. **内容区块不要过度分割** — 倾向合并为少数几个大 div，不要6个独立小卡片
5. **字体加大加粗** — 正文 28px+，标题 68-76px，突出优势点用加粗+加大
6. **从上到下的流程感** — 如 Architecture 用两列对比（❌ vs ✅）而非6个独立 div
7. **封面无黑线** — 去掉项目介绍和标签之间的分割线
8. **MIT License 不单独显示** — 如果只有 MIT License 一个标签则不渲染
9. **图5（Usage）**：底部卡片移到顶部，项目名称在最上面，建议在下面；div 间距加大

### 文案生成
1. **结尾不要互动引导语** — 不加"评论区聊聊"之类的话，以项目地址结尾即可

---

## 二、当前项目结构

```
xhs-publisher/
├── main.py              # CLI 入口（scrape/generate/publish/all）
├── config.json          # API key（gitignore）
├── config.example.json  # 配置模板
├── scraper.py           # GitHub Trending 采集
├── generator.py         # LLM 文案生成（MiMo API）
├── prompts.py           # 文案 prompt 构建（5角色 × 5风格 × 3结构 × 3长度）
├── slide_gen.py         # 幻灯片 HTML 渲染 + Playwright 截图 ← 核心
├── cover_gen.py         # 旧版封面生成（保留，非主力）
├── publisher.py         # Playwright 半自动发布到小红书
├── skills/              # 项目领域分类器（7类加权打分）
├── data/
│   ├── trending.json    # 缓存的 GitHub 项目列表
│   └── used.json        # 已发布项目记录（防重复）
├── drafts/              # 文案草稿（Markdown）
├── output/              # 生成的幻灯片 PNG
│   └── {project-name}/  # 每个项目一个子目录
└── FLOW.md              # 本文档
```

---

## 三、图片生成流程

### 入口
```python
from slide_gen import generate_slides
generate_slides(slides_data, "output/project-name")
```

### 5 页结构 & 数据格式

#### ① Cover 封面 (`type: "cover"`)
```json
{
  "type": "cover",
  "heading": "每天认识一个AI工具",
  "project_name": "Claude-Mem",
  "subheading": "让 AI Agent 拥有持久记忆...",
  "logo_emoji": "🧠",
  "avatar_url": "https://github.com/{owner}.png",
  "star_text": "80,800+",
  "lang_text": "TypeScript"
}
```
- Logo 优先级：截图 > emoji > 白底黑字项目名
- 标签：Stars + Language（MIT License 不显示）

#### ② Features 核心特性 (`type: "features"`)
```json
{
  "type": "features",
  "heading": "核心特性",
  "intro": "Claude-Mem 的核心功能",
  "project_name": "Claude-Mem",
  "summary_text": "一句话总结",
  "stats": [{"value": "500K", "label": "安装量"}],
  "items": [{"emoji": "🧠", "title": "标题", "desc": "描述"}]
}
```
- 2×2 网格，总结区在最上面（项目名加粗 32px）
- 不要 "SUMMARY" 小标题

#### ③ Highlights 核心亮点 (`type: "highlights"`)
```json
{
  "type": "highlights",
  "heading": "核心亮点",
  "intro": "一句话",
  "items": [{"emoji": "⚡", "title": "标题", "desc": "描述"}],
  "metrics": [{"value": "70%", "desc": "减少token浪费"}],
  "scenarios": ["场景1", "场景2"]
}
```
- 两列卡片 + 底部指标条 + 使用场景

#### ④ Architecture 技术架构 (`type: "architecture"`)
```json
{
  "type": "architecture",
  "heading": "技术架构",
  "intro": "一句话",
  "flow_steps": ["步骤1", "步骤2", "步骤3", "步骤4"],
  "compare": {
    "before": {"label": "传统方式", "items": ["❌ 缺点1"]},
    "after": {"label": "Claude-Mem", "items": ["✅ 优点1"]}
  },
  "layers": [{"name": "层名", "desc": "描述", "features": ["特性"]}],
  "tech_stack": ["TypeScript", "Node.js"]
}
```
- 两列对比（❌红底 vs ✅绿底）+ 2×2 架构卡片

#### ⑤ Usage 使用方式 (`type: "usage"`)
```json
{
  "type": "usage",
  "heading": "快速上手",
  "github": {"name": "owner/repo", "desc": "...", "stars": "80K", "forks": "4K", "url": "github.com/..."},
  "tips": ["建议1", "建议2", "建议3"],
  "steps": [{"cmd": "npm install", "desc": "安装依赖"}],
  "code_example": {"title": "使用示例", "code": "const memory = ..."}
}
```
- 布局顺序：GitHub卡片+tips（白卡片）→ 终端代码（深色）→ 安装步骤（白卡片）
- 项目名称在最上面，建议内容在下面

### 渲染管线
```
slides_data (dict) → render_slide_html() → HTML string
    → Playwright chromium → 1080×1440 PNG screenshot
    → output/{project}/slide_{n}_{type}.png
```

### 主题系统（Silver）
```python
THEME = {
    "name": "银灰 Silver",
    "bg": "#f5f5f5",          # 浅灰背景
    "text": "#1a1a1a",        # 黑色主文字
    "text_sub": "#666",       # 灰色副文字
    "accent": "#10b981",      # 翡翠绿强调
    "card_border": "#e5e5e5"  # 淡灰边框
}
```

---

## 四、文案生成流程

### 入口
```python
python main.py generate   # 或 all（采集+生成+发布）
```

### 流程
```
GitHub Trending → scraper.py（采集 top 项目）
    → skills/detect_skill（分类：ai_model/ai_agent/dev_tools/...）
    → generator.py（LLM 生成 3 个文案候选）
        → prompts.py（build_system_prompt 组装 prompt）
        → MiMo API（带重试 + timeout 处理）
    → data/trending.json（缓存）
    → drafts/{date}.md（用户审阅）
```

### 文案规则
- **5 角色**：科技博主 / 程序员 / 创业者 / 产品经理 / AI 爱好者
- **5 风格**：excited / calm / funny / tutorial / comparison
- **3 结构**：问题-方案-效果 / 特点-场景-对比 / 步骤-教程-总结
- **3 长度**：short（150-300）/ medium（300-600）/ long（600-1000）
- **结尾**：以项目地址结尾，不加互动引导语
- **每条 3-5 个标签**

---

## 五、发布流程

```
drafts/{date}.md（用户确认）
    → publisher.py（Playwright 打开小红书发布页）
    → 自动填入标题 + 正文 + 标签
    → 用户手动点发布（首次需扫码登录）
```

---

## 六、核心设计约束

| 约束 | 说明 |
|------|------|
| 尺寸 | 1080×1440px（小红书竖版） |
| 主题 | Silver 银灰（固定） |
| 字体 | Noto Sans SC + Noto Serif SC |
| 渲染 | Playwright Sync API（不能在 asyncio 内调用） |
| 截图 | `sync_playwright()` + `page.screenshot()` |
| 输出 | 时间戳子目录 `yyyy-mm-dd HH-MM-SS/` |
| API | MiMo（xiaiaMimo），key 在 config.json |
