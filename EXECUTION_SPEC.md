# Presento 执行规范 v1.0

> **强制阅读**：任何新需求、修改、优化开始前，必须先完整阅读本规范。

---

## 1. 产品定义（不可偏离）

### 1.1 一句话定位

**Presento = 一键把视频变成可直接讲的 PPT**

### 1.2 核心原则

| 原则 | 说明 | 违反后果 |
|------|------|----------|
| **单一入口** | 只有一个输入框 | 用户迷失 |
| **单一结果** | 只输出 PPT | 决策疲劳 |
| **零选择** | 用户不做任何选项决策 | 使用门槛高 |
| **可直接用** | 下载的 PPT 不需要大改 | 价值感低 |

### 1.3 不做的事情（红线）

- ❌ 不输出小红书笔记
- ❌ 不输出视频脚本
- ❌ 不做复杂选项配置
- ❌ 不做多种风格选择（MVP阶段）
- ❌ 不做用户系统（MVP阶段）

---

## 2. 技术架构

### 2.1 技术栈（已确定）

| 层级 | 技术 | 变更需审批 |
|------|------|-----------|
| 前端 | Next.js 14 + TailwindCSS | ✅ |
| 后端 | FastAPI (Python) | ✅ |
| AI | GPT-4 (OpenAI API) | ✅ |
| PPT | python-pptx | ✅ |

### 2.2 项目结构

```
presento/
├── DESIGN.md              # 设计文档
├── EXECUTION_SPEC.md      # 本文件（执行规范）
├── frontend/              # Next.js
│   ├── app/
│   │   ├── page.tsx       # 首页
│   │   └── result/        # 结果页
│   └── ...
└── backend/               # FastAPI
    ├── main.py
    ├── api/generate.py    # /api/generate
    └── services/
        ├── llm_service.py # GPT调用
        └── ppt_engine.py  # PPT渲染
```

---

## 3. UI 规范

### 3.1 色彩系统

| Token | 值 | 用途 |
|-------|-----|------|
| `--st-primary` | `#4D77FF` | 主按钮、行动点 |
| `--st-bg` | `#F5F7FF` | 页面背景 |
| `--st-surface` | `#FFFFFF` | 卡片背景 |
| `--st-text` | `#1E293B` | 主文字 |
| `--st-text-sub` | `#475569` | 次级文字 |

### 3.2 组件规范

#### 主按钮
- 高度：72px
- 圆角：999px（胶囊形）
- 背景：渐变 `#4D77FF` → `#6B8FFF`
- 阴影：`0 8px 20px rgba(77, 119, 255, 0.30)`

#### 卡片
- 圆角：32px
- 背景：白色
- 阴影：`0 12px 36px rgba(77, 119, 255, 0.10)`
- 边框：1px solid `#E2E8F0`

---

## 4. 功能规范

### 4.1 用户流程

```
首页输入 → 点击生成 → AI处理 → 结果页 → 下载PPT
   (5s)      (1s)       (8s)      (1s)
   └────── 总时长控制在 15 秒内 ──────┘
```

### 4.2 API 接口

```
POST /api/generate
Request: { input: string }
Response: { title, slides[], download_url }
```

### 4.3 约束条件

| 约束 | 值 | 超限处理 |
|------|-----|----------|
| 输入长度 | ≤ 5000 字 | 截断提示 |
| PPT 页数 | ≤ 10 页 | 自动分页 |
| 每页要点 | 2-5 条 | 自动拆分 |
| 要点长度 | ≤ 20 字 | 强制截断 |
| 标题长度 | ≤ 22 字 | 强制截断 |

### 4.4 输入验证（新增）

必须过滤无效输入：

```python
def is_valid_content(text):
    if len(text) < 100:
        return False, "Content too short (< 100 chars)"
    if len(text) > 5000:
        return False, "Content too long (> 5000 chars)"
    if text.count('http') > 5:
        return False, "Too many URLs"
    return True, "OK"
```

---

## 5. 规则引擎（核心壁垒）

### 5.0 关键原则（新增）

> **规则不是"建议"，是"强制"**

GPT 经常超约束，后端必须强制裁剪：

```python
def enforce_rules(slide):
    # 强制截断，不警告
    slide["title"] = slide["title"][:22]
    slide["points"] = slide["points"][:5]
    slide["points"] = [p[:20] for p in slide["points"]]
    return slide
```

### 5.0.1 内容重写层（新增）

PPT 不是原文压缩，必须重写：

```
原文：
短视频要在前3秒抓住用户注意力，否则会被划走

重写后：
前3秒决定生死
抓不住 → 被划走
```

重写规则：
1. 长句拆短句
2. 强制口语化
3. 增加节奏（换行/对比）
4. 去掉废话
5. 每行 ≤ 20 字

流程：
```
原始内容
↓
结构提取
↓
💥 内容重写（适合PPT表达）
↓
规则引擎
↓
渲染
```

### 5.1 优先级（不可更改顺序）

```
P0 (绝不妥协):
  1. 标题 > 22 字 → 智能截断
  2. 要点 > 5 条 → 自动分页
  3. 单条 > 20 字 → 强制换行/截断

P1 (动态调整):
  4. 2-3 条 → 28pt 大字号
  5. 4-5 条 → 24pt 中字号
  6. 6-8 条 → 双列 + 20pt

P2 (体验优化):
  7. 每页预留 20% 留白
  8. 行间距 1.2-1.5 倍
```

### 5.2 布局类型

```python
LAYOUTS = {
    "cover": {
        "type": "TITLE_ONLY",
        "title_max": 22,
    },
    "content": {
        "type": "TITLE_BULLET",
        "points_max": 5,
        "font_size_map": {2: 28, 3: 28, 4: 24, 5: 24}
    }
}
```

---

## 6. LLM 提示词规范

### 6.1 System Prompt

```
You are a professional PPT content designer.

Constraints (must follow):
1. Main title ≤ 22 Chinese characters
2. Each page title ≤ 18 Chinese characters
3. Each page has 2-5 bullet points
4. Each bullet point ≤ 20 Chinese characters
5. Total pages ≤ 10 pages
6. Output must be JSON only, no explanations

Output format:
{
  "title": "...",
  "slides": [{"type": "...", "title": "...", "points": []}]
}
```

### 6.2 输出格式

```json
{
  "title": "PPT主标题（≤22字）",
  "slides": [
    {
      "type": "cover",
      "title": "封面标题",
      "subtitle": "副标题"
    },
    {
      "type": "content", 
      "title": "内容页标题（≤18字）",
      "points": ["要点1（≤20字）", "要点2", "要点3"]
    }
  ]
}
```

---

## 6.3 质量评分系统（新增）

必须保证输出质量稳定：

```python
def score_ppt(slides):
    score = 100
    
    for slide in slides:
        # 要点太少扣分
        if len(slide.get("points", [])) < 2:
            score -= 20
        
        # 超长内容扣分
        if any(len(p) > 20 for p in slide.get("points", [])):
            score -= 10
        
        # 标题太长扣分
        if len(slide.get("title", "")) > 22:
            score -= 15
    
    return score

def generate_with_fallback(input_text):
    """带重试的生成"""
    for attempt in range(3):
        content = call_llm(input_text)
        score = score_ppt(content["slides"])
        
        if score >= 70:
            return content
        
        # 分数不够，加强提示词重试
        input_text = add_constraints_hint(input_text)
    
    # 3次都失败，强制裁剪
    return enforce_all_rules(content)
```

**合格标准：score ≥ 70**

---

## 7. 开发流程

### 7.1 需求评审清单

任何新需求必须通过以下检查：

- [ ] 是否符合"单一功能"原则？
- [ ] 是否增加用户决策成本？
- [ ] 是否能在 15 秒内完成？
- [ ] 是否影响现有约束条件？
- [ ] 是否需要修改规则引擎？

### 7.2 代码审查要点

- [ ] 是否遵守颜色 Token 规范？
- [ ] 主按钮是否只有一个？
- [ ] 是否处理超长内容截断？
- [ ] 是否返回结构化 JSON？
- [ ] 是否有 fallback/mock 数据？

---

## 8. 里程碑

### Week 1: MVP（必须完成）
- [ ] 首页输入框 + 生成按钮
- [ ] /api/generate 接口
- [ ] LLM 生成结构化内容
- [ ] 规则引擎 + python-pptx
- [ ] 结果页 + 下载功能

### Week 2: 优化
- [ ] 加载动画
- [ ] 错误处理
- [ ] 响应式适配

### Week 3+: 扩展
- [ ] 在线预览
- [ ] 埋点统计
- [ ] 模板选择

---

## 9. 决策记录

| 日期 | 决策 | 决策人 |
|------|------|--------|
| 2024-05-01 | Web 版优先 | 产品 |
| 2024-05-01 | 单一功能（视频→PPT） | 产品 |
| 2024-05-01 | 同步请求优先 | 技术 |
| 2024-05-01 | 代码写死布局（无模板） | 技术 |

---

## 10. 附录

### 相关文档

- `DESIGN.md` - 详细设计文档
- `backend/requirements.txt` - Python 依赖
- `frontend/package.json` - Node 依赖

### 快速命令

```bash
# 启动后端
cd backend && python -m uvicorn main:app --reload

# 启动前端
cd frontend && npm run dev
```

---

**最后更新：2024-05-01**

**规范状态：生效中**
