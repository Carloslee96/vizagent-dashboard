# Amber Console — 琥珀色复古终端风

## Visual Theme
老牌金融终端的 CRT 气质：深蓝黑画布、扫描线底纹、琥珀色作为唯一品牌强调、红绿严格保留给涨跌语义、一切数字用等宽字体右对齐。信息密度极高，每块面板都像终端屏幕上的一块行情窗口。本主题为平涂派（flat），层次感只靠底色阶梯与 1px 边框——辉光、脉冲光晕属于 kraken 的语言，本主题一概不用。

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-primary` | `#0A0E17` | 主背景（深蓝黑） |
| `--bg-card` | `#131722` | 卡片/面板 |
| `--bg-elevated` | `#191E2B` | 悬浮面板/tooltip/表头 |
| `--bg-hover` | `#212737` | 行/卡片悬停 |
| `--border-subtle` | `#1E2330` | 边框/分割线 |
| `--accent-primary` | `#F5A623` | 琥珀强调（品牌色） |
| `--accent-success` | `#00D4AA` | 上涨绿（仅涨跌语义） |
| `--accent-danger` | `#FF4757` | 下跌红（仅涨跌语义） |
| `--text-primary` | `#D1D4DC` | 主文字/数字 |
| `--text-secondary` | `#787B86` | 次要文字 |
| `--map-area` | `#191E2B` | 地图无数据区域底色 |
| `--map-boundary` | `#787B86` | 地图国家/省级边界 |
| `--text-muted` | `#4A4E5A` | 弱化/单位/网格标注 |

## Typography
- 一切数字（KPI/坐标轴/表格数字列/tooltip）：`--font-family-mono`，必须 `font-variant-numeric: tabular-nums`，千分位分隔
- 面板标签：Inter 11px 500，uppercase，letter-spacing 0.08em，`--text-secondary`
- 面板标题：Inter 13px 600，左对齐，可 uppercase
- 页头标题：Inter 26px 600，左对齐

## Border Radius
全局统一 `4px`，无例外（终端窗口的锐利精确感，禁止圆角混用）。

## Shadows
- 全主题无阴影：`--shadow-card` 为 `none`，面板层级只靠底色与 1px 边框区分
- 禁止发光/辉光：`--decoration` 为 `flat`，琥珀色只做平涂强调

## Component Patterns
- KPI 卡片走 `topbar` 变体：卡顶 3px 琥珀条是终端窗口的标识
- 页面底层铺 CRT 扫描线纹理（`--bg-pattern: scanlines`），纹理必须弱到不影响读数
- 涨跌语义贯穿全屏：同屏内绿 `#00D4AA`=涨、红 `#FF4757`=跌，绝不反用
- 琥珀色只给：KPI 顶条、主按钮、图表主系列、tooltip 边框、hover 边框

## Anti-Patterns
- 禁止把 `--accent-success`/`--accent-danger` 用作装饰色或普通系列色——红绿只属于涨跌
- 禁止任何阴影、发光、渐变装饰（flat 档，辉光为 `none`）
- 禁止大于 4px 的圆角
- 禁止浅色/白色卡片，所有面板保持深蓝黑系
- 禁止数字用非等宽字体或居左/居中，统计数字必须右对齐等宽
- 禁止琥珀色泛滥：它是稀缺强调色，不做大面积填充
- 禁止紫色系任何色相（含图表系列色）——紫色域归 kraken 专属，两主题互斥写死

## Motion
- 签名动效：数值刷新闪烁 300ms（涨绿闪 / 跌红闪）——**纯闪烁、无辉光无脉冲**，为本主题独占的刷新范式；kraken 用紫色辉光脉冲，两主题互不借用。辅以页头右上脉冲绿点 + 等宽 HH:MM:SS 跳动时钟的 Bloomberg 签名组合
- 入场编排：面板自上而下次第淡入，stagger 间隔 50ms，总时长不超过 500ms

## Layout & Grid
| 属性 | 值 |
|------|-----|
| 页面最大宽度 | 1920px |
| 网格系统 | CSS Grid 12 列，自由合并成 4-6 个密集面板 |
| 卡片间距 | 12px |
| 页面内边距 | 16px |
| 图表容器最小高度 | 280px |
| 对齐方式 | 数字一律右对齐，标签左对齐（同列数字小数点对齐） |

密度声明：12px 间距 + 16px 内边距为全库最密档（与 kraken 并列）——极致密集，终端密度即美学。

## Component Specifications

### KPI 卡片
- 背景 `--bg-card`，1px `--border-subtle` 边框，圆角 4px，无阴影，内边距 14px 16px
- 卡顶 3px `--accent-primary` 琥珀条（topbar 变体的标识）
- 标签：11px uppercase mono，`--text-muted`，左对齐置顶
- 大数字：32px 700 等宽字体，右对齐；带涨跌时数字直接染 `--accent-success`/`--accent-danger`（Bloomberg 正统如此；kraken 侧数字本体不染、仅 delta-pill 染，两主题处理方式互斥）
- 变化值：12px mono，紧跟大数字下方右对齐，格式 `+2.34%` / `-1.08%`（带符号）
- 悬停：边框转 `--accent-primary`，无浮起无阴影

### 图表容器
- 背景 `--bg-card`，1px 边框，圆角 4px，无阴影，内边距 14px
- 标题 13px 600 左对齐，右上角放 11px mono 实时时间戳或周期切换（1H/1D/1W）
- 图表区暗色 ECharts，严格按 Chart Fingerprint 执行
- 容器悬停不位移，仅边框微亮转琥珀

### 按钮
- 主按钮：`--accent-primary` 琥珀底、深底字 `#0A0E17`、4px 圆角、13px 600，hover 亮度 +10%
- 次按钮：透明底、1px `--border-subtle` 边框、`--text-secondary` 字，hover 边框转琥珀
- 危险操作按钮用 `--accent-danger` 边框+文字，不用实心红底
- 禁用：40% 透明度

### 数据表格
- 表头：`--bg-elevated`，11px uppercase mono，`--text-muted`，行高 34px
- 数据行：行高 38px，行间 1px `--border-subtle` 分隔线，**不做斑马纹**——斑马纹让位给 kraken 独占，本主题用行竖线体系
- 悬停行：背景 `--bg-hover`，左侧 3px `--accent-primary` 琥珀竖线（本主题独占的表格签名，kraken 不得使用）
- 数字列：等宽字体右对齐，涨跌值染绿/红；文字列左对齐
- 首列可放代码（mono uppercase，如 AAPL/BTC）

### 页头
- 背景 `--bg-primary`，底部分割线 1px `--border-subtle`，高度 52px
- 标题：26px 600 左对齐，前方放 6px 琥珀实心方块作标识——方块为本主题独占的页头符号（kraken 改用 2px 顶部高光线，两主题互斥）
- 右侧：13px mono 实时时钟 + 连接状态点（在线 `--accent-success` 呼吸闪）

### 进度条
- 高度 4px，圆角 2px，轨道 `--border-subtle`
- 填充：纯色 `--accent-primary`，禁止渐变与辉光
- 标注：12px mono 百分比，右对齐

## Chart Color Palette
- 系列色: #F5A623, #4D9FFF, #FFD166, #8D99AE
- 注意：`#00D4AA` 绿与 `#FF4757` 红在含涨跌语义的图表（K线、涨跌柱、涨跌折线）中必须按涨跌逐点着色，此时不占用系列色。

## Chart Fingerprint
- 折线：线宽 2px 纯色，默认不显示数据点（仅 hover 高亮当前点）；hover 触发十字准线（crosshair），准线用 `--text-muted` 虚线。
- 面积：渐变只给主系列——琥珀自顶部 0.2 透明度渐隐到 0，其余系列一律纯色描边不填面积。
- 涨跌：含涨跌语义的折线/柱形逐点红绿着色（涨 `#00D4AA`、跌 `#FF4757`），柱形仅上圆角 `[2,2,0,0]`，纯色填充禁止柱体渐变——`[2,2,0,0]` 为全库最小柱圆角（排他数值签名：接近直角但不是直角，与 vercel/palantir 的直角柱区分）。
- 标注：末端标注 `endLabel` 替代图例（11px mono 显示系列名+最新值）；`markLine` 均值虚线（`--text-muted` dashed），目标值用实线琥珀。
- 网格线：仅水平虚线 `dashed 1px`，颜色用 `--border-subtle`；垂直网格线一律关闭。
- Tooltip：背景 `--bg-elevated`，1px `--accent-primary` 琥珀边框，无阴影，数字用 12px 等宽字体——1px 琥珀边框 tooltip 为全库唯一（排他签名，kraken 的 tooltip 用紫辉光）。
- 图例：默认关闭（由 endLabel 承担）；必须开启时 11px、`--text-secondary`、8px 方形色块。
- 坐标轴：11px JetBrains Mono、`--text-muted`，数字千分位分隔。
- 允许：涨跌红绿逐点着色、主系列面积渐变、十字准线、endLabel、markLine。
- 禁止：柱体渐变、饼图发光、3D 图表、垂直网格线、把红绿用作普通系列色、多系列面积渐变。

## Do's and Don'ts
✅ 涨跌语义贯穿全屏：同一块屏幕内绿=涨、红=跌，绝不反用
✅ 所有数字用等宽字体 + tabular-nums，同列小数点对齐
✅ 卡顶 3px 琥珀条是 Terminal Amber 的标识，保持统一
✅ 密度优先：宁可缩小留白也不放大字号充数
❌ 不要用纯黑 `#000000` 背景，主背景必须是带蓝相的 `#0A0E17`
❌ 不要给涨跌数字加图标前缀，符号 `+/-` 与颜色已足够
❌ 不要加任何阴影或辉光，终端的层次感只靠底色与边框

## Token Schema
| Token | 值 | 说明 |
|--------|----|------|
| `--radius-card` | `4px` | 卡片圆角（锐利终端感） |
| `--radius-button` | `4px` | 按钮圆角 |
| `--radius-panel` | `4px` | 面板圆角 |
| `--font-family-base` | `'Inter', -apple-system, 'PingFang SC', sans-serif` | 正文/标签 |
| `--font-family-display` | `'Inter', -apple-system, sans-serif` | 页头标题 |
| `--font-family-mono` | `'JetBrains Mono', 'SF Mono', Consolas, monospace` | 一切数字/代码 |
| `--font-size-display` | `26px` | 页头大标题 |
| `--font-size-title` | `13px` | 面板标题 |
| `--font-size-kpi` | `32px` | KPI 大数字 |
| `--shadow-card` | `none` | 无阴影（flat 档） |
| `--glow-accent` | `none` | 无辉光（flat 档） |
| `--decoration` | `flat` | 纯色平涂，无渐变无发光 |
| `--bg-pattern` | `scanlines` | CRT 扫描线页面底纹（本主题独占，间距 3px；kraken 不得使用） |
| `--pattern-color` | `rgba(255,255,255,0.04)` | 扫描线纹理色（深色主题弱白） |
| `--kpi-variant` | `topbar` | KPI 卡顶 3px 琥珀条 |
