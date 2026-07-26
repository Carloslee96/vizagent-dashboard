# Skill 改造中断交接

> 日期：2026-07-27
>
> 状态：**未完成检查点，禁止视为可发布版本**
>
> 中断原因：用户要求完成计划第 1 步后停止，交由其他 AI 继续。

## 已完成的计划步骤

- 已核对 Git 最近提交、共享工作区未提交文件和 `CHANGELOG.md`。
- 已完整读取 `skill-creator` 规范及 `openai.yaml` 字段规范。
- 已确认 Claude CLI 留下的两个未跟踪示例：
  - `skill/examples/ecommerce/spec-trend.json`
  - `skill/examples/gobalplatform/`
- 上述示例属于既有共享工作区内容，本检查点没有修改或纳入提交。

## 中断前已经产生的 WIP

这些改动发生在用户发出停止指令之前，已保留以避免丢失：

- 使用官方脚手架创建 `skill/skills/build-data-dashboard/`；
- 调整 Hatch wheel 包路径和 optional dependencies；
- 增加安全版 Inventory、扩展 `DashboardSpec` 和确定性规划器；
- 开始重写 CLI、离线编译器、静态验证和浏览器验证；
- 引入随包 ECharts 5.5.1、中国/世界 GeoJSON；
- 将 20 个品牌导向主题缩减为 5 个通用主题；
- 增加 `NOTICE`。

## 明确未完成

- `skill/skills/build-data-dashboard/SKILL.md` 仍是脚手架 TODO；
- `agents/openai.yaml` 的中文内容在 Windows 脚手架阶段出现乱码，尚未修复；
- 根目录旧 `skill/SKILL.md` 尚未退役；
- 新 CLI、编译器、地图和验证器尚未完成集成测试；
- 旧 77 个单元测试尚未迁移，主题数量等断言预计会失败；
- wheel 尚未重新构建和执行干净环境导入；
- 固定 Mock Excel 尚未复测；
- 地图截图、离线浏览器和数据覆盖门禁尚未验收；
- README、provenance、SECURITY、SBOM 和第三方权利审计尚未完成；
- ECharts/GeoJSON 已记录初步 NOTICE，但公开发布前仍需许可证复核。

## 当前已知技术状态

中断前仅执行过 Python 语法编译检查，以下文件当时通过：

- `compiler/skeleton.py`
- `inventory/reader.py`
- `planner/heuristic.py`
- `schemas/dashboard_spec.py`
- `cli.py`
- `validation/static.py`
- `validation/browser.py`

语法通过不代表功能通过。

## 下一位 AI 的建议起点

1. 先阅读：
   - `skill/docs/TEST_REPORT_2026-07-27.md`
   - `skill/docs/SKILL_DESIGN.md`
   - 本交接文档。
2. 运行 `git show --stat HEAD`，确认这是 WIP 检查点。
3. 不要先扩功能；先完成可安装 Skill 结构、修复 `openai.yaml` 和 root `SKILL.md` 边界。
4. 执行：

```powershell
$env:PYTHONPATH = (Resolve-Path "skill/src").Path
python -m pytest -q skill/tests
```

5. 修复回归后再构建 wheel，并在无源码路径的临时 venv 中验证：

```powershell
python -m pip wheel --no-deps ./skill
```

6. 最后使用固定 Mock Excel 完成 Inventory、Spec、HTML、验证报告和截图闭环。

## 禁止事项

- 不要把此检查点标记为 `v0.1.0`；
- 不要直接发布 PyPI/GitHub Release；
- 不要把验证器的静态通过当作浏览器或数据覆盖通过；
- 不要覆盖或删除共享工作区既有未提交文件；
- 不要在未完成权利审计前恢复品牌导向主题。
