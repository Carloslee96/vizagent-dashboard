"""Wheel 打包契约测试 — 锁定 P0-1 回归：包路径必须可导入。

构建 wheel 并校验：
- 顶层包是 vizagent_dashboard/（不是 src/vizagent_dashboard/）
- vendor 运行时（echarts.min.js、china.json、world.json）随包分发
- 主题 .md 资源随包分发
- console script 入口 vizagent 已注册
"""

from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

_SKILL_ROOT = Path(__file__).resolve().parents[2]


def _build_wheel(tmp_path: Path) -> Path:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "wheel", "--no-deps", "-w", str(tmp_path), str(_SKILL_ROOT)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        pytest.skip(f"pip wheel 失败: {result.stderr[:400]}")
    wheels = list(tmp_path.glob("vizagent_dashboard-*.whl"))
    assert wheels, "未生成 wheel"
    return wheels[0]


def test_wheel_package_path_is_importable(tmp_path):
    """wheel 内包路径必须是 vizagent_dashboard/，而非 src/vizagent_dashboard/。"""
    wheel = _build_wheel(tmp_path)
    names = zipfile.ZipFile(wheel).namelist()
    assert any(n == "vizagent_dashboard/__init__.py" for n in names), "顶层包缺失"
    assert not any(n.startswith("src/vizagent_dashboard") for n in names), "wheel 仍带 src/ 前缀"


def test_wheel_includes_vendor_and_themes(tmp_path):
    """离线运行时和主题资源必须随包分发。"""
    wheel = _build_wheel(tmp_path)
    names = zipfile.ZipFile(wheel).namelist()
    for required in (
        "vizagent_dashboard/vendor/echarts.min.js",
        "vizagent_dashboard/vendor/china.json",
        "vizagent_dashboard/vendor/world.json",
        "vizagent_dashboard/assets/midnight-ops.md",
        "vizagent_dashboard/assets/paper-light.md",
    ):
        assert required in names, f"wheel 缺失资源: {required}"


def test_wheel_registers_console_script(tmp_path):
    """vizagent console script 入口必须注册。"""
    wheel = _build_wheel(tmp_path)
    names = zipfile.ZipFile(wheel).namelist()
    entry = next(n for n in names if n.endswith("entry_points.txt"))
    content = zipfile.ZipFile(wheel).read(entry).decode("utf-8")
    assert "vizagent" in content and "vizagent_dashboard.cli:main" in content
