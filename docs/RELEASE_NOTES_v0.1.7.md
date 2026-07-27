# Release Notes — vizagent-dashboard v0.1.7

## 一句话

修复新用户预期断裂：`pip install` 后 `/vizagent-dashboard` 在 Claude Code 找不到——安装指引补上 `vizagent skill install --target all` 第二步。

## 安装

```bash
pip install --upgrade vizagent-dashboard==0.1.7
vizagent skill install --target all   # 注册 Claude Code / Cursor / Codex 的 Skill
```

## 为什么发 v0.1.7

v0.1.6 把 Skill 规则文件打包进 wheel（`skill_assets/`），但 pip 不会自动把它们写到用户级目录。新用户按文档 `pip install` 后，直接在 Claude Code 里敲 `/vizagent-dashboard` 会「找不到命令」——必须额外执行 `vizagent skill install` 才行。这一步之前埋在文档下方，新用户容易漏看，导致预期断裂。

## 修复

| # | 问题 | 修复 |
|---|---|---|
| 7 | `pip install` 后 `/vizagent-dashboard` 在 Claude Code 找不到（Skill 未注册） | README（中/英）「1. 安装」段从一步改两步——`pip install` + `vizagent skill install --target all`，并注明两步分别装 CLI 与注册 Skill 规则文件、装完需重启工具；统一以 `--target all`（一次装齐 Claude + Cursor + Codex）为推荐命令 |

纯文档变更，无代码改动。修复后 PyPI 首页 README 与 `pip show` 显示的描述同步为两步安装。

## 说明

- `vizagent skill install --target all` 把规则文件写到 `~/.claude/skills/`、`~/.cursor/rules/`、`~/.codex/prompts/`，三个工具一次装齐。
- 装完需**重启对应工具**（Claude Code 在会话启动时扫描 Skill 目录）。
- 只想用命令行不接 AI 工具，可跳过第二步，直接 `vizagent build --data 你的数据.xlsx --open`。
