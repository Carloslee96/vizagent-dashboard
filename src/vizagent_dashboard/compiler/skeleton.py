"""HTML 骨架生成 — 编译 DashboardSpec → output.html。

Skill 编译管道（取代 SaaS 的 LLM 编排路径）：

    DashboardSpec (Pydantic JSON)
        │
        ├─→ parse_design_tokens(theme.md) → css_vars + chart_palette
        ├─→ for each chart: build_chart_option() → option JSON
        ├─→ for each KPI: extract_kpi_values_from_data() → real value
        └─→ build_html() → 完整 HTML 字符串

关键设计：
- 编译器不感知模型、提示词或 API Key
- 输入是结构化 DashboardSpec，输出是 self-contained HTML
- 主题通过 parse_design_tokens 从 .md 文件提取 CSS 变量
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from vizagent_dashboard.compiler.chart_options import build_chart_option
from vizagent_dashboard.compiler.kpi_options import extract_kpi_values_from_data
from vizagent_dashboard.compiler.themes import load_theme


# ═══════════════════════════════════════════════════════════════════════════════
# Design tokens 解析（从 .md 提取 css_vars）
# ═══════════════════════════════════════════════════════════════════════════════


def parse_design_tokens(md: str) -> dict[str, Any]:
    """从主题 .md 解析 CSS 变量（解析任意反引号值，非仅 hex）。

    Returns:
        {"css_vars": {"--bg-primary": "#0A0B0D", ...},
         "chart_palette": ["#2D5BFF", "#5B8AFF", ...]}
    """
    css_vars: dict[str, str] = {}
    palette: list[str] = []

    # 从 Color Palette 表格提取 CSS 变量
    lines = md.split("\n")
    in_palette = False
    for line in lines:
        if line.startswith("## Color Palette"):
            in_palette = True
            continue
        if in_palette:
            if line.startswith("## "):
                break
            # 表格行: | `--token-name` | `#hex` | description |
            m = re.search(r"`--([\w-]+)`\s*\|\s*`?(#[0-9a-fA-F]{3,8})`?", line)
            if m:
                token = f"--{m.group(1)}"
                value = m.group(2)
                css_vars[token] = value

    # 从 Chart Color Palette 提取系列色
    in_chart = False
    for line in lines:
        if line.startswith("## Chart Color Palette"):
            in_chart = True
            continue
        if in_chart:
            if line.startswith("## "):
                break
            for m in re.finditer(r"#[0-9a-fA-F]{6}", line):
                color = m.group(0)
                if color not in palette:
                    palette.append(color)

    if not palette:
        palette = ["#2D5BFF", "#5B8AFF", "#8AAEFF", "#B4CCFF", "#3DAB63"]

    return {"css_vars": css_vars, "chart_palette": palette}


def extract_theme_fonts(css_vars: dict[str, str]) -> list[tuple[str, str]]:
    """从 css_vars 提取字体栈（按权重排序的 (import_name, font_family) 列表）。"""
    fonts: list[tuple[str, str]] = []
    font_family = css_vars.get("--font-family-display", "")
    if font_family:
        fonts.append((font_family, font_family.split(",")[0].strip().strip("'").strip('"')))
    return fonts


# ═══════════════════════════════════════════════════════════════════════════════
# CSS / HTML 构造
# ═══════════════════════════════════════════════════════════════════════════════


def build_css_block(css_vars: dict[str, str]) -> str:
    """从 css_vars 生成完整 CSS block。"""
    declarations = "\n".join(f"  {name}: {value};" for name, value in css_vars.items())

    bg_color = css_vars.get("--bg-primary", "#0A0B0D")
    card_color = css_vars.get("--bg-card", "#13151A")
    text_color = css_vars.get("--text-primary", "#E6E8EC")
    text_secondary = css_vars.get("--text-secondary", "#8A8F98")
    border_color = css_vars.get("--border-subtle", "#23272F")
    accent_color = css_vars.get("--accent-primary", "#2D5BFF")
    radius_card = "16px"

    return f"""
:root {{
{declarations}
}}

* {{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}}

body {{
  font-family: {css_vars.get('--font-family-base', 'Inter, sans-serif')};
  background-color: {bg_color};
  color: {text_color};
  font-size: 14px;
  line-height: 1.6;
  min-height: 100vh;
  padding: 24px;
}}

.dashboard-container {{
  max-width: 1920px;
  margin: 0 auto;
}}

.dashboard-header {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 16px;
  margin-bottom: 16px;
  border-bottom: 1px solid {border_color};
}}

.dashboard-title {{
  font-family: {css_vars.get('--font-family-display', 'Inter, sans-serif')};
  font-size: 26px;
  font-weight: 600;
  color: {text_color};
}}

.dashboard-grid {{
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
}}

.panel {{
  background-color: {card_color};
  border: 1px solid {border_color};
  border-radius: {radius_card};
  padding: 20px 24px;
}}

.panel-title {{
  font-size: 16px;
  font-weight: 600;
  color: {text_color};
  margin-bottom: 12px;
}}

.kpi-card {{
  background-color: {card_color};
  border: 1px solid {border_color};
  border-radius: {radius_card};
  padding: 20px 24px;
  text-align: left;
}}

.kpi-label {{
  font-size: 13px;
  color: {text_secondary};
  margin-bottom: 8px;
}}

.kpi-value {{
  font-family: {css_vars.get('--font-family-display', 'Inter, sans-serif')};
  font-size: 32px;
  font-weight: 600;
  color: {text_color};
}}

.chart-container {{
  width: 100%;
  height: 320px;
}}

.text-secondary {{
  color: {text_secondary};
}}

.accent {{
  color: {accent_color};
}}
"""


def build_html(
    title: str,
    chart_options: list[str],
    kpi_cards: list[dict[str, str]],
    css_vars: dict[str, str],
    deployment_mode: str = "cdn",
) -> str:
    """生成完整 self-contained HTML。

    Args:
        title: 页面标题
        chart_options: 各图表的 ECharts option JSON 字符串列表
        kpi_cards: [{"label": "总销售额", "value": "¥1,234,560"}, ...]
        css_vars: CSS 变量字典
        deployment_mode: "cdn" 或 "local"
    """
    safe_title = html.escape(title)
    css_block = build_css_block(css_vars)

    # KPI cards HTML
    kpi_html_parts = []
    for kpi in kpi_cards:
        label = html.escape(str(kpi.get("label", "")))
        value = html.escape(str(kpi.get("value", "")))
        kpi_html_parts.append(f"""
        <div class="kpi-card">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{value}</div>
        </div>""")
    kpi_html = "\n".join(kpi_html_parts)

    # Chart panels HTML
    chart_panels_html_parts = []
    chart_init_scripts = []
    for idx, option_json in enumerate(chart_options):
        safe_option = option_json.replace("</script>", "<\\/script>")
        panel_id = f"chart-panel-{idx}"
        # 从 option JSON 提取标题
        try:
            opt = json.loads(option_json)
            panel_title = html.escape(str(opt.get("title", {}).get("text", "")) or f"图表 {idx + 1}")
        except (json.JSONDecodeError, AttributeError):
            panel_title = f"图表 {idx + 1}"
        chart_panels_html_parts.append(f"""
        <div class="panel">
          <div class="panel-title">{panel_title}</div>
          <div id="{panel_id}" class="chart-container"></div>
        </div>""")
        chart_init_scripts.append(f"""
    (function() {{
      var chart = echarts.init(document.getElementById('{panel_id}'));
      chart.setOption({safe_option});
      window.addEventListener('resize', function() {{ chart.resize(); }});
    }})();""")

    chart_panels_html = "\n".join(chart_panels_html_parts)
    chart_init_js = "\n".join(chart_init_scripts)

    if deployment_mode == "local":
        echarts_script = '<script src="assets/echarts.min.js"></script>'
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "connect-src 'self';"
        )
    else:
        echarts_script = """<!-- ECharts 主库 — 三层备用加载 -->
<script src="https://registry.npmmirror.com/echarts/5.4.3/files/dist/echarts.min.js"></script>
<script>
  if (typeof echarts === 'undefined') {
    document.write('<script src="https://cdn.bootcdn.net/ajax/libs/echarts/5.4.3/echarts.min.js"><\\/script>');
  }
  if (typeof echarts === 'undefined') {
    document.write('<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"><\\/script>');
  }
</script>"""
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' "
            "https://registry.npmmirror.com https://cdn.bootcdn.net https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "connect-src 'self';"
        )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{safe_title}</title>
  <meta http-equiv="Content-Security-Policy" content="{csp}">
  <style>{css_block}</style>
</head>
<body>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h1 class="dashboard-title">{safe_title}</h1>
      <span class="text-secondary">vizagent-dashboard</span>
    </div>

    <div class="dashboard-grid">
{kpi_html}
    </div>

    <div class="dashboard-grid" style="margin-top: 16px;">
{chart_panels_html}
    </div>
  </div>

  {echarts_script}
  <script>
{chart_init_js}
  </script>
</body>
</html>
"""


# ═══════════════════════════════════════════════════════════════════════════════
# Compile pipeline — top-level entry point
# ═══════════════════════════════════════════════════════════════════════════════


def compile_dashboard(
    spec: BaseModel,
    excel_data: list[dict] | None = None,
    theme_id: str = "midnight-ops",
    deployment_mode: str = "cdn",
) -> str:
    """顶层编译入口：DashboardSpec + 数据 → HTML 字符串。

    Args:
        spec: DashboardSpec（带 title / theme / layout）
        excel_data: 真实数据行（[{"col1": v1, ...}, ...]）
        theme_id: 主题 ID（去品牌命名，如 "paper-linen"）
        deployment_mode: "cdn" 或 "local"

    Returns:
        完整 self-contained HTML 字符串
    """
    # 1. 加载主题
    theme_md = load_theme(theme_id)
    if not theme_md:
        theme_md = load_theme("midnight-ops")
    tokens = parse_design_tokens(theme_md)
    css_vars = tokens["css_vars"]
    chart_palette = tokens["chart_palette"]

    # 2. 解析 spec（duck-typed: spec 字段名兼容）
    title = getattr(spec, "title", "数据大屏")
    layout = getattr(spec, "layout", []) or []

    # 3. 收集 KPI 和 chart
    kpi_cards: list[dict[str, str]] = []
    chart_options: list[str] = []

    # 把 layout 转成扁平化的 chart items
    chart_items: list[dict] = []
    for row in layout:
        for item in getattr(row, "items", []) or []:
            # chart_type 可能是枚举，统一转成字符串值
            raw_ct = getattr(item, "chart_type", "bar")
            ct_str = raw_ct.value if hasattr(raw_ct, "value") else str(raw_ct)
            chart_items.append({
                "chart_type": ct_str,
                "title": getattr(item, "title", "") or f"图表 {len(chart_items) + 1}",
                "x_field": getattr(item, "x_field", ""),
                "y_field": getattr(item, "y_field", ""),
                "data_field": getattr(item, "data_field", ""),
                "aggregation": getattr(item, "aggregation", ""),
            })

    # 4. 区分 KPI 和 Chart
    chart_only_items = []
    for item in chart_items:
        ct = str(item.get("chart_type", "")).lower()
        if ct in {"kpi", "kpi_card"}:
            # KPI 卡片：尝试从数据提取
            label = item.get("title", "")
            value = ""
            if excel_data:
                field = item.get("data_field", "") or label
                aggr = item.get("aggregation", "").lower()
                if field in (excel_data[0] if excel_data else {}):
                    values = []
                    for row in reversed(excel_data):
                        raw = row.get(field)
                        if raw is not None and raw != "" and raw != 0:
                            try:
                                num = float(str(raw).replace(",", "").replace("¥", "").replace("%", "").strip())
                                values.append(num)
                            except (ValueError, TypeError):
                                pass
                    if aggr == "sum":
                        total = sum(values)
                        if any(kw in label.lower() for kw in ["率", "占比", "%"]):
                            value = f"{total:.1f}%"
                        elif any(kw in label for kw in ["¥", "收入", "金额", "销售额", "利润"]):
                            value = f"¥{total:,.0f}" if abs(total) >= 10000 else f"¥{total:,.2f}"
                        else:
                            value = f"{total:,.0f}"
                    elif values:
                        # 默认取最后一个非空值
                        num = values[0]
                        if any(kw in label.lower() for kw in ["率", "占比", "%"]):
                            value = f"{num:.1f}%"
                        elif any(kw in label for kw in ["¥", "收入", "金额", "销售额", "利润"]):
                            value = f"¥{num:,.0f}" if abs(num) >= 10000 else f"¥{num:,.2f}"
                        else:
                            value = f"{num:,.0f}"
            kpi_cards.append({"label": label, "value": value or "—"})
        else:
            chart_only_items.append(item)

    # 5. 生成每个 chart 的 option
    for item in chart_only_items:
        ct = str(item.get("chart_type", "bar")).lower().replace("map:", "map")
        x_field = item.get("x_field", "")
        y_field = item.get("y_field", "")
        data_field = item.get("data_field", "")

        # 自动选择 x/y field（如果 spec 没指定）
        if not x_field and excel_data and excel_data:
            cols = list(excel_data[0].keys())
            x_field = next((c for c in cols if any(kw in c.lower() for kw in ["month", "date", "category", "name", "type", "月", "日期", "类别", "名称"])), cols[0] if cols else "")
        if not y_field and excel_data:
            cols = list(excel_data[0].keys())
            y_field = next((c for c in cols if any(kw in c.lower() for kw in ["value", "amount", "count", "sales", "值", "金额", "数量", "销售"])), "")

        # 处理地图类型
        if ct in {"map", "map_china", "map_world"}:
            # 地图由 chart_registry 中的模板处理，这里简化处理
            chart_options.append(json.dumps({
                "title": {"text": item.get("title", ""), "left": "left"},
                "backgroundColor": "transparent",
            }))
            continue

        # 数据筛选
        data = excel_data or []
        # 处理 y_field：逗号分隔 → 多系列
        if isinstance(y_field, str) and "," in y_field:
            y_fields_list = [f.strip() for f in y_field.split(",") if f.strip()]
        else:
            y_fields_list = []

        # 单系列聚合（按 x_field 分组，仅当 y_field 是单字段且 chart_type 需要分组）
        if y_fields_list:
            # 多字段（如 scatter 的 x/y）：不聚合，传原始数据
            pass
        elif data and x_field and y_field and isinstance(y_field, str):
            # 单系列：按 x_field 聚合 y_field
            aggregated: dict[str, float] = {}
            for row in data:
                key = str(row.get(x_field, "")).strip()
                if not key:
                    continue
                raw = row.get(y_field)
                if raw is None or raw == "" or raw == 0:
                    continue
                try:
                    val = float(str(raw).replace(",", "").replace("¥", "").replace("%", "").strip())
                    aggregated[key] = aggregated.get(key, 0.0) + val
                except (ValueError, TypeError):
                    pass
            data = [{x_field: k, y_field: v} for k, v in aggregated.items()]

        # 对多字段、或 scatter 等需要两轴的，把 y_field 转成 list
        final_y: str | list[str] = y_field
        if ct == "scatter" and y_fields_list:
            final_y = y_fields_list
        elif y_fields_list:
            final_y = y_fields_list

        option = build_chart_option(
            chart_type=ct if ct not in {"map_china", "map_world"} else "bar",
            title=item.get("title", ""),
            data=data,
            x_field=x_field,
            y_field=final_y,
            chart_palette=chart_palette,
            css_vars=css_vars,
        )
        chart_options.append(option)

    # 6. 拼装 HTML
    return build_html(
        title=title,
        chart_options=chart_options,
        kpi_cards=kpi_cards,
        css_vars=css_vars,
        deployment_mode=deployment_mode,
    )