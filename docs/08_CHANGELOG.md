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
