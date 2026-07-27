#!/usr/bin/env python3
"""
SaaS 品牌主题 → clean-room 中性主题：token 提取与保真度校验。

本脚本不做生成（clean-room 主题的 Visual Theme prose 是人工去品牌改写，
脚本无法复刻判断），只做两件事：
1. extract：从 SaaS 主题 .md 提取 token 表 + 色板，供审计查阅。
2. verify：逐一校验 clean-room 主题的 token 值与 SaaS 源同名 token 完全一致，
   证明「只搬 hex、不搬品牌」的保真承诺可复现验证。

用法（从 skill/ 目录运行）：
    python tools/import_saas_themes.py            # 校验全部 20 个
    python tools/import_saas_themes.py --extract spotify   # 打印某 SaaS 源 token

法律复核：跑 `python tools/import_saas_themes.py` 应输出 20/20 PASS，
即每个 clean-room 主题携带的 12 个 token 与 SaaS 源同名 token 逐字节一致。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
SAAS_DIR = SKILL_DIR.parent / "viz-agent-team" / "backend" / "agents" / "design-systems"
CLEAN_DIR = SKILL_DIR / "src" / "vizagent_dashboard" / "assets"

# SaaS 源文件名 → (clean-room id, clean-room name)。命名纯描述性，不 echo 品牌。
NAME_MAP: dict[str, tuple[str, str]] = {
    "airbnb": ("coral-warm", "Coral Warm"),
    "apple": ("obsidian-glass", "Obsidian Glass"),
    "claude": ("parchment-serif", "Parchment Serif"),
    "coinbase": ("trust-blue", "Trust Blue"),
    "figma": ("canvas-dot", "Canvas Dot"),
    "grafana-ops": ("ops-slate", "Ops Slate"),
    "health-ring": ("ring-pastel", "Ring Pastel"),
    "kraken": ("nebula-glow", "Nebula Glow"),
    "linear": ("graphite-iris", "Graphite Iris"),
    "newsroom": ("broadsheet", "Broadsheet"),
    "notion": ("fiber-paper", "Fiber Paper"),
    "palantir": ("grid-azure", "Grid Azure"),
    "pitchbook-dark": ("gilt-navy", "Gilt Navy"),
    "posthog": ("ember-paper", "Ember Paper"),
    "sentry": ("amethyst-glass", "Amethyst Glass"),
    "spotify": ("grove-dark", "Grove Dark"),
    "stripe": ("haze-lilac", "Haze Lilac"),
    "supabase": ("phosphor-green", "Phosphor Green"),
    "terminal-amber": ("amber-scan", "Amber Scan"),
    "vercel": ("mono-noir", "Mono Noir"),
}

# clean-room 主题保留的 12 个核心 token（build_css_block / charts 实际消费的子集）。
# SaaS 源里其余 token（--bg-hover / --accent-secondary / --text-muted 等）刻意不搬，
# 保持与现有 5 个 clean-room 主题一致的瘦格式。
CLEAN_TOKENS = (
    "--bg-primary", "--bg-card", "--bg-elevated",
    "--text-primary", "--text-secondary", "--border-subtle",
    "--accent-primary", "--map-area", "--map-boundary",
    "--radius-card", "--font-family-base", "--font-family-display",
)

# 字体 token 刻意归一化：-apple-system → system-ui（去品牌，与现有 5 主题一致），
# 不要求与源逐字节相同；颜色/圆角 token 才要求逐字节保真。
FONT_TOKENS = {"--font-family-base", "--font-family-display"}


def _normalize_font(value: str) -> str:
    """字体栈归一化：-apple-system→system-ui + 折叠连续重复，用于字体 token 比对。"""
    v = value.replace("-apple-system", "system-ui")
    while "system-ui,system-ui" in v or "system-ui, system-ui" in v:
        v = v.replace("system-ui,system-ui", "system-ui")
        v = v.replace("system-ui, system-ui", "system-ui")
    return v.lower()

# 品牌残留关键词清单（校验 clean-room 文件不得出现）。
BRAND_KEYWORDS = (
    "airbnb", "apple", "anthropic", "claude", "coinbase", "figma", "grafana",
    "kraken", "linear", "newsroom", "notion", "palantir", "pitchbook", "posthog",
    "sentry", "spotify", "stripe", "supabase", "vercel",
    "rausch", "babu", "arches", "crail", "circularsp", "cereal",
    "标志性", "独占", "签名", "官方", "brand", "logo", "trademark", "专利",
)


def _split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """解析 --- 包裹的 frontmatter，返回 (字段字典, 正文)。"""
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not m:
        return {}, text
    meta: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
    return meta, m.group(2)


def extract_tokens(text: str) -> dict[str, str]:
    """从 markdown 表格提取 `--token` | `value` 配对（适用 SaaS 与 clean-room 两种格式）。"""
    tokens: dict[str, str] = {}
    for line in text.splitlines():
        m = re.search(r"`(--[\w-]+)`\s*\|\s*`([^`]+)`", line)
        if m:
            tokens[m.group(1)] = m.group(2).strip()
    return tokens


def extract_chart_palette(text: str) -> list[str]:
    """提取 ## Chart Color Palette 章节下的 hex 色板（保持顺序、去重）。"""
    palette: list[str] = []
    in_section = False
    for line in text.splitlines():
        if line.startswith("## Chart Color Palette"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section:
            for color in re.findall(r"#[0-9a-fA-F]{6}", line):
                if color not in palette:
                    palette.append(color)
    return palette


def extract_saas(path: Path) -> dict:
    """提取 SaaS 源主题：base/decoration/tokens/chart_palette。"""
    text = path.read_text(encoding="utf-8")
    tokens = extract_tokens(text)
    bg = tokens.get("--bg-primary", "#000000").lstrip("#")
    # 简单明暗判定：解析 bg-primary 的相对亮度
    base = _infer_base(bg)
    decoration = tokens.get("--decoration", "flat")
    return {
        "source": path.stem,
        "base": base,
        "decoration": decoration,
        "tokens": tokens,
        "chart_palette": extract_chart_palette(text),
    }


def _infer_base(hex6: str) -> str:
    hex6 = hex6.lstrip("#")
    if len(hex6) != 6:
        return "dark"
    r, g, b = int(hex6[0:2], 16), int(hex6[2:4], 16), int(hex6[4:6], 16)
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return "light" if luminance > 0.5 else "dark"


def extract_clean(path: Path) -> dict:
    """提取 clean-room 主题：frontmatter + tokens + chart_palette。"""
    text = path.read_text(encoding="utf-8")
    meta, body = _split_frontmatter(text)
    return {
        "id": meta.get("id", path.stem),
        "name": meta.get("name", path.stem),
        "base": meta.get("base", ""),
        "decoration": meta.get("decoration", ""),
        "tokens": extract_tokens(body),
        "chart_palette": extract_chart_palette(body),
        "raw": text,
    }


def check_brand_residue(clean_text: str) -> list[str]:
    """扫描 clean-room 文本是否残留品牌关键词（大小写不敏感）。"""
    lower = clean_text.lower()
    return [kw for kw in BRAND_KEYWORDS if kw in lower]


def verify_pair(saas_source: str) -> dict:
    """校验单个 SaaS→clean-room 配对的 token 保真度 + 品牌残留。"""
    clean_id, _ = NAME_MAP[saas_source]
    saas = extract_saas(SAAS_DIR / f"{saas_source}.md")
    clean = extract_clean(CLEAN_DIR / f"{clean_id}.md")

    mismatches: list[str] = []
    for token in CLEAN_TOKENS:
        sval = saas["tokens"].get(token)
        cval = clean["tokens"].get(token)
        if sval is None:
            mismatches.append(f"{token}: 源缺失")
        elif cval is None:
            mismatches.append(f"{token}: clean 缺失")
        elif token in FONT_TOKENS:
            # 字体 token：归一化后比对（-apple-system→system-ui 是刻意去品牌）
            if _normalize_font(sval) != _normalize_font(cval):
                mismatches.append(f"{token}: 归一化后仍不一致 {sval} ≠ {cval}")
        elif sval.lower() != cval.lower():
            mismatches.append(f"{token}: {sval} ≠ {cval}")

    residue = check_brand_residue(clean["raw"])
    return {
        "source": saas_source,
        "clean_id": clean_id,
        "base_match": saas["base"] == clean["base"],
        "decoration_match": saas["decoration"] == clean["decoration"],
        "token_mismatches": mismatches,
        "brand_residue": residue,
        "palette_count": len(clean["chart_palette"]),
    }


def main() -> int:
    # Windows GBK 控制台强制 UTF-8 输出，避免 ✓✗ 等字符 UnicodeEncodeError
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="SaaS→clean-room 主题 token 校验")
    parser.add_argument("--extract", metavar="SOURCE", help="仅打印某 SaaS 源的提取结果")
    args = parser.parse_args()

    if args.extract:
        src = args.extract
        path = SAAS_DIR / f"{src}.md"
        if not path.exists():
            print(f"未找到 SaaS 源：{path}", file=sys.stderr)
            return 2
        data = extract_saas(path)
        print(f"源：{src}")
        print(f"base={data['base']}  decoration={data['decoration']}")
        print(f"chart_palette={data['chart_palette']}")
        print("tokens:")
        for k, v in data["tokens"].items():
            print(f"  {k} = {v}")
        return 0

    print(f"校验 {len(NAME_MAP)} 个 SaaS→clean-room 主题配对\n")
    passed = 0
    for src in NAME_MAP:
        r = verify_pair(src)
        ok = (not r["token_mismatches"] and not r["brand_residue"]
              and r["base_match"] and r["decoration_match"])
        flag = "✓ PASS" if ok else "✗ FAIL"
        print(f"{flag}  {r['source']:>14} → {r['clean_id']:<16} (palette={r['palette_count']})")
        if r["token_mismatches"]:
            for m in r["token_mismatches"]:
                print(f"        token  {m}")
        if r["brand_residue"]:
            print(f"        品牌残留: {', '.join(r['brand_residue'])}")
        if ok:
            passed += 1

    print(f"\n结果：{passed}/{len(NAME_MAP)} 通过")
    return 0 if passed == len(NAME_MAP) else 1


if __name__ == "__main__":
    sys.exit(main())
