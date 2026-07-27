"""Planner 选型回归测试 — heuristic.py。

P3 改造前先固化现行选型行为，确保 data_hints 重构后产出不变：
- 时间字段 + 数值 → line
- 占比词命中 value 字段且 ≤12 行 → pie
- 有数值无时间无占比 → bar
- 无数值 → table
- 显式「只展示 X」→ X
- 地理字段 + 地图需求 → map_china
- 经纬度 + 海外 sheet → map_world
"""

from __future__ import annotations

from typing import Any

from vizagent_dashboard.inventory.spec import ColumnInfo, DataInventory, SheetInfo
from vizagent_dashboard.planner.heuristic import plan_dashboard
from vizagent_dashboard.schemas.dashboard_spec import ChartType


def _build(sheet_name: str, columns: list[ColumnInfo], rows: list[dict[str, Any]]):
    inventory = DataInventory(
        sheets=[SheetInfo(name=sheet_name, row_count=len(rows), columns=columns)],
        source_sha256="test",
    )
    return inventory, {sheet_name: rows}


def _first_chart_type(spec) -> ChartType:
    for row in spec.layout:
        for item in row.items:
            return item.chart_type
    raise AssertionError("layout 无 item")


class TestPlannerSelection:
    def test_time_field_selects_line(self):
        columns = [ColumnInfo(name="月份", dtype="date"), ColumnInfo(name="销售额", dtype="numeric")]
        rows = [{"月份": f"2025-{m:02d}", "销售额": str(m * 100)} for m in range(1, 7)]
        inv, sheets = _build("销售趋势", columns, rows)
        spec = plan_dashboard(inv, sheets)
        assert _first_chart_type(spec) == ChartType.line

    def test_ratio_field_selects_pie(self):
        columns = [ColumnInfo(name="渠道", dtype="categorical"), ColumnInfo(name="转化率", dtype="numeric")]
        rows = [{"渠道": c, "转化率": str(v)} for c, v in [("A", "10"), ("B", "20"), ("C", "30")]]
        inv, sheets = _build("渠道转化", columns, rows)
        spec = plan_dashboard(inv, sheets)
        assert _first_chart_type(spec) == ChartType.pie

    def test_default_numeric_selects_bar(self):
        columns = [ColumnInfo(name="品类", dtype="categorical"), ColumnInfo(name="销售额", dtype="numeric")]
        rows = [{"品类": c, "销售额": str(v)} for c, v in [("数码", "100"), ("服装", "200")]]
        inv, sheets = _build("品类对比", columns, rows)
        spec = plan_dashboard(inv, sheets)
        assert _first_chart_type(spec) == ChartType.bar

    def test_no_numeric_selects_table(self):
        columns = [ColumnInfo(name="姓名", dtype="text"), ColumnInfo(name="备注", dtype="text")]
        rows = [{"姓名": "张三", "备注": "ok"}, {"姓名": "李四", "备注": "ok"}]
        inv, sheets = _build("名单", columns, rows)
        spec = plan_dashboard(inv, sheets)
        assert _first_chart_type(spec) == ChartType.table

    def test_explicit_requirement_overrides(self):
        columns = [ColumnInfo(name="月份", dtype="date"), ColumnInfo(name="销售额", dtype="numeric")]
        rows = [{"月份": "2025-01", "销售额": "100"}]
        inv, sheets = _build("销售趋势", columns, rows)
        spec = plan_dashboard(inv, sheets, requirement="只展示饼图")
        assert _first_chart_type(spec) == ChartType.pie

    def test_geo_field_with_map_requirement(self):
        columns = [ColumnInfo(name="地区", dtype="categorical"), ColumnInfo(name="销售额", dtype="numeric")]
        rows = [{"地区": "广东", "销售额": "100"}, {"地区": "北京", "销售额": "200"}]
        inv, sheets = _build("地区销售", columns, rows)
        spec = plan_dashboard(inv, sheets, requirement="看地图")
        assert _first_chart_type(spec) == ChartType.map_china

    def test_longitude_latitude_world_map(self):
        columns = [
            ColumnInfo(name="城市", dtype="categorical"),
            ColumnInfo(name="经度", dtype="numeric"),
            ColumnInfo(name="纬度", dtype="numeric"),
            ColumnInfo(name="销售额", dtype="numeric"),
        ]
        rows = [{"城市": "纽约", "经度": "-74", "纬度": "40", "销售额": "100"}]
        inv, sheets = _build("海外销售", columns, rows)
        spec = plan_dashboard(inv, sheets)
        assert _first_chart_type(spec) == ChartType.map_world


class TestPlannerMisc:
    def test_metric_sheet_produces_kpis(self):
        columns = [ColumnInfo(name="指标", dtype="categorical"), ColumnInfo(name="值", dtype="numeric")]
        rows = [{"指标": "营收", "值": "1000"}, {"指标": "利润", "值": "200"}]
        inv, sheets = _build("核心指标", columns, rows)
        spec = plan_dashboard(inv, sheets)
        types = [item.chart_type for row in spec.layout for item in row.items]
        assert all(t == ChartType.kpi for t in types)
        assert len(types) == 2

    def test_theme_inference_light(self):
        columns = [ColumnInfo(name="月份", dtype="date"), ColumnInfo(name="销售额", dtype="numeric")]
        rows = [{"月份": "2025-01", "销售额": "100"}]
        inv, sheets = _build("销售", columns, rows)
        spec = plan_dashboard(inv, sheets, requirement="用浅色主题")
        assert spec.theme == "paper-light"
