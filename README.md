# XHS Publisher

小红书自动发布工具：GitHub 热门项目 → LLM 文案 → 5页幻灯片 → 半自动发布到小红书。

## 工作流

```
GitHub Trending 采集 → LLM 生成 3 条候选文案 → 5 页 Silver 主题幻灯片 → Playwright 截图 PNG → 半自动发布到小红书
```

**完全免费** — 使用 MiMo API（免费额度）+ Playwright（开源）

## 快速开始

### 1. 复制配置
```bash
cp config.example.json config.json
```

### 2. 填入你的 API key
编辑 `config.json`，填入 MiMo API key。

### 3. 生成文案
```bash
python main.py generate          # 生成文案草稿
python main.py --pick 3          # 选择第 3 个项目
python main.py --skills          # 列出所有可用 skill
```

### 4. 发布到小红书
```bash
python main.py all               # 采集 + 生成 + 发布
```

## 文案生成

- **5 种角色**：科技博主 / 程序员 / 创业者 / 产品经理 / AI 爱好者
- **5 种风格**：兴奋 / 平静 / 幽默 / 教程 / 对比
- **3 种结构**：问题-方案-效果 / 特点-场景-对比 / 步骤-教程-总结
- **3 种长度**：short（150-300 字）/ medium（300-600 字）/ long（600-1000 字）
- 每次生成 **3 条候选文案**，用户审阅后选择发布
- 结尾以项目地址收尾，不加互动引导语

## 幻灯片生成

5 页固定结构，Silver 银灰主题，1080×1440px（小红书竖版）：

| 页码 | 类型 | 内容 |
|------|------|------|
| ① | Cover | 刊头 + Logo + 项目名 + 一句话介绍 + 标签 |
| ② | Features | 2×2 功能网格 + 项目摘要 + 关键指标 |
| ③ | Highlights | 数据指标 + 亮点卡片 + 使用场景 |
| ④ | Architecture | 两列对比（传统 vs 新方案）+ 架构卡片 |
| ⑤ | Usage | GitHub 项目卡 + 最佳实践 + 终端代码 + 安装步骤 |

```python
from slide_gen import generate_slides
generate_slides(slides_data, "output/project-name")
```

## Skill 系统

根据 GitHub topics、编程语言、description 关键词自动匹配项目领域（7 类），用于文案生成时的风格推荐。

## 项目结构

```
xhs-publisher/
├── main.py              # CLI 入口（generate/publish/all）
├── scraper.py           # GitHub Trending 项目采集
├── generator.py         # LLM 文案生成（MiMo API）
├── prompts.py           # 文案 prompt 构建（角色×风格×结构×长度）
├── slide_gen.py         # 幻灯片 HTML 渲染 + Playwright 截图
├── publisher.py         # Playwright 半自动发布到小红书
├── skills/              # 项目领域分类器（7 类加权打分）
├── config.json          # 配置文件（已 gitignore）
├── config.example.json  # 配置模板
├── data/
│   ├── trending.json    # 缓存的热门项目列表
│   └── used.json        # 已使用过的项目（防重复）
├── drafts/              # 文案草稿（Markdown）
├── output/              # 生成的幻灯片 PNG
└── FLOW.md              # 详细流程文档
```

## 许可

MIT
