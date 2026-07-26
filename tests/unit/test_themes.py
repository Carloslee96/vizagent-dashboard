"""主题加载测试 — themes.py。

覆盖（5 个 clean-room 通用主题）：
- 所有主题文件存在、可加载、含必要章节
- load_theme 别名（旧 ID 兼容映射到新主题）
- list_themes 返回完整列表
- theme_display_name / resolve_theme_id
- build_design_context
"""

from __future__ import annotations

from vizagent_dashboard.compiler.themes import (
    THEME_IDS,
    list_themes,
    load_theme,
    theme_display_name,
    resolve_theme_id,
    build_design_context,
)


class TestLoadTheme:
    def test_known_theme_exists(self):
        content = load_theme("midnight-ops")
        assert len(content) > 100
        assert "Color Palette" in content
        assert "Chart Color Palette" in content
        assert "Visual Theme" in content

    def test_all_themes_loadable(self, known_themes):
        """所有主题文件必须能加载且包含必要章节。"""
        required_sections = ["Color Palette", "Chart Color Palette", "Visual Theme"]
        for tid in known_themes:
            content = load_theme(tid)
            assert content, f"Theme {tid} not loaded"
            for section in required_sections:
                assert section in content, f"Theme {tid} missing section: {section}"

    def test_theme_ids_constant_matches_fixtures(self, known_themes):
        assert set(THEME_IDS) == set(known_themes)

    def test_unknown_theme_returns_empty(self):
        assert load_theme("nonexistent-theme-xyz") == ""

    def test_alias_monitor_dark_to_midnight_ops(self):
        """旧 ID monitor-dark → midnight-ops。"""
        assert load_theme("monitor-dark") == load_theme("midnight-ops")

    def test_alias_paper_brief_to_paper_light(self):
        assert load_theme("paper-brief") == load_theme("paper-light")

    def test_alias_paper_linen_to_paper_light(self):
        assert load_theme("paper-linen") == load_theme("paper-light")

    def test_alias_command_post_to_signal_dark(self):
        assert load_theme("command-post") == load_theme("signal-dark")


class TestListThemes:
    def test_returns_five_themes(self):
        themes = list_themes()
        assert len(themes) == 5

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
        name = theme_display_name("midnight-ops")
        assert isinstance(name, str)
        assert len(name) > 0

    def test_unknown_id(self):
        assert theme_display_name("") == ""
        assert theme_display_name(None) == ""

    def test_alias_resolved(self):
        """别名 monitor-dark 返回 midnight-ops 的显示名。"""
        assert theme_display_name("monitor-dark") == theme_display_name("midnight-ops")


class TestResolveThemeId:
    def test_by_id(self):
        assert resolve_theme_id("midnight-ops") == "midnight-ops"

    def test_by_display_name(self):
        name = theme_display_name("midnight-ops")
        resolved = resolve_theme_id(name)
        assert resolved == "midnight-ops"

    def test_alias_resolved(self):
        assert resolve_theme_id("monitor-dark") == "midnight-ops"
        assert resolve_theme_id("paper-linen") == "paper-light"

    def test_empty_input(self):
        assert resolve_theme_id("") == ""
        assert resolve_theme_id(None) == ""


class TestBuildDesignContext:
    def test_known_theme_returns_context(self):
        ctx = build_design_context("midnight-ops")
        assert "按以下通用设计 token" in ctx
        assert "不要复制第三方品牌" in ctx
        assert "Color Palette" in ctx

    def test_none_returns_default(self):
        ctx = build_design_context(None)
        assert "按以下通用设计 token" in ctx

    def test_unknown_returns_default(self):
        ctx = build_design_context("nonexistent")
        assert "按以下通用设计 token" in ctx
