# Release Notes — vizagent-dashboard v0.1.6

## 一句话

修复 `vizagent --version` 永远报 0.1.0 的版本号双源头问题，改为从包元数据读取（SSOT）。

## 安装

```bash
pip install --upgrade vizagent-dashboard==0.1.6
```

## 为什么发 v0.1.6

v0.1.5 验证时发现 `vizagent --version` 始终报 `0.1.0`，但 `pip show` 显示正确版本。根因：`__init__.py` 里有硬编码的 `__version__ = "0.1.0"`，从 v0.1.0 起就没同步过，与 `pyproject.toml` 的版本号形成双源头，违反单一事实来源原则。

## 修复

| # | 问题 | 修复 |
|---|---|---|
| 6 | `vizagent --version` 永远报 0.1.0（`__init__.__version__` 硬编码，从未同步 pyproject） | 改用 `importlib.metadata.version("vizagent-dashboard")` 读包元数据，版本号 SSOT 在 pyproject.toml；源码未安装时兜底 `0.0.0` |

修复后 `vizagent --version` 与 `pip show vizagent-dashboard` 始终一致，以后 bump pyproject 版本即自动同步到 CLI。

## 测试

141 passed（新增 `test_version_matches_package_metadata` 防退化）；ruff src/ tests/ 全清。
