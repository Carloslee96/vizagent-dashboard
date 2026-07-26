# Clean Slate — 简洁亮色科技风

## Visual Theme
"暴力美学"留白 + 标志性毛玻璃(vibrancy)。SF Pro 字体、Apple Blue 唯一主彩色、药丸形按钮。深色不是灰——纯黑底上叠半透明白，层次靠模糊而非边框。去除一切非必要，让内容呼吸。分层五式中本主题独占"模糊"一式（毛玻璃），不混用边框/辉光/缝隙分层。与 vercel 同为纯黑底双雄：本主题 = noise 噪点 + 毛玻璃，vercel = 零纹理 + 细边框，两者互斥、禁止杂交。

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-primary` | `#000000` | 主背景（纯黑，Apple 深色系正统） |
| `--bg-card` | `#1c1c1e` | 卡片（iOS 深色二级背景） |
| `--bg-elevated` | `#2c2c2e` | 悬浮层 |
| `--bg-hover` | `#3a3a3c` | 悬停态 |
| `--bg-glass` | `rgba(28,28,30,0.72)` | 毛玻璃面板（配 backdrop-blur） |
| `--border-subtle` | `#38383a` | 分隔线（极细，克制使用） |
| `--accent-primary` | `#0071e3` | Apple Blue — 唯一主彩色 |
| `--accent-secondary` | `#5ac8fa` | 浅蓝辅助 |
| `--accent-success` | `#30d158` | 成功（iOS 深色绿） |
| `--accent-warning` | `#ff9f0a` | 警告（iOS 深色橙） |
| `--accent-danger` | `#ff453a` | 危险（iOS 深色红） |
| `--text-primary` | `#f5f5f7` | 主文字 |
| `--text-secondary` | `#86868b` | 次要文字 |
| `--map-area` | `#2c2c2e` | 地图无数据区域底色 |
| `--map-boundary` | `#86868b` | 地图国家/省级边界 |
| `--text-muted` | `#6e6e73` | 弱化文字 |

## Chart Fingerprint
ECharts option 严格按此生成：
- **排他签名**：tooltip 是全库唯一的"毛玻璃深色 + 无任何彩色边框"浮层——sentry 也是毛玻璃 tooltip 但带 1px 紫边框，本主题一律无边框；环图半径固定 `['58%','78%']`（20% 环厚），配 2px 扇区间隙的参数组合全库独此一家
- **折线**：线宽 2.5px，`smooth:true` 平滑曲线；`symbol:'none'` 常隐数据点，hover 时才浮现 8px 白心圆点；面积渐变允许但极克制——仅主系列用 accent-primary 自上而下 opacity 0.18→0，其余系列纯线；hover 不改变线宽，只显示数据点
- **末端标注**：折线一律用 `endLabel` 在系列末端直接标注系列名（12px，跟随系列色），**替代图例**——画布更干净，视线不用来回跳
- **markLine**：折线/柱形图加均值参考线——细虚线 1px `--text-muted`，标签 11px 置线端；目标线用同色实线；不启用 markArea 与阈值染色——Apple 保持画面干净
- **柱形**：独立柱全圆角 `[6,6,6,6]`，堆叠柱仅首尾圆角；纯色填充，禁止柱体渐变；hover 亮度提升 15%（不改变色相）
- **饼/环图**：一律细环 `radius:['58%','78%']`，扇区 `borderRadius:6` + 2px 间隙（borderColor 同 --bg-card）；外圈标签与引线全部关闭，中心显示总计大数字；禁止扇区发光
- **网格线**：仅保留横向虚线 1px，色用 `--border-subtle`；纵向网格线一律删除；坐标轴线隐藏
- **Tooltip**：毛玻璃——背景 `rgba(28,28,30,0.85)` + `backdrop-blur(20px)`，圆角 12px，无彩色边框，阴影 `0 8px 24px rgba(0,0,0,0.4)`
- **图例**：仅多系列非折线图保留（12px `--text-secondary`，图标圆形）；折线图无图例，用末端标注；数据标签默认关闭，仅环图中心与柱顶关键值可显示（12px `--text-primary`）
- **坐标轴刻度文字**：11px `--text-muted`
- **允许**：毛玻璃 tooltip、极轻单色面积渐变（仅主系列）、全圆角柱、细环图、endLabel 末端标注、markLine 均值/目标参考线
- **禁止**：一切发光/霓虹、3D、柱体渐变、饼图外圈标签引线、纵向网格线、markArea 区间染色

## Chart Color Palette
- 系列色: #0071e3, #5ac8fa, #30d158, #ff9f0a, #bf5af2

## Typography
- 全局: **SF Pro**（Web 端栈首 Google 字体为 Inter 兜底，见 Token Schema）
- 大数字: SF Pro Display, 48-64px, 600, letter-spacing -0.02em, tabular-nums
- 页面标题: 28px, 600；面板标题: 17px, 600
- 正文: 15-17px, 400 — Apple 基准字号
- 标签/辅助: 12-13px, 400-500, `--text-secondary`
- 字号对比要"暴力"：56px 大数字 vs 13px 标签，中间不要堆砌过渡字号
- 层级倒挂是刻意的：KPI 56px > 页头标题 28px——大数字是主角，页头只是导航，禁止把页头字号抬到 KPI 之上

## Border Radius
- 卡片/面板: **18px**
- 按钮/进度条/Tab: **980px**（pill 药丸形）
- Tooltip/小浮层: 12px
- 任何元素圆角不得小于 10px，禁止直角

## Shadows
层级靠模糊与亮度差，不靠阴影。卡片无阴影；毛玻璃浮层仅 `0 8px 32px rgba(0,0,0,0.4)`；发光阴影一律禁止。

## Motion
- 签名动效: **进度环入场弧长生长 800ms ease-in-out**——ring 变体的品牌时刻；缓动参数与 health-ring 的 ease-out 环生长互斥，不得混用
- 入场编排: 卡片自上而下 60ms stagger 淡入并上浮 4px，像 iOS 主屏小组件依次就位；图表随容器同现，不做系列级编排
- 悬停: 微亮 或 scale(1.02) 二选一（时长走机制默认，不另声明）
- 展开/收起: **350ms ease-in-out**
- 数字动画: **800ms ease-out**
- 禁止弹跳、回弹等夸张缓动——动效要"感觉不到存在"

## Token Schema
| Token | 值 | 说明 |
|--------|----|------|
| `--radius-card` | `18px` | 卡片圆角 |
| `--radius-button` | `980px` | 按钮圆角（pill） |
| `--radius-panel` | `18px` | 面板圆角 |
| `--font-family-base` | `-apple-system,'Inter','SF Pro Text','Helvetica Neue',Arial,sans-serif` | 正文字体栈（Inter 为 Google Fonts 兜底） |
| `--font-family-display` | `-apple-system,'Inter','SF Pro Display','Helvetica Neue',sans-serif` | 标题/大数字字体栈 |
| `--font-family-mono` | `ui-monospace,'JetBrains Mono','SF Mono',Menlo,monospace` | 时间/编号等宽字体（JetBrains Mono 兜底） |
| `--font-size-display` | `28px` | 页面大标题 |
| `--font-size-title` | `17px` | 面板标题 |
| `--font-size-kpi` | `56px` | KPI 大数字 |
| `--shadow-card` | `none` | 卡片无阴影——层级靠毛玻璃模糊与亮度差 |
| `--glow-accent` | `none` | 无发光——Apple 不用霓虹 |
| `--decoration` | `glass` | 半透明 + backdrop-blur，无高光线无发光 |
| `--bg-pattern` | `noise` | 极轻噪点纹理，给纯黑底一点"胶片颗粒"，打破死寂；与 vercel 的零纹理纯黑互斥 |
| `--pattern-color` | `rgba(255,255,255,0.04)` | 深色主题纹理色，纯黑底上恰好可感（0.03 在多数显示器不可见） |
| `--kpi-variant` | `ring` | 进度环——致敬 Apple Watch 健身三环，品牌签名形态；本主题环一律单色蓝（`--accent-primary`），禁止多环/多色环——那是 health-ring 的语言 |

## Component Specifications

### KPI 卡片
- 背景: `--bg-glass` + `backdrop-blur(20px) saturate(180%)`，无边框、无顶部高光线
- 圆角 18px，内边距 28px，内容整体**垂直水平居中**
- **标签在上**：13px `--text-secondary`，eyebrow 式小标签
- **大数字**：56px 600 SF Pro Display, `--text-primary`, letter-spacing -0.02em
- **趋势**：数字下方 8px，pill 徽章（彩色文字 + 同色 12% 透明度底，如 `#30d158` 字配 `rgba(48,209,88,0.12)` 底）
- **进度环形态**（`--kpi-variant:ring`）：数字右侧放进度环，轨道 `--bg-elevated` 4px 宽、填充 `--accent-primary` 单色圆头，环心或数字旁标注百分比；单卡单环，禁止多环堆叠
- 悬停: 背景提亮到 `--bg-elevated`，进度环亮度 +10%（ring 变体在本主题的专属反馈），无位移无边框变化

### 图表容器
- 背景: `--bg-glass` + backdrop-blur，无边框，圆角 18px，内边距 24px
- **标题**: 17px 600 `--text-primary` 左对齐，距图表 16px；不加左侧色条、不加图标
- **图表区**: ECharts，按 Chart Fingerprint 执行
- 容器之间靠 20px+ 间距分隔，不靠边框

### 按钮
- **主按钮**: `#0071e3` 填充 + 白字，pill 圆角，内边距 10px 22px，14px 500
- **次按钮**: 透明背景 + 1px `#0071e3` 边框 + `#0071e3` 文字
- **悬停**: 主按钮微亮至 `#0077ed`；次按钮背景浮现 `rgba(0,113,227,0.1)`
- **禁用**: 40% 透明度，不改变颜色

### 数据表格
- 表头无底色：12px `--text-muted`，仅下方 1px `--border-subtle` 分隔线
- 数据行: 行高 44px，行间 0.5px 细线，无交替底色、无竖线
- 悬停行: 背景 `--bg-hover`，无左侧色条
- 数字列: tabular-nums 右对齐；文字列左对齐

### 页头
- 背景透明或 `--bg-glass` + backdrop-blur(20px)，高度 64px
- 标题 28px 600 左对齐；右侧时间用 SF Mono 13px `--text-muted`
- 页头与内容之间不加分割线，靠留白分隔

### 进度条
- 高度 4px，全圆角（两端圆头），轨道 `--bg-elevated`
- 填充 `#0071e3` 纯色，无渐变无流光
- 标注: 百分比 12px `--text-muted`，置于右侧

## Anti-Patterns
- ❌ 任何发光效果：text-shadow、彩色 box-shadow、drop-shadow 滤镜
- ❌ 直角或小于 10px 的圆角
- ❌ 渐变文字、金属/拟物质感、3D 效果
- ❌ 粗边框与深色分割线——分隔靠留白和 0.5px 细线
- ❌ 同屏超过 3 种彩色（蓝 + 绿/橙语义色为上限）
- ❌ 卡片内边距小于 24px 的拥挤布局——毛玻璃面板一挤就廉价
- ❌ 科技风装饰：面板左侧色条、顶部高光线、扫描线、网格背景
- ❌ 多色/多环进度环（health-ring 的身份色多环不属于本主题）、零纹理纯黑配边框分层（那是 vercel）

## Do's and Don'ts
✅ 单屏只让 Apple Blue 唱主角，其余彩色仅用于成功/警告语义
✅ 毛玻璃面板统一 `backdrop-blur(20px) saturate(180%)`
✅ 数字用 tabular-nums，KPI 字号对比拉到 56px vs 13px
✅ 按钮、Tab、进度条一律 pill 药丸形
✅ 悬停只做两件事：微亮 或 scale(1.02)
❌ 不要给面板加彩色左边条/顶部高光线——那是科技风，不是 Apple
❌ 不要用深灰背景代替纯黑——Apple 深色 = 纯黑 + 半透明白
❌ 不要给图表容器加外边框

## Layout & Grid

| 属性 | 值 |
|------|-----|
| 页面最大宽度 | 1920px |
| 网格系统 | CSS Grid，宽松分栏，留白优先 |
| 卡片间距 | 20px |
| 页面内边距 | 32px |
| 密度基调 | 极宽松——"KPI 居中（全库唯二，另一家 health-ring）+ 纯黑 + 毛玻璃"三件套缺一不可 |
| KPI 卡片对齐 | 内容居中对齐 |
| 图表容器最小高度 | 300px |
| 对齐方式 | 标题左对齐 + KPI 居中，大量负空间 |
