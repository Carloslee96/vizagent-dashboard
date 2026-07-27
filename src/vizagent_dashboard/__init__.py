"""vizagent-dashboard: Turn business requirements into standalone HTML dashboards."""

from importlib.metadata import PackageNotFoundError, version

try:
    # 单一事实来源：pyproject.toml 的 version（通过包元数据读取），不再硬编码
    __version__ = version("vizagent-dashboard")
except PackageNotFoundError:  # 源码直接运行（未安装）时兜底
    __version__ = "0.0.0"
