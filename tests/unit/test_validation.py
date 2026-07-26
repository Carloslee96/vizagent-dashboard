"""验证模块测试 — validation/static.py。

覆盖：
- check_html_truncation
- count_charts_in_html
- check_overlaps / check_zero_size / check_duplicate_maps / check_empty_options
- validate_html 聚合报告
- 边界情况：空文本、无图表、真实编译产物
"""

from __future__ import annotations

from vizagent_dashboard.compiler.skeleton import compile_dashboard
from vizagent_dashboard.validation.static import (
    check_duplicate_maps,
    check_empty_options,
    check_html_truncation,
    check_overlaps,
    check_zero_size,
    count_charts_in_html,
    validate_html,
)


class TestCheckHTMLTruncation:
    def test_complete_html(self):
        """完整 HTML → is_truncated=False。"""
        result = check_html_truncation("<html><body></body></html>")
        assert result["is_truncated"] is False

    def test_truncated_html(self):
        """缺闭合标签 → is_truncated=True。"""
        result = check_html_truncation("<html><body>")
        assert result["is_truncated"] is True

    def test_empty_string(self):
        result = check_html_truncation("")
        assert result["is_truncated"] is True

    def test_returns_dict(self):
        """确保返回 dict 而非 bool。"""
        result = check_html_truncation("<html><body></body></html>")
        assert isinstance(result, dict)
        assert "is_truncated" in result
        assert "score" in result


class TestCountChartsInHTML:
    def test_no_charts(self):
        assert count_charts_in_html("<html></html>")["total"] == 0

    def test_count_echarts_init(self):
        html = """
        <html>
        <script>echarts.init(document.getElementById('c1'));</script>
        <script>echarts.init(document.getElementById('c2'));</script>
        </html>
        """
        assert count_charts_in_html(html)["total"] == 2

    def test_count_empty_html(self):
        assert count_charts_in_html("")["total"] == 0

    def test_count_with_series_types(self):
        html = """
        <html>
        <script>var chart = echarts.init(...);
        chart.setOption({"series":[{"type":"line"},{"type":"bar"}]});
        </script>
        </html>
        """
        result = count_charts_in_html(html)
        assert result["total"] == 1
        assert result["line"] == 1
        assert result["bar"] == 1


class TestCheckOverlaps:
    """check_overlaps 仅报告显式 overlap 标记；真实几何重叠由浏览器验证。"""

    def test_no_overlaps(self):
        issues = check_overlaps([])
        assert len(issues) == 0

    def test_copes_with_mixed_types(self):
        """F4 防御：非 dict 元素不崩溃。"""
        issues = check_overlaps([{"x": 0, "y": 0, "w": 10, "h": 10}, "not-a-dict"])
        assert isinstance(issues, list)

    def test_plain_series_no_false_positive(self):
        """无 overlap 标记的 option 不产生告警。"""
        boxes = [{"series": []}, {"series": []}]
        issues = check_overlaps(boxes)
        assert len(issues) == 0

    def test_explicit_overlap_flag_reported(self):
        issues = check_overlaps([{"overlap": "panel#0 与 panel#1 重叠"}])
        assert len(issues) == 1


class TestCheckZeroSize:
    def test_all_valid(self):
        opts = [{"series": [{"data": [1, 2, 3]}]}]
        issues = check_zero_size(opts)
        assert len(issues) == 0

    def test_empty_option_flagged(self):
        """缺 series 的 option 被标记。"""
        issues = check_zero_size([{}])
        assert len(issues) == 1

    def test_mixed(self):
        opts = [
            {"series": [{"data": [1, 2, 3]}]},
            {},
        ]
        issues = check_zero_size(opts)
        assert len(issues) == 1


class TestCheckDuplicateMaps:
    def test_no_maps(self):
        html = "<html><body></body></html>"
        issues = check_duplicate_maps(html)
        assert len(issues) == 0

    def test_single_map(self):
        """单个 registerMap 不触发警告。"""
        html = '<html><script>registerMap("china", {...})</script></html>'
        issues = check_duplicate_maps(html)
        assert len(issues) == 0

    def test_duplicate_china_map(self):
        """同一地图注册 2 次应触发告警。"""
        html = """
        <html>
        <script>registerMap("china", {...})</script>
        <script>registerMap("china", {...})</script>
        <script>registerMap("world", {...})</script>
        </html>
        """
        issues = check_duplicate_maps(html)
        assert len(issues) >= 1


class TestCheckEmptyOptions:
    def test_valid_options(self):
        html = '<html><script>chart.setOption({"series":[{"data":[1]}]});</script></html>'
        issues = check_empty_options(html)
        assert len(issues) == 0

    def test_empty_option_block(self):
        html = '<html><script>chart.setOption({"title":{}});</script></html>'
        issues = check_empty_options(html)
        assert len(issues) == 0

    def test_no_charts(self):
        issues = check_empty_options("<html></html>")
        assert len(issues) == 0


class TestValidateHTML:
    def test_valid_compiled_html(self, mini_data, mini_spec):
        """真实编译产物应通过门禁。"""
        html = compile_dashboard(spec=mini_spec, excel_data=mini_data)
        report = validate_html(html)
        assert report["is_valid"] is True
        assert report["score"] == 100
        assert isinstance(report["issues"], list)
        assert isinstance(report["chart_counts"], dict)
        assert report["offline"] is True

    def test_bare_html_rejected(self):
        """裸 HTML（无图表 option 清单）不再判为健康。"""
        report = validate_html("<html><body></body></html>")
        assert report["is_valid"] is False
        assert any("图表 option" in issue for issue in report["errors"])

    def test_truncated_html(self):
        report = validate_html("<html>")
        assert report["is_valid"] is False
        assert any("</html>" in issue for issue in report["errors"])

    def test_empty_html(self):
        report = validate_html("")
        assert report["is_valid"] is False

    def test_external_script_rejected(self, mini_data, mini_spec):
        """embedded 产物被注入外部脚本后应判为不可离线。"""
        html = compile_dashboard(spec=mini_spec, excel_data=mini_data)
        injected = html.replace("</body>", '<script src="https://evil.example/x.js"></script></body>')
        report = validate_html(injected)
        assert report["is_valid"] is False
        assert report["offline"] is False

    def test_real_output_valid(self, ecommerce_data, ecommerce_spec):
        """用真实电商编译产物验证。"""
        html = compile_dashboard(spec=ecommerce_spec, excel_data=ecommerce_data)
        report = validate_html(html)
        assert report["is_valid"] is True
        assert report["score"] == 100
