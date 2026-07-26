# Checkout Light — 亮色支付简洁风

## Visual Theme
支付基础设施标杆。浅色大屏：雾蓝白底 + 纯白卡片 + 海军蓝文字，blurple `#635bff` 只做克制的强调点缀（高光线、按钮、进度条）。干净、克制、教科书级的留白与层级。

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-primary` | `#f6f9fc` | 主背景（Stripe 标志性雾蓝白） |
| `--bg-card` | `#ffffff` | 卡片/面板/图表容器 |
| `--bg-elevated` | `#eef3f9` | 悬浮面板/选中行 |
| `--bg-hover` | `#f0f5fa` | 行悬停/控件悬停 |
| `--border-subtle` | `#e6ebf1` | 边框/分割线 |
| `--accent-primary` | `#635bff` | 主色（Stripe blurple） |
| `--accent-secondary` | `#00d4ff` | 辅助强调（青蓝，渐变末端） |
| `--accent-success` | `#00a869` | 成功/上涨 |
| `--accent-warning` | `#c75101` | 警告 |
| `--accent-danger` | `#df1b41` | 失败/下跌 |
| `--text-primary` | `#0a2540` | 主文字（海军蓝，非纯黑） |
| `--text-secondary` | `#425466` | 次要文字/坐标轴 |
| `--map-area` | `#eef3f9` | 地图无数据区域底色 |
| `--map-boundary` | `#425466` | 地图国家/省级边界 |
| `--text-muted` | `#8898aa` | 弱化文字/KPI 标签 |

## Chart Color Palette
- 系列色: #635bff, #00d4ff, #ff5996, #ff7a00, #00a869
- 同屏最多 3 个 accent 系列色同时出现，其余用主色的深浅变体

## Chart Fingerprint（生成 ECharts option 时严格执行）
- 折线：线宽 2.5px，`smooth: true`，默认不显示数据点；面积渐变允许——顶部系列色 18% 透明度渐变到 0%，仅主系列填充；hover 显示十字准线，命中点放大为 6px 白边圆点
- 柱形：仅上圆角 `barBorderRadius: [4,4,0,0]`，纯色填充（禁止柱体渐变）；hover 颜色加深 10%，不位移不放大
- 饼/环图：一律环图 `radius: ['45%','70%']`，标签用外部引导线 + 12px `--text-secondary`，中心可放 KPI 总数；禁止任何发光/阴影
- 网格线：仅横向虚线 `[4,4]` 1px，颜色 `--border-subtle`；纵向无网格线；轴线不显示
- Tooltip：白底 + 1px `--border-subtle` 边框 + `--shadow-card` 蓝色调柔和阴影，文字 `--text-primary`，圆角 8px
- 排他签名：环图 `radius: ['45%','70%']` 是全库最粗环（别家环图内半径 55% 起）——数值即签名；且本主题是浅色组唯一允许 Tooltip 带彩色调阴影的主题（别家浅色 Tooltip 用灰阴影或无边框）
- 末端标注：单系列折线一律 `endLabel` 替代图例——系列色 12px 系列名 + 末值，放折线末端右侧；仅多系列对比才启用图例
- 参考线：`markLine` 均值虚线（`--text-muted` `[4,4]` + 12px 均值标注）；目标线用 `--accent-primary` 实线，标注"目标"二字；不用 markArea 与阈值染色
- 图例：12px `--text-secondary`，圆点图标，放容器右上角；数据标签默认隐藏，仅在饼图引导线上出现
- 允许：折线面积渐变（≤18% 透明度）、卡片顶部 3px accent 高光线、胶囊按钮
- 禁止：发光/text-shadow/box-shadow 发光、深色系背景、玻璃拟态、大面积渐变铺底、柱体渐变

## Token Schema

| Token | 值 | 说明 |
|--------|----|------|
| `--radius-card` | `8px` | 卡片圆角 |
| `--radius-button` | `999px` | 胶囊按钮（Stripe 标志形态） |
| `--radius-panel` | `8px` | 面板圆角 |
| `--font-family-base` | `'Inter',system-ui,-apple-system,sans-serif` | 正文字体栈（替代 sohne 的近似几何无衬线） |
| `--font-family-display` | `'Inter',system-ui,-apple-system,sans-serif` | 标题字体栈 |
| `--font-family-mono` | `'IBM Plex Mono','SF Mono',Menlo,Consolas,monospace` | 数字/代码字体栈 |
| `--font-size-display` | `32px` | 页头标题 |
| `--font-size-title` | `16px` | 面板标题 |
| `--font-size-kpi` | `40px` | KPI 大数字 |
| `--shadow-card` | `0 2px 5px -1px rgba(50,50,93,0.1), 0 1px 3px -1px rgba(0,0,0,0.1)` | 蓝色调双层柔和阴影 |
| `--glow-accent` | `none` | 本主题无发光 |
| `--decoration` | `gradient` | 渐变仅限高光线/进度条/折线面积，面板纯白 |
| `--bg-pattern` | `none` | 页面无纹理——雾蓝白底必须纯净，纹理会破坏 Stripe 的留白感 |
| `--pattern-color` | `rgba(0,0,0,0.04)` | 纹理关闭，占位色（浅色主题基准透明度） |
| `--kpi-variant` | `delta-pill` | 涨跌胶囊：大数字旁放 ▲/▼ 胶囊（浅色状态底 + 状态色字，999px 全圆角） |

## Typography

| Role | Font | Size | Weight | 特殊处理 |
|------|------|------|--------|----------|
| KPI 大数字 | mono 栈 | 40px | 700 | tabular-nums，左对齐 |
| KPI 标签 | base 栈 | 11px | 600 | uppercase，letter-spacing 0.05em，`--text-muted` |
| 面板标题 | display 栈 | 16px | 600 | 左对齐，`--text-primary` |
| 页头标题 | display 栈 | 32px | 700 | letter-spacing -0.02em |
| 坐标轴/图例 | base 栈 | 12px | 400 | `--text-secondary` |
| 表格正文 | base 栈 | 14px | 400 | line-height 1.5 |

## Border Radius
- 卡片/面板: **8px**
- 按钮/进度条/标签 chip: **999px 全圆角**
- Tooltip/输入框: **6px**
- 表格: 无圆角

## Shadows
- 卡片: `--shadow-card`（蓝色调，禁止灰黑阴影）
- 签名纪律: `rgba(50,50,93,...)` 蓝色调阴影是全库唯一"阴影带品牌色温"的浅色主题（别家浅色为暖棕或纯灰黑阴影）
- 悬停卡片: `0 6px 16px -4px rgba(50,50,93,0.16), 0 2px 6px -2px rgba(0,0,0,0.08)`
- 按钮: `0 4px 6px rgba(50,50,93,0.11), 0 1px 3px rgba(0,0,0,0.08)`

## Motion
- 悬停过渡: **150ms ease-out**（Stripe 交互偏快而轻）
- 阴影/上浮: **240ms ease-out**
- 数字滚动: **800ms ease-out**
- 签名动效: KPI 数字 800ms 滚动到位后，delta-pill 涨跌胶囊再淡入 200ms——先数后势
- 入场编排: 无 stagger、无飞入、无位移，所有卡片整屏同现——Stripe 的大屏是加载即完成
- 禁止弹簧回弹、禁止入场飞入动画

## Layout & Grid

| 属性 | 值 |
|------|-----|
| 网格系统 | CSS Grid, 12 列 |
| 卡片间距 | 24px（Stripe 偏好宽松留白） |
| 页面内边距 | 32px 上下, 40px 左右 |
| 图表容器最小高度 | 300px |
| 对齐方式 | 全部左对齐（标题/KPI/表格），图例外置右上 |

宽松是 Stripe 的奢侈：24px 间距 + 40px 左右内边距是全库最宽松布局，不得压缩。

## Component Specifications

### KPI 卡片
- 白底 + 8px 圆角 + `--shadow-card`，顶部 3px `--accent-primary` 高光线（仅首 KPI 或主指标，其余无高光线；本主题高光线一律纯色 blurple，airbnb 的渐变高光线在本主题禁用）
- **大数字**: mono 栈 40px 700，`--text-primary`，左对齐，tabular-nums
- **标签**: 11px 600 uppercase，`--text-muted`，在大数字上方（eyebrow 式）
- **趋势**: delta-pill 涨跌胶囊——▲/▼ + 百分比，状态色 10% 透明度浅底 + `--accent-success` / `--accent-danger` 字，999px 全圆角，放数字右侧
- **悬停**: 阴影过渡到悬停档，无位移

### 图表容器
- 白底 + 8px 圆角 + `--shadow-card`，无边框（靠阴影与底色分层）
- **标题**: 16px 600 左对齐，副标题 13px `--text-secondary` 紧随其后
- **图例/时间切换**: 容器右上角，胶囊 chip 样式
- 网格线/Tooltip 按 Chart Fingerprint 执行

### 按钮
- **主按钮**: 胶囊 999px，`--accent-primary` 底 + 白字 + 按钮阴影，内边距 8px 20px，14px 600
- **次按钮**: 胶囊，白底 + `--border-subtle` 边框 + `--text-primary` 字
- **悬停**: 主按钮底色加深为 `#5851ea`，阴影略微增强；禁用 40% 透明度

### 数据表格
- 无竖向分隔线；行分隔 1px `--border-subtle`，行高 52px
- 表头: 11px 600 uppercase，`--text-muted`，无底色的干净表头
- 悬停行: 背景 `--bg-hover`，无左边框变色
- 数字列: mono 栈右对齐；状态用胶囊 chip（浅色底 + 彩色字）

### 页头
- 白底 + 底部 1px `--border-subtle`，高度 64px
- 标题 32px 700 `--text-primary` 左对齐，上方可放 11px uppercase blurple eyebrow 标签
- 右侧: 时间 14px `--text-muted` + 胶囊筛选按钮

### 进度条
- 高度 6px，全圆角 999px
- 轨道 `--border-subtle`；填充 `--accent-primary → --accent-secondary` 线性渐变（全屏仅此处与高光线允许渐变）
- 标注: 百分比 12px `--text-muted` 右侧

## Anti-Patterns
- ❌ 深色/暗色背景——本主题必须是浅色大屏
- ❌ 纯黑 `#000000` 文字，一律用海军蓝 `#0a2540`
- ❌ 发光、text-shadow、backdrop-filter 玻璃拟态
- ❌ 大面积渐变铺底或渐变卡片（渐变仅限进度条/高光线/折线面积）
- ❌ 直角或小于 999px 圆角的按钮
- ❌ 灰黑色阴影（阴影必须带 `rgba(50,50,93,...)` 蓝色调）
- ❌ 同屏超过 3 个 accent 色（Stripe 的克制即高级感）

## Do's and Don'ts
✅ KPI 标签用 11px uppercase eyebrow 风格，放在大数字上方
✅ 首 KPI 卡片加 3px blurple 顶部高光线，建立视觉锚点
✅ 按钮、进度条、chip 一律胶囊全圆角
✅ 数字一律 mono 字体栈 + tabular-nums
❌ 不要把 `#635bff` 当铺底色用——它是标点，不是墙纸
❌ 不要用紫色底配紫色字的组件（对比度损失）
❌ 不要给图表加任何发光或投影效果
