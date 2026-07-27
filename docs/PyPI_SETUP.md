# PyPI 发布登记指南（Trusted Publisher）

> 面向 maintainer 与接手 AI。记录 vizagent-dashboard 在 PyPI 上的发布配置、登记步骤、
> 以及本机环境下的发布操作方式。读完应能独立完成 PyPI 发布与排错。

## 1. 当前状态（2026-07-27）

| 项 | 值 |
|---|---|
| PyPI 包名 | `vizagent-dashboard` |
| PyPI 页面 | https://pypi.org/project/vizagent-dashboard/ |
| 已发布版本 | `0.1.1`（v0.1.0 仅 GitHub，未上 PyPI） |
| 发布机制 | Trusted Publisher（OIDC），GitHub Actions 自动发布，**无需手工 token** |
| GitHub 仓库 | `Carloslee96/vizagent-dashboard` |
| 发布工作流 | `.github/workflows/release.yml`（tag `v*` 触发） |

**已登记的 Trusted Publisher 配置**（pypi.org → Account settings → Publishing）：

| 字段 | 值 |
|---|---|
| PyPI Project Name | `vizagent-dashboard` |
| owner | `Carloslee96` |
| repository | `vizagent-dashboard` |
| workflow filename | `release.yml` |
| environment | （空）|

## 2. 机制说明：什么是 Trusted Publisher

传统 PyPI 发布要在仓库里存一个 API token（长期凭证，有泄漏风险）。

Trusted Publisher（OIDC）不需要 token：GitHub Actions 发布时，PyPI 实时向 GitHub 验证
「这次发布是否来自 `Carloslee96/vizagent-dashboard` 仓库的 `release.yml` 工作流」。
匹配则放行。凭证不落盘，零泄漏面。

代价：**首次必须人工在 pypi.org 登记一次**（见第 3 节）。登记后全自动。

## 3. 登记步骤（已完成；重做或新包时参考）

1. 注册 https://pypi.org/account/register/ 账号。
2. Account settings → **Two-factor authentication** → 用认证器 App 开启 2FA（**发布者强制**），保存恢复码。
3. Account settings → **Publishing** → **Add a new pending publisher**，填第 1 节表里的 5 个字段。
4. 在 `release.yml` 启用 PyPI step（见第 5 节）。
5. 打一个新版本 tag 触发首发。

> 注意：pending publisher **不占包名**，首次实际发布才占名。若包名被他人抢注会失败，故尽早首发。

## 4. PyPI 版本规则

- **PyPI 不允许覆盖版本号**：已上传的 `0.1.1` 永远不能重传同号。
- 因此每次发布必须递增版本号（`0.1.1` → `0.1.2` → `0.2.0` …）。
- 版本号改三处：`pyproject.toml` 的 `version`、`SBOM.md` 标题与版本表、`CHANGELOG.md` 新增段。
- `release.yml` 的 `body_path` 指向对应版本号的 `docs/RELEASE_NOTES_vX.Y.Z.md`（每次发版新建一份）。

## 5. release.yml 的 PyPI 开关

```yaml
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
```

已启用。如需暂停 PyPI（仅发 GitHub Release），把这两行注释掉即可。工作流 `permissions` 已含
`id-token: write`（OIDC 必需）。

## 6. 发布操作

### 6.1 正常路径（github.com 可达时）

在 monorepo 根目录跑：

```bash
bash skill/tools/publish.sh
```

脚本流程：自检（lint+测试+构建）→ `git subtree split --prefix=skill` 拆成根布局 →
`--force` 推送到 `Carloslee96/vizagent-dashboard` main → 打 tag → 触发 release.yml。

> `publish.sh` 默认打 `v0.1.0` tag（脚本里 `VERSION` 变量）。发新版本前先改脚本里的
> `VERSION`，或改用手动步骤。

### 6.2 API 回退路径（github.com 不通时）

本机网络环境下 `github.com` 常常 443 超时，但 `api.github.com` 可达。此时 `git push`
不可用，用 API 在服务端直接构造提交 + tag：

```bash
# 在 monorepo 根目录
python skill/tools/publish_via_api.py 0.1.2
```

脚本通过 gh CLI 调 GitHub Git Data API：
1. 取远端 main HEAD + tree
2. 把 skill/ 下所有文件创建为 blobs
3. 构造新 tree → 新 commit（父=main HEAD）
4. 更新 main → 创建 tag 对象 → 创建 tag ref
5. tag ref 创建即触发 release.yml

**前提**：gh CLI 已登录（见第 7 节）。脚本不依赖 github.com，只走 api.github.com。

### 6.3 手动单文件更新（仅改个别文件时）

若只改一两个文件且 github.com 不通，可单独用 API 更新（参考 `publish_via_api.py` 的
blob/tree/commit 流程，或直接用 contents API 单文件 PUT）。历史上 security.yml 修复
即用此法。

## 7. 本机环境运维要点（接手 AI 必读）

- **gh CLI 不在 PATH**：位于 `C:\Program Files\GitHub CLI\gh.exe`。bash 里用全路径调用。
- **gh 登录状态**：账号 `Carloslee96`，token scopes 含 `gist, read:org, repo, workflow`。
  - 已 `gh auth setup-git`，git HTTPS 推送会用 gh token（但前提是 github.com 可达）。
  - 若 scopes 缺 `workflow`，推送 `.github/workflows/` 会被拒；用
    `gh auth refresh -h github.com -s workflow < /dev/null` 续权（会输出设备码，浏览器授权）。
- **网络**：`github.com` 常超时，`api.github.com` 稳定。git push 失败时走第 6.2 节 API 路径。
- **仓库结构**：dashboard 公开仓库采用**根布局**（`pyproject.toml`/`src/`/`README.md` 在根），
  不是 monorepo 的 `skill/` 子目录。workflow 里**没有** `working-directory: skill`。
- **subtree split**：`git subtree split --prefix=skill -b <branch>` 把 monorepo 的 skill/
  拆成根布局分支，保留 skill 专属提交历史，不碰 SaaS 代码（`app/`、`viz-agent-team/` 不入公开仓库）。
- **monorepo 无云端远端**：monorepo 本身没有 origin，只有 `origin-dashboard` 指向 dashboard 仓库。
  monorepo 本地提交不 push 到任何地方（项目约定 commit 不 push），不影响 skill 发布。

## 8. 验证发布是否成功

```bash
# GitHub Release
gh release view vX.Y.Z --repo Carloslee96/vizagent-dashboard

# release 工作流
gh run list --repo Carloslee96/vizagent-dashboard --workflow release.yml --limit 3

# PyPI
curl -s https://pypi.org/pypi/vizagent-dashboard/json | python -c "import sys,json;d=json.load(sys.stdin);print(d['info']['version'],list(d['releases'].keys()))"

# 实际可装
pip install --dry-run vizagent-dashboard==X.Y.Z
```

## 9. 排错速查

| 现象 | 原因 / 处理 |
|---|---|
| 推送 workflow 文件被拒 `without workflow scope` | gh token 缺 workflow scope → 第 7 节续权 |
| PyPI 步骤报 `failed to retrieve OIDC token` | Trusted Publisher 登记的 owner/repo/workflow 与实际不符 → 核对第 1 节 |
| PyPI 报 `File already exists` | 版本号已发布过 → 递增版本号（第 4 节） |
| `git push` 超时连不上 | github.com 不通 → 走第 6.2 节 API 路径 |
| release.yml 触发了但没建 Release | 检查 `body_path` 指向的文件是否存在该 tag 提交里 |
