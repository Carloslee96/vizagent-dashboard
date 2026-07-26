# Minimal Doc — 温暖纸感文档风

## Visual Theme
浅色、纸感、反科技感。暖灰画布上铺开白色面板，像一页排版考究的文档：大量留白、纤细边框、克制的蓝色强调。页面背景铺一层极轻噪点纹理（noise），像纸面纤维——**纸纤维噪点是 notion 签名，noise 纹理由本主题独占**（三胞胎解撞：claude 用 dots 点阵、newsroom 用 hatch 网点，互不使用 noise）。正文全面无衬线，衬线只留页头标题。层次靠底色差而非阴影。

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-primary` | `#f7f6f3` | 页面背景（Notion 暖灰） |
| `--bg-card` | `#ffffff` | 卡片/面板（纸面白） |
| `--bg-elevated` | `#ffffff` | 悬浮面板（靠阴影浮起） |
| `--bg-hover` | `#efedea` | 悬停表面 |
| `--border-subtle` | `#e9e8e6` | 边框/分隔线（仅 1px） |
| `--accent-primary` | `#2383e2` | Notion Blue |
| `--accent-success` | `#448361` | 上涨/完成（Notion 绿） |
| `--accent-warning` | `#cb912f` | 警告（Notion 黄） |
| `--accent-danger` | `#d44c47` | 下跌/异常（Notion 红） |
| `--text-primary` | `#37352f` | 主文字（暖黑，禁用纯黑） |
| `--text-secondary` | `#787774` | 次要文字 |
| `--map-area` | `#ffffff` | 地图无数据区域底色 |
| `--map-boundary` | `#787774` | 地图国家/省级边界 |
| `--text-muted` | `#b4b3af` | 弱化文字/占位 |

## Typography
- 页头标题: **Source Serif 4 衬线**, 28px 700 — 对应 Notion 文档的 Serif 模式（系统回退 Georgia）
- 面板标题: Inter 15px 600, 左对齐
- KPI 数字: Inter 34px 600, tabular-nums — **浅色组最小 KPI 字号：克制的小 KPI，文档不是海报**
- 正文/表格: Inter 14px 400, 行高 1.6
- 数字/代码: IBM Plex Mono 13px

## Border Radius
- 卡片/面板: **6px** | 按钮: **4px** | 进度条: **3px** — 全部小圆角，接近直角

## Shadows
- 卡片: `0 1px 2px rgba(15,15,15,0.05)`（几乎不可见，层次靠白/暖灰底色差）
- 悬浮层/Tooltip: `0 4px 12px rgba(15,15,15,0.08)`

## Motion
- 悬停: **120ms ease-out**（只换背景色的即时反馈，无位移无阴影变化）
- **签名动效**: KPI 数字 **700ms ease-out 慢滚动**——文档气质的从容更新节奏，禁止弹跳/弹性曲线
- **入场编排**: **无 stagger，整屏同现 200ms 淡入**——文档是整页渲染的，不做逐卡片入场

## Layout & Grid

| 属性 | 值 |
|------|-----|
| 页面最大宽度 | 1920px |
| 网格系统 | CSS Grid 12 列，内容驱动 |
| 卡片间距 | 20px |
| 页面内边距 | 28px |
| 图表容器最小高度 | 280px |
| 对齐方式 | 全左对齐（文档式，禁止居中排版） |
| 信息密度 | 标准——文档工作台不追求海报式留白，也不过载 |

## Component Specifications

### KPI 卡片
- 白底 `--bg-card` + 1px `--border-subtle`，圆角 6px，内边距 18px 20px
- **形态**: plain — 纯大数字+单位，不用迷你图/进度环/涨跌胶囊（趋势仅小箭头+百分比文字）
- **结构即签名**: "标签在上 + 数字 34px + 趋势与标签同行右侧"的紧凑三段式是 notion 专属 KPI 版式
- **标签在上**（Notion 属性式）: 13px `--text-secondary`，数字下方留 6px 到数字；标签前可加 8px 系列色圆点（tag 风，与表格分类圆点同源）
- **数字**: 34px 600 Inter, `--text-primary`，左对齐，tabular-nums
- **趋势**: 小箭头 + 百分比，success/danger 色，与标签同行右侧
- **悬停**: 整卡背景变 `--bg-hover`，无阴影变化

### 图表容器
- 白底 + 1px 细边框，圆角 6px，内边距 20px
- 标题: 15px 600 Inter 左对齐，图例 12px 放标题行右侧
- 图表区: ECharts 浅色主题（容器背景透明），四周留白 ≥16px
- 无任何装饰条、角标、光效

### 按钮
- 主按钮: `--accent-primary` 纯色，白字，圆角 4px，内边距 8px 16px，14px 500
- 次按钮: 白底 + `--border-subtle` 边框，`--text-primary` 文字
- 悬停: 主按钮明度降 10%；次按钮背景变 `--bg-hover`
- 禁用: 40% 透明度

### 数据表格
- Notion Database 风: 无纵向边框，仅 1px `--border-subtle` 行分隔线
- 表头: 12px 500 `--text-muted`，背景透明，行高 32px
- 数据行: 行高 36px 白底，悬停整行 `--bg-hover`
- 数字列右对齐用 mono；首列可用 10px 系列色圆点作分类标签——**Notion tag 圆点是本主题装饰符号签名**，贯穿表格首列与 KPI 标签前缀

### 页头
- 透明背景融入页面，底部至多 1px `--border-subtle` 分隔线
- 标题: 28px 700 Source Serif 4 衬线, `--text-primary`，左对齐
- 时间/副标题: 13px `--text-muted`，标题下方

### 进度条
- 高度 6px，圆角 3px，轨道 `--border-subtle`
- 填充 `--accent-primary` 纯色，无渐变
- 百分比标注 12px `--text-muted`，置于右侧

## Chart Fingerprint
- **折线**: 线宽 2px 纯色；symbol: none 不显示数据点，hover 时才出现 6px 圆点+白描边；**禁止面积填充与渐变**
- **柱形**: 仅上圆角 [3,3,0,0]；纯色无渐变；hover 柱体明度降 15%，不加阴影
- **饼/环**: 只做环形 radius ['52%','72%']；扇区间 2px 白色分隔；标签默认隐藏，中心显示衬体总数；**禁止发光**
- **网格线**: 仅横向 1px 实线 `--border-subtle`；纵向网格线和坐标轴线一律删除
- **Tooltip**: 白底 + 1px `--border-subtle` + `0 4px 12px rgba(15,15,15,0.08)`，文字 `--text-primary`，无品牌色边框
- **排他签名**: notion 是**浅色组唯一全面禁用面积填充的主题**——折线一律无 `areaStyle`、柱/环纯色零渐变（pitchbook/vercel 的禁面积条款仅限深色组，不构成并列）；文档图表只画线与块，绝不铺色
- **签名句式**: 多系列折线/柱形用 `endLabel` 线端直接标注系列名替代图例（文档式直标，分类维度图仍保留图例）；`markLine` 均值虚线（`--text-muted`）/目标实线（`--accent-primary`）；超阈值数据点/柱体用 success/danger 阈值染色；**不启用 markArea，面积渐变一律禁用**（与本主题禁面积填充一致）
- **图例/标签**: 图例 12px `--text-secondary` 圆点标记右对齐；数据标签默认关闭
- **允许**: 单蓝色主导 + 暖色点缀；hover 换色；图表内大留白
- **禁止**: 一切渐变、发光、面积图、纵向网格线、深色 Tooltip

## Chart Color Palette
系列色: #2383e2, #d9730d, #448361, #9065b0, #d44c47

## Anti-Patterns
- 禁止深色卡片/深色模式——本主题是浅色大屏
- 禁止纯黑 `#000000` 文字或背景，用暖黑 `--text-primary`
- 禁止渐变、发光、玻璃拟态、粗于 1px 的边框
- 禁止冷灰背景（如 `#f4f4f5`），保持暖灰 `--bg-primary`
- 禁止 KPI 数字居中放大阵仗——克制、左对齐
- 禁止"结论句标题"（如"营收再创新高"）——该句式让给 newsroom，notion 标题只写中性的文档式命名
- 禁止衬线 KPI 数字/衬线正文——衬线只留页头标题，衬线数字让给 claude

## Do's and Don'ts
✅ 页头标题用衬线体，营造文档感
✅ 面板层次靠白卡片落在暖灰底上，不靠阴影
✅ 悬停只换背景色，120ms 即时反馈
✅ 表格用系列色小圆点做分类标签（Notion tag 风）
❌ 不要加顶部装饰条/渐变分割线
❌ 不要让图表撑满面板——四周留白 ≥16px

## Token Schema

| Token | 值 | 说明 |
|--------|----|------|
| `--radius-card` | `6px` | 卡片圆角（浅色组最小，与 posthog 并列——近直角=工具感） |
| `--radius-button` | `4px` | 按钮圆角 |
| `--radius-panel` | `6px` | 面板圆角 |
| `--font-family-base` | `"Inter", -apple-system, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif` | 正文（CDN 环境带系统 fallback） |
| `--font-family-display` | `"Source Serif 4", Georgia, serif` | 页头标题（衬线，Google Fonts 加载 Source Serif 4） |
| `--font-family-mono` | `"IBM Plex Mono", ui-monospace, Consolas, monospace` | 数字/代码 |
| `--font-size-display` | `28px` | 页头标题 |
| `--font-size-title` | `15px` | 面板标题 |
| `--font-size-kpi` | `34px` | KPI 大数字 |
| `--shadow-card` | `0 1px 2px rgba(15,15,15,0.05)` | 卡片阴影 |
| `--glow-accent` | `none` | 本主题无发光 |
| `--bg-pattern` | `noise` | 页面层噪点纸纹——纸纤维噪点是 notion 签名，noise 全库独占（claude=dots、newsroom=hatch） |
| `--pattern-color` | `rgba(0,0,0,0.04)` | 纹理色（浅色主题 0.04~0.06，取最轻档） |
| `--kpi-variant` | `plain` | KPI 纯大数字+单位，克制左对齐 |
| `--decoration` | `flat` | 纯平：无渐变、无发光 |
