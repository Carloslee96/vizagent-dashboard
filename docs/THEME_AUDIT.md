# 主题 clean-room 审计

> 审计日期：2026-07-27
>
> 范围：`src/vizagent_dashboard/assets/*.md` 的 5 个活动主题
>
> 结论：**通过** — 5 个主题均为原创通用 token，不含第三方品牌名、Logo 或专有文案。

## 1. 背景

SaaS 主项目原有 20 个品牌导向主题（文件名含 airbnb / apple / claude / coinbase /
figma / grafana / kraken / linear / notion / palantir / pitchbook / posthog /
sentry / spotify / stripe / supabase / vercel / …）。开源 skill 不得复刻这些
品牌资产，故全部弃用，改为 5 个 clean-room 通用主题。

旧 ID 仅作为输入别名映射到新主题（见 `compiler/themes.py:ALIASES`），不复制
旧主题任何内容。

## 2. 活动 主题清单

| ID | 文件 | 风格定位 |
|---|---|---|
| `midnight-ops` | `midnight-ops.md` | 深靛灰背景、蓝绿数据色，运营监控 |
| `paper-light` | `paper-light.md` | 暖白纸张、墨色文字，经营汇报 |
| `warm-editorial` | `warm-editorial.md` | 浅米色、暗红重点，内容/趋势故事 |
| `clinical-light` | `clinical-light.md` | 冷白、蓝青强调，健康/服务质量 |
| `signal-dark` | `signal-dark.md` | 炭黑、琥珀青信号，告警/基础设施 |

## 3. 审计方法

对每个主题文件全文检索以下关键词，均**无命中**：

- 品牌名：Apple, Airbnb, Coinbase, Figma, Grafana, Kraken, Linear, Notion,
  Palantir, PitchBook, PostHog, Sentry, Spotify, Stripe, Supabase, Vercel,
  Claude, Anthropic
- 模仿性描述词：标志性、独占、签名、官方、brand、logo、trademark
- 专有资产引用：任何外部 URL、字体文件引用、图片引用

每个主题结构统一为三段：`## Visual Theme`（一句话定位）、`## Color Palette`
（token 表）、`## Chart Color Palette`（5 色板）。token 值为原创配色，非从
任何品牌设计系统复制。

## 4. 别名映射（仅 ID 兼容，不复制内容）

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

## 5. 后续约束

- 新增主题必须沿用三段结构，禁止引入品牌名或专有资产。
- 任何主题改动须重跑本审计（关键词清单见 `tools/` 或手动按第 3 节执行）。
- 本审计结论须在每次发布前复核。
