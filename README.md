# 📕 小红书自动发布工具 (xhs-publisher)

> GitHub 热门开源项目 → LLM 生成小红书文案 → 自动生成封面图 → 半自动发布

每天自动从 GitHub Trending 挖掘值得推荐的 AI/开发者工具项目，用 LLM 生成小红书风格的图文内容，一键发布。

---

## ✨ 功能

- 🔍 **智能采集** — 从 GitHub Trending 抓取本周热门 AI、开发工具类项目
- ✍️ **AI 文案** — 调用 LLM 生成小红书风格推荐文案（标题 / 正文 / 标签）
- 🎨 **封面图生成** — 自动生成 3 张 1080×1440 竖版封面图（HTML → Playwright 截图 → PNG）
- 📤 **半自动发布** — Playwright 自动打开小红书发布页并填入内容，用户手动点发布
- 🔁 **去重机制** — 自动记录已推荐项目，避免重复内容

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/JuneJay/xhs-publisher.git
cd xhs-publisher
```

### 2. 安装依赖

```bash
pip install requests beautifulsoup4 playwright
playwright install chromium
```

### 3. 配置 API Key

复制配置模板并填入你的 LLM API key：

```bash
cp config.example.json config.json
```

编辑 `config.json`：

```json
{
  "llm": {
    "api_key": "sk-xxxxxxxxxxxxxxxx",
    "api_url": "https://api.example.com/v1/chat/completions",
    "model": "your-model-name",
    "max_tokens": 2000
  }
}
```

> 💡 支持任何兼容 OpenAI 格式的 LLM API（OpenAI、DeepSeek、MiMo、硅基流动等）

### 4. 运行

```bash
# 仅生成文案草稿 + 封面图（推荐）
python main.py --draft

# 指定第 N 个项目
python main.py --draft --pick 2

# 完整流程（生成 + 打开小红书发布页）
python main.py
```

---

## 📁 项目结构

```
xhs-publisher/
├── main.py                # 主入口
├── scraper.py             # GitHub Trending 采集
├── generator.py           # LLM 文案生成
├── cover_gen.py           # HTML 封面图生成 + Playwright 截图
├── publisher.py           # Playwright 半自动发布
├── config.json            # 你的配置（不提交到 Git）
├── config.example.json    # 配置模板
├── data/
│   ├── trending.json      # 缓存的热门项目列表
│   └── used.json          # 已推荐项目记录（去重用）
├── drafts/
│   └── YYYY-MM-DD.md      # 每日生成的文案草稿
└── covers/
    ├── YYYY-MM-DD-01-cover.png       # 封面图
    ├── YYYY-MM-DD-02-features.png    # 功能亮点图
    └── YYYY-MM-DD-03-quickstart.png  # 快速上手图
```

---

## ⚙️ 配置说明

| 字段 | 说明 | 示例 |
|------|------|------|
| `llm.api_key` | LLM API 密钥（必填） | `sk-xxx` |
| `llm.api_url` | API 地址（兼容 OpenAI 格式） | `https://api.deepseek.com/v1/chat/completions` |
| `llm.model` | 模型名称 | `deepseek-chat` |
| `llm.max_tokens` | 最大生成长度 | `2000` |
| `topics` | 感兴趣的技术领域（用于评分） | `["AI", "LLM", "agent"]` |
| `max_results` | 采集项目数量 | `20` |
| `language` | 偏好编程语言 | `"Python"` |
| `xiaohongshu.headless` | 发布时是否无头模式 | `false` |

---

## 📝 生成效果

每次运行会产出：

**文案草稿** (`drafts/YYYY-MM-DD.md`)
- 吸引眼球的标题（含 emoji + 数据）
- 500-800 字正文（痛点引入 → 项目介绍 → 核心功能 → 使用方式 → 推荐理由）
- 8-10 个相关标签
- AI 封面图提示词

**封面图** (`covers/`)

| 图片 | 内容 |
|------|------|
| `01-cover.png` | 主封面：项目名 + Star 数 + 核心卖点 |
| `02-features.png` | 功能亮点：3 个核心功能卡片 |
| `03-quickstart.png` | 快速上手：3 步安装指南 |

---

## 🔁 定时自动运行

### Windows（任务计划程序）

```powershell
# 每天早上 8 点自动生成
schtasks /create /tn "XHS-Publisher" /tr "python X:\path\to\main.py --draft" /sc daily /st 08:00
```

### Linux/macOS（crontab）

```bash
0 8 * * * cd /path/to/xhs-publisher && python main.py --draft
```

---

## 🛠️ 常见问题

**Q: LLM API 报 401？**
检查 `config.json` 中的 `api_key` 是否有效，是否过期。

**Q: 封面图中文显示为方块？**
Playwright 的 Chromium 需要中文字体。Windows 一般自带，Linux 需安装：
```bash
sudo apt install fonts-noto-cjk
```

**Q: 采集不到项目？**
可能是 GitHub Trending 页面结构变化，检查 `scraper.py` 中的选择器。

---

## 📄 License

MIT
