# Growth Analytics — 产品数据分析风

## Visual Theme
PostHog 产品 OS 气质：暖米纸底 + 白色卡片 + 海军蓝墨色文字，刺猬橙 (#F54E00) 只做点睛。平涂、清晰描边、零发光零渐变，数据密集但读着轻松，像打印精良的分析报告。

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-primary` | `#F2EFE9` | 主背景（暖米纸） |
| `--bg-card` | `#FFFFFF` | 卡片/面板 |
| `--bg-elevated` | `#FAF9F5` | 表头/悬浮层 |
| `--bg-hover` | `#F0EDE5` | 悬停背景 |
| `--border-subtle` | `#E5E1D8` | 边框/分割线 |
| `--accent-primary` | `#F54E00` | 刺猬橙，主交互/第一系列 |
| `--accent-secondary` | `#1D4AFF` | 品牌蓝，次强调/链接 |
| `--success` | `#36BF6B` | 上涨/成功 |
| `--warning` | `#F9BD2B` | 品牌黄，警示 |
| `--danger` | `#E83A5F` | 下降/错误 |
| `--text-primary` | `#1D1F27` | 海军蓝墨，主文字 |
| `--text-secondary` | `#5E6372` | 次要文字 |
| `--map-area` | `#FAF9F5` | 地图无数据区域底色 |
| `--map-boundary` | `#5E6372` | 地图国家/省级边界 |
| `--text-muted` | `#9CA0AB` | 弱化文字 |

## Chart Color Palette
- 系列色: #F54E00, #1D4AFF, #F9BD2B, #36BF6B, #856CFF

## Chart Fingerprint
ECharts option 逐项严格按此执行：

- **折线**: lineStyle.width=2.5 纯色；symbol='circle'、symbolSize=5 **常显**（hover 放大到 7）；**禁止 areaStyle**——趋势图就是干净的线；emphasis 仅线宽加粗到 3.5，不加阴影。
- **排他签名**: **全库唯一"hover 加粗线宽"的指纹**——emphasis 只把线宽 2.5→3.5，不加阴影不换色（apple 等主题明确禁止改变线宽）；本主题同时是浅色组唯一 symbol 常显（5px 圆点）的主题，与 palantir 深色圆点、figma 深色方块构成三家常显对位。
- **柱形**: itemStyle.borderRadius=[4,4,0,0] 仅上圆角；**纯色填充，禁止渐变**；barCategoryGap='35%'；emphasis 颜色加深 10%（同色系变暗），禁止发光。
- **饼/环图**: radius=['48%','70%']；标签放外侧，引导线细 1px，11px `--text-secondary`；**禁止发光与渐变**；中心可放总数大数字（mono 字体）。
- **网格线**: 仅水平虚线（dashType='dashed'，1px，`#E5E1D8`），无垂直网格线；坐标轴文字 11px `--text-muted`。
- **Tooltip**: 白底 `#FFFFFF`、1px solid `#E5E1D8`、阴影 `0 4px 12px rgba(29,31,39,0.10)`、文字 `--text-primary`——白色卡片感，不用深色 tooltip。
- **图例/数据标签**: 图例 12px、顶部左对齐、方形色块 8×8；数据标签 11px `--text-secondary`，柱顶/环外侧，不堆砌。
- **末端标注**: 折线系列不超过 3 条时，用 endLabel 在末端直接标注系列名+最新值（11px、跟随系列色、加白底描边防重叠），替代顶部图例；多系列才回退图例。
- **markLine**: 均值线= 1px 虚线 `--text-muted`，尾端标签"均值"11px；有目标值时加 1px 实线 `--accent-secondary`，标签"目标"；禁止彩色粗线。
- **markArea**: 活动期/灰度发布期等区间用 `rgba(29,31,39,0.04)` 浅灰底 + 12px `--text-muted` 顶部标注，不抢主数据。
- **允许**: 纯色系列、白色 tooltip、小圆角、幽默克制的留白。
- **禁止**: 一切渐变、一切发光/阴影堆叠、深色面板、彩虹色乱搭（系列色按序用）。

## Token Schema

| Token | 值 | 说明 |
|-------|-----|------|
| `--radius-card` | `6px` | 卡片圆角（小而利落） |
| `--radius-button` | `4px` | 按钮圆角 |
| `--radius-panel` | `6px` | 面板圆角 |
| `--font-family-base` | `'Inter',-apple-system,'Segoe UI',sans-serif` | 正文（Matter 不在 Google Fonts，用 Inter 近似） |
| `--font-family-display` | `'Inter',-apple-system,sans-serif` | 标题/大数字展示 |
| `--font-family-mono` | `'IBM Plex Mono','SFMono-Regular',Menlo,Consolas,monospace` | 数字/代码 |
| `--font-size-display` | `44px` | 页头大标题 |
| `--font-size-title` | `16px` | 面板标题 |
| `--font-size-kpi` | `40px` | KPI 大数字 |
| `--shadow-card` | `0 1px 2px rgba(29,31,39,0.06)` | 极轻投影，主要靠描边分层 |
| `--glow-accent` | `none` | 本主题无发光 |
| `--decoration` | `flat` | 纯平：无渐变无发光无玻璃 |
| `--bg-pattern` | `hatch` | 页面层 45° 斜线纹理，呼应"打印报告"纸感——**全库唯一斜纹，本主题独占** |
| `--pattern-color` | `rgba(29,31,39,0.05)` | 取海军蓝墨色的 5% 透明，与文字同族 |
| `--kpi-variant` | `delta-pill` | KPI 大数字右侧涨跌胶囊（与既有趋势 pill 一致） |

## Typography

| Role | Font | Size | Weight |
|------|------|------|--------|
| 页头标题 | Inter | 28-44px | 700 |
| 面板标题 | Inter | 16px | 600 |
| KPI 大数字 | IBM Plex Mono（tabular-nums） | 36-40px | 600 |
| 正文/标签 | Inter | 13-14px | 400-500 |
| 辅助说明 | Inter | 12px | 400 |

## Border Radius
- 按钮/输入框: **4px**
- 卡片/面板: **6px**
- badge/趋势胶囊: **10px**（小 pill 仅用于趋势标记，不用在容器上）

## Shadows
- 卡片: `0 1px 2px rgba(29,31,39,0.06)`（分层主要靠 1px 描边，不靠阴影）
- 悬停/tooltip: `0 4px 12px rgba(29,31,39,0.10)`
- 禁止彩色投影与内发光

## Motion
- 动效人格: 工具型"跟手"——轻快、有"咔哒"感；hover 属边框派（只变边框色，不换底不位移）
- **签名动效**: 数据刷新时数值 150ms 交叉淡化（旧值淡出、新值淡入），不滚动不闪烁——像报告翻到新的一页
- **入场编排**: 卡片自上而下 50ms stagger 入场，像报告逐节打印；图表入场 500ms 内完成后静止
- 展开/收起: **200ms ease-in-out**
- 禁止弹性过冲（bounce）动画与一切循环动画

## Layout & Grid

| 属性 | 值 |
|------|-----|
| 页面最大宽度 | 1920px |
| 网格系统 | CSS Grid, 3-4 列 |
| 卡片间距 | 16px |
| 页面内边距 | 24px |
| 图表容器最小高度 | 280px |
| 对齐方式 | 全部左对齐（KPI 也左对齐，像仪表盘不像海报） |

## Component Specifications

### KPI 卡片
- 背景 `--bg-card`，1px solid `--border-subtle`，圆角 6px，内边距 18px 20px
- **左对齐**：标签在上（12px 500 `--text-muted`，可全大写 + letter-spacing 0.4px），大数字在下
- **大数字**: 40px 600 IBM Plex Mono，`--text-primary`，禁止渐变文字
- **趋势**: 大数字右侧小 pill（10px 圆角），涨= `--success` 浅底深字，跌= `--danger` 浅底深字，含箭头
- **悬停**: 边框变为 `#C9C4B8`，无位移无阴影变化

### 图表容器
- 背景 `--bg-card`，1px solid `--border-subtle`，圆角 6px，内边距 16px
- **标题**: 16px 600 `--text-primary` 左对齐；副标题/口径说明 12px `--text-muted` 紧随其后
- **图表区**: 浅色背景上的 ECharts（浅色主题，勿套 dark）；网格线仅水平虚线
- **Tooltip**: 白底卡片（见 Chart Fingerprint）

### 按钮
- **主按钮**: `--accent-primary` 橙底白字，圆角 4px，内边距 9px 18px，14px 600；悬停加深为 `#D94400`
- **次按钮**: 白底，1px solid `--border-subtle`，文字 `--text-primary`；悬停底色 `--bg-hover`
- **禁用**: 50% 透明度，不改色

### 数据表格
- 表头: `--bg-elevated`，12px 600 `--text-secondary`，全大写 + letter-spacing 0.4px
- 数据行: 行高 44px，行间 1px `--border-subtle` 分割线，**不用斑马纹**
- 悬停行: 背景 `--bg-hover`，无边框变化
- 数字列: IBM Plex Mono 右对齐；文字列左对齐；状态用 `--success`/`--danger` 小圆点 + 文字

### 页头
- 背景 `--bg-primary`，底部 1px solid `--border-subtle`，高度 64px
- 标题 28-44px 700 `--text-primary` 左对齐（默认 28px，上限 44px，与 `--font-size-display` 一致），左侧可放 8px 宽橙色竖条作为品牌标记
- 右侧: 时间/数据源说明 13px `--text-muted`

### 进度条
- 高度 6px，全圆角 3px；轨道 `#E5E1D8`
- 填充 `--accent-primary` 纯色（达标段可换 `--success`），禁止渐变
- 标注: 百分比 12px IBM Plex Mono `--text-secondary`，置于条右端

## Anti-Patterns
- ❌ 深色/暗黑背景——本主题就是浅色，深色卡片同样禁止
- ❌ 图表渐变填充、面积图渐变、径向渐变饼图
- ❌ 发光、霓虹、彩色投影、毛玻璃
- ❌ KPI 大数字用彩色渐变文字或居中排版
- ❌ 把刺猬橙大面积铺底——它是点缀色，单屏出现面积 <5%
- ❌ 容器用 pill/大圆角（>6px）

## Do's and Don'ts
✅ 所有数字（KPI、表格、标签）用 IBM Plex Mono + tabular-nums，纵向对齐
✅ 层级靠"白卡 + 1px 米色描边"建立，不靠阴影
✅ 系列色严格按 Chart Color Palette 顺序使用
✅ 趋势 pill 是唯一的彩色小元素，其余彩色都留给图表
✅ 坐标轴、图例文字宁可小（11-12px）也不省略口径说明
❌ 不要在浅色底上用纯白文字或浅色小字（对比度必须够）
❌ 不要给 ECharts 套 dark 主题——背景必须是 `--bg-card` 白色
❌ 不要堆叠多个强调色装饰同一组件（橙色竖条 + 橙标题 + 橙边框 = 过度）
