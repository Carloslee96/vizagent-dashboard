"""散点图 builder。"""

from __future__ import annotations

import json
from typing import Any

from vizagent_dashboard.compiler.charts._common import ChartContext, _clean_number


class ScatterBuilder:
    data_hints = ("correlation",)

    def build(self, ctx: ChartContext) -> str:
        base: dict[str, Any] = ctx.base
        if len(ctx.y_fields) < 2:
            return json.dumps(base)
        scatter_data = [[_clean_number(row.get(ctx.y_fields[0])), _clean_number(row.get(ctx.y_fields[1]))]
                        for row in ctx.data
                        if _clean_number(row.get(ctx.y_fields[0])) is not None and _clean_number(row.get(ctx.y_fields[1])) is not None]
        if not scatter_data:
            return json.dumps(base)
        base.update({
            "grid": {"top": "16%", "bottom": "10%", "left": "8%", "right": "8%", "containLabel": True},
            "xAxis": {"type": "value", "name": ctx.y_fields[0],
                      "axisLine": {"lineStyle": {"color": ctx.colors["grid_color"]}},
                      "axisLabel": {"color": ctx.colors["ax_color"], "fontSize": 10},
                      "splitLine": {"lineStyle": {"color": ctx.colors["grid_color"], "type": "dashed"}}},
            "yAxis": {"type": "value", "name": ctx.y_fields[1],
                      "axisLine": {"lineStyle": {"color": ctx.colors["grid_color"]}},
                      "axisLabel": {"color": ctx.colors["ax_color"], "fontSize": 10},
                      "splitLine": {"lineStyle": {"color": ctx.colors["grid_color"], "type": "dashed"}}},
            "series": [{
                "type": "scatter", "data": scatter_data,
                "symbolSize": 12,
                "itemStyle": {"color": ctx.palette[0], "opacity": 0.7},
                "emphasis": {"focus": "self"},
            }],
        })
        return json.dumps(base, ensure_ascii=False)
