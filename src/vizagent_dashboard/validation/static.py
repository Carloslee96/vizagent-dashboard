"""HTML、图表数据和覆盖清单的确定性发布门禁。"""

from __future__ import annotations

import json
import re
from typing import Any

from vizagent_dashboard.inventory.spec import DataInventory
from vizagent_dashboard.schemas.dashboard_spec import ChartType, DashboardSpec


def _to_float(value: Any) -> float | None:
    try:
        cleaned = str(value).replace(",", "").replace("¥", "").replace("$", "").replace("%", "").strip()
        return float(cleaned) if cleaned else None
    except (TypeError, ValueError):
        return None


def _is_numeric(value: Any) -> bool:
    return _to_float(value) is not None


def check_html_truncation(html_content: str) -> dict[str, Any]:
    tail = html_content[-500:].lower()
    issues = []
    if "</body>" not in tail:
        issues.append("HTML 末尾缺少 </body>")
    if "</html>" not in tail:
        issues.append("HTML 末尾缺少 </html>")
    return {
        "is_truncated": bool(issues),
        "score": max(0, 100 - len(issues) * 50),
        "issues": issues,
        "html_length": len(html_content),
        "has_closing_html": "</html>" in tail,
        "has_closing_body": "</body>" in tail,
    }


def extract_chart_entries(html_content: str) -> list[dict[str, Any]]:
    payload = _extract_json_script(html_content, "vizagent-chart-options")
    return payload if isinstance(payload, list) else []


def extract_build_manifest(html_content: str) -> dict[str, Any]:
    payload = _extract_json_script(html_content, "vizagent-build-manifest")
    return payload if isinstance(payload, dict) else {}


def count_charts_in_html(html_content: str) -> dict[str, int]:
    counts = {"line": 0, "bar": 0, "pie": 0, "scatter": 0, "map": 0, "kpi": 0, "table": 0, "total": 0}
    entries = extract_chart_entries(html_content)
    if entries:
        counts["total"] = len(entries)
        for entry in entries:
            chart_type = str(entry.get("type", ""))
            key = "map" if chart_type in {"map_china", "map_world", "map"} else chart_type
            if key in counts:
                counts[key] += 1
        counts["kpi"] = len(re.findall(r'data-viz-type="kpi"', html_content))
        counts["table"] = len(re.findall(r'data-viz-type="table"', html_content))
        return counts

    counts["total"] = len(re.findall(r"echarts\.init\s*\(", html_content))
    for chart_type in ("line", "bar", "pie", "scatter", "map"):
        counts[chart_type] = len(re.findall(rf'"type"\s*:\s*"{chart_type}"', html_content))
    counts["kpi"] = len(re.findall(r'class="kpi-card"', html_content))
    return counts


def check_chart_entries(entries: list[dict[str, Any]]) -> list[str]:
    issues: list[str] = []
    seen_ids: set[str] = set()
    for index, entry in enumerate(entries, start=1):
        dom_id = str(entry.get("dom_id", ""))
        chart_type = str(entry.get("type", ""))
        option = entry.get("option")
        if not dom_id:
            issues.append(f"图表 {index} 缺少 dom_id")
        elif dom_id in seen_ids:
            issues.append(f"图表 DOM ID 重复: {dom_id}")
        seen_ids.add(dom_id)
        if not isinstance(option, dict):
            issues.append(f"图表 {index} option 不是对象")
            continue
        series = option.get("series")
        if not isinstance(series, list) or not series:
            issues.append(f"图表 {index}（{chart_type}）缺少 series")
            continue
        data_series = [item for item in series if isinstance(item, dict) and isinstance(item.get("data"), list)]
        if not data_series or not any(item["data"] for item in data_series):
            issues.append(f"图表 {index}（{chart_type}）没有有效数据")
        if chart_type == "map_china":  # noqa: SIM102
            if not any(item.get("type") == "map" and item.get("map") == "china" for item in series if isinstance(item, dict)):
                issues.append(f"图表 {index} 未绑定中国地图")
        if chart_type == "map_world":
            uses_world = option.get("geo", {}).get("map") == "world" or any(
                item.get("map") == "world" for item in series if isinstance(item, dict)
            )
            if not uses_world:
                issues.append(f"图表 {index} 未绑定世界地图")
    return issues


def check_overlaps(chart_options: list[Any]) -> list[str]:
    """兼容保留：真实几何重叠由浏览器验证。"""

    issues = []
    for option in chart_options:
        if isinstance(option, str):
            issues.append(option)
        elif isinstance(option, dict) and option.get("overlap"):
            issues.append(str(option["overlap"]))
    return issues[:3]


def check_zero_size(chart_options: list[Any]) -> list[str]:
    issues = []
    for index, option in enumerate(chart_options):
        if not isinstance(option, dict):
            continue
        series = option.get("series")
        if not isinstance(series, list) or not series:
            issues.append(f"图表 {index + 1} 缺少 series 数据")
    return issues


def check_duplicate_maps(html_content: str) -> list[str]:
    """同一地图最多注册一次；中国和世界各一次是合法组合。"""

    issues = []
    for map_id in ("china", "world"):
        count = len(re.findall(rf"registerMap\(\s*['\"]{map_id}['\"]", html_content))
        if count > 1:
            issues.append(f"{map_id} 地图重复注册 {count} 次")
    return issues


def check_empty_options(html_content: str) -> list[str]:
    return check_chart_entries(extract_chart_entries(html_content))


def validate_html(
    html_content: str,
    spec: DashboardSpec | None = None,
    inventory: DataInventory | None = None,
    manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    truncation = check_html_truncation(html_content)
    errors.extend(truncation["issues"])

    entries = extract_chart_entries(html_content)
    embedded_manifest = extract_build_manifest(html_content)
    active_manifest = manifest or embedded_manifest
    if not entries and (spec is None or any(item.chart_type != ChartType.kpi for row in spec.layout for item in row.items)):
        errors.append("HTML 缺少机器可读图表 option 清单")
    errors.extend(check_chart_entries(entries))

    if re.search(r'<script[^>]+src=["\']https?://', html_content, re.IGNORECASE):
        errors.append("HTML 仍依赖外部脚本，无法离线运行")

    if spec is not None:
        expected = [
            item for row in spec.layout for item in row.items
            if item.chart_type not in {ChartType.kpi, ChartType.table}
        ]
        if len(entries) != len(expected):
            errors.append(f"图表数量不匹配：Spec={len(expected)}，HTML={len(entries)}")
        expected_maps = {
            "china" if item.chart_type == ChartType.map_china else "world"
            for item in expected
            if item.chart_type in {ChartType.map_china, ChartType.map_world}
        }
        manifest_maps = set(active_manifest.get("maps", []))
        missing_maps = expected_maps - manifest_maps
        if missing_maps:
            errors.append(f"地图资源缺失：{', '.join(sorted(missing_maps))}")

    coverage = active_manifest.get("coverage", {})
    if inventory is not None:
        expected_sheets = {sheet.name: sheet.row_count for sheet in inventory.sheets if sheet.row_count > 0}
        for sheet_name, total_rows in expected_sheets.items():
            item = coverage.get(sheet_name)
            if not item:
                errors.append(f"Sheet“{sheet_name}”未进入覆盖清单")
                continue
            covered_rows = int(item.get("covered_rows", 0))
            if covered_rows != total_rows:
                errors.append(f"Sheet“{sheet_name}”覆盖不完整：{covered_rows}/{total_rows} 行")
    elif coverage and not active_manifest.get("coverage_complete", False):
        errors.append("数据覆盖不完整")
    elif not coverage:
        warnings.append("未提供 DataInventory，无法执行数据覆盖门禁")

    score = max(0, 100 - len(errors) * 15 - len(warnings) * 2)
    return {
        "is_valid": not errors,
        "score": score,
        "errors": errors,
        "warnings": warnings,
        "issues": errors + warnings,
        "chart_counts": count_charts_in_html(html_content),
        "html_length": len(html_content),
        "coverage": coverage,
        "offline": not bool(re.search(r'<script[^>]+src=["\']https?://', html_content, re.IGNORECASE)),
    }


def _extract_json_script(html_content: str, element_id: str) -> Any:
    match = re.search(
        rf'<script[^>]+id=["\']{re.escape(element_id)}["\'][^>]*>(.*?)</script>',
        html_content,
        re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return None
    try:
        return json.loads(match.group(1).replace("<\\/", "</"))
    except json.JSONDecodeError:
        return None
