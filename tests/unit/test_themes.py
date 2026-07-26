"""主题加载测试 — themes.py。

覆盖：
- 所有 20 个主题文件存在、可加载
- load_theme 别名
- list_themes 返回完整列表
- theme_display_name / resolve_theme_id
"""

from __future__ import annotations

import pytest

from vizagent_dashboard.compiler.themes import (
    list_themes,
    load_theme,
    theme_display_name,
    resolve_theme_id,
    build_design_context,
)


class TestLoadTheme:
    def test_known_theme_exists(self):
        content = load_theme("paper-linen")
        assert len(content) > 100
        assert "Color Palette" in content
        assert "Typography" in content

    def test_all_20_themes_loadable(self, known_themes):
        """所有 20 个主题文件必须能加载且包含必要章节。"""
        required_sections = ["Color Palette", "Typography", "Visual Theme"]
        for tid in known_themes:
            content = load_theme(tid)
            assert content, f"Theme {tid} not loaded"
            for section in required_sections:
                assert section in content, f"Theme {tid} missing section: {section}"

    def test_unknown_theme_returns_empty(self):
        assert load_theme("nonexistent-theme-xyz") == ""

    def test_alias_midnight_ops(self):
        """midnight-ops → monitor-dark。"""
        alias = load_theme("midnight-ops")
        direct = load_theme("monitor-dark")
        assert alias == direct

    def test_alias_paper_brief(self):
        alias = load_theme("paper-brief")
        direct = load_theme("minimal-doc")
        assert alias == direct


class TestListThemes:
    def test_returns_20_themes(self):
        themes = list_themes()
        assert len(themes) >= 20

    def test_each_theme_has_required_fields(self):
        for t in list_themes():
            assert "id" in t
            assert "name" in t
            assert "description" in t
            assert "colors" in t
            assert isinstance(t["colors"], list)
            assert len(t["colors"]) >= 1

    def test_ids_are_unique(self):
        themes = list_themes()
        ids = [t["id"] for t in themes]
        assert len(ids) == len(set(ids))

    def test_names_are_unique(self):
        themes = list_themes()
        names = [t["name"] for t in themes]
        assert len(names) == len(set(names))

    def test_colors_are_hex(self):
        for t in list_themes():
            for color in t["colors"]:
                assert color.startswith("#")
                assert len(color) in {7, 9}  # #RRGGBB or #RRGGBBAA


class TestThemeDisplayName:
    def test_known_id(self):
        name = theme_display_name("paper-linen")
        assert isinstance(name, str)
        assert len(name) > 0

    def test_unknown_id(self):
        assert theme_display_name("") == ""
        assert theme_display_name(None) == ""

    def test_alias_resolved(self):
        """别名 midnight-ops 返回 monitor-dark 的显示名。"""
        name = theme_display_name("midnight-ops")
        assert isinstance(name, str) and len(name) > 0


class TestResolveThemeId:
    def test_by_id(self):
        assert resolve_theme_id("paper-linen") == "paper-linen"

    def test_by_display_name(self):
        name = theme_display_name("paper-linen")
        resolved = resolve_theme_id(name)
        assert resolved == "paper-linen"

    def test_empty_input(self):
        assert resolve_theme_id("") == ""
        assert resolve_theme_id(None) == ""


class TestBuildDesignContext:
    def test_known_theme_returns_context(self):
        ctx = build_design_context("paper-linen")
        assert "设计系统规范" in ctx
        assert "Color Palette" in ctx
        assert "Typography" in ctx
        assert "Component Patterns" in ctx

    def test_none_returns_default(self):
        ctx = build_design_context(None)
        assert "设计系统规范" in ctx

    def test_unknown_returns_default(self):
        ctx = build_design_context("nonexistent")
        assert "设计系统规范" in ctx
