"""Browser-based validation — Playwright checks (optional dependency)."""

from __future__ import annotations


def check_js_errors(html_path: str) -> list[str]:
    """Open HTML in headless browser and collect JS errors."""
    raise NotImplementedError("Will be extracted from SaaS in Step 2")


def check_chart_rendered(html_path: str) -> bool:
    """Verify at least one chart rendered non-empty."""
    raise NotImplementedError("Will be extracted from SaaS in Step 2")
