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

- **🧠 AI-Powered, Your AI** — In Agent Skill mode the host AI (Claude, Codex, …) authors the `DashboardSpec` using reasoning you already pay for — no extra API key, no hidden bills.
- **🔧 Zero-API Spec Mode** — Prefer no AI at all? Write a structured `DashboardSpec` JSON and compile deterministically — zero LLM calls, zero API cost, works fully offline. The `--requirement` flag steers a built-in deterministic planner (still no LLM).
- **📦 Single HTML Output** — One self-contained file. No server, no database, no build step. Drop it on any static host or open directly in a browser.
- **📊 Rich Charts** — Line, bar, pie, scatter, map (China/world), KPI cards — powered by ECharts, inlined for offline use.
- **🎨 5 Clean-Room Themes** — `midnight-ops`, `paper-light`, `warm-editorial`, `clinical-light`, `signal-dark`. No third-party brand names or assets. Switch with `--theme <name>`.
- **📁 CSV & Excel** — Read from `.csv` or `.xlsx`, multiple sheets supported with per-sheet data-coverage tracking.
- **✅ Built-in Validation** — Static + optional Playwright checks for truncation, external-script dependency, empty series, unbound maps, and row-level data coverage.
- **🔒 Secure by Default** — Content Security Policy, HTML escaping, path traversal protection.
- **🤖 Agent Skill Ready** — Loadable as a Claude Code / Codex skill under `skills/build-data-dashboard/`.

---

## 🔑 API Key Model (Clear & Simple)

| Mode | Who pays for AI? | API Key needed? |
|------|-----------------|-----------------|
| **Agent Skill** (Claude/Codex) | **You** — already paying for your AI subscription | The skill uses your host AI's reasoning — no separate key to configure |
| **CLI — Spec mode** (`--spec`) | **Nobody** — compiler is fully deterministic | ❌ No API key needed |
| **CLI — Planner mode** (`--requirement`) | **Nobody** — a built-in deterministic planner steers the Spec from keywords | ❌ No API key needed |

> There is no `config` command and no `--planner` flag. The compiler and planner never call an LLM. All AI reasoning happens in your host agent (Agent Skill mode) — charged to your own subscription, never to this project.

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

## 🎨 5 Clean-Room Themes

One data file, five looks — each a generic, brand-free token set. Pick a theme that matches your story:

| Theme | Vibe | Best for |
|-------|------|----------|
| `midnight-ops` (default) | 深靛灰背景、蓝绿数据色 | 运营监控、技术演示 |
| `paper-light` | 暖白纸张、墨色文字 | 经营汇报、长时间阅读 |
| `warm-editorial` | 浅米色、暗红重点 | 内容分析、趋势故事 |
| `clinical-light` | 冷白、蓝青强调 | 健康、设备、服务质量 |
| `signal-dark` | 炭黑、琥珀青信号 | 告警、基础设施、高优先级状态 |

Legacy IDs (`monitor-dark`, `paper-brief`, `paper-linen`, `minimal-doc`, `clean-slate`, `fitness-glass`, `command-post`, `amber-console`) resolve to the closest theme above.

Switch with `--theme <name>`:

```bash
vizagent build --data sales.xlsx --theme paper-light --output dashboard/
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

# Planner mode: data file + requirement keywords → deterministic Spec (still no LLM)
vizagent build --data data.xlsx --requirement "按省份的销售额地图" --output dashboard/

# Specify theme
vizagent build --data data.xlsx --theme midnight-ops --output dashboard/

# Full pipeline
vizagent build \
  --data data.xlsx \
  --requirement "展示各品类季度趋势，顶部 KPI 卡片显示总额和增长" \
  --theme paper-light \
  --output dashboard/
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--data` | required | Path to CSV or Excel file |
| `--requirement` | `""` | Business requirement; steers the deterministic planner (no LLM) |
| `--spec` | — | Path to DashboardSpec JSON (zero-API mode) |
| `--theme` | from Spec or `midnight-ops` | Theme override; see [Themes](#-5-clean-room-themes) |
| `--page-mode` | `single_page` | `single_page` or `tabs` |
| `--deployment` | `embedded` | `embedded` (offline) or `cdn` |
| `--output` | `./output` | Output directory |
| `--browser` | `false` | Run the Playwright validation gate |
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

**Key design**: The Compiler is fully deterministic — no LLM, no API call, no network. The Planner (requirement → Spec) is a deterministic keyword planner, not an LLM. In Agent Skill mode the host AI authors the `DashboardSpec` using its own reasoning. In spec mode, the entire pipeline works offline with zero API cost.

---

## 🤖 Agent Skill Mode

vizagent-dashboard ships as a loadable **Claude Code / Codex** skill at `skills/build-data-dashboard/` (with `SKILL.md` + `agents/openai.yaml`). The host AI reads the inventory, authors a `DashboardSpec`, then runs the `vizagent` CLI to compile and validate:

```bash
vizagent inventory --data <file> --output data.inventory.json
vizagent compile  --data <file> --spec <spec.json> --output dashboard/
vizagent validate --data <file> --spec <spec.json> --html dashboard/output.html
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
