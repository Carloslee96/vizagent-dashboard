# Fitness Glass — 健康玻璃环风

## Visual Theme
Apple 健康 App 的大屏化：iOS 系统灰底 `#F2F2F7` 上漂浮纯白卡片，层级只靠底色与卡面的色阶差，零边框零投影。每个指标拥有固定身份色——心红 `#FF2D55`、橙 `#FF9500`、靛 `#5856D6`、薄荷 `#30D158`，像健康 App 的"三环"一样一指标一色、全站贯穿。圆头进度环是唯一 KPI 形态，整体气质活泼、干净、消费级，禁止做成医疗科技风或深色仪表盘。

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-primary` | `#F2F2F7` | 页面底色（iOS 系统分组灰） |
| `--bg-card` | `#ffffff` | 卡片/面板纯白 |
| `--bg-elevated` | `#e5e5ea` | 环轨道、表头、嵌套区 |
| `--bg-hover` | `#f7f7fa` | 行/卡片悬停 |
| `--border-subtle` | `#e5e5ea` | 极细分隔线（克制使用） |
| `--accent-primary` | `#FF2D55` | 心红 — 第一指标身份色 |
| `--accent-secondary` | `#FF9500` | 橙 — 第二指标身份色 |
| `--accent-indigo` | `#5856D6` | 靛 — 第三指标身份色 |
| `--accent-success` | `#30D158` | 薄荷绿 — 正向/第四指标身份色 |
| `--accent-warning` | `#FF9500` | 警告（复用橙） |
| `--accent-danger` | `#FF2D55` | 危险（复用心红） |
| `--text-primary` | `#1c1c1e` | 主文字（iOS 深色文字，非纯黑） |
| `--text-secondary` | `#6e6e73` | 次要文字 |
| `--map-area` | `#e5e5ea` | 地图无数据区域底色 |
| `--map-boundary` | `#6e6e73` | 地图国家/省级边界 |
| `--text-muted` | `#aeaeb2` | 弱化文字/单位 |

## Typography
- 全局: SF Pro 风格人文无衬线（CDN 环境用 Inter，见 Token Schema）
- KPI 数字/单位**双字重对比**: 数字 44px 700 `--text-primary`；紧随的单位 15px 500 `--text-muted`，基线对齐，不得同字重同字号
- 页面标题: 28px 700；卡片标题: 16px 600 `--text-primary`
- 正文: 14px 400 line-height 1.5；标签/辅助: 12-13px 500 `--text-secondary`
- 数字开启 tabular-nums；字号对比要干脆：44px 数字 vs 12px 标签，中间不堆过渡字号

## Border Radius
- 卡片/面板: **18px**（16-20px 大圆角区间，全站固定 18px）
- 按钮/进度条/筛选 Chip: **999px** 全圆角 pill
- Tooltip/小浮层: 12px
- 全站只有这三档，禁止直角，禁止小于 10px 的圆角

## Shadows
**零投影**。层级完全靠 `#F2F2F7` 灰底与纯白卡面的色阶差分层；卡片、面板、按钮一律无 box-shadow，更禁止彩色阴影与发光。Tooltip 允许唯一的例外：`0 4px 16px rgba(0,0,0,0.08)`。

## Component Patterns
- **身份色系统**: 指标按顺序绑定 心红→橙→靛→薄荷 四色；同一指标的 KPI 环、图表系列、图例、进度条必须用同一身份色，全站可追踪
- **KPI = 圆头进度环**: 环形轨道 `--bg-elevated`，进度弧用该指标身份色，两端圆头（roundCap），环心放百分比大数字；同屏最多 4 个环、各环不同身份色——身份色多环与 apple 的单色蓝环互斥，禁止出现单色环
- **卡片即内容**: 白卡无装饰——无左边条、无顶部高光线、无图标堆砌，色彩只出现在数据本身

## Anti-Patterns
- ❌ 任何投影、发光、霓虹、backdrop-blur 毛玻璃
- ❌ 卡片边框、深色背景、直角或 <10px 圆角
- ❌ 指标与身份色错配（同一指标多处用不同颜色）
- ❌ 数字与单位同字重同字号——双对比是本主题指纹
- ❌ 医疗科技风装饰：扫描线、网格背景、心电图纹样、蓝紫冷色主导
- ❌ 图表网格线——本主题全库唯一全禁网格，LLM 默认画网格是头号错误
- ❌ 一屏超过 4 种身份色之外的彩色

## Motion
- **签名动效**: 圆头进度环弧长从 0 生长到目标值，**800ms ease-out**——apple 的环生长用 ease-in-out，本主题独占 ease-out 环生长，缓动参数即签名
- **入场编排**: KPI 环按身份色顺序（心红→橙→靛→薄荷）依次生长，间隔 **150ms**——把身份色系统延伸到时间维度；图表随后 500ms ease-out 入场
- 数字动画: **800ms ease-out**；悬停仅白卡微亮至 `--bg-hover`，无位移无阴影变化
- 禁止弹跳、回弹——动效要"感觉不到存在"

## Layout & Grid

| 属性 | 值 |
|------|-----|
| 页面最大宽度 | 1920px |
| 网格系统 | CSS Grid，KPI 4 列，图表 12 列 |
| 卡片间距 | 16px |
| 页面内边距 | 28px |
| KPI 卡片对齐 | 内容居中（环居中、标签在上） |
| 图表容器最小高度 | 300px |
| 对齐方式 | 标题左对齐 + KPI 居中，大量负空间 |

## Component Specifications

### KPI 卡片
- 白卡 + 18px 圆角，无边框零投影，内边距 24px，内容整体居中
- **标签在上**: 13px 500 `--text-secondary`
- **圆头进度环**: SVG 环，轨道 `--bg-elevated` 7px，进度弧身份色 7px `stroke-linecap:round`；环心百分比 28px 700 `--text-primary`
- 环下方数字行: 数值 20px 700 + 单位 13px 500 `--text-muted`（双字重对比）
- 悬停: 背景微亮 `--bg-hover`，无位移无边框变化

### 图表容器
- 白卡 + 18px 圆角，无边框零投影，内边距 24px
- 标题 16px 600 `--text-primary` 左对齐；右侧可放该图身份色 8px 圆点作标记，不加左侧色条
- 图表样式严格执行 Chart Fingerprint
- 容器靠 16px 间距与底色差分隔，不靠边框

### 按钮
- **主按钮**: `--accent-primary` 填充 + 白字，999px pill，内边距 10px 22px，14px 600
- **次按钮**: 白底 + 1px `--border-subtle` 边框 + `--text-primary` 文字，pill
- **悬停**: 主按钮亮度提升 8%；次按钮底色变 `--bg-hover`
- **禁用**: 40% 透明度，禁止发光与阴影按钮

### 数据表格
- 表头无底色：12px 600 `--text-secondary`，仅下方 1px `--border-subtle` 分隔线
- 数据行: 行高 48px，行间 0.5px 细线，无斑马纹无竖线
- 悬停行: 背景 `--bg-hover`，无左侧色条
- 数字列: tabular-nums 右对齐；文字列左对齐

### 页头
- 背景透明（融进 `--bg-primary`），高度 64px，无分割线靠留白分隔
- 标题 28px 700 `--text-primary` 左对齐；右侧时间 mono 字体 13px `--text-muted`
- 可放一组 4 枚身份色 8px 圆点作品牌记号，禁止发光 Logo

### 进度条
- 高度 6px，两端全圆头，轨道 `--bg-elevated`
- 填充用对应指标身份色纯色，无渐变无流光
- 百分比标注 12px `--text-muted`，置于条右端外侧

## Chart Color Palette
- 系列色: #FF2D55, #FF9500, #5856D6, #30D158, #64D2FF
- 前四色为固定身份色组，按指标顺序一一绑定；第五色浅蓝仅用于对照/基线系列

## Chart Fingerprint
ECharts option 严格按此生成：
- **折线**: 线宽 3px，`smooth:true`，`symbol:'none'` 常隐数据点，hover 浮现 8px 白心圆点；面积渐变只给主系列——同指标身份色自上而下 opacity 0.2→0，其余系列纯线
- **柱形**: 独立柱全圆角 `[6,6,6,6]`，堆叠柱仅首尾圆角；纯色填充，禁止柱体渐变；hover 亮度提升 10%
- **饼/环图 + gauge**: 一律细环 `radius:['62%','80%']`，扇区与仪表盘进度条必须 `roundCap:true` 圆头端点；扇区 `borderRadius:6` + 2px 白色间隙（borderColor 同 `--bg-card`）；外圈标签引线全部关闭，环心显示大数字
- **网格线**: **全库唯一禁用一切网格线**——横向纵向全部删除，坐标轴线隐藏，靠轴刻度文字定位；这是本主题第一指纹，LLM 默认画网格即视为失败
- **目标线**: **全库唯一"目标线非灰非虚"**——健康/达成类指标用 `markLine` 目标实线（身份色 2px，非虚线非灰色）标注目标值；仅均值参考用 `markLine` 虚线 `--text-muted`
- **末端标注**: 折线末端用 `endLabel` 直接标注系列名（身份色 12px），替代传统图例；仅多系列共用一图时才保留图例（12px `--text-secondary` 圆形图标）
- **Tooltip**: 白底、圆角 12px、无边框、阴影 `0 4px 16px rgba(0,0,0,0.08)`，文字 `--text-primary`
- **坐标轴刻度文字**: 11px `--text-muted`；数据标签默认关闭，仅环心与柱顶关键值可显示
- **允许**: roundCap 圆头、单色 20%→0 面积渐变、全圆角柱、markLine 目标线、endLabel 末端标注
- **禁止**: 一切网格线、发光/阴影、3D、柱体渐变、饼图外圈标签引线、深色 tooltip

## Do's and Don'ts
✅ 一指标一身份色，KPI 环、图表、进度条同色贯穿
✅ 数字 700 vs 单位 500 的双字重对比，单位缩到 1/3 字号
✅ 层级只靠灰底白卡色阶差，全程零边框零投影
✅ gauge/环图/进度条全部 roundCap 圆头
✅ markLine 目标实线呼应"健康目标"语义
❌ 不要给卡片加任何边框、投影或顶部高光线
❌ 不要画网格线——本主题的图表"悬浮"在白卡上
❌ 不要把身份色当装饰乱用，色彩只承载数据语义
❌ 不要做成深色医疗监控风——这是消费电子，不是 ICU

## Token Schema
| Token | 值 | 说明 |
|--------|----|------|
| `--radius-card` | `18px` | 卡片圆角（大圆角） |
| `--radius-button` | `999px` | 按钮圆角（pill） |
| `--radius-panel` | `18px` | 面板圆角 |
| `--font-family-base` | `'Inter',-apple-system,'PingFang SC','Helvetica Neue',sans-serif` | 正文字体栈（Inter 最接近 SF Pro） |
| `--font-family-display` | `'Inter',-apple-system,'PingFang SC',sans-serif` | 标题/大数字字体栈 |
| `--font-family-mono` | `'JetBrains Mono',ui-monospace,'SF Mono',Menlo,monospace` | 时间/编号等宽字体 |
| `--font-size-display` | `28px` | 页面大标题 |
| `--font-size-title` | `16px` | 面板标题 |
| `--font-size-kpi` | `44px` | KPI 大数字（单位 15px 双对比） |
| `--shadow-card` | `none` | 零投影——层级靠色阶差 |
| `--glow-accent` | `none` | 无发光 |
| `--decoration` | `flat` | 纯白平涂卡片，无渐变无发光无玻璃 |
| `--bg-pattern` | `none` | 无背景纹理——灰底白卡色阶差即分层 |
| `--pattern-color` | `rgba(0,0,0,0.04)` | 备用纹理色（bg-pattern=none 时不生效） |
| `--kpi-variant` | `ring` | KPI 卡形态：圆头进度环 |
