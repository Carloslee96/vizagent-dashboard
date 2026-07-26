"""CSV / XLSX 数据读取。

支持：
- CSV (.csv)
- Excel (.xlsx, .xls) — 单/多 Sheet

输出：每行一个 dict，key 为列名。
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


def read_file(path: str | Path) -> dict[str, list[dict[str, Any]]]:
    """读取 CSV 或 Excel 文件，返回 {sheet_name: [row_dict, ...]}。

    Args:
        path: 文件路径

    Returns:
        {"Sheet1": [{"col1": v1, "col2": v2, ...}, ...], ...}
        CSV 文件的 sheet 名为 "Sheet1"。
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {path}")

    suffix = path.suffix.lower()

    if suffix == ".csv":
        return {"Sheet1": _read_csv(path)}

    if suffix in {".xlsx", ".xls"}:
        return _read_excel(path)

    raise ValueError(f"不支持的文件格式: {suffix}（仅支持 .csv / .xlsx / .xls）")


def _read_csv(path: Path) -> list[dict[str, Any]]:
    """读取 CSV 文件。"""
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows: list[dict[str, Any]] = []
        for row in reader:
            # 去掉 None key（CSV 末尾空列）
            cleaned = {k: v for k, v in row.items() if k is not None}
            rows.append(cleaned)
        return rows


def _read_excel(path: Path) -> dict[str, list[dict[str, Any]]]:
    """读取 Excel 文件（多 Sheet）。"""
    try:
        from openpyxl import load_workbook
    except ImportError:
        raise ImportError("读取 Excel 需要安装 openpyxl: pip install openpyxl")

    wb = load_workbook(path, read_only=True, data_only=True)
    sheets: dict[str, list[dict[str, Any]]] = {}

    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        rows_iter = ws.iter_rows(values_only=True)

        try:
            header_row = next(rows_iter)
        except StopIteration:
            sheets[sheet_name] = []
            continue

        # 表头处理：去掉 None
        headers = [str(h) if h is not None else "" for h in header_row]

        rows: list[dict[str, Any]] = []
        for row in rows_iter:
            row_dict: dict[str, Any] = {}
            for header, val in zip(headers, row):
                if header:  # 跳过空列名
                    row_dict[header] = val
            # 跳过完全空行
            if any(v is not None and v != "" for v in row_dict.values()):
                rows.append(row_dict)

        sheets[sheet_name] = rows

    wb.close()
    return sheets