# Software Bill of Materials (SBOM) — vizagent-dashboard v0.1.0

> 生成日期：2026-07-27（手工维护，v0.2 起 CI 自动生成）

## 1. 本项目

| 字段 | 值 |
|---|---|
| 名称 | vizagent-dashboard |
| 版本 | 0.1.0 |
| 许可证 | Apache-2.0 |
| 主页 | https://github.com/vizagent/dashboard |

## 2. 随包分发资产（写入 wheel，进入产物 HTML）

| 资产 | 版本 | 许可证 | 来源 |
|---|---|---|---|
| Apache ECharts | 5.5.1 | Apache-2.0 | https://github.com/apache/echarts |
| china.json (GeoJSON) | — | **待复核** | 阿里云 DataV.GeoAtlas / Apache ECharts map data |
| world.json (GeoJSON) | — | **待复核** | 阿里云 DataV.GeoAtlas / Apache ECharts map data |

> 两份 GeoJSON 在历史提取中来源记录不一致。**公开发布前必须确认实际来源
> 与可再分发许可**，并据此更新本表与 NOTICE。在此完成前不得打 v0.1.0 标签。

## 3. 运行时依赖（声明于 pyproject.toml，安装时拉取，不分发）

| 包 | 约束 | 许可证 | 来源 |
|---|---|---|---|
| click | >=8.0.0 | BSD-3-Clause | https://palletsprojects.com/p/click/ |
| openpyxl | >=3.1.0 | MIT | https://openpyxl.readthedocs.io |
| pydantic | >=2.0.0 | MIT | https://github.com/pydantic/pydantic |

## 4. 可选依赖

| 包 | extra | 许可证 | 来源 |
|---|---|---|---|
| playwright | `[browser]` / `[all]` | Apache-2.0 | https://github.com/microsoft/playwright-python |

## 5. 开发依赖（不进入 wheel）

| 包 | 用途 | 许可证 |
|---|---|---|
| build | sdist/wheel 构建 | MIT |
| pytest | 测试 | MIT |
| ruff | lint | MIT |

## 6. 字体

不分发字体文件。主题 token 声明 system-ui / Georgia / Consolas 等系统字体族，
由用户系统提供。

## 7. 示例数据

`examples/` 下全部 CSV/XLSX/spec.json 为合成数据，零真实数据。
