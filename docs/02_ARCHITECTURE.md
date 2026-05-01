# 架构说明

> **原则**: 分层清晰，边界明确，可扩展

---

## 目录结构

```
backend/
├── api/              # 路由层（只做输入输出）
│   └── generate.py
├── core/             # 核心业务逻辑
│   ├── pipeline.py   # 唯一入口
│   ├── rules.py      # 规则引擎
│   └── renderer.py   # PPT 渲染
├── infra/            # 外部依赖
│   └── llm/
│       └── client.py # GPT 调用
└── models/           # 数据结构
    └── schemas.py
```

---

## 分层职责

### 1. api/ 层

**职责**: HTTP 请求处理

- 输入验证
- 调用 pipeline
- 返回结果

**禁止**: 业务逻辑、直接调用 LLM

---

### 2. core/ 层

**职责**: 业务核心

| 文件 | 职责 |
|------|------|
| pipeline.py | 串联整个流程 |
| rules.py | 强制规则引擎 |
| renderer.py | PPT 生成 |

**禁止**: 直接调用外部 API

---

### 3. infra/ 层

**职责**: 外部依赖封装

| 目录 | 职责 |
|------|------|
| llm/ | GPT/Claude 调用 |
| storage/ | 文件存储 |

**原则**: 可替换，不影响上层

---

## 数据流向

```
User Input
    ↓
api/generate.py (验证)
    ↓
core/pipeline.py (编排)
    ↓
infra/llm/client.py (结构提取)
    ↓
infra/llm/client.py (内容重写)
    ↓
core/rules.py (强制规则)
    ↓
core/renderer.py (生成 PPT)
    ↓
返回 URL
```

---

## 扩展规则

### 新增功能时：

1. **不影响 Pipeline**: 在现有步骤内扩展
2. **新增步骤**: 必须插入 Pipeline，不得绕过
3. **新增模块**: 按分层放入对应目录

---

## 禁止事项

| 禁止行为 | 原因 |
|----------|------|
| 在 api 层写业务逻辑 | 破坏分层 |
| 绕过 pipeline 直接调用 | 破坏流程 |
| 直接调用 renderer | 缺少规则校验 |
| 修改分层边界 | 架构混乱 |

---

## CI 检查

每次提交自动检查：

```bash
python ci/run_checks.py
```

检查项：
- 架构边界
- 文件大小
- Pipeline 完整性
- 禁止导入

---

**最后更新**: 2026-05-01
