# Contributing to VizAgent Dashboard

Thanks for your interest! This skill is developed in a separate `skill/`
directory and must stay **physically isolated** from the SaaS main project
(`app/`, `viz-agent-team/`). Do not modify SaaS code from this directory,
and do not pull SaaS code into the skill except through the one-time
extraction script (`tools/import_from_vizagent.py`) with an updated
`tools/upstream-manifest.toml`.

## Setup

```bash
cd skill/
pip install -e ".[dev]"
pip install -e ".[browser]"   # optional, for the Playwright gate
python -m playwright install chromium
```

## Development loop

```bash
# Unit + contract tests (fast)
PYTHONPATH=src python -m pytest tests/ -q

# Browser gate on a real build
PYTHONPATH=src python -m vizagent_dashboard.cli build \
  --data examples/ecommerce/data.csv --browser --output build/
```

## Before opening a PR

1. `ruff check src/ tests/` passes.
2. `python -m pytest tests/ -q` is green (unit + contract).
3. If you changed the compiler, themes, or validators, run the Mock Excel
   loop and confirm `validation.report.json` reports `is_valid: true` with
   complete coverage.
4. Do **not** commit generated artifacts (`build/`, `dist/`, `*.html`
   outputs) — they are gitignored.
5. Add a `skill/CHANGELOG.md` entry under `[Unreleased]`.

## Scope rules

- **Surgical changes.** Touch only what your change requires. Match existing
  style. Do not refactor adjacent code that is not broken.
- **SSOT.** A concept has one authoritative source. Themes live only in
  `assets/*.md`; do not hardcode theme colors in the compiler.
- **Deterministic compiler.** The compiler must never call an LLM or the
  network. AI reasoning belongs to the host agent (Agent Skill mode), not
  the compiler.
- **Clean-room only.** Do not reintroduce third-party brand names, logos, or
  proprietary assets into themes or examples.

## Releasing

Releases are gated by `docs/TEST_REPORT_2026-07-27.md` section 8. Do not tag
`v0.1.0` until every gate there is satisfied and the GeoJSON license audit is
signed off in `NOTICE`.
