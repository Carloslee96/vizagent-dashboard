# Release Notes — vizagent-dashboard v0.1.0

> 这是 GitHub Release 的正文草稿。发布时把本文件内容粘贴到
> 「Describe this release」框即可（release.yml 已配 `generate_release_notes: true`，
> 可在其自动生成的基础上替换为本草稿）。

## 一句话

把 CSV / Excel 数据 + 一句业务需求，编译成一个**自包含、可离线打开、内置质量门禁**的 HTML 大屏。不需要数据库、不需要服务端、不需要额外的 API Key。

## 安装

```bash
pip install vizagent-dashboard
```

需要浏览器门禁（可选）：

```bash
pip install "vizagent-dashboard[browser]"
playwright install chromium
```

## 30 秒上手

```bash
vizagent build --data sales.xlsx --requirement "每月销售额趋势，按类别和地区拆分" --output dashboard/
# → dashboard/output.html  直接浏览器打开
```

或纯 Spec 模式（零 LLM、完全离线）：

```bash
vizagent build --data sales.xlsx --spec spec.json --output dashboard/
```

## 本次发布包含什么

### 双模式架构
- **Agent Skill 模式**：作为 Claude Code / Codex 的可加载 Skill，由你已有的 AI 订阅承担推理，编写 `DashboardSpec`，再调用 CLI 编译验证——本仓库不收任何额外 API Key。
- **CLI 模式**：`--spec`（确定性编译）与 `--requirement`（确定性关键词规划）全程不调 LLM，可离线运行。

### 编译内核
- 确定性编译器（无 LLM / 无网络），输出可复现。
- 图表：折线、柱状、饼图、散点、KPI 卡片、中国地图、世界地图（ECharts 5.5.1 内嵌，支持离线渲染）。
- CSV / Excel 多 Sheet 读取，逐 Sheet、逐行数据覆盖追踪。
- 5 个 clean-room 通用主题：`midnight-ops`、`paper-light`、`warm-editorial`、`clinical-light`、`signal-dark`。无第三方品牌名或专有资产。旧主题 ID 作为别名兼容映射。
- 单文件 HTML 产物（embedded 离线 / cdn 两种部署模式）。

### 质量门禁
- 静态门禁：HTML 转义、Content Security Policy、路径穿越防护、空 series / 未绑定地图 / 字段缺失阻断。
- 浏览器门禁（可选，Playwright）：截断、重叠、零尺寸图表、地图注册与渲染、Tab 切换后隐藏图不再误报。
- 逐行数据覆盖报告。

### 工程化
- Hatch 打包，干净 venv 可安装、可导入、可执行。
- ruff lint 全绿；97 个单元 + 契约测试通过。
- GitHub Actions：Windows / macOS / Ubuntu × Python 3.10–3.12，含 CLI 与 wheel 契约 job。
- 完整 provenance 审计（`tools/upstream-manifest.toml`）、SBOM、NOTICE、SECURITY、CONTRIBUTING。

### 权利审计（已核实）
- 两份 GeoJSON（china.json / world.json）经逐字节比对，确认均来自 npm `echarts@4.9.0`（Apache 2.0，可再分发），纠正了设计文档误写的「DataV」来源。
- ECharts 运行时 5.5.1（Apache 2.0）内嵌。
- 5 个主题为 clean-room 原创，经 `docs/THEME_AUDIT.md` 关键词审计无品牌残留。

## 已知限制

- `--requirement` 规划器为确定性关键词匹配，复杂表结构可能产出空 Spec；复杂场景建议用 Agent Skill 模式或手写 `--spec`。
- 浏览器门禁需额外安装 Playwright 与 Chromium。
- GitHub Pages 在线 demo 站与演示 GIF 暂未提供；请用 `examples/ecommerce/` 本地构建查看。
- 暂未发布到 PyPI（v0.1.0 仅 GitHub Release；PyPI 发布待 maintainer 执行）。

## 验证

```bash
git clone https://github.com/vizagent/dashboard.git
cd skill
pip install -e ".[dev]"
python -m pytest tests/ -q -k "not e2e and not real"
```

## 致谢

- [Apache ECharts](https://github.com/apache/echarts) — 图表渲染运行时与 GeoJSON 地图数据。
- 底层边界数据源自 Natural Earth（公共领域）。

## 许可证

Apache License 2.0 © VizAgent Team。
