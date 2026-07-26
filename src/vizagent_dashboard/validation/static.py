"""静态验证 — 编译后 HTML 的质量检查。

从 viz-agent-team/backend/agents/quality.py 提取（参考源码 commit 见 upstream-manifest.toml）。

保留的 check_* 函数（纯静态检查，无需 LLM / 浏览器）：
- check_html_truncation：检查 HTML 是否被截断
- count_charts_in_html：统计图表类型和数量
- check_overlaps：检查图表元素是否重叠（防御性：兼容 list[str] / list[dict]）
- check_zero_size：检查零尺寸图表
- _to_float / _is_numeric：数值清洗

丢弃：
- 所有依赖 PRD 文本匹配的 coverage 检查（在 Skill 中不适用，spec 直接表达意图）
- LLM 驱动的评价（review_node / test_node / release_node 不在 Skill 范围内）
"""

from __future__ import annotations

import re
from typing import Any


# ═══════════════════════════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════════════════════════


def _to_float(v: Any) -> float | None:
    """容错转 float（剥 $,¥,%,千分位逗号）。"""
    try:
        cleaned = str(v).replace(",", "").replace("¥", "").replace("$", "").replace("%", "").strip()
        return float(cleaned) if cleaned else None
    except (ValueError, TypeError):
        return None


def _is_numeric(v: Any) -> bool:
    cleaned = str(v).replace(",", "").replace("¥", "").replace("$", "").replace("%", "").strip()
    if not cleaned:
        return False
    try:
        float(cleaned)
        return True
    except ValueError:
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# HTML 静态检查
# ═══════════════════════════════════════════════════════════════════════════════


def check_html_truncation(html_content: str) -> dict[str, Any]:
    """检测 HTML 是否被截断。

    判断优先级：
    1. 以 </html> 结尾 → 完整，不检查标签配对
    2. 有 </body> 无 </html> → 可能截断
    3. 无 </body> 无 </html> → 截断
    """
    issues: list[str] = []
    truncated = False

    last_200 = html_content[-200:] if len(html_content) > 200 else html_content
    has_closing_html = "</html>" in last_200.lower()
    has_closing_body = "</body>" in last_200.lower()

    if not has_closing_html and not has_closing_body:
        truncated = True
        issues.append("HTML 末尾缺少 </html> 或 </body> 闭合标签")
    elif has_closing_body and not has_closing_html:
        truncated = True
        issues.append("HTML 末尾缺少 </html> 闭合标签")

    score = 100
    if truncated:
        score = max(30, 100 - len(issues) * 35)

    return {
        "is_truncated": truncated,
        "score": score,
        "issues": issues,
        "html_length": len(html_content),
        "has_closing_html": has_closing_html,
        "has_closing_body": has_closing_body,
    }


def count_charts_in_html(html_content: str) -> dict[str, int]:
    """统计 HTML 中的 ECharts 图表类型和数量。

    Returns:
        {"line": 2, "bar": 1, "pie": 1, "map": 0, "kpi": 0, "total": 4}
    """
    counts: dict[str, int] = {"line": 0, "bar": 0, "pie": 0, "scatter": 0, "map": 0, "kpi": 0, "total": 0}

    # 数 ECharts init 调用数
    n_init = len(re.findall(r"echarts\.init\s*\(", html_content))
    counts["total"] = n_init

    # 数 series: type 出现次数（按 series 类型）
    for series_type in ["line", "bar", "pie", "scatter", "map"]:
        counts[series_type] = len(re.findall(rf'"type"\s*:\s*"{series_type}"', html_content))

    # 数 KPI 卡片
    counts["kpi"] = len(re.findall(r'class="kpi-card"', html_content))

    return counts


def check_overlaps(chart_options: list[Any]) -> list[str]:
    """检查图表元素是否重叠。

    防御性设计：兼容浏览器返回的 overlaps 格式（list[str] 或 list[dict]）。
    ★ F4 修复：isinstance(o, dict) 防御 list[str] 类型。

    Returns:
        重叠描述列表（最多 3 条）。空列表表示无重叠。
    """
    issues: list[str] = []

    if not chart_options:
        return issues

    # 简单几何检查：每个 chart option 的 grid + width/height 重叠检测
    # （这里是简化版，真实检查由 Playwright 完成）
    occupied: list[tuple[float, float, float, float]] = []

    def overlap_area(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> float:
        x1 = max(a[0], b[0])
        y1 = max(a[1], b[1])
        x2 = min(a[2], b[2])
        y2 = min(a[3], b[3])
        if x2 > x1 and y2 > y1:
            return (x2 - x1) * (y2 - y1)
        return 0.0

    for opt in chart_options:
        if not isinstance(opt, dict):
            continue
        # 从 option 提取 grid 区域（简化）
        grid = opt.get("grid", {})
        rect = (0, 0, 100, 100)  # 占位，实际由浏览器检测
        for prev in occupied:
            if overlap_area(rect, prev) > 50:  # 阈值
                issues.append(f"图表与已有图表重叠 ({rect} vs {prev})")
                break
        occupied.append(rect)

    return issues[:3]


def check_zero_size(chart_options: list[Any]) -> list[str]:
    """检查是否有零尺寸图表。"""
    issues: list[str] = []
    for idx, opt in enumerate(chart_options):
        if not isinstance(opt, dict):
            continue
        series = opt.get("series", [])
        if isinstance(series, list) and len(series) == 0:
            issues.append(f"图表 {idx + 1} 缺少 series 数据")
    return issues


def check_duplicate_maps(html_content: str) -> list[str]:
    """检查是否包含重复地图。"""
    issues: list[str] = []
    map_count = len(re.findall(r"registerMap\(", html_content))
    if map_count > 2:
        issues.append(f"包含 {map_count} 个地图实例，超过 2 个上限")
    return issues


def check_empty_options(html_content: str) -> list[str]:
    """检查是否有空 ECharts option。"""
    issues: list[str] = []
    # 空 option 的特征：setOption({}) 后面跟逗号或空对象
    matches = re.findall(r"setOption\(\s*\{[^}]{0,5}\}\s*\)", html_content)
    if matches:
        for _ in matches:
            issues.append("ECharts option 内容为空")
    return issues


def validate_html(html_content: str) -> dict[str, Any]:
    """综合验证：跑全部静态检查，返回聚合报告。"""
    all_issues: list[str] = []

    trunc = check_html_truncation(html_content)
    all_issues.extend(trunc["issues"])

    dup_maps = check_duplicate_maps(html_content)
    all_issues.extend(dup_maps)

    empty_opts = check_empty_options(html_content)
    all_issues.extend(empty_opts)

    return {
        "is_valid": not trunc["is_truncated"] and len(all_issues) == 0,
        "is_truncated": trunc["is_truncated"],
        "score": trunc["score"],
        "issues": all_issues,
        "chart_counts": count_charts_in_html(html_content),
        "html_length": len(html_content),
    }