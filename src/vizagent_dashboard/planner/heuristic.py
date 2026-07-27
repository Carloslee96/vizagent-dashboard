"""根据 Inventory 和明确需求生成可复现的 DashboardSpec。

该规划器不是自然语言大模型。它负责 CLI 的无 Key 兜底路径，并保证每个有效
Sheet 至少有一个可视化载体。Agent Skill 模式可在其结果上进一步修订 Spec。
"""

from __future__ import annotations

import re
from typing import Any

from vizagent_dashboard.compiler.charts import select_chart_type_by_hint
from vizagent_dashboard.inventory.spec import DataInventory, SheetInfo
from vizagent_dashboard.schemas.dashboard_spec import ChartItem, ChartType, DashboardSpec, LayoutRow, PageMode

_TIME_WORDS = ("日期", "时间", "月份", "年月", "季度", "周", "date", "time", "month", "year")
_GEO_WORDS = ("地区", "区域", "省份", "省", "城市", "region", "province", "country")
_LONGITUDE_WORDS = ("经度", "longitude", "lng", "lon")
_LATITUDE_WORDS = ("纬度", "latitude", "lat")
_RATIO_WORDS = ("占比", "比例", "百分比", "率", "ratio", "percent", "%")


def plan_dashboard(
    inventory: DataInventory,
    sheets: dict[str, list[dict[str, Any]]],
    requirement: str = "",
    theme: str | None = None,
    page_mode: str | None = None,
) -> DashboardSpec:
    """为所有有效 Sheet 生成一份覆盖完整的基础 Spec。"""

    normalized_requirement = requirement.strip()
    selected_theme = theme or _infer_theme(normalized_requirement)
    selected_mode = _infer_page_mode(normalized_requirement, page_mode)
    kpis: list[ChartItem] = []
    maps: list[ChartItem] = []
    charts: list[ChartItem] = []

    for sheet in inventory.sheets:
        rows = sheets.get(sheet.name, [])
        if not rows or not sheet.columns:
            continue
        numeric = [column.name for column in sheet.columns if column.dtype == "numeric"]
        dimensions = [column.name for column in sheet.columns if column.dtype in {"categorical", "text", "date"}]

        if _is_metric_sheet(sheet, rows, numeric, dimensions):
            dimension = dimensions[0]
            value_field = numeric[0]
            for row in rows:
                label = str(row.get(dimension, "")).strip()
                if not label:
                    continue
                kpis.append(
                    ChartItem(
                        chart_type=ChartType.kpi,
                        title=label,
                        data_sheet=sheet.name,
                        data_field=value_field,
                        aggregation="sum",
                        filters={dimension: row.get(dimension)},
                    )
                )
            continue

        item = _plan_sheet_chart(sheet, rows, numeric, dimensions, normalized_requirement)
        if item.chart_type in {ChartType.map_china, ChartType.map_world}:
            maps.append(item)
        else:
            charts.append(item)

    layout: list[LayoutRow] = []
    for start in range(0, len(kpis), 4):
        chunk = kpis[start : start + 4]
        layout.append(LayoutRow(title="核心指标", columns=max(1, len(chunk)), items=chunk))
    if maps:
        layout.append(LayoutRow(title="地域分布", columns=2, items=maps))
    for start in range(0, len(charts), 4):
        chunk = charts[start : start + 4]
        layout.append(LayoutRow(title="多维分析", columns=max(1, len(chunk)), items=chunk))

    title = _infer_title(normalized_requirement)
    return DashboardSpec(
        title=title,
        theme=selected_theme,
        page_mode=selected_mode,
        layout=layout,
        metadata={
            "planner": "deterministic-inventory-v1",
            "requirement": normalized_requirement,
            "source_sha256": inventory.source_sha256,
        },
    )


def _plan_sheet_chart(
    sheet: SheetInfo,
    rows: list[dict[str, Any]],
    numeric: list[str],
    dimensions: list[str],
    requirement: str,
) -> ChartItem:
    names = [column.name for column in sheet.columns]
    longitude = _find_field(names, _LONGITUDE_WORDS)
    latitude = _find_field(names, _LATITUDE_WORDS)
    geographic = _find_field(names, _GEO_WORDS)
    time_field = _find_field(names, _TIME_WORDS)
    dimension = time_field or geographic or (dimensions[0] if dimensions else names[0])
    values = numeric[:3]
    value_field = values[0] if values else ""
    lower_sheet = sheet.name.lower()
    map_requested = "地图" in requirement or "map" in requirement.lower()

    if longitude and latitude and values and (map_requested or any(word in lower_sheet for word in ("海外", "全球", "世界"))):
        metric = next((field for field in values if field not in {longitude, latitude}), values[-1])
        return ChartItem(
            chart_type=ChartType.map_world,
            title=f"{sheet.name}（世界地图）",
            data_sheet=sheet.name,
            x_field=dimensions[0] if dimensions else "",
            y_field=metric,
            longitude_field=longitude,
            latitude_field=latitude,
            width=2,
            height=2,
        )

    if geographic and values and (map_requested or any(word in lower_sheet for word in ("地域", "地区", "省份", "中国"))):
        return ChartItem(
            chart_type=ChartType.map_china,
            title=f"{sheet.name}（中国地图）",
            data_sheet=sheet.name,
            x_field=geographic,
            y_field=value_field,
            width=2,
            height=2,
        )

    explicit = _explicit_chart_type(requirement)
    if explicit:
        chart_type = explicit
    elif time_field and values:
        chart_type = _hint_type("time_series", ChartType.line)
    elif values and any(word in value_field.lower() for word in _RATIO_WORDS) and len(rows) <= 12:
        chart_type = _hint_type("composition", ChartType.pie)
    elif values:
        chart_type = _hint_type("comparison", ChartType.bar)
    else:
        chart_type = ChartType.table

    title_suffix = {
        ChartType.line: "趋势",
        ChartType.pie: "构成",
        ChartType.bar: "对比",
        ChartType.scatter: "分布",
        ChartType.table: "明细",
    }.get(chart_type, "分析")
    return ChartItem(
        chart_type=chart_type,
        title=f"{sheet.name}{title_suffix}",
        data_sheet=sheet.name,
        x_field=dimension,
        y_field=values if len(values) > 1 and chart_type in {ChartType.line, ChartType.bar} else value_field,
        width=1,
        height=1,
    )


def _is_metric_sheet(
    sheet: SheetInfo,
    rows: list[dict[str, Any]],
    numeric: list[str],
    dimensions: list[str],
) -> bool:
    name_match = any(word in sheet.name.lower() for word in ("核心指标", "关键指标", "概览", "summary", "kpi"))
    return bool(numeric and dimensions and len(rows) <= 8 and (name_match or "指标" in dimensions[0]))


def _find_field(fields: list[str], words: tuple[str, ...]) -> str:
    return next((field for field in fields if any(word in field.lower() for word in words)), "")


def _explicit_chart_type(requirement: str) -> ChartType | None:
    if "只展示" not in requirement and "仅展示" not in requirement:
        return None
    patterns = (
        (("饼图", "环图", "占比"), ChartType.pie),
        (("南丁格尔", "玫瑰图"), ChartType.nightingale),
        (("矩形树图", "树图"), ChartType.treemap),
        (("漏斗", "转化"), ChartType.funnel),
        (("仪表盘", "进度"), ChartType.gauge),
        (("雷达",), ChartType.radar),
        (("热力",), ChartType.heatmap),
        (("散点",), ChartType.scatter),
        (("折线", "趋势"), ChartType.line),
        (("面积",), ChartType.area),
        (("柱状", "条形", "排行"), ChartType.bar),
        (("表格", "明细"), ChartType.table),
    )
    return next((chart_type for words, chart_type in patterns if any(word in requirement for word in words)), None)


def _hint_type(hint: str, fallback: ChartType) -> ChartType:
    """按 data_hints 从注册表选型；无匹配回退 fallback（保行为不变）。"""
    chart_type = select_chart_type_by_hint(hint)
    return ChartType(chart_type) if chart_type else fallback


def _infer_theme(requirement: str) -> str:
    if any(word in requirement for word in ("浅色", "明亮", "纸张", "白色")):
        return "paper-light"
    return "midnight-ops"


def _infer_page_mode(requirement: str, explicit: str | None) -> PageMode:
    if explicit:
        return PageMode(explicit)
    if any(word in requirement for word in ("分页", "多页签", "多个页签")):
        return PageMode.tabs
    return PageMode.single_page


def _infer_title(requirement: str) -> str:
    if not requirement:
        return "数据分析大屏"
    cleaned = re.sub(r"\s+", " ", requirement).strip("，。；; ")
    if len(cleaned) > 28:
        cleaned = cleaned[:28].rstrip("，, ") + "…"
    return cleaned or "数据分析大屏"
