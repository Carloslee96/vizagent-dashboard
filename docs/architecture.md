# Architecture Overview

## 双模式单编译内核

```
┌──────────────┐    ┌────────────┐    ┌──────────────┐
│  CSV / XLSX  │───▶│  Inventory │───▶│   Compiler   │───▶ output.html
│  (your data) │    │  (analyze) │    │  (generate)  │
└──────────────┘    └────────────┘    └──────────────┘
                          │                  │
                          ▼                  ▼
                   ┌──────────────┐   ┌──────────────┐
                   │ DashboardSpec│   │  Validator   │
                   │  (SSOT)      │   │  (quality)   │
                   └──────────────┘   └──────────────┘
```

### Core interfaces

- `inventory(source, policy)` → `DataInventory`
- `plan(requirement, inventory, planner)` → `DashboardSpec`
- `compile_dashboard(spec, inventory, theme)` → `BuildManifest`
- `validate_dashboard(html, spec, inventory)` → `ValidationReport`

See SKILL_DESIGN.md for full architecture document.
