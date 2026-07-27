"""仪表盘 builder（单值进度，灰底 + 彩色进度填充）。"""

from __future__ import annotations

import json
from typing import Any

from vizagent_dashboard.compiler.charts._common import ChartContext, _clean_number


class GaugeBuilder:
    data_hints = ("single_metric",)

    def build(self, ctx: ChartContext) -> str:
        base: dict[str, Any] = ctx.base
        if not ctx.y_fields:
            return json.dumps(base)
        metric = ctx.y_fields[0]
        values = [_clean_number(row.get(metric)) for row in ctx.data]
        values = [v for v in values if v is not None]
        if not values:
            return json.dumps(base)
        value = sum(values)
        # 百分比类（≤100）按 0-100 量程；否则量程上限取 max(100, value)
        gauge_max = max(100, value)
        base["tooltip"] = {"trigger": "item", "backgroundColor": ctx.colors["tooltip_bg"],
                           "borderColor": ctx.colors["grid_color"],
                           "textStyle": {"color": ctx.colors["tooltip_text"], "fontSize": 12}}
        base["series"] = [{
            "type": "gauge",
            "min": 0,
            "max": gauge_max,
            "splitNumber": 4,
            "radius": "90%",
            "center": ["50%", "55%"],
            "progress": {"show": True, "width": 14, "itemStyle": {"color": ctx.palette[0]}},
            "axisLine": {"lineStyle": {"width": 14, "color": [[1, ctx.colors["grid_color"]]]}},
            "axisTick": {"show": False},
            "splitLine": {"show": False},
            "axisLabel": {"show": False},
            "pointer": {"show": True, "length": "60%", "width": 4, "itemStyle": {"color": ctx.palette[0]}},
            "anchor": {"show": False},
            "detail": {
                "valueAnimation": True, "fontSize": 28, "color": ctx.colors["tooltip_text"],
                "offsetCenter": [0, "40%"], "formatter": "{value}",
            },
            "title": {"show": True, "color": ctx.colors["ax_color"], "fontSize": 11, "offsetCenter": [0, "-30%"]},
            "data": [{"name": metric, "value": value}],
        }]
        return json.dumps(base, ensure_ascii=False)
