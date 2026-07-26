# Vibe Night — 音乐暗色律动风

## Visual Theme
深黑底 + 标志性品牌绿，专辑封面驱动的圆润友好美学。靠三层灰色背景（#121212 → #181818 → #282828）分层，不用边框和阴影堆砌；大胆粗体字、药丸形按钮、大圆角，氛围是"深夜听歌"的温暖而非冷酷科技感。

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-primary` | `#121212` | 主背景（禁用纯黑） |
| `--bg-card` | `#181818` | 卡片/面板 |
| `--bg-elevated` | `#282828` | 悬浮/选中/hover |
| `--bg-hover` | `#2a2a2a` | 列表行悬停 |
| `--border-subtle` | `#292929` | 微边框/分隔线 |
| `--accent-primary` | `#1ed760` | Spotify Green — 仅用于强调与关键数据 |
| `--accent-secondary` | `#509bf5` | 链接/辅助信息 |
| `--success` | `#1ed760` | 正向趋势 |
| `--danger` | `#f15e6c` | 负向趋势 |
| `--text-primary` | `#ffffff` | 主文字 |
| `--text-secondary` | `#b3b3b3` | 次要文字 |
| `--map-area` | `#282828` | 地图无数据区域底色 |
| `--map-boundary` | `#b3b3b3` | 地图国家/省级边界 |
| `--text-muted` | `#727272` | 弱化文字 |

## Chart Fingerprint

- 折线：线宽 **3px**（全库最粗线宽之一，自信有力），`smooth: true` 平滑曲线；默认不显示数据点，hover 时显示 8px 白色描边圆点；**允许**面积渐变（`--accent-primary` 从 30% 透明度渐到 0%）——**30% 是全库最大面积填充，数值即排他签名**；多系列时仅主系列用渐变
- 柱形：**全圆角** `[8,8,8,8]`——**全库最大柱圆角（airbnb 为 6px），数值即排他签名**；允许**同色系**垂直渐变（亮绿→深绿）——跨色品牌渐变归 airbnb，本主题禁用；hover 时整柱亮度提升 15%
- 饼/环图：只用环形 `radius: ['55%', '80%']`，环形中心可放总数大字；标签用外部引导线 + `--text-secondary`，**禁止**发光与阴影
- 网格线：仅保留横向虚线 `1px dashed --border-subtle`，纵向网格线一律关闭；坐标轴线不显示
- Tooltip：背景 `--bg-elevated`，无边框，圆角 8px，阴影 `0 8px 24px rgba(0,0,0,0.5)`，文字 13px
- 末端标注：**endLabel 替代图例**，系列名直接标在折线末端（12px `--text-secondary`），图例默认不渲染；仅多系列密集交叉无法末端标注时才退回 12px 圆点图例
- 参考线：**markLine 均值虚线**（`1px dashed --text-muted`，标注"均值"），有业务目标时另加**目标实线**（`1px solid --accent-primary`）
- 阈值染色：柱形/数据点低于均值或目标时染 `--danger`，达标保持 `--accent-primary` 纯色
- 数据标签默认关闭，仅 KPI 类图表显示端点数值
- 允许：大圆角、柔和面积渐变、平滑曲线、环形图中心大数字
- 禁止：发光/投影、直角柱形、纵向网格线、3D 效果、纯黑 `#000000`

## Token Schema

| Token | 值 | 说明 |
|--------|----|------|
| `--radius-card` | `12px` | 卡片圆角 |
| `--radius-button` | `999px` | 药丸形按钮（Spotify 标志性） |
| `--radius-panel` | `8px` | 面板圆角 |
| `--font-family-base` | `'Nunito Sans', 'Inter', -apple-system, 'Segoe UI', sans-serif` | 全局字体（替代专有 CircularSp 的圆润几何无衬线） |
| `--font-family-display` | `'Nunito Sans', 'Inter', -apple-system, sans-serif` | 大数字/标题 |
| `--font-family-mono` | `'JetBrains Mono', 'SFMono-Regular', Consolas, monospace` | 表格数字 |
| `--font-size-display` | `28px` | 页头标题 |
| `--font-size-title` | `16px` | 面板标题 |
| `--font-size-kpi` | `48px` | KPI 大数字（weight 800） |
| `--shadow-card` | `none` | 靠背景色分层，不用阴影 |
| `--glow-accent` | `none` | 无发光 |
| `--decoration` | `flat` | 纯平三层灰背景分层，无渐变无发光 |
| `--bg-pattern` | `dots` | 页面层 **32px 大间距疏点**纹理，像专辑封面的印刷网点（figma 20px 密点/supabase 16px minimap 点，同纹理不同参数） |
| `--pattern-color` | `rgba(255,255,255,0.03)` | 深色主题纹理色，仅隐约可辨 |
| `--kpi-variant` | `sparkline` | KPI 卡底部迷你走势线（绿色、无坐标轴） |

## Typography
- 全局: **Nunito Sans**（圆润几何无衬线，替代 Spotify 专有 CircularSp）/ **Inter** fallback
- KPI 大数字: 48-64px, weight **800**, letter-spacing -0.03em, 左对齐——**800 是全库最粗 KPI 字重，与 supabase 400 构成全库字重两极**
- 面板标题: 16px 700, 左对齐
- 正文: 14px 400, `--text-secondary`

## Border Radius
卡片 12px / 面板 8px / 按钮与标签 **999px 药丸形** / 输入框 4px。圆角是 Spotify 友好感的核心，禁止小于 4px。

## Shadows
几乎不用。卡片/面板 `none`，仅悬浮层（tooltip、下拉）用 `0 8px 24px rgba(0,0,0,0.5)`。层级靠 `#121212 → #181818 → #282828` 背景色递进表达。

## Component Specifications

### KPI 卡片
- 背景 `--bg-card`，**无边框无阴影**，圆角 12px，内边距 24px
- 大数字 48px 800 `--text-primary` **左对齐**置顶；标签 13px `--text-secondary` 在数字下方
- 卡底放 sparkline 迷你走势线（`--accent-primary` 2px 平滑曲线、无坐标轴无数据点，面积渐变 20%→0%），呼应"听歌趋势"手感
- 趋势箭头：↑ `#1ed760` / ↓ `#f15e6c`，12px，放数字右侧同行
- 悬停：整张卡片背景过渡到 `--bg-elevated`（像歌单卡片悬停），无位移无阴影

### 图表容器
- 背景 `--bg-card`，无边框，圆角 8px，内边距 20px
- 标题 16px 700 `--text-primary` 左对齐，副标题（如有）13px `--text-muted`
- 图表区按 Chart Fingerprint 执行；容器悬停不变（与 KPI 卡片区分层级）

### 按钮
- 主按钮：`--accent-primary` 背景 + **#000000 黑字**，999px 药丸形，14px 700，内边距 12px 32px
- 次按钮：透明背景 + `1px solid --text-muted` 边框 + 白字，同为药丸形
- 悬停：`transform: scale(1.04)` 放大 + 亮度微升（Spotify 标志性交互），不用变色

### 数据表格
- 表头：12px 600 `--text-muted` 全大写字母，无背景色
- 数据行：行高 52px，行间 `1px solid --border-subtle`，**不用交替背景**
- 悬停行：整行背景变 `--bg-hover`，无左边框高亮
- 数字列：`--font-family-mono` 右对齐；文字列左对齐

### 页头
- 背景 `--bg-primary` 无下边框，高度 64px
- 标题 28px 800 `--text-primary` 左对齐；右侧放药丸形时间筛选器（`--bg-elevated` 底 + 999px 圆角）——**页头绿色只出现在筛选器选中态**
- 更新时间 13px `--text-muted`

### 进度条
- 高度 4px，圆角 999px（两端全圆，像播放进度条）
- 轨道 `--bg-elevated`，填充 `--accent-primary` 纯色
- 百分比标注 12px `--text-muted`，放进度条右端

## Motion
- 动效人格: 消费型"有感但轻"（200-350ms 区间），禁止弹跳
- **签名动效**: scale+换底组合——按钮 hover `transform: scale(1.04)`（**全库唯一缩放式交互**）+ KPI 卡 hover 背景 200ms 过渡到 `--bg-elevated`（模拟歌单卡悬停），两动作成对出现
- **入场编排**: KPI 卡从左到右 **80ms stagger** 依次入场（像歌单横向浏览），图表系列依次淡入 400ms
- 数字滚动: 800ms ease-out
- 展开/收起: 250ms ease-in-out

## Layout & Grid

| 属性 | 值 |
|------|-----|
| 页面最大宽度 | 1920px |
| 网格系统 | CSS Grid, 3-4 列 |
| 卡片间距 | 16px |
| 页面内边距 | 24px |
| 图表容器最小高度 | 280px |
| 对齐方式 | 全部左对齐（Spotify 不做居中排版） |
| 密度基调 | 标准偏松 |

## Chart Color Palette
- 系列色: #1ed760, #509bf5, #ff6437, #ffc862, #b49bc8（绿色永远是第一系列；第 5 色紫仅用于对照/基线系列）

## Anti-Patterns
- ❌ 纯黑 `#000000` 背景——Spotify 最暗是 `#121212`
- ❌ 直角或仅上圆角的柱形——必须全圆角 `[8,8,8,8]`
- ❌ 直角矩形按钮——必须药丸形 999px
- ❌ 给卡片加发光、投影或彩色边框——层级只用灰背景递进
- ❌ 绿色滥用——`--accent-primary` 只给关键强调，不做大面积填充背景
- ❌ 居中排版 KPI 或标题——一律左对齐
- ❌ uppercase 全大写宽字距工程标签——消费品牌不用工程标签语言，与 figma/grafana/terminal 组划清

## Do's and Don'ts
✅ 按钮 hover 用 `scale(1.04)` 而非变色
✅ KPI 卡片悬停整卡背景变 `--bg-elevated`，模拟歌单卡片手感
✅ 折线 3px 粗线 + 平滑曲线，面积渐变仅主系列
✅ 表格行间细分隔线 + 行悬停变亮，不用斑马纹
❌ 不要 3D、玻璃拟态、霓虹发光等科技感装饰
❌ 不要用渐变面板或顶部高光线——Spotify 是纯平分层
❌ 不要把系列色用到第 6 种以上，绿色永远是第一系列
