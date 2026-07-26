"""KPI 数值格式化和数据驱动提取。

从 viz-agent-team/backend/agents/kpi_options.py 提取。

保留部分（去 SaaS LangChain/LLMClient 依赖）：
- extract_kpi_values_from_data：从全量 Excel 数据按列聚合提取 KPI 真实数值
- _format_value：根据指标名称和值类型，自动推断显示格式（千分位/百分比/货币）
- KpiValue / KpiValueBundle：Pydantic schema

丢弃部分（依赖 SaaS 状态机/LLM）：
- generate_kpi_values（依赖 LLMClient + LangChain SystemMessage/HumanMessage）
- _generate_text（LLM 调用）
- _build_user_prompt（注入 LLM prompt）

在 Skill 中，KPI 数值由 AI 在 DashboardSpec 中声明（可选）或由编译器从数据中提取。
"""

from __future__ import annotations

import logging
import re
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════════════════
# Pydantic Schemas
# ═══════════════════════════════════════════════════════════════════════════════


class KpiValue(BaseModel):
    slot_id: int = Field(description="KPI 槽位序号,必须与输入的 slot_id 一致")
    label: str = Field(description="KPI 指标名称(与输入一致)")
    value: str = Field(description="KPI 显示文本,带正确格式,如 ¥1,284,560 / 98.7% / 12,450")


class KpiValueBundle(BaseModel):
    kpi_values: list[KpiValue] = Field(description="本批 KPI 数值列表")


# ═══════════════════════════════════════════════════════════════════════════════
# 数据驱动提取（无 LLM）
# ═══════════════════════════════════════════════════════════════════════════════


def extract_kpi_values_from_data(
    excel_data: list[dict],
    kpi_slots: list[Any],  # 接受任意带 .id 和 .name 的对象
) -> dict[int, str]:
    """从全量 Excel 数据按列聚合提取 KPI 真实数值。

    策略（按优先级）:
    1. 【列名精确匹配】KPI 名 → 清洗后匹配列名 → 取该列末行非空值
    2. 【列名子串匹配】去"总"前缀后在列名中搜索子串
    3. 【行值匹配】在已知"指标/名称/项目"列中查找 KPI 名对应的"数值/值"列

    Returns:
        {slot_id: 格式化显示文本}  未匹配到的项不包含在返回值中。
    """
    if not excel_data or not kpi_slots:
        return {}

    # 收集全部列名（合并数据集的并集）
    all_col_names: list[str] = []
    for row in excel_data:
        for k in row:
            if k not in all_col_names:
                all_col_names.append(k)

    # 清洗后的列名 → 原始列名映射
    clean_col_map: dict[str, str] = {}
    for key in all_col_names:
        ck = key.strip().lower().replace("(", "").replace(")", "").replace("-", "").replace("_", "")
        if ck and ck != "sheet":
            clean_col_map[ck] = key

    # 识别"标签列"和"数值列"
    label_cols = [k for k in all_col_names if any(kw in k.lower() for kw in ["指标", "名称", "项目", "类型", "类别", "app", "车型", "套餐", "性别", "年龄段", "站点"])]
    value_cols = [k for k in all_col_names if any(kw in k.lower() for kw in ["数值", "值", "数量", "数据", "连接数", "激活数", "消耗", "占比", "环比", "热度", "企业数"])]

    def _collect_column_values(col_name: str) -> list[float]:
        """从该列提取所有非空数值。"""
        vals: list[float] = []
        for row in excel_data:
            raw = row.get(col_name)
            if raw is None or raw == '' or raw == 0:
                continue
            try:
                cleaned = str(raw).replace(",", "").replace("¥", "").replace("$", "").replace("￥", "").replace("%", "").strip()
                if cleaned:
                    num = float(cleaned)
                    vals.append(num)
            except (ValueError, TypeError):
                pass
        return vals

    def _aggregate_values(vals: list[float], slot_name: str) -> float:
        """根据语义选择聚合方式（总→末行 / 率→平均 / 其余→末行）。"""
        if not vals:
            return 0.0
        name_lower = slot_name.lower()
        if any(kw in name_lower for kw in ["率", "占比", "percent", "%"]):
            return sum(vals) / len(vals)
        # "总XXX" → 取末行（累计值通常是最新的最大）
        return vals[-1]

    def _find_by_column_match(slot_name: str) -> str | None:
        """策略 1+2：通过列名匹配（带优先级打分）。"""
        clean_slot = slot_name.strip().lower().replace("(", "").replace(")", "").replace("-", "").replace("_", "")
        # 策略 1：精确匹配
        if clean_slot in clean_col_map:
            return clean_col_map[clean_slot]

        # 策略 2a：去掉"总"前缀再精确匹配
        if clean_slot.startswith("总") and len(clean_slot) > 1:
            no_zong = clean_slot[1:]
            if no_zong in clean_col_map:
                return clean_col_map[no_zong]

        # 策略 2b：子串匹配 — 按匹配质量打分，选最优
        kw = clean_slot.replace("总", "")
        if len(kw) <= 1:
            return None

        best_score = 0
        best_key = None
        for ck, orig_key in clean_col_map.items():
            if ck == "sheet":
                continue
            if kw in ck or ck in kw:
                score = 0
                if ck == kw:
                    score = 100
                elif ck.replace("万", "").replace("tb", "").replace("家", "").strip() == kw:
                    score = 80
                elif kw in ck:
                    score = 50 + (len(kw) / max(len(ck), 1)) * 30
                if score > best_score:
                    best_score = score
                    best_key = orig_key
        return best_key

    def _find_by_row_value(slot_name: str) -> float | None:
        """策略 3：在标签列中找 KPI 名 → 返回该行具体的数值单元格(非整列聚合)。

        用于"指标/数值"长表(如核心指标 sheet:每行一个不同KPI)。
        """
        if not label_cols or not value_cols:
            return None
        slot_lower = slot_name.strip().lower()
        for label_col in label_cols:
            for row in excel_data:
                cell_val = str(row.get(label_col, "")).strip().lower()
                if cell_val and (cell_val == slot_lower or (len(slot_lower) > 2 and slot_lower in cell_val)):
                    for vc in value_cols:
                        raw = row.get(vc)
                        if raw is None or raw == '' or raw == 0:
                            continue
                        try:
                            return float(str(raw).replace(",", "").replace("¥", "").replace("$", "").replace("￥", "").replace("%", "").strip())
                        except (ValueError, TypeError):
                            pass
        return None

    def _format_value(val: object, name: str, unit: str = "") -> str:
        """根据指标名称和值类型，自动推断显示格式。"""
        if val is None:
            return ""
        try:
            num = float(val)
        except (ValueError, TypeError):
            return str(val)

        name_lower = name.lower()
        # 百分比
        if any(kw in name_lower for kw in ["率", "占比", "百分比", "比例", "percent", "%"]) or unit == "%":
            return f"{num:.1f}%"
        # 货币
        if any(kw in name_lower for kw in ["收入", "金额", "销售额", "营收", "利润", "成本", "¥", "$", "元"]):
            if abs(num) >= 10000:
                return f"¥{num:,.0f}"
            return f"¥{num:,.2f}"
        # 整数计数
        if any(kw in name_lower for kw in ["数量", "次数", "人数", "订单", "访问", "客户", "用户", "count", "连接数", "连接数(万)"]):
            if "万" in name_lower or "(万" in name_lower:
                return f"{num:,.2f} 万"
            if abs(num) >= 100000000:
                return f"{num / 100000000:.2f} 亿"
            if abs(num) >= 10000:
                return f"{num:,.0f}"
            return f"{int(num):,}"
        # 带单位后缀
        if any(kw in name_lower for kw in ["消耗", "tb", "流量"]):
            return f"{num:,.0f} TB"
        # 默认：千分位
        if num == int(num):
            return f"{int(num):,}"
        return f"{num:,.2f}"

    # 主逻辑：遍历每个 KPI 槽位
    result: dict[int, str] = {}
    for slot in kpi_slots:
        slot_name = slot.name.strip()
        if not slot_name:
            continue

        # 策略 1+2：列名匹配
        matched_col = _find_by_column_match(slot_name)
        if matched_col:
            vals = _collect_column_values(matched_col)
            if vals:
                agg_val = _aggregate_values(vals, slot_name)
                result[slot.id] = _format_value(agg_val, slot_name)
                continue
            # 列存在但无有效数值 → 用该列末行原始值
            for row in reversed(excel_data):
                raw = row.get(matched_col)
                if raw is not None and raw != '' and raw != 0:
                    result[slot.id] = _format_value(raw, slot_name)
                    break
            continue

        # 策略 3：行值匹配
        row_val = _find_by_row_value(slot_name)
        if row_val is not None:
            result[slot.id] = _format_value(row_val, slot_name)

    matched_ids = set(result.keys())
    all_ids = {s.id for s in kpi_slots}
    logger.info("extract_kpi_values_from_data: matched %d/%d KPI slots", len(matched_ids), len(all_ids))
    if matched_ids != all_ids:
        logger.info("  unmatched slots: %s", [s.name for s in kpi_slots if s.id not in matched_ids])

    return result