"""pytest 共享 fixtures（测试数据、主题、spec）。

参考源：viz-agent-team/backend/data/test_reports/ 中的 PRD 样例。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from vizagent_dashboard.schemas.dashboard_spec import (
    ChartItem,
    ChartType,
    DashboardSpec,
    LayoutRow,
)

_HERE = Path(__file__).parent
_DATA_DIR = _HERE.parent / "examples" / "ecommerce"


# ═══════════════════════════════════════════════════════════════════
# 电商销售数据（72 行，6 列）
# ═══════════════════════════════════════════════════════════════════


@pytest.fixture(scope="session")
def ecommerce_csv_path() -> str:
    return str(_DATA_DIR / "data.csv")


@pytest.fixture(scope="session")
def ecommerce_data() -> list[dict[str, Any]]:
    """读取真实电商数据（72 行）。"""
    from vizagent_dashboard.inventory.reader import read_file

    sheets = read_file(str(_DATA_DIR / "data.csv"))
    return next(iter(sheets.values()))


@pytest.fixture(scope="session")
def ecommerce_spec() -> DashboardSpec:
    """从 spec.json 加载 DashboardSpec。"""
    spec_path = _DATA_DIR / "spec.json"
    with open(spec_path, encoding="utf-8") as f:
        return DashboardSpec(**json.load(f))


# ═══════════════════════════════════════════════════════════════════
# 迷你测试数据（避免依赖外部文件）
# ═══════════════════════════════════════════════════════════════════


@pytest.fixture
def mini_data() -> list[dict[str, Any]]:
    """3 行迷你数据用于快速测试。"""
    return [
        {"月份": "2025-01", "销售额": "1000", "类别": "数码", "地区": "华东", "利润": "200", "数量": "50"},
        {"月份": "2025-02", "销售额": "2000", "类别": "服装", "地区": "华南", "利润": "300", "数量": "80"},
        {"月份": "2025-03", "销售额": "1500", "类别": "数码", "地区": "华东", "利润": "250", "数量": "60"},
    ]


@pytest.fixture
def mini_spec() -> DashboardSpec:
    """3 个 KPI + line + pie + bar 的迷你 spec。"""
    return DashboardSpec(
        title="测试大屏",
        theme="midnight-ops",
        layout=[
            LayoutRow(
                columns=3,
                items=[
                    ChartItem(chart_type=ChartType.kpi, title="总销售额", data_field="销售额", aggregation="sum", width=1, height=1),
                    ChartItem(chart_type=ChartType.kpi, title="总利润", data_field="利润", aggregation="sum", width=1, height=1),
                    ChartItem(chart_type=ChartType.kpi, title="总销量", data_field="数量", aggregation="sum", width=1, height=1),
                ],
            ),
            LayoutRow(
                columns=2,
                items=[
                    ChartItem(chart_type=ChartType.line, title="月销售额趋势", x_field="月份", y_field="销售额", width=1, height=1),
                    ChartItem(chart_type=ChartType.pie, title="品类占比", x_field="类别", y_field="销售额", width=1, height=1),
                ],
            ),
        ],
    )


# ═══════════════════════════════════════════════════════════════════
# 主题相关
# ═══════════════════════════════════════════════════════════════════


@pytest.fixture
def midnight_ops_theme_content() -> str:
    """加载 midnight-ops（monitor-dark）主题内容。"""
    from vizagent_dashboard.compiler.themes import load_theme
    return load_theme("midnight-ops")


@pytest.fixture
def known_themes() -> list[str]:
    """已知存在的 clean-room 主题 ID 列表（5 个通用主题）。"""
    return ["midnight-ops", "paper-light", "warm-editorial", "clinical-light", "signal-dark"]


@pytest.fixture
def chart_palette() -> list[str]:
    return ["#2D5BFF", "#5B8AFF", "#8AAEFF", "#B4CCFF", "#3DAB63"]


@pytest.fixture
def css_vars() -> dict[str, str]:
    return {
        "--bg-primary": "#0A0B0D",
        "--bg-card": "#13151A",
        "--text-primary": "#E6E8EC",
        "--text-secondary": "#8A8F98",
        "--border-subtle": "#23272F",
        "--accent-primary": "#2D5BFF",
    }
