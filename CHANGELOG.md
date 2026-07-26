# vizagent-dashboard 更新日志

## [Unreleased] - 2026-07-27

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
