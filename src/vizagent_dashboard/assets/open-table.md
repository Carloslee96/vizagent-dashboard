# Open Table — 开源数据暗色风

## Visual Theme
午夜 IDE 质感：近黑炭灰画布、99% 灰度界面，磷光绿 `#3ecf8e` 是全场唯一的高饱和色，且被严格"配给"——只出现在主按钮、强调关键词、激活状态与主数据系列上。层级完全靠 1px 发丝边框对比建立，几乎不用阴影，绝无发光。气质安静、终端原生、工程师审美。

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-primary` | `#121212` | 页面画布（近黑炭灰） |
| `--bg-card` | `#171717` | 卡片/面板 |
| `--bg-elevated` | `#242424` | 悬浮层/Tooltip/悬停态 |
| `--bg-hover` | `#1f1f1f` | 行悬停/控件悬停 |
| `--border-subtle` | `#2e2e2e` | 发丝边框（核心分层手段） |
| `--accent-primary` | `#3ecf8e` | 磷光绿（配给使用） |
| `--accent-secondary` | `#00c573` | 链接/次级绿 |
| `--accent-code` | `#bda4ff` | 代码高亮紫（语法色） |
| `--success` | `#3ecf8e` | 成功态 |
| `--warning` | `#f59e0b` | 警告 |
| `--danger` | `#f43f5e` | 错误/危险 |
| `--text-primary` | `#fafafa` | 主文字 |
| `--text-secondary` | `#b4b4b4` | 次要文字 |
| `--map-area` | `#242424` | 地图无数据区域底色 |
| `--map-boundary` | `#b4b4b4` | 地图国家/省级边界 |
| `--text-muted` | `#6b6b6b` | 弱化文字/元数据 |

## Typography
- 全局正文: **"Inter", -apple-system, "Segoe UI", sans-serif**；标题/大数字: **"Nunito Sans", "Inter", -apple-system, sans-serif** —— 几何人文无衬线，标题用 400/500 字重，**绝不用 700 粗体**（anti-bold 是品牌签名），letter-spacing -0.01em
- 代码/数字: **"Source Code Pro", "JetBrains Mono", ui-monospace, monospace**，等宽数字对齐
- 技术标签可用等宽体 + 全大写 + 0.1em 字距（如 `API REQUESTS`），营造"开发者控制台"标记感

## Border Radius
- 卡片: **16px**；按钮/标签/状态点: **9999px 全圆角 pill**；输入框/小面板: 8px
- pill 与大圆角卡片的对比是本主题的形状签名

## Shadows
- 卡片**不用阴影**，靠 `--border-subtle` 边框与背景差分层
- 仅 Tooltip/Popover: `0 4px 12px rgba(0,0,0,0.4)`

## Chart Fingerprint
- 折线：线宽 2px，不显示数据点（symbol: none），hover 才显示 6px 圆点；面积渐变允许但仅限主绿色系列：从 `rgba(62,207,142,0.18)` 渐变到完全透明，其余系列一律纯色无面积
- 末端标注：折线/面积图用 endLabel 替代图例——系列名 11px 等宽体标在线末端，颜色同系列色，全图不放图例
- 参考线：markLine 均值虚线用 `--text-muted` 灰色虚线（label 等宽体 11px），目标值用 `--accent-primary` 实线；标注文字右对齐贴线尾
- 柱形：仅上圆角 `[6,6,0,0]`，纯色填充（禁止柱内渐变）；主系列用 `--accent-primary`，其余系列用灰阶或其他系列色；hover 时该柱亮度提升约 15%，不缩放不投影
- 饼/环图：只用环图，radius `['58%','78%']`，环段间 2px `#121212` 间隔；标签放环外细引导线或直接省略、用图例代替；中心可放等宽体总数；**禁止发光、禁止阴影**
- 网格线：仅保留横向，1px **实线**，颜色 `--border-subtle`（`#2e2e2e`），纵向网格线一律关闭；坐标轴线也去掉，只留刻度文字。**排他签名：全库深色组唯一用实线网格的主题（别家深色一律虚线）——编辑器标尺是实线**
- Tooltip：背景 `--bg-elevated`（`#242424`），1px `--border-subtle` 边框，8px 圆角，阴影 `0 4px 12px rgba(0,0,0,0.4)`；数值用等宽体，系列名用 `--text-secondary`
- 图例与数据标签：折线/面积图一律用 endLabel 末端标注（见上），不放图例；饼/环图等无末端可标的图保留 12px、`--text-secondary` 圆点图例；数据标签默认关闭，需要时 11px 等宽体 `--text-muted`
- 允许：单系列绿色的低透明面积渐变、pill 图例、等宽数字、hover 亮点
- 禁止：任何发光/外发光、多色渐变、3D、粗网格、每个系列都填面积

## Token Schema
| Token | 值 | 说明 |
|--------|----|------|
| `--radius-card` | `16px` | 卡片圆角（大圆角是签名） |
| `--radius-button` | `9999px` | 按钮/标签全圆角 pill |
| `--radius-panel` | `8px` | 输入框/小面板 |
| `--font-family-base` | `"Inter", -apple-system, "Segoe UI", sans-serif` | 正文/UI |
| `--font-family-display` | `"Nunito Sans", "Inter", -apple-system, sans-serif` | 标题/大数字 |
| `--font-family-mono` | `"Source Code Pro", "JetBrains Mono", ui-monospace, monospace` | 代码/指标数字 |
| `--font-size-display` | `28px` | 页头标题（字重 500，非粗体） |
| `--font-size-title` | `15px` | 卡片标题（500） |
| `--font-size-kpi` | `36px` | KPI 大数字（等宽体，400） |
| `--shadow-card` | `none` | 卡片无阴影，靠边框分层 |
| `--glow-accent` | `none` | 无发光 |
| `--decoration` | `flat` | 纯平：无渐变面板、无发光、无高光线 |
| `--bg-pattern` | `dots` | 页面层点阵纹理（16px 密点间距），编辑器 minimap 式的技术感；与 figma 20px 密点、spotify 32px 疏点参数化区分 |
| `--pattern-color` | `rgba(255,255,255,0.04)` | 深色主题点阵色，近乎不可察觉 |
| `--kpi-variant` | `topbar` | KPI 卡顶部 3px `--accent-primary` 强调条 |

## Component Specifications

### KPI 卡片
- 背景 `--bg-card`，1px `--border-subtle` 边框，16px 圆角，内边距 20px 24px，无阴影
- **topbar 形态**：卡片顶部一条 3px `--accent-primary` 圆角条（贴卡顶，左右各留 1px，两端 3px 圆角——顶条派中唯一圆角顶条，terminal-amber 顶条为直角，形状互斥），是 KPI 区唯一允许的绿色横条；除此之外卡内不再出现绿色装饰
- **大数字**: 36px 400 等宽体（Source Code Pro），`--text-primary`，**左对齐**
- **标签**: 12px 等宽体全大写 + 0.1em 字距，`--text-muted`，置于大数字**上方**（控制台标记风格）
- **趋势**: 小 pill 徽章（9999px 圆角），正增长绿字深绿底 `rgba(62,207,142,0.12)`，负增长红字深红底
- 悬停：边框变为 `#3d3d3d`，无位移无阴影

### 图表容器
- 与 KPI 卡同表面：`--bg-card` + 1px 边框 + 16px 圆角，内边距 20px
- **标题**: 15px 500，`--text-primary`，左对齐；右侧可放等宽体全大写小标签（如 `LAST 24H`）
- 图表区遵循 Chart Fingerprint；卡片内不再叠加任何装饰线条

### 按钮
- **主按钮**: pill 全圆角，`--accent-primary` 填充 + `#06281b` 深色文字，14px 500，内边距 8px 20px；hover 底色加深为 `#34bd7f`，边框出现 `#1f4b37`
- **次按钮**: pill 全圆角，透明底 + 1px `#393939` 边框，`--text-primary`；hover 背景 `rgba(255,255,255,0.04)`
- 绿色填充按钮是全场唯一的大面积彩色，一屏最多一个

### 数据表格
- 表头：等宽体全大写 11px + 0.1em 字距，`--text-muted`，底部 1px `--border-subtle`
- 数据行：行高 44px，行间 1px `--border-subtle` 分隔线，**不用交替底色**
- 悬停行：背景 `--bg-hover`，无左边框
- 数字列等宽体右对齐；状态列用 pill 徽章（绿/灰/红）

### 页头
- 背景 `--bg-primary`，高度 60px，底部 1px `--border-subtle`
- 标题 28px 500（非粗体）`--text-primary` 左对齐，关键词可用 `--accent-primary` 高亮一两个词
- 右侧：等宽体 12px 时间戳 `--text-muted` + 状态点（8px 圆点，绿=正常）

### 进度条
- 高度 6px，9999px 全圆角；轨道 `#2e2e2e`，填充 `--accent-primary` 纯色
- 标注：等宽体百分比 12px，`--text-muted`，右对齐

## Chart Color Palette
- 系列色: #3ecf8e, #bda4ff, #f59e0b, #60a5fa, #f43f5e
- 语义约定：系列 2 `#bda4ff` 代码紫固定作对照/代码语义系列（如基准线、对照组），不作主数据色

## Anti-Patterns
- ❌ 禁止任何发光/外发光/霓虹效果——本主题无 glow
- ❌ 禁止标题用 700 及以上粗体（500 封顶）
- ❌ 禁止给卡片加投影——层级只靠边框对比
- ❌ 禁止大面积铺绿色（绿底卡片、绿渐变面板）——绿色只作点状强调
- ❌ 禁止柱状图/按钮用直角或小圆角混用——按钮一律 pill，柱只圆上部

## Motion
- 签名动效：**KPI 大数字 600ms ease-out 等宽体逐位滚动**——像终端打印输出，逐位对齐不跳动，是全场唯一"会动"的元素
- 入场编排：**无 stagger，整屏同现**——控制台是即时全量渲染的，所有卡片同时出现，不做逐项延迟
- 悬停与展开只改边框/底色明度，不动位置不加阴影；绿色不参与任何交互反馈（配给制的延伸）
- 禁止弹性回弹、弹跳类缓动

## Layout & Grid

| 属性 | 值 |
|------|-----|
| 页面最大宽度 | 1920px |
| 网格系统 | CSS Grid, 12 列 |
| 卡片间距 | 16px |
| 页面内边距 | 24px |
| 图表容器最小高度 | 280px |
| 对齐方式 | 全部左对齐，控制台式信息密度 |
| 密度基调 | 标准偏密（控制台密度） |

## Do's and Don'ts
✅ 绿色配给制：一个视觉区域内只让一个元素是绿色
✅ 用等宽体全大写小标签做"控制台标记"（如 `TOTAL ROWS`）
✅ 按钮、徽章、进度条全部 pill 圆角，卡片 16px，形成形状二元对比
✅ 用 1px `#2e2e2e` 边框做全部分层与分隔
❌ 不要用纯黑 `#000000` 背景（用 `#121212` 炭灰）
❌ 不要把标签放在大数字下方（本主题标签在上方）
❌ 不要给次按钮也填绿色
❌ 不要居中排版——全部左对齐
