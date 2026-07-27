# 主题 clean-room 审计

> 审计日期：2026-07-27（初版），2026-07-27 更新（P1 去品牌引入 20 主题）
>
> 范围：`src/vizagent_dashboard/assets/*.md` 的 5 个原创主题 + 20 个去品牌引入主题
>
> 结论：**通过** — 25 个主题均不含第三方品牌名、Logo 或专有文案；20 个去品牌主题的颜色/圆角 token 与 SaaS 源逐字节保真，可复现验证（`python tools/import_saas_themes.py` → 20/20 PASS）。

## 1. 背景

SaaS 主项目原有 20 个品牌导向主题（文件名含 airbnb / apple / claude / coinbase /
figma / grafana / kraken / linear / notion / palantir / pitchbook / posthog /
sentry / spotify / stripe / supabase / vercel / …）。开源 skill 不得复刻这些
品牌资产。

初版策略（v0.1.0–v0.1.3）：**全部弃用**，改为 5 个 clean-room 原创主题，旧 ID 仅作
别名映射到新主题（见 `compiler/themes.py` 别名），不复制旧主题任何内容。

P1 策略（本次，2026-07-27）：将 20 个 SaaS 主题**去品牌引入**——只提取纯 token 值
（hex 色板、圆角、字体栈、装饰类型），赋纯描述性中性名，重写中性 Visual Theme prose，
**剔除全部品牌名、品牌专有色名、品牌签名指纹、品牌定位文案、Logo/外部资产引用**。
色值（hex）原样保留（色值本身是数字/事实，不可版权；配中性名+中性 prose 后可辩护）。

## 2. 活动主题清单

### 2.1 原创主题（5 个，v0.1.0 起）

| ID | 文件 | 风格定位 |
|---|---|---|
| `midnight-ops` | `midnight-ops.md` | 深靛灰背景、蓝绿数据色，运营监控 |
| `paper-light` | `paper-light.md` | 暖白纸张、墨色文字，经营汇报 |
| `warm-editorial` | `warm-editorial.md` | 浅米色、暗红重点，内容/趋势故事 |
| `clinical-light` | `clinical-light.md` | 冷白、蓝青强调，健康/服务质量 |
| `signal-dark` | `signal-dark.md` | 炭黑、琥珀青信号，告警/基础设施 |

### 2.2 去品牌引入主题（20 个，P1）

| SaaS 源文件 | clean-room ID | clean-room 名 | base | decoration |
|---|---|---|---|---|
| `airbnb.md` | `coral-warm` | Coral Warm | light | gradient |
| `apple.md` | `obsidian-glass` | Obsidian Glass | dark | glass |
| `claude.md` | `parchment-serif` | Parchment Serif | light | flat |
| `coinbase.md` | `trust-blue` | Trust Blue | dark | flat |
| `figma.md` | `canvas-dot` | Canvas Dot | dark | flat |
| `grafana-ops.md` | `ops-slate` | Ops Slate | dark | flat |
| `health-ring.md` | `ring-pastel` | Ring Pastel | light | flat |
| `kraken.md` | `nebula-glow` | Nebula Glow | dark | glow |
| `linear.md` | `graphite-iris` | Graphite Iris | dark | flat |
| `newsroom.md` | `broadsheet` | Broadsheet | light | flat |
| `notion.md` | `fiber-paper` | Fiber Paper | light | flat |
| `palantir.md` | `grid-azure` | Grid Azure | dark | flat |
| `pitchbook-dark.md` | `gilt-navy` | Gilt Navy | dark | flat |
| `posthog.md` | `ember-paper` | Ember Paper | light | flat |
| `sentry.md` | `amethyst-glass` | Amethyst Glass | dark | glass |
| `spotify.md` | `grove-dark` | Grove Dark | dark | flat |
| `stripe.md` | `haze-lilac` | Haze Lilac | light | gradient |
| `supabase.md` | `phosphor-green` | Phosphor Green | dark | flat |
| `terminal-amber.md` | `amber-scan` | Amber Scan | dark | flat |
| `vercel.md` | `mono-noir` | Mono Noir | dark | flat |

## 3. 去品牌变换规则（P1）

每个 SaaS 主题经以下变换成为 clean-room 主题：

1. **提取**：仅取 Color Palette 表与 Token Schema 表中的 12 个核心 token
   （`--bg-primary/card/elevated`、`--text-primary/secondary`、`--border-subtle`、
   `--accent-primary`、`--map-area/boundary`、`--radius-card`、`--font-family-base/display`）
   + `## Chart Color Palette` 色板。SaaS 源其余 token（`--bg-hover`、
   `--accent-secondary/success/warning/danger`、`--text-muted` 等）刻意不搬，
   保持与原创主题一致的瘦格式。
2. **颜色/圆角 token 逐字节保真**：hex 色值与 px 圆角与 SaaS 源同名 token 完全一致
   （校验器逐对比对，大小写不敏感）。
3. **字体 token 归一化去品牌**：`-apple-system` → `system-ui`（W3C 标准等价关键字，
   与原创主题一致），折叠连续重复。这是字体栈唯一的刻意改动。
4. **命名纯描述性**：起与品牌无关的视觉特征名（如 spotify→grove-dark、airbnb→coral-warm），
   不 echo 品牌名、不用近音/近形词。`aliases` 一律为空。
5. **prose 重写**：Visual Theme 改写为 1 句中性美学描述（颜色+明暗+圆角+装饰风格），
   剔除全部品牌名、品牌专有色名（Rausch/Babu/Arches/Crail/CircularSp/Cereal 等）、
   品牌签名指纹（「全库唯一」「标志性」「专利」）、品牌定位文案（「像家一样」「深夜听歌」）。
6. **丢弃整段**：SaaS 主题的 Chart Fingerprint / Token Schema 其余行 / Typography /
   Border Radius / Shadows / Motion / Component Specifications / Anti-Patterns /
   Do's and Don'ts / Layout & Grid 等章节一律不搬（lean 编译器不消费这些 prose）。

## 4. 审计方法

`tools/import_saas_themes.py` 自动执行两项校验：

- **token 保真**：每个 clean-room 主题的 12 个 token 与 SaaS 源同名 token 比对——
  颜色/圆角要求逐字节一致；字体 token 归一化后一致。
- **品牌残留扫描**：clean-room 全文检索品牌名 + 品牌专有色名 + 模仿性描述词
  （标志性/独占/签名/官方/brand/logo/trademark/专利），均须无命中。

对原创 5 主题同样全文检索上述关键词，均无命中。

## 5. 已知限制

- **glass / glow 装饰不渲染特效**：lean 编译器（`skeleton.py:build_css_block`）
  只把 css_vars 原样灌进 `:root`，**不按 `--decoration` 分支生成模糊/辉光 CSS**。
  故 `obsidian-glass` / `amethyst-glass`（glass）、`nebula-glow`（glow）、
  `coral-warm` / `haze-lilac`（gradient）在 skill 里仅按 token 颜色平铺渲染，
  不产生 backdrop-blur / box-shadow glow / 渐变装饰。`--decoration` frontmatter
  字段保留为元数据，供未来扩展或用户主题目录消费者参考。
- **`amethyst-glass` 的 `--bg-card` 为半透明** `rgba(31,22,51,0.65)`：源主题配
  backdrop-blur 实现毛玻璃；skill 不渲染模糊时该面板呈 65% 不透明叠在 body 上，
  视觉偏柔和但非破损。原样保留以忠于源 token。
- **`amber-console` 色板 4 色 / `mono-noir` 色板 6 色**：原样保留源色板数量，
  图表系列色按 `palette[i % len]` 轮换，不影响渲染。

## 6. 别名映射（仅 ID 兼容，不复制内容）

原创主题的旧 ID 别名（v0.1.0 起，供旧 spec 平滑迁移）：

```
monitor-dark          -> midnight-ops
dark-ops              -> midnight-ops
paper-brief           -> paper-light
paper-linen           -> paper-light
minimal-doc           -> paper-light
clean-slate           -> clinical-light
fitness-glass         -> clinical-light
command-post          -> signal-dark
amber-console         -> signal-dark
```

> 注：P1 新增的 terminal-amber 去品牌主题命名为 `amber-scan`（非 `amber-console`），
> 刻意避开与上述旧别名 `amber-console -> signal-dark` 的 id/别名同名碰撞。

## 7. 后续约束

- 新增主题必须沿用三段结构（frontmatter + Visual Theme + Color Palette + Chart Color Palette），禁止引入品牌名或专有资产。
- 任何主题改动须重跑 `python tools/import_saas_themes.py`（20/20 PASS）+ 原创主题关键词扫描。
- 本审计结论须在每次发布前复核。
- SaaS 源主题若有更新，重跑 import 脚本可定位 token 漂移；clean-room prose 改写需人工复核。
