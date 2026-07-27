"""热力图 builder（二维网格：x_field × series_field，值为 metric 聚合）。"""

from __future__ import annotations

import json
from typing import Any

from vizagent_dashboard.compiler.charts._common import ChartContext, _clean_number


class HeatmapBuilder:
    data_hints = ("matrix",)

    def build(self, ctx: ChartContext) -> str:
        base: dict[str, Any] = ctx.base
        if not ctx.y_fields or not ctx.series_field:
            return json.dumps(base)
        metric = ctx.y_fields[0]

        # x / y 维度的去重类别（保留首次出现顺序）
        x_cats: list[str] = []
        y_cats: list[str] = []
        agg: dict[tuple[str, str], float] = {}
        for row in ctx.data:
            x = str(row.get(ctx.x_field, "")).strip()
            y = str(row.get(ctx.series_field, "")).strip()
            value = _clean_number(row.get(metric))
            if not x or not y or value is None:
                continue
            if x not in x_cats:
                x_cats.append(x)
            if y not in y_cats:
                y_cats.append(y)
            key = (x, y)
            agg[key] = agg.get(key, 0) + value

        if not agg:
            return json.dumps(base)

        triples = [[x_cats.index(x), y_cats.index(y), value] for (x, y), value in agg.items()]
        values = [value for _, _, value in triples]
        area = ctx.colors["grid_color"]
        base["tooltip"] = {"trigger": "item", "backgroundColor": ctx.colors["tooltip_bg"],
                           "borderColor": ctx.colors["grid_color"],
                           "textStyle": {"color": ctx.colors["tooltip_text"], "fontSize": 12}}
        base["grid"] = {"top": "12%", "bottom": "18%", "left": "8%", "right": "8%", "containLabel": True}
        base["xAxis"] = {"type": "category", "data": x_cats, "splitArea": {"show": True},
                         "axisLabel": {"color": ctx.colors["ax_color"], "fontSize": 10},
                         "axisLine": {"lineStyle": {"color": ctx.colors["grid_color"]}}}
        base["yAxis"] = {"type": "category", "data": y_cats, "splitArea": {"show": True},
                         "axisLabel": {"color": ctx.colors["ax_color"], "fontSize": 10},
                         "axisLine": {"lineStyle": {"color": ctx.colors["grid_color"]}}}
        base["visualMap"] = {
            "min": min(values),
            "max": max(values),
            "calculable": True,
            "orient": "horizontal",
            "left": "center",
            "bottom": 0,
            "inRange": {"color": [area, ctx.palette[0]]},
            "textStyle": {"color": ctx.colors["ax_color"], "fontSize": 10},
        }
        base["series"] = [{
            "type": "heatmap",
            "data": triples,
            "label": {"show": True, "color": ctx.colors["tooltip_text"], "fontSize": 9},
            "emphasis": {"focus": "item", "itemStyle": {"shadowBlur": 6}},
        }]
        return json.dumps(base, ensure_ascii=False)
