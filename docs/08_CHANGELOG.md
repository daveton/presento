# Changelog

## 格式规范

```
## [日期]

### Added / Changed / Fixed
- 改动内容

### Reason
- 为什么做

### Impact
- 是否影响核心流程
- 是否需要更新文档
```

---

## 2026-05-01

### Added
- 初始化项目结构
- 创建分层架构（api/core/infra）
- 实现两阶段 Prompt（Step1结构提取 + Step2PPT重写）
- 添加规则引擎（强制22字/20字/10页限制）
- 实现质量评分系统（70分合格线）
- 首页黑白极简设计
- CI 检查体系（架构/文件大小/导入检查）

### Architecture
- 确定技术栈：Next.js + FastAPI + GPT-4 + python-pptx
- 分层：api（路由）→ core（业务）→ infra（外部依赖）
- Pipeline：解析 → 提取 → 重写 → 规则 → 评分 → 渲染

### Product
- 定位：一键视频转PPT
- 原则：单一入口、单一结果、零选择、可直接用

### Docs
- 创建 00_RULES.md（开发规则）
- 创建 01_PRODUCT.md（产品定义）
- 创建 02_ARCHITECTURE.md（架构说明）
- 创建 03_PIPELINE.md（核心流程）

### Notes
- 确定单一功能方向，拒绝多功能诱惑
- 核心壁垒：规则引擎 + 质量评分 = 稳定输出

---

## 2026-05-02

### Added
- 创建 AI Prompt 约束体系（.ai/ 目录）
- DEV_SYSTEM_PROMPT.txt - 系统级开发约束
- FEATURE_TASK_PROMPT.txt - 任务描述模板
- GUARD_PROMPT.txt - 代码违规检查
- DOC_UPDATE_PROMPT.txt - 文档维护规范

### Reason
- 建立 AI 开发规范，防止架构失控
- 确保每次 AI 生成代码都遵守项目规则
- 实现文档约束 → AI 执行的自动化

### Impact
- 不影响核心流程（纯工具/规范层）
- 提升开发可控性
- 要求每次开发必须先加载 DEV_SYSTEM_PROMPT

### Docs Updated
- [x] 08_CHANGELOG.md

---

## 2026-05-02 (2)

### Changed
- 重构 `core/renderer.py`，集成完整规则引擎
- 添加 `enforce_rules()` - 强制标题/要点/页数限制
- 添加 `score_slides()` - 质量评分系统（满分100，合格线60）
- 添加 `rewrite_point()` - 内容优化（短句化、节奏调整）
- 添加 `split_points()` - 自动分页（每页最多5要点）
- 整合用户提供的 `ppt_engine.py` 核心能力

### Reason
- 提升 PPT 输出质量到产品级别
- 确保所有输出符合规则约束（22字/20字/≤10页）
- 实现自动分页，避免单页内容过多

### Impact
- 增强 Pipeline 的 render 步骤
- 不破坏现有架构（保持在 core/ 层）
- 下游调用方式不变（`create_ppt_file()` 接口保持一致）

### Docs Updated
- [x] 08_CHANGELOG.md

---

## 2026-05-02 (3)

### Changed
- 重命名 DESIGN.md → docs/04_DESIGN.md
- 重命名 EXECUTION_SPEC.md → docs/05_EXECUTION_SPEC.md
- 根目录仅保留 README.md

### Reason
- 统一文档结构，所有文档集中在 docs/ 目录
- 建立清晰的文档编号体系

### Impact
- 不影响代码功能
- 文档访问路径变更

### Docs Updated
- [x] 08_CHANGELOG.md

---

## 模板（复制使用）

```
## YYYY-MM-DD

### Added
- 

### Changed
- 

### Fixed
- 

### Reason
- 

### Impact
- 

### Docs Updated
- [ ] 00_RULES.md
- [ ] 01_PRODUCT.md
- [ ] 02_ARCHITECTURE.md
- [ ] 03_PIPELINE.md
```

---

**维护者**: 每次开发后必须更新
