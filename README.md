# 📕 小红书自动发布工具

GitHub 热门开源项目 → LLM 生成小红书文案 → HTML 封面图 → 半自动发布

## 功能

- 🔍 **自动采集** GitHub Trending 项目（AI/开发工具方向）
- ✍️ **LLM 文案生成** 用 MiMo 生成小红书风格推荐文案
- 🎨 **HTML 封面图** 自动生成 1080×1440 竖版封面，截图即用
- 📤 **半自动发布** Playwright 自动填入内容，用户手动点发布

## 快速开始

```bash
# 安装依赖
pip install requests playwright beautifulsoup4

# 配置
# 编辑 config.json，填入你的 LLM API key

# 生成文案草稿 + 封面图
python main.py --draft

# 完整流程（生成 + 打开小红书发布页）
python main.py

# 指定第 N 个项目
python main.py --draft --pick 2
```

## 项目结构

```
xhs-publisher/
├── main.py          # 主入口
├── scraper.py       # GitHub 项目采集
├── generator.py     # LLM 文案生成
├── cover_gen.py     # HTML 封面图生成
├── publisher.py     # Playwright 半自动发布
├── config.json      # 配置（LLM API、小红书等）
├── data/
│   └── trending.json    # 缓存的热门项目
├── drafts/
│   └── YYYY-MM-DD.md   # 生成的文案草稿
└── covers/
    └── YYYY-MM-DD-*.html  # 封面图 HTML
```

## 工作流程

1. 采集本周 GitHub 热门 AI/dev 工具项目
2. 选取一个未推荐过的项目，用 LLM 生成小红书文案
3. 生成 3 张 HTML 封面图（封面 / 功能亮点 / 快速上手）
4. 草稿保存到 `drafts/`，封面保存到 `covers/`
5. 确认后运行 `python main.py` 打开小红书发布页，自动填入内容

## 定时任务

配合 cron 可实现每天自动生成文案草稿：
```bash
# 每天早上 8 点自动生成
python main.py --draft
```

## License

MIT
