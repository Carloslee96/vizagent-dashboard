"""矩形树图 builder（占比/构成类，面积反映数值）。"""

from __future__ import annotations

import json
from typing import Any

from vizagent_dashboard.compiler.charts._common import ChartContext, _clean_number


class TreemapBuilder:
    data_hints = ("composition",)

    def build(self, ctx: ChartContext) -> str:
        base: dict[str, Any] = ctx.base
        if not ctx.y_fields:
            return json.dumps(base)
        metric = ctx.y_fields[0]
        data = [
            {"name": cat, "value": _clean_number(row.get(metric))}
            for cat, row in zip(ctx.categories, ctx.data)
            if _clean_number(row.get(metric)) is not None
        ]
        if not data:
            return json.dumps(base)
        base["tooltip"] = {"trigger": "item", "backgroundColor": ctx.colors["tooltip_bg"],
                           "borderColor": ctx.colors["grid_color"],
                           "textStyle": {"color": ctx.colors["tooltip_text"], "fontSize": 12}}
        base["series"] = [{
            "name": metric,
            "type": "treemap",
            "roam": False,
            "breadcrumb": {"show": False},
            "label": {"show": True, "formatter": "{b}\n{c}", "fontSize": 10, "color": ctx.colors["tooltip_text"]},
            "upperLabel": {"show": False},
            "itemStyle": {"borderColor": ctx.colors["grid_color"], "borderWidth": 1},
            "data": data,
        }]
        return json.dumps(base, ensure_ascii=False)
