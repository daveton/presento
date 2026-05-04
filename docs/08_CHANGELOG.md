# Changelog

## 格式规范（产品决策日志）

```
## [日期]

### Added / Changed / Fixed
- 改动内容

### Reason
- 为什么做（假设/背景）

### Expected
- 预期效果（希望发生什么）
- 可量化的目标（如有）

### Result（上线后补）
- 实际效果（数据或主观评价）
- 与预期的差距

### Decision
- 保留 / 回滚 / 优化
- 下一步行动

### Impact
- 是否影响核心流程
- 是否需要更新文档

### Docs Updated
- [ ] 00_RULES.md
- [ ] 01_PRODUCT.md
- [ ] 02_ARCHITECTURE.md
- [ ] 03_PIPELINE.md
```

> 🎯 **关键原则**：没有 Result 的 Changelog 是开发日记，有 Result 的才是产品决策系统。

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

## 2026-05-02 (4)

### Added
- 创建 tests/ 目录，添加规则引擎测试套件
- test_rules.py - 独立测试（不依赖外部库）
- test_cases.py - 5个真实测试用例数据
- 测试覆盖：规则引擎、质量评分、内容重写

### Test Results
- ✅ Rule Enforcement: 通过
- ✅ Quality Scoring: 通过（高分100，低分55）
- ✅ Content Rewrite: 通过（替换/截断/清理）

### Expected
- 规则引擎在边界情况下稳定工作
- 质量评分能区分好坏内容
- 内容重写符合预期（短句化、节奏化）

### Result
- 全部通过，规则引擎可靠
- 评分系统：高质量100分，低质量55分（<60触发阈值）
- 内容重写："因为"→"原因："、超长自动截断、去标点

### Decision
- ✅ 保留当前规则引擎
- 下一步：添加更多口语化表达替换

### Impact
- 确保核心规则引擎稳定工作
- 可验证自动分页、长度限制、质量评分

### Docs Updated
- [x] 08_CHANGELOG.md

---

## 2026-05-04

### Fixed
- 修复 CORS 跨域错误，添加端口 5668 到允许列表
- 更新 `backend/main.py` 和 `docker-compose.yml` 的 ALLOWED_ORIGINS

### Reason
- 前端访问 backend 时遇到 "No 'Access-Control-Allow-Origin' header" 错误
- 前端运行在 port 5668，但 CORS 配置只允许 5666/3000

### Expected
- 消除跨域错误，前后端正常通信
- 支持 IP 地址访问（192.168.10.105）

### Result
- ✅ CORS 错误已解决
- ✅ 前后端通信正常

### Decision
- ✅ 保留当前 CORS 配置
- 支持动态扩展 via ALLOWED_ORIGINS 环境变量

### Impact
- 影响部署配置，不影响核心代码逻辑

### Docs Updated
- [x] 08_CHANGELOG.md

---

## 2026-05-02 (5)

### Added
- 可用性测试框架（产品价值验证层）
- `test_usability.py` - 可讲性/惊喜感/信息密度评分
- `USABILITY_VALIDATION_PLAN.md` - 5个真实案例验证计划
- 用户反馈收集模板（核心问题：你会用这个讲吗？）

### Reason
- 工程正确性测试 ≠ 产品价值验证
- 需要验证：生成的PPT有没有人愿意用

### Expected
- 建立"可用性评分"体系（可讲性≥60，综合≥70）
- 跑通5个真实案例
- 获得至少2个"会直接用"的反馈

### Result（待验证）
- 框架已建立，真实测试待执行
- 需配置API key后生成PPT验证

### Decision
- 保留框架，立即执行真实验证
- 下一步：跑5个案例，找人试用

### Metrics
| 维度 | 权重 | 合格线 |
|------|------|--------|
| 可讲性 | 50% | ≥60 |
| 惊喜感 | 30% | ≥40 |
| 信息密度 | 20% | ≥60 |

### Impact
- 不修改代码，增加验证层
- 建立产品价值判断标准

### Docs Updated
- [x] 08_CHANGELOG.md

---

## 模板（复制使用 - 升级版）

```
## YYYY-MM-DD

### Added / Changed / Fixed
- 

### Reason
- 为什么做（假设/背景）

### Expected
- 预期效果（希望发生什么）
- 可量化的目标（如有）

### Result（上线后补）
- 实际效果（数据或主观评价）
- 与预期的差距

### Decision
- 保留 / 回滚 / 优化
- 下一步行动

### Impact
- 是否影响核心流程
- 是否需要更新文档

### Docs Updated
- [ ] 00_RULES.md
- [ ] 01_PRODUCT.md
- [ ] 02_ARCHITECTURE.md
- [ ] 03_PIPELINE.md
```

---

**使用指南**：
1. 开发前填写 **Expected**（想清楚目标）
2. 上线后填写 **Result**（验证效果）
3. 根据结果做 **Decision**（决策沉淀）
4. 无 Result 的条目标记为 **（待验证）**

---

**维护者**: 每次开发后必须更新
