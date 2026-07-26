"""Data inventory schema definitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ColumnInfo:
    """Metadata about a single column in a dataset."""
    name: str
    dtype: str  # "numeric", "text", "date", "categorical"
    null_count: int = 0
    unique_values: list[Any] | None = None
    min: float | None = None
    max: float | None = None


@dataclass
class SheetInfo:
    """Metadata about a single sheet/table."""
    name: str
    row_count: int
    columns: list[ColumnInfo] = field(default_factory=list)


@dataclass
class DataInventory:
    """Complete inventory of all data sources."""
    sheets: list[SheetInfo] = field(default_factory=list)
    source_path: str = ""
