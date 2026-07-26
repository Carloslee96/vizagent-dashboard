# Command Post — 冷峻指挥中心风

## Visual Theme
克制、冷峻、工程感。像情报指挥中心的数据终端——实质胜于装饰，每一寸像素都要有信息价值。
近黑微冷背景 + 单色蓝阶 + 等宽数字 + 强网格。**蓝色是"挣来的"，不是泼上去的**：仅用于关键数据与交互态，绝不作装饰。

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-primary` | `#0A0B0D` | 主背景（近黑微冷，禁止纯黑 #000） |
| `--bg-card` | `#13151A` | 卡片/面板 |
| `--bg-elevated` | `#1A1D24` | 悬浮/表头/tooltip |
| `--bg-hover` | `#20242C` | 悬停态 |
| `--border-subtle` | `#23272F` | 边框/分隔线（1px 低对比） |
| `--accent-primary` | `#2D5BFF` | 主色（仅关键交互/主数据系列） |
| `--accent-secondary` | `#5B8AFF` | 次级数据高光 |
| `--accent-warning` | `#F5A623` | 警示（仅异常态） |
| `--accent-danger` | `#E5484D` | 危险/下降 |
| `--accent-success` | `#3DAB63` | 成功/上升 |
| `--text-primary` | `#E6E8EC` | 主文字（off-white，禁止纯白） |
| `--text-secondary` | `#8A8F98` | 次要文字/坐标轴 |
| `--map-area` | `#1A1D24` | 地图无数据区域底色 |
| `--map-boundary` | `#8A8F98` | 地图国家/省级边界 |
| `--text-muted` | `#5C6168` | 辅助/时间戳 |

## Chart Color Palette
- 系列色: `#2D5BFF`, `#5B8AFF`, `#8AAEFF`, `#B4CCFF`, `#3DAB63`（单色蓝阶为主，绿色仅作语义对照系列）
- 警示/异常: `#F5A623`, `#E5484D`（不进系列色，仅状态标记）

## Chart Fingerprint
- **排他签名**：折线 3px 实心圆点**常显**——全库深色主题唯一常显 symbol（与 figma 的常显方块构成圆/方对位）；柱形 hover 加 1px `--accent-primary` 描边是全库唯一的"描边式 hover"反馈（别家只变亮度）
- **折线**：线宽 2px，**显示数据点**（symbol: circle，3px，实心）；面积渐变允许但仅限主系列、透明度从 0.08 递减到 0，其余系列纯线；hover 触发十字准线（crosshair axisPointer，palantir 独占——linear 用 1px 细竖线 axisPointer，二者禁止互换），数值用等宽字体
- **柱形**：**直角（圆角 0）**，纯色填充禁止渐变；hover 整列提亮 10% 并描边 `--accent-primary` 1px
- **饼/环图**：细环 `radius: ['55%', '75%']`，标签走外侧引导线 + 等宽百分比；禁止任何发光/阴影
- **网格线**：仅水平虚线（`type: 'dashed'`，1px，`--border-subtle`），垂直网格线一律关闭
- **均值/目标**：折线/柱形叠加 markLine——均值用 `--text-muted` 虚线、目标用 `--accent-primary` 实线，标签用等宽 10px 小字置于线端
- **阈值染色与区间**：越界数据点/柱按阈值染 `--accent-warning` / `--accent-danger`；异常区间用 markArea 标注（`--accent-danger` 透明度 0.06 底纹，直角无边框）
- **Tooltip**：`--bg-elevated` 背景 + 左侧 2px `--accent-primary` 竖条（tooltip 竖条为 palantir 独占语境——linear 的 2px 竖条是列表选中态，二者不得混用），直角，无阴影无圆角，内部数字等宽
- **图例**：多系列折线一律用 **endLabel 替代图例**（线末端直接标系列名，11px 等宽，颜色随系列）；柱/饼等非折线图保留方形小色块图例于右上角；数据标签默认关闭，只标极值点
- **允许**：十字准线、极值标注、endLabel、markLine 均值/目标线、markArea 阈值区间、阈值染色、水平虚线网格、主系列低透明度面积
- **禁止**：平滑曲线加粗发光、柱子圆角/渐变、饼图发光、垂直网格、tooltip 投影

## Token Schema

| Token | 值 | 说明 |
|-------|-----|------|
| `--radius-card` | `3px` | 卡片圆角（锐利工程感） |
| `--radius-button` | `3px` | 按钮圆角 |
| `--radius-panel` | `2px` | 内嵌面板/tooltip 圆角 |
| `--font-family-base` | `"Inter", "Helvetica Neue", "PingFang SC", "Microsoft YaHei", sans-serif` | 正文/标签 |
| `--font-family-display` | `"Inter", "Helvetica Neue", "PingFang SC", sans-serif` | 标题（600，紧凑字距） |
| `--font-family-mono` | `"IBM Plex Mono", "JetBrains Mono", Consolas, monospace` | 一切数字/时间戳 |
| `--font-size-display` | `22px` | 页头标题 |
| `--font-size-title` | `15px` | 卡片标题 |
| `--font-size-kpi` | `40px` | KPI 大数字（等宽） |
| `--shadow-card` | `none` | 不用阴影，靠 1px 边框分层 |
| `--glow-accent` | `none` | 无发光，层次全靠边框与背景微变 |
| `--decoration` | `flat` | 纯平：无渐变面板、无发光、无高光线 |
| `--bg-pattern` | `grid` | 页面层背景网格纹理，32px 中格（linear 24px / grafana 48px 之间的工程图纸底纹，呼应"强网格"定位） |
| `--pattern-color` | `rgba(255,255,255,0.04)` | 深色主题网格线色（近乎不可见，只起定位参照，绝不抢数据） |
| `--kpi-variant` | `delta-pill` | KPI 卡：大数字旁涨跌胶囊（涨 success / 跌 danger，唯一药丸形例外） |

## Decorative Style
工程图纸的理性延伸——以极细几何线条为基调，拒绝任何有机曲线与装饰性插画。
- P0 标题栏：面板标题上方 1px 等宽渐变横线（accent 蓝 60% → transparenet 10%），无圆角，不做发光。
- P1 四角：左上/右下对称的 90° 直角 L 形角标，线宽 1px，色用 `--border-subtle`，40×40px，只描线不填充。
- P2 分隔线：KPI 区与图表区之间的 1px 水平虚线（`--border-subtle`），中间加一个 4px 菱形小点（accent 蓝）。
- 整体原则：**像工程图纸的标注线**——克制、精确、不抢数据风头。

## Typography
- 正文 13-14px `--font-family-base`，行高紧凑 1.4-1.5
- 标题 15-22px 600，`letter-spacing: -0.01em`，**一律左对齐**
- 一切数字：`--font-family-mono` + `font-variant-numeric: tabular-nums` 强制对齐
- KPI 标签：12px 500，**全大写 + `letter-spacing: 0.08em`**（终端标签风格）

## Border Radius
2-4px。卡片 3px、面板/tooltip 2px、按钮 3px。**禁止超过 6px**，禁止药丸形（KPI 涨跌胶囊是唯一例外）。

## Shadows
不用。层次靠 1px `--border-subtle` 边框 + 背景色阶（primary→card→elevated）区分。禁止任何装饰性 box-shadow / text-shadow。

## Component Specifications

### KPI 卡片
- `--bg-card` + 1px `--border-subtle` + 3px 圆角，内边距 18px 20px，无阴影
- 标签在上：12px 全大写宽字距 `--text-secondary`；大数字在下：40px 等宽 tabular `--text-primary`，左对齐
- 趋势：涨跌胶囊（delta-pill）紧跟大数字右侧基线对齐——12px 600 等宽 `↑ 3.2%` / `↓ 1.8%`，12% 状态色底 + `--accent-success` / `--accent-danger` 文字，药丸形（本主题唯一药丸形例外）
- 悬停：仅边框转 `--accent-primary`，背景不变

### 图表容器
- `--bg-card` + 1px `--border-subtle` + 3px 圆角，内边距 16px
- 标题 15px 600 左对齐，右上角可放等宽单位说明（11px `--text-muted`）
- 坐标轴 11px `--text-secondary`，轴线用 `--border-subtle`

### 按钮
- 主按钮：`--accent-primary` 纯色背景 + `#fff` 文字，3px 圆角，无阴影无渐变
- 次按钮：透明 + 1px `--border-subtle`，文字 `--text-secondary`
- 悬停：亮度 +8%，100ms；禁用态降透明度不改成色

### 数据表格
- 表头 `--bg-elevated`，12px 600 全大写 `--text-secondary`，下边框 1px `--border-subtle`
- 行高 44px，行间仅 1px 分隔线；悬停 `--bg-hover` + 左侧 2px `--accent-primary` 竖条
- 数字列等宽 tabular 右对齐，文字列左对齐；状态列用色点（6px 圆点）不用色块徽章

### 页头
- 56px 高，底部 1px `--border-subtle` 实线
- 标题 22px 700 左对齐，可带 4px 宽 `--accent-primary` 竖条前置
- 右侧：13px 等宽 UTC 时间戳 `--text-muted` + 在线状态绿点（`--accent-success`，唯一允许的脉冲动画）

### 进度条
- 高度 2-4px，**直角无圆角**；轨道 `--border-subtle`，填充 `--accent-primary` 纯色
- 禁止渐变填充、流光动画、光晕；百分比用等宽数字右对齐跟在条后

## Motion
- 动效人格：静态权威型——克制、即时、无表演；唯一允许的循环动画是状态指示点脉冲
- 签名动效：数据更新 300ms 等宽数字滚动——全库最快数字动画，情报终端的数字不等人
- 入场编排：面板按网格行优先 60ms stagger 入场，像终端开机自检逐项点亮；图表重绘用 ECharts 默认过渡
- 悬停 100ms 只变边框/亮度、不变位；展开 200ms ease-in-out
- 禁止流光边框、扫描线、呼吸光

## Layout & Grid

| 属性 | 值 |
|------|-----|
| 页面尺寸 | 1920×1080（按需自适应） |
| 网格系统 | CSS Grid 3-4 列，强对齐 |
| 卡片间距 | 16px |
| 页面内边距 | 24px |
| 图表容器最小高度 | 300px |
| 对齐方式 | 文字左对齐、数字右对齐，标题禁止居中 |

## Anti-Patterns（🔴 违反即不合格）
- ❌ 任何发光 / text-shadow / 装饰性 box-shadow / backdrop-filter 毛玻璃
- ❌ 渐变文字、渐变柱形、渐变进度条
- ❌ 圆角 > 6px、药丸形按钮/徽章（KPI 涨跌胶囊除外）
- ❌ 鲜艳青色 `#00E5FF` 等霓虹色；纯黑 `#000000` / 纯白 `#FFFFFF`
- ❌ 标题居中、数字用非等宽字体
- ❌ 省略面板 1px 边框（无框“裸卡片”在本主题视为未完成）
- ❌ 饼图/环图发光或中心大 Logo 装饰

## Do's and Don'ts
- ✅ 一切数字等宽 + tabular-nums，时间戳用 UTC 等宽小字
- ✅ KPI 标签全大写 + 宽字距，制造“终端标签”感
- ✅ 蓝色只给关键数据、主系列与交互态，其余用灰阶
- ✅ 每个面板 1px 边框 + 直角/微圆角，层次靠背景色阶
- ❌ 不要用装饰性图标/插画填充留白——留白本身是设计
- ❌ 不要把 warning/danger 色用作系列色，它们只属于状态
