"""布局规划器（生成前页面组织预估与布局偏好规范化）。

从 viz-agent-team/backend/agents/layout_planner.py 提取（参考源码 commit 见 upstream-manifest.toml）。

该模块是「用户布局意图」的单一事实来源：
- 前端确认页用 estimate_layout_plan() 展示预计模块数与推荐方案；
- 流程入口和骨架布局统一使用 normalize_layout_mode()；
- 中国/世界地图合并为一个面板，但保留两个内部地图视图。

纯函数式，零 SaaS 依赖。
"""

from __future__ import annotations

import math
from typing import Any

LAYOUT_MODES = frozenset({"auto", "single_page", "tabs"})
SINGLE_PAGE_COMFORTABLE_MAX = 8
SINGLE_PAGE_HARD_MAX = 16
TAB_TARGET_SIZE = 7
GRID_GAP = 12
OUTER_HORIZONTAL_PADDING = 48
HEADER_WITH_KPI_RESERVED_HEIGHT = 256
HEADER_ONLY_RESERVED_HEIGHT = 112
MAP_PANEL_CHROME_HEIGHT = 52
STANDARD_PANEL_CHROME_HEIGHT = 44
MIN_MAP_CANVAS_HEIGHT = 320
MIN_STANDARD_CANVAS_HEIGHT = 140
MAX_SINGLE_PAGE_CONTENT_ROWS = 4

_MAP_TYPES = frozenset({"world_map", "china_map", "map"})
_WIDE_TYPES = frozenset({
    "line", "area", "table", "sankey", "parallel", "heatmap", "calendar",
})


def normalize_layout_mode(value: str | None) -> str:
    """归一化布局偏好；非法值回退 auto，禁止在各层重复发明兜底规则。"""
    mode = (value or "auto").strip().lower()
    return mode if mode in LAYOUT_MODES else "auto"


def _field_type(field: dict[str, Any]) -> str:
    return str(field.get("type") or field.get("inferred_use") or "").lower()


def _estimated_from_fields(data_fields: list[dict[str, Any]]) -> tuple[int, int]:
    """文本需求没有显式图表计划时，根据结构化字段做保守预估。"""
    numeric = [
        field for field in data_fields
        if _field_type(field) in {
            "number", "currency", "percentage", "metric", "metric_percent", "数值", "比率",
        }
    ]
    temporal = [
        field for field in data_fields
        if _field_type(field) in {"datetime", "time", "时间"}
    ]
    categories = [
        field for field in data_fields
        if _field_type(field) in {"text", "category", "dimension", "分类", "维度"}
    ]
    kpi_count = min(len(numeric), 4)
    chart_count = 0
    if numeric and temporal:
        chart_count += 1
    if numeric and categories:
        chart_count += 2
    if numeric and not (temporal or categories):
        chart_count = 1
    return kpi_count, chart_count


def _requirement_chart_count(requirement: str) -> int:
    """提取用户明确点名的图表类型数，仅作无结构化字段时的轻量兜底。"""
    keywords = (
        "折线", "柱状", "条形", "饼图", "环形", "雷达", "散点", "漏斗",
        "仪表", "树图", "词云", "热力", "桑基", "瀑布", "箱线", "地图",
        "表格", "明细",
    )
    return sum(1 for keyword in keywords if keyword in (requirement or ""))


def _normalize_series_type(value: str | None) -> str:
    """把前端目录类型归一成布局角色使用的稳定类型。"""
    series_type = (value or "chart").strip().lower()
    aliases = {
        "world_map": "map",
        "china_map": "map",
        "horizontal_bar": "bar",
        "stacked_bar": "bar",
        "nightingale": "pie",
        "donut": "pie",
        "rose": "pie",
    }
    return aliases.get(series_type, series_type)


def _visual_role(item: dict[str, Any]) -> str:
    """从图表语义派生视觉角色；布局属性不得散落到骨架渲染层。"""
    kind = str(item.get("kind") or "").lower()
    series_type = _normalize_series_type(
        str(item.get("series_type") or item.get("type") or "")
    )
    if kind == "map" or series_type == "map":
        return "focal"
    if kind == "table" or series_type in _WIDE_TYPES:
        return "wide"
    return "standard"


def _find_free_placement(
    occupied: list[list[bool]],
    *,
    col_span: int,
    row_span: int,
) -> tuple[int, int] | None:
    """寻找最靠近网格视觉中心的可用矩形，返回零基 row/column。"""
    rows = len(occupied)
    columns = len(occupied[0]) if rows else 0
    grid_center_x = columns / 2
    grid_center_y = rows / 2
    candidates: list[tuple[float, int, int]] = []
    for row in range(rows - row_span + 1):
        for column in range(columns - col_span + 1):
            if any(
                occupied[r][c]
                for r in range(row, row + row_span)
                for c in range(column, column + col_span)
            ):
                continue
            item_center_x = column + col_span / 2
            item_center_y = row + row_span / 2
            distance = (
                (item_center_x - grid_center_x) ** 2
                + (item_center_y - grid_center_y) ** 2
            )
            candidates.append((distance, row, column))
    if not candidates:
        return None
    _, row, column = min(candidates)
    return row, column


def _occupy(
    occupied: list[list[bool]],
    row: int,
    column: int,
    row_span: int,
    col_span: int,
) -> None:
    for r in range(row, row + row_span):
        for c in range(column, column + col_span):
            occupied[r][c] = True


def plan_single_page_grid(
    items: list[dict[str, Any]],
    *,
    screen_width: int = 1920,
    screen_height: int = 1080,
    kpi_count: int = 0,
) -> dict[str, Any]:
    """生成确定性的单页内容网格计划。

    地图是焦点模块，固定占 2×2；宽图只在网格仍有容量时扩为 2×1，
    普通图按 1×1 填充。输出同时供生成前预估与最终 HTML 骨架使用。
    """
    normalized: list[dict[str, Any]] = []
    for index, raw in enumerate(items):
        item = dict(raw)
        item["id"] = int(item.get("id") or index + 1)
        item["role"] = _visual_role(item)
        normalized.append(item)

    if not normalized:
        return {
            "columns": 1,
            "rows": 0,
            "placements": [],
            "feasible": True,
            "violations": [],
            "estimated_map_canvas_width": 0,
            "estimated_map_canvas_height": 0,
            "map_col_span": 0,
            "map_row_span": 0,
        }

    focal_items = [item for item in normalized if item["role"] == "focal"]
    ordinary_items = [item for item in normalized if item["role"] != "focal"]
    content_count = len(normalized)
    if focal_items:
        # 小规模地图大屏使用 3 列；常规 1080p 使用 4 列，地图才能居中 2×2。
        columns = 3 if content_count <= 5 or screen_width < 1600 else 4
        base_units = len(focal_items) * 4 + len(ordinary_items)
        rows = max(2, math.ceil(base_units / columns))
    else:
        columns = 2 if content_count <= 4 else 3 if content_count <= 6 else 4
        base_units = content_count
        rows = max(1, math.ceil(base_units / columns))

    occupied = [[False for _ in range(columns)] for _ in range(rows)]
    placements: dict[int, dict[str, Any]] = {}
    violations: list[str] = []

    for item in focal_items:
        found = _find_free_placement(occupied, col_span=2, row_span=2)
        if found is None:
            violations.append(f"焦点图表 {item['id']} 无法获得 2×2 区域")
            continue
        row, column = found
        _occupy(occupied, row, column, 2, 2)
        placements[item["id"]] = {
            "id": item["id"],
            "role": "focal",
            "column": column + 1,
            "row": row + 1,
            "col_span": 2,
            "row_span": 2,
        }

    free_units = rows * columns - sum(sum(1 for cell in row if cell) for row in occupied)
    # 每个普通图至少需要一格；多出的格子优先奖励给多系列/长数据宽图。
    expansion_budget = max(0, free_units - len(ordinary_items))
    wide_candidates = sorted(
        (item for item in ordinary_items if item["role"] == "wide"),
        key=lambda item: (
            int(item.get("series_count") or 0),
            int(item.get("source_row_count") or 0),
            -int(item["id"]),
        ),
        reverse=True,
    )
    expanded_ids = {
        item["id"] for item in wide_candidates[:expansion_budget]
    }

    # 先放宽图，确保连续格不会被 1×1 模块切碎。
    for item in ordinary_items:
        if item["id"] not in expanded_ids:
            continue
        found = _find_free_placement(occupied, col_span=2, row_span=1)
        if found is None:
            expanded_ids.discard(item["id"])
            continue
        row, column = found
        _occupy(occupied, row, column, 1, 2)
        placements[item["id"]] = {
            "id": item["id"],
            "role": "wide",
            "column": column + 1,
            "row": row + 1,
            "col_span": 2,
            "row_span": 1,
        }

    for item in ordinary_items:
        if item["id"] in placements:
            continue
        found = _find_free_placement(occupied, col_span=1, row_span=1)
        if found is None:
            violations.append(f"图表 {item['id']} 无可用网格")
            continue
        row, column = found
        _occupy(occupied, row, column, 1, 1)
        placements[item["id"]] = {
            "id": item["id"],
            "role": "standard",
            "column": column + 1,
            "row": row + 1,
            "col_span": 1,
            "row_span": 1,
        }

    content_width = max(0, screen_width - OUTER_HORIZONTAL_PADDING)
    reserved_height = (
        HEADER_WITH_KPI_RESERVED_HEIGHT if kpi_count else HEADER_ONLY_RESERVED_HEIGHT
    )
    content_height = max(0, screen_height - reserved_height)
    cell_width = max(0.0, (content_width - GRID_GAP * (columns - 1)) / columns)
    cell_height = max(0.0, (content_height - GRID_GAP * (rows - 1)) / rows)
    standard_canvas_height = max(0, round(cell_height - STANDARD_PANEL_CHROME_HEIGHT))

    map_canvas_width = 0
    map_canvas_height = 0
    if focal_items:
        map_panel_width = cell_width * 2 + GRID_GAP
        map_panel_height = cell_height * 2 + GRID_GAP
        map_canvas_width = max(0, round(map_panel_width - 28))
        map_canvas_height = max(0, round(map_panel_height - MAP_PANEL_CHROME_HEIGHT))
        if map_canvas_height < MIN_MAP_CANVAS_HEIGHT:
            violations.append(
                f"地图有效高度 {map_canvas_height}px 低于 {MIN_MAP_CANVAS_HEIGHT}px"
            )

    if standard_canvas_height < MIN_STANDARD_CANVAS_HEIGHT:
        violations.append(
            f"普通图表有效高度 {standard_canvas_height}px 低于 "
            f"{MIN_STANDARD_CANVAS_HEIGHT}px"
        )
    if rows > MAX_SINGLE_PAGE_CONTENT_ROWS:
        violations.append(
            f"内容网格需要 {rows} 行，超过单页上限 {MAX_SINGLE_PAGE_CONTENT_ROWS} 行"
        )

    return {
        "columns": columns,
        "rows": rows,
        "placements": [
            placements[item["id"]]
            for item in normalized
            if item["id"] in placements
        ],
        "feasible": not violations and len(placements) == len(normalized),
        "violations": violations,
        "estimated_map_canvas_width": map_canvas_width,
        "estimated_map_canvas_height": map_canvas_height,
        "map_col_span": 2 if focal_items else 0,
        "map_row_span": 2 if focal_items else 0,
        "standard_canvas_height": standard_canvas_height,
    }


def estimate_layout_plan(
    *,
    requirement: str = "",
    data_fields: list[dict[str, Any]] | None = None,
    suggested_charts: list[dict[str, Any]] | None = None,
    screen_width: int = 1920,
    screen_height: int = 1080,
) -> dict[str, Any]:
    """生成用户确认前的可解释布局预估。

    suggested_charts 是 Excel 图表预览确认后的高优先级事实；
    文本模式没有它时，才根据 data_fields/需求关键词估算。
    """
    fields = data_fields or []
    suggestions = suggested_charts or []

    map_types = {
        str(chart.get("type") or "").lower()
        for chart in suggestions
        if str(chart.get("type") or "").lower() in _MAP_TYPES
    }
    map_views = len(map_types)
    map_panels = 1 if map_views else 0

    explicit_kpis = sum(
        1 for chart in suggestions
        if str(chart.get("type") or "").lower() == "kpi"
    )
    ordinary_charts = sum(
        1 for chart in suggestions
        if str(chart.get("type") or "").lower() not in {
            "kpi", "world_map", "china_map", "map",
        }
    )

    layout_items: list[dict[str, Any]] = []
    if suggestions:
        kpi_count = explicit_kpis
        if kpi_count == 0:
            inferred_kpis, _ = _estimated_from_fields(fields)
            kpi_count = min(inferred_kpis, 3)
        chart_count = ordinary_charts + map_panels
        if map_panels:
            layout_items.append({"id": 1, "kind": "map", "series_type": "map"})
        for chart in suggestions:
            chart_type = str(chart.get("type") or "").lower()
            if chart_type == "kpi" or chart_type in _MAP_TYPES:
                continue
            layout_items.append({
                "id": len(layout_items) + 1,
                "kind": "table" if chart_type == "table" else "chart",
                "series_type": chart_type,
            })
    else:
        kpi_count, chart_count = _estimated_from_fields(fields)
        if not fields:
            # 自由文本无法在 PM 前精确知道最终清单，给出保守的标准大屏规模。
            explicit = _requirement_chart_count(requirement)
            chart_count = max(explicit, 3)
            kpi_count = 3
        has_requirement_map = "地图" in requirement and chart_count > 0
        if has_requirement_map:
            map_panels = 1
            map_views = 1
            layout_items.append({"id": 1, "kind": "map", "series_type": "map"})
        remaining = max(0, chart_count - map_panels)
        for index in range(remaining):
            layout_items.append({
                "id": len(layout_items) + 1,
                "kind": "chart",
                "series_type": "line" if index == 0 else "bar",
            })

    estimated_slots = max(kpi_count + chart_count, 1)
    grid_plan = plan_single_page_grid(
        layout_items,
        screen_width=screen_width,
        screen_height=screen_height,
        kpi_count=kpi_count,
    )
    single_page_feasible = (
        estimated_slots <= SINGLE_PAGE_HARD_MAX
        and screen_width >= 1280
        and screen_height >= 720
        and grid_plan["feasible"]
    )
    recommended_layout = (
        "single_page"
        if estimated_slots <= SINGLE_PAGE_COMFORTABLE_MAX and single_page_feasible
        else "tabs"
    )
    density = (
        "comfortable"
        if estimated_slots <= SINGLE_PAGE_COMFORTABLE_MAX
        else "compact"
        if estimated_slots <= 12
        else "dense"
    )
    tab_count = max(2, math.ceil(estimated_slots / TAB_TARGET_SIZE))

    if recommended_layout == "single_page":
        reason = f"预计 {estimated_slots} 个模块，单页可保持清晰阅读。"
    elif single_page_feasible:
        reason = f"预计 {estimated_slots} 个模块，分页更易读；仍可选择紧凑单页。"
    else:
        reason = (
            f"预计 {estimated_slots} 个模块，已超过当前分辨率的单页可读容量，"
            "建议分页展示。"
        )

    return {
        "estimated_slots": estimated_slots,
        "estimated_charts": chart_count,
        "kpi_cards": kpi_count,
        "map_panels": map_panels,
        "map_views": map_views,
        "recommended_layout": recommended_layout,
        "single_page_feasible": single_page_feasible,
        "single_page_density": density,
        "estimated_tabs": tab_count,
        "reason": reason,
        "grid_columns": grid_plan["columns"],
        "grid_rows": grid_plan["rows"],
        "map_col_span": grid_plan["map_col_span"],
        "map_row_span": grid_plan["map_row_span"],
        "estimated_map_canvas_width": grid_plan["estimated_map_canvas_width"],
        "estimated_map_canvas_height": grid_plan["estimated_map_canvas_height"],
        "layout_violations": grid_plan["violations"],
    }