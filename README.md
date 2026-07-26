<div align="center">

# ⭐ vizagent-dashboard

**Turn business requirements into HTML dashboards — Use your own AI**

[![CI](https://github.com/vizagent/dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/vizagent/dashboard/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/vizagent-dashboard)](https://pypi.org/project/vizagent-dashboard/)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**You bring your data + your AI subscription. We compile them into a single HTML dashboard.**

</div>

<br>

<div align="center">
  <a href="https://vizagent.github.io/dashboard/demo/ecommerce">
    <img src="https://raw.githubusercontent.com/vizagent/dashboard/main/docs/assets/demo.gif"
         alt="vizagent-dashboard demo"
         width="720">
  </a>
  <br>
  <sub><i>pip install → one command → interactive HTML dashboard. No database, no server, no hidden API bills.</i></sub>
</div>

<br>

```bash
pip install vizagent-dashboard
vizagent build --data sales.xlsx --requirement "每月销售额趋势" --output dashboard/
# ✓ Dashboard generated in 3.2s → dashboard/output.html
# Open in browser — done.
```

---

## ✨ Features

- **🧠 AI-Powered, Your AI** — Describe your requirements in natural language. Works with your existing AI subscription (Claude, Codex, OpenAI, etc.) — no extra API key to configure, no hidden bills. Agent Skill mode uses your host AI's reasoning; CLI Planner mode uses your own LLM key.
- **🔧 Zero-API Spec Mode** — Prefer no AI at all? Write a structured `DashboardSpec` JSON and compile deterministically — zero LLM calls, zero API cost, works fully offline.
- **📦 Single HTML Output** — One self-contained file. No server, no database, no build step. Drop it on any static host or open directly in a browser.
- **📊 Rich Charts** — Line, bar, pie, scatter, map (China/world), KPI cards — powered by ECharts.
- **🎨 20+ Built-in Themes** — Dark ops, paper brief, warm editorial, command center, fitness glass, music vibe, crypto sleek, terminal amber, and more. Switch with `--theme <name>`.
- **📁 CSV & Excel** — Read from `.csv` or `.xlsx`, multiple sheets supported.
- **✅ Built-in Validation** — Automatic checks for truncation, overlap, zero-size charts, map coverage.
- **🔒 Secure by Default** — Content Security Policy, HTML escaping, path traversal protection.
- **🤖 Agent Skill Ready** — Loadable as Claude Code / Codex skill, uses your host AI's subscription.

---

## 🔑 API Key Model (Clear & Simple)

| Mode | Who pays for AI? | API Key needed? |
|------|-----------------|-----------------|
| **Agent Skill** (Claude/Codex) | **You** — already paying for your AI subscription | The skill uses your host AI's reasoning — no separate key to configure |
| **CLI — Spec mode** (`--spec`) | **Nobody** — compiler is fully deterministic | ❌ No API key needed |
| **CLI — Planner mode** (`--requirement` + optional `--planner`) | **You** — the planner calls your configured LLM | 🟡 Configure your own key via `vizagent config --set api_key=...` |

> This project never provides free API credits. Every LLM call is charged to **your** account or runs on **your** local AI client. No hidden surprises.

---

## 🖼️ Gallery

<div align="center">
  <table>
    <tr>
      <td align="center" width="33%">
        <a href="https://vizagent.github.io/dashboard/demo/ecommerce">
          <img src="https://raw.githubusercontent.com/vizagent/dashboard/main/docs/assets/ecommerce-thumb.png" width="100%">
          <br><b>🛒 电商经营分析</b>
        </a>
        <br>Sales trends, category breakdown, regional map
      </td>
      <td align="center" width="33%">
        <a href="https://vizagent.github.io/dashboard/demo/connectivity">
          <img src="https://raw.githubusercontent.com/vizagent/dashboard/main/docs/assets/connectivity-thumb.png" width="100%">
          <br><b>🌐 全球连接分布</b>
        </a>
        <br>World map, protocol mix, latency heatmap
      </td>
      <td align="center" width="33%">
        <a href="https://vizagent.github.io/dashboard/demo/operations">
          <img src="https://raw.githubusercontent.com/vizagent/dashboard/main/docs/assets/operations-thumb.png" width="100%">
          <br><b>🏥 运营健康监控</b>
        </a>
        <br>System metrics, error rates, SLA tracking
      </td>
    </tr>
  </table>
</div>

---

## 🎨 20+ Built-in Themes

One data file, twenty-plus looks. Pick a theme that matches your story:

| Theme | Vibe | Best for |
|-------|------|----------|
| `paper-linen` | 暖纸衬线人文风 | 排版精良的报告、人文叙事 |
| `minimal-doc` | 温暖纸感文档风 | 文档型仪表盘、读多写少 |
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
| `midnight-ops` | 默认深色酷炫风 | 默认通用主题 |

Switch with `--theme <name>`:

```bash
vizagent build --data sales.xlsx --theme paper-linen --output dashboard/
```

---

## 🚀 Quick Start

### 1. Install

```bash
pip install vizagent-dashboard
```

### 2. Prepare your data

Save your data as CSV or Excel:

```bash
# sales.xlsx
# ┌──────────┬──────────┬──────────┬──────────┐
# │ 月份     │ 销售额   │ 类别     │ 地区     │
# ├──────────┼──────────┼──────────┼──────────┤
# │ 2026-01  │ 128000   │ 数码     │ 华东     │
# │ 2026-02  │ 135000   │ 数码     │ 华东     │
# │ ...      │ ...      │ ...      │ ...      │
# └──────────┴──────────┴──────────┴──────────┘
```

### 3. Build your dashboard

```bash
vizagent build \
  --data sales.xlsx \
  --requirement "月度销售额趋势，按类别和地区拆分，包含关键指标" \
  --output my-dashboard/
```

### 4. Open `my-dashboard/output.html` in your browser

---

## 📖 Usage

```bash
# Spec mode: data file + structured spec → zero API cost
vizagent build --data data.xlsx --spec spec.json --output dashboard/

# Planner mode: data file + natural language → uses your LLM key
vizagent build --data data.xlsx --requirement "按省份的销售额地图" --output dashboard/

# Specify theme
vizagent build --data data.xlsx --theme midnight-ops --output dashboard/

# Full pipeline
vizagent build \
  --data data.xlsx \
  --requirement "展示各品类季度趋势，顶部 KPI 卡片显示总额和增长" \
  --theme paper-brief \
  --output dashboard/
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--data` | required | Path to CSV or Excel file |
| `--requirement` | auto-detect | Business requirement in natural language |
| `--spec` | — | Path to DashboardSpec JSON (zero-API mode) |
| `--theme` | `midnight-ops` | Theme: see the [Themes gallery](#-20-built-in-themes) below — 20+ options |
| `--output` | `./output` | Output directory |
| `--open` | `false` | Open dashboard in browser after build |

---

## 🏗️ Architecture

```
┌──────────────┐    ┌────────────┐    ┌──────────────┐
│  CSV / XLSX  │───▶│  Inventory │───▶│   Compiler   │───▶ output.html
│  (your data) │    │  (analyze) │    │  (generate)  │
└──────────────┘    └────────────┘    └──────────────┘
                          │                  │
                          ▼                  ▼
                   ┌──────────────┐   ┌──────────────┐
                   │ Requirement  │   │  Validator   │
                   │ (NLP → spec) │   │  (quality)   │
                   └──────────────┘   └──────────────┘
```

**Key design**: The Compiler is fully deterministic — no LLM, no API call, no network. The Planner (NLP → spec) runs on **your** AI client (Agent Skill mode) or on **your** configured LLM key (CLI Planner mode). In spec mode, the entire pipeline works offline with zero API cost.

---

## 🤖 Agent Skill Mode

vizagent-dashboard can be loaded as a **Claude Code** or **Codex** skill:

```xml
<skill name="vizagent-dashboard">
  <context>
    You can generate data dashboards using the vizagent tool.
  </context>
  <instruction>
    When the user provides a data file and business requirements:
    1. Analyze the data structure
    2. Design the dashboard layout in DashboardSpec format
    3. Run: vizagent build --data <file> --spec <spec>
    4. Open the output HTML
  </instruction>
</skill>
```

The skill uses **your host AI's own reasoning** — you're already paying for your AI subscription, no extra key to configure.

---

## 🧪 Development

```bash
# Clone
git clone https://github.com/vizagent/dashboard.git
cd skill/

# Install in editable mode
pip install -e ".[dev]"

# Run tests
python -m pytest tests/ -v

# Lint
pip install ruff
ruff check src/ tests/
```

---

## 📄 License

Apache 2.0 © VizAgent Team. See [LICENSE](LICENSE).

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=vizagent/dashboard&type=Date)](https://star-history.com/#vizagent/dashboard&Date)

---

<div align="center">
  <b>No database. No server. Just one HTML file.<br>
  You bring your data and your AI subscription — we do the rest.</b>
  <br><br>
  <a href="https://github.com/vizagent/dashboard/stargazers">
    <img src="https://img.shields.io/github/stars/vizagent/dashboard?style=social" alt="stars">
  </a>
</div>
