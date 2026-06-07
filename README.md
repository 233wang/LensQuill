# LensQuill - AI 小说转剧本工具

将小说文本自动转换为结构化YAML格式剧本的AI工具。

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com)
[![Vue 3](https://img.shields.io/badge/Vue.js-3.3+-green.svg)](https://vuejs.org/)

## 演示视频

观看 LensQuill 的演示视频：

<div align="center">
  <video src="docs/演示demo.mp4" controls width="80%"></video>
</div>

## 项目简介

本工具帮助小说作者将小说作品改编成剧本。支持自动识别章节结构，**按章节整体生成**剧本，包含分镜设计、人物对话、场景描述、人物动作等完整剧本要素。

### 核心特性

- 支持上传 .txt/.md 文件或粘贴小说文本
- 自动章节解析（支持中英文数字章节标题）
- 智能人物、场景识别
- **流式生成** - 实时查看AI生成进度
- 打字机效果显示模型原始输出
- 可视化章节选择（支持选择任意章节处理）
- **撤销/重做** - YAML编辑器支持多步撤销
- YAML格式输出
- 可直接编辑使用的剧本初稿

## 技术栈

- 后端: Python 3.9 + FastAPI
- AI: 讯飞星火API (astron-code-latest)
- 前端: Vue 3 + Composition API + Element Plus + Pinia
- 数据格式: YAML
- 动画: GSAP
- 代码编辑: CodeMirror 6

## 安装方式

```bash
# 克隆仓库
git clone https://github.com/233wang/LensQuill.git
cd LensQuill

# 创建并激活虚拟环境（推荐使用 venv）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装后端依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，填入讯飞星火API密钥
```

### 前端安装

```bash
cd frontend
npm install
```

## 运行方式

```bash
# 启动后端服务
python -m uvicorn api.routes:router --host 0.0.0.0 --port 8000 --reload

# 前端开发服务器（需要先安装依赖）
cd frontend
npm run dev
```

访问地址：
- 前端: http://localhost:3001/
- 后端 API: http://localhost:8000

**注意：** 前端默认运行在 3001 端口，API 请求会通过 Vite 代理转发到后端 8000 端口。

## 项目结构

```
├── core/              # 核心业务逻辑
├── llm/               # LLM集成
├── api/               # Web服务
├── frontend/          # 前端界面
├── cli/               # CLI工具
├── docs/              # 文档
│   └── yaml_schema.md    # YAML Schema 详细说明
├── examples/          # 示例
│   └── input_novel.txt   # 示例小说
├── tests/             # 测试
└── .env               # 环境变量配置
```

## 使用流程

1. **访问首页** - 打开 http://localhost:3001/
2. **输入小说** - 粘贴小说文本或上传 .txt/.md 文件
3. **章节预览** - 查看自动分割的章节列表
4. **生成剧本** - 选择需要处理的章节（最多5章），点击"生成剧本"
5. **查看进度** - 在编辑页实时查看AI生成进度和打字机效果
6. **编辑剧本** - 在YAML编辑器中撤销/重做修改，调整内容
7. **AI对话** - 与AI助手对话，优化剧本细节

## YAML输出格式

输出为结构化YAML格式，包含元信息、人物列表、按章节组织的场景和分镜。

**主要特点：**

- 按章节组织，每个章节包含完整的场景和分镜
- 分镜是剧本的基本单元，包含动作、对话、特效等要素
- 所有文本使用中文，保持文学性和剧本格式的平衡

详见 `docs/yaml_schema.md`。

## 环境变量配置

在 `.env` 文件中配置以下环境变量：

```env
# 讯飞星火API配置（兼容 OpenAI 格式）
OPENAI_API_KEY=your_api_key_here
OPENAI_API_URL=https://maas-coding-api.cn-huabei-1.xf-yun.com/v2
OPENAI_MODEL_ID=qwen3.6-35b-a3b
```

**注意：** 如果不配置 API 密钥，工具仍可运行，但会使用降级模式（简单规则提取）而不是 AI 智能分析。

## 示例

### 输入

```txt
第1章 塞壬小镇

白柳醒来，他发现自己坐在一个车的后座上...
面板上写着【游戏须知】。
...

第2章 塞壬小镇

白柳从车后座探头出来，这是一辆七人座的面包车...
...
```

### 输出

```yaml
script:
  metadata:
    version: "1.0"
    generated_by: "AI Tool v1.0"
    generated_at: "2026-06-07T12:00:00"
    source_chapters: 2
    llm_model: "astron-code-latest"

  characters:
    - id: "char_001"
      name: "白柳"
      role: "protagonist"
      description: "25岁，失业青年，对金钱有强烈渴望..."

  chapters:
    - chapter_index: 1
      chapter_title: "第1章 塞壬小镇"
      scenes:
        - scene_index: 1
          scene_title: "醒来"
          location: "面包车后座"
          shots:
            - shot_index: 1
              shot_type: "内景"
              action: "白柳皱起眉来，手指轻轻敲击着面板边缘。"
              dialogue:
                - character: "白柳"
                  line: "这是哪里？我为什么在这里？"
```

## 快速开始

### 1. 安装依赖

```bash
# 后端
pip install -r requirements.txt

# 前端
cd frontend && npm install
```

### 2. 配置 API 密钥

```bash
cp .env.example .env
# 编辑 .env，填入您的讯飞星火 API 密钥
```

### 3. 运行服务

```bash
# 终端 1：启动后端
python -m uvicorn api.routes:router --host 0.0.0.0 --port 8000 --reload

# 终端 2：启动前端
cd frontend
npm run dev
```

### 4. 使用工具

打开浏览器访问 `http://localhost:3001/`，开始您的剧本创作之旅！

## 开发计划

详见 `docs/design.md` 和 `CLAUDE.md`。

## 贡献指南

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 联系方式

如有问题，请联系项目维护者。
