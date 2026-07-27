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


class TestPlannerNewChartTypes:
    """Bug#1+#2: 新图表类型无需"只展示"即可达，且按字段兼容性分配。"""

    def test_radar_keyword_without_zhiding(self):
        """Bug#1: "用雷达图"（无"只展示"）应产出 radar，前提是 sheet 有 ≥2 数值字段。"""
        columns = [
            ColumnInfo(name="月份", dtype="date"),
            ColumnInfo(name="销售额", dtype="numeric"),
            ColumnInfo(name="订单数", dtype="numeric"),
        ]
        rows = [{"月份": "2025-01", "销售额": "100", "订单数": "10"}]
        inv, sheets = _build("月度趋势", columns, rows)
        spec = plan_dashboard(inv, sheets, requirement="用雷达图")
        item = next(item for row in spec.layout for item in row.items)
        assert item.chart_type == ChartType.radar
        assert item.y_field == ["销售额", "订单数"]

    def test_radar_incompatible_falls_back(self):
        """Bug#2: 单数值 sheet 点名 radar → 不兼容，回退到 hint 默认（bar）。"""
        columns = [ColumnInfo(name="品类", dtype="categorical"), ColumnInfo(name="销售额", dtype="numeric")]
        rows = [{"品类": "A", "销售额": "100"}]
        inv, sheets = _build("品类", columns, rows)
        spec = plan_dashboard(inv, sheets, requirement="用雷达图")
        item = next(item for row in spec.layout for item in row.items)
        assert item.chart_type == ChartType.bar

    def test_funnel_keyword_picks_funnel(self):
        columns = [ColumnInfo(name="环节", dtype="categorical"), ColumnInfo(name="人数", dtype="numeric")]
        rows = [{"环节": "曝光", "人数": "100"}, {"环节": "点击", "人数": "50"}]
        inv, sheets = _build("漏斗", columns, rows)
        spec = plan_dashboard(inv, sheets, requirement="用漏斗图")
        assert _first_chart_type(spec) == ChartType.funnel

    def test_gauge_keyword_picks_gauge(self):
        columns = [ColumnInfo(name="客群", dtype="categorical"), ColumnInfo(name="客单价", dtype="numeric")]
        rows = [{"客群": "新客", "客单价": "198"}]
        inv, sheets = _build("客单价", columns, rows)
        spec = plan_dashboard(inv, sheets, requirement="用仪表盘")
        item = next(item for row in spec.layout for item in row.items)
        assert item.chart_type == ChartType.gauge

    def test_heatmap_needs_two_dims(self):
        """Bug#2: heatmap 需 ≥2 分类维度；单维度 sheet 点名热力 → 回退。"""
        columns = [ColumnInfo(name="品类", dtype="categorical"), ColumnInfo(name="销售额", dtype="numeric")]
        rows = [{"品类": "A", "销售额": "100"}]
        inv, sheets = _build("品类", columns, rows)
        spec = plan_dashboard(inv, sheets, requirement="用热力图")
        assert _first_chart_type(spec) == ChartType.bar

    def test_heatmap_with_two_dims_binds_series_field(self):
        columns = [
            ColumnInfo(name="区域", dtype="categorical"),
            ColumnInfo(name="品类", dtype="categorical"),
            ColumnInfo(name="销售额", dtype="numeric"),
        ]
        rows = [{"区域": "华东", "品类": "数码", "销售额": "100"}]
        inv, sheets = _build("矩阵", columns, rows)
        spec = plan_dashboard(inv, sheets, requirement="用热力图")
        item = next(item for row in spec.layout for item in row.items)
        assert item.chart_type == ChartType.heatmap
        assert item.series_field == "品类"

    def test_mixed_keywords_distribute_by_compatibility(self):
        """多 sheet + 多关键词：按各自字段形态分配不同类型。"""
        inv_sheets = {}
        from vizagent_dashboard.inventory.spec import DataInventory, SheetInfo
        sheets_meta = [
            ("月度趋势", [ColumnInfo(name="月份", dtype="date"), ColumnInfo(name="销售额", dtype="numeric"), ColumnInfo(name="订单数", dtype="numeric")],
             [{"月份": "2025-01", "销售额": "100", "订单数": "10"}]),
            ("渠道", [ColumnInfo(name="渠道", dtype="categorical"), ColumnInfo(name="占比", dtype="numeric")],
             [{"渠道": "A", "占比": "50"}]),
        ]
        inventory = DataInventory(
            sheets=[SheetInfo(name=n, row_count=len(r), columns=c) for n, c, r in sheets_meta],
            source_sha256="test",
        )
        for n, _c, r in sheets_meta:
            inv_sheets[n] = r
        spec = plan_dashboard(inventory, inv_sheets, requirement="用雷达图和南丁格尔")
        types = {item.chart_type for row in spec.layout for item in row.items}
        assert ChartType.radar in types
        assert ChartType.nightingale in types
