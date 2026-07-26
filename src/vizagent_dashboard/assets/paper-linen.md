# Paper Linen — 暖纸衬线人文风

## Visual Theme
Anthropic 官方暖纸美学：羊皮纸底色 #faf9f5 + 陶土橙 #d97757，衬线标题（Lora）配几何无衬线正文（Poppins）。整套屏**不用一寸深蓝、不发光、不玻璃拟态**——像一份排版精良的纸质报告，而不是一块监控屏。这是浅色主题，禁止改深。

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-primary` | `#faf9f5` | 主背景（羊皮纸米白） |
| `--bg-card` | `#ffffff` | 卡片（纯白浮于纸面） |
| `--bg-elevated` | `#f0eee6` | 悬浮/表头/轨道（亚麻色） |
| `--bg-hover` | `#e8e6dc` | 悬停态（浅灰米） |
| `--border-subtle` | `#e3e0d6` | 分隔线（暖灰发丝线） |
| `--accent-primary` | `#d97757` | Crail 陶土橙（主强调） |
| `--accent-secondary` | `#6a9bcc` | 灰蓝（次强调/信息） |
| `--accent-success` | `#788c5d` | 苔绿（成功/正向） |
| `--accent-danger` | `#b0483a` | 赭红（告警，不用纯红） |
| `--text-primary` | `#141413` | 主文字（墨黑，非纯黑） |
| `--text-secondary` | `#6b6960` | 次要文字（石灰） |
| `--map-area` | `#f0eee6` | 地图无数据区域底色 |
| `--map-boundary` | `#6b6960` | 地图国家/省级边界 |
| `--text-muted` | `#b0aea5` | 弱化文字（沙灰） |

## Chart Color Palette
- 系列色: #d97757, #6a9bcc, #788c5d, #d3a04d, #b0aea5

## Chart Fingerprint
生成 ECharts option 时逐项照此执行：
- **折线**：`lineWidth: 3`，`smooth: true`（柔和曲线，不是折角）；默认不显示数据点，hover 时当前点放大为 8px 白芯橙边圆点；面积填充**允许但克制**——仅主系列用 `--accent-primary` 从 12% 透明度渐变到 0，多系列时一律不填面积
- **柱形**：仅上圆角 `barBorderRadius: [8,8,0,0]`，纯色填充（按系列色轮换），**禁止柱体渐变**；hover 时该柱明度微降其余淡出（`emphasis.focus: 'series'`）
- **饼/环图**：只做环形，`radius: ['55%','78%']`，扇区间 2px `--bg-card` 色缝隙；标签放外侧、12px `--text-secondary`、引导线细短；环中心用 Lora 衬线大字显示合计；**禁止任何发光/投影**
- **排他签名（全库唯一）**：环图中心衬线大字合计是全库唯一的"衬线环心"（newsroom 已改无衬线 mono 总数让位，本主题独占）；叠加全库唯一的 `[2,6]` 点划线横向网格，两者构成图表区身份
- **网格线**：只画横向，**点划线 `[2,6]`**、1px、色取 `--border-subtle`——纸面点线比虚线更"印刷"，`[2,6]` 是全库唯一网格线型；纵向网格线一律删除；坐标轴线不显示，只留刻度文字
- **Tooltip**：白底 `#ffffff`、1px `--border-subtle` 边框、暖色软阴影 `0 4px 16px rgba(20,20,19,0.12)`、文字 `--text-primary`，左侧小色点标识系列
- **图例**：`icon: 'circle'`，12px Poppins、`--text-secondary`，置于图表上方左对齐；轴标签与数据标签 11-12px `--text-secondary`，数据标签非必要不开
- **签名句式**：单系列折线/柱形默认 `endLabel` 末端标注替代图例（系列名+终值，`--text-secondary` 12px）；有明确基线的图加 `markLine`——均值用 `--text-muted` 虚线、目标值用 `--accent-primary` 实线（报告式参考线，标注文字 11px）；允许阈值染色（达标 `--accent-success`、超标 `--accent-danger`）；面积渐变只给主系列（同折线条款）
- **允许**：衬线大字合计、`[2,6]` 点划线网格、柔和曲线、淡面积填充
- **禁止**：发光（shadowBlur）、霓虹色、深色图表底、3D 图表、柱状渐变、冷蓝主色

## Token Schema

| Token | 值 | 说明 |
|--------|----|------|
| `--radius-card` | `16px` | 卡片圆角（友好大圆角） |
| `--radius-button` | `999px` | 按钮圆角（胶囊形） |
| `--radius-panel` | `12px` | 面板圆角 |
| `--font-family-base` | `'Poppins',-apple-system,'Segoe UI',sans-serif` | 正文/标签字体栈（CDN 加载 Poppins，带系统 fallback） |
| `--font-family-display` | `'Lora',Georgia,'Times New Roman',serif` | 标题/KPI 数字字体栈（衬线是灵魂，fallback Georgia） |
| `--font-family-mono` | `'JetBrains Mono','SFMono-Regular',Consolas,monospace` | 代码/表格数字字体栈 |
| `--font-size-display` | `26px` | 页头标题 |
| `--font-size-title` | `16px` | 卡片标题 |
| `--font-size-kpi` | `40px` | KPI 大数字（衬线） |
| `--shadow-card` | `0 1px 3px rgba(20,20,19,0.08)` | 卡片阴影（纸张级轻柔） |
| `--glow-accent` | `none` | 本主题无发光 |
| `--decoration` | `flat` | 纯平无渐变无发光 |
| `--bg-pattern` | `dots` | 页面层信纸点阵纹理（dots 是本主题在三胞胎中的独占纹理；noise 让给 newsroom/notion，本主题禁用） |
| `--pattern-color` | `rgba(0,0,0,0.05)` | 点阵色（浅色主题 5% 黑；点阵是离散墨点，需比噪点略可见才成立） |
| `--kpi-variant` | `plain` | KPI 纯大数字+单位降级（衬线大数字即品牌时刻） |

## Decorative Style
暖纸上的印刷品装饰——像一本精装书的章节装饰线，有温度、有触感。
- P0 标题栏：面板标题上方 2px 高暖橙色横线（`--accent-primary` #d97757），两端渐隐，左端起始处加 6px 直径实心圆点（同色），整体像印刷品的章节分隔线。圆角 3px。
- P1 四角：左上/右下对称的短弧线（1.5px 线宽，暖灰 `--border-subtle`），端点回勾像书角装饰。30×30px。
- P2 分隔线：KPI 区与图表区之间一条 2px 点划线（`--accent-primary` 30% 透明度），中间一枚 8×4px 的扁椭圆装饰（暖橙色渐变）。
- 整体原则：**像印刷品的装帧元素**——圆润、温暖、有纸质触感。

## Typography
- 标题/KPI 数字: **Lora** 衬线，600，KPI 40px / 页头 26px / 卡题 16px
- 正文/标签: **Poppins** 400-500，12-14px，line-height 1.6
- 表格数字: **JetBrains Mono** 12px（等宽对齐）
- 字重克制：全屏只用 400/500/600 三档，不用 700+

## Border Radius: 卡片 16px / 面板 12px / 按钮胶囊 / 输入框 10px——整体偏圆，但图表柱体只圆上方

## Shadows
- 卡片: `0 1px 3px rgba(20,20,19,0.08)`（唯一常规阴影）
- 悬浮面板/Tooltip: `0 4px 16px rgba(20,20,19,0.12)`
- 阴影色永远带暖棕底（rgba(20,20,19,...)），禁用蓝灰阴影

## Motion
- **签名动效**：数字滚动 **900ms ease-out** + Lora 衬线数字——全库最慢的慢滚动，衬线数字逐位翻过即品牌时刻，禁止加速
- **入场编排**：图表入场 600ms ease-out，各系列 **stagger 80ms 依次入场**（纸张逐页翻开的节奏）
- 展开/收起: **300ms cubic-bezier(0.2,0,0,1)**（先快后稳的"落定感"）

## Layout & Grid

| 属性 | 值 |
|------|-----|
| 页面最大宽度 | 1920px |
| 网格系统 | CSS Grid，3 列为主（宽松呼吸感） |
| 卡片间距 | 20px |
| 页面内边距 | 32px |
| 图表容器最小高度 | 300px |
| 对齐方式 | 全部左对齐（报告式阅读动线） |

## Component Specifications

### KPI 卡片
- 背景 `--bg-card` + 1px `--border-subtle` + `--shadow-card`，圆角 16px，内边距 24px
- **大数字**: Lora 衬线 40px 600 `--text-primary`，**左对齐**（本主题的签名特征）
- **标签**: 13px 500 Poppins `--text-secondary`，数字上方（先标签后数字的报告式层级）
- **趋势**: 12px 文字式（"+12.4% vs 上周"），涨用 `--accent-success` 跌用 `--accent-danger`，不用箭头图标
- **悬停**: 仅阴影加深到 `0 4px 12px rgba(20,20,19,0.10)`，无边框变色无位移

### 图表容器
- 背景 `--bg-card`，圆角 16px，内边距 20px 24px
- **标题**: Lora 16px 600 `--text-primary` 左对齐；可带一行 12px `--text-muted` **口径说明**（数据来源/统计周期，只陈述口径不下结论——"结论句标题"是 newsroom 的签名，本主题禁用）
- 图表区执行 Chart Fingerprint；浅色图表，坐标轴文字 `--text-secondary`

### 按钮
- **主按钮**: `--accent-primary` 底 + 白字，胶囊圆角，内边距 10px 24px，14px 500；hover 底加深为 `#c96645`
- **次按钮**: 透明底 + 1px `--border-subtle` + `--text-primary`，hover 底色变 `--bg-elevated`
- **禁用**: 50% 透明度，不改配色

### 数据表格
- 表头：**无底色**，仅 1px `--border-subtle` 下边框，12px 600 `--text-muted`，字母间距 0.02em
- 数据行：行高 44px，行间发丝线 `--border-subtle`，**不做交替底色**（纸面感）
- 悬停行：整行底色变 `--bg-elevated`，无左边框强调条
- 数字列：JetBrains Mono 右对齐；首列文字 Lora 500 左对齐

### 页头
- 无底色无卡片，直接印在羊皮纸上，底部 1px `--border-subtle` 通栏发丝线
- 标题: Lora 26px 600 `--text-primary` 左对齐；时间/筛选器 13px `--text-muted` 右侧
- 标题旁可用一小段 `--text-secondary` 副标题说明数据口径

### 进度条
- 高度 6px，全圆角；轨道 `--bg-elevated`，填充 `--accent-primary` 纯色
- 标注：百分比 12px `--text-secondary` 放条右端同行，不换行不加底色

## Anti-Patterns
- ❌ 把背景改成深色——浅色纸面是本主题的身份
- ❌ 纯黑 `#000000`：墨黑一律用 `#141413`
- ❌ 任何发光（box-shadow 彩色光晕 / text-shadow glow）与玻璃拟态
- ❌ 科技蓝主色、蓝紫渐变——Claude 调色板里没有深蓝
- ❌ KPI 数字用无衬线粗黑体——必须是 Lora 衬线
- ❌ 居中排版大屏标题/KPI——全部左对齐
- ❌ 图表标题写"结论句"（如"销售额大幅增长"）——结论句让给 newsroom，本主题副标题只写口径说明
- ❌ 页面纹理用 noise——dots 信纸点阵是本主题纹理，noise 让给 newsroom/notion
- ❌ 环图中心用无衬线数字——衬线环心是本主题独占，无衬线环心属于 newsroom

## Do's and Don'ts
✅ 强调色按橙→蓝→绿顺序轮换，暖橙永远是第一系列
✅ 标签在前、衬线大数字在后的 KPI 层级
✅ 用发丝线（1px 暖灰）而非色块做分隔
✅ 图表标题下写一行口径说明句（陈述数据来源/周期，不下结论）
✅ 圆角偏大、阴影极轻、留白偏多
❌ 不要交替行底色表格（用发丝线分行）
❌ 不要箭头图标表达趋势（用文字 +/-%）
❌ 不要 700 以上字重
❌ 不要给柱体/饼块加渐变或投影
