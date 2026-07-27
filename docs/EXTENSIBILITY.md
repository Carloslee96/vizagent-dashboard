# 可扩展架构方案：主题与图表类型的插件化

> 状态：设计稿，待实施。创建于 2026-07-27。
> 目标：让增减 UI 主题和图表类型变成「丢文件 / 加模块」，不必改核心编译逻辑。

## 背景

skill 当前只暴露 5 个 clean-room 主题和 8 种图表类型，但：
- SaaS `viz-agent-team/backend/agents/design-systems/` 下有 **23 个品牌名主题**（airbnb/apple/claude/figma/spotify…），因版权顾虑未引入 skill。
- SaaS `chart_options.py` 支持约 16 种 skill 没有的图表（radar/funnel/gauge/treemap/heatmap/sankey/boxplot/wordcloud/nightingale/bullet/waterfall/calendar/pictorial/parallel/chord/stream 等）。

要把这两批存量低成本接入，且未来能灵活增减，需要先把扩展骨架立起来。

## 现状与痛点（探查结论）

### 主题链路
- 25 个主题是 `src/vizagent_dashboard/assets/*.md`（token 表格 + Chart Palette）：5 原创 + 20 P1 去品牌引入（详见 `docs/THEME_AUDIT.md`）。
- `compiler/themes.py`：`THEME_IDS` 硬编码 tuple + `ALIASES` dict + `resolve_theme_id()` + `list_themes()`。
- `compiler/skeleton.py:parse_design_tokens()` 解析 md 表格 → css_vars + palette；`build_css_block()` 生成 CSS。
- `compiler/chart_options.py:_chart_colors_from_vars()` 把主题色注入 ECharts。
- `schemas/dashboard_spec.py`：`theme: str = "midnight-ops"`。
- **痛点**：加主题要改 `THEME_IDS` + manifest + schema，三处。

### 图表类型链路
- `ChartType` 枚举 8 种（line/bar/pie/scatter/map_china/map_world/kpi/table），`schemas/dashboard_spec.py`。
- `chart_options.py:build_chart_option()` 是大 if/elif 分发（pie / line,area / bar / scatter…）。
- `skeleton.py` 编译循环对 kpi、map_china、map_world 有 special-case 分支。
- `planner/heuristic.py`：`_explicit_chart_type()` 关键词匹配 + 自动推断（日期→line、占比→pie、else→bar）。
- **痛点**：加图表类型要改 `build_chart_option` 核心 + 枚举 + planner，耦合深。

## 设计目标

| 目标 | 衡量标准 |
|---|---|
| 加新主题 | 只丢一个数据文件，零代码改动 |
| 加新图表类型 | 只加一个独立模块 + 一行注册，不动编译主循环 |
| 删主题/图表 | 删文件即可，无残留依赖 |
| 第三方扩展（可选） | 用户/插件包能加自己的主题和图表，不必 fork |
| 向后兼容 | 现有 DashboardSpec（midnight-ops / line 等）行为不变 |

核心思想：**把主题和图表类型从「硬编码枚举 + if/elif 分发」改成「数据/模块自描述 + 注册表分发」**。编译器只认接口，不认具体类型。

---

## 一、主题扩展方案

### 1.1 主题自描述：加 frontmatter

把 `assets/*.md` 升级为带 frontmatter 的自描述文件，元数据由文件自己声明：

```markdown
---
id: paper-light
name: 纸张浅色
aliases: [paper-brief, paper-linen, minimal-doc]   # 旧别名自声明
decoration: flat                                     # flat/gradient/glow/glass
base: light                                          # light/dark，供 fallback 判断
---

## Color Palette
| Token | Value | Purpose |
| --bg-canvas | `#FAF8F3` | 页面背景 |
...

## Chart Palette
`#2D3142` `#4F6D7A` `#C0D6DF` ...
```

### 1.2 注册表自动发现，干掉 THEME_IDS

`themes.py` 不再硬编码 `THEME_IDS`，改成扫描目录：

```
list_themes()          → 扫 assets/themes/*.md + ~/.vizagent/themes/*.md
                        解析 frontmatter → 返回 [{id, name, aliases, ...}]
resolve_theme_id(key)  → 遍历所有主题的 id 和 aliases 匹配
```

**加主题 = 丢一个 .md 文件**，`themes.py` / schema / manifest 都不改。`ALIASES` dict 退役——别名由各主题 frontmatter 自声明，分散到各文件，SSOT。

### 1.3 用户级主题目录（可选，低成本）

加载顺序：包内 `assets/themes/` → 用户 `~/.vizagent/themes/`（后者覆盖同名前者）。`--theme-dir <path>` CLI 参数支持项目级覆盖。用户/团队可放自己品牌主题，不 fork。

### 1.4 存量 23 个品牌主题的引入流水线

一次性脚本 `tools/import_saas_themes.py`，把 SaaS `design-systems/*.md` 去品牌后倒入 `assets/themes/`：

```
SaaS airbnb.md  →  去品牌  →  assets/themes/warm-stay.md
SaaS apple.md   →  去品牌  →  assets/themes/clean-glass.md
SaaS spotify.md →  去品牌  →  assets/themes/vibe-green.md
```

**去品牌 checklist**（脚本自动 + 人工复核）：
1. 文件名和 `id`/`name` 改成通用词，不含品牌名。
2. 删 Logo、品牌专属文案、品牌专有色名（"Spotify Green"→"signal-green"）。
3. 保留纯 token 数值（颜色 hex、字号、圆角——事实数据，不构成版权）。
4. 跑 `docs/THEME_AUDIT.md` 审计脚本扫残留品牌词。

跑完得到 ~20 个去品牌主题，自动被注册表发现。颜色 hex 本身不受版权保护，品牌名/Logo/专属文案有风险——去品牌后纯 token 安全。

---

## 二、图表类型扩展方案

### 2.1 Builder 接口：每个图表类型一个自描述模块

```python
class ChartBuilder(Protocol):
    chart_type: str                    # "radar"
    data_hints: tuple[str, ...]        # ("multivariate",) 供 planner 匹配数据形态
    required_assets: dict              # {"map": "china"} 需预注册的 GeoJSON，可空

    def build(self, item, rows, ctx) -> dict:
        """返回 ECharts option dict。ctx 含 css_vars/palette/tooltip 样式。"""
```

每个类型一个文件：`charts/line.py`、`charts/radar.py`、`charts/map_china.py`…各自封装 ECharts option 构造逻辑。

### 2.2 注册表取代 if/elif

`charts/__init__.py` 显式注册（import 即注册）：

```python
from .line import LineBuilder
from .bar import BarBuilder
from .radar import RadarBuilder
...
CHART_BUILDERS: dict[str, ChartBuilder] = {
    b.chart_type: b for b in [LineBuilder(), BarBuilder(), RadarBuilder(), ...]
}
```

`build_chart_option()` 从大 if/elif 收敛成一行分发：

```python
def build_chart_option(chart_type, ...):
    builder = CHART_BUILDERS.get(chart_type)
    if builder is None:
        raise UnknownChartType(chart_type, known=sorted(CHART_BUILDERS))
    return builder.build(item, rows, ctx)
```

**加图表类型 = 新建 builder 文件 + 注册表加一行**，`build_chart_option` 和编译主循环永不触碰。

### 2.3 统一编译循环，干掉 special-case

`skeleton.py` 现在对 kpi / map_china / map_world 有特殊分支。统一成：

```python
for item in row.items:
    builder = CHART_BUILDERS[item.chart_type]
    for kind, mid in builder.required_assets.items():
        ensure_asset(kind, mid)          # 注册 china/world 地图，只注册一次
    option = builder.build(item, rows, ctx)
```

kpi、map_china、map_world 各自实现 ChartBuilder 接口，特殊逻辑封装在各自 builder 里。编译循环对任何图表类型一视同仁。

### 2.4 Schema：枚举 → 注册表校验

`ChartType` 枚举退役，改成字符串 + 运行时注册表校验：

```python
class ChartItem(BaseModel):
    chart_type: str
    @field_validator("chart_type")
    def _known(cls, v):
        if v not in CHART_BUILDERS: raise ValueError(unknown...)
        return v
```

向后兼容：现有 `line`/`bar`/`pie` 等只是预注册的 builder，行为不变。

### 2.5 Planner 用 data_hints 自动选型

`heuristic.py` 现在硬编码「日期→line、占比→pie」。改成查 builder 的 `data_hints`：

```
builder.data_hints 含 "time_series"   →  时间字段命中时候选
builder.data_hints 含 "composition"   →  占比字段命中时候选
builder.data_hints 含 "geography"     →  地理字段命中时候选
```

新图表类型只要在 builder 里声明 hints，planner 自动会选它，不用改 planner 代码。`--requirement` 关键词匹配（"只要雷达图"）也走同一张 hints 表。

### 2.6 SaaS 图表类型分批迁入

SaaS `chart_options.py` 每个 if/elif 分支是现成的 ECharts option 逻辑，迁入 = 抽成 builder。按复杂度分批：

| 批次 | 类型 | 难度 | 说明 |
|---|---|---|---|
| P1 | area / gauge / funnel / radar | 低 | 单 series，ECharts 原生，逻辑短 |
| P2 | heatmap / treemap / boxplot / nightingale | 中 | 数据需聚合/分箱 |
| P3 | sankey / chord / parallel / graph | 中高 | 多字段绑定，数据形态特殊 |
| P4 | wordcloud / calendar / pictorial / themeRiver | 高 | 需额外 ECharts 扩展或特殊数据预处理 |

每批独立 builder，互不影响，可随时停。先做 P1 立刻多 4 种图表，收益最大。

---

## 三、关键取舍

| 决策点 | 选项 A（推荐） | 选项 B |
|---|---|---|
| 主题发现 | 自动扫目录（加文件即用，错误运行时暴露） | 显式注册列表（import 时校验，加文件改一行） |
| 图表注册 | 显式注册表（代码 import 时检查） | entry_points 自动发现（支持第三方插件包，更复杂） |
| ChartType | `Literal` 内置 + 注册表校验（有补全又能扩展） | 纯字符串 + 注册表（最灵活，无补全） |
| 23 个 SaaS 主题 | 去品牌后全量引入（主题丰富） | 只留 5 个 clean-room（最安全，不扩） |
| 装饰系统 | 暂不引入（skill 无 LLM，装饰是 SaaS 能力） | 用模板化 SVG 替代 LLM 装饰（额外工作） |

**推荐组合**：主题自动发现 + 图表显式注册 + `Literal`+注册表 + SaaS 主题去品牌引入 + 装饰暂不做。

---

## 四、分阶段实施计划

| 阶段 | 内容 | 验证 | 工作量 |
|---|---|---|---|
| **P0 主题注册表** | themes.py 改自动发现 + frontmatter + 别名自声明；5 个现有主题加 frontmatter | 现有 5 主题行为不变，测试全绿 | 中 |
| **P1 主题引入** | `import_saas_themes.py` 去品牌脚本 + 审计；导入 ~20 主题 | THEME_AUDIT 无品牌残留，全部可切换 | 中 |
| **P2 图表注册表** | ChartBuilder 接口 + 注册表 + `build_chart_option` 收敛为分发；现有 8 类型逐一抽成 builder（含 kpi/map special-case 统一） | 现有图表输出字节级不变（回归测试） | 大 |
| **P3 Planner 解耦** | heuristic.py 改用 data_hints 选型 | 自动选型测试覆盖各 hint | 小 |
| **P4 SaaS 图表迁入** | P1 批（area/gauge/funnel/radar）先上 | 新类型可 build 可 validate | 中 |
| **P5 用户主题目录** | `~/.vizagent/themes/` + `--theme-dir` | 用户主题能覆盖包内 | 小 |

**P0 + P2 是地基**（不做的话后面每加一个都要改核心）。建议先做 P0 + P2 立扩展骨架，再按需灌主题和图表。

---

## 五、最终效果

```bash
# 加主题：丢文件
cp my-brand.md skill/src/vizagent_dashboard/assets/themes/my-brand.md
vizagent build --data x.xlsx --theme my-brand    # 立即可用

# 加图表类型：加 builder + 注册一行
# skill/src/vizagent_dashboard/charts/radar.py  →  RadarBuilder
# charts/__init__.py 注册表加一行
vizagent build --data x.xlsx --requirement "用雷达图"   # 立即可用
```

核心编译器、schema、planner 都不动——这就是「不用重新开发核心逻辑」。

---

## 附录：关键文件位置（实施时参考）

- 主题数据：`src/vizagent_dashboard/assets/*.md`（将迁至 `assets/themes/`）
- 主题注册：`src/vizagent_dashboard/compiler/themes.py`（`THEME_IDS` / `ALIASES` / `resolve_theme_id` / `list_themes`）
- 主题解析：`src/vizagent_dashboard/compiler/skeleton.py`（`parse_design_tokens` / `build_css_block`）
- 主题色注入：`src/vizagent_dashboard/compiler/chart_options.py`（`_chart_colors_from_vars`）
- 图表枚举：`src/vizagent_dashboard/schemas/dashboard_spec.py`（`ChartType`）
- 图表分发：`src/vizagent_dashboard/compiler/chart_options.py`（`build_chart_option` if/elif）
- 编译循环：`src/vizagent_dashboard/compiler/skeleton.py`（`compile_artifacts`，kpi/map special-case）
- Planner：`src/vizagent_dashboard/planner/heuristic.py`（`_explicit_chart_type` + 自动推断）
- SaaS 存量主题源：`viz-agent-team/backend/agents/design-systems/*.md`（23 个品牌名）
- SaaS 存量图表逻辑：`viz-agent-team/backend/agents/chart_options.py`
- 主题审计：`docs/THEME_AUDIT.md`
