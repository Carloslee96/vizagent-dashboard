"""通用主题加载器。

活动主题全部为开源边界内重新编写的通用 token。旧 ID 仅作为输入兼容别名，
不会复制旧主题内容。
"""

from __future__ import annotations

import re
from importlib.resources import files

THEME_IDS = (
    "midnight-ops",
    "paper-light",
    "warm-editorial",
    "clinical-light",
    "signal-dark",
)

ALIASES = {
    "monitor-dark": "midnight-ops",
    "dark-ops": "midnight-ops",
    "paper-brief": "paper-light",
    "paper-linen": "paper-light",
    "minimal-doc": "paper-light",
    "clean-slate": "clinical-light",
    "fitness-glass": "clinical-light",
    "command-post": "signal-dark",
    "amber-console": "signal-dark",
}

_cache: dict[str, str] = {}


def resolve_theme_id(id_or_name: str | None) -> str:
    key = (id_or_name or "").strip()
    if not key:
        return ""
    normalized = ALIASES.get(key, key)
    if normalized in THEME_IDS:
        return normalized
    for theme in list_themes():
        if theme["name"] == key:
            return theme["id"]
    return ""


def load_theme(theme_id: str) -> str:
    resolved = resolve_theme_id(theme_id)
    if not resolved:
        return ""
    if resolved not in _cache:
        _cache[resolved] = files("vizagent_dashboard.assets").joinpath(f"{resolved}.md").read_text(encoding="utf-8")
    return _cache[resolved]


def list_themes() -> list[dict[str, object]]:
    themes: list[dict[str, object]] = []
    for theme_id in THEME_IDS:
        content = files("vizagent_dashboard.assets").joinpath(f"{theme_id}.md").read_text(encoding="utf-8")
        lines = content.splitlines()
        name = lines[0].lstrip("# ").strip()
        description = next(
            (
                line.strip()
                for index, line in enumerate(lines)
                if index > 2 and line.strip() and not line.startswith("#") and not line.startswith("|")
            ),
            name,
        )
        colors = []
        chart_section = content.partition("## Chart Color Palette")[2]
        for color in re.findall(r"#[0-9a-fA-F]{6}", chart_section):
            if color not in colors:
                colors.append(color)
        themes.append({"id": theme_id, "name": name, "description": description, "colors": colors[:5]})
    return themes


def theme_display_name(theme_id: str | None) -> str:
    resolved = resolve_theme_id(theme_id)
    for theme in list_themes():
        if theme["id"] == resolved:
            return str(theme["name"])
    return ""


def build_design_context(theme_id: str | None) -> str:
    resolved = resolve_theme_id(theme_id) or "midnight-ops"
    return (
        "按以下通用设计 token 生成 DashboardSpec；不要复制第三方品牌名称、Logo 或专有资产。\n\n"
        + load_theme(resolved)
    )
