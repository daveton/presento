# Presento

一键把视频变成可直接讲的 PPT。

## 产品定位

**Presento = Turn any video into a ready-to-use presentation**

- 单一入口：粘贴视频链接或文案
- 单一结果：直接下载可用 PPT
- 零选择：用户不做任何配置决策
- 可直接用：下载后无需大改即可演讲

## 技术栈

- **前端**: Next.js 14 + TailwindCSS
- **后端**: FastAPI (Python)
- **AI**: GPT-4 (OpenAI API)
- **PPT**: python-pptx

## 快速开始

### 安装依赖

```bash
# 后端
cd backend
pip install -r requirements.txt

# 前端
cd frontend
npm install
```

### 配置环境变量

```bash
# backend/.env
OPENAI_API_KEY=your_api_key_here
```

### 启动服务

```bash
# 后端（端口 3301）
cd backend
python -m uvicorn main:app --reload

# 前端（端口 3000）
cd frontend
npm run dev
```

## 项目结构

```
presento/
├── DESIGN.md              # 详细设计文档
├── EXECUTION_SPEC.md      # 执行规范（必读）
├── frontend/              # Next.js 前端
│   ├── app/
│   │   ├── page.tsx       # 首页
│   │   └── result/        # 结果页
│   └── ...
└── backend/               # FastAPI 后端
    ├── main.py
    ├── api/
    │   ├── generate.py      # 生成接口
    │   └── templates.py     # 模板列表
    └── core/                # Pipeline V2
        ├── pipeline.py      # 主流程
        ├── intent.py        # 意图识别
        ├── structure.py     # 结构生成
        ├── rewrite.py       # 内容重写
        ├── adapter.py       # 模板适配
        ├── renderer.py      # 默认渲染
        ├── template_config.py   # 模板配置
        └── template_renderer.py # 模板渲染
    └── infra/
        └── llm/
            ├── client.py    # LLM客户端
            └── slides.py    # 幻灯片生成
```

## API 接口

### 生成 PPT

```bash
POST /api/generate
Content-Type: application/json

{
  "input": "视频链接或文案",
  "template": "business"  // 可选: minimal/business/teach
}

Response:
{
  "title": "PPT标题",
  "slides": [...],
  "download_url": "/download/xxx.pptx"
}
```

### 获取模板列表

```bash
GET /api/templates

Response:
{
  "templates": [
    {"id": "minimal", "name": "极简黑白", "description": "通用简洁风格"},
    {"id": "business", "name": "商业风格", "description": "演示文稿4风格"},
    {"id": "teach", "name": "内容讲解", "description": "适合知识讲解"}
  ]
}
```

## 核心特性

### Pipeline V2（意图驱动生成）

- **意图识别**: 自动识别内容类型（教学/解释/商业/实践/汇报）
- **结构重构**: 不按原文顺序，按「问题→方法→能力→结果」重组
- **内容重写**: 长句 → 短句+停顿，像人讲话
- **模板适配**: 2-3套固定模板，不解析只填充

### 规则引擎（自动排版）

- 标题 > 22 字 → 智能截断
- 要点 > 5 条 → 自动截断
- 每页要点 2-5 条
- 要点长度 ≤ 20 字
- 标题口语化: "问题"→"为什么会这样"

## 文档

- [DESIGN.md](DESIGN.md) - 设计决策和架构
- [EXECUTION_SPEC.md](EXECUTION_SPEC.md) - 执行规范（开发前必读）

## 里程碑

- [x] 项目结构设计
- [x] 前端首页 + 结果页
- [x] FastAPI 后端接口
- [x] LLM 提示词优化（结构重构版）
- [x] Pipeline V2（意图→结构→重写→模板）
- [x] 规则引擎实现
- [x] PPT 文件生成
- [x] 模板系统 Lite（2-3套固定模板）
- [x] Rewrite V2（拆句+口语化）
- [ ] 用户验证测试（5个真实案例）
- [ ] 高冲击表达优化

## License

MIT
