"""Playwright 浏览器质量门禁。"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def _rects_intersect(a: dict, b: dict, min_area: int = 100) -> bool:
    width = max(0.0, min(a["x"] + a["w"], b["x"] + b["w"]) - max(a["x"], b["x"]))
    height = max(0.0, min(a["y"] + a["h"], b["y"] + b["h"]) - max(a["y"], b["y"]))
    return width * height > min_area


def find_overlaps(boxes: list[dict]) -> list[str]:
    issues: list[str] = []
    for left in range(len(boxes)):
        for right in range(left + 1, len(boxes)):
            if _rects_intersect(boxes[left], boxes[right]):
                issues.append(f"panel#{left} 与 panel#{right} 边界框重叠")
    return issues


def playwright_available() -> bool:
    try:
        import playwright  # noqa: F401
        return True
    except ImportError:
        return False


async def run_browser_checks(
    html_path: str,
    *,
    viewport_width: int = 1920,
    viewport_height: int = 1080,
    screenshot_path: str | None = None,
) -> dict[str, Any]:
    """打开所有页签和地图 Tab，检查真实 option、Canvas、布局和错误。"""

    if not playwright_available():
        return {
            "available": False,
            "is_healthy": False,
            "errors": ["playwright 未安装，请安装 vizagent-dashboard[browser]"],
            "warnings": [],
            "charts_rendered": 0,
            "expected_charts": 0,
        }

    from playwright.async_api import async_playwright

    source = Path(html_path).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page(viewport={"width": viewport_width, "height": viewport_height})
        page.on("pageerror", lambda exc: errors.append(str(exc)))
        page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)
        try:
            await page.goto(source.as_uri(), wait_until="load", timeout=20_000)
            await page.wait_for_timeout(350)

            for selector in (".map-tab", ".page-tab"):
                count = await page.locator(selector).count()
                for index in range(count):
                    await page.locator(selector).nth(index).click()
                    await page.wait_for_timeout(80)
            # 回到首个页签与地图，截图展示默认状态。
            for selector in (".page-tab", ".map-tab"):
                if await page.locator(selector).count():
                    await page.locator(selector).first.click()
            await page.wait_for_timeout(150)

            metrics = await page.evaluate(
                """() => {
                  const payload = JSON.parse(document.getElementById('vizagent-chart-options')?.textContent || '[]');
                  const charts = payload.map(entry => {
                    const node = document.getElementById(entry.dom_id);
                    const chart = node && window.echarts ? echarts.getInstanceByDom(node) : null;
                    const option = chart ? chart.getOption() : null;
                    const series = option?.series || [];
                    const dataLengths = series.map(item => Array.isArray(item.data) ? item.data.length : 0);
                    const rect = node?.getBoundingClientRect();
                    return {
                      domId: entry.dom_id,
                      type: entry.type,
                      initialized: Boolean(chart),
                      visible: Boolean(node && node.offsetParent),
                      width: rect?.width || 0,
                      height: rect?.height || 0,
                      seriesCount: series.length,
                      dataLengths,
                      hasData: dataLengths.some(length => length > 0),
                    };
                  });
                  const panels = [...document.querySelectorAll('.panel, .kpi-card')]
                    .filter(node => node.offsetParent)
                    .map(node => {
                      const rect = node.getBoundingClientRect();
                      return {x: rect.x, y: rect.y, w: rect.width, h: rect.height};
                    });
                  return {
                    charts,
                    panels,
                    canvasCount: document.querySelectorAll('canvas').length,
                    scrollWidth: document.documentElement.scrollWidth,
                    scrollHeight: document.documentElement.scrollHeight,
                    innerWidth,
                    innerHeight,
                    chinaRegistered: Boolean(window.echarts?.getMap('china')),
                    worldRegistered: Boolean(window.echarts?.getMap('world')),
                    expectedMaps: JSON.parse(document.getElementById('vizagent-build-manifest')?.textContent || '{}').maps || [],
                  };
                }"""
            )
            if screenshot_path:
                await page.screenshot(path=str(Path(screenshot_path).resolve()), full_page=True)
        except Exception as exc:
            errors.append(f"playwright 执行失败: {exc}")
            metrics = {
                "charts": [],
                "panels": [],
                "canvasCount": 0,
                "scrollWidth": 0,
                "scrollHeight": 0,
                "innerWidth": viewport_width,
                "innerHeight": viewport_height,
                "chinaRegistered": False,
                "worldRegistered": False,
                "expectedMaps": [],
            }
        finally:
            await browser.close()

    chart_issues = []
    for chart in metrics["charts"]:
        if not chart["initialized"]:
            chart_issues.append(f"{chart['domId']} 未初始化")
        # 零尺寸只对当前可见的图生效；隐藏 Tab（page-tabs / map-tabs）上的图
        # 在其页签被激活前 offsetParent 为 null，容器 rect 为 0 是预期行为。
        if chart.get("visible") and (chart["width"] <= 0 or chart["height"] <= 0):
            chart_issues.append(f"{chart['domId']} 容器尺寸为零")
        if chart["seriesCount"] <= 0:
            chart_issues.append(f"{chart['domId']} 缺少 series")
        elif not chart["hasData"]:
            chart_issues.append(f"{chart['domId']} 没有有效数据")
    errors.extend(chart_issues)

    if "china" in metrics["expectedMaps"] and not metrics["chinaRegistered"]:
        errors.append("中国地图未注册")
    if "world" in metrics["expectedMaps"] and not metrics["worldRegistered"]:
        errors.append("世界地图未注册")

    overlaps = find_overlaps(metrics["panels"])
    errors.extend(overlaps)
    if metrics["scrollWidth"] > metrics["innerWidth"] + 2:
        errors.append(f"页面横向溢出：{metrics['scrollWidth']}/{metrics['innerWidth']}px")
    if metrics["scrollHeight"] > metrics["innerHeight"] + 24:
        warnings.append(f"页面纵向滚动：{metrics['scrollHeight']}/{metrics['innerHeight']}px")

    return {
        "available": True,
        "is_healthy": not errors,
        "errors": errors,
        "warnings": warnings,
        "charts_rendered": sum(1 for chart in metrics["charts"] if chart["initialized"] and chart["hasData"]),
        "expected_charts": len(metrics["charts"]),
        "canvas_count": metrics["canvasCount"],
        "maps_registered": {
            "china": metrics["chinaRegistered"],
            "world": metrics["worldRegistered"],
        },
        "overlaps": overlaps,
        "viewport": {
            "width": metrics["innerWidth"],
            "height": metrics["innerHeight"],
            "scroll_width": metrics["scrollWidth"],
            "scroll_height": metrics["scrollHeight"],
        },
        "charts": metrics["charts"],
    }


async def check_js_errors(html_path: str) -> list[str]:
    result = await run_browser_checks(html_path)
    return result.get("errors", [])


async def check_chart_rendered(html_path: str) -> dict[str, Any]:
    result = await run_browser_checks(html_path)
    return {
        "rendered": result.get("charts_rendered", 0),
        "total_canvases": result.get("canvas_count", 0),
        "errors": result.get("errors", []),
    }
