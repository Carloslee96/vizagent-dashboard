# Monitor Dark — 暗色运维监控风

## Visual Theme
深夜值班室的监控墙：近黑底上整齐排列的深色面板，靠缝隙分隔而非边框与阴影（全库"分层五式"中本主题独占缝隙式，禁止混用边框/辉光/模糊分层）。绿色代表健康、橙色预警、红色事故——状态色是唯一允许"大声说话"的颜色，其余一律克制。整体是运维人员的仪表盘，不是演示用的展品：密度高、装饰零、阈值驱动一切。

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-primary` | `#111217` | 主背景（近黑微蓝，禁止纯黑） |
| `--bg-deeper` | `#0b0c0f` | 页头/页脚（比主背景深一层） |
| `--bg-card` | `#181b1f` | 面板/卡片（与背景靠缝隙分隔） |
| `--bg-elevated` | `#1f2329` | 抬升面：表头、悬停、tooltip |
| `--bg-hover` | `#262b33` | 行/面板悬停（微增亮） |
| `--border-subtle` | `#2a2f37` | 仅表格行线/tooltip 边线用，面板不用边框 |
| `--accent-primary` | `#5794F2` | 主交互色（Grafana 蓝，仅链接/交互/主系列） |
| `--accent-success` | `#73BF69` | 健康/正常阈值 |
| `--accent-warning` | `#FF9830` | 预警阈值 |
| `--accent-danger` | `#F2495C` | 告警/事故阈值 |
| `--text-primary` | `#d8d9da` | 主文字（off-white） |
| `--text-secondary` | `#9fa4ad` | 次要文字/坐标轴 |
| `--map-area` | `#1f2329` | 地图无数据区域底色 |
| `--map-boundary` | `#9fa4ad` | 地图国家/省级边界 |
| `--text-muted` | `#6e7280` | 弱化文字/时间戳 |

## Typography

| Role | Font | Size | Weight |
|------|------|------|--------|
| 页头标题 | Display 栈 | 22px | 600 |
| 面板标题 | Base 栈 | 14px | 500 |
| KPI 大数字 | Mono 栈, tabular-nums | 40px | 500 |
| KPI 标签 | Base 栈 | 12px | 500 |
| 正文/表格 | Base 栈 | 13px | 400 |
| 坐标轴/时间/单位 | Mono 栈 | 11px | 400 |

## Border Radius
- 面板/卡片: **3px**，tooltip/内嵌件: **2px**
- 按钮/输入框: **2px**
- 状态点: 6px 圆点；禁止超过 4px 的圆角，禁止药丸形按钮

## Shadows
不用。面板靠缝隙（露出 --bg-primary）与背景色阶分层。禁止一切 box-shadow / text-shadow / 发光。

## Component Patterns
- 面板即容器：深灰面板浮在近黑底上，之间留 12px 缝隙，无框无影
- KPI 用 stat 形态：整卡按阈值状态染色，一眼读出健康度
- 状态三色（绿/橙/红）是语义系统，不是装饰色板
- 一切数字等宽 tabular，时间戳 UTC 小字
- 单位与精度是设计的一部分：Y 轴单位显式标注（%/ms/req/s），百分比一律 1 位小数，整数指标带千分位

## Anti-Patterns
- ❌ 任何阴影/发光/毛玻璃/渐变面板
- ❌ 面板加 1px 边框（本主题靠缝隙分隔，边框是冗余）
- ❌ 状态三色用作普通系列色或装饰
- ❌ 圆角 > 4px、药丸按钮、纯黑 #000000
- ❌ 大面积蓝色铺底——蓝只给交互与主数据系列
- ❌ 循环闪烁/呼吸动画（唯一例外：告警状态点）
- ❌ tooltip 带边框——本主题 tooltip 无边框无阴影是细节签名

## Motion
- 动效人格：工具型"跟手"，一切过渡 ≤120ms 且只变亮度不变位
- 签名动效：critical 状态点 1.5s 脉冲——全库唯一允许的循环动画，其余元素一律静止
- 入场编排：无 stagger 同现——所有面板与图表同帧直接渲染，无任何入场动画（全库唯一"零入场"主题）
- 数字滚动: 500ms ease-out

## Layout & Grid

| 属性 | 值 |
|------|-----|
| 页面尺寸 | 1920×1080（按需自适应） |
| 网格 | CSS Grid 12 列，强对齐 |
| 卡片间距 | 12px（缝隙即分隔） |
| 页面内边距 | 20px |
| 页头 | 48px 高，底色 --bg-deeper，无底边线 |
| KPI 对齐 | 左对齐（标签上、数字下、趋势右） |
| 图表容器最小高度 | 260px |

## Component Specifications

### KPI 卡片
- stat 形态：**整卡染状态色**——按当前阈值用 --accent-success/warning/danger 的实色或 85% 深化色铺满卡底，数字与标签一律 `#fff`；无阈值语义的指标降级为 `--bg-card` 底 + `--text-primary` 数字
- 互斥声明：本主题的 stat 染色是**满铺实色/85% 深化**（sentry 的 stat 是 10% 淡染+毛玻璃，两者不得折中混用）
- 圆角 3px，内边距 14px 16px，无阴影无边框
- 标签 12px 500 居上；大数字 40px Mono tabular 居下，单位 14px 跟数字右侧基线对齐
- 趋势 ▲▼ + 百分比 12px Mono，染色卡上用白字 70% 透明度，不另起颜色

### 图表容器
- `--bg-card` 纯色底，圆角 3px，内边距 12px 16px，无阴影无边框
- 标题 14px 500 `--text-secondary` 左对齐，零装饰；右上角可放 11px Mono 单位/区间说明 `--text-muted`
- 图表区按 Chart Fingerprint 执行

### 按钮
- 主按钮: `--accent-primary` 底 + `#fff` 字，圆角 2px，13px 500，无阴影
- 次按钮: 透明 + `--text-secondary` 字，悬停时背景 `--bg-hover`
- 悬停亮度 +8%，100ms；禁用态降透明度至 40%

### 数据表格
- 表头: `--bg-elevated`，11px uppercase letter-spacing 0.06em `--text-muted`
- 行高 40px，行间 1px `--border-subtle` 分隔，无斑马纹
- 悬停行: 整行 `--bg-hover`；状态列用 6px 圆点（绿/橙/红），不用色块徽章
- 数字列 Mono 右对齐，文字列左对齐

### 页头
- 背景 `--bg-deeper`，高 48px，与内容区之间无底边线（靠色差分隔）
- 标题 22px 600 左对齐；可带一个 6px `--accent-success` 状态点表达全局健康度
- 右侧: Mono 11px UTC 时间戳 `--text-muted` + 告警计数（>0 时用 `--accent-danger` 数字）

### 进度条
- 高 4px，圆角 2px；轨道 `rgba(255,255,255,0.08)`
- 填充按阈值染色：<70% 用 `--accent-success`、70-90% 用 `--accent-warning`、>90% 用 `--accent-danger`
- 百分比 Mono 11px 右对齐跟在条后；禁止渐变填充与流光动画

## Chart Color Palette
- 系列色: #5794F2, #73BF69, #EAB839, #B877D9, #6ED0E0
- 状态三色 #73BF69/#FF9830/#F2495C 属于阈值与状态标记，不进常规系列轮换（绿与系列 2 同色时，系列 2 仅在无阈值语义的图表中使用）

## Chart Fingerprint
- 排他签名：**主系列面积填充透明度 0.10 是全库最低透明度渐变填充**——"10% 填充 + 阈值分档染色"组合全库唯一（别家最低填充 8% 的 linear 禁止多系列填充，无阈值分档）
- 折线（核心指纹）：线宽 2px，不显示常设数据点（hover 才出现 5px 圆点）；**面积渐变只给主系列**——系列色 0.10 → 0 纵向渐变，其余系列纯线；hover 显示竖直 crosshair（1px 虚线 `--text-muted`）并联动全部面板数值
- 阈值驱动配色：有阈值语义的折线/面积按 markLine 阈值线分档——超过 warning 阈值的区段线条与面积切 `--accent-warning`，超过 critical 切 `--accent-danger`；阈值线用 markLine 虚线（warning 橙 / critical 红，1px dashed，线右端标注阈值数值）
- markArea 区间标注：已知事件窗口（发布、维护、事故时段）用 `rgba(255,152,48,0.08)` 竖向 markArea 标出
- 柱形：直角（圆角 0），纯色填充禁止渐变；同组柱间距 30%；hover 整柱亮度 +15%
- 饼/环图：细环 radius ["55%","78%"]，中心 Mono 显示总数；标签走外侧引导线；禁止发光与玫瑰图
- 网格线：仅横向虚线 [4,4] `rgba(255,255,255,0.06)`；纵向网格线一律删除
- Tooltip：`--bg-elevated` 底 + 2px 圆角，无边框无阴影；系列用色点标示，数值 Mono tabular
- 图例：底部居中，12px `--text-secondary`，方形小色块 marker；坐标轴标签 11px Mono `--text-muted`；数据标签默认关闭
- 允许：阈值分档染色、markLine 阈值线、markArea 事件区间、主系列 10% 面积渐变
- 禁止：平滑曲线加粗发光、常设数据点、柱体渐变、3D、纵向网格线、状态三色当系列色

## Do's and Don'ts
- ✅ 折线 2px + 主系列 10%→0 面积渐变，这是监控风的第一眼指纹
- ✅ 阈值线必画：warning 橙虚线、critical 红虚线，数值标在线端
- ✅ KPI stat 卡整卡染色，一屏扫过去就知道哪里绿了哪里红了
- ✅ 一切数字等宽 tabular，时间戳 UTC 小字
- ✅ 面板靠缝隙分隔，无框无影
- ❌ 不要把状态三色撒进系列色轮换，它们只属于阈值与状态
- ❌ 不要给所有系列都加面积渐变——只给主系列，其余纯线
- ❌ 不要加装饰图标/插画，密度与对齐本身就是运维美学

## Token Schema

| Token | 值 | 说明 |
|-------|-----|------|
| `--radius-card` | `3px` | 卡片/KPI 圆角 |
| `--radius-button` | `2px` | 按钮圆角 |
| `--radius-panel` | `2px` | 图表容器/tooltip 圆角 |
| `--font-family-base` | `Inter, "Helvetica Neue", "PingFang SC", "Microsoft YaHei", sans-serif` | 全站 UI 字体 |
| `--font-family-display` | `Inter, "Helvetica Neue", "PingFang SC", sans-serif` | 页头标题（600） |
| `--font-family-mono` | `"Roboto Mono", "JetBrains Mono", Consolas, monospace` | 一切数字/时间/单位 |
| `--font-size-display` | `22px` | 页头主标题 |
| `--font-size-title` | `14px` | 面板标题 |
| `--font-size-kpi` | `40px` | KPI 大数字（Mono + tabular-nums） |
| `--shadow-card` | `none` | 无阴影，靠缝隙与色阶分层 |
| `--glow-accent` | `none` | 本主题无任何发光 |
| `--decoration` | `flat` | 纯平：无渐变面板、无发光、无高光线 |
| `--bg-pattern` | `grid` | 页面层 3% 细网格纹理，模拟监控墙坐标纸；网格间距 48px 大格（与 linear 24px / palantir 32px / sentry 40px 参数化区分） |
| `--pattern-color` | `rgba(255,255,255,0.03)` | 深色主题纹理色（细网格线） |
| `--kpi-variant` | `stat` | 整卡染阈值状态色的 Grafana stat 卡 |
