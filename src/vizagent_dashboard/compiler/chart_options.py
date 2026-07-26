"""Chart option generation — produce ECharts option dicts from spec."""

from __future__ import annotations


def build_chart_option(chart_spec: dict, data: list[dict], theme_tokens: dict) -> dict:
    """Build ECharts option dict for a single chart."""
    raise NotImplementedError("Will be extracted from SaaS in Step 2")
