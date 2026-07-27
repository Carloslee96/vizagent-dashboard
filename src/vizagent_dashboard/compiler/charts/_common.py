"""图表 builder 共享助手。

从 ``compiler/chart_options.py`` 原样搬迁，供各 builder 复用。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ChartContext:
    """dispatcher 传给 builder 的上下文：共享预处理结果 + 原始入参。"""

    chart_type: str
    title: str
    data: list[dict]
    x_field: str
    y_fields: list[str]
    palette: list[str]
    colors: dict[str, str]
    base: dict[str, Any]
    categories: list[str]
    series_field: str = ""


def _clean_number(value: Any) -> int | float | None:
    """清洗数值：去除千分位、货币符号、百分号。"""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return value
    try:
        cleaned = str(value).replace(",", "").replace("¥", "").replace("$", "").replace("￥", "").replace("%", "").strip()
        if not cleaned:
            return None
        if "." in cleaned:
            return float(cleaned)
        return int(cleaned)
    except (ValueError, TypeError):
        return None


def _chart_colors_from_vars(css_vars: dict[str, str] | None) -> dict[str, str]:
    """从 CSS 变量字典中提取图表相关颜色（带 fallback）。"""
    if not css_vars:
        css_vars = {}

    def get(name: str, fallback: str) -> str:
        return css_vars.get(name) or fallback

    return {
        "tooltip_bg": get("--bg-card", "#13151A"),
        "tooltip_text": get("--text-primary", "#E6E8EC"),
        "grid_color": get("--border-subtle", "#23272F"),
        "ax_color": get("--text-secondary", "#8A8F98"),
        "series_color": get("--accent-primary", "#2D5BFF"),
    }
