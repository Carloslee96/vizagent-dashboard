# Release Notes — vizagent-dashboard v0.1.4

## 一句话

主题数 5 → 25（去品牌引入 20 个 SaaS 主题），图表类型 8 → 14（新增 area/nightingale/treemap/funnel/gauge/radar/heatmap），planner 用 data_hints 选型，支持 `--theme-dir` 自定义主题。

## 安装

```bash
pip install vizagent-dashboard==0.1.4
```

## 相对 v0.1.3 的变化

### 主题：5 → 25

- **20 个去品牌主题**：从 SaaS 主项目 20 个品牌导向主题去品牌引入——只提取 12 个核心 token + Chart 色板，颜色/圆角 token 逐字节保真，字体栈 `-apple-system`→`system-ui` 归一化，赋纯描述性中性名（如 `grove-dark` / `coral-warm` / `parchment-serif` / `obsidian-glass`），prose 重写剔除全部品牌名/专有色名/签名指纹/定位文案。详见 `docs/THEME_AUDIT.md`。
- **`--theme-dir` 自定义主题**：`build` / `compile` 新增 `--theme-dir <path>`，丢一个 `.md` 到 `~/.vizagent/themes/` 或指定目录即可用自己品牌主题，不 fork、不碰源码。同 id 后者覆盖前者。
- 主题加载改为自动发现（frontmatter 自描述），加主题只需丢一个 .md 文件。

### 图表类型：8 → 14

新增 6 种 ECharts 图表：`area`（面积）、`nightingale`（南丁格尔玫瑰）、`treemap`（矩形树图）、`funnel`（漏斗）、`gauge`（仪表盘）、`radar`（雷达）、`heatmap`（热力图，二维网格 + visualMap）。builder 注册表 + `data_hints` 让 planner 自动识别新类型。

### Planner

- 自动选型从硬编码改为 `data_hints` 注册表查询（time_series→line、composition→pie、comparison→bar 等），新图表类型声明 hints 即被识别，不必改 planner 选型分支。
- `--requirement` 关键词扩展：仪表盘/雷达/南丁格尔/树图/漏斗/面积/热力 等显式指定。

### 已知限制

- **glass / glow 装饰不渲染特效**：lean 编译器只把 token 灌进 CSS 变量，不按 `--decoration` 生成 backdrop-blur / 辉光。`obsidian-glass` / `amethyst-glass` / `nebula-glow` 等主题在 skill 里按 token 颜色平铺渲染。`--decoration` frontmatter 为元数据。
- 20 个去品牌主题保留原样品牌签名 hex（色值本身不可版权，配中性名+中性 prose 后可辩护）。`python tools/import_saas_themes.py` 可复现验证 20/20 token 保真 + 零品牌残留。

## 30 秒上手

```bash
# 默认主题（midnight-ops），编译完自动打开
vizagent build --data sales.xlsx --open

# 换主题（25 个任选）
vizagent build --data sales.xlsx --theme grove-dark --open

# 自定义主题目录
vizagent build --data sales.xlsx --theme-dir ./my-themes --open
```

## 25 个主题

- **原创 5**：`midnight-ops`（默认）/ `paper-light` / `warm-editorial` / `clinical-light` / `signal-dark`
- **去品牌 20**：`coral-warm` / `obsidian-glass` / `parchment-serif` / `trust-blue` / `canvas-dot` / `ops-slate` / `ring-pastel` / `nebula-glow` / `graphite-iris` / `broadsheet` / `fiber-paper` / `grid-azure` / `gilt-navy` / `ember-paper` / `amethyst-glass` / `grove-dark` / `haze-lilac` / `phosphor-green` / `amber-scan` / `mono-noir`

## 测试

127 passed（含 P1 去品牌主题校验 5 项 + P3/P4 图表类型回归）；ruff src/ tests/ 全清。
