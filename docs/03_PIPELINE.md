# Pipeline 流程

> **核心**: 稳定输出可直接用的 PPT

---

## 主流程（6步）

```
输入内容
  ↓ Step 1: 解析 (parser)
  ↓ Step 2: 结构提取 (extractor)
  ↓ Step 3: PPT重写 (rewriter)  
  ↓ Step 4: 规则引擎 (rules)
  ↓ Step 5: 质量评分 (scorer)
  ↓ Step 6: 渲染 (renderer)
输出 PPT
```

---

## 各步骤详解

### Step 1: 解析 (parser)

**输入**: 用户原始文本  
**输出**: 标准化文本

**处理**:
- 长度检查（50-5000 字符）
- URL 检测（不超过 10 个）
- 格式清理

---

### Step 2: 结构提取 (extractor)

**输入**: 标准化文本  
**输出**: JSON 结构（章节划分）

**调用**: `infra/llm/client.py`  
**Prompt**: Step 1 结构提取

**输出示例**:
```json
{
  "title": "主题",
  "sections": [
    {"title": "章节1", "summary": "要点"}
  ]
}
```

---

### Step 3: PPT重写 (rewriter)

**输入**: JSON 结构  
**输出**: PPT 内容（带格式）

**调用**: `infra/llm/client.py`  
**Prompt**: Step 2 PPT重写

**关键转换**:
- 长句 → 短句
- 书面语 → 口语化
- 普通文本 → PPT 节奏

**输出示例**:
```json
{
  "title": "PPT标题",
  "slides": [
    {
      "type": "content",
      "title": "页面标题",
      "points": ["短句1", "短句2"]
    }
  ]
}
```

---

### Step 4: 规则引擎 (rules)

**输入**: PPT 内容  
**输出**: 规则校验后的内容

**强制规则**:
| 规则 | 处理 |
|------|------|
| 标题 > 22 字 | 直接截断 |
| 要点 > 5 条 | 只保留前 5 |
| 单条 > 20 字 | 截断到 20 |
| 总页 > 10 页 | 只保留前 10 |

**绝不妥协**。

---

### Step 5: 质量评分 (scorer)

**输入**: 规则后的内容  
**输出**: 分数（0-100）

**评分标准**:
| 检查项 | 扣分 |
|--------|------|
| 要点 < 2 条 | -20 |
| 要点 > 5 条 | -15 |
| 超长内容 | -10 |
| 标题超长 | -15 |

**合格线**: 70 分

**< 70 分**: 触发重试（加强 Prompt）

---

### Step 6: 渲染 (renderer)

**输入**: 最终内容  
**输出**: .pptx 文件

**调用**: `python-pptx`

**生成**:
- 封面页
- 内容页（2-5 要点）
- 字体大小自适应

---

## 重试机制

如果 Step 5 分数 < 70：

```
回到 Step 3
  ↓
使用加强版 Prompt（STRICT_STEP2_PROMPT）
  ↓
重新生成
  ↓
最多重试 3 次
```

3 次后仍不合格：强制规则兜底 → 继续渲染

---

## 关键原则

1. **每步独立**: 可单独测试
2. **不允许跳过**: 必须按顺序执行
3. **每步可观测**: 有日志输出
4. **可回退**: 任一步失败有 fallback

---

## 调试命令

```bash
# 测试 Pipeline
python -c "from core.pipeline import run_pipeline; run_pipeline('测试内容')"

# 检查输出
ls -la outputs/
```

---

**最后更新**: 2026-05-01
