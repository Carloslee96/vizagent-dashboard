"""图表 option 生成（数据驱动版）。

从 viz-agent-team/backend/agents/chart_options.py 提取（参考源码 commit 见 upstream-manifest.toml）。

去 SaaS 依赖策略：
- 保留：Pydantic schema、纯辅助函数（_guess_chart_type 等 agent 模式助手）
- 保留：确定性 build_chart_option（生成常见图表的 ECharts option JSON）
- 丢弃：所有 LangChain SystemMessage/HumanMessage + LLMClient.chat 调用

架构：``build_chart_option`` 由 ``compiler/charts/`` 注册表分发，
本模块作为向后兼容 facade 再导出，旧调用方（skeleton / 测试）无需改动。
新增图表类型见 ``compiler/charts/__init__.py``。

Skill 中使用方式：
  - Spec 模式：编译器从 DashboardSpec 直接生成 option_json（零 API 调用）
  - Agent Skill 模式：宿主 AI 读 dashboard_spec.py 后调用 build_chart_option 生成 option
"""

from __future__ import annotations

import json
import logging

from pydantic import BaseModel, Field

from vizagent_dashboard.compiler.charts import build_chart_option

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
            if line.strip().startswith("#") or line.strip().startswith("【"):  # noqa: SIM102
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
        except Exception as e:  # noqa: BLE001 - 批量生成单图失败不应中断整批
            logger.warning(f"build_chart_options_batch failed for chart {chart_id}: {e}")
            option_json = json.dumps({"title": {"text": c.get("title", "")}})

        out.append(ChartOption(
            chart_id=chart_id,
            chart_type=c.get("chart_type", "bar"),
            title=c.get("title", ""),
            option_json=option_json,
        ))
    return out