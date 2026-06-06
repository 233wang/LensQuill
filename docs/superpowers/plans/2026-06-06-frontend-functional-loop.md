# 功能闭环实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现完整的功能闭环：用户粘贴小说 → 章节预览 → 生成剧本 → YAML编辑 + AI对话打磨

**Architecture:** 
- 前端：Vue 3 + Pinia + GSAP 动画 + CodeMirror YAML编辑器 + AI对话组件
- 后端：FastAPI + 讯飞星火API（兼容OpenAI格式）
- 数据流：用户输入 → 章节解析 → AI分析 → 剧本生成 → YAML导出 → 人工编辑 + AI打磨

**Tech Stack:** Vue 3, Pinia, GSAP, CodeMirror 6, js-yaml, Element Plus, FastAPI, xunfei_api

---

## 核心功能需求

### 1. 完整功能流程

```
用户操作流程：
1. 复制小说到输入框 → 点击"开始处理"
2. 进入章节预览页 → 显示解析后的章节列表 → 点击"生成剧本"
3. 前端动画显示生成过程 → 进入编辑页显示YAML格式
4. 左侧YAML编辑器 → 右侧AI对话框 → 用户可手动修改YAML + 与AI对话打磨
```

### 2. 功能约束

- **输入验证**：至少需要3个章节才能生成
- **加载状态**：所有异步操作都要显示loading状态和动画
- **错误处理**：友好的错误提示，不中断用户操作
- **状态持久化**：使用localStorage保存中间状态
- **YAML编辑**：用户可手动修改YAML内容
- **AI对话**：右侧对话框用于与大模型交流打磨剧本

---

## 文件结构

```
前端文件：
- frontend/src/views/Home.vue          # 首页：输入小说
- frontend/src/views/Preview.vue       # 预览页：章节列表 + 生成按钮
- frontend/src/views/Editor.vue        # 编辑页：YAML编辑器 + AI对话
- frontend/src/components/YamlEditor.vue  # YAML代码编辑器（CodeMirror）
- frontend/src/components/AIChat.vue   # AI对话界面
- frontend/src/stores/novel.ts         # Pinia状态管理

后端文件：
- llm/xunfei_api.py                  # 讯飞星火API集成
- api/routes.py                      # API路由
- core/script_generator.py           # 剧本生成器
- core/novel_analyzer.py             # 小说分析器

配置文件：
- .env                               # API配置
- frontend/vite.config.ts            # Vite配置
```

---

## 实现步骤

### 1. 前端状态管理

- [ ] 创建 Pinia store 管理整个流程状态
- [ ] 定义状态类型：content, chapters, script, loading, error等

### 2. 修复 Home.vue

- [ ] 确保文件读取使用 utf-8 编码
- [ ] 添加章节检测（至少3个章节）
- [ ] 修复 localStorage 数据存储

### 3. 修复 Preview.vue

- [ ] 修复 generateScript API 调用参数
- [ ] 添加生成动画效果
- [ ] 优化错误处理

### 4. 修复 Editor.vue

- [ ] 集成 YamlEditor 组件
- [ ] 集成 AIChat 组件
- [ ] 实现 YAML 格式转换（JSON ↔ YAML）
- [ ] 优化保存和下载功能

### 5. 修复后端 API

- [ ] 确保 xunfei_api.py 正确集成
- [ ] 修复 generate 路由的参数传递
- [ ] 确保章节解析正确

### 6. 测试完整流程

- [ ] 端到端测试：输入 → 预览 → 生成 → 编辑 → AI对话
- [ ] 错误场景测试

---

## 执行选择

**1. Subagent-Driven (推荐)** - 我dispatch一个subagent负责前端，一个负责后端，分别完成各自任务，然后合并

**2. Inline Execution** - 在本session中依次执行所有任务，每完成一个模块就检查

**Which approach?**