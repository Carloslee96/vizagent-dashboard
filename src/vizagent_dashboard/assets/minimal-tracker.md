# Minimal Tracker — 极简项目管理风

## Visual Theme
Linear 式工具美学：近黑深灰底、几乎不可见的边框、唯一的鸢尾紫强调色。去掉一切装饰——无阴影、无发光、无渐变面板，靠间距、对齐和 13px 级别的精密排版建立秩序。像命令面板一样克制，像 IDE 一样高效。

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-primary` | `#0d0e10` | 主背景（近黑深灰，非纯黑） |
| `--bg-card` | `#141518` | 卡片/面板 |
| `--bg-elevated` | `#1a1c20` | 浮层、Tooltip、表头 |
| `--bg-hover` | `#1f2125` | 悬停态（仅靠背景微亮表达） |
| `--border-subtle` | `#232529` | 边框（低存在感，1px） |
| `--accent-primary` | `#5e6ad2` | 鸢尾紫，唯一主强调色 |
| `--accent-secondary` | `#4ea7fc` | 冷蓝，链接/次强调 |
| `--success` | `#4cb782` | 成功 |
| `--warning` | `#f2c94c` | 警告 |
| `--danger` | `#eb5757` | 危险 |
| `--text-primary` | `#edeef0` | 主文字 |
| `--text-secondary` | `#9a9da2` | 次要文字/坐标轴 |
| `--map-area` | `#1a1c20` | 地图无数据区域底色 |
| `--map-boundary` | `#9a9da2` | 地图国家/省级边界 |
| `--text-muted` | `#62666d` | 弱化文字/时间戳 |

## Chart Color Palette
- 系列色: #5e6ad2, #4ea7fc, #4cb782, #f2c94c, #9a9da2
- 单一系列图表（如单折线）只用 `#5e6ad2`；灰 `#9a9da2` 只用于对照/基线系列。

## Chart Fingerprint
- 折线：线宽 2px，`symbol: none` 不显示数据点，仅 hover 时在该点出现 6px 圆点；允许面积填充但仅 `#5e6ad2` 从 8% 透明度渐变到 0，多系列折线禁止面积填充；hover 触发 axisPointer 细竖线（1px `--border-subtle`）。
- 柱形：仅上圆角 `barBorderRadius: [3,3,0,0]`，柱宽 ≤ 40%，纯色填充，禁止柱内渐变；hover 时该柱亮度 +15%，不用阴影不用描边。
- 饼/环图：只用环形，`radius: ['55%','75%']`，中心可放 KPI 大数字；标签不进图表区，靠图例+tooltip 传达；禁止发光、禁止描边高亮放大，hover 仅扇区透明度 1→0.85。
- 网格线：只保留 Y 轴横向虚线 `[4,4]` 1px `--border-subtle`；X 轴网格线、坐标轴线、刻度线全部隐藏。
- Tooltip：背景 `--bg-elevated`，1px `--border-subtle` 边框，无阴影，文字 12px，数值用 mono 字体。
- 图例：11px `--text-secondary`，方形小色块 8×8 圆角 2px；数据标签默认关闭，仅在柱顶必要时显示 11px mono `--text-secondary`。
- 折线优先用 endLabel 替代图例：末端直接标注系列名（11px `--text-secondary`，与系列同色），仅 ≥4 系列或环形图才回退图例。
- markLine：均值用虚线 `[4,4]` 1px `--text-muted`，目标值用实线 1px `--accent-primary`，标签 11px mono 置于线末端，不加符号。
- markArea：仅用于标注明确的异常/目标区间（如维护窗口），填充 `rgba(94,106,210,0.06)`，无描边，标签 11px `--text-muted`。
- 阈值染色：柱形/进度条超阈值时该柱切 `--warning`/`--danger` 纯色，不做渐变过渡，其余柱保持系列色。
- 面积渐变只给主系列：仅 `#5e6ad2` 单一系列折线允许 8%→0 渐变，其余系列一律无填充。
- 排他签名：面积填充全库最克制——仅单一系列 8%→0，多系列一律纯线（别家最低 10% 起）；柱宽 ≤40% 是全库最窄数值签名；hover 仅 1px 细竖线 axisPointer 全库独占，crosshair 十字准线归 palantir，本主题禁用。
- 允许：单一紫主色贯穿、极淡（≤8%）面积渐变、mono 数字。
- 禁止：任何发光/外阴影、柱状渐变、3D、环形图空心以外的装饰（无中心图标无环形轨道线）。

## Token Schema

| Token | 值 | 说明 |
|--------|----|------|
| `--radius-card` | `6px` | 卡片圆角 |
| `--radius-button` | `5px` | 按钮圆角 |
| `--radius-panel` | `6px` | 面板圆角 |
| `--font-family-base` | `"Inter", -apple-system, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif` | 全局 |
| `--font-family-display` | `"Inter", -apple-system, "Segoe UI", "PingFang SC", sans-serif` | 大数字/标题（letter-spacing -0.02em） |
| `--font-family-mono` | `"JetBrains Mono", "SF Mono", Consolas, monospace` | 数字/时间戳 |
| `--font-size-display` | `26px` | 页头标题 |
| `--font-size-title` | `14px` | 卡片标题 |
| `--font-size-kpi` | `34px` | KPI 大数字（550 字重 + tabular-nums） |
| `--shadow-card` | `none` | 全站无投影 |
| `--glow-accent` | `none` | 无发光 |
| `--decoration` | `flat` | 纯平：无渐变面板、无发光、无高光线 |
| `--bg-pattern` | `grid` | 页面层工程网格纹理，24px 小格（IDE 编辑器网格感；与 palantir 32 / sentry 40 / grafana 48 参数化区分），必须极淡近乎不可见 |
| `--pattern-color` | `rgba(255,255,255,0.03)` | 深色底上的纹理色，仅作纸面肌理，不得喧宾夺主 |
| `--kpi-variant` | `plain` | 纯大数字+单位降级：无状态染色、无装饰条，全靠排版 |

## Typography
- 全局 Inter，基准 13px，行高 1.4，信息密度优先
- 卡片标题 14px/500；正文与坐标轴 11-12px
- 所有数字（KPI、表格数值、tooltip 数值）用 mono 或 Inter 开 `font-variant-numeric: tabular-nums`
- 大标题 letter-spacing -0.02em，标签/表头 letter-spacing +0.01em

## Border Radius
卡片/面板 6px，按钮 5px，小元素（badge、图例色块、进度条）2-3px。全站只有这一组尺度，禁止混用。

## Shadows
不用任何 box-shadow。层级靠 `--bg-card` → `--bg-elevated` 的明度阶梯表达，悬停靠背景色微变（`--bg-hover`）。

## Motion
- 签名动效：120ms ease-out 即时反馈——hover/选中只切背景明度（`--bg-hover`），零位移零缩放，跟手感即签名
- 入场编排：图表入场 400ms 一次性，全屏同步开始、无 stagger——Linear 不做编排做整齐；禁止循环呼吸动画
- 展开/收起: 200ms ease-in-out
- 数字滚动: 600ms ease-out，不加回弹

## Layout & Grid

| 属性 | 值 |
|------|-----|
| 页面最大宽度 | 1920px |
| 网格系统 | 12 列 CSS Grid，列间距 16px |
| 卡片间距 | 16px |
| 页面内边距 | 24px |
| 图表容器最小高度 | 280px |
| 对齐方式 | 全部左对齐，拒绝居中排版 |

页面背景叠 `--bg-pattern: grid`（`--pattern-color` 极淡网格线），仅作图纸肌理；卡片、图表区背景保持 `--bg-card` 不透明，纹理不得穿透卡片影响可读性。

## Component Specifications

### KPI 卡片
- `--kpi-variant: plain`：纯大数字+单位降级形态，整卡不染状态色、无顶部色条、无环形/胶囊装饰
- 背景 `--bg-card`，1px `--border-subtle`，圆角 6px，内边距 14px 16px，无阴影
- 顶部一行：12px `--text-muted` 标签（左）+ 迷你状态点（右，6px 圆点用 success/warning/danger）
- 大数字 34px/550 mono `--text-primary` 左对齐，letter-spacing -0.02em
- 数字下方 6px：12px 变化量，涨 `--success` 跌 `--danger`，格式 `+12.4%` 不带箭头图标
- hover：背景变 `--bg-hover`，120ms，无边框变化无位移

### 图表容器
- 同 KPI 卡片外观（`--bg-card` + 1px 边框 + 6px），内边距 16px
- 标题 14px/500 `--text-primary` 左对齐，同行右侧放 12px `--text-muted` 副信息（如"近 30 天"）
- 标题距图表区 12px，容器内不再有二级边框或分隔线

### 按钮
- 主按钮：`--accent-primary` 底白字，圆角 5px，内边距 7px 14px，13px/500；hover 背景 `#6d79e0`（同色相提亮，非透明度叠加）
- 次按钮：透明底 + 1px `--border-subtle`，hover 背景 `--bg-hover`
- 主按钮全屏最多 1 个；禁用态 40% 透明度

### 数据表格
- 表头：11px `--text-muted` 全大写字母（letter-spacing +0.05em），底部 1px `--border-subtle`，无背景色
- 行高 40px，行与行之间仅 1px `--border-subtle` 分隔，不用斑马纹
- hover 行：整行背景 `--bg-hover`；选中行：左侧 2px `--accent-primary` 竖条（Linear 列表签名式处理）
- 数字列 mono 右对齐，文字列左对齐，状态列用彩色小字 badge（2px 圆角）

### 页头
- 背景 `--bg-primary`，底部 1px `--border-subtle`，高度 52px
- 左：产品名/标题 15px/600 `--text-primary`；右：时间戳 12px mono `--text-muted` + 可选一个主按钮
- 不做大标题横幅，页头是工具栏不是海报

### 进度条
- 高度 3px，圆角 2px，轨道 `--border-subtle`
- 填充 `--accent-primary` 纯色；超阈值（如 >90%）可切 `--warning`/`--danger`
- 右侧 11px mono `--text-muted` 百分比，与进度条同基线

## Anti-Patterns
- ❌ 任何 box-shadow / 发光 / backdrop-blur（flat 主题）
- ❌ 渐变面板、渐变柱形、顶部高光线
- ❌ 居中排版（标题、KPI、页头一律左对齐）
- ❌ 斑马纹表格、加粗分隔线、卡片内再套卡片
- ❌ 第二种强调色滥用：`--accent-secondary` 蓝只用于链接/次系列，不与紫并列做主视觉
- ❌ 大号圆角（>6px）、圆角混用、圆形 KPI 图标底座

## Do's and Don'ts
✅ 全站只用紫 `#5e6ad2` 一个主强调色，系列色按 Chart Color Palette 顺序取
✅ 数字一律 mono/tabular-nums，保证纵向对齐
✅ 悬停只改背景明度（`--bg-hover`），120ms，不位移不缩放
✅ 选中/激活用 2px 左侧紫色竖条表达
✅ 边框统一 1px `--border-subtle`，层级靠背景明度阶梯而非阴影
❌ 不要纯黑 `#000` 背景（`--bg-primary` 是带灰度的近黑）
❌ 不要给图表加外发光、轨道线、中心图标等"大屏感"装饰
❌ 不要用箭头 emoji/SVG 表达涨跌，用 `+/-` 加状态色文字
