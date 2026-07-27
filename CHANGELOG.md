# vizagent-dashboard 更新日志

## [Unreleased]

## [0.1.6] - 2026-07-27

### 修复：版本号 SSOT

- **Bug#6 `vizagent --version` 报错版本**：`__init__.py` 的 `__version__` 硬编码 `"0.1.0"` 从未同步，导致 CLI 永远报 0.1.0（`pip show` 才准）。改为 `importlib.metadata.version("vizagent-dashboard")` 读包元数据，版本号单一事实来源在 `pyproject.toml`，bump 即自动同步。源码未安装时兜底 `"0.0.0"`。
- 测试：新增 `test_version_matches_package_metadata` 防退化；141 测试全绿。

## [0.1.5] - 2026-07-27

### 关键修复：图表不渲染 + 新图表类型自动可达

E2E 测试发现 v0.1.4 含 gauge 的大屏整屏图表不渲染，并暴露 planner 选型与控制台编码问题，本轮一并修复。

- **Bug#4 gauge 炸全屏（critical）**：`gauge.py` 的 `axisLine.lineStyle` 误写成列表 `[{...}]`，ECharts 5 要求对象 `{width,color}`，`setOption` 抛 `Cannot read properties of undefined (reading 'length')`。修复为对象。
- **Bug#5 init 无容错（critical）**：`skeleton.py` 的 `initVisible` 循环无 per-chart try/catch，单图 setOption 抛异常会中断循环、连累后续所有图表不初始化。改为 per-chart try/catch，失败显示占位 + console.error，不连累其他图。
- **Bug#1 新图表类型自动模式够不着**：`_explicit_chart_type` 原要求 requirement 含「只展示/仅展示」才生效，且全局强制单一类型。新增 `_requested_types`——雷达/漏斗/仪表盘/南丁格尔/树图/面积/热力 等关键词无需「只展示」即可触发；「尽可能多类型/丰富/各种图表」触发全类型分发。保留「只展示 X」全局强制语义（向后兼容）。
- **Bug#2 planner 不校验字段兼容性**：硬塞 radar 给单数值 sheet 会报错。新增 `_compatible_types`：radar 需 ≥2 数值、heatmap 需 2 分类维度 + 1 数值、area 需时间字段、gauge 需 ≥1 数值，不兼容回退 bar/pie。选型用「最少使用优先」最大化类型多样性，特异性做 tiebreak（radar 优先于 nightingale）。
- **Bug#3 Windows 控制台中文 GBK 乱码**：CLI 顶层 `sys.stdout/stderr.reconfigure(encoding="utf-8")`，所有命令中文路径/列名/警告不再乱码。
- 主题推断补「暖色/暖色调/珊瑚/温暖」→ `coral-warm`。
- 测试：`test_planner.py` 加 `TestPlannerNewChartTypes` 7 项（关键词可达 / 字段兼容回退 / 多类型分发）；140 测试全绿，ruff 全清。
- E2E：销售明细 +「要用尽可能多类型的图表」自动产出 10 种图表类型（kpi/map_world/radar/gauge/pie/nightingale/area/treemap/funnel/line），Playwright 9/9 渲染 0 报错。

## [0.1.3] - 2026-07-27

### 多 AI 工具 Skill 安装 + 安装提示语

- **Cursor 支持**：新增 `.cursor/rules/vizagent-dashboard.mdc`（按 .csv/.xlsx glob 自动注入），clone 即用。
- **Codex CLI 支持**：新增 `.codex/prompts/vizagent-dashboard.md`（`/vizagent-dashboard` 斜杠命令），clone 即用。
- **`vizagent skill install --target`**：支持 `claude`（默认）/ `cursor` / `codex` / `all`，一次装齐多个工具到用户级目录。
- **安装提示语**：`skill install` 成功后打印各工具触发方式 + 命令行直跑示例 + 文档链接；Windows GBK 控制台强制 UTF-8 输出避免乱码。
- **wheel 打包 3 套规则文件**：pyproject `force-include` 映射 SKILL.md / cursor .mdc / codex .md 进 `skill_assets/`。
- **契约测试**：新增 `test_skill_install_all_targets` / `test_skill_path_all_targets`；干净 venv 装 wheel 实测三工具全装上。
- README 中英两版「作为 Skill 使用」章节扩成多工具表。

## [0.1.2] - 2026-07-27

### Claude Code Skill 开箱即用（治本）

修复 v0.1.1 的发布缺陷：pip 安装后无法在 Claude Code 里用 `/vizagent-dashboard` 触发——SKILL.md 既没进 pip 包，也没文档说明安装路径。

- **canonical SKILL.md**：新增 `.claude/skills/vizagent-dashboard/SKILL.md`（`user-invocable: true`，含工作流 + DashboardSpec 参考 + 排错表）。clone 仓库并用 Claude Code 打开即自动注册为项目级 Skill。
- **`vizagent skill install` 子命令**：pip 用户一行命令把 SKILL.md 装到 `~/.claude/skills/vizagent-dashboard/`，重启 Claude Code 即可斜杠触发；`vizagent skill path` 查看打包位置。定位逻辑双路回退（wheel 包内数据 → 仓库相对路径）。
- **wheel 打包 SKILL.md**：pyproject 加 hatch `force-include`，把 SKILL.md 映射进 `vizagent_dashboard/skill_assets/SKILL.md`，pip 装完即含。
- **README 安装说明**：中英两版补「作为 Claude Code Skill 使用」章节（pip 路径 + clone 路径 + Codex 路径）。
- **契约测试**：新增 `test_skill_path_command` / `test_skill_install_command`，验证定位与安装（monkeypatch 重定向 home，不污染真实用户目录）。干净 venv 装 wheel 实测通过。
- **lint 清债**：`tools/feishu_publish.py` 5 处 ruff 错误清零（import 排序、contextlib.suppress、with open、set comprehension）。

## [0.1.4] - 2026-07-27

### SaaS 品牌主题去品牌引入（P1）

把 SaaS 主项目 20 个品牌导向主题**去品牌**引入开源 skill，主题数 5 → 25。

- **去品牌变换**：每个 SaaS 主题只提取 12 个核心 token（`--bg-*` / `--text-*` / `--border-subtle` / `--accent-primary` / `--map-*` / `--radius-card` / `--font-family-*`）+ Chart 色板；**颜色/圆角 token 逐字节保真**（hex 与源同名 token 完全一致）；**字体栈 `-apple-system` → `system-ui`** 归一化去品牌；赋纯描述性中性名（如 spotify→`grove-dark`、airbnb→`coral-warm`、claude→`parchment-serif`）；Visual Theme prose 重写为中性美学描述，剔除全部品牌名 / 品牌专有色名（Rausch/Babu/Crail 等）/ 品牌签名指纹 / 品牌定位文案；SaaS 的 Fingerprint/Component/Motion/Anti-Pattern 等重 prose 一律不搬（lean 编译器不消费）。
- **新主题 20 个**：`coral-warm` / `obsidian-glass` / `parchment-serif` / `trust-blue` / `canvas-dot` / `ops-slate` / `ring-pastel` / `nebula-glow` / `graphite-iris` / `broadsheet` / `fiber-paper` / `grid-azure` / `gilt-navy` / `ember-paper` / `amethyst-glass` / `grove-dark` / `haze-lilac` / `phosphor-green` / `amber-scan` / `mono-noir`（7 light + 13 dark）。
- **保真度校验器** `tools/import_saas_themes.py`：逐对校验 clean-room 主题 token 与 SaaS 源同名 token 一致（颜色/圆角逐字节，字体归一化）+ 全文品牌残留扫描；`python tools/import_saas_themes.py` → 20/20 PASS，可复现验证供法律复核。
- **审计文档** `docs/THEME_AUDIT.md` 扩写：记录 20 主题来源映射、去品牌变换规则、glass/glow 不渲染特效的限制（lean 编译器只灌 css_vars 不按 `--decoration` 分支）、`amethyst-glass` 半透明卡说明。
- **命名避碰**：terminal-amber 命名为 `amber-scan` 而非 `amber-console`，避开与原创主题旧别名 `amber-console -> signal-dark` 的 id/别名同名碰撞。
- 测试：`test_themes.py` 加 `TestDebrandedThemes`（注册/加载/解析/品牌残留/id-别名不碰撞/解析 5 项）+ `test_skeleton` 加 P1 主题端到端编译；主题数断言 5→25；127 测试全绿。

### 新图表类型 batch C（P4：heatmap）

- **heatmap**：热力图，x_field × series_field 二维网格，值为 y_field 聚合（同坐标求和）；visualMap 分色段（grid_color→palette[0]）。`data_hints=("matrix",)`，需 series_field 否则返回 base。
- **series_field 透传**：`build_chart_option` 新增可选 `series_field` 参数 + `ChartContext.series_field`；skeleton 传 `item.series_field`，`_prepare_chart_rows` 跳过 heatmap（保留二维原行，不按 x 聚合）。向后兼容（默认 None，现有调用输出不变）。
- planner 加「热力」关键词→heatmap。
- 测试：heatmap 网格/visualMap/无 series 降级 + skeleton 端到端；8 case 字节级不变；127 passed。

### 新图表类型 batch B（P4：gauge/radar）

- **gauge**：仪表盘单值进度（灰底 + 彩色 progress 填充 + 中心 detail 大数字）；百分比类（≤100）按 0-100 量程，否则量程=max(100,value)。`data_hints=("single_metric",)`。
- **radar**：雷达图，每 y_field 一维度（max 取数据最大值），每 x 类别一条数据，半透明 areaStyle；需 ≥2 个 y 字段否则返回 base。`data_hints=("multivariate",)`。
- planner `_explicit_chart_type` 加关键词：仪表盘/进度→gauge、雷达→radar（+ 南丁格尔/树图/漏斗/面积 补齐），`--requirement` 可达。
- 测试：gauge（求和+量程）、gauge 百分比、radar 多维度、radar 单字段降级 + skeleton 端到端；8 case 字节级不变；124 passed。

### 新图表类型 batch A（P4：area/nightingale/treemap/funnel）

- **area**：补 `ChartType.area` 枚举值（builder 已存在），Spec 可达。
- **nightingale**：南丁格尔玫瑰图（pie + `roseType="area"`，radius `["18%","70%"]`）。
- **treemap**：矩形树图（面积反映数值），从 SaaS port。
- **funnel**：漏斗图（转化/阶段，descending）。
- 三者 `data_hints=("composition",)`，注册在 pie 之后（pie 仍是 composition 默认）。
- skeleton else 分支自动路由，无需改编译循环。测试：4 个 build_chart_option 用例 + 1 个 skeleton 端到端；现有 8 case 字节级不变；119 passed。

### Planner 用 data_hints 选型（P3）

- **builder 自声明 data_hints**：`ChartBuilder` Protocol 加 `data_hints` 类属性；line/area=`time_series`、bar=`comparison`、pie=`composition`、scatter=`correlation`。新增 `select_chart_type_by_hint(hint)` 按注册顺序取第一个匹配者（约定：同 hint 的默认类型先注册，故 time_series→line、composition→pie）。
- **planner 解耦**：`heuristic.py` 自动推断从硬编码 `ChartType.line/pie/bar` 改为 `_hint_type(hint, fallback)` 走注册表；显式「只展示 X」、map/kpi/table special-case 不变。**选型行为完全不变**（先补 `test_planner.py` 9 个回归基线兜底）。
- 价值：新图表类型声明 hints 即可被 planner 选型机制识别，不必改 planner 选型分支。
- 测试：新增 `test_planner.py`；build_chart_option 8 case 字节级仍一致；114 passed。

### 用户主题目录（P5）

- **多源主题扫描**：`compiler/themes.py` 加载顺序为 包内 `assets/*.md` → 用户 `~/.vizagent/themes/*.md` → `--theme-dir <path>`，同 id 后者覆盖前者；`set_theme_dir()` 清缓存确保覆盖立即生效。
- **`--theme-dir` CLI**：`build` / `compile` 命令新增 `--theme-dir` 选项，注入项目级主题目录。用户/团队丢一个 `.md` 到 `~/.vizagent/themes/` 或指定目录即可用自己品牌主题，不 fork、不碰源码。
- **测试**：新增 `TestUserThemeDir`（发现/覆盖/恢复）+ `test_compile_theme_dir_loads_user_theme`（CLI 端到端）。105 测试全绿。

### 主题 + 图表类型扩展骨架（P0 + P2-core）

立「丢文件/加模块即可增减」的扩展骨架，核心编译逻辑零改动。详见 `docs/EXTENSIBILITY.md`。

- **P0 主题注册表**：5 个主题 `.md` 加 frontmatter（`id`/`name`/`aliases`/`decoration`/`base`，别名自声明，SSOT）；`compiler/themes.py` 退役硬编码 `THEME_IDS`/`ALIASES`，改自动扫描 `assets/*.md`；`load_theme` 返回去 frontmatter 的正文。加主题 = 丢一个 .md 文件。`THEME_IDS` 保留为派生常量（向后兼容）。
- **P2 图表注册表核心**：新建 `compiler/charts/` 包——`ChartBuilder` Protocol + `ChartContext` + `CHART_BUILDERS` 显式注册表 + `build_chart_option` 分发器；line/area/bar/pie/scatter 各一个 builder，代码从 `chart_options.py` 逐行搬迁。`chart_options.py` 降为向后兼容 facade（skeleton / 测试导入路径不变）。加 ECharts 图表类型 = 加 enum 值 + builder 文件 + 注册一行，skeleton 编译循环自动路由。
- **回归保证**：5 主题 `parse_design_tokens` 输出与改前字节级一致；`build_chart_option` 8 个 case（line/bar/pie/scatter/area/空数据/未知类型回退/自定义 palette）输出与改前字节级一致；101 测试全绿。
- **不动**：`skeleton.py` 编译循环、`ChartType` 枚举、planner、schema（kpi/table/map 不产 ECharts option，强塞统一接口属过度抽象；枚举退役波及面大收益低，均按设计稿后续阶段处理）。

### 飞书 Wiki 自动发布

- **发布脚本**：新增 `tools/feishu_publish.py`——把 Markdown 自动发布到飞书知识库（建 wiki docx 节点 → 解析 md 为飞书 blocks → 逐个写入），仅依赖 Python 标准库。MD 路径与标题走命令行参数，可移植。
- **运维指南**：新增 `docs/FEISHU_PUBLISH.md`——凭证、5 个 scope、知识库成员授权、block 字段映射表（标题 heading{level}、分隔线 divider:{}）、6 条踩坑记录、安全须知，供 maintainer 与接手 AI 无缝衔接。
- **个人版飞书适配**：drive 上传被禁（1061004），改走 wiki 节点 + docx blocks 写入；图片不内嵌改文字链接；表格转代码块；引用降级斜体文本。

## [0.1.1] - 2026-07-27

### README 重写（未发布版本，仅 main）

- **英文版 README**：新增 `README.en.md`，结构与中文版对齐，便于海外推广；中英两版顶部加语言切换链接。
- **全中文**：去除中英文混杂，所有描述改中文（命令/技术术语保留英文）。
- **场景故事开头**：以「老板要大屏」场景代入，直观展示「给数据自动出大屏」。
- **requirement 定位澄清**：明确 `--requirement` 可选、默认自动分析；新增「关于需求参数」专节，回答「给了数据为何不能自动分析」——默认就是自动分析（日期→折线、地理→地图、占比→饼图），已用 3 表数据实测验证。
- **新演示图**：`docs/assets/demo.png` 为真实自动生成的大屏全页截图——4 KPI + 世界地图站点分布 + 8 图表（2 折线/4 柱状/2 饼图），由 10 个 Sheet 自动识别，浏览器门禁 100/100。
- **示例数据**：新增 `examples/销售明细.xlsx`（10 Sheet 合成数据），用户克隆后可 `vizagent build --data examples/销售明细.xlsx` 复现 README 演示。

### PyPI 上线

- **release.yml 开启 PyPI 发布**：取消 PyPI step 注释，启用 Trusted Publisher（OIDC 免 token）。依赖 maintainer 在 pypi.org 预登记 pending publisher（project=vizagent-dashboard, owner=Carloslee96, repo=vizagent-dashboard, workflow=release.yml）。
- **登记指南文档**：新建 `docs/PyPI_SETUP.md`（登记步骤、版本规则、发布路径、本机环境运维要点、排错速查），供 maintainer 与接手 AI 无缝衔接。
- **API 发布工具**：新建 `tools/publish_via_api.py`——github.com 不通时通过 Git Data API 在服务端构造提交+tag，绕开 git push；可传版本号复用。
- **版本号 0.1.0 → 0.1.1**：pyproject / SBOM 同步；PyPI 不允许覆盖版本号，故 v0.1.0 仅 GitHub，PyPI 从 v0.1.1 起。
- **Release Notes v0.1.1**：新建 `docs/RELEASE_NOTES_v0.1.1.md`，release.yml `body_path` 指向它。

### 一键发布自动化

- **仓库归属落定**：公开仓库为 `Carloslee96/vizagent-dashboard`（已存在、公开、空），采用根布局（`pyproject.toml`/`src/`/`README.md` 在根）。
- **一键发布脚本**：新建 `tools/publish.sh`——自检（lint+测试+构建）→ `git subtree split` 拆 skill/ 为根布局 → 推送 main → 打 v0.1.0 tag 触发 release.yml。全程不碰 SaaS 代码。
- **workflow 适配根布局**：ci.yml / security.yml / release.yml 移除 monorepo 专用的 `working-directory: skill` 与 `paths: ["skill/**"]`；dist 路径改为根 `dist/`。
- **release.yml 用精修正文**：GitHub Release 正文改用 `docs/RELEASE_NOTES_v0.1.0.md`（`body_path`）。
- **PyPI v0.1.0 暂停**：release.yml 的 PyPI step 注释掉，待 maintainer 在 pypi.org 做一次性 Trusted Publisher 登记后开启。
- **仓库 URL 全局修正**：README / pyproject / SBOM / CONTRIBUTING / RELEASE_NOTES 里的 `vizagent/dashboard` 全部改为 `Carloslee96/vizagent-dashboard`，`cd skill/` 改为 `cd vizagent-dashboard`。

### 发布材料准备

- **Release Notes**：新建 `docs/RELEASE_NOTES_v0.1.0.md`，精修的 GitHub Release 正文草稿（安装、上手、内容清单、已知限制、致谢）。
- **发布操作手册**：新建 `docs/PUBLISH_RUNBOOK.md`，面向 maintainer 的发布流程（commit/push/release 概念辨析、自检、打 tag、PyPI、回滚）。
- **README 截图去死链**：用真实 ecommerce 大屏截图替换不存在的 `demo.gif`；Gallery 改为「同数据 5 主题」实景首屏（midnight-ops / paper-light / warm-editorial / signal-dark），移除指向未建 Pages demo 站的死链。
- **Lint 整理**：3 个测试文件 import 按 ruff 字母序重排，无逻辑变化。

### Phase 4 收口：开源清理与权利审计

- **Provenance**：重写 `tools/upstream-manifest.toml`，记录代码模块来源 commit `94f763f` + extracted_at；删除 20 个已废弃品牌主题映射；声明 5 个新主题为 clean-room 原创非提取；声明 vendor 资产来源。
- **治理文件**：扩写 `NOTICE`（完整第三方清单）；新建 `SECURITY.md`（安全模型 + 漏洞报告）、`CONTRIBUTING.md`（README 已链接）、`SBOM.md`（依赖许可证清单）。
- **主题审计**：新建 `docs/THEME_AUDIT.md`，实证 5 主题无第三方品牌残留，9 别名解析到 clean 主题。
- **GeoJSON 许可已核实**：china.json / world.json 经逐字节比对确认均来自 npm `echarts@4.9.0`（Apache 2.0，可再分发），纠正了设计文档误写的「DataV」来源；NOTICE / SBOM / upstream-manifest 同步落定，移除「待复核」标记。
- **CI 三平台**：`ci.yml` 扩为 Windows/macOS/Ubuntu × Python 3.10-3.12 跑 unit；新增 contract job 跑 CLI + wheel 契约测试。
- **Lint 清债**：ruff 24 个错误清零（auto-fix import 排序/未用导入 + 手动修 cli 重复 except + 5 处提取代码合理模式 noqa），CI lint 门禁转绿。

### Phase 1 收口：可安装、可验证、可复现

接手 WIP 检查点（0d4be9e）后的 Phase 1 完成项，对照 `docs/TEST_REPORT_2026-07-27.md` 的发布阻断：

- **测试迁移到新 API**：21 个失败测试全部迁移到 5 主题 / 新编译 / 新门禁契约，新增 CLI 与 wheel 契约测试，共 97 passed。
- **修复主题规范化**（skeleton）：manifest 现记录规范化主题 ID，旧别名（monitor-dark 等）与规范 ID 产出一致。
- **修复浏览器门禁假阳性**（browser）：tabs / map-tabs 模式下隐藏 Tab 的图不再误报零尺寸；零尺寸检查只对可见图生效。
- **修复电商示例 scatter**（spec.json）：`y_field` 由逗号字符串改为 list，散点图正确生成 series。
- **Skill 边界**：退役 root `SKILL.md`，填充规范 `skills/build-data-dashboard/SKILL.md`（合规 frontmatter，仅 name+description）；修复 `agents/openai.yaml` 乱码。
- **README 去虚假宣传**：移除未实现的 `config --set api_key` / `--planner` / LLM-key 模式；主题表改为 5 个 clean-room 主题。
- **wheel 干净安装验证**（P0-1）：包路径修正为 `vizagent_dashboard/`，源码路径外临时 venv 安装可 import / 可执行 / 可 build。
- **Mock Excel 闭环**（10 sheet / 103 行）：3 KPI + 9 图（line×2 / bar×3 / pie×2 / china+world 地图），coverage 103/103，tabs 切换，浏览器门禁 100/100，9/9 图表渲染，两地图注册。

## [0.1.0] - 2026-07-26

### ✨ 初始发布

- **双模式架构**：Agent Skill（宿主 LLM 推理） + CLI（离线编译），同一编译内核
- **数据盘点**：CSV / XLSX 自动读取，多 Sheet 支持，数据类型推断
- **DashboardSpec 契约**：版本化 JSON Schema 作为唯一意图载体
- **确定性编译**：Compiler 无 LLM/网络依赖，输出可复现
- **图表类型**：折线图、柱状图、饼图、散点图、KPI 卡片、中国地图、世界地图
- **20+ 预置主题**：从 SaaS 设计系统一次性提取，去品牌重命名 — paper-linen（暖纸衬线）、minimal-doc（温暖纸感）、command-post（指挥中心）、fitness-glass（健康玻璃）、warm-editorial（暖色新闻）、monitor-dark（暗色运维）、cozy-retreat（旅行暖棕）、clean-slate（简洁亮色）、design-toolkit（设计师工具）、vibe-night（音乐暗色）、crypto-sleek（金融深色）、checkout-light（亮色支付）、minimal-tracker（极简项目管理）、ocean-night（深海）、error-monitor（错误监控）、growth-analytics（产品分析）、deal-room（金融暗色）、open-table（开源暗色）、amber-console（琥珀终端）、deploy-light（亮色部署）
- **质量门禁**：自动检查截断、重叠、零尺寸图表、地图覆盖率
- **安全基线**：HTML 转义 + Content Security Policy + 路径穿越防护
- **CLI 接口**：`vizagent build --data --requirement --output --theme`
- **Agent Skill**：可加载为 Claude Code / Codex Skill，无需 API Key
- **示例大屏**：电商经营分析、全球连接分布、运营健康监控
