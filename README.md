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
# 后端（端口 8000）
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
    ├── api/generate.py
    └── services/
        ├── llm_service.py
        └── ppt_engine.py
```

## API 接口

```bash
POST /api/generate
Content-Type: application/json

{
  "input": "视频链接或文案"
}

Response:
{
  "title": "PPT标题",
  "slides": [...],
  "download_url": "/download/xxx.pptx"
}
```

## 核心特性

### 规则引擎（自动排版）

- 标题 > 22 字 → 智能截断
- 要点 > 5 条 → 自动分页
- 2-3 条 → 28pt 大字号
- 4-5 条 → 24pt 中字号
- 自动留白 20%

### 约束条件

- 输入长度 ≤ 5000 字
- PPT 页数 ≤ 10 页
- 每页要点 2-5 条
- 要点长度 ≤ 20 字

## 文档

- [DESIGN.md](DESIGN.md) - 设计决策和架构
- [EXECUTION_SPEC.md](EXECUTION_SPEC.md) - 执行规范（开发前必读）

## 里程碑

- [x] 项目结构设计
- [x] 前端首页 + 结果页
- [ ] FastAPI 后端接口
- [ ] LLM 提示词优化
- [ ] 规则引擎实现
- [ ] PPT 文件生成
- [ ] 联调测试

## License

MIT
