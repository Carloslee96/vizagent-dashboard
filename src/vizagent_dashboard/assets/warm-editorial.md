# Warm Editorial — 暖色调新闻室风

## Visual Theme
浅色、纸感、编辑部气质。米白纸底（#FAF9F6）上铺开墨黑（#1a1a1a）文字与图表，唯一强调色是深红 #A23E48——像 Our World in Data / Datawrapper 的数据新闻图表：衬线大标题、结论先行、末端标注取代图例、参考线直给判断依据。层次靠纸底色差与细线，不靠阴影与装饰。

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-primary` | `#FAF9F6` | 页面背景（米白纸底） |
| `--bg-card` | `#ffffff` | 卡片/面板（纸面白） |
| `--bg-elevated` | `#f1efe9` | 表头、弹层、嵌套区（略深的纸色） |
| `--bg-hover` | `#f1efe9` | 行/卡片悬停 |
| `--border-subtle` | `#e3e1da` | 分隔线与卡片描边（仅 1px） |
| `--accent-primary` | `#A23E48` | 深红（唯一强调色） |
| `--accent-secondary` | `#7a2e36` | 深红暗调，hover/激活态 |
| `--accent-success` | `#3a7d5c` | 正向指标（低饱和绿） |
| `--accent-warning` | `#b0762a` | 预警（赭黄） |
| `--accent-danger` | `#A23E48` | 负向/异常（与强调色同源深红） |
| `--text-primary` | `#1a1a1a` | 主文字（墨黑，禁用纯黑 #000） |
| `--text-secondary` | `#5f5f5a` | 次要文字 |
| `--map-area` | `#f1efe9` | 地图无数据区域底色 |
| `--map-boundary` | `#5f5f5a` | 地图国家/省级边界 |
| `--text-muted` | `#9b9a93` | 弱化文字/来源注 |

## Typography
- 页头标题: **Playfair Display 衬线**, 30px 700 — 报纸头版式标题
- 面板标题: Playfair Display 16px 600, 左对齐；可用一句话结论作标题
- KPI 数字: Playfair Display 40px 700, tabular-nums；单位降级为小字
- 正文/表格: Inter 14px 400, 行高 1.6
- 数字/代码: IBM Plex Mono 13px

## Border Radius
- 卡片/面板: **4px** | 按钮: **3px** | 进度条: **2px** — 接近直角的印刷感

## Shadows
- 卡片: `0 1px 2px rgba(26,26,26,0.05)`（几乎不可见，层次靠白卡落在米白底上）
- 悬浮层/Tooltip: `0 4px 12px rgba(26,26,26,0.10)`

## Component Patterns
- 层次三件套：米白底 + 白卡 + 1px 细边框，禁止第四层装饰
- 深红只给：主数据系列、主按钮、关键 markLine/阈值——一屏红元素 ≤3 处
- 注释文字（来源、口径说明）用 12px `--text-muted`，是编辑风的合法成员

## Anti-Patterns
- 禁止深色卡片/深色模式——本主题是纸面浅色大屏
- 禁止渐变、发光、玻璃拟态、粗于 1px 的边框
- 禁止多色图表——除深红外只允许灰阶系列
- 禁止冷灰背景（如 `#f4f4f5`），保持米白 `--bg-primary`
- 禁止把面板标题写成"XX统计"式名词短语——新闻风标题是结论句
- "结论句标题"为本主题独占句式——"口径说明句/讲人话"式说明句归 claude（对方 Anti-Patterns 亦以本主题为反例）；本主题标题必须带判断、可站立场

## Motion
- 签名动效: **入场即静止**——所有动效跑完后画面完全定格，禁止一切循环动画（脉冲、呼吸、无限滚动、循环高亮）；报纸不动，只有读者在动
- 入场编排: **无 stagger，整版同现**——全部图表 500ms ease-out 同时入场，像摊开一份已排版完成的报纸；禁止弹跳/弹性曲线
- 展开/收起: **200ms ease-in-out**
- 数字滚动: **700ms ease-out**

## Layout & Grid

| 属性 | 值 |
|------|-----|
| 页面最大宽度 | 1920px |
| 网格系统 | CSS Grid 12 列，内容驱动 |
| 卡片间距 | 20px |
| 页面内边距 | 28px |
| 图表容器最小高度 | 280px |
| 对齐方式 | 全左对齐（报纸栏式，禁止居中排版） |

## Component Specifications

### KPI 卡片
- 白底 `--bg-card` + 1px `--border-subtle`，圆角 4px，内边距 18px 20px
- **标签在上**: 13px `--text-secondary`，数字下方留 6px
- **数字**: 40px 700 Playfair Display, `--text-primary`，左对齐，tabular-nums
- **单位降级**: 单位/量级（万、%）降为 14px `--text-secondary`，与数字基线对齐
- **趋势**: 12px 带 ↑↓ 箭头，涨 success、跌 danger，与标签同行右侧
- **悬停**: 整卡背景变 `--bg-hover`，无阴影变化

### 图表容器
- 白底 + 1px 细边框，圆角 4px，内边距 20px
- 标题: 16px 600 Playfair Display 左对齐（结论句），下方可有一行 13px `--text-secondary` 副题
- 图表区: ECharts 浅色主题（容器背景透明），四周留白 ≥16px
- 卡片右下角可放 12px `--text-muted` 来源注（Source: …）
- 无任何装饰条、角标、光效

### 按钮
- 主按钮: `--accent-primary` 纯色，白字，圆角 3px，内边距 8px 16px，14px 500
- 次按钮: 白底 + `--border-subtle` 边框，`--text-primary` 文字
- 悬停: 主按钮明度降 10%；次按钮背景变 `--bg-hover`
- 禁用: 40% 透明度

### 数据表格
- 报纸表格风: 无纵向边框，仅 1px `--border-subtle` 行分隔线
- 表头: 12px 600 `--text-secondary`，背景透明，行高 32px，底部 2px `--text-primary` 墨线
- 数据行: 行高 36px 白底，悬停整行 `--bg-hover`
- 数字列右对齐用 mono；首列可用 10px 深红/灰色圆点作分类标签

### 页头
- 透明背景融入页面，底部 2px `--text-primary` 墨黑分隔线（报纸刊头线），其上无装饰
- 标题: 30px 700 Playfair Display, `--text-primary`，左对齐；刊名可加 1px 深红小字 kicker
- 时间/副标题: 13px `--text-muted`，标题下方

### 进度条
- 高度 4px，圆角 2px，轨道 `--border-subtle`
- 填充 `--accent-primary` 纯色，无渐变
- 百分比标注 12px `--text-muted`，置于右侧

## Chart Color Palette
系列色: #A23E48, #1a1a1a, #5f5f5a, #9b9a93, #c9c8c0

## Chart Fingerprint
- **末端标注**: 折线/柱状一律用 endLabel 替代图例——最后一数据点右侧直接写系列名+终值，12px 取系列色；**禁止传统图例**
- **参考线**: 必配 markLine——均值用 1px 虚线 `--text-muted`，目标/阈值用 1px 实线 `--accent-primary`，线端写 12px 注释文字（如"近五年均值"）
- **折线**: 线宽 2.5px 纯色；symbol: none 不显示数据点，hover 时才出现 6px 圆点+白描边；面积渐变只给主系列（深红 15% → 0 自上而下），其余系列禁止填充
- **柱形**: 仅上圆角 [2,2,0,0]；纯色无渐变；仅主系列深红，其余灰阶；hover 柱体明度降 15%
- **阈值染色**: 超过目标/警戒线的柱体或数据段染 `--accent-primary`，其余保持灰阶——一眼定位"出格"数据
- **饼/环**: 只做环形 radius ['55%','75%']；扇区间 2px 白色分隔；主扇区深红其余灰阶；中心用 IBM Plex Mono 无衬线显示总数——衬线环心总数是 claude 的独占签名，本主题禁用（衬线只出现在标题与 KPI 数字）
- **网格线**: 只留水平 1px 实线 `--border-subtle`（极浅）——**全库最"印刷感"的网格签名：数据新闻的网格是印出来的实线，不是发光的虚线**；纵向网格线和坐标轴线一律删除
- **Tooltip**: 白底 + 1px `--border-subtle` 细边框 + `0 4px 12px rgba(26,26,26,0.10)`，文字 `--text-primary`，无彩色边框
- **允许**: 结论式标题、markLine 注释、endLabel、单红主导 + 灰阶、图表内大留白
- **禁止**: 一切渐变（主系列面积渐变除外）、发光、图例、纵向网格线、深色 Tooltip、多色系列

## Do's and Don'ts
✅ 页头标题与面板标题用衬线体，标题写结论句（"碳排放十年首降"而非"碳排放统计"）
✅ 深红是稀缺资源：一屏 ≤3 处红色元素，留给最重要的数据
✅ 每张图配 markLine 参考线并写注释，让读者立刻知道"多少算好"
✅ 卡片角落放来源注（Source: …），建立新闻公信力
❌ 不要把面板标题居中或做成科技风徽章——报纸是全左对齐的
❌ 不要给图表加图例——endLabel 末端标注是本主题指纹
❌ 不要让图表撑满面板——四周留白 ≥16px

## Token Schema

| Token | 值 | 说明 |
|--------|----|------|
| `--radius-card` | `4px` | 卡片圆角（接近直角的印刷感） |
| `--radius-button` | `3px` | 按钮圆角 |
| `--radius-panel` | `4px` | 面板圆角 |
| `--font-family-base` | `"Inter", -apple-system, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif` | 正文（无衬线，带系统 fallback） |
| `--font-family-display` | `"Playfair Display", "Lora", Georgia, "Songti SC", serif` | 标题/KPI 数字（衬线，双字体） |
| `--font-family-mono` | `"IBM Plex Mono", ui-monospace, Consolas, monospace` | 数字/代码 |
| `--font-size-display` | `30px` | 页头标题 |
| `--font-size-title` | `16px` | 面板标题 |
| `--font-size-kpi` | `40px` | KPI 大数字 |
| `--shadow-card` | `0 1px 2px rgba(26,26,26,0.05)` | 卡片阴影 |
| `--glow-accent` | `none` | 本主题无发光 |
| `--decoration` | `flat` | 纯平：无渐变、无发光 |
| `--bg-pattern` | `hatch` | 页面层报纸网点斜纹（印刷网屏感；noise 已让给 notion，dots 归 claude） |
| `--pattern-color` | `rgba(0,0,0,0.03)` | 墨黑 3% 透明（比 posthog 的 0.05 蓝墨 hatch 更淡、更冷，参数与色温互斥区分） |
| `--kpi-variant` | `plain` | KPI 纯大数字 + 单位降级 |
