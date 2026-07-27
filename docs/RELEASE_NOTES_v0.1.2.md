# Release Notes — vizagent-dashboard v0.1.2

## 一句话

修复 v0.1.1 的 Skill 安装缺陷：pip 装完即可在 Claude Code 里用 `/vizagent-dashboard` 触发，无需手动创建 SKILL.md。

## 安装

```bash
pip install vizagent-dashboard==0.1.2
```

## 作为 Claude Code Skill 使用（本版新增）

```bash
pip install vizagent-dashboard
vizagent skill install          # 装到 ~/.claude/skills/vizagent-dashboard/
# 重启 Claude Code → 输入 /vizagent-dashboard，或直接说「用 xx.xlsx 做个大屏」
```

clone 仓库并用 Claude Code 打开会自动注册为项目级 Skill（仓库根 `.claude/skills/`），无需手动安装。

## 相对 v0.1.1 的变化

- **`vizagent skill install` 子命令**：一行命令把 Skill 定义装到用户级目录。
- **canonical SKILL.md**：`user-invocable: true`，含工作流 + DashboardSpec 参考 + 排错表。
- **wheel 打包 SKILL.md**：hatch `force-include` 把 SKILL.md 映射进包内 `skill_assets/`，pip 装完即含。
- **README 安装说明**：中英两版补「作为 Claude Code Skill 使用」章节。
- 契约测试覆盖 skill 定位与安装；干净 venv 装 wheel 实测通过。

## 30 秒上手（CLI）

```bash
vizagent build --data sales.xlsx --output dashboard/
# → dashboard/output.html  直接浏览器打开
```

## 已知限制

- `--requirement` 规划器为确定性关键词匹配，复杂表结构可能产出空 Spec；复杂场景建议用 Agent Skill 模式或手写 `--spec`。
- 浏览器门禁需额外安装 Playwright 与 Chromium。

## 验证

```bash
git clone https://github.com/Carloslee96/vizagent-dashboard.git
cd vizagent-dashboard
pip install -e ".[dev]"
python -m pytest tests/ -q -k "not e2e and not real"
```

## 许可证

Apache License 2.0 © VizAgent Team。
