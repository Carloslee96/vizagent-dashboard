# vizagent-dashboard

Build an offline HTML dashboard from the user's CSV/Excel data using the `vizagent` CLI. No database, server, or API key — the compiler is deterministic and reproducible.

## Prerequisite

`pip install vizagent-dashboard` if `vizagent` is not on PATH.

## Workflow

1. Confirm the data file path; ask the user if not given.
2. (optional but recommended) `vizagent inventory --data <file>` — inspect `data.inventory.json` for sheet names, columns, dtypes, row counts. **Never guess column names.**
3. Build the dashboard:
   - **Auto** (default): `vizagent build --data <file>` — auto-selects charts by field type (date → line, geography → map, ratio → pie, other categorical → bar).
   - **Tweak**: `vizagent build --data <file> --requirement "只展示饼图，浅色主题，分页展示"`.
   - **Spec mode**: `vizagent plan --data <file> --requirement "..." --output spec.json` → edit spec → `vizagent compile --data <file> --spec spec.json` → `vizagent validate --data <file> --spec spec.json --html output/output.html`.
4. Report the output path. `output/output.html` is self-contained (ECharts inlined); double-click to open. Add `--open` to auto-open.

## Themes

`midnight-ops` (default) · `paper-light` · `warm-editorial` · `clinical-light` · `signal-dark`

## Tips

- China map: use full province names ("广东省", not "广东").
- KPI cards go in the first row.
- Iterate until `validation.report.json` reports `is_valid: true` before presenting.
- `--requirement` keywords: `只要饼图/仅展示柱状` (force chart type), `浅色/纸张` (paper-light theme), `分页/多页签` (tabs layout), `地图` (prefer map).
