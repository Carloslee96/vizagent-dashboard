"""折线 / 面积图 builder。"""

from __future__ import annotations

import json
from typing import Any

from vizagent_dashboard.compiler.charts._common import ChartContext, _clean_number


class LineBuilder:
    """处理 line 与 area（area 在 line 基础上追加 areaStyle）。"""

    def build(self, ctx: ChartContext) -> str:
        base: dict[str, Any] = ctx.base
        valid_y = [y for y in ctx.y_fields if any(_clean_number(row.get(y)) is not None for row in ctx.data)]
        if not valid_y:
            return json.dumps(base)
        base.update({
            "grid": {"top": "18%", "bottom": "10%", "left": "5%", "right": "7%", "containLabel": True},
            "xAxis": {"type": "category", "name": ctx.x_field, "boundaryGap": False, "data": ctx.categories,
                      "axisLine": {"lineStyle": {"color": ctx.colors["grid_color"]}},
                      "axisLabel": {"color": ctx.colors["ax_color"], "fontSize": 10}},
            "yAxis": {"type": "value", "name": " / ".join(valid_y),
                      "axisLine": {"lineStyle": {"color": ctx.colors["grid_color"]}},
                      "axisLabel": {"color": ctx.colors["ax_color"], "fontSize": 10},
                      "splitLine": {"lineStyle": {"color": ctx.colors["grid_color"], "type": "dashed"}}},
            "legend": {"show": len(valid_y) > 1, "top": 0, "right": 0, "textStyle": {"color": ctx.colors["ax_color"], "fontSize": 10}},
            "series": [],
        })
        for idx, metric in enumerate(valid_y):
            values = [_clean_number(row.get(metric)) for row in ctx.data]
            series: dict[str, Any] = {
                "name": metric, "type": "line", "data": values,
                "smooth": True, "showSymbol": False, "connectNulls": False,
                "lineStyle": {"width": 2, "color": ctx.palette[idx % len(ctx.palette)]},
                "itemStyle": {"color": ctx.palette[idx % len(ctx.palette)]},
                "emphasis": {"focus": "series"},
            }
            if ctx.chart_type == "area":
                series["areaStyle"] = {"opacity": 0.14}
            base["series"].append(series)
        return json.dumps(base, ensure_ascii=False)
