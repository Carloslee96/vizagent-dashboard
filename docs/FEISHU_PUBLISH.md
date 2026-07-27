# 飞书 Wiki 自动发布运维指南

把项目介绍 Markdown 自动发布到飞书知识库（docx blocks）。面向 maintainer 与接手 AI，记录凭证、权限、踩坑与发布流程。

- 发布脚本：`tools/feishu_publish.py`
- 脚本依赖：仅 Python 标准库（`urllib`/`json`/`re`），无需 pip 安装。

## 1. 前置条件

### 1.1 创建飞书自建应用

1. 打开 https://open.feishu.cn → 创建企业自建应用，拿到 **App ID**（`cli_` 开头）和 **App Secret**。
2. 「权限管理」开通以下 5 个 scope 并发布版本生效：
   - `wiki:wiki`（知识库读写）
   - `docx:document`（文档读写）
   - `docx:document:create`（建文档）
   - `drive:drive`（云空间）
   - `drive:file:upload`（文件上传，个人版实际被禁，但保留以免 scope 报错）

### 1.2 把应用加进知识库（关键，否则建节点报 131006）

应用默认只有读权限，**必须在目标知识库里把它加为「可编辑」成员**：

1. 浏览器打开目标知识库 wiki 链接。
2. 知识库「设置」→「成员管理」→「添加成员」→ 切到「**应用**」标签 → 搜索应用名 → 权限给「**可编辑**」。

> 飞书**个人版**（my.feishu.cn）若成员管理里找不到「应用」标签，说明个人版不支持给应用授权知识库，只能走手动导入 .md。企业版无此限制。

## 2. 定位知识库

脚本里两个常量需要改成你的目标知识库（`tools/feishu_publish.py` 顶部）：

```python
SPACE_ID = "7656448196486400982"      # 知识库 ID
PARENT_NODE = "GXaFwruWUi3brfkEg7eceSpJncb"  # 父节点 token（wiki URL 末段）
```

- `PARENT_NODE`：wiki 链接 `https://my.feishu.cn/wiki/<这一段>` 就是父节点 token。
- `SPACE_ID`：用 token 调 `GET /open-apis/wiki/v2/spaces/get_node?token=<父节点>&obj_type=wiki`，返回里的 `space_id`。

辅助探测脚本（验证凭证 + 拿 space_id）：`build/feishu_probe.py`（monorepo 内，不入开源包）。

## 3. 发布流程

```bash
# 一次性导出凭证（当前 shell 生效）
export FEISHU_APP_ID=cli_xxxxxxxx
export FEISHU_APP_SECRET=xxxxxxxxxxxxxxxx

# 发布：建新节点 + 写入整篇 md
python tools/feishu_publish.py vizagent-dashboard-飞书介绍.md "vizagent-dashboard 介绍"

# 复用已有节点（追加 / 重发，不新建）
FEISHU_DOC_ID=<doc_id> python tools/feishu_publish.py vizagent-dashboard-飞书介绍.md
```

成功输出：

```
[1] token OK
[2] create_node OK  doc_id=GeHBdMBMDoMHHExSGRpclc9Jn4g
[3] 解析 md 完成，共 65 个 block
[4] 写入完成 65/65 成功，0 个跳过 -> https://feishu.cn/docx/GeHBdMBMDoMHHExSGRpclc9Jn4g
```

## 4. Markdown → 飞书 block 映射

| Markdown | 飞书 block_type | 字段名 | 备注 |
|---|---|---|---|
| `#`/`##`/`###` | 3/4/5（heading1-3） | `heading{level}` | **字段名是 heading1/2/3，不是 text** |
| 段落 | 2（text） | `text` | |
| `- ` / `* ` | 12（bullet） | `bullet` | |
| `1. ` | 13（ordered） | `ordered` | |
| ``` ``` ``` | 14（code） | `code` | language=1（PlainText） |
| `> ` | 2（text + italic） | `text` | 直接建 quote(15) 不稳，降级为斜体文本 |
| `---` | 22（divider） | `divider: {}` | **必须带空 divider 字段** |
| 表格 | 14（code） | `code` | table block 太复杂，转代码块保留可读性 |
| `![](url)` | 2（text） | `text` | 个人版 drive 上传被禁，图片改文字链接 |
| `` `code` `` / `**bold**` / `[t](url)` | 行内 text_run style | — | inline_code / bold / link |

## 5. 踩坑记录（接手必读）

1. **131006 tenant needs edit permission**：应用没加进知识库或只读。→ 第 1.2 节，加为「可编辑」成员。
2. **1770001 invalid param（标题/分隔线失败）**：
   - 标题块字段名误用 `text`，飞书要求 `heading{level}`。
   - 分隔线块缺 `divider: {}` 字段。
3. **1061004 forbidden（drive 上传）**：个人版飞书禁止应用上传文件到云空间。→ 改走 wiki 建节点 + docx blocks 写入（本脚本即此路径）。
4. **99991672 scope 缺失**：→ 第 1.1 节补 scope 并发布版本。
5. **GBK 控制台 UnicodeEncodeError**：Windows 控制台打印 `✓` 等字符崩溃。→ 脚本已 `sys.stdout.reconfigure(encoding="utf-8")`，且打印避免特殊符号。
6. **批量写入失败定位难**：飞书 create-children 批量接口不告知哪个 block 非法。→ 脚本采用逐个写入 + 容错跳过日志，定位到具体 block_type。

## 6. 安全

- App Secret 通过环境变量传入，不入仓库。
- 若 Secret 曾在对话/日志中明文出现，发布完成后立即到 open.feishu.cn **重置 Secret**，重置不影响已发布文档。
- `SPACE_ID` / `PARENT_NODE` 不是机密，可入仓库；机密只有 App Secret。

## 7. 当前实例信息（维护者参考）

- App ID：`cli_aac788723ab89bd5`
- 知识库 wiki：https://my.feishu.cn/wiki/GXaFwruWUi3brfkEg7eceSpJncb
- 已发布文档：https://feishu.cn/docx/GeHBdMBMDoMHHExSGRpclc9Jn4g（vizagent-dashboard 介绍）
- 历史调试中残留的空/半空节点（XVyrdR1dMobh4hxSScqcvNDNn7c、Hmqkdj0QFoHcWtxOsdKcaQSIn7c、Z8bWdafFeoi4oDxBo3WcQC80nZe）应在飞书手动删除。
