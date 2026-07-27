#!/usr/bin/env python3
"""通过 GitHub Git Data API 在服务端创建发布提交 + tag（绕开 git push）。

背景：本机网络环境下 github.com 常常不通（443 超时），但 api.github.com 可达。
当 git push 无法使用时，用本脚本通过 gh CLI 调 GitHub API 在服务端直接构造
提交和 tag，触发 release 工作流。

前提：
  - gh CLI 已登录（本机位于 C:\\Program Files\\GitHub CLI\\gh.exe，账号 Carloslee96，
    scopes 含 repo + workflow）
  - 待发布的文件改动已 commit 到 monorepo 的 skill/ 子目录

用法：
  python tools/publish_via_api.py 0.1.2
  python tools/publish_via_api.py 0.1.2 --files tools/publish.sh,pyproject.toml

不传 --files 时，自动同步 skill/ 下所有文件到远端（全量对齐）。
脚本需在 monorepo 的 skill/ 目录下运行（tools/ 的上一级即 skill 根）。
"""
from __future__ import annotations

import argparse
import base64
import json
import pathlib
import subprocess
import sys
import tempfile

GH = r"C:\Program Files\GitHub CLI\gh.exe"
OWNER_REPO = "Carloslee96/vizagent-dashboard"
# tools/publish_via_api.py 的上一级 = skill 根
SKILL_DIR = pathlib.Path(__file__).resolve().parent.parent

# 本地扫描时跳过的目录/后缀（构建产物等，不进公开仓库）
SKIP_DIRS = {"build", "dist", "__pycache__", ".pytest_cache", ".ruff_cache", "output"}


def api(method: str, endpoint: str, body: dict | None = None) -> dict:
    """调用 gh api，body 为 dict 时用 --input 传 UTF-8 JSON。"""
    args = [GH, "api", "-X", method, f"repos/{OWNER_REPO}/{endpoint}"]
    if body is not None:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
            json.dump(body, f, ensure_ascii=False)
            name = f.name
        args += ["--input", name]
    r = subprocess.run(args, capture_output=True, check=False)
    if r.returncode != 0:
        sys.stderr.write(f"API FAIL {method} {endpoint}\n{r.stderr.decode('utf-8','replace')}\n")
        sys.exit(1)
    return json.loads(r.stdout) if r.stdout.strip() else {}


def local_files() -> list[str]:
    """列出 skill/ 下 git 跟踪的文件相对路径（POSIX），与 subtree split 语义一致。

    用 git ls-files 而非 rglob，避免把未跟踪的本地文件（examples 试验数据、
    validation.report.json 等）误推到公开仓库。
    """
    r = subprocess.run(
        ["git", "ls-files"],
        cwd=SKILL_DIR, capture_output=True, check=False, text=True,
    )
    if r.returncode != 0:
        sys.stderr.write(f"git ls-files 失败: {r.stderr}\n")
        sys.exit(1)
    rels = [line.strip() for line in r.stdout.splitlines() if line.strip()]
    # 保险：跳过构建产物（即便被误跟踪）
    rels = [
        rel for rel in rels
        if not any(part in SKIP_DIRS for part in pathlib.PurePath(rel).parts)
    ]
    return rels


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("version", help="版本号，如 0.1.2")
    ap.add_argument("--files", help="逗号分隔的相对 skill/ 根的文件路径；省略则全量对齐")
    ap.add_argument("--message", help="提交信息", default=None)
    args = ap.parse_args()

    tag = args.version if args.version.startswith("v") else f"v{args.version}"

    # 1. 取远端 main HEAD + tree
    main_ref = api("GET", "git/refs/heads/main")
    main_sha = main_ref["object"]["sha"]
    main_commit = api("GET", f"git/commits/{main_sha}")
    base_tree = main_commit["tree"]["sha"]
    print(f"[1] main HEAD = {main_sha[:8]}  base_tree = {base_tree[:8]}")

    # 2. 决定要同步的文件
    if args.files:
        rels = [p.strip() for p in args.files.split(",") if p.strip()]
    else:
        rels = local_files()
        print(f"[2] 全量对齐模式，本地文件数 = {len(rels)}")

    # 3. 创建 blobs + tree entries
    entries = []
    for rel in rels:
        src = SKILL_DIR / rel
        if not src.exists():
            print(f"    跳过（本地不存在）: {rel}")
            continue
        content = src.read_bytes()
        blob = api("POST", "git/blobs", {"content": base64.b64encode(content).decode(), "encoding": "base64"})
        entries.append({"path": rel, "mode": "100644", "type": "blob", "sha": blob["sha"]})
    print(f"[3] 创建 {len(entries)} 个 blob")

    # 4. 新 tree
    new_tree = api("POST", "git/trees", {"base_tree": base_tree, "tree": entries})
    print(f"[4] new_tree = {new_tree['sha'][:8]}")

    # 5. 新 commit
    msg = args.message or f"release: vizagent-dashboard {tag}"
    new_commit = api("POST", "git/commits", {"message": msg, "tree": new_tree["sha"], "parents": [main_sha]})
    commit_sha = new_commit["sha"]
    print(f"[5] new_commit = {commit_sha[:8]}")

    # 6. 更新 main
    api("PATCH", "git/refs/heads/main", {"sha": commit_sha, "force": True})
    print("[6] main updated")

    # 7. tag object + ref
    tag_obj = api("POST", "git/tags", {
        "tag": tag,
        "message": f"vizagent-dashboard {tag}",
        "object": commit_sha,
        "type": "commit",
    })
    api("POST", "git/refs", {"ref": f"refs/tags/{tag}", "sha": tag_obj["sha"]})
    print(f"[7] tag {tag} created -> release workflow triggered")
    print(f"    https://github.com/{OWNER_REPO}/actions")


if __name__ == "__main__":
    main()
