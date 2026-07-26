# Deploy Light — 亮色部署极简风

## Visual Theme
Vercel 的设计语言是"克制到苛刻"：纯黑背景、近白文字、1px 微边框，白色本身就是强调色。渐变、发光、彩色面板一律禁止——信息层级完全靠字号、字重与灰阶建立。Geist 字体 + 负字距等宽大数字是标志性特征，参考 vercel.com 与 Geist Design System。

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-primary` | `#000000` | 主背景（纯黑，禁止替换） |
| `--bg-card` | `#0a0a0a` | 卡片 |
| `--bg-elevated` | `#141414` | 悬浮面板/Tooltip |
| `--bg-hover` | `#1f1f1f` | 悬停背景 |
| `--border-subtle` | `#1a1a1a` | 边框（仅 1px） |
| `--accent-primary` | `#ffffff` | 强调色=纯白 |
| `--accent-secondary` | `#3291ff` | 链接/交互蓝（Geist Blue） |
| `--accent-success` | `#50e3c2` | 成功（Geist Teal） |
| `--accent-warning` | `#f5a623` | 警告 |
| `--accent-danger` | `#ee0000` | 错误 |
| `--text-primary` | `#fafafa` | 主文字 |
| `--text-secondary` | `#888888` | 次要文字 |
| `--map-area` | `#141414` | 地图无数据区域底色 |
| `--map-boundary` | `#888888` | 地图国家/省级边界 |
| `--text-muted` | `#555555` | 弱化文字 |

## Chart Fingerprint
- 折线：线宽 1.5px；默认 symbol: none，hover 才显示 5px 白色圆点；禁止面积渐变，如需填充仅允许纯色 rgba(255,255,255,0.04)；hover 触发 1px 实线 #333 十字指示线
- 柱形：直角 [0,0,0,0]（绝不用圆角）；纯色填充，禁止渐变；hover 整柱亮度 +15%，无其他效果
- 饼/环图：优先环图，radius ['55%','78%']；标签放环外细引线，11px `--text-secondary`，数值用等宽字体；禁止发光与扇区分离
- 网格线：仅横向，1px 虚线，用 `--border-subtle`；纵向网格线一律关闭
- Tooltip：背景 #000，1px 实线边框 #333，无阴影，文字 12px，数值用 Geist Mono
- 图例：11px，`--text-secondary`，8px 圆形图标；数据标签默认关闭，仅 KPI 型图表开启，12px 等宽字体
- 排他签名：折线 1.5px 是全库最细线宽（多数主题 ≥2px）；`rgba(255,255,255,0.04)` 纯白微填充是全库唯一的白色系面积填充——别家的面积填充一律是彩色，只有 vercel 用白
- 签名句式：折线优先 `endLabel` 末端标注替代图例（12px `--text-primary` 等宽数值）；`markLine` 均值用 1px 虚线 `--border-subtle`、目标线用 1px 实线 #fff；`markArea` 仅标注阈值区间，纯色 rgba(255,255,255,0.04)；阈值染色：越限系列/柱形改 `--accent-warning`/`--accent-danger` 纯色；面积渐变一律不启用
- 允许：白色单色图表、蓝/青作状态点缀、等宽数字、细十字指示线
- 禁止：渐变填充、发光/阴影、3D、explode、任何粗于 2px 的线条

## Token Schema
| Token | 值 | 说明 |
|--------|----|------|
| `--radius-card` | `6px` | 卡片圆角 |
| `--radius-button` | `6px` | 按钮圆角 |
| `--radius-panel` | `6px` | 面板圆角 |
| `--font-family-base` | `'Geist','Inter',-apple-system,'Segoe UI',sans-serif` | 正文字体栈 |
| `--font-family-display` | `'Geist','Inter',-apple-system,'Segoe UI',sans-serif` | 标题/大数字字体栈 |
| `--font-family-mono` | `'Geist Mono',ui-monospace,'SF Mono',Menlo,monospace` | 数字/代码字体栈 |
| `--font-size-display` | `56px` | 主 KPI 大数字 |
| `--font-size-title` | `16px` | 卡片标题 |
| `--font-size-kpi` | `32px` | 次要 KPI 数字 |
| `--shadow-card` | `none` | 卡片无阴影 |
| `--glow-accent` | `none` | 无发光 |
| `--decoration` | `flat` | 纯平：无渐变、无发光、无高光线 |
| `--bg-pattern` | `none` | 零纹理是立场——纯黑不容噪点；与 apple 划清互斥：apple=noise+毛玻璃，vercel=零纹理+边框，禁止杂交 |
| `--pattern-color` | `rgba(255,255,255,0.04)` | 纹理色（none 时仅作备用，深色主题白纹） |
| `--kpi-variant` | `plain` | 纯大数字+小号灰单位，字重双对比，零装饰 |

## Decorative Style
极简主义的零装饰哲学——空白本身就是最好的装饰。装饰必须少到几乎看不见。
- P0 标题栏：一条 1px 高纯白色半透明横线（`rgba(255,255,255,0.08)`），两端平齐无圆角，不做渐隐。每个面板上方，但透明度极低，几乎不可见。
- P1 四角：无。四角不做任何装饰。
- P2 分隔线：无。不用分隔线，只用 1px `--border-subtle` 边框分割。
- 整体原则：**装饰即干扰**——当不确定是否需要装饰时，选择不加。任何可见的装饰都是失败。

## Typography
- 全局 Geist，fallback Inter + 系统字体；数字/代码 Geist Mono，fallback ui-monospace
- 大数字：48-56px，700，letter-spacing -0.03em，必用 tabular-nums
- 卡片标题 16px/600；正文 14px/400，line-height 1.5；辅助文字 12px
- 层级靠字重与灰阶区分，不靠增加颜色

## Border Radius
6px 全局统一（卡片/按钮/面板/输入框），状态圆点等圆形元素除外；禁止混入其他圆角值。

## Shadows
一律无阴影，层级只用边框与背景灰阶表达；唯一允许：悬浮层 1px #333 边框代替阴影。

## Motion
- 签名动效：数字滚动 800ms ease-out，一次完成绝不循环——Vercel 的数字只说一遍（全库唯一"不循环"声明）；其余交互 150ms 只改色不改形，快而静
- 入场编排：无 stagger——整屏卡片与图表同现，不做逐项延迟；黑底白字一次到位即完成
- 禁止弹跳、弹性、发光脉冲动画

## Layout & Grid

| 属性 | 值 |
|------|-----|
| 页面最大宽度 | 1920px |
| 网格系统 | CSS Grid，4 列 |
| 卡片间距 | 16px |
| 页面内边距 | 24px |
| 图表容器最小高度 | 280px |
| 对齐方式 | 全部左对齐（标题、数字、图例） |

## Component Specifications

### KPI 卡片
- 背景 `--bg-card`，1px `--border-subtle` 边框，6px 圆角，内边距 20px 24px
- 大数字左对齐：48px/700，`--text-primary`，letter-spacing -0.03em，tabular-nums
- 标签在大数字上方（Vercel 惯例：小标签在上），12px，`--text-secondary`
- 单位降级为 0.42em 小字灰色（`--kpi-variant: plain`：数字/单位字重双对比）
- 不渲染趋势徽章与迷你图——变化趋势交给折线图表达，卡片只陈述当前值
- 悬停：边框变 #333，无位移无阴影

### 图表容器
- 背景 `--bg-card`，1px 边框，6px 圆角，内边距 16px
- 标题 16px/600 左对齐；可选副标题 12px `--text-muted` 紧随其下
- 右上角可放 12px 时间范围切换（纯文字按钮，无背景）
- 图表区严格按 Chart Fingerprint 执行

### 按钮
- 主按钮：白底黑字（#fff 背景 / #000 文字），6px 圆角，14px/500，padding 8px 16px
- 次按钮：透明背景 + 1px `--border-subtle` 边框，`--text-primary` 文字
- 悬停：主按钮变 #e0e0e0，次按钮边框变 #444；无阴影无发光

### 数据表格
- 表头：12px/600，`--text-secondary`，背景 `--bg-primary`，下边框 1px `--border-subtle`
- 数据行：行高 44px，行间 1px `--border-subtle` 分割线，不用斑马纹
- 悬停行：背景 `--bg-hover`，无左侧色条
- 数字列：Geist Mono 右对齐；状态用 8px 圆点 + 文字

### 页头
- 高度 56px，背景 `--bg-primary`，底部 1px `--border-subtle` 分割线
- 标题 20px/700 左对齐；右侧时间戳用 Geist Mono 12px `--text-muted`
- 可用 ▲ 三角符号作品牌标记

### 进度条
- 高度 4px，pill 圆角，背景 `--border-subtle`，填充纯白 `--accent-primary`，无渐变
- 百分比标注：右侧，12px Geist Mono，`--text-muted`

## Chart Color Palette
系列色: #fafafa, #888888, #3291ff, #50e3c2, #f5a623, #555555

## Anti-Patterns
- ❌ 任何渐变（背景、图表、按钮一律纯色）
- ❌ 发光、阴影、模糊装饰
- ❌ 彩色大面积背景——颜色只允许出现在数据与状态中
- ❌ 圆角 ≠ 6px 的元素、粗于 1px 的边框
- ❌ 居中排版的 KPI 或标题
- ❌ 把纯黑底换成深蓝/深灰偏色

## Do's and Don'ts
✅ 大数字负字距 + tabular-nums，等宽字体对齐
✅ 层级用灰阶（#fafafa/#888/#555）而非新颜色
✅ 白色作为最强强调色（主按钮、关键数字、第一系列）
✅ 交互反馈快而轻：150ms，只改色不改形
✅ 用 ▲ 符号、等宽时间戳等 Vercel 标志性细节
❌ 不要为"丰富"加装饰——空白本身就是设计
❌ 不要把蓝/青当装饰色大面积铺，它们只属于链接与状态
