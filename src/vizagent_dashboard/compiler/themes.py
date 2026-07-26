"""Theme loading and token parsing."""

from __future__ import annotations


def load_theme(theme_id: str) -> dict:
    """Load theme tokens from assets/<theme_id>.md."""
    raise NotImplementedError("Will be extracted from SaaS in Step 2")


def parse_design_tokens(markdown_content: str) -> dict:
    """Parse design token tables from markdown."""
    raise NotImplementedError("Will be extracted from SaaS in Step 2")
