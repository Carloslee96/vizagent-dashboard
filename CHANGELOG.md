# vizagent-dashboard 更新日志

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
