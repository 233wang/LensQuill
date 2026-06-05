# AI 小说转剧本工具 - 设计文档

**文档版本:** 1.0  
**创建日期:** 2026-06-05  
**状态:** 设计阶段

---

## 目录

1. [项目概述](#项目概述)
2. [技术架构](#技术架构)
3. [系统设计](#系统设计)
4. [YAML Schema 设计](#yaml-schema-设计)
5. [模块设计](#模块设计)
6. [API 设计](#api-设计)
7. [前端界面设计](#前端界面设计)
8. [开发计划](#开发计划)

---

## 项目概述

### 项目目标

开发一款 AI 辅助剧本创作工具，帮助小说作者将小说文本自动转换为结构化剧本。

### 核心功能

- 支持 3 个及以上章节的小说输入
- 自动识别章节结构
- AI 理解小说内容（人物、场景、情节）
- 转换为结构化 YAML 格式剧本
- 提供可编辑的剧本初稿

### 输入方式

- 直接粘贴小说文本
- 上传 .txt / .md 文件
- 从指定目录读取多个章节文件

### 输出格式

- YAML 格式，结构化存储
- 可读性强，便于手动编辑
- 支持后续扩展

---

## 技术架构

### 总体架构

```
ai-novel-to-script/
│
├── core/              # 核心业务逻辑层
├── llm/               # LLM集成层（讯飞星火API）
├── api/               # FastAPI Web服务层
├── frontend/          # Vue 3 前端界面
├── cli/               # CLI工具
├── docs/              # 文档
├── examples/          # 示例
└── tests/             # 单元测试
```

### 技术选型

| 层级 | 技术 | 说明 |
|------|------|------|
| 后端框架 | Python + FastAPI | RESTful API服务 |
| AI处理 | Python | 调用讯飞星火Qwen3.6-35B-A3B API |
| 前端框架 | Vue 3 + Composition API | 响应式用户界面 |
| 状态管理 | Pinia | 状态管理 |
| HTTP客户端 | axios | API调用 |
| YAML处理 | js-yaml | 前端YAML解析 |
| 代码编辑器 | CodeMirror | YAML编辑器 |

### 运行环境

- Python 3.9+
- Node.js 18+
- Docker (可选)

---

## 系统设计

### 数据流图

```
用户输入 → 前端界面 → API服务 → 核心处理 → AI分析 → YAML生成 → 返回结果
                                         ↓
                                    临时存储
```

### 处理流程

1. **输入阶段**：用户通过Web界面或CLI输入小说文本
2. **解析阶段**：解析章节结构，识别章节标题和内容
3. **分析阶段**：AI理解小说内容（人物、场景、情节等）
4. **生成阶段**：转换为剧本结构（场景、对白、动作等）
5. **输出阶段**：导出为结构化YAML格式

### 错误处理

- 输入验证：检查章节数量、文本格式
- AI调用失败：重试机制和错误提示
- 处理中断：保留中间状态，支持断点续传

---

## YAML Schema 设计

### 主要字段

```yaml
# 元信息
metadata:
  version: "1.0"
  generated_by: "AI Tool v1.0"
  generated_at: "2024-01-01T12:00:00"
  source_files: []
  llm_model: "qwen3.6-35b-a3b"

# 来源信息
source:
  type: "novel"
  title: "小说标题"
  author: "作者名"
  chapters_count: 3
  chapters: []

# 人物列表
characters:
  - id: "char_001"
    name: "林舟"
    role: "protagonist"
    description: "角色描述"
    aliases: []
    relationships: []

# 场景列表
scenes:
  - id: "scene_001"
    title: "场景标题"
    chapter_ref: "chapter_001"
    location: "旧城区巷口"
    time: "夜晚"
    date: ""
    characters: ["char_001"]
    summary: "场景摘要"
    beats: []

# 情节节点
beats:
  - id: "beat_001"
    type: "action"  # action/dialogue/narration/description
    content: "内容文本"
    character: ""
    speaker_name: ""
    location_ref: ""
    time_ref: ""
    notes: []

# 全局备注
notes:
  - id: "note_001"
    type: "editorial"
    content: "备注内容"
    referenced_id: ""
    author: "ai/user"
```

### 字段类型说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| metadata | object | 是 | 元信息对象 |
| source | object | 是 | 来源信息对象 |
| characters | array | 是 | 人物列表 |
| scenes | array | 是 | 场景列表 |
| beats | array | 是 | 情节节点列表 |
| notes | array | 否 | 全局备注列表 |

---

## 模块设计

### 1. 章节解析器 (chapter_parser.py)

**功能：**
- 识别章节标题（支持多种格式）
- 拆分章节内容
- 处理超长章节

**主要方法：**
- `parse_chapters(text)`: 解析章节
- `detect_chapter_titles(text)`: 检测章节标题

### 2. 小说分析器 (novel_analyzer.py)

**功能：**
- 人物识别（NER）
- 人物关系识别
- 场景地点识别
- 时间线识别
- 关键事件提取
- 对白与叙述区分

**主要方法：**
- `extract_characters(chapters)`: 提取人物
- `extract_scenes(chapters)`: 提取场景
- `analyze_relationships(characters)`: 分析关系

### 3. 剧本生成器 (script_generator.py)

**功能：**
- 将小说内容转换为剧本结构
- 生成场景和情节节点
- 添加剧本元素（对白、动作、旁白）

**主要方法：**
- `generate_scenes(chapters, analysis)`: 生成场景
- `create_beats(scene)`: 创建情节节点

### 4. YAML导出器 (yaml_exporter.py)

**功能：**
- 格式化输出YAML
- 验证数据结构
- 缩进和格式化

**主要方法：**
- `export_yaml(data)`: 导出YAML
- `validate_schema(data)`: 验证Schema

---

## API 设计

### 1. 上传接口

```
POST /api/upload
```

**请求：**
```json
{
  "content": "string",
  "format": "text|file",
  "filename": "string"
}
```

**响应：**
```json
{
  "status": "success",
  "chapters": [...]
}
```

### 2. 分析接口

```
POST /api/analyze
```

**请求：**
```json
{
  "chapters": [...]
}
```

**响应：**
```json
{
  "status": "success",
  "characters": [...],
  "scenes": [...],
  "relationships": [...]
}
```

### 3. 生成接口

```
POST /api/generate
```

**请求：**
```json
{
  "chapters": [...],
  "analysis": {...}
}
```

**响应：**
```json
{
  "status": "success",
  "script": {...}
}
```

### 4. 导出接口

```
POST /api/export
```

**请求：**
```json
{
  "script": {...}
}
```

**响应：**
```json
{
  "status": "success",
  "yaml": "string"
}
```

---

## 前端界面设计

### 页面结构

#### 1. 首页 (Home.vue)

**功能：**
- 输入方式选择（粘贴/上传/目录）
- 文本输入框
- 上传文件选择
- 目录路径输入

#### 2. 预览页 (Preview.vue)

**功能：**
- 显示解析后的章节列表
- AI处理进度显示
- 处理状态提示

#### 3. 编辑页 (Editor.vue)

**功能：**
- YAML代码编辑器
- 人物列表查看
- 场景列表查看
- 编辑和保存功能

### 组件设计

```
components/
├── YamlEditor.vue      # YAML代码编辑器
├── ChapterList.vue     # 章节列表展示
├── CharacterList.vue   # 人物列表展示
├── SceneList.vue       # 场景列表展示
└── ProgressBar.vue     # 进度条组件
```

---

## 开发计划

### 阶段一：项目初始化
- [ ] 初始化项目结构
- [ ] 配置开发环境
- [ ] 编写 README

### 阶段二：核心功能
- [ ] 章节解析器
- [ ] 小说分析器
- [ ] 剧本生成器
- [ ] YAML导出器

### 阶段三：LLM集成
- [ ] 讯飞星火API集成
- [ ] API密钥配置
- [ ] 错误处理和重试

### 阶段四：Web服务
- [ ] FastAPI服务搭建
- [ ] API路由实现
- [ ] 数据模型定义

### 阶段五：前端界面
- [ ] Vue 3项目搭建
- [ ] 页面路由配置
- [ ] 组件开发
- [ ] YAML编辑器集成

### 阶段六：测试和文档
- [ ] 单元测试
- [ ] 集成测试
- [ ] YAML Schema文档
- [ ] 示例文件

### 阶段七：完善和优化
- [ ] 用户体验优化
- [ ] 性能优化
- [ ] Demo视频制作

---

## 进度跟踪

### 已完成

- [x] 需求分析
- [x] 架构设计
- [x] YAML Schema设计
- [x] 实现计划编写
- [x] 项目初始化
- [x] 核心功能开发
  - [x] 章节解析器（使用 txt_to_epub 库）
  - [x] 小说分析器
  - [x] 剧本生成器
  - [x] YAML导出器
- [x] API集成（讯飞星火API）
- [x] Web服务（FastAPI）
  - [x] 服务搭建
  - [x] API路由实现
  - [x] 数据模型定义
- [x] 测试和文档
  - [x] 单元测试（18个测试全部通过）
  - [x] YAML Schema文档
  - [x] 示例文件

### 进行中

- [ ] 前端开发（Vue 3）
  - [ ] Vue 3项目搭建
  - [ ] 页面路由配置
  - [ ] 组件开发
  - [ ] YAML编辑器集成

### 待开发

- [ ] 用户体验优化
- [ ] 性能优化
- [ ] Demo视频制作

---

## 参考资料

- 题目要求文档：`AI小说转剧本工具_题目要求.md`
- 讯飞星火API文档：https://www.xunfei.com/
- Vue 3文档：https://vuejs.org/
- FastAPI文档：https://fastapi.tiangolo.com/
- YAML规范：https://yaml.org/
