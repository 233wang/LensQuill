# AI 小说转剧本工具

将3个章节以上的小说文本自动转换为结构化YAML格式剧本的AI工具。

## 项目简介

本工具帮助小说作者将小说作品改编成剧本。支持自动识别章节结构、提取人物信息、分析场景情节，并生成可编辑的YAML格式剧本初稿。

## 功能特性

- 支持3个及以上章节的小说输入
- 自动章节解析
- AI人物识别与关系分析
- 场景与情节提取
- YAML格式输出
- 可编辑剧本初稿

## 技术栈

- 后端: Python + FastAPI
- AI: 讯飞星火API (Qwen3.6-35B-A3B)
- 前端: Vue 3 + Pinia
- 数据格式: YAML

## 安装方式

```bash
# 克隆仓库
git clone https://github.com/your-username/ai-novel-to-script.git
cd ai-novel-to-script

# 创建虚拟环境
conda create -n agent_debate python=3.9
conda activate agent_debate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，填入讯飞星火API密钥
```

## 运行方式

```bash
# 启动后端服务
python -m api.main

# 前端开发服务器
cd frontend
npm install
npm run dev
```

## 项目结构

```
├── core/              # 核心业务逻辑
├── llm/               # LLM集成
├── api/               # Web服务
├── frontend/          # 前端界面
├── cli/               # CLI工具
├── docs/              # 文档
├── examples/          # 示例
└── tests/             # 测试
```

## YAML输出格式

输出为结构化YAML格式，包含元信息、人物列表、场景列表、情节节点等。详见 `docs/yaml_schema.md`。

## 示例

输入：
```
第一章 雨夜
林舟撑着伞，快步穿过狭窄的巷子...

第二章 旧书店
第二天，林舟来到城西的旧书店...

第三章 真相
"那本书里记载着一个秘密..."
```

输出：结构化YAML剧本文件

## 开发计划

详见 `docs/design.md` 和 `CLAUDE.md`。

## 贡献指南

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 联系方式

如有问题，请联系项目维护者。