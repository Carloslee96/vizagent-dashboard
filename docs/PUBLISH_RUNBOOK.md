# 发布操作手册 — vizagent-dashboard v0.1.0

> 面向 maintainer 的发布流程。读完这份，你应该能独立完成从「本地提交」到
> 「GitHub 上出现 Release」的全过程。每一步都写了「这步在干嘛」和「怎么确认做完了」。

## 🚀 快速路径（推荐）

不想懂细节？只需在 monorepo 任意目录跑一条命令：

```bash
bash skill/tools/publish.sh
```

它会自动完成：自检（lint+测试+构建）→ 拆分 skill/ 为根布局 → 推送到公开仓库
`Carloslee96/vizagent-dashboard` → 打 `v0.1.0` tag → 触发 GitHub Actions 自动建 Release。

**唯一需要你操作的一步**：首次推送时浏览器可能弹出 GitHub 登录授权，点一下即可。
（这台机器没有配置 GitHub 凭证，所以推送这一下必须由你来完成授权。）

跑完之后看：
- 构建进度：https://github.com/Carloslee96/vizagent-dashboard/actions
- Release：https://github.com/Carloslee96/vizagent-dashboard/releases

下面各节是脚本背后原理的展开，供排错或手动操作参考。

---


## 0. 先搞清楚三个概念

很多人混「提交」「推送」「发布」，这里一次说清：

| 动作 | 命令 | 效果 | 谁能看到 |
|------|------|------|----------|
| **提交 commit** | `git commit` | 把改动记进**本地**版本历史 | 只有你自己（在你电脑上） |
| **推送 push** | `git push` | 把本地提交**上传到 GitHub** | 任何能访问该仓库的人 |
| **发布 release** | GitHub 上打 tag + 写 Release 说明 | 在 GitHub Release 页面挂出一个**版本**，可附安装包 | 全网，是「正式发版」 |

类比：commit = 存进电脑草稿箱；push = 点「上传到网盘」；release = 正式「出版上架」。

**关键**：我们之前的 3 次 commit（`b7fb815` / `f841072` / `3641edf`）只在本地，GitHub 上还看不到。要发布必须先 push。

---

## 1. 发布前自检（必做）

在 `skill/` 目录下：

```bash
# 1.1 工作区干净（除 build/ 等忽略项外无未提交改动）
git status

# 1.2 测试全绿
python -m pytest tests/ -q -k "not e2e and not real"
# 期望：97 passed

# 1.3 lint 全绿
ruff check src/ tests/
# 期望：All checks passed

# 1.4 wheel 能构建
python -m build
# 期望：dist/ 下出现 vizagent_dashboard-0.1.0-py3-none-any.whl 与 .tar.gz
```

四项全过才继续。任何一项失败：**停止发布，先修。**

---

## 2. 确认版本号

- `pyproject.toml` 里 `version = "0.1.0"`
- `CHANGELOG.md` 有 `[0.1.0]` 段落
- `SBOM.md` 标注 v0.1.0

若要改版本号，三处同步改，commit 后再继续。

---

## 3. 推送到 GitHub（push）

```bash
# 3.1 看本地有哪些提交还没上传
git log --oneline origin/main..HEAD   # 或 origin/<当前分支>..HEAD

# 3.2 推送当前分支
git push -u origin feat/v2.1-5items-rollup
```

**确认做完**：去 GitHub 仓库网页，能看到这几次 commit 出现在分支历史里。

> 如果当前分支不是 main，发布前通常要发 PR 合并到 main。v0.1.0 的 tag 应打在 main 上。

---

## 4. 打 tag（标记版本点）

```bash
# 4.1 切到要发版的分支（通常是 main），确保拉到最新
git checkout main
git pull

# 4.2 打带注释的 tag
git tag -a v0.1.0 -m "vizagent-dashboard v0.1.0"

# 4.3 把 tag 推到 GitHub
git push origin v0.1.0
```

**确认做完**：GitHub 仓库 → 「Tags」能看到 `v0.1.0`。

> tag 一旦推送，会触发 `.github/workflows/release.yml`：自动构建 wheel/sdist、创建 GitHub Release、发布到 PyPI。所以**打 tag = 触发自动发布**，打之前确保 1、2、3 步都过了。

---

## 5. 创建 / 校对 GitHub Release

`release.yml` 会自动建一个 Release 并用 `generate_release_notes: true` 生成说明。

- 去 GitHub → Releases，找到 `v0.1.0`。
- 把自动生成的说明**替换为** `docs/RELEASE_NOTES_v0.1.0.md` 的内容（更精修）。
- 确认附件里有 `vizagent_dashboard-0.1.0-py3-none-any.whl` 与 `.tar.gz`。

**确认做完**：Release 页面正文是精修版，Assets 区有两个包。

---

## 6. PyPI 发布（可选，v0.1.0 可暂缓）

`release.yml` 已含 `pypa/gh-action-pypi-publish`，打 tag 时会自动发 PyPI。
若暂不想上 PyPI，先在 workflow 里注释掉该 step，避免误发。

发布后验证：

```bash
pip install vizagent-dashboard==0.1.0
vizagent --version
```

**确认做完**：https://pypi.org/project/vizagent-dashboard/ 显示 0.1.0。

---

## 7. 发布后清单

- [ ] GitHub Release 正文已替换为精修版
- [ ] Release Assets 含 wheel + sdist
- [ ] （若启用）PyPI 可装
- [ ] README 截图链接可正常显示（`docs/assets/*.png`）
- [ ] CHANGELOG `[0.1.0]` 日期改为实际发布日
- [ ] 在 HN / Reddit / V2EX / 掘金 等渠道按 `docs/launch-plan.md` 发布

---

## 回滚

- tag 推错了：`git tag -d v0.1.0 && git push origin :refs/tags/v0.1.0`（删除远端 tag）
- PyPI 发错了：**PyPI 不允许覆盖版本**，只能发 `0.1.1` 修正，并在 CHANGELOG 说明。
- GitHub Release 建错了：Release 页面可直接 Delete。
