# 幻灯片内容扩充 Skill

## 目标
解决图3/图4/图5内容单薄、留白过多的问题，通过丰富内容和优化排版提升视觉效果。

## 设计原则

### 1. 内容密度
- **Highlights**: 4个核心亮点 + 2-3个数据对比 + 使用场景
- **Architecture**: 3-4层架构 + 流程连接 + 技术细节说明
- **Usage**: 3-4个步骤 + 代码示例 + 最佳实践提示

### 2. 视觉层次
- 使用卡片、图标、数字、标签等多种元素
- 添加分隔线、背景色块区分内容区域
- 使用 emoji 增加视觉趣味性

### 3. 信息架构
- **主标题**: 64px 大标题
- **副标题**: 28px 说明文字
- **核心内容**: 24-28px 正文
- **辅助信息**: 20-22px 说明文字
- **数字/标签**: 13-36px 强调元素

## 模板设计

### Highlights 模板 (图3)

#### 内容结构
```
┌─────────────────────────────────┐
│ 顶部栏 (HIGHLIGHTS 3/5)        │
├─────────────────────────────────┤
│ 大标题: 为什么值得用？          │
├─────────────────────────────────┤
│ 副标题: AI Agent 最大的痛点...  │
├─────────────────────────────────┤
│ 数据对比区 (3个关键指标)        │
│ ┌─────┐ ┌─────┐ ┌─────┐        │
│ │ 10x │ │ 0   │ │ 100%│        │
│ │更快 │ │中断 │ │保留 │        │
│ └─────┘ └─────┘ └─────┘        │
├─────────────────────────────────┤
│ 核心亮点 (4个)                  │
│ 🧠 跨会话记忆                   │
│ 📝 自动记录                     │
│ 🗜️ AI 压缩                     │
│ 🎯 精准注入                     │
├─────────────────────────────────┤
│ 使用场景 (2-3个)                │
│ "我用 Claude-Mem 后..."         │
├─────────────────────────────────┤
│ 底部栏                          │
└─────────────────────────────────┘
```

#### 数据字段
```python
{
    "type": "highlights",
    "heading": "为什么值得用？",
    "intro": "AI Agent 最大的痛点不是能力不够，而是「记不住」",
    "metrics": [
        {"value": "10x", "label": "开发效率提升"},
        {"value": "0", "label": "上下文中断"},
        {"value": "100%", "label": "决策保留率"}
    ],
    "items": [
        {"icon": "🧠", "title": "跨会话记忆", "desc": "传统 AI 助手每次对话都是独立的..."},
        {"icon": "📝", "title": "自动记录", "desc": "像一个忠实的书记官..."},
        {"icon": "🗜️", "title": "AI 压缩", "desc": "用 AI 将原始记录压缩..."},
        {"icon": "🎯", "title": "精准注入", "desc": "根据当前任务的相关性..."}
    ],
    "scenarios": [
        {"quote": "我用 Claude-Mem 后，再也不用每次都重新解释项目背景了", "author": "全栈开发者"},
        {"quote": "跨会话的代码修改记录完美保留，调试效率翻倍", "author": "后端工程师"}
    ]
}
```

### Architecture 模板 (图4)

#### 内容结构
```
┌─────────────────────────────────┐
│ 顶部栏 (ARCHITECTURE 4/5)      │
├─────────────────────────────────┤
│ 大标题: 怎么实现的？            │
├─────────────────────────────────┤
│ 副标题: 三层记忆架构...         │
├─────────────────────────────────┤
│ 架构流程图 (横向连接)           │
│ ┌─────┐    ┌─────┐    ┌─────┐  │
│ │捕获层│ → │压缩层│ → │检索层│  │
│ └─────┘    └─────┘    └─────┘  │
├─────────────────────────────────┤
│ 技术细节卡片 (3个)              │
│ ┌─────────────────────────────┐ │
│ │ 🔍 捕获层                   │ │
│ │ 自动拦截 Agent 的工具调用...│ │
│ │ • 工具调用监控              │ │
│ │ • 代码修改追踪              │ │
│ │ • 文件操作记录              │ │
│ └─────────────────────────────┘ │
├─────────────────────────────────┤
│ 技术栈标签 (6-8个)              │
├─────────────────────────────────┤
│ 底部栏                          │
└─────────────────────────────────┘
```

#### 数据字段
```python
{
    "type": "architecture",
    "heading": "怎么实现的？",
    "intro": "三层记忆架构 + AI 压缩引擎 + 语义检索",
    "flow_steps": ["捕获层", "压缩层", "检索层"],
    "layers": [
        {
            "name": "捕获层",
            "desc": "自动拦截 Agent 的工具调用、代码修改、文件操作",
            "features": ["工具调用监控", "代码修改追踪", "文件操作记录"]
        },
        {
            "name": "压缩层",
            "desc": "AI 引擎将原始记录压缩成语义摘要",
            "features": ["语义理解", "关键信息提取", "冗余去除"]
        },
        {
            "name": "检索层",
            "desc": "三层记忆 + 语义搜索",
            "features": ["即时记忆", "短期记忆", "长期记忆"]
        }
    ],
    "tech_stack": ["TypeScript", "AI Agent", "持久记忆", "语义搜索", "Claude Code", "MCP"]
}
```

### Usage 模板 (图5)

#### 内容结构
```
┌─────────────────────────────────┐
│ 顶部栏 (GETTING STARTED 5/5)   │
├─────────────────────────────────┤
│ 大标题: 快速开始                │
├─────────────────────────────────┤
│ 安装步骤 (3-4个)                │
│ ① npx claude-mem install        │
│   一行命令安装...               │
│ ② 重启 Claude Code              │
│   重启后自动生效...             │
│ ③ npx claude-mem viewer         │
│   打开 Web UI...                │
├─────────────────────────────────┤
│ 代码示例区                      │
│ ┌─────────────────────────────┐ │
│ │ // 使用示例                 │ │
│ │ const memory = new Memory() │ │
│ │ memory.add("key", "value")  │ │
│ └─────────────────────────────┘ │
├─────────────────────────────────┤
│ 最佳实践提示                    │
│ 💡 建议在项目开始时安装         │
│ 💡 定期清理过期记忆             │
├─────────────────────────────────┤
│ GitHub 数据卡片                 │
├─────────────────────────────────┤
│ 底部栏                          │
└─────────────────────────────────┘
```

#### 数据字段
```python
{
    "type": "usage",
    "heading": "快速开始",
    "steps": [
        {"cmd": "npx claude-mem install", "desc": "一行命令安装 — 自动配置 Claude Code"},
        {"cmd": "# 重启 Claude Code", "desc": "重启后自动生效 — 历史上下文自动注入"},
        {"cmd": "npx claude-mem viewer", "desc": "打开 Web UI — 实时查看记忆流入"}
    ],
    "code_example": {
        "title": "使用示例",
        "code": "// 初始化记忆系统\nconst memory = new ClaudeMemory();\n\n// 添加记忆\nawait memory.add('project', 'Peko 桌面宠物');\n\n// 检索记忆\nconst context = await memory.search('项目架构');"
    },
    "tips": [
        "💡 建议在项目开始时安装，让 AI 从第一天就记住你的项目",
        "💡 定期使用 `npx claude-mem cleanup` 清理过期记忆"
    ],
    "github": {
        "name": "thedotmack/claude-mem",
        "desc": "Persistent memory compression system for Claude Code",
        "stars": "80.8k",
        "forks": "2.1k",
        "url": "github.com/thedotmack/claude-mem"
    }
}
```

## 实现步骤

### 1. 更新 slide_gen.py
- 修改 `_render_highlights()` 函数
- 修改 `_render_architecture()` 函数
- 修改 `_render_usage()` 函数

### 2. 更新 generate_claude_mem.py
- 更新数据结构以匹配新的模板字段

### 3. 测试验证
- 生成新的幻灯片图片
- 检查内容密度和视觉效果
- 调整样式和布局

## 样式规范

### 卡片样式
```css
.card {
    background: #fff;
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 20px;
    border: 1px solid #e5e5e5;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
```

### 数字指标样式
```css
.metric {
    text-align: center;
    padding: 20px;
    background: #fff;
    border-radius: 12px;
}
.metric-value {
    font-size: 48px;
    font-weight: 900;
    color: #667eea;
}
.metric-label {
    font-size: 16px;
    color: #86868b;
}
```

### 流程图样式
```css
.flow {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
    padding: 30px 0;
}
.flow-step {
    background: #fff;
    border-radius: 12px;
    padding: 20px 30px;
    font-weight: 700;
    font-size: 24px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
.flow-arrow {
    font-size: 28px;
    color: #667eea;
}
```

### 代码块样式
```css
.code-block {
    background: #1e1e1e;
    border-radius: 12px;
    padding: 24px;
    font-family: 'SF Mono', monospace;
    font-size: 18px;
    color: #d4d4d4;
    line-height: 1.6;
}
```

## 注意事项

1. **内容真实性**: 所有数据和描述必须基于真实信息
2. **视觉平衡**: 确保各元素间距均匀，避免拥挤或空旷
3. **响应式**: 内容应适应 1080×1440 的画布尺寸
4. **可读性**: 文字大小和颜色对比度要符合阅读习惯
