"""图表类型注册表 + build_chart_option 分发器。

新增图表类型：写一个 ``charts/<type>.py`` 实现 ``ChartBuilder.build(ctx)``，
在 ``CHART_BUILDERS`` 注册一行即可；``compiler/chart_options.py`` 的 facade、
``skeleton.py`` 的编译循环都无需改动（非 kpi/table/map 类型自动走 build_chart_option）。
"""

from __future__ import annotations

import json
import logging
from typing import Any, Protocol

from vizagent_dashboard.compiler.charts._common import ChartContext, _chart_colors_from_vars
from vizagent_dashboard.compiler.charts.bar import BarBuilder
from vizagent_dashboard.compiler.charts.funnel import FunnelBuilder
from vizagent_dashboard.compiler.charts.line import LineBuilder
from vizagent_dashboard.compiler.charts.nightingale import NightingaleBuilder
from vizagent_dashboard.compiler.charts.pie import PieBuilder
from vizagent_dashboard.compiler.charts.scatter import ScatterBuilder
from vizagent_dashboard.compiler.charts.treemap import TreemapBuilder

logger = logging.getLogger(__name__)

_DEFAULT_PALETTE = ["#2D5BFF", "#5B8AFF", "#8AAEFF", "#B4CCFF", "#3DAB63"]


class ChartBuilder(Protocol):
    """单个图表类型的 ECharts option 构造器。"""

    data_hints: tuple[str, ...]
    """数据形态提示，供 planner 选型匹配（如 time_series/composition/comparison/correlation）。"""

    def build(self, ctx: ChartContext) -> str:
        """返回 ECharts option JSON 字符串。"""
        ...


# 显式注册表：chart_type → builder。line/area 共用 LineBuilder。
# 约定：同一 data_hints 的「默认类型」先注册——select_chart_type_by_hint 按注册顺序
# 取第一个匹配者，因此 time_series 默认命中 line（早于 area）、composition 默认命中 pie。
_line_builder = LineBuilder()
CHART_BUILDERS: dict[str, ChartBuilder] = {
    "line": _line_builder,
    "area": _line_builder,
    "bar": BarBuilder(),
    "pie": PieBuilder(),
    "nightingale": NightingaleBuilder(),
    "treemap": TreemapBuilder(),
    "funnel": FunnelBuilder(),
    "scatter": ScatterBuilder(),
}


def select_chart_type_by_hint(hint: str) -> str:
    """按 data_hints 选型：返回第一个（注册顺序）含该 hint 的 chart_type，无匹配返回空串。"""
    for chart_type, builder in CHART_BUILDERS.items():
        if hint in getattr(builder, "data_hints", ()):
            return chart_type
    return ""


def build_chart_option(
    chart_type: str,
    title: str,
    data: list[dict],
    x_field: str,
    y_field: str | list[str],
    chart_palette: list[str] | None = None,
    css_vars: dict[str, str] | None = None,
) -> str:
    """根据图表类型和数据生成 ECharts option JSON（确定性，零 LLM 调用）。

    未知类型回退到柱状图（保留历史契约）。
    """
    if not data:
        logger.warning(f"build_chart_option: empty data for chart '{title}'")
        return json.dumps({"title": {"text": title}})

    palette = chart_palette or _DEFAULT_PALETTE
    colors = _chart_colors_from_vars(css_vars)
    chart_type = chart_type.lower().replace("map:", "map")
    y_fields = [y_field] if isinstance(y_field, str) else y_field

    categories = [
        str(row.get(x_field, "")).strip() or f"第{idx + 1}项"
        for idx, row in enumerate(data)
    ]

    base: dict[str, Any] = {
        "backgroundColor": "transparent",
        "color": palette,
        "animationDuration": 600,
        "animationEasing": "cubicOut",
        "title": {"text": title, "left": "left", "textStyle": {"color": colors["tooltip_text"], "fontSize": 14, "fontWeight": "normal"}},
        "tooltip": {
            "trigger": "axis" if chart_type in {"line", "area", "bar"} else "item",
            "backgroundColor": colors["tooltip_bg"],
            "borderColor": colors["grid_color"],
            "textStyle": {"color": colors["tooltip_text"], "fontSize": 12},
        },
    }

    builder = CHART_BUILDERS.get(chart_type)
    if builder is None:
        # 未知类型回退到柱状图（与历史行为一致）
        return build_chart_option(
            chart_type="bar", title=title, data=data, x_field=x_field, y_field=y_fields,
            chart_palette=chart_palette, css_vars=css_vars,
        )

    ctx = ChartContext(
        chart_type=chart_type,
        title=title,
        data=data,
        x_field=x_field,
        y_fields=y_fields,
        palette=palette,
        colors=colors,
        base=base,
        categories=categories,
    )
    return builder.build(ctx)
