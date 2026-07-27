"""大屏意图契约。

`DashboardSpec` 是需求规划、编译和验证之间唯一的机器可读事实来源。
模型保持对 v0.1 示例的向后兼容，但禁止静默接收未知字段。
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ChartType(str, Enum):
    line = "line"
    area = "area"
    bar = "bar"
    pie = "pie"
    nightingale = "nightingale"
    treemap = "treemap"
    funnel = "funnel"
    gauge = "gauge"
    radar = "radar"
    scatter = "scatter"
    map_china = "map_china"
    map_world = "map_world"
    kpi = "kpi"
    table = "table"


class PageMode(str, Enum):
    single_page = "single_page"
    tabs = "tabs"


class ChartItem(BaseModel):
    """一个图表、地图或 KPI 卡片。"""

    model_config = ConfigDict(extra="forbid")

    chart_type: ChartType
    title: str = ""
    data_sheet: str = ""
    x_field: str = ""
    y_field: str | list[str] = ""
    data_field: str = ""
    series_field: str | None = None
    longitude_field: str = ""
    latitude_field: str = ""
    aggregation: str | None = None
    filters: dict[str, Any] = Field(default_factory=dict)
    width: int = Field(default=1, ge=1, le=4)
    height: int = Field(default=1, ge=1, le=3)

    @field_validator("title", "data_sheet", "x_field", "data_field", "longitude_field", "latitude_field")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()


class LayoutRow(BaseModel):
    """大屏的一组视觉模块。"""

    model_config = ConfigDict(extra="forbid")

    title: str = ""
    columns: int = Field(default=4, ge=1, le=4)
    items: list[ChartItem] = Field(default_factory=list)


class DashboardSpec(BaseModel):
    """版本化大屏规格。"""

    model_config = ConfigDict(extra="forbid")

    version: str = "1.0"
    title: str = "数据大屏"
    theme: str = "midnight-ops"
    page_mode: PageMode = PageMode.single_page
    layout: list[LayoutRow] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
