# Ocean Night — 深海暗色风

## Visual Theme
机构级加密交易所的行情终端气质：深紫近黑画布、紫色辉光强调、红绿严格保留给涨跌语义、等宽数字右对齐。信息密度极高，每个面板都像行情终端的一块屏幕。

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-primary` | `#0a0814` | 主背景（近黑紫） |
| `--bg-card` | `#12102a` | 卡片/面板 |
| `--bg-elevated` | `#1a1733` | 悬浮面板/表头 |
| `--bg-hover` | `#211d40` | 行/卡片悬停 |
| `--border-subtle` | `#2a2547` | 边框/分割线 |
| `--accent-primary` | `#5741d9` | Kraken 品牌紫 |
| `--accent-secondary` | `#8b5cf6` | 辅助紫（渐变末端） |
| `--accent-success` | `#16c784` | 上涨绿（仅涨跌语义） |
| `--accent-danger` | `#ea3943` | 下跌红（仅涨跌语义） |
| `--accent-warning` | `#f59e0b` | 警告橙 |
| `--text-primary` | `#f2f0fa` | 主文字/数字 |
| `--text-secondary` | `#a29cc0` | 次要文字 |
| `--map-area` | `#1a1733` | 地图无数据区域底色 |
| `--map-boundary` | `#a29cc0` | 地图国家/省级边界 |
| `--text-muted` | `#5d5880` | 弱化/单位 |

## Chart Color Palette
- 系列色: #5741d9, #16c784, #3b82f6, #f59e0b, #8b5cf6
- 注意：`#16c784` 绿与 `#ea3943` 红在含涨跌语义的图表（K线、涨跌柱）中必须按涨跌逐点着色，此时不占用系列色。

## Chart Fingerprint
- 折线：线宽 2px，默认不显示数据点（仅 hover 高亮当前点）；面积渐变允许，accent 紫自顶部 0.25 透明度渐隐到 0；hover 触发十字准线（crosshair），准线用 `--text-muted` 虚线。
- 柱形：仅上圆角 `[3,3,0,0]`，纯色填充禁止柱体渐变；含涨跌语义时逐柱绿/红着色；hover 柱体亮度 +15%，不出现外发光。
- 饼/环图：环形 `radius: ['55%','78%']`，扇区间用 2px `--bg-card` 描边分隔；标签放外部引导线，11px 等宽字体显示数值；禁止扇区发光与 3D 效果。
- 网格线：仅水平虚线 `dashed 1px`，颜色用 `--border-subtle`；垂直网格线一律关闭。
- Tooltip：背景 `--bg-elevated`，1px `--accent-primary` 边框，阴影 `0 0 12px rgba(87,65,217,0.35)`（紫色辉光），数字用 12px 等宽字体。
- 图例：11px、`--text-secondary`、8px 方形色块；数据标签默认关闭，仅柱图顶部允许开启（11px mono）。
- 坐标轴：11px JetBrains Mono、`--text-muted`，数字千分位分隔。
- 末端标注：多系列折线用 `endLabel` 在线末端直接标系列名+最新值（11px mono），替代图例；柱图、饼图等类目型图表仍保留图例。
- 参考线：均值用 `markLine` 虚线（`--text-muted`），目标/阈值用实线（`--accent-warning`）；标注文字 11px mono 右对齐。
- 阈值染色：折线/柱形按阈值分段着色——突破目标区段染 `--accent-success`，跌破警戒区段染 `--accent-danger`，其余保持系列色。
- 面积渐变只给主系列（第一系列），其余系列纯线不加面积。
- 排他签名：面积渐变起始透明度 0.25 为全库第二高（仅 spotify 30% 更高，其余主题 ≤20%），数值本身即签名；紫色辉光 tooltip（`0 0 12px rgba(87,65,217,0.35)`）为全库唯一——terminal-amber 用 1px 琥珀实线边框 tooltip，两家禁止互换。
- 允许：面积渐变（仅主系列）、十字准线、紫色辉光 tooltip、涨跌红绿逐点着色、endLabel 末端标注、markLine 均值/阈值参考线、阈值分段染色。
- 禁止：柱体渐变、饼图发光、3D 图表、垂直网格线、把红绿用作普通系列色。

## Token Schema
| Token | 值 | 说明 |
|--------|----|------|
| `--radius-card` | `4px` | 卡片圆角（锐利终端感） |
| `--radius-button` | `4px` | 按钮圆角 |
| `--radius-panel` | `4px` | 面板圆角 |
| `--font-family-base` | `'Inter', -apple-system, 'Segoe UI', sans-serif` | 正文/标签 |
| `--font-family-display` | `'Space Grotesk', 'Inter', sans-serif` | 页头标题 |
| `--font-family-mono` | `'JetBrains Mono', 'SF Mono', Consolas, monospace` | 一切数字/代码 |
| `--font-size-display` | `28px` | 页头大标题 |
| `--font-size-title` | `15px` | 面板标题 |
| `--font-size-kpi` | `34px` | KPI 大数字 |
| `--shadow-card` | `0 2px 8px rgba(0,0,0,0.4)` | 卡片投影 |
| `--glow-accent` | `rgba(87,65,217,0.35)` | 紫色辉光 |
| `--decoration` | `glow` | 渐变+发光+高光线 |
| `--bg-pattern` | `scanlines` | 页面层扫描线纹理（CRT 终端质感） |
| `--pattern-color` | `rgba(255,255,255,0.03)` | 扫描线颜色（深色主题低透明白） |
| `--kpi-variant` | `delta-pill` | KPI 涨跌用胶囊呈现 |

## Typography
- 数字/价格：`--font-family-mono`，必须 `font-variant-numeric: tabular-nums`，千分位分隔
- 面板标签：Inter 11px 500，uppercase，letter-spacing 0.08em，`--text-secondary`
- 面板标题：Inter 15px 600，左对齐
- 页头标题：`--font-family-display` 28px 600，左对齐

## Border Radius
全局统一 `4px`，无例外（终端面板的锐利精确感，禁止圆角混用）。

## Shadows
- 卡片：`0 2px 8px rgba(0,0,0,0.4)`
- 悬停/激活面板：叠加 `0 0 12px rgba(87,65,217,0.35)` 紫色辉光

## Motion
- 签名动效：数值刷新用辉光脉冲——新值到达时数字背景按涨跌染绿/红闪烁 300ms，同时整卡叠加一层 `--glow-accent` 紫色辉光脉冲（0→35%→0，450ms 渐隐），不做位移动画；无辉光的纯闪烁范式归 terminal-amber 独占，本主题不写裸闪烁
- 入场编排：stagger 入场——面板自上而下次第淡入，间隔 60ms，总时长不超过 600ms
- 面板展开：200ms ease-in-out

## Layout & Grid
| 属性 | 值 |
|------|-----|
| 页面最大宽度 | 1920px |
| 网格系统 | CSS Grid 12 列，自由合并成 4-6 个密集面板 |
| 卡片间距 | 12px |
| 页面内边距 | 20px |
| 图表容器最小高度 | 280px |
| 对齐方式 | 数字一律右对齐，标签左对齐（同列数字小数点对齐） |

## Component Specifications

### KPI 卡片
- 背景 `--bg-card`，1px `--border-subtle` 边框，圆角 4px，内边距 14px 18px
- 顶部 2px `--accent-primary` 高光线（终端面板的标识）
- 标签：11px uppercase mono，`--text-muted`，左对齐置顶
- 大数字：34px 700 等宽字体，右对齐；带涨跌时数字直接染 `--accent-success`/`--accent-danger`
- 变化值：delta-pill 胶囊——12px mono 数值带符号（`+2.34%` / `-1.08%`），装在 4px 圆角胶囊内，涨=10% 透明度 `--accent-success` 底+绿字，跌=10% 透明度 `--accent-danger` 底+红字，右对齐紧跟大数字下方
- 悬停：边框转 `--accent-primary`，卡片浮起紫色辉光

### 图表容器
- 背景 `--bg-card`，1px 边框，圆角 4px，内边距 14px
- 标题 15px 600 左对齐，右上角放 11px mono 实时时间戳或周期切换（1H/1D/1W）
- 图表区暗色 ECharts，严格按 Chart Fingerprint 执行
- 容器悬停不位移，仅边框微亮

### 按钮
- 主按钮：`--accent-primary` 底、白字、4px 圆角、13px 600，hover 叠加紫色辉光
- 次按钮：透明底、1px `--border-subtle` 边框、hover 边框转紫
- 危险操作按钮用 `--accent-danger` 边框+文字，不用实心红底
- 禁用：40% 透明度，无辉光

### 数据表格
- 表头：`--bg-elevated`，11px uppercase mono，`--text-muted`，行高 36px
- 数据行：行高 40px，斑马纹 `--bg-card`/`--bg-primary` 交替——斑马纹表格为本主题独占签名（terminal-amber 已让位为行间 1px 分隔线，全库其他主题一律用行线/缝隙，不得回用斑马纹）
- 悬停行：背景 `--bg-hover`，左侧 2px `--accent-primary` 竖线
- 数字列：等宽字体右对齐，涨跌值染绿/红；文字列左对齐
- 首列可放币种代码（mono uppercase，如 BTC/ETH）

### 页头
- 背景 `--bg-primary`，高度 52px；底部用 2px `--accent-primary` 紫色高光线作页头签名（复用 KPI 卡顶条语言，全库唯一的整宽高光页头）——6px 实心方块标识归 terminal-amber 独占，本主题禁用方块
- 标题：`--font-family-display` 28px 600 左对齐
- 右侧：14px mono 实时时钟 + 连接状态点（在线 `--accent-success` 呼吸闪）

### 进度条
- 高度 4px，圆角 2px，轨道 `--border-subtle`
- 填充：`--accent-primary` → `--accent-secondary` 水平渐变，末端带 4px 紫色辉光
- 标注：12px mono 百分比，右对齐

## Anti-Patterns
- 禁止把 `--accent-success`/`--accent-danger` 用作装饰色或普通系列色——红绿只属于涨跌
- 禁止任何大于 4px 的圆角（圆角混用或偏圆都破坏终端感）
- 禁止浅色/白色卡片，所有面板保持深紫系
- 禁止数字居左或居中，价格与统计数字必须右对齐等宽
- 禁止无面板感的裸图表——每块图表必须有边框容器包裹
- 禁止用阴影代替辉光：强调态只用紫色辉光，不用灰色大投影

## Do's and Don'ts
✅ 涨跌语义贯穿全屏：同一块屏幕内绿=涨、红=跌，绝不反用
✅ 所有数字用等宽字体 + tabular-nums，同列小数点对齐
✅ 面板顶部 2px 紫色高光线是 Kraken 的标识，保持统一
✅ 密度优先：宁可缩小留白也不放大字号充数
❌ 不要用纯黑 `#000000` 背景，主背景必须是带紫相的 `#0a0814`
❌ 不要给涨跌数字加图标前缀，符号 `+/-` 与颜色已足够
❌ 不要在非交互元素上加辉光，辉光只属于 hover/激活/进度条
