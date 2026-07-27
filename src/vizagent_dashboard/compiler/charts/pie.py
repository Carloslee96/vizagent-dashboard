"""饼图 builder。"""

from __future__ import annotations

import json
from typing import Any

from vizagent_dashboard.compiler.charts._common import ChartContext, _clean_number


class PieBuilder:
    data_hints = ("composition",)

    def build(self, ctx: ChartContext) -> str:
        base: dict[str, Any] = ctx.base
        if not ctx.y_fields:
            return json.dumps(base)
        metric = ctx.y_fields[0]
        pie_data = [
            {"name": cat, "value": _clean_number(row.get(metric))}
            for cat, row in zip(ctx.categories, ctx.data)
            if _clean_number(row.get(metric)) is not None
        ]
        if not pie_data:
            return json.dumps(base)
        base["legend"] = {"type": "scroll", "top": 0, "right": 0, "textStyle": {"color": ctx.colors["ax_color"], "fontSize": 10}}
        base["series"] = [{
            "name": metric,
            "type": "pie",
            "radius": ["28%", "68%"],
            "center": ["45%", "56%"],
            "startAngle": 90,
            "avoidLabelOverlap": True,
            "label": {"show": True, "color": ctx.colors["ax_color"], "fontSize": 10, "formatter": "{b} {c}"},
            "labelLine": {"length": 8, "length2": 6},
            "emphasis": {"scale": True, "scaleSize": 6, "focus": "self"},
            "data": pie_data,
        }]
        return json.dumps(base, ensure_ascii=False)
