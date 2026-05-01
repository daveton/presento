# AI 开发规则系统

> 每次让 AI 写代码前，必须先加载 `DEV_SYSTEM_PROMPT.txt`

## 使用流程

### 1. 系统约束（必须）
```
[粘贴 DEV_SYSTEM_PROMPT.txt 内容]
```

### 2. 具体任务
```
[粘贴 FEATURE_TASK_PROMPT.txt 内容]
[填入你的具体需求]
```

### 3. 生成代码
AI 输出代码

### 4. 违规检查（可选但建议）
```
[粘贴 GUARD_PROMPT.txt 内容]
[粘贴 AI 生成的代码]
```

### 5. 更新文档（必须）
```
[粘贴 DOC_UPDATE_PROMPT.txt 内容]
```

## Prompt 说明

| 文件 | 用途 | 使用时机 |
|------|------|----------|
| `DEV_SYSTEM_PROMPT.txt` | 系统级约束 | 每次对话开头 |
| `FEATURE_TASK_PROMPT.txt` | 任务描述模板 | 具体开发时 |
| `GUARD_PROMPT.txt` | 违规检查 | 代码生成后 |
| `DOC_UPDATE_PROMPT.txt` | 文档维护 | 开发完成后 |

## 快速开始

复制以下内容开始新的开发任务：

```text
[加载 DEV_SYSTEM_PROMPT.txt]

任务：
[描述你的需求]

要求：
- 不破坏架构
- 遵循现有分层
- 最小改动原则
```

## 注意事项

- 永远不要跳过 `DEV_SYSTEM_PROMPT`
- 如果 AI 拒绝执行，说明需求违反了规则，需要调整
- 每次开发后必须更新 `docs/08_CHANGELOG.md`
