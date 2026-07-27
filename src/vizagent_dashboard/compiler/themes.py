"""通用主题加载器（自动发现）。

活动主题全部为开源边界内重新编写的通用 token，存为 ``assets/*.md``。
每个主题文件以 frontmatter 自描述 ``id`` / ``name`` / ``aliases`` / ``decoration``
/ ``base``，加载器扫描目录自动发现——加主题只需丢一个 .md 文件，无需改本模块。
旧 ID 仅作为 frontmatter 中声明的兼容别名，不会复制旧主题内容。
"""

from __future__ import annotations

import re
from importlib.resources import files
from typing import Any

_cache: dict[str, str] = {}


def _iter_theme_files():
    """枚举包内 assets/ 下的主题 .md 文件（Traversable）。"""
    for entry in files("vizagent_dashboard.assets").iterdir():
        if entry.name.endswith(".md"):
            yield entry


def _split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """解析主题文件首部的 YAML frontmatter，返回 (meta, body)。

    不引入 PyYAML 依赖，仅支持本主题格式用到的简单标量与内联列表。
    """
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        return {}, text
    meta: dict[str, Any] = {}
    for line in lines[1:end]:
        if not line.strip() or ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            meta[key] = [item.strip().strip("'\"") for item in inner.split(",") if item.strip()]
        else:
            meta[key] = value.strip("'\"")
    body = "\n".join(lines[end + 1:]).lstrip("\n")
    return meta, body


def list_themes() -> list[dict[str, object]]:
    """扫描 assets/*.md，返回所有主题的元信息（按 id 排序）。"""
    themes: list[dict[str, object]] = []
    for entry in _iter_theme_files():
        content = entry.read_text(encoding="utf-8")
        meta, body = _split_frontmatter(content)
        theme_id = str(meta.get("id") or entry.name[:-3])
        name = str(meta.get("name") or theme_id)
        aliases = list(meta.get("aliases") or [])
        lines = body.splitlines()
        description = next(
            (
                line.strip()
                for index, line in enumerate(lines)
                if index > 2 and line.strip() and not line.startswith("#") and not line.startswith("|")
            ),
            name,
        )
        colors: list[str] = []
        chart_section = body.partition("## Chart Color Palette")[2]
        for color in re.findall(r"#[0-9a-fA-F]{6}", chart_section):
            if color not in colors:
                colors.append(color)
        themes.append(
            {
                "id": theme_id,
                "name": name,
                "aliases": aliases,
                "description": description,
                "colors": colors[:5],
            }
        )
    themes.sort(key=lambda item: str(item["id"]))
    return themes


def resolve_theme_id(id_or_name: str | None) -> str:
    """把 id / 别名 / 显示名 解析为规范主题 id；未命中返回空串。"""
    key = (id_or_name or "").strip()
    if not key:
        return ""
    for theme in list_themes():
        if theme["id"] == key:
            return str(theme["id"])
        if key in (theme.get("aliases") or []):
            return str(theme["id"])
        if theme["name"] == key:
            return str(theme["id"])
    return ""


def load_theme(theme_id: str) -> str:
    """加载主题正文（去掉 frontmatter）；未命中返回空串。"""
    resolved = resolve_theme_id(theme_id)
    if not resolved:
        return ""
    if resolved not in _cache:
        for entry in _iter_theme_files():
            if entry.name == f"{resolved}.md":
                content = entry.read_text(encoding="utf-8")
                _, body = _split_frontmatter(content)
                _cache[resolved] = body
                break
    return _cache.get(resolved, "")


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


# 派生自主题文件扫描的已知 id 清单（向后兼容公开常量；单一事实来源是各 .md 的 frontmatter）。
THEME_IDS: tuple[str, ...] = tuple(str(theme["id"]) for theme in list_themes())
