---
name: build-data-dashboard
description: Compile CSV/XLSX tabular data and a DashboardSpec into a single validated offline HTML dashboard with KPIs, charts (line/bar/pie/scatter), China/world maps, theme tokens, and a data-coverage + validation report. Use when the user has a spreadsheet (CSV or XLSX) and wants a standalone HTML dashboard — for business intelligence, reports, monitoring, or embedding into static sites — without a database, server, or paid API. Also use when building an AI agent that needs deterministic data-visualization capability. Works with or without an LLM: the compiler is deterministic and offline.
---

# Build Data Dashboard

Turn CSV/XLSX data into a single, offline, validated HTML dashboard. The compiler is deterministic — no LLM call is required to produce the HTML. In Agent Skill mode you (the host AI) author the `DashboardSpec`; the skill's compiler, inventory, and validator do the rest.

## When to use

- The user has tabular data (`.csv` / `.xlsx`) and wants a visual dashboard.
- The user wants a single self-contained `.html` file (no server, no database, works offline).
- The user wants to embed a dashboard in a report, email, or static site.
- You are building an agent that needs reproducible data visualization.

Do not use for: real-time streaming dashboards, large-scale BI warehouses, or anything requiring a live backend.

## Install

```bash
pip install vizagent-dashboard
```

Optional browser validation gate (Playwright):

```bash
pip install "vizagent-dashboard[browser]"
```

## How it works

```
CSV / XLSX ──► inventory ──► plan ──► DashboardSpec ──► compile ──► output.html
                                 │                       │
                                 └──────── validate ◄────┘
```

`DashboardSpec` is the single source of truth for intent. The compiler does not call any model — given the same Spec and data it produces byte-stable HTML.

## CLI

### `build` — end-to-end (recommended)

```bash
vizagent build --data sales.xlsx --output dashboard/
```

Outputs in `--output`:
- `output.html` — standalone offline dashboard
- `dashboard.spec.json` — the resolved Spec
- `data.inventory.json` — sheet/column/row inventory
- `validation.report.json` — static (+ optional browser) gate
- `build-manifest.json` — chart/coverage/map manifest
- `screenshot.png` — when `--browser` is set

Without `--spec`, a deterministic planner generates a baseline Spec that covers every non-empty sheet. Pass `--requirement` to steer the planner (theme, page mode, explicit chart types like "只展示饼图").

### `inventory` — data profile only (no model)

```bash
vizagent inventory --data sales.xlsx --output data.inventory.json
```

### `plan` — generate a baseline Spec (no model)

```bash
vizagent plan --data sales.xlsx --requirement "月度趋势、品类占比、区域地图" --output dashboard.spec.json
```

### `compile` — compile from an existing Spec

```bash
vizagent compile --data sales.xlsx --spec dashboard.spec.json --output dashboard/
```

### `validate` — validate existing artifacts

```bash
vizagent validate --data sales.xlsx --spec dashboard.spec.json --html dashboard/output.html --output validation.report.json
```

Common flags: `--theme` (override Spec theme), `--page-mode single_page|tabs`, `--deployment embedded|cdn` (default `embedded` = fully offline), `--browser` (run Playwright gate).

## Agent Skill workflow

1. Run `vizagent inventory --data <file>` and read `data.inventory.json` to learn sheets, columns, dtypes, row counts.
2. Author a `DashboardSpec` (JSON) that binds each visual to a real `data_sheet` and field names from the inventory. Cover every non-empty sheet.
3. Run `vizagent compile --data <file> --spec <spec.json> --output <dir>`.
4. Run `vizagent validate ...` (or `--browser` in `build`). The gate fails on: truncated HTML, external script dependencies, charts missing series/data, unbound maps, or incomplete row coverage.
5. Iterate on the Spec until `validation.report.json` reports `is_valid: true`. Present `output.html` to the user.

## DashboardSpec format

```json
{
  "version": "1.0",
  "title": "Dashboard Title",
  "theme": "midnight-ops",
  "page_mode": "single_page",
  "layout": [
    {
      "columns": 3,
      "items": [
        { "chart_type": "kpi", "title": "Total Revenue", "data_sheet": "Sales", "data_field": "revenue", "aggregation": "sum", "width": 1, "height": 1 }
      ]
    },
    {
      "columns": 2,
      "items": [
        { "chart_type": "line", "title": "Revenue Trend", "data_sheet": "Sales", "x_field": "month", "y_field": "revenue", "width": 1, "height": 1 },
        { "chart_type": "map_china", "title": "省份分布", "data_sheet": "Regions", "x_field": "省份", "y_field": "amount", "width": 2, "height": 2 }
      ]
    }
  ]
}
```

Field reference:
- `chart_type`: `kpi` | `line` | `bar` | `pie` | `scatter` | `map_china` | `map_world` | `table`
- `data_sheet`: must match a sheet name from the inventory
- `aggregation` (kpi): `sum` | `avg` | `max` | `min` | `count` | `last`
- `width` 1–4, `height` 1–3
- `map_world` uses `longitude_field` / `latitude_field` for effect-scatter points
- `y_field` accepts a string or a list (multi-series for line/bar; two fields for scatter)

## Themes

Five clean-room themes (no third-party brand names or assets):

| Theme | Vibe |
|-------|------|
| `midnight-ops` (default) | 深靛灰背景、蓝绿数据色，运营监控 |
| `paper-light` | 暖白纸张、墨色文字，经营汇报 |
| `warm-editorial` | 浅米色、暗红重点，内容/趋势故事 |
| `clinical-light` | 冷白、蓝青强调，健康/服务质量 |
| `signal-dark` | 炭黑、琥珀青信号，告警/基础设施 |

Legacy IDs (`monitor-dark`, `paper-brief`, `paper-linen`, `minimal-doc`, `clean-slate`, `fitness-glass`, `command-post`, `amber-console`) resolve to the closest theme above.

## Offline guarantee

`--deployment embedded` (default) inlines the ECharts runtime and China/world GeoJSON into the HTML. The static gate rejects any external `<script src="https://...">`. The result opens and renders fully with no network.

## Best practices

1. Always inspect the inventory first — never guess column names.
2. Bind every visual to a real `data_sheet`; the coverage gate tracks every row.
3. Match chart type to data shape: time → line, categories → bar, composition → pie, geography → map, correlation → scatter.
4. Place KPI cards in the first row.
5. Use full region names for China maps (e.g. "广东省"); the compiler normalizes autonomous regions.
6. Iterate until the validation report is `is_valid: true` before presenting.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Map shows no data | Region names don't match standard names | Use full province names ("广东省" not "广东") |
| Chart is empty | Field names don't match inventory | Check `data.inventory.json` column names |
| KPI shows `—` | Non-numeric field or wrong `data_field` | Verify the field has numeric values |
| Validation fails on coverage | A sheet's rows aren't bound to any visual | Add a visual for that sheet or accept incomplete coverage |
| `is_valid: false` after compile | A chart has no series/data | Inspect `validation.report.json` errors, fix Spec field bindings |
