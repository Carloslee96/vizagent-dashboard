"""VizAgent Dashboard CLI。"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import tempfile
from pathlib import Path
from typing import Any

import click

from vizagent_dashboard import __version__
from vizagent_dashboard.compiler.skeleton import compile_artifacts
from vizagent_dashboard.inventory.reader import inventory_file
from vizagent_dashboard.planner.heuristic import plan_dashboard
from vizagent_dashboard.schemas.dashboard_spec import DashboardSpec
from vizagent_dashboard.validation.browser import playwright_available, run_browser_checks
from vizagent_dashboard.validation.static import extract_build_manifest, validate_html

logger = logging.getLogger(__name__)


@click.group()
@click.version_option(__version__)
@click.option("--verbose", "-v", is_flag=True, help="输出调试日志")
def cli(verbose: bool) -> None:
    """从 CSV/XLSX 和 DashboardSpec 生成可验证的离线 HTML 大屏。"""

    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


@cli.command("inventory")
@click.option("--data", required=True, type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--output", type=click.Path(dir_okay=False, path_type=Path), default=Path("data.inventory.json"))
def inventory_command(data: Path, output: Path) -> None:
    """盘点数据文件，不调用模型。"""

    try:
        inventory, _ = inventory_file(data)
        _write_json(output, inventory.model_dump(mode="json"))
    except Exception as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(f"Inventory: {len(inventory.sheets)} sheet(s), {inventory.total_rows} row(s)")
    click.echo(f"Written: {output.resolve()}")


@cli.command("plan")
@click.option("--data", required=True, type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--requirement", default="", help="业务需求；确定性规划器不会调用外部模型")
@click.option("--theme", default=None, help="主题 ID")
@click.option("--page-mode", type=click.Choice(["single_page", "tabs"]), default=None)
@click.option("--output", type=click.Path(dir_okay=False, path_type=Path), default=Path("dashboard.spec.json"))
def plan_command(data: Path, requirement: str, theme: str | None, page_mode: str | None, output: Path) -> None:
    """根据所有 Sheet 生成覆盖完整的基础 DashboardSpec。"""

    try:
        inventory, sheets = inventory_file(data)
        spec = plan_dashboard(inventory, sheets, requirement, theme, page_mode)
        _write_json(output, spec.model_dump(mode="json"))
    except Exception as exc:
        raise click.ClickException(str(exc)) from exc
    click.echo(f"Spec: {sum(len(row.items) for row in spec.layout)} visual(s)")
    click.echo(f"Written: {output.resolve()}")


@cli.command("compile")
@click.option("--data", required=True, type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--spec", "spec_path", required=True, type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--theme", default=None, help="显式覆盖 Spec 主题")
@click.option("--deployment", type=click.Choice(["embedded", "cdn"]), default="embedded", show_default=True)
@click.option("--output", "output_dir", type=click.Path(file_okay=False, path_type=Path), default=Path("output"))
@click.option("--browser/--no-browser", default=False, help="使用 Playwright 执行浏览器门禁")
def compile_command(
    data: Path,
    spec_path: Path,
    theme: str | None,
    deployment: str,
    output_dir: Path,
    browser: bool,
) -> None:
    """使用现有 Spec 编译大屏。"""

    spec = _load_spec(spec_path)
    _execute_build(data, spec, theme, deployment, output_dir, browser)


@cli.command("validate")
@click.option("--data", required=True, type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--spec", "spec_path", required=True, type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--html", "html_path", required=True, type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--browser/--no-browser", default=False, help="使用 Playwright 执行浏览器门禁")
@click.option("--screenshot", type=click.Path(dir_okay=False, path_type=Path), default=None)
@click.option("--output", type=click.Path(dir_okay=False, path_type=Path), default=Path("validation.report.json"))
def validate_command(
    data: Path,
    spec_path: Path,
    html_path: Path,
    browser: bool,
    screenshot: Path | None,
    output: Path,
) -> None:
    """验证已有 HTML、Spec 和数据覆盖契约。"""

    try:
        inventory, _ = inventory_file(data)
        spec = _load_spec(spec_path)
        html_content = html_path.read_text(encoding="utf-8")
        report = validate_html(
            html_content,
            spec=spec,
            inventory=inventory,
            manifest=extract_build_manifest(html_content),
        )
        _attach_browser_report(report, html_path, browser, screenshot)
        _write_json(output, report)
    except click.exceptions.Exit:
        raise
    except click.ClickException:
        raise
    except Exception as exc:
        raise click.ClickException(str(exc)) from exc
    _echo_report(report)
    if not report["is_valid"]:
        raise click.exceptions.Exit(4)


@cli.command("build")
@click.option("--data", required=True, type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--requirement", default="", help="业务需求；不调用外部模型")
@click.option("--spec", "spec_path", default=None, type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--theme", default=None, help="显式覆盖 Spec 或自动主题")
@click.option("--page-mode", type=click.Choice(["single_page", "tabs"]), default=None)
@click.option("--deployment", type=click.Choice(["embedded", "cdn"]), default="embedded", show_default=True)
@click.option("--output", "output_dir", type=click.Path(file_okay=False, path_type=Path), default=Path("output"))
@click.option("--browser/--no-browser", default=False, help="使用 Playwright 执行浏览器门禁")
@click.option("--open/--no-open", "open_browser", default=False, help="成功后打开 HTML")
def build_command(
    data: Path,
    requirement: str,
    spec_path: Path | None,
    theme: str | None,
    page_mode: str | None,
    deployment: str,
    output_dir: Path,
    browser: bool,
    open_browser: bool,
) -> None:
    """盘点、规划、编译并验证大屏。"""

    try:
        inventory, sheets = inventory_file(data)
        if spec_path:
            spec = _load_spec(spec_path)
        else:
            spec = plan_dashboard(inventory, sheets, requirement, theme, page_mode)
        html_path, report = _execute_build(
            data,
            spec,
            theme if spec_path else None,
            deployment,
            output_dir,
            browser,
            inventory=inventory,
            sheets=sheets,
        )
    except click.ClickException:
        raise
    except Exception as exc:
        raise click.ClickException(str(exc)) from exc

    if open_browser and report["is_valid"]:
        click.launch(str(html_path.resolve()))


@cli.command("skill")
@click.argument("action", type=click.Choice(["install", "path"]))
def skill_command(action: str) -> None:
    """安装或查看 Claude Code Skill 定义。

    install：把打包的 SKILL.md 拷到 ~/.claude/skills/vizagent-dashboard/，重启 Claude Code 后可用 /vizagent-dashboard 触发。
    path：打印打包的 SKILL.md 路径。
    """

    src = _find_skill_md()
    if src is None:
        raise click.ClickException("未找到打包的 SKILL.md，请升级 vizagent-dashboard")
    if action == "path":
        click.echo(str(src))
        return
    dest = Path.home() / ".claude" / "skills" / "vizagent-dashboard" / "SKILL.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    click.echo(f"Skill 已安装: {dest}")
    click.echo("重启 Claude Code 后即可用 /vizagent-dashboard 触发。")


def _find_skill_md() -> Path | None:
    """定位打包的 SKILL.md：优先包内数据（wheel），回退仓库相对路径（editable/clone）。"""
    import contextlib

    with contextlib.suppress(ImportError, AttributeError, FileNotFoundError, TypeError):
        from importlib.resources import files

        pkg = Path(str(files("vizagent_dashboard") / "skill_assets" / "SKILL.md"))
        if pkg.exists():
            return pkg
    for base in Path(__file__).resolve().parents:
        cand = base / ".claude" / "skills" / "vizagent-dashboard" / "SKILL.md"
        if cand.exists():
            return cand
    return None


def _execute_build(
    data: Path,
    spec: DashboardSpec,
    theme: str | None,
    deployment: str,
    output_dir: Path,
    browser: bool,
    *,
    inventory: Any | None = None,
    sheets: dict[str, list[dict[str, Any]]] | None = None,
) -> tuple[Path, dict[str, Any]]:
    try:
        if inventory is None or sheets is None:
            inventory, sheets = inventory_file(data)
        compiled = compile_artifacts(
            spec,
            sheets,
            theme_id=theme,
            deployment_mode=deployment,
            inventory=inventory,
        )
        report = validate_html(
            compiled.html,
            spec=spec,
            inventory=inventory,
            manifest=compiled.manifest,
        )

        output_dir = output_dir.resolve()
        output_dir.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".vizagent-build-", dir=output_dir.parent) as temp_name:
            temporary = Path(temp_name)
            temporary_html = temporary / "output.html"
            temporary_html.write_text(compiled.html, encoding="utf-8")
            _attach_browser_report(report, temporary_html, browser, temporary / "screenshot.png" if browser else None)
            _write_json(temporary / "dashboard.spec.json", spec.model_dump(mode="json"))
            _write_json(temporary / "data.inventory.json", inventory.model_dump(mode="json"))
            _write_json(temporary / "validation.report.json", report)
            _write_json(temporary / "build-manifest.json", compiled.manifest)

            output_dir.mkdir(parents=True, exist_ok=True)
            for name in (
                "output.html",
                "dashboard.spec.json",
                "data.inventory.json",
                "validation.report.json",
                "build-manifest.json",
                "screenshot.png",
            ):
                source = temporary / name
                if source.exists():
                    os.replace(source, output_dir / name)
        html_path = output_dir / "output.html"
    except Exception as exc:
        if isinstance(exc, click.ClickException):
            raise
        raise click.ClickException(str(exc)) from exc

    click.echo(f"Generated: {html_path}")
    click.echo(f"Coverage: {'complete' if compiled.manifest['coverage_complete'] else 'incomplete'}")
    _echo_report(report)
    if not report["is_valid"]:
        raise click.exceptions.Exit(4)
    return html_path, report


def _attach_browser_report(
    report: dict[str, Any],
    html_path: Path,
    browser: bool,
    screenshot: Path | None,
) -> None:
    if browser:
        if not playwright_available():
            report["errors"].append("请求了浏览器验证，但 Playwright 未安装")
            report["issues"] = report["errors"] + report["warnings"]
            report["is_valid"] = False
            return
        browser_report = asyncio.run(
            run_browser_checks(
                str(html_path),
                screenshot_path=str(screenshot) if screenshot else None,
            )
        )
        report["browser"] = browser_report
        report["errors"].extend(browser_report.get("errors", []))
        report["warnings"].extend(browser_report.get("warnings", []))
        report["is_valid"] = report["is_valid"] and browser_report.get("is_healthy", False)
    else:
        report["browser"] = {"available": playwright_available(), "executed": False}
        report["warnings"].append("未执行浏览器门禁")
    report["issues"] = report["errors"] + report["warnings"]
    report["score"] = max(0, 100 - len(report["errors"]) * 15 - len(report["warnings"]) * 2)


def _load_spec(path: Path) -> DashboardSpec:
    try:
        return DashboardSpec.model_validate_json(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise click.ClickException(f"DashboardSpec 无效: {exc}") from exc


def _write_json(path: Path, value: Any) -> None:
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def _echo_report(report: dict[str, Any]) -> None:
    status = "PASS" if report["is_valid"] else "FAIL"
    click.echo(f"Validation: {status} ({report['score']}/100)")
    for issue in report.get("errors", [])[:8]:
        click.echo(f"  ERROR: {issue}")
    for issue in report.get("warnings", [])[:4]:
        click.echo(f"  WARN: {issue}")


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
