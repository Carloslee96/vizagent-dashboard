"""图表资源注册表 — 复杂图表类型的 CDN、geoJSON、参考代码。

从 viz-agent-team/backend/agents/chart_registry.py 提取（参考源码 commit 见 upstream-manifest.toml）。

为每种复杂图表提供「即插即用」的资源包:
- 额外 CDN 资源（echarts-gl, echarts-wordcloud 等）
- GeoJSON URL（中国地图、世界地图）
- 参考代码模板（注入到 Agent Skill 的 LLM Prompt）

Skill 模式下，宿主 AI 根据 DashboardSpec 中声明的图表类型，
引用本注册表的资源生成 HTML。
"""

from __future__ import annotations

from typing import Any

# ═══════════════════════════════════════════════════════════════════════════════
# CDN 资源库
# ═══════════════════════════════════════════════════════════════════════════════

# ECharts 主库（三层备用，国内优先）
ECHARTS_CDN = """<!-- ECharts 主库 — 三层备用加载 -->
<script src="https://registry.npmmirror.com/echarts/5.4.3/files/dist/echarts.min.js"></script>
<script>
    if (typeof echarts === 'undefined') {
        document.write('<script src="https://cdn.bootcdn.net/ajax/libs/echarts/5.4.3/echarts.min.js"><\\/script>');
    }
    if (typeof echarts === 'undefined') {
        document.write('<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"><\\/script>');
    }
</script>"""

# ECharts GL — 3D 图表扩展（scatter3D, bar3D, map3D, globe）
ECHARTS_GL_CDN = """<!-- ECharts GL — 3D 图表扩展 -->
<script src="https://registry.npmmirror.com/echarts-gl/2.0.9/files/dist/echarts-gl.min.js"></script>
<script>
    if (typeof echarts === 'undefined' || typeof echarts.gl === 'undefined') {
        document.write('<script src="https://cdn.bootcdn.net/ajax/libs/echarts-gl/2.0.9/echarts-gl.min.js"><\\/script>');
    }
</script>"""

# ECharts WordCloud — 词云扩展
ECHARTS_WORDCLOUD_CDN = """<!-- ECharts WordCloud — 词云扩展 -->
<script src="https://registry.npmmirror.com/echarts-wordcloud/2.1.0/files/dist/echarts-wordcloud.min.js"></script>
<script>
    if (typeof echarts === 'undefined' || typeof echarts.wordcloud === 'undefined') {
        document.write('<script src="https://cdn.bootcdn.net/ajax/libs/echarts-wordcloud/2.1.0/echarts-wordcloud.min.js"><\\/script>');
    }
</script>"""

# 世界地图 geoJSON（echarts 4.9 自带 world.json）
WORLD_GEOJSON_URL = "https://cdn.jsdelivr.net/npm/echarts@4.9.0/map/json/world.json"
# 中国地图 geoJSON（含省份边界）
CHINA_GEOJSON_URL = "https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json"

# DataV 地图数据 API 基础（阿里云 DataV 提供的高精度 geoJSON）
DATAV_GEO_BASE = "https://geo.datav.aliyun.com/areas_v3/bound/{code}_full.json"


# ═══════════════════════════════════════════════════════════════════════════════
# 图表资源注册表
# ═══════════════════════════════════════════════════════════════════════════════

ChartResource = dict[str, Any]


def _build_registry() -> dict[str, ChartResource]:
    """构建图表类型 → 资源包的映射。"""

    registry: dict[str, ChartResource] = {}

    # ─────────────────────────────────────────────────────────────────
    # 地图 — 世界地图（含热力图、下钻）
    # ─────────────────────────────────────────────────────────────────
    registry["世界地图"] = {
        "name": "世界地图",
        "complexity": "high",
        "extra_cdn": [],
        "geo_url": WORLD_GEOJSON_URL,
        "note": "需要 fetch geoJSON → echarts.registerMap('world', geoJSON) → type:'map' map:'world'",
        "reference": r"""
// ★ 世界地图模板 — 复制此代码块，替换 data 数组为实际数据 ★
(async function() {
  try {
    const resp = await fetch('GEOJSON_URL');
    const geoJSON = await resp.json();
    echarts.registerMap('world', geoJSON);

    const chart = echarts.init(document.getElementById('chart-world-map'));
    chart.setOption({
      backgroundColor: 'transparent',
      tooltip: { trigger: 'item', formatter: '{b}<br/>{c} 值' },
      visualMap: {
        min: 0, max: 100,
        inRange: { color: ['#0a2a4a', '#1a5a9a', '#4ac8ff', '#e0f0ff'] },
        textStyle: { color: '#8B95A5' }
      },
      series: [{
        type: 'map', map: 'world', roam: true,
        label: { show: false },
        emphasis: { label: { show: true, color: '#fff' }, itemStyle: { areaColor: '#f0c060' } },
        data: [
          { name: 'China', value: 85 },
          { name: 'United States', value: 72 },
          { name: 'Brazil', value: 58 },
          { name: 'India', value: 63 },
          { name: 'Germany', value: 45 },
          // ... 更多国家数据
        ]
      }]
    });

    chart.on('click', function(params) {
      console.log('点击了:', params.name);
    });

    window.addEventListener('resize', () => chart.resize());

  } catch(e) {
    document.getElementById('chart-world-map').innerHTML =
      '<div style="color:#EF4444;text-align:center;padding:40px;">地图数据加载失败，请检查网络</div>';
  }
})();
""".replace("GEOJSON_URL", WORLD_GEOJSON_URL),
    }

    # ─────────────────────────────────────────────────────────────────
    # 地图 — 中国地图
    # ─────────────────────────────────────────────────────────────────
    registry["中国地图"] = {
        "name": "中国地图",
        "complexity": "high",
        "extra_cdn": [],
        "geo_url": CHINA_GEOJSON_URL,
        "note": "需要 fetch geoJSON → echarts.registerMap('china', geoJSON) → type:'map' map:'china'",
        "reference": r"""
// ★ 中国地图模板 ★
(async function() {
  try {
    const resp = await fetch('GEOJSON_URL');
    const geoJSON = await resp.json();
    echarts.registerMap('china', geoJSON);

    const chart = echarts.init(document.getElementById('chart-china-map'));
    chart.setOption({
      backgroundColor: 'transparent',
      tooltip: { trigger: 'item', formatter: '{b}<br/>{c} 值' },
      visualMap: {
        min: 0, max: 100,
        inRange: { color: ['#0a2a4a', '#1a5a9a', '#4ac8ff', '#e0f0ff'] },
        textStyle: { color: '#8B95A5' }
      },
      series: [{
        type: 'map', map: 'china', roam: false,
        label: { show: true, color: '#8B95A5', fontSize: 10 },
        emphasis: { label: { show: true, color: '#fff' }, itemStyle: { areaColor: '#f0c060' } },
        data: [
          { name: '广东', value: 92 }, { name: '北京', value: 88 }, { name: '上海', value: 85 },
          { name: '浙江', value: 78 }, { name: '江苏', value: 82 },
        ]
      }]
    });
    window.addEventListener('resize', () => chart.resize());
  } catch(e) {
    document.getElementById('chart-china-map').innerHTML = '<div style="color:#EF4444;text-align:center;padding:40px;">地图加载失败</div>';
  }
})();
""".replace("GEOJSON_URL", CHINA_GEOJSON_URL),
    }

    # ─────────────────────────────────────────────────────────────────
    # 热力地图 — 在地图底图上叠加热力层
    # ─────────────────────────────────────────────────────────────────
    registry["热力地图"] = {
        "name": "热力地图",
        "complexity": "high",
        "extra_cdn": [],
        "geo_url": WORLD_GEOJSON_URL,
        "note": "地图 + heatmap 系列叠加。先用 registerMap 加载底图，再用 heatmap series 叠加数据点",
    }

    # ─────────────────────────────────────────────────────────────────
    # 3D 图表 — 柱状图、散点图、地球
    # ─────────────────────────────────────────────────────────────────
    registry["3D图表"] = {
        "name": "3D图表",
        "complexity": "high",
        "extra_cdn": [ECHARTS_GL_CDN],
        "note": "需要 echarts-gl CDN。支持 scatter3D, bar3D, surface, globe 等。容器必须有明确的宽高（不能用百分比）。",
    }

    # ─────────────────────────────────────────────────────────────────
    # 3D 地球
    # ─────────────────────────────────────────────────────────────────
    registry["3D地球"] = {
        "name": "3D地球",
        "complexity": "high",
        "extra_cdn": [ECHARTS_GL_CDN],
        "note": "需要 echarts-gl CDN。使用 globe 系列 + 散点叠加。",
    }

    # ─────────────────────────────────────────────────────────────────
    # 桑基图 — 流向关系
    # ─────────────────────────────────────────────────────────────────
    registry["桑基图"] = {
        "name": "桑基图",
        "complexity": "high",
        "extra_cdn": [],
        "note": "纯 ECharts 内置支持。关键是 nodes + links 数据格式。",
    }

    # ─────────────────────────────────────────────────────────────────
    # 关系网络图 — 力导向布局
    # ─────────────────────────────────────────────────────────────────
    registry["关系网络图"] = {
        "name": "关系网络图",
        "complexity": "high",
        "extra_cdn": [],
        "note": "纯 ECharts 内置支持 (type:'graph')。force layout + categories 颜色区分。",
    }

    # ─────────────────────────────────────────────────────────────────
    # 词云图
    # ─────────────────────────────────────────────────────────────────
    registry["词云图"] = {
        "name": "词云图",
        "complexity": "high",
        "extra_cdn": [ECHARTS_WORDCLOUD_CDN],
        "note": "需要 echarts-wordcloud CDN。使用 type:'wordCloud' 系列。",
    }

    # ─────────────────────────────────────────────────────────────────
    # 热力日历图
    # ─────────────────────────────────────────────────────────────────
    registry["热力日历图"] = {
        "name": "热力日历图",
        "complexity": "high",
        "extra_cdn": [],
        "note": "纯 ECharts 内置支持。使用 calendar + heatmap 系列。",
    }

    # ─────────────────────────────────────────────────────────────────
    # 漏斗图
    # ─────────────────────────────────────────────────────────────────
    registry["漏斗图"] = {
        "name": "漏斗图",
        "complexity": "medium",
        "extra_cdn": [],
        "note": "纯 ECharts 内置支持 (type:'funnel')。",
    }

    # ─────────────────────────────────────────────────────────────────
    # 雷达图
    # ─────────────────────────────────────────────────────────────────
    registry["雷达图"] = {
        "name": "雷达图",
        "complexity": "medium",
        "extra_cdn": [],
        "note": "纯 ECharts 内置支持 (type:'radar')。",
    }

    # ─────────────────────────────────────────────────────────────────
    # 散点图/气泡图
    # ─────────────────────────────────────────────────────────────────
    registry["散点图/气泡图"] = {
        "name": "散点图/气泡图",
        "complexity": "medium",
        "extra_cdn": [],
        "note": "纯 ECharts 内置支持 (type:'scatter')。气泡大小由 symbolSize 函数控制。",
    }

    # ─────────────────────────────────────────────────────────────────
    # 瀑布图
    # ─────────────────────────────────────────────────────────────────
    registry["瀑布图"] = {
        "name": "瀑布图",
        "complexity": "medium",
        "extra_cdn": [],
        "note": "用堆叠柱状图实现：透明底柱 + 数据柱。",
    }

    # ─────────────────────────────────────────────────────────────────
    # K线图
    # ─────────────────────────────────────────────────────────────────
    registry["K线图"] = {
        "name": "K线图",
        "complexity": "medium",
        "extra_cdn": [],
        "note": "纯 ECharts 内置支持 (type:'candlestick')。数据格式: [开, 收, 低, 高]。",
    }

    # ─────────────────────────────────────────────────────────────────
    # 仪表盘
    # ─────────────────────────────────────────────────────────────────
    registry["仪表盘"] = {
        "name": "仪表盘",
        "complexity": "medium",
        "extra_cdn": [],
        "note": "纯 ECharts 内置支持 (type:'gauge')。多仪表盘用多个 series 或 grid。",
    }

    # ─────────────────────────────────────────────────────────────────
    # 箱线图
    # ─────────────────────────────────────────────────────────────────
    registry["箱线图"] = {
        "name": "箱线图",
        "complexity": "medium",
        "extra_cdn": [],
        "note": "纯 ECharts 内置支持 (type:'boxplot')。数据格式: [min, Q1, median, Q3, max]。",
    }

    # ─────────────────────────────────────────────────────────────────
    # 区域下钻地图
    # ─────────────────────────────────────────────────────────────────
    registry["区域下钻地图"] = {
        "name": "区域下钻地图",
        "complexity": "high",
        "extra_cdn": [],
        "geo_url": CHINA_GEOJSON_URL,
        "note": "点击省份 → fetch 该省份的 geoJSON（DataV API）→ echarts.registerMap → setOption。",
    }

    return registry


# ═══════════════════════════════════════════════════════════════════════════════
# 公共接口
# ═══════════════════════════════════════════════════════════════════════════════

# 全局单例
_CHART_REGISTRY: dict[str, ChartResource] | None = None


def get_registry() -> dict[str, ChartResource]:
    """获取图表资源注册表（懒加载）。"""
    global _CHART_REGISTRY
    if _CHART_REGISTRY is None:
        _CHART_REGISTRY = _build_registry()
    return _CHART_REGISTRY


def lookup_chart(chart_name: str) -> ChartResource | None:
    """按图表名称查找资源。支持模糊匹配和别名映射。"""
    registry = get_registry()

    # 精确匹配
    if chart_name in registry:
        return registry[chart_name]

    # 模糊匹配：按 key 长度降序，优先匹配更具体的键
    for key in sorted(registry, key=len, reverse=True):
        if key in chart_name or chart_name in key:
            return registry[key]

    # 特殊别名映射
    aliases = {
        "3D": "3D图表",
        "三维": "3D图表",
        "world": "世界地图",
        "china": "中国地图",
        "wordcloud": "词云图",
        "sankey": "桑基图",
        "network": "关系网络图",
        "graph": "关系网络图",
        "funnel": "漏斗图",
        "radar": "雷达图",
        "gauge": "仪表盘",
        "candlestick": "K线图",
        "waterfall": "瀑布图",
        "boxplot": "箱线图",
        "treemap": "散点图/气泡图",
    }
    name_lower = chart_name.lower()
    for alias, target in aliases.items():
        if alias.lower() in name_lower:
            return registry.get(target)

    return None


def build_resource_injection(chart_names: list[str]) -> str:
    """根据图表名称列表，构建注入到宿主 AI Prompt 中的资源块。

    包含：缺失的 CDN 脚本 + 每个复杂图表的参考代码模板。
    只对「复杂图表」（complexity=high）注入参考代码，避免 token 爆炸。
    """
    if not chart_names:
        return ""

    registry = get_registry()
    parts = []
    seen_cdn = set()

    for name in chart_names:
        resource = lookup_chart(name)
        if not resource:
            continue

        # 收集 CDN
        for cdn in resource.get("extra_cdn", []):
            if cdn not in seen_cdn:
                seen_cdn.add(cdn)
                parts.append(f"【额外 CDN — {resource.get('name', name)}】\n{cdn}")

    # 参考代码（仅 high 复杂度）
    for name in chart_names:
        resource = lookup_chart(name)
        if not resource:
            continue
        if resource.get("complexity") != "high":
            continue
        ref = resource.get("reference", "")
        note = resource.get("note", "")
        geo = resource.get("geo_url", "")
        if ref or note:
            parts.append(f"\n【★ 参考模板 — {resource.get('name', name)}】")
            if note:
                parts.append(f"实现要点: {note}")
            if geo:
                parts.append(f"geoJSON数据源: {geo}")
            if ref:
                parts.append(f"参考代码（请根据实际数据字段和数据值修改）:\n```javascript\n{ref.strip()}\n```")

    return "\n".join(parts) if parts else ""