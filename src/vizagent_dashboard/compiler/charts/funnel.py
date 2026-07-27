"""漏斗图 builder（转化/阶段类，从大到小堆叠）。"""

from __future__ import annotations

import json
from typing import Any

from vizagent_dashboard.compiler.charts._common import ChartContext, _clean_number


class FunnelBuilder:
    data_hints = ("composition",)

    def build(self, ctx: ChartContext) -> str:
        base: dict[str, Any] = ctx.base
        if not ctx.y_fields:
            return json.dumps(base)
        metric = ctx.y_fields[0]
        funnel_data = [
            {"name": cat, "value": _clean_number(row.get(metric))}
            for cat, row in zip(ctx.categories, ctx.data)
            if _clean_number(row.get(metric)) is not None
        ]
        if not funnel_data:
            return json.dumps(base)
        base["legend"] = {"type": "scroll", "top": 0, "right": 0, "textStyle": {"color": ctx.colors["ax_color"], "fontSize": 10}}
        base["series"] = [{
            "name": metric,
            "type": "funnel",
            "left": "10%",
            "width": "80%",
            "minSize": "12%",
            "sort": "descending",
            "label": {"show": True, "color": ctx.colors["ax_color"], "fontSize": 10, "formatter": "{b} {c}"},
            "labelLine": {"show": False},
            "itemStyle": {"borderColor": ctx.colors["grid_color"], "borderWidth": 1},
            "emphasis": {"focus": "self"},
            "data": funnel_data,
        }]
        return json.dumps(base, ensure_ascii=False)
