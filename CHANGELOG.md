# vizagent-dashboard 更新日志

## [Unreleased]

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
