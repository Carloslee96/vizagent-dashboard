"""评审节点结构化输出 schema。

供 review_node / test_node / release_node 使用 chat_structured,
替代旧的 _extract_json + 容错放行,消除解析失败时盲放行(pass=True)的误判。

注意:Python 关键字 `pass` 不能作字段名,故用 `passed`,由节点代码映射回 "pass" 键,
保持 state["review_json"]["pass"] / state["test_json"]["pass"] 接口不变(路由逻辑零改动)。

---

在开源 Skill 中,这些 Pydantic 模型作为可选的自我评估契约 —
Agent Skill 模式下宿主 AI 可以用它来自我评审生成的 DashboardSpec,
确保 spec 满足业务需求且 DashboardSpec 契约合法。
"""

from __future__ import annotations

from pydantic import BaseModel, Field


# ═══════════════════════════════════════════════════════════════════════════════
# Review Agent — 需求评审结果
# ═══════════════════════════════════════════════════════════════════════════════


class ReviewScores(BaseModel):
    domain_match: int = Field(description="领域一致性 0-10")
    clarity: int = Field(description="需求清晰度 0-10")
    quantifiability: int = Field(description="指标可量化性 0-10")
    chart_feasibility: int = Field(description="图表清单可行性 0-10")
    completeness: int = Field(description="完整性 0-10")


class ReviewResult(BaseModel):
    passed: bool = Field(description="评审是否通过")
    total_score: int = Field(description="总分 0-50")
    scores: ReviewScores
    reason: str = Field(description="总评说明")
    suggestions: list[str] = Field(description="改进建议列表")


# ═══════════════════════════════════════════════════════════════════════════════
# Test Agent — HTML 测试结果
# ═══════════════════════════════════════════════════════════════════════════════


class TestIssue(BaseModel):
    severity: str = Field(description="high / medium / low")
    dimension: str = Field(description="问题所在维度")
    description: str = Field(description="具体问题描述")
    pdr_citation: str = Field(
        default="inferred",
        description="证据等级:literal(原始需求字面要求)/inferred(LLM 推测)/system(程序化检测补)",
    )


class TestResult(BaseModel):
    passed: bool = Field(description="测试是否通过")
    score: int = Field(description="总分 0-100")
    scores_detail: dict[str, int] = Field(description="各维度得分")
    issues: list[TestIssue] = Field(description="问题列表")
    summary: str = Field(description="一句话总结")
    missing_charts: list[str] = Field(description="需求提到但 spec 中缺失的图表")
    attribution: str = Field(default="", description="一句话归因:哪个环节什么问题")
    root_cause: str = Field(
        default="",
        description="根因分类:truncation/missing_chart/js_error/layout/coverage/no_browser/passed",
    )
    fix_suggestion: str = Field(default="", description="修复建议:可执行的下一动作")


# ═══════════════════════════════════════════════════════════════════════════════
# Release Agent — 发布决策
# ═══════════════════════════════════════════════════════════════════════════════


class ReleaseDebt(BaseModel):
    item: str = Field(description="技术债务描述")
    severity: str = Field(description="high / medium / low")


class ReleaseDecision(BaseModel):
    approved: bool = Field(description="是否批准发布")
    confidence: float = Field(description="置信度 0.0-1.0")
    decision_reason: str = Field(description="通过/拒绝原因")
    debt: list[ReleaseDebt] = Field(description="技术债务列表")
    next_steps: list[str] = Field(description="后续改进建议")