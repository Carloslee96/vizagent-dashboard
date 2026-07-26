"""DashboardSpec — versioned JSON schema as single source of truth for dashboard intent."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ChartType(str, Enum):
    line = "line"
    bar = "bar"
    pie = "pie"
    scatter = "scatter"
    map_china = "map_china"
    map_world = "map_world"
    kpi = "kpi"


class ChartItem(BaseModel):
    """A single chart or KPI card in the dashboard."""
    chart_type: ChartType
    title: str = ""
    data_sheet: str = ""
    x_field: str = ""
    y_field: str = ""
    series_field: str | None = None
    aggregation: str | None = None
    width: int = 1
    height: int = 1


class LayoutRow(BaseModel):
    """A row in the dashboard layout grid."""
    columns: int = 3
    items: list[ChartItem] = Field(default_factory=list)


class DashboardSpec(BaseModel):
    """Versioned dashboard specification — the single source of truth."""
    version: str = "1.0"
    title: str = "Dashboard"
    theme: str = "midnight-ops"
    layout: list[LayoutRow] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
