# Design Toolkit — 设计师工具风

## Visual Theme
创意工作者的暗色画布：深灰面板、微圆角、细密边框，界面本身极度克制扁平，所有视觉能量来自高饱和品牌色（选择蓝/组件紫/成功绿/信号橙）。像 Figma 编辑器一样——工具感优先，装饰让位于内容。

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-primary` | `#1e1e1e` | 主背景（编辑器底色） |
| `--bg-card` | `#2c2c2c` | 卡片/面板 |
| `--bg-elevated` | `#383838` | 悬浮层/tooltip |
| `--bg-hover` | `#444444` | 交互悬停背景 |
| `--border-subtle` | `#3e3e3e` | 细分隔线 |
| `--accent-primary` | `#0d99ff` | 主强调（Figma 选择蓝） |
| `--accent-secondary` | `#9747ff` | 组件紫（仅次强调/系列色） |
| `--accent-success` | `#14ae5c` | 成功绿 |
| `--accent-warning` | `#ffcd29` | 警示黄 |
| `--accent-danger` | `#f24822` | 错误红 |
| `--text-primary` | `#ffffff` | 主文字 |
| `--text-secondary` | `#b3b3b3` | 次要文字 |
| `--map-area` | `#383838` | 地图无数据区域底色 |
| `--map-boundary` | `#b3b3b3` | 地图国家/省级边界 |
| `--text-muted` | `#7a7a7a` | 弱化文字/轴标签 |

## Token Schema

| Token | 值 | 说明 |
|--------|----|------|
| `--radius-card` | `6px` | 卡片圆角 |
| `--radius-button` | `6px` | 按钮圆角 |
| `--radius-panel` | `4px` | 面板圆角 |
| `--font-family-base` | `"Inter", -apple-system, Segoe UI, PingFang SC, Microsoft YaHei, sans-serif` | 正文（Google Fonts 加载 Inter，系统字体栈尾兜底） |
| `--font-family-display` | `"Inter", -apple-system, Segoe UI, PingFang SC, Microsoft YaHei, sans-serif` | 大数字/标题，600 字重 |
| `--font-family-mono` | `"JetBrains Mono", SF Mono, Consolas, monospace` | 表格数字/代码 |
| `--font-size-display` | `30px` | 大屏主标题 |
| `--font-size-title` | `13px` | 面板标题（uppercase, 字距 0.5px） |
| `--font-size-kpi` | `30px` | KPI 大数字 |
| `--shadow-card` | `0 2px 4px rgba(0,0,0,0.2), 0 0 0 1px rgba(0,0,0,0.1)` | 多层工具阴影 |
| `--glow-accent` | `none` | Figma 无任何发光 |
| `--decoration` | `flat` | 纯平：无渐变面板、无发光、无高光线 |
| `--bg-pattern` | `dots` | 页面层圆点纹理，20px 间距密点（像素网格感；spotify 用 32px 疏点、supabase 用 16px，三家参数化区分，互不借用间距） |
| `--pattern-color` | `rgba(255,255,255,0.04)` | 深色主题纹理色，仅可感知不可喧宾 |
| `--kpi-variant` | `sparkline` | KPI 卡内嵌迷你趋势线，工具面板的信息密度 |

## Chart Fingerprint

- 折线：2px 实线；数据点**常显** 5px 小方块（symbol `rect`，呼应矢量节点——全库深色主题唯一的常显方块 symbol，与 palantir 常显圆点构成方/圆签名对位），白色 1.5px 描边；面积渐变只给主系列且极克制（accent 色 8% → 0% 透明），其余系列一律纯线；hover 时当前系列数据点放大至 7px，其余系列降透明度至 40%
- 柱形：仅上圆角 `[4,4,0,0]`；纯色填充，禁止渐变；hover 亮度提升 15%，无发光无阴影
- 饼/环图：只用环图，radius `['48%','72%']`；标签在环外引导线，11px `--text-secondary`；禁止发光、禁止扇区投影
- 网格线：仅横向虚线 `[4,4]` 1px，色用 `--border-subtle`；纵向网格线一律关闭
- Tooltip：背景 `#1e1e1e`，1px `--border-subtle` 边框，圆角 6px，阴影 `0 4px 12px rgba(0,0,0,0.4)`
- 图例：折线/柱形图不用图例——用 endLabel 在系列末端直接标注系列名（11px，跟随系列色，末端数据点旁右对齐）；仅饼/环图保留图例，8px 方形色块（圆角 1px，呼应矢量锚点，不用圆形），11px `--text-secondary`，置于图表顶部左对齐
- markLine：折线/柱形图叠加均值虚线（`[4,4]`，1px `--text-muted`，标注 11px 灰色）；有业务目标值时改实线 `--accent-primary`，同图至多两条 markLine
- 阈值染色：折线越过 markLine 目标实线的区段用 `--accent-success` / `--accent-danger` 分段染色，未越界段保持系列色
- 数据标签：默认隐藏，仅 hover 通过 tooltip 呈现，不常驻显示
- 允许：主系列低透明度面积渐变、多彩系列色并排、hover 高亮当前系列
- 禁止：一切发光/霓虹、3D、柱形渐变、饼图投影、纵向网格线

## Typography
- 全局: **Inter**，基准 12-13px，工具界面密度
- 面板标题: 13px 600 uppercase，字距 0.5px，`--text-muted`
- KPI 大数字: 30px 600，`--text-primary`，开启 tabular-nums
- 轴标签/图例: 11px 400，`--text-muted`

## Border Radius: **4-6px**（卡片 6 / 按钮 6 / 面板与进度条 4 / tooltip 6，任何元素不得超过 6px）

## Shadows: 仅多层工具阴影 `0 2px 4px rgba(0,0,0,0.2), 0 0 0 1px rgba(0,0,0,0.1)`；悬浮层用 `0 4px 12px rgba(0,0,0,0.4)`；无彩色投影

## Motion
- 动效人格: 工具型跟手档——悬停/选中反馈 100ms ease-out（全库最快档之一，与 grafana/palantir/sentry 并列）
- 签名动效: 选中/悬停目标以选择蓝 tint 淡入 100ms，像编辑器 hover 选区高亮；折线 hover 时 5px 方块放大至 7px，其余系列降至 40% 透明度
- 入场编排: 面板按 Z 字阅读顺序 40ms stagger 入场（像图层面板逐项加载），图表 400ms ease-out，无回弹无弹性

## Layout & Grid

| 属性 | 值 |
|------|-----|
| 页面最大宽度 | 1920px |
| 网格系统 | CSS Grid，工具面板式紧密排布 |
| 卡片间距 | 12px |
| 页面内边距 | 20px |
| 图表容器最小高度 | 280px |
| 对齐方式 | 全部左对齐（含 KPI 数字） |

## Component Specifications

### KPI 卡片
- 背景 `--bg-card`，1px `--border-subtle` 边框，圆角 6px，内边距 14px 16px
- 标签在上：11px 600 uppercase `--text-muted`，字距 0.5px（Figma 面板标题语言）
- 大数字：30px 600 Inter，左对齐，tabular-nums
- 趋势：小三角箭头 + 百分比，12px，成功绿 `#14ae5c` / 错误红 `#f24822`，置于数字右侧同行
- Sparkline：卡底部嵌 36px 高迷你折线，1.5px `--accent-primary` 纯色无面积，不显示数据点与坐标轴，末端对齐趋势方向用成功绿/错误红
- 悬停：背景变为 `--bg-hover`，边框不变，100ms 过渡

### 图表容器
- 背景 `--bg-card`，1px `--border-subtle` 边框，圆角 4px，内边距 16px
- 标题：13px 600 uppercase `--text-muted`，左对齐，距图表 12px；右上角可放 11px 灰色图注
- 图表区：严格按 Chart Fingerprint 执行
- 选中/激活态用蓝色半透明 tint `rgba(13,153,255,0.15)`，不加粗边框（全库唯一 tint 式选中反馈，其他主题一律不用 tint）

### 按钮
- 主按钮：`#0d99ff` 背景，白字，圆角 6px，内边距 8px 16px，13px 500
- 次按钮：透明背景 + 1px `--border-subtle` 边框，`--text-primary` 文字
- 悬停：主按钮加深为 `#007be5`，次按钮背景变 `--bg-hover`
- 禁用：40% 透明度，禁止改变颜色

### 数据表格
- 表头：12px 600 uppercase `--text-muted`，底部 1px `--border-subtle`，无背景色
- 数据行：行高 40px（工具密度），行间 1px `--border-subtle` 分隔，不用斑马纹
- 悬停行：整行背景 `rgba(13,153,255,0.08)`（Figma 选中蓝 tint），不用左侧色条
- 数字列：mono 字体右对齐；文字列左对齐 13px

### 页头
- 高度 48px（顶部工具栏尺度），背景 `--bg-primary`，底部 1px `--border-subtle`
- 标题：18px 600 `--text-primary` 左对齐，前置 14px 彩色方块 logo 占位（用系列色拼接）
- 右侧：时间/筛选器，12px `--text-muted`

### 进度条
- 高度 4px，圆角 2px，背景 `--bg-elevated`
- 填充：`#0d99ff` 纯色，无渐变无光晕
- 标注：百分比 12px mono，`--text-muted`，右对齐同行

## Chart Color Palette
- 系列色: #0d99ff, #9747ff, #14ae5c, #ff7237, #ffcd29

## Anti-Patterns
- ❌ 禁止任何发光/霓虹效果（`--glow-accent` 为 `none`），Figma 视觉能量来自色彩本身
- ❌ 禁止大面积渐变背景或渐变柱形，只允许折线下 8% 透明度的面积渐变
- ❌ 紫色 `#9747ff` 不得作主强调色——主强调永远是选择蓝 `#0d99ff`，紫只出现在系列色/次强调
- ❌ 圆角超过 6px、圆角胶囊按钮均为违规
- ❌ 禁止居中对齐的大数字与标题，全部左对齐

## Do's and Don'ts
- ✅ 面板标题用 13px uppercase + 宽字距，这是 Figma 的界面语言
- ✅ 选中/悬停态用蓝色半透明 tint 而非加边框或变色块
- ✅ 折线数据点用小方块，呼应矢量节点
- ✅ 保持 12px 卡片间距的工具面板密度
- ❌ 不要用纯黑 `#000000` 背景，主背景必须是 `#1e1e1e`
- ❌ 不要给图表加彩色投影或外发光
- ❌ 不要在饼图/环图扇区间留白色粗描边分割
