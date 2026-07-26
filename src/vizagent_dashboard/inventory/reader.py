"""CSV / XLSX file reader."""

from pathlib import Path
from typing import Any


def read_file(path: str | Path) -> dict[str, list[dict[str, Any]]]:
    """Read CSV or Excel file, return {sheet_name: [row_dict, ...]}."""
    raise NotImplementedError("Will be extracted from SaaS in Step 2")
