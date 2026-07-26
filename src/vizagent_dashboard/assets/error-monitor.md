# Error Monitor — 错误监控暗色风

## Visual Theme
"凌晨三点调试代码"的氛围：暖紫黑底色（绝不用纯黑）、毛玻璃面板、带按压感的按钮，石灰绿只留给 CTA 和正向信号。整体是一个会呼吸的错误监控台，不是冷冰冰的仪表盘——暖紫替代冷灰，圆润替代锐利，发光一概不要。

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-primary` | `#1f1633` | 主背景（暖紫黑） |
| `--bg-deeper` | `#150f23` | 更深区域（页头/页脚） |
| `--bg-card` | `rgba(31,22,51,0.65)` | 卡片/面板（须配 backdrop-blur） |
| `--bg-elevated` | `#2b2145` | 抬升面：表头、悬停态、输入框 |
| `--bg-hover` | `rgba(120,98,140,0.18)` | 行/面板悬停（微增亮，不变色） |
| `--border-subtle` | `#362d59` | 边框/分割线 |
| `--accent-primary` | `#6a5fc1` | 主交互色（紫） |
| `--accent-cta` | `#c2ef4e` | 高亮 CTA / 正向趋势（石灰绿，小面积） |
| `--accent-secondary` | `#fa7faa` | 次强调（粉，聚焦态） |
| `--accent-warm` | `#ffb287` | 暖强调（珊瑚） |
| `--accent-success` | `#33bf7f` | 成功 |
| `--accent-warning` | `#ffb020` | 警告 |
| `--accent-danger` | `#f55459` | 错误/危险（Sentry 火色系） |
| `--text-primary` | `#ffffff` | 主文字 |
| `--text-secondary` | `#d6d0e8` | 次要文字（带紫调） |
| `--map-area` | `#2b2145` | 地图无数据区域底色 |
| `--map-boundary` | `#d6d0e8` | 地图国家/省级边界 |
| `--text-muted` | `#8a85a0` | 弱化文字 |

## Chart Color Palette
- 系列色: #6a5fc1, #c2ef4e, #fa7faa, #ffb287, #7fd4ff
- 石灰绿 #c2ef4e 只用于"最重要的那一个系列"或正向指标，不可默认占第一顺位

## Chart Fingerprint
- 折线：线宽 2px，圆角拐点；不显示常设数据点，hover 时才出现 6px 圆点+空心描边；面积渐变只给主系列（系列色 0.18 → 0 纵向渐变），其余系列一律纯色描边；hover 显示竖直 crosshair（1px 虚线 #8a85a0）
- 末端标注：折线末端用 endLabel 直接写系列名（12px Rubik，系列色），替代顶部图例；系列 ≥4 个时才回退顶部圆点图例
- markLine：均值用虚线（--text-muted），SLO/错误预算目标用实线（--accent-warning），标签 Monaco 11px 放线端内侧
- markArea（排他签名）：标注事故/部署窗口区间，填充 rgba(245,84,89,0.08) 红底——全库唯一的事故红区间标注（pitchbook 用金底、grafana 用橙底），是监控屏"哪里着火"的视觉锚点；无边框，标签 11px --text-muted
- 阈值染色：超过错误预算阈值的柱/点用 --accent-danger，其余保持系列色——监控屏的"哪里着火"必须一眼可见
- 柱形：仅上圆角 [4,4,0,0]，纯色填充（禁止柱体渐变）；同组柱间距 30%；hover 时该柱亮度 +15%，其余柱降至 50% 透明度
- 饼/环图：一律环形 radius ["48%","72%"]，中心用 Monaco 显示总数；标签放环外，引导线 12px，12px Rubik；禁止发光、禁止立体/玫瑰图
- 网格线：仅横向，虚线 [4,4]，颜色 --border-subtle；纵向网格线一律删除
- Tooltip：毛玻璃深色 `rgba(21,15,35,0.92)` + backdrop-blur(12px)，1px solid #362d59 边框，8px 圆角，无发光阴影（仅柔和投影）；系列色用小圆点标示
- 图例：默认由 endLabel 末端标注替代；仅系列 ≥4 时启用，12px Rubik，圆点 marker，置顶靠右；坐标轴标签 11px --text-muted；数据标签默认关闭，仅 KPI 环图中心常显
- 允许：极淡面积渐变、毛玻璃 tooltip、hover 高亮当前系列
- 禁止：一切发光/shadowBlur/text-shadow、柱体渐变、3D、纵向网格线、常设数据点（与 Anti-Patterns 一致）

## Token Schema

| Token | 值 | 说明 |
|--------|----|------|
| `--radius-card` | `12px` | 卡片/毛玻璃面板圆角 |
| `--radius-button` | `8px` | 按钮圆角 |
| `--radius-panel` | `12px` | 图表容器圆角 |
| `--font-family-base` | `"Rubik", -apple-system, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif` | 全站 UI 字体 |
| `--font-family-display` | `"Rubik", -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif` | 大标题（Rubik 700；原品牌字 Dammit Sans 不在 Google Fonts，已移除） |
| `--font-family-mono` | `Monaco, "JetBrains Mono", Menlo, Consolas, monospace` | 一切数字/时间/代码 |
| `--font-size-display` | `26px` | 页头主标题 |
| `--font-size-title` | `13px` | 面板标题（uppercase + letter-spacing 0.08em） |
| `--font-size-kpi` | `40px` | KPI 大数字（Monaco + tabular-nums） |
| `--shadow-card` | `0 10px 30px rgba(0,0,0,0.35)` | 毛玻璃面板柔和投影 |
| `--glow-accent` | `none` | 本主题无任何发光 |
| `--decoration` | `glass` | 半透明面板 + backdrop-blur(18px) saturate(180%)，无渐变面板、无发光 |
| `--bg-pattern` | `grid` | 页面层网格纹理，40px 间距（linear 24px/palantir 32px/grafana 48px），呼应 IDE 编辑器网格的调试氛围 |
| `--pattern-color` | `rgba(255,255,255,0.04)` | 深色主题白纹，仅隐约可见、不抢毛玻璃面板 |
| `--kpi-variant` | `stat` | KPI 整卡染 10% --accent-success 状态色（Grafana Stat 风），监控语义直给；sentry 是 10% 淡染+毛玻璃，grafana 是实色满铺+缝隙分隔——两者互斥，不可折中 |

## Typography

| Role | Font | Size | Weight |
|------|------|------|--------|
| 页头标题 | Display 栈 | 26px | 700 |
| 面板标题 | Rubik, uppercase, letter-spacing 0.08em | 13px | 600 |
| KPI 大数字 | Monaco 栈, tabular-nums | 40px | 600 |
| KPI 标签 | Rubik | 13px | 500 |
| 正文/表格 | Rubik | 13-14px | 400 |
| 时间/坐标轴/代码 | Monaco 栈 | 11-12px | 400 |

## Border Radius
- 按钮/输入框: **8px**
- 卡片/面板/Tooltip: **12px**
- badge/图例点: **999px** (pill)
- 禁止直角，最小 8px

## Shadows
- 面板: `0 10px 30px rgba(0,0,0,0.35)`（柔和投影，靠 blur 而非偏移堆叠）
- 按钮按压感: `inset 0 -2px 0 rgba(0,0,0,0.25)`（主按钮必备，Sentry 签名细节）
- 悬停浮起: `0 16px 40px rgba(0,0,0,0.45)`
- 一律禁止带颜色的发光阴影

## Motion
- 签名动效：按钮按压反馈——active 时内阴影从 `inset 0 -2px 0` 反转为 `inset 0 2px 0`，模拟实体按键下沉（全库唯一触感签名）；tooltip/浮层不继承按压感
- 入场编排：面板按阅读顺序 60ms stagger 淡入，毛玻璃同步从 blur(0) 聚焦到 blur(18px)——"玻璃聚焦入场"是全库唯一的入场范式
- 数字滚动: **600ms ease-out**
- 图表入场不做花哨动画，直接渲染；禁止循环呼吸/闪烁动画

## Layout & Grid

| 属性 | 值 |
|------|-----|
| 页面最大宽度 | 1920px |
| 网格 | CSS Grid 12 列 |
| 卡片间距 | 16px |
| 页面内边距 | 24px |
| 页头 | 56px 高，底色 --bg-deeper，底边 1px --border-subtle |
| KPI 对齐 | 全部左对齐（标签在上，数字在下） |
| 信息密度 | 标准 |
| 图表容器最小高度 | 280px |

## Component Specifications

### KPI 卡片
- 形态: stat 变体（--kpi-variant）——整卡底色为 10% --accent-success 混入 --bg-card 的柔和状态色，无边框无 sparkline，仍保留毛玻璃质感
- 背景: var(--bg-card) + backdrop-blur(18px) saturate(180%)，1px solid var(--border-subtle)，圆角 12px，内边距 18px 20px
- 标签 13px Rubik 500 --text-secondary 居上；大数字 40px Monaco 600 --text-primary 居下，一律左对齐（不居中）
- 趋势：▲▼ 小三角 + 百分比，正向用 --accent-cta、负向用 --accent-danger，Monaco 12px，放数字右侧基线对齐
- 悬停：背景切 var(--bg-hover)，边框不变，100ms

### 图表容器
- 与 KPI 卡同款毛玻璃，圆角 12px，内边距 20px
- 标题 13px uppercase letter-spacing 0.08em Rubik 600，左对齐，不加竖条/图标等任何装饰，距图表 14px
- 图表区按 Chart Fingerprint 执行

### 按钮
- 主按钮: --accent-cta 底 + #1f1633 文字 + `inset 0 -2px 0 rgba(0,0,0,0.25)` 按压感，圆角 8px，13px 600
- 次按钮: #79628c 底 + 白字 + 同款内阴影（Sentry 经典 muted purple 按钮）
- 悬停亮度 +8%，active 内阴影反转为 `inset 0 2px 0`

### 数据表格
- 表头: --bg-elevated，11px uppercase letter-spacing 0.06em --text-muted，无下边框加粗
- 行高 44px，无斑马纹（靠 1px --border-subtle 行线分隔）
- 悬停行: 整行背景 var(--bg-hover)，无左边框变色
- 数字列 Monaco 右对齐，文字列 Rubik 左对齐；错误数等关键列可用 --accent-danger 着色

### 页头
- 背景 --bg-deeper（比主背景深一层），高 56px，底边 1px --border-subtle
- 标题 26px Display 栈 700 左对齐；右侧 Monaco 12px --text-muted 实时时间
- 可放一个石灰绿主按钮作为唯一亮色出口

### 进度条
- 高 6px，圆角 3px；轨道 rgba(255,255,255,0.08)
- 填充 --accent-primary 纯色；达到 100% 或"健康"语义时切 --accent-cta
- 标注: Monaco 11px --text-muted，右侧百分比

## Anti-Patterns
- ❌ 纯黑 #000000 或冷灰 #111/#1a1a1a 系背景——底色必须带紫调
- ❌ 一切发光：text-shadow、shadowBlur、drop-shadow 光晕、霓虹描边
- ❌ 直角（最小圆角 8px）和超过 12px 的大圆角并存——圆角只有 8/12/pill 三档
- ❌ 蓝色系强调色（#3b82f6 等）——Sentry 的交互色是紫，蓝不属于这里；linear 的 #5e6ad2、鸢尾紫 #5741d9 等紫蓝色同样不属于本主题
- ❌ 石灰绿大面积填充或当默认系列色——它是稀缺的 CTA/正向信号
- ❌ 渐变文字、渐变柱体、3D 图表

## Do's and Don'ts
✅ 每个面板都是毛玻璃：半透明底 + backdrop-blur(18px) saturate(180%)，缺一就露馅
✅ 面板标题用 uppercase 小字 label 风格，零装饰
✅ 一切数字、时间、百分比用 Monaco + tabular-nums
✅ 主按钮必带 inset 按压阴影，这是 Sentry 的触感签名
✅ hover 只做"微增亮"，不换色、不发光
❌ 不要把石灰绿撒得到处都是——全屏 ≤2 处（一处 CTA + 一处正向趋势）
❌ 不要实心深紫大色块铺满卡片，层次靠半透明叠出来
❌ 不要给标题加 emoji/图标/竖线装饰，Sentry 靠字重和字距说话
