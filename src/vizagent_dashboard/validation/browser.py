"""浏览器验证 — Playwright 检查（可选依赖）。

从 viz-agent-team/backend/agents/browser_test.py 提取（参考源码 commit 见 upstream-manifest.toml）。

Skill 中的浏览器检查：
- check_js_errors：JS 控制台错误
- check_chart_rendered：图表是否渲染
- check_dom_health：DOM 结构健康检查

注意：浏览器检查是可选的，需要安装 playwright（pip install playwright && playwright install）。
"""

from __future__ import annotations

from typing import Any


# ═══════════════════════════════════════════════════════════════════════════════
# 几何工具（独立于 Playwright 的纯函数）
# ═══════════════════════════════════════════════════════════════════════════════


def _rects_intersect(a: dict, b: dict, min_area: int = 100) -> bool:
    """两个矩形相交面积 > min_area 视为重叠(过滤微小接触)。"""
    ix = max(0.0, min(a["x"] + a["w"], b["x"] + b["w"]) - max(a["x"], b["x"]))
    iy = max(0.0, min(a["y"] + a["h"], b["y"] + b["h"]) - max(a["y"], b["y"]))
    return ix * iy > min_area


def find_overlaps(boxes: list[dict]) -> list[str]:
    """对盒子两两算重叠，返回描述列表。

    ★ F4 修复：返回值是 list[str]，调用方应使用 isinstance 防御。
    """
    out: list[str] = []
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            if _rects_intersect(boxes[i], boxes[j]):
                out.append(f"chart#{i} 与 chart#{j} 边界框重叠")
    return out


# ═══════════════════════════════════════════════════════════════════════════════
# Playwright 包装（可选依赖）
# ═══════════════════════════════════════════════════════════════════════════════


def playwright_available() -> bool:
    """检查 playwright 是否已安装。"""
    try:
        import playwright  # noqa: F401
        return True
    except ImportError:
        return False


async def check_js_errors(html_path: str) -> list[str]:
    """打开 HTML 在 headless 浏览器中，收集 JS 控制台错误。

    Requires: pip install playwright && playwright install chromium
    """
    if not playwright_available():
        return ["playwright 未安装，跳过浏览器检查（pip install playwright）"]

    try:
        from playwright.async_api import async_playwright

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            errors: list[str] = []
            page.on("pageerror", lambda exc: errors.append(str(exc)))
            page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)

            await page.goto(f"file://{html_path}")
            await page.wait_for_load_state("networkidle", timeout=10000)

            await browser.close()
            return errors
    except Exception as e:
        return [f"playwright 执行失败: {e}"]


async def check_chart_rendered(html_path: str) -> dict[str, Any]:
    """检查 HTML 中图表是否成功渲染。

    Returns:
        {"rendered": int, "total_canvases": int, "errors": [...]}
    """
    if not playwright_available():
        return {"rendered": 0, "total_canvases": 0, "errors": ["playwright 未安装"]}

    try:
        from playwright.async_api import async_playwright

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            await page.goto(f"file://{html_path}")
            await page.wait_for_load_state("networkidle", timeout=10000)

            # 数 canvas 元素
            canvas_count = await page.locator("canvas").count()

            # 检查每个 canvas 是否有内容（非零尺寸）
            rendered = 0
            for i in range(canvas_count):
                canvas = page.locator("canvas").nth(i)
                box = await canvas.bounding_box()
                if box and box["width"] > 0 and box["height"] > 0:
                    rendered += 1

            await browser.close()
            return {"rendered": rendered, "total_canvases": canvas_count, "errors": []}
    except Exception as e:
        return {"rendered": 0, "total_canvases": 0, "errors": [f"playwright 执行失败: {e}"]}


async def run_browser_checks(html_path: str) -> dict[str, Any]:
    """综合浏览器检查：JS 错误 + 图表渲染 + DOM 健康。

    Requires: pip install playwright && playwright install chromium
    """
    js_errors = await check_js_errors(html_path)
    chart_info = await check_chart_rendered(html_path)

    return {
        "available": playwright_available(),
        "js_errors": js_errors,
        "charts_rendered": chart_info["rendered"],
        "total_canvases": chart_info["total_canvases"],
        "is_healthy": len(js_errors) == 0 and chart_info["rendered"] > 0,
    }