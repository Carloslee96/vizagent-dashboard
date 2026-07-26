---
name: vizagent-dashboard
description: Turn business requirements into standalone HTML dashboards — use your own AI
author: VizAgent Team
version: 0.1.0
---

# vizagent-dashboard

Generate professional HTML data dashboards from CSV/Excel files with natural language requirements. Uses **your** AI subscription — no hidden API bills, no free-riding on someone else's credits.

## When to use

- You have tabular data (CSV/XLSX) and want a visual dashboard
- You need quick business intelligence without setting up a BI server
- You want to embed dashboards in reports, emails, or static sites
- You're building an AI agent that needs data visualization capability

## API key model

| Mode | API Key needed? |
|------|----------------|
| **Agent Skill** (Claude/Codex) | Uses your host AI's reasoning — **you're already paying for it**. No separate key to configure. |
| **CLI — Spec mode** (`--spec`) | **No API key needed** — compiler is deterministic, zero LLM calls. |
| **CLI — Planner mode** (`--requirement`) | 🟡 **Configure your own key** via `vizagent config --set api_key=...` or `--planner` flag. |

## Skill configuration

In Agent Skill mode, no API key configuration is required — the skill uses your host AI's native reasoning.

### Optional parameters

- `theme`: Dashboard theme (`midnight-ops`, `paper-brief`, `warm-editorial`)
- `output_dir`: Where to save the generated HTML

## How to use

### Step 1: Install

```bash
pip install vizagent-dashboard
```

### Step 2: User provides

A data file (CSV or Excel) and optionally a business requirement in natural language.

### Step 3: You generate the dashboard

Use the `vizagent` CLI:

```bash
# With business requirement (uses your LLM key if configured)
vizagent build \
  --data {data_path} \
  --requirement "{user_requirement}" \
  --output {output_path}

# Spec mode — zero API cost
vizagent build --data {data_path} --spec spec.json --output {output_path}
```

### Step 4: Present the result

Open the generated HTML file and present it to the user, or provide the path.

## DashboardSpec format

When you need fine-grained control and zero API cost, provide a `--spec` parameter:

```json
{
  "version": "1.0",
  "title": "Dashboard Title",
  "theme": "midnight-ops",
  "layout": [
    {
      "type": "kpi",
      "title": "Total Revenue",
      "data_field": "revenue",
      "aggregation": "sum",
      "width": 1,
      "height": 1
    },
    {
      "type": "chart",
      "chart_type": "line",
      "title": "Revenue Trend",
      "x_field": "month",
      "y_field": "revenue",
      "width": 2,
      "height": 2
    }
  ]
}
```

## Themes

| Theme | Vibe | Best for |
|-------|------|----------|
| `midnight-ops` | Dark, technical, glowing accents | Operations, monitoring, tech demos |
| `paper-brief` | Light, clean, print-friendly | Reports, presentations, PDF export |
| `warm-editorial` | Warm, editorial, story-driven | Newsrooms, content analytics, publishing |

## Best practices

1. Always analyze the data structure first (columns, types, ranges) before designing the layout
2. Match chart types to data: time → line, categories → bar, composition → pie, geography → map
3. Place KPI cards at the top for key metrics
4. Group related charts on the same visual level
5. Validate the output: check for truncated labels, overlapping elements, missing data
6. For multi-sheet Excel files, each sheet can be a separate dashboard page or tab

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Map shows no data | Province names don't match standard names | Use full province names (e.g., "广东省" not "广东") |
| Charts are empty | Data columns don't match spec fields | Check column names in the data file |
| KPI shows 0 | Wrong aggregation or field name | Verify the field exists and has numeric values |
| HTML opens blank | Browser security restrictions | Use `--open` flag or serve via HTTP |


## Examples

### E-commerce dashboard

User: "I have sales.xlsx with monthly revenue by category and region"

```bash
vizagent build --data sales.xlsx --requirement "销售额月度趋势、各品类占比、区域地图" --output dashboard/
```

### Operations monitoring

User: "Monitor server metrics from ops_log.csv"

```bash
vizagent build --data ops_log.csv --requirement "CPU/内存趋势图、错误率、SLA 达标率" --theme midnight-ops --output dashboard/
```

### Global connectivity

User: "Show global connection distribution from connectivity_data.xlsx"

```bash
vizagent build --data connectivity_data.xlsx --requirement "世界地图连接分布、协议占比、延迟热力图" --theme paper-brief --output dashboard/
```
