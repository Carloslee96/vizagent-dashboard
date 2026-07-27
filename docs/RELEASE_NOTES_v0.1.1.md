# Release Notes — vizagent-dashboard v0.1.1

## 一句话

v0.1.1 是 v0.1.0 之后的首个 PyPI 可安装版本。功能与 v0.1.0 一致，新增 PyPI 自动发布通路。

## 安装

```bash
pip install vizagent-dashboard==0.1.1
```

需要浏览器门禁（可选）：

```bash
pip install "vizagent-dashboard[browser]==0.1.1"
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

## 相对 v0.1.0 的变化

- **PyPI 上线**：`release.yml` 启用 Trusted Publisher（OIDC），打 tag 后自动发 PyPI，无需手工上传或长期 token。
- 版本号 0.1.0 → 0.1.1（PyPI 不允许覆盖版本号，v0.1.0 仅 GitHub，PyPI 从本版起）。

## 功能清单（与 v0.1.0 一致）

- 双模式架构：Agent Skill（宿主 LLM 推理）+ CLI（确定性编译，离线零 API）
- 图表：折线、柱状、饼图、散点、KPI 卡片、中国地图、世界地图（ECharts 5.5.1 内嵌）
- CSV / Excel 多 Sheet，逐行数据覆盖追踪
- 5 个 clean-room 主题：`midnight-ops`、`paper-light`、`warm-editorial`、`clinical-light`、`signal-dark`
- 质量门禁：静态 + 可选 Playwright 浏览器门禁
- 安全基线：HTML 转义 + CSP + 路径穿越防护
- 权利审计：两份 GeoJSON 经逐字节比对确认来自 echarts@4.9.0（Apache 2.0）

## 已知限制

- `--requirement` 规划器为确定性关键词匹配，复杂表结构可能产出空 Spec；复杂场景建议用 Agent Skill 模式或手写 `--spec`。
- 浏览器门禁需额外安装 Playwright 与 Chromium。

## 验证

```bash
git clone https://github.com/Carloslee96/vizagent-dashboard.git
cd vizagent-dashboard
pip install -e ".[dev]"
python -m pytest tests/ -q -k "not e2e and not real"
```

## 致谢

- [Apache ECharts](https://github.com/apache/echarts) — 图表渲染运行时与 GeoJSON 地图数据。
- 底层边界数据源自 Natural Earth（公共领域）。

## 许可证

Apache License 2.0 © VizAgent Team。
