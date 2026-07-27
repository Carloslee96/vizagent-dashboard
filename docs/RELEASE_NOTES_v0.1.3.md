# Release Notes — vizagent-dashboard v0.1.3

## 一句话

Skill 安装扩展到 Cursor 和 Codex CLI；`vizagent skill install` 一条命令装齐多个 AI 工具，装完打印快速上手提示。

## 安装

```bash
pip install vizagent-dashboard==0.1.3
```

## 作为 AI 工具的 Skill 使用（本版增强）

```bash
pip install vizagent-dashboard
vizagent skill install --target all   # 一次装齐 Claude + Cursor + Codex
```

| 工具 | 触发方式 |
|---|---|
| Claude Code | `/vizagent-dashboard`，或「用 xx.xlsx 做个大屏」 |
| Cursor | 编辑 .csv/.xlsx 时自动注入规则 |
| Codex CLI | `/vizagent-dashboard` |

clone 仓库并用对应工具打开会自动加载项目级规则，无需手动安装。

## 相对 v0.1.2 的变化

- 新增 Cursor（`.cursor/rules/*.mdc`）和 Codex CLI（`.codex/prompts/*.md`）规则文件。
- `vizagent skill install` 支持 `--target claude|cursor|codex|all`。
- 安装成功后打印各工具触发方式 + 命令行直跑示例 + 文档链接（Windows GBK 控制台 UTF-8 兼容）。
- wheel 打包 3 套规则文件；契约测试覆盖多 target；干净 venv 实测通过。

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
