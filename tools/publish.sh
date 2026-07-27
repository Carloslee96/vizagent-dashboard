#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# vizagent-dashboard 一键发布脚本
#
# 作用：把 monorepo 里的 skill/ 子目录，作为根目录推送到独立的公开仓库
#       Carloslee96/vizagent-dashboard，并打 v0.1.0 tag 触发 GitHub Actions
#       自动构建 wheel 并创建 GitHub Release。
#
# 全程不碰 SaaS 代码（app/、viz-agent-team/ 等不会进入公开仓库）。
#
# 用法：在 monorepo 根目录或任意子目录执行
#       bash skill/tools/publish.sh
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

VERSION="v0.1.0"
REMOTE_URL="https://github.com/Carloslee96/vizagent-dashboard.git"
SPLIT_BRANCH="dashboard-release-split"

# 定位 monorepo 根目录
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

echo "▶ [1/5] 发布前自检：lint + 单元测试 + wheel 构建"
( cd skill && ruff check src/ tests/ )
( cd skill && python -m pytest tests/ -q -k "not e2e and not real" )
( cd skill && rm -rf dist && python -m build >/dev/null )
echo "  ✓ 自检通过"

echo "▶ [2/5] 拆分 skill/ 为根布局分支（保留 skill 专属提交历史）"
git branch -D "$SPLIT_BRANCH" 2>/dev/null || true
git subtree split --prefix=skill -b "$SPLIT_BRANCH" >/dev/null
SPLIT_HEAD="$(git rev-parse "$SPLIT_BRANCH")"
echo "  ✓ 拆分完成 → $SPLIT_HEAD"

echo "▶ [3/5] 推送到公开仓库 main 分支"
echo "  （若弹出浏览器要求登录 GitHub，请完成授权；这是唯一需要你操作的一步）"
# 用 --force：subtree split 每次重算提交哈希，main 是单分支全量覆盖，
# 且公开仓库只有本项目的提交，不存在覆盖他人工作的风险。
git push --force "$REMOTE_URL" "$SPLIT_BRANCH:main"
echo "  ✓ 推送完成"

echo "▶ [4/5] 打 tag $VERSION 并推送（触发自动 Release）"
if git rev-parse "$VERSION" >/dev/null 2>&1; then
  echo "  ! 本地已存在 tag $VERSION，跳过创建。如需重打请先：git tag -d $VERSION"
else
  git tag -a "$VERSION" "$SPLIT_HEAD" -m "vizagent-dashboard $VERSION"
fi
git push "$REMOTE_URL" "$VERSION"
echo "  ✓ tag 已推送"

echo "▶ [5/5] 清理本地临时分支"
git branch -D "$SPLIT_BRANCH" 2>/dev/null || true

cat <<EOF

═══════════════════════════════════════════════════════════════
✅ 发布已触发！

接下来全自动发生（无需你操作）：
  1. GitHub Actions 的 release.yml 被触发（由 tag 推送）
  2. 它构建 wheel + sdist
  3. 用 docs/RELEASE_NOTES_v0.1.0.md 作为正文创建 GitHub Release，并附 wheel

查看进度：
  https://github.com/Carloslee96/vizagent-dashboard/actions
查看 Release：
  https://github.com/Carloslee96/vizagent-dashboard/releases

注：PyPI 发布在 v0.1.0 暂停（需先在 pypi.org 做一次性 Trusted Publisher 登记）。
═══════════════════════════════════════════════════════════════
EOF
