# Deal Room — 金融暗色交易风

## Visual Theme
克制、厚重、有纸感。像顶级投行打印研报的屏幕版——深蓝黑纸面、细金线分隔、衬线大数字、密集表格。
低饱和、零霓虹：**金铜色是标点，不是颜料**——只做 1px 分隔线、内描边与关键数字，绝不铺底、绝不发光。

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-primary` | `#0B1220` | 主背景（深蓝黑，禁止纯黑 #000） |
| `--bg-card` | `#131C2E` | 卡片/面板（钢青灰） |
| `--bg-elevated` | `#1A2438` | 悬浮/表头/tooltip |
| `--bg-hover` | `#1E2A42` | 行/卡片悬停 |
| `--border-subtle` | `#26324A` | 边框/分隔线（1px 低对比） |
| `--accent-primary` | `#C9A96A` | 金铜强调（仅细线/内描边/主系列/关键数字） |
| `--accent-secondary` | `#5B8DB8` | 雾蓝（次系列/链接/坐标高光） |
| `--accent-success` | `#4E9E78` | 上涨/正向（低饱和） |
| `--accent-warning` | `#C08A45` | 警示（仅异常态） |
| `--accent-danger` | `#B26060` | 下跌/负向（低饱和赭红） |
| `--text-primary` | `#EDEAE2` | 主文字（暖纸白，禁止纯白） |
| `--text-secondary` | `#93A1B5` | 次要文字/坐标轴 |
| `--map-area` | `#1A2438` | 地图无数据区域底色 |
| `--map-boundary` | `#93A1B5` | 地图国家/省级边界 |
| `--text-muted` | `#5E6B80` | 辅助/脚注/时间戳 |

## Typography
- 正文 13-14px Inter，行高 1.5，左对齐
- 标题与 KPI 大数字：**Cormorant Garamond 衬线**，600，字距正常不压缩
- 表格数字/代码：`--font-family-mono` + `font-variant-numeric: tabular-nums`
- KPI 标签：11px 全大写 + `letter-spacing: 0.12em` `--text-muted`（研报眉标风格）
- 单位降级：KPI 大数字后的单位用 14px `--text-secondary`，基线对齐

## Border Radius
克制微圆角：卡片 4px、按钮 4px、面板 3px。**禁止超过 6px**，禁止药丸形。

## Shadows
不用投影。层次靠 `#0B1220 → #131C2E → #1A2438` 色阶 + 双边框（见组件规格）。禁止任何 text-shadow / 发光 / 毛玻璃。

## Component Patterns
- **细金线分隔**：页头底部、卡片标题下方、表格小节之间用 `1px solid rgba(201,169,106,0.35)` 细金线，不使用粗色块标题栏
- **双边框卡**：外 `1px solid var(--border-subtle)` + 内 `1px rgba(201,169,106,0.2)`（inset 实现），全站卡片统一
- **密集表格**：36px 行高、12-13px 字号、行间 1px 细线，信息密度向打印研报看齐
- **衬线大数字**：KPI 一律 Cormorant Garamond，不用等宽体充大数字

## Anti-Patterns（🔴 违反即不合格）
- ❌ 任何霓虹色（青 `#00E5FF`、品红、电紫）、任何发光/渐变面板
- ❌ 金铜色大面积铺底或作按钮底色——金色只做线与点
- ❌ 圆角 > 6px、药丸控件
- ❌ KPI 大数字用等宽/无衬线字体（本主题 KPI 必须衬线）
- ❌ 面积渐变、3D 图表、饼图实心发光
- ❌ 纯黑 `#000` / 纯白 `#FFF`

## Motion
- 签名动效：KPI 刷新时衬线大数字逐位滚动 600ms ease-out 落位——数字沉稳归位，不跳变、不闪烁
- 入场编排：自上而下 60ms stagger（页头 → KPI 行 → 图表区），像研报逐版落版
- 图表重绘用 ECharts 默认过渡；禁止弹跳/弹性缓动、流光边框、扫描线
- 无任何循环动画（状态点脉冲也不允许）——全库最严动效纪律，与 newsroom 并列静态权威派；hover 唯一反馈是内金线 alpha 变化，禁止位移/浮起

## Layout & Grid

| 属性 | 值 |
|------|-----|
| 页面尺寸 | 1920×1080（按需自适应） |
| 网格系统 | CSS Grid 3-4 列，强对齐 |
| 卡片间距 | 16px |
| 页面内边距 | 24px |
| 图表容器最小高度 | 300px |
| 对齐方式 | 文字左对齐、表格数字右对齐，标题禁止居中 |

## Component Specifications

### KPI 卡片（kpi-variant=plain）
- `--bg-card` + 双边框（外 1px `--border-subtle` + 内 `box-shadow: inset 0 0 0 1px rgba(201,169,106,0.2)`），4px 圆角，内边距 18px 20px，无投影
- 标签在上：11px 全大写宽字距 `--text-muted`；大数字在下：**44px Cormorant Garamond 600 衬线** `--text-primary`，左对齐
- 单位降级：大数字后单位 14px `--text-secondary` 基线对齐
- 趋势：12px + ↑↓ 符号，涨 `--accent-success` / 跌 `--accent-danger`，数字下方一行，不做胶囊不做色底
- 悬停：仅内金线 alpha 升至 0.4，背景不变

### 图表容器
- `--bg-card` + 同款双边框 + 4px 圆角，内边距 16px
- 标题 15px 600 左对齐（Inter），标题下方 **1px 细金线** `rgba(201,169,106,0.35)` 通栏分隔
- 右上角可放 11px `--text-muted` 单位/周期说明（等宽）
- 坐标轴 11px `--text-secondary`，轴线 `--border-subtle`

### 按钮
- 主按钮：透明底 + `1px solid var(--accent-primary)` 金色描边 + `--accent-primary` 文字，4px 圆角（金线按钮，不填金底）
- 次按钮：透明 + 1px `--border-subtle`，文字 `--text-secondary`
- 悬停：主按钮金底 8% alpha 淡入；禁用态降透明度不改成色

### 数据表格
- 表头 `--bg-elevated`，11px 600 全大写 `--text-secondary`，下边框 **1px 细金线**
- 行高 36px 密集排列，行间 1px `--border-subtle` 细分隔线，无斑马纹
- 数字列等宽 tabular 右对齐，文字列左对齐；涨跌幅列 ↑↓ + 语义色
- 悬停行 `--bg-hover`；状态用 6px 色点不用色块徽章

### 页头
- 56px 高，底部 **1px 细金线** `rgba(201,169,106,0.35)` 分隔
- 标题 26px Cormorant Garamond 600 衬线左对齐，可前置 3px 宽金色竖条
- 右侧：12px 等宽日期/更新时间 `--text-muted`，无脉冲状态点

### 进度条
- 高度 3px，直角无圆角；轨道 `--border-subtle`，填充 `--accent-primary` 纯色
- 禁止渐变/流光/光晕；百分比 12px 等宽右对齐跟在条后

## Chart Color Palette
- 系列色: `#C9A96A`, `#5B8DB8`, `#7FA3C0`, `#4E9E78`, `#B26060`（金铜领衔，雾蓝阶为辅，绿红仅语义对照）
- 警示/异常: `#C08A45`（不进系列色，仅状态标记）

## Chart Fingerprint
- **折线**：线宽 2px，不显示数据点（symbol: none），hover 十字准线；**endLabel 替代图例**（线尾直接标系列名，11px 系列色，关闭 legend）；**禁止面积渐变——任何系列都不铺面积**（全库仅本主题与 vercel 两家全面禁面积，vercel 为黑白语境、本主题为研报语境，共存不冲突）
- **柱形**：直角（圆角 0），纯色填充禁止渐变；hover 整列提亮 10% 并描边 `--accent-primary` 1px
- **饼/环图**：细环 `radius: ['55%', '75%']`，外侧引导线 + 百分比标签；禁止发光与中心装饰
- **网格线**：**仅水平细实线**（1px，`--border-subtle`，type: 'solid'），垂直网格一律关闭
- **标注**：**markLine 均值虚线/目标实线**（均值用 `--text-muted` 虚线，目标用 `--accent-primary` 实线）；**markArea 区间标注**：财季/政策窗口用 `rgba(201,169,106,0.06)` 金底区间——**全库唯一的金色区间标注，本主题排他签名**
- **Tooltip**：`--bg-elevated` + 双边框（外 1px `--border-subtle` + 内 1px 金线 inset，与卡片同构造），直角无阴影，内部数字等宽右对齐
- **允许**：endLabel、markLine 均值/目标、markArea 区间、水平细网格、阈值染色（仅状态色 1px 线段）
- **禁止**：任何发光/渐变、面积填充、垂直网格、柱子圆角、图例色块横排（已被 endLabel 替代）

## Do's and Don'ts
- ✅ 细金线分隔一切区块：页头、卡片标题、表头下方
- ✅ 双边框卡统一全站；金色 alpha 永远 ≤ 0.4
- ✅ KPI 衬线大数字 + 单位降级小字；表格数字等宽右对齐
- ✅ endLabel 线尾标注、markLine 均值/目标线，研报式图表注释
- ❌ 不要把金铜色铺底、填按钮、做大色块
- ❌ 不要发光、渐变、霓虹、毛玻璃
- ❌ 不要低密度的稀疏表格——本主题以密集为荣
- ❌ 不要给图表加图例栏，用 endLabel

## Token Schema

| Token | 值 | 说明 |
|-------|-----|------|
| `--radius-card` | `4px` | 卡片圆角 |
| `--radius-button` | `4px` | 按钮圆角 |
| `--radius-panel` | `3px` | 内嵌面板/tooltip 圆角 |
| `--font-family-base` | `"Inter", "PingFang SC", "Microsoft YaHei", sans-serif` | 正文/标签 |
| `--font-family-display` | `"Cormorant Garamond", "Playfair Display", Georgia, serif` | 标题/KPI 大数字（衬线） |
| `--font-family-mono` | `"IBM Plex Mono", Consolas, monospace` | 表格数字/时间戳 |
| `--font-size-display` | `26px` | 页头标题（衬线） |
| `--font-size-title` | `15px` | 卡片标题 |
| `--font-size-kpi` | `44px` | KPI 衬线大数字 |
| `--shadow-card` | `none` | 无投影，靠色阶+双边框分层 |
| `--glow-accent` | `none` | 无发光 |
| `--decoration` | `flat` | 纯平：无渐变面板、无发光、无高光线 |
| `--bg-pattern` | `none` | 页面背景无纹理（研报纸面感靠纯色） |
| `--pattern-color` | `rgba(255,255,255,0.04)` | 纹理备用色（bg-pattern=none 时不生效） |
| `--kpi-variant` | `plain` | 纯大数字+单位降级（衬线 KPI 招牌形态） |
