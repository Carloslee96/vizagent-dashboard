"""Static validation — check for truncation, overlap, zero-size charts."""

from __future__ import annotations


def check_truncation(html_content: str) -> list[str]:
    """Check for truncated labels or text in the dashboard."""
    raise NotImplementedError("Will be extracted from SaaS in Step 2")


def check_overlaps(chart_options: list[dict]) -> list[str]:
    """Check for overlapping chart elements."""
    raise NotImplementedError("Will be extracted from SaaS in Step 2")


def check_zero_size(chart_options: list[dict]) -> list[str]:
    """Check for zero-size charts."""
    raise NotImplementedError("Will be extracted from SaaS in Step 2")
