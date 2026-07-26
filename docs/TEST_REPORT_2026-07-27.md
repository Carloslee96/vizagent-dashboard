# VizAgent Dashboard Skill 独立测试报告

> 测试日期：2026-07-27
>
> 被测版本：`15b0bbb`
>
> 环境：Windows 11、Python 3.12、Chromium 端到端渲染
>
> 结论：**NO-GO，不具备 GitHub / PyPI / Agent Skill 公开发布条件**

## 1. 执行摘要

当前版本已经具备一个可继续开发的确定性编译原型：

- 源码模式下 77 个单元测试全部通过；
- CSV 与多 Sheet XLSX 可以读取；
- 电商示例通过 `DashboardSpec` 能生成 3 个 KPI 和 4 张真实图表；
- 在线环境下 Chromium 无 JavaScript 错误。

但“源码示例能运行”不等于“Skill 可用”。独立验收发现 8 个发布阻断：

1. wheel 安装成功后无法导入 Python 包；
2. `SKILL.md` 未通过官方结构校验；
3. 自然语言需求没有进入 Planner，互相矛盾的需求生成完全相同的 HTML；
4. 10 Sheet / 103 行基准数据只生成 1 个 KPI、2 张图、0 张地图；
5. 中国与世界地图只生成空容器，没有地图、GeoJSON 或 Tab；
6. 空地图和严重数据缺失仍被静态与浏览器验证器判定为健康；
7. 所谓“单文件、离线”产物依赖三个 ECharts CDN，断网后 0 张图；
8. 开源 provenance 为空，主题仅改名但仍大量保留第三方品牌与高度特征化描述。

因此，当前版本适合作为内部 Alpha 原型，不应以 `v0.1.0` 对外发布。

## 2. 测试矩阵

| 测试项 | 结果 | 证据 |
|---|---|---|
| 源码单元测试 | PASS | `77 passed in 0.12s` |
| wheel 构建 | PASS | 生成 `vizagent_dashboard-0.1.0-py3-none-any.whl` |
| wheel 干净安装与导入 | FAIL | pip 显示安装成功，`import vizagent_dashboard` 报 `ModuleNotFoundError` |
| Skill 结构校验 | FAIL | `Unexpected key(s): author, version` |
| 源码 CLI 帮助 | PASS | 仅有 `build` 命令 |
| 电商 Spec 生成 | PARTIAL PASS | 3 KPI + 4 图，在线 Chromium 0 JS error |
| 自然语言需求敏感性 | FAIL | 两条相反需求的 HTML SHA-256 完全一致 |
| 固定 Mock Excel 全量覆盖 | FAIL | 10 Sheet / 103 行 → 1 KPI + 2 图 + 0 地图 |
| 中国/世界地图契约 | FAIL | `registerMap=false`、`Tab=false`，两个面板为空 |
| 静态验证可信度 | FAIL | 空地图仍返回 `is_valid=true`、`score=100` |
| 浏览器验证可信度 | FAIL | 仅检查 Canvas 非零尺寸，空地图仍返回 `is_healthy=true` |
| 离线单文件 | FAIL | 断网后 `echarts is not defined`，Canvas 数为 0 |
| Spec 主题优先级 | FAIL | `spec.theme=warm-editorial` 被 CLI 默认 `midnight-ops` 覆盖 |
| 布局契约 | FAIL | `LayoutRow.columns`、`width`、`height` 被扁平化忽略 |
| 开源权利与 provenance | FAIL | 来源 commit 和 `extracted_at` 为空，品牌内容未清理 |

## 3. 基准项目复测

输入：

```text
D:\AIIIIIIIIIIIIII\vizagent\用户测试材料\Mock数据（丰富版）.xlsx
```

数据盘点：

| Sheet | 有效行 |
|---|---:|
| 核心指标 | 3 |
| 地域排名 | 15 |
| 月度增长 | 12 |
| 月度流量 | 12 |
| 用户性别 | 2 |
| 用户年龄 | 7 |
| 服务车企生态 | 5 |
| 用户上网行为偏好 | 16 |
| 流量套餐偏好分析 | 19 |
| 海外签约连接分布 | 12 |
| 合计 | 103 |

执行需求：

```text
完整分析全部工作表，所有有效数据均可视化，中国与世界地图使用 Tab 切换
```

实际输出：

- 标题固定为“数据分析大屏”；
- 1 个“总数值”KPI；
- 1 张折线图和 1 张柱状图；
- 两张图都只使用“核心指标”Sheet 的 3 行数据；
- 折线图把“全球有效连接数、海外签约连接、平台 API 调用次数”三个不同量纲指标错误连接为趋势；
- 其余 9 个 Sheet 未被可视化；
- 中国地图、世界地图和地图 Tab 均不存在；
- 页面下半屏大面积空白；
- CLI 与验证器仍报告成功。

此结果不满足 VizAgent 既有硬性验收标准，也不满足 README 对自然语言生成和多 Sheet Excel 的描述。

## 4. 发布阻断问题

### P0-1：发布包装入错误路径

wheel 内的包路径是：

```text
src/vizagent_dashboard/...
```

而 Python 运行时需要：

```text
vizagent_dashboard/...
```

因此 entry point 指向的 `vizagent_dashboard.cli:main` 不可导入。

根因是 `pyproject.toml` 只配置了：

```toml
[tool.hatch.build]
include = ["src/vizagent_dashboard/**"]
```

但没有配置 wheel 的 `packages = ["src/vizagent_dashboard"]` 映射。

### P0-2：Skill 本身未通过校验

`SKILL.md` frontmatter 包含 `author`、`version`，官方校验器拒绝加载。当前目录还存在以下问题：

- Skill 名称是 `vizagent-dashboard`，但安装目录是泛化的 `skill/`；
- 没有 `agents/openai.yaml`；
- 没有可被 Agent 调用的薄 `scripts/`；
- 没有渐进式 `references/`；
- GitHub README、CHANGELOG、LICENSE 与 Skill 本体混在同一加载边界；
- 正文重复“When to use”，触发条件没有完整收口到 description。

### P0-3：自然语言能力属于错误宣传

README 和 `SKILL.md` 声称：

- `--requirement` 会进入 Planner；
- `--planner` 可选择模型；
- `vizagent config --set api_key=...` 可配置密钥。

实际 CLI：

- 只有 `build` 命令；
- 没有 `config`；
- 没有 `--planner`；
- 没有 Provider Adapter；
- `--requirement` 只判断字符串是否为空，然后把标题固定为“数据分析大屏”；
- 其余需求内容完全不参与 Spec 或图表规划。

使用同一份数据执行：

```text
只展示销售趋势折线图，使用浅色主题
```

以及：

```text
只展示品类饼图，使用深色主题
```

两份 `output.html` 的 SHA-256 完全一致：

```text
6BCE0878DA742F953498FB56E0862844B6A806FAB5EA8D1BDD98EB158CE7D54F
```

### P0-4：多 Sheet 数据覆盖失效

CLI 把所有 Sheet 行合并成一个稀疏列表，再根据第一行字段自动推断图表。

第一行来自“核心指标”，因此后续 9 个 Sheet 的字段与该推断不匹配，聚合时全部被静默丢弃。系统没有生成 `DataInventory`，也没有数据覆盖报告或未覆盖清单。

### P0-5：地图是空实现

Schema 声明了 `map_china` 和 `map_world`，但编译器遇到地图时只追加：

```json
{
  "title": {"text": "..."},
  "backgroundColor": "transparent"
}
```

没有：

- `series.type = "map"`；
- GeoJSON；
- `echarts.registerMap()`；
- 地域名称标准化；
- 中国/世界 Tab；
- 地图数据绑定。

实机截图显示两个完全空白的地图面板。

### P0-6：质量门禁产生假阳性

静态验证目前主要检查 HTML 是否以 `</html>` 结尾。地图 option 虽然没有 series，但不符合其“空对象”正则，因此获得：

```json
{
  "is_valid": true,
  "score": 100,
  "issues": []
}
```

浏览器验证只判断 Canvas 是否存在且尺寸大于零。ECharts 可以为无数据 option 创建 Canvas，因此两个空地图也获得：

```json
{
  "charts_rendered": 2,
  "is_healthy": true
}
```

验证器没有比较 Spec、Inventory 和浏览器中的真实 series/data，也没有检查数据覆盖、空图、布局或地图注册状态。

### P0-7：产物不是真正的单文件离线 HTML

CLI 强制使用 CDN 模式，依次加载：

- `registry.npmmirror.com`；
- `cdn.bootcdn.net`；
- `cdn.jsdelivr.net`。

离线 Chromium 结果：

```json
{
  "errors": [
    "Failed to load resource: net::ERR_INTERNET_DISCONNECTED",
    "echarts is not defined"
  ],
  "canvases": 0
}
```

代码中的 local 模式只引用 `assets/echarts.min.js`，但该文件没有进入包，CLI 也没有暴露 local 模式。

### P0-8：开源权利门禁未执行

`upstream-manifest.toml` 的 `commit` 与 `extracted_at` 均为空。

主题虽然修改了文件名，但正文仍明确出现 Apple、Airbnb、Coinbase、Figma、Grafana、Linear、Palantir、PostHog、Sentry、Spotify、Stripe、Supabase、Vercel 等品牌，并保留“标志性”“独占”“签名”等高度模仿性描述。

仓库已经放入 Apache-2.0 LICENSE，但缺少：

- 权属结论；
- NOTICE；
- 第三方许可证清单；
- 地图与字体许可；
- SBOM；
- SECURITY.md；
- 合成示例数据声明。

“重命名”不能替代版权、商标和来源审计。

## 5. P1 功能与文档问题

### P1-1：Spec 主题被 CLI 默认参数覆盖

`spec-trend.json` 声明 `warm-editorial`，不传 `--theme` 时结果仍为 `midnight-ops`。CLI 应区分“用户显式主题”与“未传主题”，后者从 Spec 派生。

### P1-2：布局 Schema 没有进入编译器

编译器把所有 `LayoutRow.items` 扁平化，丢弃：

- `LayoutRow.columns`；
- `ChartItem.width`；
- `ChartItem.height`；
- 行顺序对应的视觉层级。

电商 Spec 声明三行布局，实际 1920px 下四张图全部排成一行，且页面下半屏为空。

### P1-3：输出契约不完整

当前只输出 `output.html`，没有方案要求的：

- `dashboard.spec.json`；
- `data.inventory.json`；
- `validation.report.json`；
- `build-manifest.json`。

### P1-4：测试数量不能代表发布质量

77 个测试全部位于 `tests/unit/`。以下目录只有 `__init__.py` 或没有用例：

- `tests/contract/`；
- `tests/browser/`；
- `tests/fixtures/`。

没有覆盖 wheel 安装、CLI、CSV/XLSX Inventory、自然语言差异、地图、离线运行、数据覆盖、跨平台和恶意输入。

### P1-5：开发文档不可复现

README 建议：

```bash
pip install -e ".[dev]"
```

但 `pyproject.toml` 没有定义 `dev` extra。README 中展示的 XML Skill 片段也不是当前 Codex Skill 的实际目录契约。

## 6. 可保留的成果

以下部分可以继续作为重构基础：

- Pydantic `DashboardSpec` 雏形；
- CSV/XLSX 基础读取；
- KPI、折线、柱状、饼图和散点图的真实数据 option；
- 主题 token 解析机制；
- HTML 转义与 `</script>` 基础防护；
- 77 个纯函数单元测试；
- 无 LLM 的确定性编译方向。

不建议推倒重写，但必须按边界重接全链路。

## 7. 修复顺序

### 第一阶段：使项目可安装、可验证

1. 修复 wheel 包路径并增加干净环境安装测试；
2. 将 GitHub 仓库根与 `skills/build-data-dashboard/` 分离；
3. 修正 frontmatter，生成 `agents/openai.yaml`；
4. 删除未实现的 Planner、config、离线等宣传，或完成对应实现；
5. 增加 CLI、contract 和 browser 测试。

### 第二阶段：打通真实数据闭环

1. 实现并落盘 `DataInventory`；
2. 宿主 Agent 根据 Inventory 和 Schema 生成 Spec；
3. 多 Sheet 分别绑定数据，不再稀疏合并；
4. 编译器严格执行主题和布局 Spec；
5. 输出 Spec、Inventory、ValidationReport 和 BuildManifest。

### 第三阶段：补齐地图与质量门禁

1. 完成中国/世界 GeoJSON、地域规范化和 Tab；
2. 检查真实 ECharts series/data，而不是只数 Canvas；
3. 对比 Spec 与 Inventory，输出 Sheet、字段和行级覆盖；
4. 增加溢出、重叠、空图、地图注册和离线检查；
5. 固定 Mock Excel 达到 10/10 Sheet、103/103 行可追踪覆盖。

### 第四阶段：完成开源清理

1. 冻结来源 commit 与哈希；
2. 对主题做 clean-room 重写，而非改名；
3. 完成依赖、字体、地图和示例数据许可证审计；
4. 补充 NOTICE、SECURITY、SBOM 和发布 provenance。

## 8. 重新发布验收门禁

满足以下条件后再判定 GO：

- `quick_validate.py` 通过；
- wheel 和 sdist 在干净环境安装后可导入、可执行；
- Agent Skill 无额外 Key 完成 `Inventory → Spec → HTML → Report`；
- 两条相反需求产生不同且符合语义的 Spec；
- 固定 Mock Excel 的 10 个 Sheet、103 行数据全部可追踪；
- 中国与世界地图真实渲染并通过 Tab 切换；
- 空地图、空 series 和字段缺失必须阻断发布；
- 断网打开 HTML 仍能渲染全部图表；
- Spec 中的主题和布局得到忠实执行；
- Windows、macOS、Ubuntu CI 全部通过；
- provenance 与第三方权利审计完成。

## 9. 本轮未执行

- 未修改实现代码；
- 未运行外部 LLM Planner，因为当前版本没有该能力；
- 未执行跨宿主 Agent 前向测试，因为 Skill 静态校验和安装门禁已经失败；
- 未将临时 HTML 与截图写入仓库；
- 未触碰共享工作区已有的未提交测试截图、trace 或 Claude CLI 的未跟踪示例。
