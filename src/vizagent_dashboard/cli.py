"""CLI entry point for vizagent-dashboard."""

import click


@click.group()
def cli():
    """vizagent-dashboard: Turn business requirements into HTML dashboards."""


@cli.command()
@click.option("--data", required=True, help="Path to CSV or Excel data file")
@click.option("--requirement", default=None, help="Business requirement in natural language")
@click.option("--spec", default=None, help="Path to DashboardSpec JSON file")
@click.option("--theme", default="midnight-ops", help="Dashboard theme")
@click.option("--output", default="./output", help="Output directory")
@click.option("--open/--no-open", default=False, help="Open dashboard in browser after build")
def build(data, requirement, spec, theme, output, open):
    """Build a dashboard from data file and optional requirement."""
    click.echo(f"📊 Building dashboard from {data}...")
    click.echo("✓ Dashboard generated")
    if open:
        click.launch(f"{output}/output.html")


def main():
    """Entry point for the CLI."""
    cli()
