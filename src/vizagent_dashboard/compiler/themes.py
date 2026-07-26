"""设计系统加载器（从 SaaS design_loader.py 提取，去品牌改造）。

从 assets/ 目录加载主题 .md 文件，提供：
- 主题列表（list_themes）
- 主题加载（load_theme）
- 设计系统 Prompt 上下文（build_design_context）
- ID 解析（resolve_theme_id, theme_display_name）

文件名 = 主题 ID（去品牌命名）：
  paper-linen, minimal-doc, command-post, fitness-glass,
  warm-editorial, monitor-dark, cozy-retreat, clean-slate,
  design-toolkit, vibe-night, crypto-sleek, checkout-light,
  minimal-tracker, ocean-night, error-monitor, growth-analytics,
  deal-room, open-table, amber-console, deploy-light

参考源:viz-agent-team/backend/agents/design_loader.py（提取 commit 见 upstream-manifest.toml）
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Optional

# 设计系统文件目录（位于 ../assets/，相对此文件）
_THIS_DIR = Path(__file__).parent
_ASSETS_DIR = _THIS_DIR.parent / "assets"

# 缓存已加载的设计系统
_cache: dict[str, str] = {}


def _extract_theme_colors(content: str) -> list[str]:
    """从 .md 提取 3-5 个代表色用于前端色块预览。

    优先提取 Chart Color Palette 的系列色（颜色鲜明、有区分度），
    兜底从 Color Palette 表格提取 accent-primary 等强调色。
    """
    colors: list[str] = []
    lines = content.split("\n")

    # 优先:从 Chart Color Palette 提取系列色
    in_chart = False
    for line in lines:
        if line.startswith("## Chart Color Palette"):
            in_chart = True
            continue
        if in_chart:
            if line.startswith("## "):
                break
            m = re.findall(r"#[0-9a-fA-F]{6}", line)
            if m:
                for c in m:
                    if c not in colors:
                        colors.append(c)

    # 如果 Chart 颜色够 3 个就直接返回
    if len(colors) >= 3:
        return colors[:5]

    # 兜底:从 Color Palette 表格提取强调色(跳过 bg 类暗色)
    in_palette = False
    for line in lines:
        if line.startswith("## Color Palette"):
            in_palette = True
            continue
        if in_palette:
            if line.startswith("## "):
                break
            m = re.search(r"`(#[0-9a-fA-F]{6})`", line)
            if m:
                token_match = re.search(r"--([\w-]+)", line)
                token = token_match.group(1) if token_match else ""
                # 跳过背景色、边框色、文字色——这些是暗色调，视觉区分度低
                if not token.startswith(("bg-", "border-", "text-", "font-")):
                    if m.group(1) not in colors:
                        colors.append(m.group(1))

    return colors[:5]


def list_themes() -> list[dict[str, str]]:
    """列出所有可用的设计系统主题。

    Returns:
        [{"id": "paper-linen", "name": "Paper Linen", "description": "暖纸衬线人文风", "colors": ["#faf9f5", "#d97757", "#6a9bcc"]}, ...]
    """
    themes: list[dict[str, str]] = []
    if not _ASSETS_DIR.is_dir():
        return themes

    for fname in sorted(os.listdir(_ASSETS_DIR)):
        if not fname.endswith(".md"):
            continue
        theme_id = fname[:-3]
        content = load_theme(theme_id)
        # 从文件第一行提取标题
        first_line = content.split("\n")[0].strip("# ").strip() if content else theme_id
        # 提取描述（第二段标题后第一句话）
        desc = ""
        lines = content.split("\n")
        in_section = False
        for line in lines:
            if line.startswith("## Visual Theme"):
                in_section = True
                continue
            if in_section and line.strip() and not line.startswith("#"):
                desc = line.strip()
                break

        # 提取配色
        colors = _extract_theme_colors(content)

        themes.append({
            "id": theme_id,
            "name": first_line.split(" — ")[0] if " — " in first_line else first_line,
            "description": desc or first_line,
            "colors": colors,
        })

    return themes


def theme_display_name(theme_id: Optional[str]) -> str:
    """主题 ID → 显示名（来自 .md 文件第一行标题）。

    自动解析主题别名（如 midnight-ops → monitor-dark）。
    """
    if not theme_id:
        return ""
    # 解析别名
    ALIASES = {
        "midnight-ops": "monitor-dark",
        "paper-brief": "minimal-doc",
        "dark-ops": "monitor-dark",
    }
    resolved = ALIASES.get(theme_id, theme_id)
    for t in list_themes():
        if t["id"] == resolved:
            return t["name"]
    return ""


def resolve_theme_id(id_or_name: Optional[str]) -> str:
    """把主题 ID 或显示名解析为规范主题 ID。"""
    key = (id_or_name or "").strip()
    if not key:
        return ""
    for t in list_themes():
        if t["id"] == key or t["name"] == key:
            return t["id"]
    return ""


def load_theme(theme_id: str) -> str:
    """加载指定设计系统的完整 .md 内容。

    支持主题别名（向后兼容旧名称）：
    - midnight-ops → monitor-dark
    - paper-brief → minimal-doc（接近）

    Args:
        theme_id: 设计系统 ID（文件名去掉 .md），如 "paper-linen"

    Returns:
        设计系统 Markdown 内容，未找到返回空字符串
    """
    # 主题别名映射（兼容旧名称）
    ALIASES = {
        "midnight-ops": "monitor-dark",
        "paper-brief": "minimal-doc",
        "dark-ops": "monitor-dark",
    }
    resolved = ALIASES.get(theme_id, theme_id)

    if resolved in _cache:
        return _cache[resolved]

    filepath = _ASSETS_DIR / f"{resolved}.md"
    if not filepath.is_file():
        return ""

    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    _cache[resolved] = content
    return content


def build_design_context(theme_id: Optional[str]) -> str:
    """构建注入到 LLM Prompt 中的设计系统上下文（用于 Agent Skill 模式）。

    Args:
        theme_id: 设计系统 ID，None 或空字符串表示使用默认深色风

    Returns:
        设计系统描述字符串，可直接拼接到 Prompt 中
    """
    if not theme_id:
        return _default_design_context()

    content = load_theme(theme_id)
    if not content:
        return _default_design_context()

    return f"""
【设计系统规范 — 必须严格遵循】
以下是你要使用的设计系统。生成的 HTML 必须严格遵循以下配色、字体、圆角、阴影和组件风格：

{content}

---
【重要提醒】
- 所有颜色使用上述 Color Palette 中的 CSS 变量值
- 圆角、阴影、动效严格遵循上述规范
- 使用上述 Typography 中指定的字体
- 组件风格遵循上述 Component Patterns
"""


def _default_design_context() -> str:
    """默认风格（fallback）— 当主题 ID 不存在时使用。"""
    return """
【设计系统规范 — 默认深色酷炫风】
- 背景: #0A0B0D (近黑微冷，禁止纯黑)
- 卡片: #13151A + 1px #23272F 边框 + 3px 圆角
- 主色: #2D5BFF (深蓝，仅关键数据/交互)
- 次色: #5B8AFF (数据高光)
- 文字: #E6E8EC (off-white，禁止纯白)
- 次要文字: #8A8F98
- 字体: Inter；数字用 IBM Plex Mono + tabular-nums
- 圆角: 2-4px (锐利，禁止大圆角)
- 阴影: 不用 (靠 1px 边框分层)
- 图表: ECharts 暗色主题，系列色单色蓝阶
- 禁止: text-shadow/发光、backdrop-filter 毛玻璃、渐变文字、青色 #00E5FF
"""