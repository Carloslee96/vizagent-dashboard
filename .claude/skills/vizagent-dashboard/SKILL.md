---
name: vizagent-dashboard
description: 给数据自动生成离线可打开的 HTML 数据大屏。输入 CSV/Excel 文件，自动分析字段、选图表、生成 ECharts 单文件大屏。支持折线、柱状、饼图、KPI、地图等多种图表和 25 个主题切换。
user-invocable: true
argument-hint: "[build|compile|inventory|validate] [--data <file>] [--requirement <需求>]"
allowed-tools:
  - Bash(vizagent *)
  - Bash(pip show vizagent-dashboard)
  - Bash(vizagent --help)
  - Bash(vizagent build *)
  - Bash(vizagent inventory *)
  - Bash(vizagent compile *)
  - Bash(vizagent validate *)
  - Bash(vizagent skill *)
---

# vizagent-dashboard

给数据，自动出大屏。把 CSV / Excel 编译成单个可离线打开的 HTML 数据大屏——不用数据库、不用服务器、不用 API Key。编译器完全确定性，无 LLM 调用，输出可复现。

## 前置依赖

本 Skill 调用 `vizagent` CLI。若未安装：

```
pip install vizagent-dashboard
```

若提示找不到 `vizagent` 命令，先确认：`pip show vizagent-dashboard`。

## 触发条件

- **生成大屏**：用户说"做个大屏"、"生成大屏"、"数据可视化"、"出个看板"、"自动出图"等
- **数据文件**：用户给了 CSV 或 Excel（.xlsx / .xls），想变成可交互 HTML 大屏
- **分析数据**：用户说"帮我分析一下这个数据"、"看看数据趋势"，且手头有表格文件
- **快速看板**：临时报表、经营分析看板、运营监控面板

不触发：用户只问数据分析结论，没有可视化/大屏需求。

## 工作流

### Step 1: 确认数据文件

找到用户的 CSV / Excel 路径。没有就先问清楚数据在哪。

### Step 2: 盘点数据（可选但推荐）

```
vizagent inventory --data <文件路径>
```

读 `data.inventory.json` 了解 sheet、列名、数据类型、行数——**永远不要猜列名**。

### Step 3: 生成大屏

#### 方式 A：自动模式（最省事，默认）

```
vizagent build --data <文件路径>
```

自动分析字段类型 → 选图表 → 生成 HTML，无需写任何需求。

#### 方式 B：微调模式

```
vizagent build --data <文件路径> --requirement "要用尽可能多类型的图表，暖色主题"
```

`--requirement` 影响：
- `尽可能多类型` / `丰富` / `各种图表` → 自动分发多种图表类型（按各 sheet 字段形态分配）
- `用雷达图` / `漏斗图` / `仪表盘` / `南丁格尔` / `树图` / `面积` / `热力` → 点名具体类型（按字段兼容性分配，不兼容自动回退）
- `只展示饼图` / `仅展示柱状` → 全局强制单一图表类型
- `浅色` / `明亮` / `纸张` → paper-light 主题；`暖色` / `珊瑚` → coral-warm 主题
- `分页` / `多页签` → tabs 多页签布局
- `地图` → 优先出地图

#### 方式 C：Spec 模式（完全手动）

```
vizagent plan --data <文件路径> --requirement "月度趋势、品类占比、区域地图" --output dashboard.spec.json
# 用户确认/修改 Spec 后
vizagent compile --data <文件路径> --spec dashboard.spec.json --output dashboard/
vizagent validate --data <文件路径> --spec dashboard.spec.json --html dashboard/output.html
```

### Step 4: 输出

默认输出到 `output/`：`output.html`（自包含，ECharts 已内嵌，双击即看）、`dashboard.spec.json`、`data.inventory.json`、`validation.report.json`、`build-manifest.json`。向用户报告路径，可加 `--open` 自动打开。

## 主题

共 25 个主题。原创 5 个：

| 主题 ID | 风格 | 适合 |
|---------|------|------|
| `midnight-ops`（默认） | 深靛灰背景、蓝绿数据色 | 运营监控、技术演示 |
| `paper-light` | 暖白纸张、墨色文字 | 经营汇报、长时间阅读 |
| `warm-editorial` | 浅米色、暗红重点 | 内容分析、趋势故事 |
| `clinical-light` | 冷白、蓝青强调 | 健康、设备、服务质量 |
| `signal-dark` | 炭黑、琥珀青信号 | 告警、基础设施 |

去品牌引入 20 个：`coral-warm` / `obsidian-glass` / `parchment-serif` / `trust-blue` / `canvas-dot` / `ops-slate` / `ring-pastel` / `nebula-glow` / `graphite-iris` / `broadsheet` / `fiber-paper` / `grid-azure` / `gilt-navy` / `ember-paper` / `amethyst-glass` / `grove-dark` / `haze-lilac` / `phosphor-green` / `amber-scan` / `mono-noir`（详见 `docs/RELEASE_NOTES_v0.1.4.md`）。也可用 `--theme-dir` 加载自定义主题。

## DashboardSpec 格式（Spec 模式用）

```json
{
  "version": "1.0",
  "title": "Dashboard Title",
  "theme": "midnight-ops",
  "page_mode": "single_page",
  "layout": [
    { "columns": 3, "items": [
      { "chart_type": "kpi", "title": "总营收", "data_sheet": "Sales", "data_field": "revenue", "aggregation": "sum", "width": 1, "height": 1 }
    ]},
    { "columns": 2, "items": [
      { "chart_type": "line", "title": "营收趋势", "data_sheet": "Sales", "x_field": "month", "y_field": "revenue", "width": 1, "height": 1 },
      { "chart_type": "map_china", "title": "省份分布", "data_sheet": "Regions", "x_field": "省份", "y_field": "amount", "width": 2, "height": 2 }
    ]}
  ]
}
```

字段参考：
- `chart_type`: `kpi` | `line` | `area` | `bar` | `pie` | `nightingale` | `treemap` | `funnel` | `gauge` | `radar` | `heatmap` | `scatter` | `map_china` | `map_world` | `table`
- `data_sheet`: 必须与 inventory 中的 sheet 名一致
- `aggregation`（kpi）: `sum` | `avg` | `max` | `min` | `count` | `last`
- `width` 1–4，`height` 1–3
- `map_world` 用 `longitude_field` / `latitude_field` 做散点
- `y_field` 接受字符串或列表（line/bar 多系列；radar 传 ≥2 数值字段列表做维度；scatter 两字段）
- `series_field`（heatmap）: 第二分类维度，与 x_field 构成二维网格

## 常用参数

| 参数 | 说明 |
|------|------|
| `--data <file>` | 数据文件路径（必填） |
| `--requirement <text>` | 业务需求（可选） |
| `--theme <id>` | 主题 ID |
| `--page-mode single_page\|tabs` | 分页模式 |
| `--deployment embedded\|cdn` | 默认 embedded（完全离线） |
| `--output <dir>` | 输出目录 |
| `--open` | 生成后自动浏览器打开 |
| `--browser` | 启用 Playwright 浏览器门禁 |

## 排错

| 症状 | 原因 | 修复 |
|------|------|------|
| 地图无数据 | 区域名不标准 | 用全称（"广东省" 不是 "广东"） |
| 图表空白 | 字段名与 inventory 不符 | 查 `data.inventory.json` 列名 |
| KPI 显示 `—` | 字段非数值或 `data_field` 错 | 确认字段是数值 |
| 覆盖率校验失败 | 某 sheet 行未绑定任何图 | 给该 sheet 加图，或接受不完整覆盖 |
| `is_valid: false` | 图表无 series/数据 | 查 `validation.report.json`，修 Spec 字段绑定 |

## 最佳实践

1. 先看 inventory，别猜列名。
2. 每个图绑定真实 `data_sheet`，覆盖门禁会追踪每行。
3. 图表类型匹配数据形态：时间→折线、分类→柱状、构成→饼图、地理→地图、相关性→散点。
4. KPI 卡放第一行。
5. 中国地图用全称省份名，编译器会规范化自治区。
6. 迭代到 `validation.report.json` 的 `is_valid: true` 再交付。
