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

20+ built-in themes. Pick one that matches your story:

| Theme | Vibe | Best for |
|-------|------|----------|
| `midnight-ops` (default) | Dark, technical, glowing accents | Operations, monitoring, tech demos |
| `paper-linen` | 暖纸衬线人文风 | 排版精良的报告、人文叙事 |
| `minimal-doc` | 温暖纸感文档风 | 文档型仪表盘 |
| `command-post` | 冷峻指挥中心风 | 运营监控、情报终端 |
| `fitness-glass` | 健康玻璃环风 | 消费级数据环、健康指标 |
| `warm-editorial` | 暖色调新闻室风 | 内容分析、媒体故事 |
| `monitor-dark` | 暗色运维监控风 | Grafana 风运维仪表盘 |
| `cozy-retreat` | 温暖舒适旅行风 | 暖棕色系的旅行/居家数据 |
| `clean-slate` | 简洁亮色科技风 | 极简风格的科技仪表盘 |
| `design-toolkit` | 设计师工具风 | 设计师审美的看板 |
| `vibe-night` | 音乐暗色律动风 | 暗色音乐风格仪表盘 |
| `crypto-sleek` | 深色金融科技风 | 加密资产、深色金融 |
| `checkout-light` | 亮色支付简洁风 | 支付/电商亮色简洁风 |
| `minimal-tracker` | 极简项目管理风 | 项目跟踪、看板 |
| `ocean-night` | 深海暗色风 | 海洋/能源暗色仪表盘 |
| `error-monitor` | 错误监控暗色风 | 错误日志监控 |
| `growth-analytics` | 产品数据分析风 | 产品增长分析 |
| `deal-room` | 金融暗色交易风 | 金融交易仪表盘 |
| `open-table` | 开源数据暗色风 | 开源数据仪表盘 |
| `amber-console` | 琥珀色复古终端风 | 复古终端风格的运维 |
| `deploy-light` | 亮色部署极简风 | 部署流水/极简风 |

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
