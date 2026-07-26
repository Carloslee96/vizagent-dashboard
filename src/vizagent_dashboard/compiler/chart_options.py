"""图表 option 生成（数据驱动版）。

从 viz-agent-team/backend/agents/chart_options.py 提取（参考源码 commit 见 upstream-manifest.toml）。

去 SaaS 依赖策略：
- 保留：Pydantic schema、纯辅助函数（_guess_chart_type, _clean_number 等）
- 保留：简化版 build_chart_option（确定性生成常见图表的 ECharts option JSON）
- 丢弃：所有 LangChain SystemMessage/HumanMessage + LLMClient.chat 调用

Skill 中使用方式：
  - Spec 模式：编译器从 DashboardSpec 直接生成 option_json（零 API 调用）
  - Agent Skill 模式：宿主 AI 读 dashboard_spec.py 后调用 build_chart_option 生成 option
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# Pydantic Schemas
# ═══════════════════════════════════════════════════════════════════════════════


class ChartOption(BaseModel):
    """单个图表的 ECharts option。"""
    chart_id: int = Field(description="图表序号,必须与输入的 chart_id 一致")
    chart_type: str = Field(description="ECharts 系列类型,如 bar/line/pie/scatter")
    title: str = Field(description="图表标题")
    option_json: str = Field(description="ECharts option 对象的 JSON 字符串")


class ChartOptionBundle(BaseModel):
    """一批图表 options。"""
    charts: list[ChartOption] = Field(description="本批图表 option 列表")


# ═══════════════════════════════════════════════════════════════════════════════
# 纯辅助函数
# ═══════════════════════════════════════════════════════════════════════════════


def _guess_chart_type(name: str) -> str:
    """根据图表名猜测类型（fallback）。"""
    name_lower = name.lower()
    if "饼" in name or "占比" in name or "pie" in name_lower:
        return "pie"
    if "折线" in name or "趋势" in name or "line" in name_lower:
        return "line"
    if "柱" in name or "bar" in name_lower or "排行" in name:
        return "bar"
    if "散点" in name or "scatter" in name_lower:
        return "scatter"
    if "面积" in name or "area" in name_lower:
        return "area"
    return "bar"


def _clean_number(value: Any) -> int | float | None:
    """清洗数值：去除千分位、货币符号、百分号。"""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return value
    try:
        cleaned = str(value).replace(",", "").replace("¥", "").replace("$", "").replace("￥", "").replace("%", "").strip()
        if not cleaned:
            return None
        if "." in cleaned:
            return float(cleaned)
        return int(cleaned)
    except (ValueError, TypeError):
        return None


def _extract_chart_inventory_short(prd: str) -> str:
    """从需求文本提取图表清单（短摘要）。"""
    # 找 "图表清单" 之后的内容
    lines = prd.split("\n")
    capturing = False
    inventory_lines = []
    for line in lines:
        if "图表清单" in line or "图表列表" in line:
            capturing = True
            continue
        if capturing:
            if line.strip().startswith("#") or line.strip().startswith("【"):
                if inventory_lines:
                    break
            if line.strip():
                inventory_lines.append(line.strip())
            if len(inventory_lines) > 10:
                break
    return "\n".join(inventory_lines) if inventory_lines else "(无图表清单)"


def _extract_md_section(text: str, header: str) -> str:
    """从 markdown 文本中提取指定标题段的内容。"""
    lines = text.split("\n")
    capturing = False
    section_lines = []
    for line in lines:
        if line.startswith(f"## {header}"):
            capturing = True
            continue
        if capturing:
            if line.startswith("## "):
                break
            section_lines.append(line)
    return "\n".join(section_lines).strip()


def _chart_fingerprint(design_ctx: str) -> str:
    """从设计系统上下文中提取 Chart Fingerprint 段。"""
    return _extract_md_section(design_ctx, "Chart Fingerprint")


def _design_summary(design_ctx: str) -> str:
    """从设计系统上下文中提取 Visual Theme 段。"""
    return _extract_md_section(design_ctx, "Visual Theme")


def _chart_colors_from_vars(css_vars: dict[str, str] | None) -> dict[str, str]:
    """从 CSS 变量字典中提取图表相关颜色（带 fallback）。"""
    if not css_vars:
        css_vars = {}

    def get(name: str, fallback: str) -> str:
        return css_vars.get(name) or fallback

    return {
        "tooltip_bg": get("--bg-card", "#13151A"),
        "tooltip_text": get("--text-primary", "#E6E8EC"),
        "grid_color": get("--border-subtle", "#23272F"),
        "ax_color": get("--text-secondary", "#8A8F98"),
        "series_color": get("--accent-primary", "#2D5BFF"),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 确定性图表 option 生成（核心函数）
# ═══════════════════════════════════════════════════════════════════════════════


def build_chart_option(
    chart_type: str,
    title: str,
    data: list[dict],
    x_field: str,
    y_field: str | list[str],
    chart_palette: list[str] | None = None,
    css_vars: dict[str, str] | None = None,
) -> str:
    """根据图表类型和数据生成 ECharts option JSON（确定性，零 LLM 调用）。

    Args:
        chart_type: 图表类型（line/bar/pie/scatter/area/wordcloud/treemap）
        title: 图表标题
        data: 数据行列表 [{"field1": val1, "field2": val2, ...}, ...]
        x_field: 横轴字段名（维度）
        y_field: 纵轴字段名（指标），单值或列表（多系列）
        chart_palette: 系列色板（hex 列表）
        css_vars: 主题 CSS 变量

    Returns:
        ECharts option JSON 字符串。无法生成时返回 None。
    """
    if not data:
        logger.warning(f"build_chart_option: empty data for chart '{title}'")
        return json.dumps({"title": {"text": title}})

    palette = chart_palette or ["#2D5BFF", "#5B8AFF", "#8AAEFF", "#B4CCFF", "#3DAB63"]
    colors = _chart_colors_from_vars(css_vars)
    chart_type = chart_type.lower().replace("map:", "map")

    # 标准化 y_field 为列表
    y_fields = [y_field] if isinstance(y_field, str) else y_field

    categories = [
        str(row.get(x_field, "")).strip() or f"第{idx + 1}项"
        for idx, row in enumerate(data)
    ]

    base: dict[str, Any] = {
        "backgroundColor": "transparent",
        "color": palette,
        "animationDuration": 600,
        "animationEasing": "cubicOut",
        "title": {"text": title, "left": "left", "textStyle": {"color": colors["tooltip_text"], "fontSize": 14, "fontWeight": "normal"}},
        "tooltip": {
            "trigger": "axis" if chart_type in {"line", "area", "bar"} else "item",
            "backgroundColor": colors["tooltip_bg"],
            "borderColor": colors["grid_color"],
            "textStyle": {"color": colors["tooltip_text"], "fontSize": 12},
        },
    }

    # ──────── 饼图 ────────
    if chart_type == "pie":
        if not y_fields:
            return json.dumps(base)
        metric = y_fields[0]
        pie_data = [
            {"name": cat, "value": _clean_number(row.get(metric))}
            for cat, row in zip(categories, data)
            if _clean_number(row.get(metric)) is not None
        ]
        if not pie_data:
            return json.dumps(base)
        base["legend"] = {"type": "scroll", "top": 0, "right": 0, "textStyle": {"color": colors["ax_color"], "fontSize": 10}}
        base["series"] = [{
            "name": metric,
            "type": "pie",
            "radius": ["28%", "68%"],
            "center": ["45%", "56%"],
            "startAngle": 90,
            "avoidLabelOverlap": True,
            "label": {"show": True, "color": colors["ax_color"], "fontSize": 10, "formatter": "{b} {c}"},
            "labelLine": {"length": 8, "length2": 6},
            "emphasis": {"scale": True, "scaleSize": 6, "focus": "self"},
            "data": pie_data,
        }]
        return json.dumps(base, ensure_ascii=False)

    # ──────── 折线 / 面积 ────────
    if chart_type in {"line", "area"}:
        valid_y = [y for y in y_fields if any(_clean_number(row.get(y)) is not None for row in data)]
        if not valid_y:
            return json.dumps(base)
        base.update({
            "grid": {"top": "18%", "bottom": "10%", "left": "5%", "right": "7%", "containLabel": True},
            "xAxis": {"type": "category", "name": x_field, "boundaryGap": False, "data": categories,
                      "axisLine": {"lineStyle": {"color": colors["grid_color"]}},
                      "axisLabel": {"color": colors["ax_color"], "fontSize": 10}},
            "yAxis": {"type": "value", "name": " / ".join(valid_y),
                      "axisLine": {"lineStyle": {"color": colors["grid_color"]}},
                      "axisLabel": {"color": colors["ax_color"], "fontSize": 10},
                      "splitLine": {"lineStyle": {"color": colors["grid_color"], "type": "dashed"}}},
            "legend": {"show": len(valid_y) > 1, "top": 0, "right": 0, "textStyle": {"color": colors["ax_color"], "fontSize": 10}},
            "series": [],
        })
        for idx, metric in enumerate(valid_y):
            values = [_clean_number(row.get(metric)) for row in data]
            series: dict[str, Any] = {
                "name": metric, "type": "line", "data": values,
                "smooth": True, "showSymbol": False, "connectNulls": False,
                "lineStyle": {"width": 2, "color": palette[idx % len(palette)]},
                "itemStyle": {"color": palette[idx % len(palette)]},
                "emphasis": {"focus": "series"},
            }
            if chart_type == "area":
                series["areaStyle"] = {"opacity": 0.14}
            base["series"].append(series)
        return json.dumps(base, ensure_ascii=False)

    # ──────── 柱状 ────────
    if chart_type == "bar":
        valid_y = [y for y in y_fields if any(_clean_number(row.get(y)) is not None for row in data)]
        if not valid_y:
            return json.dumps(base)
        horizontal = len(data) > 8 or bool(re.search(r"排名|排行|偏好|分布", title))
        if horizontal:
            base["xAxis"] = {"type": "value", "name": " / ".join(valid_y),
                             "axisLine": {"lineStyle": {"color": colors["grid_color"]}},
                             "axisLabel": {"color": colors["ax_color"], "fontSize": 10},
                             "splitLine": {"lineStyle": {"color": colors["grid_color"], "type": "dashed"}}}
            base["yAxis"] = {"type": "category", "name": x_field, "data": categories,
                             "inverse": True,
                             "axisLine": {"lineStyle": {"color": colors["grid_color"]}},
                             "axisLabel": {"color": colors["ax_color"], "fontSize": 9, "interval": 0}}
            base["grid"] = {"top": "14%", "bottom": "8%", "left": "5%", "right": "10%", "containLabel": True}
            bar_pos = "right"
        else:
            base["xAxis"] = {"type": "category", "name": x_field, "data": categories,
                             "axisLine": {"lineStyle": {"color": colors["grid_color"]}},
                             "axisLabel": {"color": colors["ax_color"], "fontSize": 10,
                                           "interval": 0, "rotate": 25 if any(len(c) > 5 for c in categories) else 0}}
            base["yAxis"] = {"type": "value", "name": " / ".join(valid_y),
                             "axisLine": {"lineStyle": {"color": colors["grid_color"]}},
                             "axisLabel": {"color": colors["ax_color"], "fontSize": 10},
                             "splitLine": {"lineStyle": {"color": colors["grid_color"], "type": "dashed"}}}
            base["grid"] = {"top": "16%", "bottom": "10%", "left": "5%", "right": "6%", "containLabel": True}
            bar_pos = "top"
        base["legend"] = {"show": len(valid_y) > 1, "top": 0, "right": 0, "textStyle": {"color": colors["ax_color"], "fontSize": 10}}
        base["series"] = [
            {
                "name": metric, "type": "bar",
                "data": [_clean_number(row.get(metric)) for row in data],
                "barMaxWidth": 24,
                "itemStyle": {"color": palette[idx % len(palette)],
                              "borderRadius": [0, 3, 3, 0] if horizontal else [3, 3, 0, 0]},
                "label": {"show": True, "position": bar_pos, "color": colors["ax_color"], "fontSize": 9},
                "emphasis": {"focus": "series"},
            }
            for idx, metric in enumerate(valid_y)
        ]
        return json.dumps(base, ensure_ascii=False)

    # ──────── 散点 ────────
    if chart_type == "scatter":
        if len(y_fields) < 2:
            return json.dumps(base)
        scatter_data = [[_clean_number(row.get(y_fields[0])), _clean_number(row.get(y_fields[1]))]
                        for row in data
                        if _clean_number(row.get(y_fields[0])) is not None and _clean_number(row.get(y_fields[1])) is not None]
        if not scatter_data:
            return json.dumps(base)
        base.update({
            "grid": {"top": "16%", "bottom": "10%", "left": "8%", "right": "8%", "containLabel": True},
            "xAxis": {"type": "value", "name": y_fields[0],
                      "axisLine": {"lineStyle": {"color": colors["grid_color"]}},
                      "axisLabel": {"color": colors["ax_color"], "fontSize": 10},
                      "splitLine": {"lineStyle": {"color": colors["grid_color"], "type": "dashed"}}},
            "yAxis": {"type": "value", "name": y_fields[1],
                      "axisLine": {"lineStyle": {"color": colors["grid_color"]}},
                      "axisLabel": {"color": colors["ax_color"], "fontSize": 10},
                      "splitLine": {"lineStyle": {"color": colors["grid_color"], "type": "dashed"}}},
            "series": [{
                "type": "scatter", "data": scatter_data,
                "symbolSize": 12,
                "itemStyle": {"color": palette[0], "opacity": 0.7},
                "emphasis": {"focus": "self"},
            }],
        })
        return json.dumps(base, ensure_ascii=False)

    # 默认：fallback 到柱状
    return build_chart_option(
        chart_type="bar", title=title, data=data, x_field=x_field, y_field=y_fields,
        chart_palette=chart_palette, css_vars=css_vars,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Batch helper
# ═══════════════════════════════════════════════════════════════════════════════


def build_chart_options_batch(charts: list[dict]) -> list[ChartOption]:
    """批量生成图表 options（确定性，零 LLM 调用）。

    Args:
        charts: [{"chart_id": 1, "chart_type": "line", "title": "...", "data": [...],
                  "x_field": "...", "y_field": "...", "chart_palette": [...],
                  "css_vars": {...}}, ...]

    Returns:
        ChartOption 列表，每个对应一个 chart。
    """
    out: list[ChartOption] = []
    for c in charts:
        chart_id = c.get("chart_id", 0)
        try:
            option_json = build_chart_option(
                chart_type=c.get("chart_type", "bar"),
                title=c.get("title", ""),
                data=c.get("data", []),
                x_field=c.get("x_field", ""),
                y_field=c.get("y_field", ""),
                chart_palette=c.get("chart_palette"),
                css_vars=c.get("css_vars"),
            )
        except Exception as e:
            logger.warning(f"build_chart_options_batch failed for chart {chart_id}: {e}")
            option_json = json.dumps({"title": {"text": c.get("title", "")}})

        out.append(ChartOption(
            chart_id=chart_id,
            chart_type=c.get("chart_type", "bar"),
            title=c.get("title", ""),
            option_json=option_json,
        ))
    return out