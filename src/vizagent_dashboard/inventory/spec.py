"""数据盘点契约。"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ColumnInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    dtype: str
    null_count: int = 0
    unique_count: int = 0
    sample_values: list[Any] = Field(default_factory=list)
    minimum: float | str | None = None
    maximum: float | str | None = None


class SheetInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    row_count: int
    columns: list[ColumnInfo] = Field(default_factory=list)


class DataInventory(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: str = "1.0"
    source_path: str = ""
    source_sha256: str = ""
    total_rows: int = 0
    sheets: list[SheetInfo] = Field(default_factory=list)
