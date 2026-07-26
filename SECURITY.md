# Security Policy

## Supported versions

v0.1.x (pre-release). Security fixes target the latest `main`.

## Reporting a vulnerability

Please **do not** open a public GitHub issue for security problems.

Email: security@vizagent.local (replace with a monitored address before public release)
Include: description, reproduction steps, affected version, and impact.

We aim to acknowledge within 72 hours and publish a fix advisory after a
coordinated disclosure window.

## Threat model

VizAgent Dashboard turns user-supplied CSV/XLSX data into a single offline
HTML file. The compiler is deterministic and makes **no network calls and no
LLM calls**. The relevant attack surface is:

1. **Malicious spreadsheet input** — a crafted XLSX/CSV that attempts to
   break out of the data layer.
2. **Generated HTML** — the output is opened in a browser; XSS or script
   injection in the output must be prevented.
3. **Path traversal** — output paths must not escape the intended directory.

## Implemented controls (v0.1)

| Layer | Control |
|-------|---------|
| HTML injection | All dynamic strings (titles, values, sheet names, table cells) are HTML-escaped via `html.escape`. |
| Script injection | JSON payloads embedded in `<script type="application/json">` and `</`-escaped to prevent breakout. |
| Content Security Policy | Every generated HTML ships a CSP: `default-src 'none'; script-src 'unsafe-inline' 'unsafe-eval'; ...`. No external script sources in `embedded` mode. |
| Offline guarantee | `embedded` mode (default) inlines ECharts + GeoJSON. The static validator **rejects** any `<script src="https://...">`. |
| Path traversal | Output directory is resolved and created with `parents=True`; artifacts are written via `os.replace` from a sibling temp dir. |
| Input size | Inventory reports sheet/row/column counts. (Hard size limits are planned for v0.2.) |
| Map binding | The validator rejects `map_china`/`map_world` charts whose ECharts option does not bind the corresponding map. |

## Not yet implemented (planned for v0.2)

- Hard input size / sheet count / row count limits (ZIP-bomb defense)
- Prompt-injection hardening for Agent Skill mode
- Dependency allowlist / pinning
- SBOM generation in CI (manual SBOM.md for v0.1)
