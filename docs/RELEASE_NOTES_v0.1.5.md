# Release Notes — vizagent-dashboard v0.1.5

## 一句话

修复 v0.1.4 含 gauge 的大屏整屏图表不渲染的严重 bug，并让 14 种图表类型在自动模式真正可达（按字段兼容性分配），CLI 中文不再乱码。

## 安装

```bash
pip install --upgrade vizagent-dashboard==0.1.5
```

## 为什么发 v0.1.5

v0.1.4 发布后 E2E 测试发现：凡是用到 gauge 仪表盘的大屏，**整屏图表都不显示**。根因是 gauge builder 的 option 结构写错，叠加图表初始化代码没有 per-chart 容错——一张图抛异常就中断整个初始化循环。本轮修这个 critical bug，并顺带修了 planner 选型和控制台编码问题。

## 相对 v0.1.4 的变化

### 修复

| # | 问题 | 严重度 | 修复 |
|---|---|---|---|
| 4 | gauge `axisLine.lineStyle` 写成列表，setOption 抛异常 → 含 gauge 的大屏整屏不渲染 | **critical** | 改为对象 |
| 5 | 图表初始化循环无 try/catch，单图炸连累全屏 | **critical** | per-chart try/catch，失败显示占位 |
| 1 | 新图表类型（radar/gauge/heatmap 等）自动模式够不着，需「只展示」前缀且全局强制单一类型 | 中 | 关键词无需「只展示」即可触发，按 sheet 兼容性分配 |
| 2 | planner 不校验字段兼容性，radar 塞单数值 sheet 报错 | 中 | `_compatible_types` 守门，不兼容回退 |
| 3 | Windows 控制台中文路径/列名/警告 GBK 乱码 | 低 | CLI 顶层强制 UTF-8 输出 |

### 新图表类型现在自动可达

v0.1.4 的 14 种图表类型中，area/nightingale/treemap/funnel/gauge/radar/heatmap 在自动模式基本够不着。v0.1.5 修复后：

```bash
# 自动分发多种新类型（按各 sheet 字段形态分配）
vizagent build --data sales.xlsx --requirement "要用尽可能多类型的图表"

# 点名具体类型
vizagent build --data sales.xlsx --requirement "用雷达图、漏斗图、仪表盘"
```

字段兼容性规则（不兼容自动回退到 bar/pie）：

| 图表类型 | 字段要求 |
|---|---|
| radar 雷达 | ≥2 个数值字段 |
| heatmap 热力图 | 2 个分类维度 + 1 个数值 |
| area 面积 | 时间字段 + 数值 |
| gauge 仪表盘 | ≥1 个数值 |
| nightingale/treemap/funnel/pie | 1 个分类 + 1 个数值 |

### 「只展示 X」语义保留

`--requirement "只展示饼图"` 仍全局强制所有图表为饼图（向后兼容）。区别：不带「只展示」时，关键词按 sheet 兼容性**分发**不同类型，不再全局强制单一类型。

## 30 秒上手

```bash
# 默认主题，编译完自动打开
vizagent build --data sales.xlsx --open

# 暖色主题 + 全类型分发
vizagent build --data sales.xlsx --requirement "要用尽可能多类型的图表，暖色" --open

# 换 25 个主题之一
vizagent build --data sales.xlsx --theme grove-dark --open
```

## 测试

140 passed（含 P1 去品牌主题校验 + 新增 7 项 planner 新图表类型测试 + P3/P4 回归）；ruff src/ tests/ 全清。E2E Playwright 验证 9/9 图表渲染、0 pageerror。

## 已知限制（承自 v0.1.4，未变）

- glass / glow 装饰不渲染特效（lean 编译器只灌 CSS 变量，不按 `--decoration` 分支）。
- 20 个去品牌主题保留原样品牌签名 hex（色值本身不可版权，配中性名 + 中性 prose 后可辩护）。
