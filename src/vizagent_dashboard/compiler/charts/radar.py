"""雷达图 builder（多指标对比，每字段一个维度）。"""

from __future__ import annotations

import json
from typing import Any

from vizagent_dashboard.compiler.charts._common import ChartContext, _clean_number


class RadarBuilder:
    data_hints = ("multivariate",)

    def build(self, ctx: ChartContext) -> str:
        base: dict[str, Any] = ctx.base
        if len(ctx.y_fields) < 2:
            return json.dumps(base)
        # 每个指标维度的最大值（取数据中该字段最大值，至少 1）
        indicators = []
        for field in ctx.y_fields:
            field_values = [_clean_number(row.get(field)) for row in ctx.data]
            field_values = [v for v in field_values if v is not None]
            indicators.append({"name": field, "max": max(field_values) if field_values else 1})
        # 每个 x 类别一条雷达数据
        radar_data = [
            {
                "name": cat,
                "value": [_clean_number(row.get(field)) for field in ctx.y_fields],
            }
            for cat, row in zip(ctx.categories, ctx.data)
        ]
        if not radar_data:
            return json.dumps(base)
        base["tooltip"] = {"trigger": "item", "backgroundColor": ctx.colors["tooltip_bg"],
                           "borderColor": ctx.colors["grid_color"],
                           "textStyle": {"color": ctx.colors["tooltip_text"], "fontSize": 12}}
        base["legend"] = {"show": len(radar_data) > 1, "top": 0, "right": 0,
                          "textStyle": {"color": ctx.colors["ax_color"], "fontSize": 10}}
        base["radar"] = {
            "indicator": indicators,
            "radius": "62%",
            "axisName": {"color": ctx.colors["ax_color"], "fontSize": 10},
            "splitLine": {"lineStyle": {"color": ctx.colors["grid_color"]}},
            "splitArea": {"show": False},
            "axisLine": {"lineStyle": {"color": ctx.colors["grid_color"]}},
        }
        base["series"] = [{
            "type": "radar",
            "data": radar_data,
            "areaStyle": {"opacity": 0.14},
            "lineStyle": {"width": 2},
            "emphasis": {"focus": "self"},
        }]
        return json.dumps(base, ensure_ascii=False)
