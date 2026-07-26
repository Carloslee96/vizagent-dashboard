"""编译管道端到端测试 — compile_artifacts / compile_dashboard 完整流程。

覆盖：
- 完整编译（spec + 数据 + 主题 → HTML）
- KPI 聚合 sum
- 空数据
- 主题别名（旧 ID → 新 clean-room 主题）
- 图表面板标题显示
- embedded / cdn 部署模式
"""

from __future__ import annotations

import json
import re

from vizagent_dashboard.compiler.skeleton import (
    compile_dashboard,
    parse_design_tokens,
    build_css_block,
    build_html,
)
from vizagent_dashboard.validation.static import validate_html


class TestParseDesignTokens:
    """主题 .md → CSS 变量 / 色板。"""

    def test_midnight_ops_has_css_vars(self, midnight_ops_theme_content):
        tokens = parse_design_tokens(midnight_ops_theme_content)
        assert "css_vars" in tokens
        assert "chart_palette" in tokens
        assert len(tokens["css_vars"]) > 5
        assert tokens["css_vars"].get("--bg-primary", "").startswith("#")

    def test_chart_palette_not_empty(self, midnight_ops_theme_content):
        tokens = parse_design_tokens(midnight_ops_theme_content)
        assert len(tokens["chart_palette"]) >= 3

    def test_unknown_md_returns_empty(self):
        tokens = parse_design_tokens("")
        assert tokens["css_vars"] == {}
        assert len(tokens["chart_palette"]) >= 3  # fallback palette


class TestBuildCSSBlock:
    def test_uses_provided_vars(self, css_vars):
        css = build_css_block(css_vars)
        assert "--bg-primary: #0A0B0D" in css
        assert "--text-primary: #E6E8EC" in css
        assert "--accent-primary: #2D5BFF" in css

    def test_includes_body_styles(self, css_vars):
        css = build_css_block(css_vars)
        assert "body {" in css
        assert "background:" in css  # 新 CSS 用 background 简写

    def test_includes_kpi_styles(self, css_vars):
        css = build_css_block(css_vars)
        assert ".kpi-card" in css
        assert ".kpi-value" in css


class TestBuildHTML:
    def test_basic_structure(self, css_vars):
        html = build_html(
            title="测试仪表盘",
            chart_options=['{"title": {"text": "图表1"}}'],
            kpi_cards=[{"label": "总销售额", "value": "¥1,000"}],
            css_vars=css_vars,
            deployment_mode="cdn",
        )
        assert "<!doctype html>" in html
        assert "测试仪表盘" in html
        assert "总销售额" in html
        assert "¥1,000" in html
        assert "echarts" in html  # 运行时 JS 引用 echarts

    def test_chart_title_in_panel(self, css_vars):
        """面板标题应从 option JSON 提取。"""
        html = build_html(
            title="测试",
            chart_options=['{"title": {"text": "自定义标题"}}'],
            kpi_cards=[],
            css_vars=css_vars,
            deployment_mode="cdn",
        )
        assert "自定义标题" in html

    def test_multiple_charts_unique_ids(self, css_vars):
        chart_opts = [
            '{"title": {"text": "A"}}',
            '{"title": {"text": "B"}}',
            '{"title": {"text": "C"}}',
        ]
        html = build_html("多图", chart_opts, [], css_vars)
        assert "viz-chart-0" in html
        assert "viz-chart-1" in html
        assert "viz-chart-2" in html

    def test_csp_present(self, css_vars):
        html = build_html("安全", [], [], css_vars)
        assert "Content-Security-Policy" in html

    def test_cdn_mode_uses_single_cdn(self, css_vars):
        """cdn 模式只引用 jsdelivr，不再使用多 CDN fallback。"""
        html = build_html("CDN", [], [], css_vars, deployment_mode="cdn")
        assert "jsdelivr.net" in html
        assert "npmmirror.com" not in html
        assert "bootcdn.net" not in html

    def test_embedded_mode_inlines_runtime(self, css_vars):
        """embedded 模式内嵌 echarts 运行时，无外部脚本。"""
        html = build_html("离线", [], [], css_vars, deployment_mode="embedded")
        assert "jsdelivr.net" not in html
        assert re.search(r'<script[^>]+src=["\']https?://', html) is None
        assert "echarts" in html  # 内嵌运行时


class TestCompileDashboard:
    """端到端编译测试。"""

    def test_compile_with_mini_data(self, mini_data, mini_spec):
        """3 行迷你数据 → 编译成功。"""
        html = compile_dashboard(spec=mini_spec, excel_data=mini_data)
        assert isinstance(html, str)
        assert len(html) > 500
        assert "测试大屏" in html

    def test_kpi_sum_aggregation(self, mini_data, mini_spec):
        """KPI aggregation=sum 求和正确。"""
        html = compile_dashboard(spec=mini_spec, excel_data=mini_data)
        # 总销售额 = 1000 + 2000 + 1500 = 4500
        assert "4,500" in html
        # 总利润 = 200 + 300 + 250 = 750
        assert "750" in html

    def test_compile_with_real_data(self, ecommerce_data, ecommerce_spec):
        """72 行真实数据 → 编译成功并通过新门禁（score=100）。"""
        html = compile_dashboard(spec=ecommerce_spec, excel_data=ecommerce_data)
        report = validate_html(html)
        assert report["is_valid"] is True
        assert report["score"] == 100
        assert len(report["issues"]) == 0

    def test_real_data_kpi_values(self, ecommerce_data, ecommerce_spec):
        """真实数据 KPI sum 值验证。"""
        html = compile_dashboard(spec=ecommerce_spec, excel_data=ecommerce_data)
        # 总销售额 = 5,465,000
        assert "5,465,000" in html
        # 总利润 = 1,300,800
        assert "1,300,800" in html

    def test_chart_titles_in_panels(self, ecommerce_data, ecommerce_spec):
        """面板标题显示真实图表名。"""
        html = compile_dashboard(spec=ecommerce_spec, excel_data=ecommerce_data)
        assert "月销售额趋势" in html
        assert "各品类销售额占比" in html
        assert "各地区销售额对比" in html
        assert "利润 vs 数量" in html

    def test_empty_data_does_not_crash(self, mini_spec):
        """无数据时编译不崩溃。"""
        html = compile_dashboard(spec=mini_spec, excel_data=None)
        assert isinstance(html, str)
        assert len(html) > 200

    def test_theme_aliases(self, mini_data, mini_spec):
        """旧 ID 别名（monitor-dark → midnight-ops）生效，产物一致。"""
        html_alias = compile_dashboard(spec=mini_spec, excel_data=mini_data, theme_id="monitor-dark")
        html_direct = compile_dashboard(spec=mini_spec, excel_data=mini_data, theme_id="midnight-ops")
        assert html_alias == html_direct

    def test_different_themes_look_different(self, mini_data, mini_spec):
        """不同主题产生不同 CSS（色值不同）。"""
        html1 = compile_dashboard(spec=mini_spec, excel_data=mini_data, theme_id="paper-linen")
        html2 = compile_dashboard(spec=mini_spec, excel_data=mini_data, theme_id="monitor-dark")
        # paper-linen→paper-light（暖纸），monitor-dark→midnight-ops（暗色），CSS 变量值不同
        assert html1 != html2

    def test_chart_count(self, ecommerce_data, ecommerce_spec):
        """HTML 中应有 4 个 chart-container（line/pie/bar/scatter），KPI 不计入。"""
        html = compile_dashboard(spec=ecommerce_spec, excel_data=ecommerce_data)
        containers = re.findall(r'class="chart-container"', html)
        assert len(containers) == 4

    def test_embedded_mode_offline(self, mini_data, mini_spec):
        """embedded 模式无 CDN 链接、无外部脚本。"""
        html = compile_dashboard(spec=mini_spec, excel_data=mini_data, deployment_mode="embedded")
        assert "jsdelivr.net" not in html
        assert re.search(r'<script[^>]+src=["\']https?://', html) is None

    def test_build_manifest_embedded(self, ecommerce_data, ecommerce_spec):
        """编译产物内嵌 build-manifest，含覆盖与图表计数。"""
        html = compile_dashboard(spec=ecommerce_spec, excel_data=ecommerce_data)
        match = re.search(
            r'<script[^>]+id="vizagent-build-manifest"[^>]*>(.*?)</script>', html, re.DOTALL
        )
        assert match is not None
        manifest = json.loads(match.group(1).replace("<\\/", "</"))
        assert manifest["chart_count"] == 4
        assert manifest["kpi_count"] == 3
        assert manifest["coverage_complete"] is True
