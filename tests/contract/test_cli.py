"""CLI 契约测试 — 验证 vizagent 子命令的端到端行为。

覆盖 inventory / plan / compile / build / validate 五个子命令的产物契约，
确保 CLI 入口、Inventory、Planner、Compiler、Validator 全链路接线正确。
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from vizagent_dashboard.cli import cli

_DATA = Path(__file__).resolve().parents[2] / "examples" / "ecommerce" / "data.csv"
_SPEC = Path(__file__).resolve().parents[2] / "examples" / "ecommerce" / "spec.json"


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def test_inventory_command(runner, tmp_path):
    output = tmp_path / "data.inventory.json"
    result = runner.invoke(cli, ["inventory", "--data", str(_DATA), "--output", str(output)])
    assert result.exit_code == 0, result.output
    assert output.exists()
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["total_rows"] == 72
    assert len(payload["sheets"]) == 1
    assert payload["sheets"][0]["name"] == "Sheet1" or payload["sheets"][0]["row_count"] == 72


def test_plan_command(runner, tmp_path):
    output = tmp_path / "dashboard.spec.json"
    result = runner.invoke(
        cli,
        ["plan", "--data", str(_DATA), "--requirement", "月度销售额趋势折线图", "--output", str(output)],
    )
    assert result.exit_code == 0, result.output
    assert output.exists()
    spec = json.loads(output.read_text(encoding="utf-8"))
    assert spec["theme"] in {"midnight-ops", "paper-light", "warm-editorial", "clinical-light", "signal-dark"}
    assert len(spec["layout"]) >= 1
    assert spec["metadata"]["planner"] == "deterministic-inventory-v1"


def test_plan_requirement_changes_spec(runner, tmp_path):
    """两条不同需求应产生不同的 Spec（P0-3 回归门禁）。"""
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    runner.invoke(cli, ["plan", "--data", str(_DATA), "--requirement", "只展示饼图，使用浅色主题", "--output", str(a)])
    runner.invoke(cli, ["plan", "--data", str(_DATA), "--requirement", "只展示折线图，使用深色主题", "--output", str(b)])
    spec_a = json.loads(a.read_text(encoding="utf-8"))
    spec_b = json.loads(b.read_text(encoding="utf-8"))
    assert spec_a["theme"] != spec_b["theme"]  # 浅色 vs 深色
    types_a = {item["chart_type"] for row in spec_a["layout"] for item in row["items"]}
    types_b = {item["chart_type"] for row in spec_b["layout"] for item in row["items"]}
    assert types_a != types_b


def test_compile_command(runner, tmp_path):
    output_dir = tmp_path / "build"
    result = runner.invoke(
        cli,
        ["compile", "--data", str(_DATA), "--spec", str(_SPEC), "--output", str(output_dir)],
    )
    assert result.exit_code == 0, result.output
    html = (output_dir / "output.html").read_text(encoding="utf-8")
    assert "<!doctype html>" in html
    manifest = json.loads((output_dir / "build-manifest.json").read_text(encoding="utf-8"))
    assert manifest["chart_count"] == 4
    assert manifest["coverage_complete"] is True


def test_build_command_full_pipeline(runner, tmp_path):
    output_dir = tmp_path / "build"
    result = runner.invoke(
        cli,
        ["build", "--data", str(_DATA), "--output", str(output_dir)],
    )
    assert result.exit_code == 0, result.output
    for name in ("output.html", "dashboard.spec.json", "data.inventory.json", "validation.report.json", "build-manifest.json"):
        assert (output_dir / name).exists(), f"missing artifact: {name}"
    report = json.loads((output_dir / "validation.report.json").read_text(encoding="utf-8"))
    assert report["is_valid"] is True


def test_build_spec_theme_not_overridden(runner, tmp_path):
    """不传 --theme 时，Spec 内声明的主题应被尊重（P1-1 回归门禁）。"""
    output_dir = tmp_path / "build"
    result = runner.invoke(
        cli,
        ["build", "--data", str(_DATA), "--spec", str(_SPEC), "--theme", "paper-light", "--output", str(output_dir)],
    )
    assert result.exit_code == 0, result.output
    manifest = json.loads((output_dir / "build-manifest.json").read_text(encoding="utf-8"))
    assert manifest["theme"] == "paper-light"


def test_validate_command(runner, tmp_path):
    output_dir = tmp_path / "build"
    runner.invoke(cli, ["compile", "--data", str(_DATA), "--spec", str(_SPEC), "--output", str(output_dir)])
    report_path = tmp_path / "report.json"
    result = runner.invoke(
        cli,
        [
            "validate",
            "--data", str(_DATA),
            "--spec", str(_SPEC),
            "--html", str(output_dir / "output.html"),
            "--output", str(report_path),
        ],
    )
    assert result.exit_code == 0, result.output
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["is_valid"] is True
    assert report["offline"] is True


def test_build_offline_embedded(runner, tmp_path):
    """默认 embedded 模式产物无外部脚本依赖。"""
    output_dir = tmp_path / "build"
    runner.invoke(cli, ["build", "--data", str(_DATA), "--output", str(output_dir)])
    html = (output_dir / "output.html").read_text(encoding="utf-8")
    import re

    assert re.search(r'<script[^>]+src=["\']https?://', html) is None
    assert "jsdelivr.net" not in html
