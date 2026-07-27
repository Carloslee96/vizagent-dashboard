# Release Notes — vizagent-dashboard v0.1.8

## 一句话

修首页主题展示标题：v0.1.7 README 主题章节仍写「5 个主题」，与「25 个主题」特性不符，改为「25 个主题任选」并补另外 20 个去品牌主题的出处。

## 安装

```bash
pip install --upgrade vizagent-dashboard==0.1.8
vizagent skill install --target all   # 注册 Claude Code / Cursor / Codex 的 Skill
```

## 为什么发 v0.1.8

v0.1.7 把特性 bullet 写成「25 个主题」，但下方「同一份数据，5 个主题」展示章节标题没同步——只展示了 5 个原创主题的截图，让人误以为总共只有 5 个主题。PyPI 首页以 README 为描述，新用户第一眼看到的就是这个矛盾。

## 修复

| # | 问题 | 修复 |
|---|---|---|
| 8 | README 主题展示章节标题写「5 个主题」，与「25 个主题」特性矛盾 | 标题改为「同一份数据，25 个主题任选」（中/英）；预览下方注明「展示 5 个原创主题预览，另 20 个去品牌主题见 `docs/THEME_AUDIT.md`，用 `--theme <id>` 切换」，并点名真实存在的 `coral-warm`/`grove-dark`/`phosphor-green` 三个示例 |

纯文档变更，无代码改动。修复后 PyPI 首页 README 主题章节与特性描述一致。
