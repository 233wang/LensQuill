# LensQuill 项目交接文档

**版本:** 1.0  
**创建日期:** 2026-06-05  
**交接对象:** 接手开发的 Agent  
**当前状态:** 后端核心模块完成，前端开发进行中

---

## 目录

1. [项目概述](#项目概述)
2. [技术架构](#技术架构)
3. [项目结构](#项目结构)
4. [已完成模块](#已完成模块)
5. [进行中工作](#进行中工作)
6. [开发规范](#开发规范)
7. [API 接口文档](#api-接口文档)
8. [YAML Schema 定义](#yaml-schema-定义)
9. [运行和测试](#运行和测试)
10. [Git 工作流](#git-工作流)
11. [关键文件说明](#关键文件说明)
12. [待办事项](#待办事项)

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

### 用户群体

- 小说作者
- 剧本创作者
- 内容创作者

---

## 技术架构

### 总体架构

```
LensQuill/
├── core/              # 核心业务逻辑层
├── llm/               # LLM集成层（讯飞星火API）
├── api/               # FastAPI Web服务层
├── frontend/          # Vue 3 前端界面（开发中）
├── cli/               # CLI工具
├── docs/              # 文档
├── examples/          # 示例
└── tests/             # 单元测试
```

### 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 后端框架 | Python + FastAPI | RESTful API服务 |
| AI处理 | Python | 调用讯飞星火Qwen3.6-35B-A3B API |
| 前端框架 | Vue 3 + Composition API | 响应式用户界面 |
| 状态管理 | Pinia | 状态管理 |
| HTTP客户端 | axios | API调用 |
| YAML处理 | js-yaml | 前端YAML解析 |
| 代码编辑器 | CodeMirror | YAML编辑器 |
| 项目构建 | Vite | 前端构建工具 |

### 运行环境

- Python 3.9+
- Node.js 18+
- conda 虚拟环境：`agent_debate`
- 讯飞星火API（Qwen3.6-35B-A3B）

---

## 项目结构

```
LensQuill/
├── AI小说转剧本工具_题目要求.md    # 题目要求文档
├── PRODUCT.md                       # 项目产品定义
├── DESIGN.md                        # 项目设计规范
├── CLAUDE.md                        # Claude Agent行为指南
├── README.md                        # 项目README
├── requirements.txt                 # Python依赖
├── .env.example                     # 环境变量示例
├── .gitignore                       # Git忽略文件
├── docs/
│   ├── design.md                    # 设计文档
│   └── superpowers/plans/           # 实现计划
├── core/                            # 核心模块
│   ├── __init__.py
│   ├── chapter_parser.py            # 章节解析器
│   ├── novel_analyzer.py            # 小说分析器
│   ├── script_generator.py          # 剧本生成器
│   └── yaml_exporter.py             # YAML导出器
├── llm/                             # LLM集成
│   ├── __init__.py
│   └── xunfei_api.py                # 讯飞星火API
├── api/                             # API服务
│   ├── __init__.py
│   ├── routes.py                    # API路由
│   └── models.py                    # 数据模型
├── frontend/                        # 前端界面（开发中）
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── router/
│   │   ├── stores/
│   │   ├── views/
│   │   ├── api/
│   │   ├── types/
│   │   └── main.ts
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
├── cli/                             # CLI工具
├── tests/                           # 单元测试
│   ├── __init__.py
│   ├── test_chapter_parser.py
│   └── test_yaml_exporter.py
└── examples/                        # 示例文件
```

---

## 已完成模块

### 1. 章节解析器 (core/chapter_parser.py)

**功能：**
- 使用 `txt_to_epub` 库进行智能章节解析
- 正则表达式作为降级策略
- 支持多种章节标题格式
- 过滤子标题

**测试：** 8个测试全部通过

### 2. 小说分析器 (core/novel_analyzer.py)

**功能：**
- 人物识别（基于关键词）
- 场景地点识别（基于关键词）
- 人物关系分析
- 关键事件提取
- 对白与叙述区分

### 3. 剧本生成器 (core/script_generator.py)

**功能：**
- 将小说内容转换为剧本结构
- 生成场景和情节节点
- 添加剧本元素（对白、动作、旁白）

### 4. YAML导出器 (core/yaml_exporter.py)

**功能：**
- 格式化输出YAML
- 验证数据结构
- 缩进和格式化

**测试：** 10个测试全部通过

### 5. 讯飞星火API集成 (llm/xunfei_api.py)

**功能：**
- 调用Qwen3.6-35B-A3B模型
- 分析小说内容
- 提取人物和场景信息
- 降级响应机制

### 6. FastAPI Web服务 (api/)

**功能：**
- `/api/upload` - 上传小说文本
- `/api/analyze` - 分析小说内容
- `/api/generate` - 生成剧本
- `/api/export` - 导出YAML

### 7. 单元测试 (tests/)

**测试文件：**
- `test_chapter_parser.py` - 8个测试
- `test_yaml_exporter.py` - 10个测试

---

## 进行中工作

### 前端开发 (Vue 3)

**当前状态：** 项目结构已搭建，开始界面设计

**已完成：**
- Vue 3 项目初始化
- Vite 构建配置
- TypeScript 配置
- 基础目录结构
- 路由配置
- 状态管理（Pinia）
- API客户端封装
- 类型定义

**进行中：**
- 首页（输入界面）设计和实现
- 使用 `/impeccable` 进行界面设计优化
- 深色主题 + Full palette配色方案
- 双输入模式（粘贴/上传）

**设计规范：**
- 项目类型：Product（工具类应用）
- 主题：深色主题
- 色彩策略：Full palette
- 参考：Obsidian, Notion, Linear

---

## 开发规范

### Git 工作流

1. **分支命名：** `feature/xxx` 或 `fix/xxx`
2. **提交规范：** `type: description`
   - `feat:` - 新功能
   - `fix:` - 修复
   - `docs:` - 文档
   - `chore:` - 构建/辅助工具
   - `refactor:` - 重构
3. **分支保护：** 主分支受保护，必须通过 PR 合并
4. **分支管理：** 每个任务完成后合并回主分支，不删除远程分支

### 代码规范

1. **Python：**
   - 遵循 PEP 8
   - 类型提示（Type Hints）
   - 模块化设计
   - 单元测试覆盖

2. **TypeScript/Vue：**
   - 使用 Composition API
   - TypeScript 类型安全
   - 单文件组件（SFC）

### 测试规范

1. **单元测试：** 使用 pytest
2. **测试覆盖：** 关键模块需有测试覆盖
3. **TDD：** 鼓励测试驱动开发

---

## API 接口文档

### 1. 上传文本

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
  "filename": "string",
  "content_length": 1234,
  "content": "string"
}
```

### 2. 分析小说

```
POST /api/analyze
```

**请求：**
```json
[
  {
    "title": "string",
    "content": "string"
  }
]
```

**响应：**
```json
{
  "status": "success",
  "analysis": {
    "characters": [],
    "scenes": [],
    "relationships": [],
    "key_events": []
  }
}
```

### 3. 生成剧本

```
POST /api/generate
```

**请求：**
```json
{
  "chapters": [],
  "analysis": {}
}
```

**响应：**
```json
{
  "status": "success",
  "script": {}
}
```

### 4. 导出YAML

```
POST /api/export
```

**请求：**
```json
{
  "script": {}
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

## YAML Schema 定义

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

## 运行和测试

### 环境准备

```bash
# 激活 conda 环境
source ~/miniconda3/etc/profile.d/conda.sh
conda activate agent_debate

# 安装 Python 依赖
pip install -r requirements.txt

# 安装 txt_to_epub 库
pip install txt-to-epub
```

### 后端运行

```bash
# 启动 FastAPI 服务
cd /home/wangjian/agent_project_test/LensQuill
python -m uvicorn api.routes:router --host 0.0.0.0 --port 8000 --reload
```

### 前端运行

```bash
cd frontend
npm install
npm run dev
```

### 测试

```bash
# 激活 conda 环境
source ~/miniconda3/etc/profile.d/conda.sh
conda activate agent_debate

# 运行单元测试
cd /home/wangjian/agent_project_test/LensQuill
pytest tests/ -v
```

### 环境变量配置

复制 `.env.example` 到 `.env` 并填写讯飞星火API凭证：

```bash
cp .env.example .env
```

---

## Git 工作流

### 当前分支

- `main` - 主分支
- `feature/core-modules` - 核心模块（已完成）
- `feature/design-phase` - 设计阶段（已完成）
- `feature/llm-integration` - LLM集成（已完成）
- `feature/script-generator` - 剧本生成器（已完成）
- `feature/tests-and-docs` - 测试和文档（已完成）
- `feature/web-service` - Web服务（已完成）
- `feature/vue3-frontend` - Vue3前端（进行中）

### 分支合并流程

1. 创建新分支：`git checkout -b feature/xxx`
2. 开发完成提交：`git add . && git commit -m "feat: xxx"`
3. 推送到远程：`git push origin feature/xxx`
4. 创建 PR 并合并到 main
5. 保留远程分支

### Git 配置

```bash
# 全局配置
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## 关键文件说明

### 核心模块

| 文件 | 说明 |
|------|------|
| `core/chapter_parser.py` | 章节解析器，支持 txt_to_epub 库和正则表达式降级 |
| `core/novel_analyzer.py` | 小说分析器，提取人物、场景、关系等 |
| `core/script_generator.py` | 剧本生成器，转换为剧本结构 |
| `core/yaml_exporter.py` | YAML导出器，验证和格式化输出 |

### API模块

| 文件 | 说明 |
|------|------|
| `api/routes.py` | FastAPI路由定义 |
| `api/models.py` | Pydantic数据模型 |

### LLM模块

| 文件 | 说明 |
|------|------|
| `llm/xunfei_api.py` | 讯飞星火API集成，支持降级响应 |

### 前端模块

| 文件 | 说明 |
|------|------|
| `frontend/src/main.ts` | Vue应用入口 |
| `frontend/src/router/index.ts` | 路由配置 |
| `frontend/src/api/client.ts` | API客户端封装 |
| `frontend/src/types/index.ts` | TypeScript类型定义 |

---

## 待办事项

### 高优先级

- [ ] 完成前端首页实现（深色主题 + 双输入模式）
- [ ] 完成前端预览页实现
- [ ] 完成前端编辑页实现
- [ ] 集成 YAML 编辑器组件
- [ ] 完成单元测试覆盖

### 中优先级

- [ ] 完善前端状态管理（Pinia stores）
- [ ] 优化 LLM 调用性能
- [ ] 添加错误处理和用户提示
- [ ] 完善文档（YAML Schema、API文档）

### 低优先级

- [ ] CLI工具开发
- [ ] 示例文件完善
- [ ] Demo视频制作
- [ ] README完善

---

## 交接检查清单

- [x] 项目结构清晰完整
- [x] 核心模块已实现并通过测试
- [x] API服务已搭建并可运行
- [x] 设计规范已定义（PRODUCT.md, DESIGN.md）
- [x] 实现计划已编写（docs/superpowers/plans/）
- [x] 前端项目已初始化
- [ ] 前端首页实现中
- [ ] 前端预览页待实现
- [ ] 前端编辑页待实现
- [ ] 单元测试需补充
- [ ] 文档需完善

---

## 关键联系人

**原开发者:** wangjian  
**项目路径:** /home/wangjian/agent_project_test/LensQuill  
**虚拟环境:** conda agent_debate

---

## 附录

### 常用命令

```bash
# 激活环境
source ~/miniconda3/etc/profile.d/conda.sh && conda activate agent_debate

# 运行后端
cd /home/wangjian/agent_project_test/LensQuill && python -m uvicorn api.routes:router --reload

# 运行测试
pytest tests/ -v

# 构建前端
cd frontend && npm run build

# 预览前端
cd frontend && npm run preview
```

### 常见问题

**Q: 如何添加新的章节解析模式？**  
A: 修改 `core/chapter_parser.py`，在 `_parse_with_regex` 方法中添加新的正则表达式模式。

**Q: 如何修改 AI 分析逻辑？**  
A: 修改 `core/novel_analyzer.py` 中的提取方法，或调整 `llm/xunfei_api.py` 中的 prompt。

**Q: 如何添加新的 API 端点？**  
A: 在 `api/routes.py` 中添加新的路由函数，确保有相应的测试。

**Q: 前端如何调用后端 API？**  
A: 使用 `frontend/src/api/client.ts` 中封装的 API 函数，所有请求会自动加上 `/api` 前缀。

---

**文档更新日期:** 2026-06-05  
**下次更新:** 前端开发完成后
