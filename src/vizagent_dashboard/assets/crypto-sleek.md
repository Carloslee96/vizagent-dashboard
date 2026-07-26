# Crypto Sleek — 深色金融科技风

## Visual Theme
单一 Coinbase Blue (#0052ff) 功能性强调色 + 近黑深底。机构级金融信任感：蓝色只用于交互与关键数据，不做装饰；深度靠色块对比而非阴影。冷静、精确、数据密集但绝不凌乱。无纹理是刻意的——色阶即纹理：本主题层次手段归属"色阶梯式"（`#0a0b0d → #16181d → #282b31`），不借用边框/缝隙/辉光/模糊等其他分层式。

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-primary` | `#0a0b0d` | 主背景（近黑，非纯黑） |
| `--bg-card` | `#16181d` | 卡片 |
| `--bg-elevated` | `#282b31` | 悬浮面板/Tooltip |
| `--bg-hover` | `#1f2228` | 行/卡片悬停 |
| `--border-subtle` | `#26292f` | 边框 |
| `--accent-primary` | `#0052ff` | Coinbase Blue，仅交互与主系列 |
| `--accent-secondary` | `#578bfa` | 悬停蓝/次系列 |
| `--accent-success` | `#098551` | 上涨/正向 |
| `--accent-warning` | `#f7931a` | 警示/中性波动（BTC 橙） |
| `--accent-danger` | `#cf202f` | 下跌/负向 |
| `--text-primary` | `#ffffff` | 主文字 |
| `--text-secondary` | `#8a919e` | 次要文字/坐标轴 |
| `--map-area` | `#282b31` | 地图无数据区域底色 |
| `--map-boundary` | `#8a919e` | 地图国家/省级边界 |
| `--text-muted` | `#5b616e` | 弱化文字/时间戳 |

## Typography
- 全局: **'Inter', -apple-system, 'Segoe UI', Roboto, sans-serif**（Coinbase Sans 无公开网络字体，Inter 为最接近替代）
- 展示标题: 同族 700，行高收紧至 1.1
- 价格/数字: **'Roboto Mono', 'JetBrains Mono', 'SF Mono', Consolas, monospace**，必须 `font-variant-numeric: tabular-nums`
- KPI 大数字: 40px, 600
- 标签: 12px, 600, sentence case（不大写）, 字间距 0.2px——uppercase 宽字距标签让给 palantir/terminal 组，本主题用机构金融的克制

## Border Radius: **12px 卡片 / 999px 胶囊按钮**（Coinbase 标志性 pill）

## Shadows
- 卡片: 无投影，靠 `#0a0b0d → #16181d → #282b31` 三级色阶分层
- Tooltip: `0 8px 24px rgba(0,0,0,0.4)`

## Chart Fingerprint
- 折线：线宽 2px；不显示数据点（symbol: none），hover 时才出现 6px 圆点 + 竖直标线；面积渐变允许，自 `--accent-primary` 20% 透明渐至 0%；hover 时其他系列降为 40% 透明度
- 柱形：全圆角 [6,6,6,6]——把胶囊语言推进图表区，与 palantir 直角柱形成对位；纯色填充，禁止渐变；hover 亮度提升 15%，不描边不位移
- 饼/环图：只用环形，radius ['55%','78%']；标签外部引导线 + 百分比，12px `--text-secondary`；禁止发光与斜切
- 网格线：仅横向虚线 1px，`--border-subtle`；纵向无网格
- Tooltip：背景 `--bg-elevated`，1px `--border-subtle` 边框，深色阴影，数字一律等宽右对齐
- 图例 12px `--text-secondary` 圆点标记；数据标签默认关闭，仅极值可标
- 涨跌语义：凡是"变化量"类系列，绿 `#098551` 涨 / 红 `#cf202f` 跌，不用蓝
- 末端标注：单系列折线/面积图用 endLabel 在折线末端直接标注最新值，替代图例；多系列仍用图例
- markLine：价格类图表叠加均值虚线（1px dashed `--text-muted`）；目标价用实线 `--accent-warning`，末端带值标签
- markArea：支撑/阻力区间用 `--accent-primary` 6% 透明度区间标注，不描边
- 阈值染色（全库唯一排他签名）：涨跌面积图以 0 轴为阈值整段分段染色，上方绿下方红——全库唯一"0 轴分段"染色范式，kraken/terminal-amber 的逐点着色不得混入本主题；面积渐变只给主系列（20% → 0%）
- 允许：折线面积渐变 20%、胶囊形交互控件、绿涨红跌语义色
- 禁止：任何发光/霓虹阴影、柱形渐变、蓝色装饰性大面积铺底、3D 图表

## Token Schema
| Token | 值 | 说明 |
|--------|----|------|
| `--radius-card` | `12px` | 卡片圆角 |
| `--radius-button` | `999px` | 胶囊按钮（品牌标志） |
| `--radius-panel` | `12px` | 面板圆角 |
| `--font-family-base` | `'Inter',-apple-system,'Segoe UI',Roboto,sans-serif` | 全局字体 |
| `--font-family-display` | `'Inter',-apple-system,'Segoe UI',Roboto,sans-serif` | 标题字体(700) |
| `--font-family-mono` | `'Roboto Mono','JetBrains Mono','SF Mono',Consolas,monospace` | 数字字体 |
| `--font-size-display` | `28px` | 页面大标题 |
| `--font-size-title` | `16px` | 卡片标题 |
| `--font-size-kpi` | `40px` | KPI 大数字 |
| `--shadow-card` | `none` | 卡片无投影，色阶分层 |
| `--glow-accent` | `none` | 本主题无发光 |
| `--bg-pattern` | `none` | 无背景纹理，纯色阶分层 |
| `--pattern-color` | `rgba(255,255,255,0.03)` | 纹理色（none 时备用） |
| `--kpi-variant` | `delta-pill` | KPI 卡涨跌胶囊形态 |
| `--decoration` | `flat` | 纯平无渐变无发光 |

## Component Specifications

### KPI 卡片
- 背景 `--bg-card`，圆角 12px，无边框无阴影，内边距 20px 24px
- 顶部 12px sentence case 标签（`--text-muted`）左对齐
- 大数字 40px 等宽字体左对齐，tabular-nums
- 数字下方为涨跌胶囊（delta-pill）：圆角 999px 全圆角 pill——本主题 pill 必须全圆角，与 palantir 的 12px 微圆角 pill 互斥，禁止折中圆角；涨 `rgba(9,133,81,0.15)` 底绿字 / 跌 `rgba(207,32,47,0.15)` 底红字，内嵌 ▲/▼ + 百分比，14px 600
- 悬停：背景变为 `--bg-hover`，无边框变化

### 图表容器
- 背景 `--bg-card`，圆角 12px，无边框，内边距 20px
- 标题 16px 600 左对齐 + 右侧 12px `--text-muted` 周期切换（1H/1D/1W，胶囊分段控件）——签名细节：全库独有的胶囊形周期切换分段控件，其他主题不得复用该形态
- 涨跌类图表用绿/红单色面积图，不用多系列彩虹色

### 按钮
- 主按钮：`--accent-primary` 底白字，圆角 999px 胶囊，内边距 10px 24px，14px 600
- 悬停：底色变 `--accent-secondary`（#578bfa），无位移无阴影
- 次按钮：`--bg-elevated` 底，`--text-primary` 字，同为胶囊
- 禁用：40% 透明度

### 数据表格
- 表头 12px sentence case `--text-muted`，无背景色，底部 1px `--border-subtle` 分隔
- 行高 52px，行间无斑马纹，仅 1px `--border-subtle` 细分隔线
- 悬停行：整行背景 `--bg-hover`
- 价格/数量列：等宽字体右对齐；涨跌幅列：绿/红带 ▲▼
- 首列：币种图标圆点 + 名称（600）+ 缩写（`--text-muted`）

### 页头
- 背景 `--bg-primary`，高度 64px，底部 1px `--border-subtle`
- 左侧标题 28px 700 + 右侧行情摘要条（BTC/ETH 价格 + 24h 涨跌，等宽数字，绿涨红跌）
- 右侧可放 12px `--text-muted` 更新时间

### 进度条
- 高度 4px，全圆角 999px
- 背景 `--bg-elevated`，填充 `--accent-primary` 纯色
- 标注：右端百分比，12px 等宽 `--text-secondary`

## Chart Color Palette
- 系列色: #0052ff, #098551, #cf202f, #f7931a, #578bfa

## Anti-Patterns
- 禁止把 Coinbase Blue 当装饰色大面积铺底或做渐变背景——蓝色只标识可交互与主数据
- 禁止给卡片加投影/发光来制造层次，层次只能来自 `#0a0b0d → #16181d → #282b31` 色阶
- 禁止方形直角按钮——所有可点控件必须胶囊形
- 禁止用蓝/紫等非语义色表达涨跌——涨 `#098551`、跌 `#cf202f` 不可互换
- 禁止非等宽字体显示价格与数量，禁止居中对齐数字列
- 禁止饼图实心饼与中心发光，只用环形
- 禁止顶部高光线/装饰色条——本主题靠色阶分层，不靠装饰条，与 terminal-amber/supabase 顶条派互斥

## Do's and Don'ts
✅ 变化量数据一律绿涨红跌 + ▲▼ 符号
✅ 数字用等宽字体 + tabular-nums，右对齐
✅ 胶囊按钮、胶囊分段控件、全圆角进度条，圆角语言统一
✅ KPI 与表格全部左对齐（数字列右对齐）
✅ 悬停反馈只换背景色/底色，不做位移与阴影
❌ 不要用纯黑 `#000000` 背景（用 `#0a0b0d`）
❌ 不要蓝色装饰、蓝色发光、蓝色大面积渐变
❌ 不要直角按钮或混用圆角规格
❌ 不要给每个面板都加边框——默认无边框靠色阶分隔，仅页头/表格用细分隔线
❌ 不要把涨跌系列画成蓝色或彩虹多色

## Motion
- 签名动效: **数字逐位滚动 800ms ease-out**——等宽字体 + tabular-nums 下每一位数字独立滚动到位，像行情终端翻牌；全库唯一的逐位滚动范式，与 kraken/terminal-amber 的闪烁范式互斥
- 入场编排: **无 stagger，整屏同现**——所有卡片 200ms fade-in 一次性出现，机构终端开机即全景，不逐项加载
- 实时价格刷新: 数值闪白 200ms 提示变动（不用闪绿/红——该刷新范式归属 kraken/terminal-amber）
- 禁止弹跳（bounce/elastic）缓动，金融界面只用线性减速曲线

## Layout & Grid

| 属性 | 值 |
|------|-----|
| 页面最大宽度 | 1920px |
| 网格系统 | CSS Grid, 4 列 |
| 卡片间距 | 16px |
| 页面内边距 | 24px |
| 图表容器最小高度 | 280px |
| 对齐方式 | 文本左对齐, 数字右对齐, tabular-nums |
| 密度基调 | 标准偏密——数据密集的机构终端，但绝不凌乱 |
