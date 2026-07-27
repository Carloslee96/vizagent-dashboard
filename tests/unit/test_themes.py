"""主题加载测试 — themes.py。

覆盖（5 个 clean-room 通用主题）：
- 所有主题文件存在、可加载、含必要章节
- load_theme 别名（旧 ID 兼容映射到新主题）
- list_themes 返回完整列表
- theme_display_name / resolve_theme_id
- build_design_context
"""

from __future__ import annotations

import pytest

from vizagent_dashboard.compiler.themes import (
    THEME_IDS,
    build_design_context,
    list_themes,
    load_theme,
    resolve_theme_id,
    set_theme_dir,
    theme_display_name,
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
    def test_returns_25_themes(self):
        """5 原创 + 20 P1 去品牌引入 = 25 个活动主题。"""
        themes = list_themes()
        assert len(themes) == 25

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


class TestUserThemeDir:
    """P5：项目级主题目录（--theme-dir）覆盖包内主题。"""

    @pytest.fixture
    def theme_dir(self, tmp_path):
        directory = tmp_path / "mythemes"
        directory.mkdir()
        yield directory
        set_theme_dir(None)  # 清除全局状态，避免污染其他测试

    def _write_theme(self, directory, theme_id, name, palette_hex):
        (directory / f"{theme_id}.md").write_text(
            "---\n"
            f"id: {theme_id}\n"
            f"name: {name}\n"
            "aliases: []\n"
            "decoration: flat\n"
            "base: dark\n"
            "---\n\n"
            f"# {name}\n\n## Visual Theme\n\n测试主题。\n\n## Color Palette\n\n"
            "| Token | Value | Purpose |\n|---|---|---|\n"
            "| `--bg-primary` | `#101112` | 背景 |\n"
            "| `--accent-primary` | `#abcdef` | 强调 |\n\n"
            "## Chart Color Palette\n\n"
            f"`{palette_hex}` `#45C486` `#F2B84B`\n",
            encoding="utf-8",
        )

    def test_extra_theme_discovered(self, theme_dir):
        """--theme-dir 下的新主题被发现并可加载。"""
        self._write_theme(theme_dir, "my-brand", "My Brand", "#AABBCC")
        set_theme_dir(theme_dir)
        ids = [t["id"] for t in list_themes()]
        assert "my-brand" in ids
        assert load_theme("my-brand") != ""
        assert "My Brand" in load_theme("my-brand")

    def test_extra_theme_overrides_packaged(self, theme_dir):
        """同 id 主题：--theme-dir 覆盖包内。"""
        self._write_theme(theme_dir, "midnight-ops", "Override Ops", "#FF0000")
        set_theme_dir(theme_dir)
        # list_themes 取覆盖项的 name
        names = {t["id"]: t["name"] for t in list_themes()}
        assert names["midnight-ops"] == "Override Ops"
        # load_theme 取覆盖项正文
        body = load_theme("midnight-ops")
        assert "Override Ops" in body
        assert "Midnight Ops" not in body  # 包内原 name 已被覆盖

    def test_clear_theme_dir_restores_packaged(self, theme_dir):
        """清除 --theme-dir 后恢复包内主题。"""
        self._write_theme(theme_dir, "midnight-ops", "Override Ops", "#FF0000")
        set_theme_dir(theme_dir)
        assert load_theme("midnight-ops").count("Override Ops") >= 1
        set_theme_dir(None)
        assert "Midnight Ops" in load_theme("midnight-ops")


# P1 去品牌引入的 20 个主题：SaaS 源品牌名 → clean-room id。
# 这些品牌名不得出现在任何 clean-room 主题正文中（去品牌校验）。
DEBRANDED_THEMES = {
    "coral-warm": "airbnb", "obsidian-glass": "apple", "parchment-serif": "claude",
    "trust-blue": "coinbase", "canvas-dot": "figma", "ops-slate": "grafana",
    "ring-pastel": "health-ring", "nebula-glow": "kraken", "graphite-iris": "linear",
    "broadsheet": "newsroom", "fiber-paper": "notion", "grid-azure": "palantir",
    "gilt-navy": "pitchbook", "ember-paper": "posthog", "amethyst-glass": "sentry",
    "grove-dark": "spotify", "haze-lilac": "stripe", "phosphor-green": "supabase",
    "amber-scan": "terminal-amber", "mono-noir": "vercel",
}

# 品牌残留关键词（品牌名 + 品牌专有色名 + 模仿性描述词），clean-room 主题不得命中。
BRAND_RESIDUE_KEYWORDS = [
    "airbnb", "apple", "anthropic", "claude", "coinbase", "figma", "grafana",
    "kraken", "linear", "newsroom", "notion", "palantir", "pitchbook", "posthog",
    "sentry", "spotify", "stripe", "supabase", "vercel",
    "rausch", "babu", "arches", "crail", "circularsp", "cereal",
    "标志性", "独占", "签名", "官方", "brand", "logo", "trademark", "专利",
]


class TestDebrandedThemes:
    """P1：20 个 SaaS 品牌主题去品牌引入的校验。"""

    def test_all_20_present_in_registry(self):
        """20 个去品牌主题都已注册进 THEME_IDS。"""
        ids = set(THEME_IDS)
        for theme_id in DEBRANDED_THEMES:
            assert theme_id in ids, f"{theme_id} 未注册"

    def test_each_loads_and_parses(self):
        """每个去品牌主题可加载，parse_design_tokens 产出非空 css_vars 与色板。"""
        from vizagent_dashboard.compiler.skeleton import parse_design_tokens

        for theme_id in DEBRANDED_THEMES:
            body = load_theme(theme_id)
            assert body, f"{theme_id} 加载为空"
            tokens = parse_design_tokens(body)
            assert len(tokens["css_vars"]) >= 9, f"{theme_id} css_vars 不足"
            # amber-scan 源 4 色、mono-noir 源 6 色；其余 5 色
            min_palette = 4 if theme_id == "amber-scan" else 5
            assert len(tokens["chart_palette"]) >= min_palette, (
                f"{theme_id} 色板不足：{tokens['chart_palette']}"
            )

    def test_no_brand_residue(self):
        """任何 clean-room 主题正文不得残留品牌名/专有色名/签名词。"""
        for theme_id in DEBRANDED_THEMES:
            body = load_theme(theme_id).lower()
            for kw in BRAND_RESIDUE_KEYWORDS:
                assert kw not in body, f"{theme_id} 残留品牌关键词：{kw}"

    def test_no_id_alias_collision_with_original_aliases(self):
        """去品牌主题 id 不得与原创主题的别名碰撞（amber-scan 而非 amber-console）。"""
        original_aliases = {
            "monitor-dark", "dark-ops", "paper-brief", "paper-linen", "minimal-doc",
            "clean-slate", "fitness-glass", "command-post", "amber-console",
        }
        for theme_id in DEBRANDED_THEMES:
            assert theme_id not in original_aliases, (
                f"{theme_id} 与原创主题别名碰撞"
            )

    def test_resolves_by_id(self):
        for theme_id in DEBRANDED_THEMES:
            assert resolve_theme_id(theme_id) == theme_id
