"""CLI entry point for vizagent-dashboard."""

import json
import logging
from pathlib import Path

import click

from vizagent_dashboard.compiler.skeleton import compile_dashboard
from vizagent_dashboard.inventory.reader import read_file
from vizagent_dashboard.schemas.dashboard_spec import DashboardSpec
from vizagent_dashboard.validation.static import validate_html

logger = logging.getLogger(__name__)


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
@click.pass_context
def cli(ctx, verbose):
    """vizagent-dashboard: Turn business requirements into HTML dashboards."""
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


@cli.command()
@click.option("--data", required=True, help="Path to CSV or Excel data file")
@click.option("--requirement", default=None, help="Business requirement in natural language")
@click.option("--spec", "spec_path", default=None, help="Path to DashboardSpec JSON file")
@click.option("--theme", default="midnight-ops", help="Dashboard theme (see README §Themes)")
@click.option("--output", default="./output", help="Output directory")
@click.option("--open/--no-open", default=False, help="Open dashboard in browser after build")
def build(data, requirement, spec_path, theme, output, open):
    """Build a dashboard from data file and optional spec/requirement."""
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)

    click.echo(f"📊 Building dashboard from {data}...")
    click.echo(f"   Theme: {theme}")

    # 1. 读取数据
    try:
        sheets = read_file(data)
        # 取第一个 sheet 的数据（或合并所有 sheet）
        if len(sheets) == 1:
            excel_data = list(sheets.values())[0]
        else:
            # 多 sheet：合并所有数据（保留 sheet 字段以便区分）
            excel_data = []
            for sheet_name, rows in sheets.items():
                for row in rows:
                    row_with_sheet = dict(row)
                    row_with_sheet["sheet"] = sheet_name
                    excel_data.append(row_with_sheet)
        click.echo(f"   Data: {len(excel_data)} rows, {len(sheets)} sheet(s)")
    except Exception as e:
        click.echo(f"❌ Failed to read data: {e}", err=True)
        raise click.Abort()

    # 2. 加载或构造 DashboardSpec
    if spec_path:
        try:
            with open(spec_path, encoding="utf-8") as f:
                spec_data = json.load(f)
            spec = DashboardSpec(**spec_data)
            click.echo(f"   Spec: loaded from {spec_path}")
        except Exception as e:
            click.echo(f"❌ Failed to load spec: {e}", err=True)
            raise click.Abort()
    else:
        # 默认 spec：基于数据自动推断
        spec = _auto_spec(excel_data, requirement, theme)
        click.echo(f"   Spec: auto-generated ({len(spec.layout)} rows)")

    # 3. 编译 HTML
    try:
        html_content = compile_dashboard(
            spec=spec,
            excel_data=excel_data,
            theme_id=theme,
            deployment_mode="cdn",
        )
    except Exception as e:
        click.echo(f"❌ Compilation failed: {e}", err=True)
        raise click.Abort()

    # 4. 验证
    report = validate_html(html_content)
    click.echo(f"   Validation: {'✓ OK' if report['is_valid'] else '⚠ ' + str(len(report['issues'])) + ' issue(s)'}")
    if report["issues"]:
        for issue in report["issues"][:5]:
            click.echo(f"     - {issue}")

    # 5. 写入输出
    output_file = output_path / "output.html"
    output_file.write_text(html_content, encoding="utf-8")

    click.echo(f"✓ Dashboard generated → {output_file.absolute()}")
    click.echo(f"   HTML: {report['html_length']} bytes")
    click.echo(f"   Charts: {report['chart_counts']}")

    if open:
        click.launch(str(output_file.absolute()))


def _auto_spec(excel_data: list[dict], requirement: str | None, theme: str) -> DashboardSpec:
    """从数据自动推断 DashboardSpec。

    启发式：
    - 顶部 1 行 KPI（第一个数值列的 sum）
    - 中间 1 行 折线图（按首个时间列分组的第一个数值列）
    - 底部 1 行 柱状图（按首个分类列分组的第一个数值列）
    """
    from vizagent_dashboard.schemas.dashboard_spec import ChartItem, LayoutRow

    if not excel_data:
        return DashboardSpec(title="数据大屏", theme=theme)

    cols = list(excel_data[0].keys())
    # 分类列（找可能的字段名）
    cat_col = next((c for c in cols if any(kw in c.lower() for kw in ["month", "category", "type", "name", "月", "类别", "名称", "类型", "地区"])), cols[0] if cols else "")
    # 数值列
    num_col = next((c for c in cols if any(kw in c.lower() for kw in ["value", "amount", "count", "sales", "值", "金额", "数量", "销售", "收入"])), "")
    if not num_col:
        # fallback：选第一个数值型列
        for c in cols:
            try:
                float(str(excel_data[0].get(c, "0")).replace(",", "").replace("¥", "").replace("%", ""))
                num_col = c
                break
            except (ValueError, TypeError):
                continue

    title = "数据大屏"
    if requirement:
        # 从需求中提取标题关键词
        title = f"数据分析大屏"

    layout = [
        LayoutRow(items=[
            ChartItem(
                chart_type="kpi",
                title=f"总{num_col}" if num_col else "数据",
                data_field=num_col,
                aggregation="sum",
                width=1,
                height=1,
            ),
        ]),
        LayoutRow(items=[
            ChartItem(
                chart_type="line",
                title=f"{num_col} 趋势" if num_col else "趋势",
                x_field=cat_col,
                y_field=num_col,
                width=2,
                height=1,
            ),
        ]),
        LayoutRow(items=[
            ChartItem(
                chart_type="bar",
                title=f"各{cat_col}{num_col}对比" if cat_col and num_col else "对比",
                x_field=cat_col,
                y_field=num_col,
                width=2,
                height=1,
            ),
        ]),
    ]

    return DashboardSpec(title=title, theme=theme, layout=layout)


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()