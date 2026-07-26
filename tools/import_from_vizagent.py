#!/usr/bin/env python3
"""
One-time extraction script: copy SaaS core modules into skill/src/vizagent_dashboard/.

Usage:
    python tools/import_from_vizagent.py

This script:
1. Reads upstream-manifest.toml to know which SaaS files to copy
2. Reads source files from viz-agent-team/backend/agents/
3. Strips LangGraph / FastAPI / DB dependencies
4. Rewrites imports to function-oriented interfaces
5. Writes to skill/src/vizagent_dashboard/
6. Records the source commit hash for auditability

Run from the skill/ directory.
"""

import re
import shutil
import subprocess
import tomllib
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
SAAS_DIR = SKILL_DIR.parent / "viz-agent-team" / "backend" / "agents"
TARGET = SKILL_DIR / "src" / "vizagent_dashboard"

MANIFEST = SKILL_DIR / "tools" / "upstream-manifest.toml"


def get_current_commit() -> str:
    """Get the current git HEAD hash."""
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True, text=True, cwd=SKILL_DIR.parent,
    )
    return result.stdout.strip()


def strip_llm_deps(source: str) -> str:
    """Remove LangGraph, LLMClient, FastAPI, DB dependencies from source."""
    # Remove imports from forbidden modules
    lines = source.splitlines()
    cleaned = []
    for line in lines:
        if re.match(r"^\s*(from|import)\s+(langchain|langgraph|fastapi|sqlalchemy|asyncpg)", line):
            continue
        if "LLMClient" in line and "import" in line:
            continue
        if "from agents." in line:
            line = re.sub(r"from agents\.", "from vizagent_dashboard.", line)
        if "from services." in line:
            line = re.sub(r"from services\.", "", line)
        if re.search(r"FlowState|GraphState|StateGraph", line) and "import" in line:
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def extract() -> int:
    """Run the extraction. Returns number of files copied."""
    with open(MANIFEST, "rb") as f:
        manifest = tomllib.load(f)

    current_commit = get_current_commit()
    extracted = 0

    for entry in manifest["extract"]:
        source_rel = entry["path"]
        target_rel = entry["target"]
        source_file = SAAS_DIR / source_rel
        target_file = TARGET / target_rel

        if not source_file.exists():
            print(f"  ⚠ SKIP: {source_rel} (not found)")
            continue

        source_text = source_file.read_text(encoding="utf-8")
        cleaned = strip_llm_deps(source_text)

        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(cleaned, encoding="utf-8")

        entry["extracted_at"] = current_commit
        print(f"  ✓ {source_rel} → {target_rel}")
        extracted += 1

    # Update manifest with extraction hash
    with open(MANIFEST, "w") as f:
        # Re-serialize TOML (basic)
        f.write("# Upstream manifest — source commit + hash for audit\n")
        f.write(f'extracted_at = "{current_commit}"\n\n')
        f.write("[[extract]]\n" + "\n[[extract]]\n".join(
            "\n".join(f'{k} = "{v}"' for k, v in e.items())
            for e in manifest["extract"]
        ))

    print(f"\n✅ Extracted {extracted}/{len(manifest['extract'])} files")
    print(f"   Source commit: {current_commit}")
    return extracted


if __name__ == "__main__":
    extract()
