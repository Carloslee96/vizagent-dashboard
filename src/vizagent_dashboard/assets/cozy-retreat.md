# Cozy Retreat — 温暖舒适旅行风

## Visual Theme
浅色、温暖、圆角、留白优先。Airbnb 是浅色品牌：米白底色 + 纯白卡片 + 柔和阴影，Rausch 粉红 (#ff385c) 作唯一强调色，Babu 青与 Arches 橙作暖色辅助。整体气质是"民宿房源卡片"——亲切、可信赖、零科技感，禁止做成深色科技风。

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-primary` | `#f7f7f7` | 页面底色（Airbnb 标志性浅灰） |
| `--bg-card` | `#ffffff` | 卡片/面板纯白 |
| `--bg-elevated` | `#f0f0f0` | 表头、弹层、嵌套区 |
| `--bg-hover` | `#f7f7f7` | 行/卡片悬停 |
| `--border-subtle` | `#ebebeb` | 分隔线与卡片描边 |
| `--accent-primary` | `#ff385c` | Rausch 粉红（唯一主强调色） |
| `--accent-secondary` | `#d70466` | 深粉，hover/激活态 |
| `--success` | `#008a05` | 正向指标 |
| `--warning` | `#fc642d` | Arches 橙，预警 |
| `--danger` | `#c13515` | 负向指标（暖棕红，非亮红） |
| `--text-primary` | `#222222` | 主文字（不用纯黑） |
| `--text-secondary` | `#717171` | 次要文字 |
| `--map-area` | `#f0f0f0` | 地图无数据区域底色 |
| `--map-boundary` | `#717171` | 地图国家/省级边界 |
| `--text-muted` | `#b0b0b0` | 弱化文字 |

## Chart Color Palette
- 系列色: #ff385c, #00a699, #fc642d, #484848, #767676
- 第一系列固定用 Rausch 粉红；Babu 青与 Arches 橙拉开冷暖对比；Hof/Foggy 两档灰用于对照系列。

## Chart Fingerprint
- 排他签名: 全库唯一允许主系列柱体使用跨色品牌渐变（Rausch→Arches 纵向，仅主系列柱，其余主题一律纯色柱）；浅色组最粗 3px 折线线宽 + 22% 面积填充为双数值签名，数值本身即指纹。
- 折线: 线宽 3px，`smooth: true` 平滑曲线；默认不显示数据点，hover 时显示 8px 白边圆点；面积渐变允许——仅第一系列铺设，自上而下 系列色22%透明度 → 0；axisPointer 用 1px `#dddddd` 竖直线。
- 柱形: 单系列全圆角 `[6,6,6,6]`，堆叠/分组时仅顶部圆角 `[6,6,0,0]`；纯色填充，仅主系列允许 Rausch→Arches 纵向品牌渐变；hover 时柱体加柔和投影 `0 2px 8px rgba(0,0,0,0.15)`。
- 饼/环图: 只用环图，radius `['58%','78%']`，扇区 `borderRadius: 6` + 2px 白色间隙；标签走外部引导线，12px `#717171` + 百分比；中心可放总计大数字。
- 网格线: 仅横向虚线 1px `--border-subtle`(#ebebeb)，禁止纵向网格线；坐标轴线也省略。
- Tooltip: 白底、1px `#dddddd` 边框、圆角 12px、阴影 `0 6px 16px rgba(0,0,0,0.12)`，文字 `#222222`——浅色Tooltip，与深色科技风划清界限。
- 末端标注: 单系列折线/柱形用 endLabel 在末端直接标注系列名+末值（12px `#717171`），endLabel 替代图例，省掉图例行；≥2 系列时才保留图例。
- markLine: 时间序列默认叠加均值虚线（1px `#717171` dashed，标签 11px 置右端）；PM 给出目标值时目标线用 2px Rausch 实线，虚线=现状、实线=目标。
- 面积渐变只给主系列（第一系列），其余系列纯线，保持画面松弛。
- 图例 12px `#717171` 圆形图标；数据标签 11px `#717171`，只在柱顶等必要位置显示。
- 允许: 平滑曲线、≤22% 透明度的面积渐变、品牌渐变柱、大圆角扇区。
- 禁止: 一切发光/外发光、深色 tooltip、直角柱、3D 效果、霓虹配色。

## Token Schema
| Token | 值 | 说明 |
|--------|----|------|
| `--radius-card` | `16px` | 卡片圆角（标志性大圆角） |
| `--radius-button` | `8px` | 按钮圆角（Airbnb 标准圆角矩形） |
| `--radius-panel` | `12px` | 面板/输入框圆角 |
| `--font-family-base` | `"Nunito Sans", -apple-system, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif` | 全局字体（Nunito Sans 替代 Airbnb 自研 Cereal，Google Fonts 可加载） |
| `--font-family-display` | `"Nunito Sans", -apple-system, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif` | 大数字/标题同族，靠字重区分 |
| `--font-family-mono` | `ui-monospace, "SF Mono", Consolas, monospace` | 表格数字列 |
| `--font-size-display` | `30px` | 页头主标题 |
| `--font-size-title` | `16px` | 卡片标题 |
| `--font-size-kpi` | `40px` | KPI 大数字 |
| `--shadow-card` | `0 2px 8px rgba(0,0,0,0.08)` | 卡片静态柔和阴影 |
| `--glow-accent` | `none` | 本主题无发光 |
| `--decoration` | `gradient` | 面板纯白无发光；渐变仅用于强调元素（见组件规范） |
| `--bg-pattern` | `dots` | 页面层圆点纹理，像网格纸一样衬在白卡下，增加"家"的手工感 |
| `--pattern-color` | `rgba(0,0,0,0.05)` | 浅色底用低透明黑点，隐约可见不抢内容 |
| `--kpi-variant` | `sparkline` | KPI 卡底部迷你趋势图，像房源卡的价格走势，亲切直观 |

## Typography
- 全局 Nunito Sans 人文无衬线（圆角字腔贴合 Cereal 气质），fallback 见 Token Schema。
- KPI 数字 40px / 700；卡片标题 16px / 600 / #222222；副标题 13px / #717171。
- 正文 14px / 400 / line-height 1.5；辅助说明 12-13px / #717171。
- 数字开启 `font-variant-numeric: tabular-nums` 对齐。

## Border Radius
卡片 16px，面板 12px，按钮 8px，筛选 Chip 与进度条用全圆角 `999px`，图表柱顶圆角 6px。除此之外禁止出现其他圆角值，尤其禁止 0 直角。

## Shadows
- 卡片静态: `0 2px 8px rgba(0,0,0,0.08)`
- 卡片 hover: `0 6px 16px rgba(0,0,0,0.12)`（Airbnb 标志性浮起阴影）
- 禁用彩色阴影与发光。

## Motion
- 动效人格: 消费型"有感但轻"（200-350ms 区间），禁止弹跳与循环动画。
- 签名动效: 卡片 hover `translateY(-2px)` + 阴影加深，250ms ease-out——全库唯一的"位移式"hover（其余主题禁止位移），像房源卡片浮起，位移浮起是 airbnb 专利。
- 入场编排: 卡片从左到右 60ms stagger 依次入场，像房源列表横向滑动；数字滚动 800ms ease-out，图表入场 500ms ease-out。

## Layout & Grid

| 属性 | 值 |
|------|-----|
| 页面最大宽度 | 1920px |
| 网格系统 | CSS Grid，KPI 4 列，图表 12 列 |
| 卡片间距 | 20px |
| 页面内边距 | 32px |
| 图表容器最小高度 | 300px |
| 对齐方式 | 全部左对齐（含 KPI），Airbnb 不用居中排版 |

## Component Specifications

### KPI 卡片
- 白卡 + 16px 圆角 + `--shadow-card`，无硬边框；全部左对齐。
- 标签在上：13px 500 `#717171`；大数字在下：40px 700 `#222222`。
- 趋势小字 12px 带 ↑↓ 箭头，涨 `--success`(#008a05)、跌 `--danger`(#c13515)，不用亮红亮绿。
- 卡底配 sparkline 迷你趋势（`--kpi-variant: sparkline`）：Rausch 单色 2px 平滑线 + ≤15% 透明度面积，无坐标轴无边框。
- 仅主 KPI 卡顶部可加 3px Rausch→Arches 渐变高光线，其余卡片不加。

### 图表容器
- 白卡 + 16px 圆角 + `--shadow-card`，无 1px 硬边框，靠阴影分层。
- 标题 16px 600 `#222222` 左对齐，下方 13px `#717171` 一行副标题，距图表区 16px。
- 图表样式严格执行 Chart Fingerprint。

### 按钮
- 主按钮: Rausch→Arches 线性渐变底（`#ff385c`→`#d70466`）+ 白字，8px 圆角，hover 整体加深 8%——对应 Airbnb "Reserve" 按钮。
- 次按钮: 白底 + 1px `#222222` 边框 + `#222222` 字，hover 底色变 `#f7f7f7`。
- 筛选 Chip: `999px` 全圆角 + 1px `#dddddd` 边框，选中变黑底白字。
- 禁用态 40% 透明度，禁止发光与阴影按钮。

### 数据表格
- 无斑马纹，用 1px `#ebebeb` 行分隔线（Airbnb 列表式）。
- 表头 12px 600 `#717171`，底色 `--bg-elevated`；行高 52px。
- hover 整行 `#f7f7f7`，无左侧色条。
- 数字列 mono 字体右对齐，文字列左对齐。

### 页头
- 白底 + 底部 1px `#ebebeb` 分隔线，高度 64px。
- 标题 30px 700 `#222222` 左对齐；右侧时间/筛选器 14px `#717171`。
- 可放一枚粉红圆形 Logo 点（8px `#ff385c` 圆点）作品牌记号，禁止放发光 Logo。

### 进度条
- 高度 6px，全圆角；轨道 `#ebebeb`。
- 填充用 Rausch→Arches 渐变（`#ff385c`→`#fc642d`），不用纯色。
- 百分比标注 12px `#717171`，置于条右端外侧。

## Anti-Patterns
- 禁止深色背景/深色面板——本主题是浅色大屏。
- 禁止发光、霓虹、玻璃拟态、backdrop-blur。
- 禁止纯黑 `#000000` 文字与冷蓝紫科技色作主色。
- 禁止直角（0 圆角）卡片、按钮、柱形。
- 禁止斑马纹表格与纵向网格线。

## Do's and Don'ts
✅ 卡片 hover 像房源卡片一样轻微浮起（translateY + 阴影加深）
✅ 品牌渐变只给主 CTA、进度条、主 KPI 高光线，其余保持克制
✅ 大面积留白 + 全部左对齐，营造"家"的松弛感
✅ 暖色系辅助色（橙/青）配粉红，冷暖平衡
❌ 不要把 Airbnb 做成深色科技风，粉红糖果霓虹风同样禁止
❌ 不要给图表元素加任何外发光或彩色阴影
❌ 不要混用四档以外的圆角数值
❌ 不要把 Tooltip 做成深色——浅色白卡 Tooltip 是本主题指纹
