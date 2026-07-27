"""柱状图 builder。"""

from __future__ import annotations

import json
import re
from typing import Any

from vizagent_dashboard.compiler.charts._common import ChartContext, _clean_number


class BarBuilder:
    data_hints = ("comparison",)

    def build(self, ctx: ChartContext) -> str:
        base: dict[str, Any] = ctx.base
        valid_y = [y for y in ctx.y_fields if any(_clean_number(row.get(y)) is not None for row in ctx.data)]
        if not valid_y:
            return json.dumps(base)
        horizontal = len(ctx.data) > 8 or bool(re.search(r"排名|排行|偏好|分布", ctx.title))
        if horizontal:
            base["xAxis"] = {"type": "value", "name": " / ".join(valid_y),
                             "axisLine": {"lineStyle": {"color": ctx.colors["grid_color"]}},
                             "axisLabel": {"color": ctx.colors["ax_color"], "fontSize": 10},
                             "splitLine": {"lineStyle": {"color": ctx.colors["grid_color"], "type": "dashed"}}}
            base["yAxis"] = {"type": "category", "name": ctx.x_field, "data": ctx.categories,
                             "inverse": True,
                             "axisLine": {"lineStyle": {"color": ctx.colors["grid_color"]}},
                             "axisLabel": {"color": ctx.colors["ax_color"], "fontSize": 9, "interval": 0}}
            base["grid"] = {"top": "14%", "bottom": "8%", "left": "5%", "right": "10%", "containLabel": True}
            bar_pos = "right"
        else:
            base["xAxis"] = {"type": "category", "name": ctx.x_field, "data": ctx.categories,
                             "axisLine": {"lineStyle": {"color": ctx.colors["grid_color"]}},
                             "axisLabel": {"color": ctx.colors["ax_color"], "fontSize": 10,
                                           "interval": 0, "rotate": 25 if any(len(c) > 5 for c in ctx.categories) else 0}}
            base["yAxis"] = {"type": "value", "name": " / ".join(valid_y),
                             "axisLine": {"lineStyle": {"color": ctx.colors["grid_color"]}},
                             "axisLabel": {"color": ctx.colors["ax_color"], "fontSize": 10},
                             "splitLine": {"lineStyle": {"color": ctx.colors["grid_color"], "type": "dashed"}}}
            base["grid"] = {"top": "16%", "bottom": "10%", "left": "5%", "right": "6%", "containLabel": True}
            bar_pos = "top"
        base["legend"] = {"show": len(valid_y) > 1, "top": 0, "right": 0, "textStyle": {"color": ctx.colors["ax_color"], "fontSize": 10}}
        base["series"] = [
            {
                "name": metric, "type": "bar",
                "data": [_clean_number(row.get(metric)) for row in ctx.data],
                "barMaxWidth": 24,
                "itemStyle": {"color": ctx.palette[idx % len(ctx.palette)],
                              "borderRadius": [0, 3, 3, 0] if horizontal else [3, 3, 0, 0]},
                "label": {"show": True, "position": bar_pos, "color": ctx.colors["ax_color"], "fontSize": 9},
                "emphasis": {"focus": "series"},
            }
            for idx, metric in enumerate(valid_y)
        ]
        return json.dumps(base, ensure_ascii=False)
