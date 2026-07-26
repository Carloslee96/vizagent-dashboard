"""DashboardSpec → 离线单文件 HTML 的确定性编译器。"""

from __future__ import annotations

import html
import json
import re
from dataclasses import dataclass
from importlib.resources import files
from typing import Any

from pydantic import BaseModel

from vizagent_dashboard.compiler.chart_options import build_chart_option
from vizagent_dashboard.compiler.themes import load_theme, resolve_theme_id
from vizagent_dashboard.inventory.spec import DataInventory
from vizagent_dashboard.schemas.dashboard_spec import ChartItem, ChartType, DashboardSpec, PageMode


@dataclass
class CompiledDashboard:
    html: str
    manifest: dict[str, Any]
    chart_options: list[dict[str, Any]]


def parse_design_tokens(markdown: str) -> dict[str, Any]:
    """从主题 Markdown 表格解析 CSS token 和图表调色板。"""

    css_vars: dict[str, str] = {}
    palette: list[str] = []
    for line in markdown.splitlines():
        token_match = re.search(r"`(--[\w-]+)`\s*\|\s*`([^`]+)`", line)
        if token_match:
            css_vars[token_match.group(1)] = token_match.group(2).strip()

    in_chart_palette = False
    for line in markdown.splitlines():
        if line.startswith("## Chart Color Palette"):
            in_chart_palette = True
            continue
        if in_chart_palette and line.startswith("## "):
            break
        if in_chart_palette:
            for color in re.findall(r"#[0-9a-fA-F]{6}", line):
                if color not in palette:
                    palette.append(color)

    if not palette:
        palette = ["#4F8CFF", "#45C486", "#F2B84B", "#B47BE8", "#4CC9D9"]
    return {"css_vars": css_vars, "chart_palette": palette}


def extract_theme_fonts(css_vars: dict[str, str]) -> list[tuple[str, str]]:
    font_family = css_vars.get("--font-family-display", "")
    if not font_family:
        return []
    return [(font_family, font_family.split(",")[0].strip().strip("'").strip('"'))]


def build_css_block(css_vars: dict[str, str]) -> str:
    """构建响应式网格、地图焦点位和深浅主题通用 CSS。"""

    declarations = "\n".join(f"  {name}: {value};" for name, value in sorted(css_vars.items()))
    values = {
        "bg": css_vars.get("--bg-primary", "#0f1115"),
        "card": css_vars.get("--bg-card", css_vars.get("--bg-secondary", "#171a20")),
        "elevated": css_vars.get("--bg-elevated", "#1d2129"),
        "text": css_vars.get("--text-primary", "#edf0f5"),
        "muted": css_vars.get("--text-secondary", "#939baa"),
        "border": css_vars.get("--border-subtle", "#2b313b"),
        "accent": css_vars.get("--accent-primary", "#4f8cff"),
        "font": css_vars.get("--font-family-base", "system-ui, sans-serif"),
        "display": css_vars.get("--font-family-display", "system-ui, sans-serif"),
        "radius": css_vars.get("--radius-card", "10px"),
    }
    template = """
:root {
__DECLARATIONS__
}
* { box-sizing: border-box; }
html, body { margin: 0; min-height: 100%; }
body {
  background: __BG__;
  color: __TEXT__;
  font-family: __FONT__;
  font-size: 14px;
}
button { font: inherit; }
.dashboard {
  width: min(100%, 1920px);
  min-height: 100vh;
  margin: 0 auto;
  padding: 20px 24px 24px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.dashboard-header {
  min-height: 48px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  border-bottom: 1px solid __BORDER__;
}
.dashboard-title {
  margin: 0;
  font-family: __DISPLAY__;
  font-size: clamp(22px, 1.7vw, 32px);
  line-height: 1.2;
}
.dashboard-meta { color: __MUTED__; font-size: 12px; }
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(var(--columns, 4), minmax(0, 1fr));
  gap: 12px;
}
.kpi-card, .panel {
  background: __CARD__;
  border: 1px solid __BORDER__;
  border-radius: __RADIUS__;
  min-width: 0;
}
.kpi-card { min-height: 96px; padding: 15px 18px; }
.kpi-label { color: __MUTED__; font-size: 12px; margin-bottom: 6px; }
.kpi-value {
  font-family: __DISPLAY__;
  font-variant-numeric: tabular-nums;
  font-size: clamp(26px, 2vw, 38px);
  font-weight: 700;
  line-height: 1.1;
}
.visual-grid {
  flex: 1;
  min-height: 0;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  grid-auto-rows: minmax(210px, 1fr);
  gap: 12px;
}
.panel {
  min-height: 0;
  padding: 14px 16px 12px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.panel.span-2 { grid-column: span 2; }
.panel.span-3 { grid-column: span 3; }
.panel.span-4 { grid-column: span 4; }
.panel.tall-2 { grid-row: span 2; }
.panel.tall-3 { grid-row: span 3; }
.panel-title {
  margin: 0 0 8px;
  font-size: 15px;
  line-height: 1.3;
  font-weight: 650;
}
.chart-container { width: 100%; min-height: 0; flex: 1; }
.chart-container[hidden] { display: none; }
.map-tabs, .page-tabs {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 8px;
}
.tab-button {
  border: 1px solid __BORDER__;
  border-radius: 6px;
  padding: 5px 10px;
  color: __MUTED__;
  background: transparent;
  cursor: pointer;
}
.tab-button.active {
  color: __TEXT__;
  border-color: __ACCENT__;
  background: color-mix(in srgb, __ACCENT__ 12%, transparent);
}
.page-panel { display: none; flex: 1; min-height: 0; }
.page-panel.active { display: flex; }
.page-panel > .visual-grid { width: 100%; }
.table-wrap { overflow: auto; flex: 1; min-height: 0; }
table { width: 100%; border-collapse: collapse; font-size: 12px; }
th, td { padding: 8px 10px; border-bottom: 1px solid __BORDER__; text-align: left; }
th { color: __MUTED__; position: sticky; top: 0; background: __CARD__; }
.empty-state { color: __MUTED__; display: grid; place-items: center; height: 100%; }
@media (max-width: 1200px) {
  .visual-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .panel.span-3, .panel.span-4 { grid-column: span 2; }
}
@media (max-width: 760px) {
  .dashboard { padding: 14px; }
  .kpi-grid, .visual-grid { grid-template-columns: 1fr; }
  .panel.span-2, .panel.span-3, .panel.span-4 { grid-column: span 1; }
  .panel.tall-2, .panel.tall-3 { grid-row: span 1; }
}
"""
    return (
        template.replace("__DECLARATIONS__", declarations)
        .replace("__BG__", values["bg"])
        .replace("__CARD__", values["card"])
        .replace("__ELEVATED__", values["elevated"])
        .replace("__TEXT__", values["text"])
        .replace("__MUTED__", values["muted"])
        .replace("__BORDER__", values["border"])
        .replace("__ACCENT__", values["accent"])
        .replace("__FONT__", values["font"])
        .replace("__DISPLAY__", values["display"])
        .replace("__RADIUS__", values["radius"])
    )


def compile_artifacts(
    spec: DashboardSpec,
    sheet_data: dict[str, list[dict[str, Any]]] | list[dict[str, Any]] | None = None,
    theme_id: str | None = None,
    deployment_mode: str = "embedded",
    inventory: DataInventory | None = None,
) -> CompiledDashboard:
    """编译 HTML，并返回数据覆盖和图表契约清单。"""

    sheets = _normalize_sheet_data(sheet_data)
    chosen_theme = _resolve_theme(theme_id or spec.theme or "midnight-ops")
    theme_markdown = load_theme(chosen_theme) or load_theme("midnight-ops")
    tokens = parse_design_tokens(theme_markdown)
    css_vars = tokens["css_vars"]
    palette = tokens["chart_palette"]

    coverage_indices: dict[str, set[int]] = {name: set() for name in sheets}
    coverage_fields: dict[str, set[str]] = {name: set() for name in sheets}
    kpis: list[dict[str, Any]] = []
    visuals: list[dict[str, Any]] = []
    options: list[dict[str, Any]] = []
    map_assets: set[str] = set()

    for row in spec.layout:
        for item in row.items:
            rows, sheet_name = _rows_for_item(item, sheets)
            filtered_rows, original_indices = _filter_rows(rows, item.filters)
            chart_type = item.chart_type.value

            if item.chart_type == ChartType.kpi:
                used = _valid_indices_for_fields(filtered_rows, original_indices, [item.data_field])
                coverage_indices.setdefault(sheet_name, set()).update(used)
                coverage_fields.setdefault(sheet_name, set()).add(item.data_field)
                kpis.append(
                    {
                        "title": item.title or item.data_field,
                        "value": _aggregate_kpi(filtered_rows, item.data_field, item.aggregation),
                        "sheet": sheet_name,
                    }
                )
                continue

            dom_id = f"viz-chart-{len(options)}"
            required_fields = _item_fields(item)
            used = _valid_indices_for_fields(filtered_rows, original_indices, required_fields, any_value=True)
            coverage_indices.setdefault(sheet_name, set()).update(used)
            coverage_fields.setdefault(sheet_name, set()).update(field for field in required_fields if field)

            if item.chart_type in {ChartType.map_china, ChartType.map_world}:
                map_id = "china" if item.chart_type == ChartType.map_china else "world"
                option = _build_map_option(item, filtered_rows, css_vars, palette, map_id)
                map_assets.add(map_id)
            elif item.chart_type == ChartType.table:
                option = {}
            else:
                chart_rows = _prepare_chart_rows(item, filtered_rows)
                option = json.loads(
                    build_chart_option(
                        chart_type=chart_type,
                        title="",
                        data=chart_rows,
                        x_field=item.x_field,
                        y_field=item.y_field,
                        chart_palette=palette,
                        css_vars=css_vars,
                    )
                )
                option.pop("title", None)

            entry = {
                "dom_id": dom_id,
                "title": item.title or f"{sheet_name}分析",
                "type": chart_type,
                "sheet": sheet_name,
                "fields": required_fields,
                "width": item.width,
                "height": item.height,
                "option": option,
                "table_rows": filtered_rows if item.chart_type == ChartType.table else [],
            }
            visuals.append(entry)
            if item.chart_type != ChartType.table:
                options.append(
                    {
                        "dom_id": dom_id,
                        "type": chart_type,
                        "sheet": sheet_name,
                        "option": option,
                    }
                )

    coverage: dict[str, Any] = {}
    for sheet_name, rows in sheets.items():
        covered = coverage_indices.get(sheet_name, set())
        coverage[sheet_name] = {
            "total_rows": len(rows),
            "covered_rows": len(covered),
            "fields": sorted(coverage_fields.get(sheet_name, set())),
            "complete": len(rows) == len(covered),
        }

    manifest = {
        "version": "1.0",
        "spec_version": spec.version,
        "theme": chosen_theme,
        "page_mode": spec.page_mode.value,
        "source_sha256": inventory.source_sha256 if inventory else spec.metadata.get("source_sha256", ""),
        "visual_count": len(kpis) + len(visuals),
        "chart_count": len(options),
        "kpi_count": len(kpis),
        "maps": sorted(map_assets),
        "coverage": coverage,
        "coverage_complete": all(item["complete"] for item in coverage.values()),
    }
    html_content = _render_html(
        title=spec.title,
        kpis=kpis,
        visuals=visuals,
        options=options,
        css_vars=css_vars,
        map_assets=map_assets,
        manifest=manifest,
        page_mode=spec.page_mode,
        deployment_mode=deployment_mode,
    )
    return CompiledDashboard(html=html_content, manifest=manifest, chart_options=[entry["option"] for entry in options])


def compile_dashboard(
    spec: BaseModel,
    excel_data: dict[str, list[dict[str, Any]]] | list[dict[str, Any]] | None = None,
    theme_id: str | None = None,
    deployment_mode: str = "embedded",
) -> str:
    """兼容旧调用方的 HTML-only 编译入口。"""

    normalized = spec if isinstance(spec, DashboardSpec) else DashboardSpec.model_validate(spec.model_dump())
    return compile_artifacts(
        spec=normalized,
        sheet_data=excel_data,
        theme_id=theme_id,
        deployment_mode=deployment_mode,
    ).html


def build_html(
    title: str,
    chart_options: list[str],
    kpi_cards: list[dict[str, str]],
    css_vars: dict[str, str],
    deployment_mode: str = "embedded",
) -> str:
    """兼容旧单元测试和外部调用的低层 HTML 构建接口。"""

    visuals: list[dict[str, Any]] = []
    options: list[dict[str, Any]] = []
    for index, raw in enumerate(chart_options):
        option = json.loads(raw)
        option_title = str((option.get("title") or {}).get("text") or f"图表 {index + 1}")
        option.pop("title", None)
        dom_id = f"viz-chart-{index}"
        visuals.append(
            {
                "dom_id": dom_id,
                "title": option_title,
                "type": _option_type(option),
                "sheet": "",
                "fields": [],
                "width": 1,
                "height": 1,
                "option": option,
                "table_rows": [],
            }
        )
        options.append({"dom_id": dom_id, "type": _option_type(option), "sheet": "", "option": option})
    kpis = [{"title": item.get("label", ""), "value": item.get("value", ""), "sheet": ""} for item in kpi_cards]
    manifest = {
        "version": "1.0",
        "visual_count": len(kpis) + len(visuals),
        "chart_count": len(options),
        "kpi_count": len(kpis),
        "maps": [],
        "coverage": {},
        "coverage_complete": True,
    }
    return _render_html(
        title=title,
        kpis=kpis,
        visuals=visuals,
        options=options,
        css_vars=css_vars,
        map_assets=set(),
        manifest=manifest,
        page_mode=PageMode.single_page,
        deployment_mode=deployment_mode,
    )


def _render_html(
    *,
    title: str,
    kpis: list[dict[str, Any]],
    visuals: list[dict[str, Any]],
    options: list[dict[str, Any]],
    css_vars: dict[str, str],
    map_assets: set[str],
    manifest: dict[str, Any],
    page_mode: PageMode,
    deployment_mode: str,
) -> str:
    safe_title = html.escape(title)
    css = build_css_block(css_vars)
    kpi_columns = min(4, max(1, len(kpis)))
    kpi_html = "".join(
        (
            '<article class="kpi-card" data-viz-type="kpi" '
            f'data-viz-sheet="{html.escape(str(item["sheet"]))}">'
            f'<div class="kpi-label">{html.escape(str(item["title"]))}</div>'
            f'<div class="kpi-value">{html.escape(str(item["value"]))}</div>'
            "</article>"
        )
        for item in kpis
    )

    maps = [entry for entry in visuals if entry["type"] in {"map_china", "map_world"}]
    ordinary = [entry for entry in visuals if entry["type"] not in {"map_china", "map_world"}]
    panels: list[str] = []
    if maps:
        panels.append(_render_map_panel(maps))
    panels.extend(_render_panel(entry) for entry in ordinary)

    page_tabs = ""
    if page_mode == PageMode.tabs and len(panels) > 4:
        chunks = [panels[index : index + 4] for index in range(0, len(panels), 4)]
        buttons = "".join(
            f'<button class="tab-button page-tab{" active" if index == 0 else ""}" '
            f'data-page-target="viz-page-{index}">第 {index + 1} 页</button>'
            for index in range(len(chunks))
        )
        pages = "".join(
            f'<section id="viz-page-{index}" class="page-panel{" active" if index == 0 else ""}">'
            f'<div class="visual-grid">{"".join(chunk)}</div></section>'
            for index, chunk in enumerate(chunks)
        )
        page_tabs = f'<nav class="page-tabs" aria-label="大屏页签">{buttons}</nav>{pages}'
    else:
        page_tabs = f'<div class="visual-grid">{"".join(panels)}</div>'

    option_json = _json_script(options)
    manifest_json = _json_script(manifest)
    map_scripts = ""
    for map_id in sorted(map_assets):
        resource = files("vizagent_dashboard.vendor").joinpath(f"{map_id}.json").read_text(encoding="utf-8")
        safe_resource = resource.replace("</", "<\\/")
        map_scripts += (
            f'<script type="application/json" id="viz-map-{map_id}">'
            f"{safe_resource}"
            "</script>"
        )

    if deployment_mode == "embedded":
        runtime = files("vizagent_dashboard.vendor").joinpath("echarts.min.js").read_text(encoding="utf-8")
        safe_runtime = runtime.replace("</script", "<\\/script")
        echarts_script = f"<script>{safe_runtime}</script>"
        csp = "default-src 'none'; script-src 'unsafe-inline' 'unsafe-eval'; style-src 'unsafe-inline'; img-src data:; font-src data:; connect-src 'none'"
    elif deployment_mode == "cdn":
        echarts_script = '<script src="https://cdn.jsdelivr.net/npm/echarts@5.5.1/dist/echarts.min.js"></script>'
        csp = "default-src 'none'; script-src 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; style-src 'unsafe-inline'; img-src data:; connect-src 'none'"
    else:
        raise ValueError("deployment_mode 仅支持 embedded 或 cdn")

    template = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Content-Security-Policy" content="__CSP__">
  <title>__TITLE__</title>
  <style>__CSS__</style>
</head>
<body>
  <main class="dashboard">
    <header class="dashboard-header">
      <h1 class="dashboard-title">__TITLE__</h1>
      <span class="dashboard-meta">VizAgent · Offline</span>
    </header>
    <section class="kpi-grid" style="--columns: __KPI_COLUMNS__">__KPIS__</section>
    __PAGES__
  </main>
  <script type="application/json" id="vizagent-chart-options">__OPTIONS__</script>
  <script type="application/json" id="vizagent-build-manifest">__MANIFEST__</script>
  __MAPS__
  __ECHARTS__
  <script>
  (() => {
    const entries = JSON.parse(document.getElementById('vizagent-chart-options').textContent);
    const byId = new Map(entries.map(entry => [entry.dom_id, entry]));
    const instances = new Map();
    for (const mapId of ['china', 'world']) {
      const source = document.getElementById(`viz-map-${mapId}`);
      if (source) echarts.registerMap(mapId, JSON.parse(source.textContent));
    }
    function initVisible() {
      document.querySelectorAll('.chart-container:not([hidden])').forEach(node => {
        if (!node.offsetParent || instances.has(node.id)) return;
        const entry = byId.get(node.id);
        if (!entry) return;
        const chart = echarts.init(node);
        chart.setOption(entry.option);
        instances.set(node.id, chart);
      });
    }
    function activate(button, selector, targetAttribute) {
      const target = button.getAttribute(targetAttribute);
      const scope = button.closest('.panel') || document;
      scope.querySelectorAll(selector).forEach(node => {
        const active = node.id === target;
        if (node.classList.contains('chart-container')) node.hidden = !active;
        else node.classList.toggle('active', active);
      });
      button.parentElement.querySelectorAll('.tab-button').forEach(item => item.classList.toggle('active', item === button));
      requestAnimationFrame(() => {
        initVisible();
        const chart = instances.get(target);
        if (chart) chart.resize();
      });
    }
    document.querySelectorAll('.map-tab').forEach(button => button.addEventListener('click', () => activate(button, '.chart-container', 'data-map-target')));
    document.querySelectorAll('.page-tab').forEach(button => button.addEventListener('click', () => activate(button, '.page-panel', 'data-page-target')));
    initVisible();
    const observer = new ResizeObserver(entries => {
      for (const entry of entries) {
        const chart = instances.get(entry.target.id);
        if (chart) chart.resize();
      }
    });
    document.querySelectorAll('.chart-container').forEach(node => observer.observe(node));
    window.addEventListener('resize', () => instances.forEach(chart => chart.resize()));
  })();
  </script>
</body>
</html>
"""
    return (
        template.replace("__CSP__", csp)
        .replace("__TITLE__", safe_title)
        .replace("__CSS__", css)
        .replace("__KPI_COLUMNS__", str(kpi_columns))
        .replace("__KPIS__", kpi_html)
        .replace("__PAGES__", page_tabs)
        .replace("__OPTIONS__", option_json)
        .replace("__MANIFEST__", manifest_json)
        .replace("__MAPS__", map_scripts)
        .replace("__ECHARTS__", echarts_script)
    )


def _render_panel(entry: dict[str, Any]) -> str:
    panel_class = f'panel span-{entry["width"]} tall-{entry["height"]}'
    attributes = (
        f'data-viz-type="{html.escape(entry["type"])}" '
        f'data-viz-sheet="{html.escape(entry["sheet"])}"'
    )
    if entry["type"] == "table":
        rows = entry["table_rows"]
        if not rows:
            content = '<div class="empty-state">暂无数据</div>'
        else:
            columns = list(rows[0].keys())
            head = "".join(f"<th>{html.escape(str(column))}</th>" for column in columns)
            body = "".join(
                "<tr>" + "".join(f"<td>{html.escape(str(row.get(column, '')))}</td>" for column in columns) + "</tr>"
                for row in rows[:200]
            )
            content = f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'
    else:
        content = f'<div id="{entry["dom_id"]}" class="chart-container"></div>'
    return (
        f'<article class="{panel_class}" {attributes}>'
        f'<h2 class="panel-title">{html.escape(entry["title"])}</h2>{content}</article>'
    )


def _render_map_panel(entries: list[dict[str, Any]]) -> str:
    buttons = "".join(
        f'<button class="tab-button map-tab{" active" if index == 0 else ""}" '
        f'data-map-target="{entry["dom_id"]}">'
        f'{"中国地图" if entry["type"] == "map_china" else "世界地图"}</button>'
        for index, entry in enumerate(entries)
    )
    canvases = "".join(
        f'<div id="{entry["dom_id"]}" class="chart-container"{" hidden" if index else ""}></div>'
        for index, entry in enumerate(entries)
    )
    sheets = ",".join(entry["sheet"] for entry in entries)
    return (
        f'<article class="panel span-2 tall-2" data-viz-type="map-tabs" data-viz-sheet="{html.escape(sheets)}">'
        '<h2 class="panel-title">全球与中国连接分布</h2>'
        f'<nav class="map-tabs" aria-label="地图切换">{buttons}</nav>{canvases}</article>'
    )


def _build_map_option(
    item: ChartItem,
    rows: list[dict[str, Any]],
    css_vars: dict[str, str],
    palette: list[str],
    map_id: str,
) -> dict[str, Any]:
    text = css_vars.get("--text-primary", "#edf0f5")
    muted = css_vars.get("--text-secondary", "#939baa")
    boundary = css_vars.get("--map-boundary", css_vars.get("--border-strong", "#5f6b7a"))
    area = css_vars.get("--map-area", css_vars.get("--bg-elevated", "#252b35"))
    emphasis = css_vars.get("--accent-primary", palette[0])
    metric = item.y_field[0] if isinstance(item.y_field, list) and item.y_field else str(item.y_field)

    if map_id == "world" and item.longitude_field and item.latitude_field:
        points = []
        for row in rows:
            longitude = _to_number(row.get(item.longitude_field))
            latitude = _to_number(row.get(item.latitude_field))
            value = _to_number(row.get(metric))
            if longitude is None or latitude is None or value is None:
                continue
            points.append(
                {
                    "name": str(row.get(item.x_field, "")),
                    "value": [longitude, latitude, value],
                }
            )
        return {
            "backgroundColor": "transparent",
            "tooltip": {"trigger": "item"},
            "geo": {
                "map": "world",
                "roam": True,
                "silent": False,
                "itemStyle": {"areaColor": area, "borderColor": boundary, "borderWidth": 1},
                "emphasis": {"itemStyle": {"areaColor": emphasis}, "label": {"color": text}},
            },
            "visualMap": {
                "show": True,
                "min": min((point["value"][2] for point in points), default=0),
                "max": max((point["value"][2] for point in points), default=1),
                "dimension": 2,
                "left": 4,
                "bottom": 4,
                "textStyle": {"color": muted},
                "inRange": {"color": [palette[1 % len(palette)], palette[0]]},
            },
            "series": [
                {
                    "type": "effectScatter",
                    "coordinateSystem": "geo",
                    "data": points,
                    "symbolSize": 9,
                    "rippleEffect": {"scale": 2.5},
                    "itemStyle": {"color": palette[2 % len(palette)]},
                }
            ],
        }

    data = []
    for row in rows:
        name = _normalize_china_region(str(row.get(item.x_field, ""))) if map_id == "china" else str(row.get(item.x_field, ""))
        value = _to_number(row.get(metric))
        if name and value is not None:
            data.append({"name": name, "value": value})
    return {
        "backgroundColor": "transparent",
        "tooltip": {"trigger": "item"},
        "visualMap": {
            "show": True,
            "min": min((item["value"] for item in data), default=0),
            "max": max((item["value"] for item in data), default=1),
            "left": 4,
            "bottom": 4,
            "textStyle": {"color": muted},
            "inRange": {"color": [area, palette[0]]},
        },
        "series": [
            {
                "type": "map",
                "map": map_id,
                "roam": True,
                "data": data,
                "label": {"show": False, "color": text},
                "itemStyle": {"areaColor": area, "borderColor": boundary, "borderWidth": 1},
                "emphasis": {"label": {"show": True}, "itemStyle": {"areaColor": emphasis}},
            }
        ],
    }


def _normalize_sheet_data(
    data: dict[str, list[dict[str, Any]]] | list[dict[str, Any]] | None,
) -> dict[str, list[dict[str, Any]]]:
    if data is None:
        return {}
    if isinstance(data, list):
        return {"Sheet1": data}
    return data


def _resolve_theme(theme_id: str) -> str:
    """主题 ID 规范化：别名解析到规范 ID，未知值回退到 midnight-ops。"""

    return resolve_theme_id(theme_id) or "midnight-ops"


def _rows_for_item(
    item: ChartItem,
    sheets: dict[str, list[dict[str, Any]]],
) -> tuple[list[dict[str, Any]], str]:
    if item.data_sheet:
        return sheets.get(item.data_sheet, []), item.data_sheet
    if not sheets:
        return [], ""
    first = next(iter(sheets))
    return sheets[first], first


def _filter_rows(
    rows: list[dict[str, Any]],
    filters: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[int]]:
    selected: list[dict[str, Any]] = []
    indices: list[int] = []
    for index, row in enumerate(rows):
        if all(row.get(field) == expected for field, expected in filters.items()):
            selected.append(row)
            indices.append(index)
    return selected, indices


def _item_fields(item: ChartItem) -> list[str]:
    y_fields = item.y_field if isinstance(item.y_field, list) else [item.y_field]
    return list(
        dict.fromkeys(
            field
            for field in (
                item.x_field,
                *y_fields,
                item.data_field,
                item.longitude_field,
                item.latitude_field,
            )
            if field
        )
    )


def _valid_indices_for_fields(
    rows: list[dict[str, Any]],
    original_indices: list[int],
    fields: list[str],
    any_value: bool = False,
) -> set[int]:
    if not fields:
        return set(original_indices)
    used: set[int] = set()
    for row, original_index in zip(rows, original_indices):
        values = [row.get(field) not in (None, "") for field in fields if field]
        if values and (any(values) if any_value else all(values)):
            used.add(original_index)
    return used


def _aggregate_kpi(rows: list[dict[str, Any]], field: str, aggregation: str | None) -> str:
    values = [number for row in rows if (number := _to_number(row.get(field))) is not None]
    if not values:
        return "—"
    operation = (aggregation or "last").lower()
    if operation == "sum":
        value = sum(values)
    elif operation in {"avg", "average", "mean"}:
        value = sum(values) / len(values)
    elif operation == "max":
        value = max(values)
    elif operation == "min":
        value = min(values)
    elif operation == "count":
        value = float(len(values))
    else:
        value = values[-1]
    return f"{value:,.2f}".rstrip("0").rstrip(".")


def _prepare_chart_rows(item: ChartItem, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if item.chart_type in {ChartType.scatter, ChartType.table}:
        return rows
    y_fields = item.y_field if isinstance(item.y_field, list) else [item.y_field]
    y_fields = [field for field in y_fields if field]
    if not item.x_field or not y_fields:
        return rows
    grouped: dict[str, dict[str, Any]] = {}
    for row in rows:
        category = str(row.get(item.x_field, "")).strip()
        if not category:
            continue
        target = grouped.setdefault(category, {item.x_field: category})
        for field in y_fields:
            number = _to_number(row.get(field))
            if number is not None:
                target[field] = float(target.get(field, 0)) + number
    return list(grouped.values())


def _to_number(value: Any) -> float | None:
    try:
        text = str(value).replace(",", "").replace("¥", "").replace("$", "").replace("%", "").strip()
        return float(text) if text else None
    except (TypeError, ValueError):
        return None


def _normalize_china_region(name: str) -> str:
    value = name.strip()
    replacements = {
        "内蒙古自治区": "内蒙古",
        "广西壮族自治区": "广西",
        "西藏自治区": "西藏",
        "宁夏回族自治区": "宁夏",
        "新疆维吾尔自治区": "新疆",
        "香港特别行政区": "香港",
        "澳门特别行政区": "澳门",
    }
    if value in replacements:
        return replacements[value]
    return re.sub(r"(省|市)$", "", value)


def _option_type(option: dict[str, Any]) -> str:
    series = option.get("series") or []
    if series and isinstance(series[0], dict):
        return str(series[0].get("type") or "chart")
    return "chart"


def _json_script(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
