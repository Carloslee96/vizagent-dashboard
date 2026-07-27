"""Chart option 生成测试 — build_chart_option 所有图表类型。

测试策略：
- 每种图表类型至少一个 happy-path case
- 边界：空数据、无字段匹配
- 输出必须是合法 JSON 且包含必要的 ECharts 字段
"""

from __future__ import annotations

import json

from vizagent_dashboard.compiler.chart_options import build_chart_option


class TestBuildChartOption:
    """build_chart_option 确定性测试（零 LLM 依赖）。"""

    def test_line_chart(self, mini_data, chart_palette, css_vars):
        """折线图：按月销售额聚合。"""
        option_json = build_chart_option(
            chart_type="line",
            title="月销售额趋势",
            data=mini_data,
            x_field="月份",
            y_field="销售额",
            chart_palette=chart_palette,
            css_vars=css_vars,
        )
        opt = json.loads(option_json)
        assert opt["title"]["text"] == "月销售额趋势"
        assert opt["series"][0]["type"] == "line"
        assert len(opt["series"][0]["data"]) == 3  # 3 rows after aggregation
        assert "xAxis" in opt
        assert opt["xAxis"]["type"] == "category"

    def test_bar_chart(self, mini_data, chart_palette, css_vars):
        """柱状图：按类别聚合销售额。"""
        option_json = build_chart_option(
            chart_type="bar",
            title="各品类对比",
            data=mini_data,
            x_field="类别",
            y_field="销售额",
            chart_palette=chart_palette,
            css_vars=css_vars,
        )
        opt = json.loads(option_json)
        assert opt["series"][0]["type"] == "bar"
        assert len(opt["xAxis"]["data"]) >= 2  # 数码 + 服装

    def test_pie_chart(self, mini_data, chart_palette, css_vars):
        """饼图：按类别占比。"""
        option_json = build_chart_option(
            chart_type="pie",
            title="品类占比",
            data=mini_data,
            x_field="类别",
            y_field="销售额",
            chart_palette=chart_palette,
            css_vars=css_vars,
        )
        opt = json.loads(option_json)
        assert opt["series"][0]["type"] == "pie"
        assert len(opt["series"][0]["data"]) >= 2
        # 检查饼图数据格式
        for item in opt["series"][0]["data"]:
            assert "name" in item
            assert "value" in item

    def test_scatter_chart(self, mini_data, chart_palette, css_vars):
        """散点图：两轴（利润 vs 数量）。"""
        option_json = build_chart_option(
            chart_type="scatter",
            title="利润 vs 数量",
            data=mini_data,
            x_field="",
            y_field=["利润", "数量"],
            chart_palette=chart_palette,
            css_vars=css_vars,
        )
        opt = json.loads(option_json)
        assert opt["series"][0]["type"] == "scatter"
        assert len(opt["series"][0]["data"]) == 3
        # 每个数据点应为 [x, y] 对
        assert len(opt["series"][0]["data"][0]) == 2

    def test_area_chart(self, mini_data, chart_palette, css_vars):
        """面积图：line type + areaStyle。"""
        option_json = build_chart_option(
            chart_type="area",
            title="面积趋势",
            data=mini_data,
            x_field="月份",
            y_field="销售额",
            chart_palette=chart_palette,
            css_vars=css_vars,
        )
        opt = json.loads(option_json)
        assert opt["series"][0]["type"] == "line"
        assert "areaStyle" in opt["series"][0]

    def test_empty_data_returns_valid_json(self, chart_palette, css_vars):
        """空数据时返回基础 JSON（不崩溃）。"""
        option_json = build_chart_option(
            chart_type="line",
            title="空图表",
            data=[],
            x_field="月份",
            y_field="销售额",
            chart_palette=chart_palette,
            css_vars=css_vars,
        )
        opt = json.loads(option_json)
        assert "title" in opt

    def test_no_column_match_fallback(self, chart_palette, css_vars):
        """字段名不匹配也不崩溃。"""
        option_json = build_chart_option(
            chart_type="pie",
            title="无匹配",
            data=[{"a": "1", "b": "2"}],
            x_field="nonexistent",
            y_field="also_nonexistent",
            chart_palette=chart_palette,
            css_vars=css_vars,
        )
        opt = json.loads(option_json)
        # 无匹配字段时 pie 返回 base（无 series）
        assert "title" in opt
        assert opt["title"]["text"] == "无匹配"

    def test_invalid_chart_type_falls_to_bar(self, mini_data, chart_palette, css_vars):
        """不支持的类型回退到柱状图。"""
        option_json = build_chart_option(
            chart_type="unknown_type_xyz",
            title="回退测试",
            data=mini_data,
            x_field="月份",
            y_field="销售额",
            chart_palette=chart_palette,
            css_vars=css_vars,
        )
        opt = json.loads(option_json)
        assert opt["series"][0]["type"] == "bar"

    def test_output_is_valid_json(self, mini_data, chart_palette, css_vars):
        """对所有图表类型输出合法 JSON。"""
        for ct in ["line", "bar", "pie", "scatter", "area"]:
            option_json = build_chart_option(
                chart_type=ct,
                title=f"测试{ct}",
                data=mini_data,
                x_field="月份",
                y_field="销售额",
                chart_palette=chart_palette,
                css_vars=css_vars,
            )
            assert option_json is not None
            opt = json.loads(option_json)
            assert isinstance(opt, dict)
            assert "series" in opt or "title" in opt

    def test_color_palette_applied(self, mini_data, css_vars):
        """自定义 palette 应反映到系列颜色。"""
        custom_palette = ["#FF0000", "#00FF00", "#0000FF"]
        option_json = build_chart_option(
            chart_type="bar",
            title="颜色测试",
            data=mini_data,
            x_field="月份",
            y_field="销售额",
            chart_palette=custom_palette,
            css_vars=css_vars,
        )
        opt = json.loads(option_json)
        assert opt["color"] == custom_palette

    def test_nightingale_chart(self, mini_data, chart_palette, css_vars):
        """南丁格尔玫瑰图：pie + roseType=area。"""
        option_json = build_chart_option(
            chart_type="nightingale", title="品类玫瑰", data=mini_data,
            x_field="类别", y_field="销售额", chart_palette=chart_palette, css_vars=css_vars,
        )
        opt = json.loads(option_json)
        assert opt["series"][0]["type"] == "pie"
        assert opt["series"][0]["roseType"] == "area"
        assert opt["series"][0]["radius"] == ["18%", "70%"]
        assert len(opt["series"][0]["data"]) >= 2

    def test_treemap_chart(self, mini_data, chart_palette, css_vars):
        """矩形树图：type=treemap。"""
        option_json = build_chart_option(
            chart_type="treemap", title="品类占比", data=mini_data,
            x_field="类别", y_field="销售额", chart_palette=chart_palette, css_vars=css_vars,
        )
        opt = json.loads(option_json)
        assert opt["series"][0]["type"] == "treemap"
        assert len(opt["series"][0]["data"]) >= 2
        assert opt["series"][0]["breadcrumb"] == {"show": False}

    def test_funnel_chart(self, mini_data, chart_palette, css_vars):
        """漏斗图：type=funnel。"""
        option_json = build_chart_option(
            chart_type="funnel", title="转化漏斗", data=mini_data,
            x_field="类别", y_field="销售额", chart_palette=chart_palette, css_vars=css_vars,
        )
        opt = json.loads(option_json)
        assert opt["series"][0]["type"] == "funnel"
        assert opt["series"][0]["sort"] == "descending"
        assert len(opt["series"][0]["data"]) >= 2

    def test_new_types_empty_data_safe(self, chart_palette, css_vars):
        """新类型空数据不崩溃，返回 base。"""
        for ct in ["nightingale", "treemap", "funnel"]:
            option_json = build_chart_option(
                chart_type=ct, title=f"空{ct}", data=[],
                x_field="类别", y_field="销售额", chart_palette=chart_palette, css_vars=css_vars,
            )
            assert "title" in json.loads(option_json)

    def test_gauge_chart(self, mini_data, chart_palette, css_vars):
        """仪表盘：单值进度。"""
        option_json = build_chart_option(
            chart_type="gauge", title="完成率", data=mini_data,
            x_field="月份", y_field="销售额", chart_palette=chart_palette, css_vars=css_vars,
        )
        opt = json.loads(option_json)
        assert opt["series"][0]["type"] == "gauge"
        assert opt["series"][0]["data"][0]["value"] == 4500  # 1000+2000+1500
        assert opt["series"][0]["max"] == 4500  # value>100 → max=value

    def test_gauge_percentage_max_100(self, chart_palette, css_vars):
        """百分比类（≤100）量程 0-100。"""
        data = [{"项": "A", "率": "75"}]
        option_json = build_chart_option(
            chart_type="gauge", title="转化率", data=data,
            x_field="项", y_field="率", chart_palette=chart_palette, css_vars=css_vars,
        )
        opt = json.loads(option_json)
        assert opt["series"][0]["max"] == 100
        assert opt["series"][0]["data"][0]["value"] == 75

    def test_radar_chart(self, mini_data, chart_palette, css_vars):
        """雷达图：多指标多维度。"""
        option_json = build_chart_option(
            chart_type="radar", title="多维对比", data=mini_data,
            x_field="类别", y_field=["销售额", "利润", "数量"],
            chart_palette=chart_palette, css_vars=css_vars,
        )
        opt = json.loads(option_json)
        assert opt["series"][0]["type"] == "radar"
        assert len(opt["radar"]["indicator"]) == 3  # 3 个维度
        # build_chart_option 直调不聚合，mini_data 3 行 → 3 条雷达数据
        assert len(opt["series"][0]["data"]) == 3

    def test_radar_single_field_returns_base(self, mini_data, chart_palette, css_vars):
        """雷达图需 ≥2 个 y 字段，否则返回 base。"""
        option_json = build_chart_option(
            chart_type="radar", title="单维度", data=mini_data,
            x_field="类别", y_field="销售额", chart_palette=chart_palette, css_vars=css_vars,
        )
        opt = json.loads(option_json)
        assert "series" not in opt or opt.get("series", []) == []

    def test_heatmap_chart(self, chart_palette, css_vars):
        """热力图：x×series 二维网格，值为 metric 聚合。"""
        data = [
            {"月份": "1月", "地区": "华东", "销售额": "100"},
            {"月份": "1月", "地区": "华南", "销售额": "200"},
            {"月份": "2月", "地区": "华东", "销售额": "150"},
            {"月份": "2月", "地区": "华南", "销售额": "250"},
        ]
        option_json = build_chart_option(
            chart_type="heatmap", title="月度×地区", data=data,
            x_field="月份", y_field="销售额", series_field="地区",
            chart_palette=chart_palette, css_vars=css_vars,
        )
        opt = json.loads(option_json)
        assert opt["series"][0]["type"] == "heatmap"
        assert opt["xAxis"]["data"] == ["1月", "2月"]
        assert opt["yAxis"]["data"] == ["华东", "华南"]
        # 4 个网格点
        assert len(opt["series"][0]["data"]) == 4
        # visualMap min/max 正确
        assert opt["visualMap"]["min"] == 100
        assert opt["visualMap"]["max"] == 250

    def test_heatmap_without_series_returns_base(self, mini_data, chart_palette, css_vars):
        """热力图无 series_field 时返回 base（需二维）。"""
        option_json = build_chart_option(
            chart_type="heatmap", title="无二维", data=mini_data,
            x_field="类别", y_field="销售额", chart_palette=chart_palette, css_vars=css_vars,
        )
        opt = json.loads(option_json)
        assert "series" not in opt or opt.get("series", []) == []


class TestBuildChartOptionWithRealData:
    """用真实电商数据（72 行）测试。"""

    def test_line_with_real_data(self, ecommerce_data, chart_palette, css_vars):
        """真实数据 72 行 → 折线图生成无崩溃，数据点数合理。"""
        option_json = build_chart_option(
            chart_type="line",
            title="月销售额趋势",
            data=ecommerce_data,
            x_field="月份",
            y_field="销售额",
            chart_palette=chart_palette,
            css_vars=css_vars,
        )
        opt = json.loads(option_json)
        assert opt["series"][0]["type"] == "line"
        # 数据在外部聚合后传入；直接传 72 行 → 72 个 data 点（合理）

    def test_bar_with_real_data(self, ecommerce_data, chart_palette, css_vars):
        """按类别聚合→4 类。"""
        # 使用已聚合的数据（skeleton 层在调用前聚合，这里直接测 build_chart_option）
        from collections import defaultdict

        agg: dict[str, float] = defaultdict(float)
        for row in ecommerce_data:
            agg[row["类别"]] += float(row["销售额"])
        data = [{"类别": k, "销售额": v} for k, v in sorted(agg.items())]

        option_json = build_chart_option(
            chart_type="bar",
            title="品类对比",
            data=data,
            x_field="类别",
            y_field="销售额",
            chart_palette=chart_palette,
            css_vars=css_vars,
        )
        opt = json.loads(option_json)
        assert len(opt["series"][0]["data"]) == 4  # 数码/服装/食品/家居

    def test_pie_with_real_data(self, ecommerce_data, chart_palette, css_vars):
        """按地区聚合→3 区。"""
        from collections import defaultdict
        agg: dict[str, float] = defaultdict(float)
        for row in ecommerce_data:
            agg[row["地区"]] += float(row["销售额"])
        data = [{"地区": k, "销售额": v} for k, v in sorted(agg.items())]

        option_json = build_chart_option(
            chart_type="pie",
            title="地区占比",
            data=data,
            x_field="地区",
            y_field="销售额",
            chart_palette=chart_palette,
            css_vars=css_vars,
        )
        opt = json.loads(option_json)
        assert len(opt["series"][0]["data"]) == 3
