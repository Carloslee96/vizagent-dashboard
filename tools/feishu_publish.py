"""把一份 Markdown 发布到飞书 wiki 节点下（docx blocks）。

链路：取 token -> 建 wiki docx 节点 -> 解析 md 为飞书 blocks -> 逐个写入。
个人版飞书 drive 上传被禁，故图片不内嵌，改为文字链接块。

用法：
    FEISHU_APP_ID=xxx FEISHU_APP_SECRET=yyy \
        python tools/feishu_publish.py <md路径> [文档标题]

复用已有节点（追加 / 重发）：
    FEISHU_DOC_ID=<doc_id> python tools/feishu_publish.py <md路径>

前置条件见 docs/FEISHU_PUBLISH.md（凭证、权限、知识库成员）。
"""
import json, os, re, sys, urllib.request, urllib.error

# GBK 控制台兼容：避免打印中文符号崩溃
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

APP_ID = os.environ["FEISHU_APP_ID"]
APP_SECRET = os.environ.get("FEISHU_SECRET") or os.environ["FEISHU_APP_SECRET"]

# 维护者编辑这两项为目标知识库（见 docs/FEISHU_PUBLISH.md「定位知识库」）
SPACE_ID = "7656448196486400982"
PARENT_NODE = "GXaFwruWUi3brfkEg7eceSpJncb"

MD_PATH = sys.argv[1] if len(sys.argv) > 1 else None
DOC_TITLE = sys.argv[2] if len(sys.argv) > 2 else "vizagent-dashboard 介绍"
if not MD_PATH:
    print("用法: python tools/feishu_publish.py <md路径> [文档标题]"); raise SystemExit(1)


def http(method, url, body=None, headers=None):
    h = headers or {}
    data = None
    if body is not None:
        h.setdefault("Content-Type", "application/json; charset=utf-8")
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))


# ---------- token ----------
_, r = http("POST", "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
            {"app_id": APP_ID, "app_secret": APP_SECRET})
if r.get("code") != 0:
    print("token 失败:", json.dumps(r, ensure_ascii=False)); raise SystemExit(1)
token = r["tenant_access_token"]
auth = {"Authorization": f"Bearer {token}"}
print("[1] token OK")

# ---------- 建节点（或复用已有） ----------
doc_id = os.environ.get("FEISHU_DOC_ID")
if doc_id:
    print(f"[2] 复用节点 doc_id={doc_id}")
else:
    st, r = http("POST", f"https://open.feishu.cn/open-apis/wiki/v2/spaces/{SPACE_ID}/nodes",
                 {"obj_type": "docx", "parent_node_token": PARENT_NODE, "node_type": "origin", "title": DOC_TITLE},
                 headers=auth)
    if r.get("code") != 0:
        print("[2] create_node 失败:", json.dumps(r, ensure_ascii=False)); raise SystemExit(1)
    doc_id = r["data"]["node"]["obj_token"]
    print(f"[2] create_node OK  doc_id={doc_id}")
print(f"    URL: https://feishu.cn/docx/{doc_id}")


# ---------- markdown -> blocks ----------
def text_runs(text):
    """解析行内 `code` / **bold** / [t](url) 为 text_run elements。"""
    elements = []
    pattern = re.compile(r"`([^`]+)`|\*\*([^*]+)\*\*|\[([^\]]+)\]\(([^)]+)\)")
    pos = 0
    for m in pattern.finditer(text):
        if m.start() > pos:
            elements.append({"text_run": {"content": text[pos:m.start()], "text_element_style": {}}})
        if m.group(1) is not None:  # `code`
            elements.append({"text_run": {"content": m.group(1), "text_element_style": {"inline_code": True}}})
        elif m.group(2) is not None:  # **bold**
            elements.append({"text_run": {"content": m.group(2), "text_element_style": {"bold": True}}})
        else:  # [t](url)
            elements.append({"text_run": {"content": m.group(3),
                                          "text_element_style": {"link": {"url": m.group(4)}}}})
        pos = m.end()
    if pos < len(text):
        elements.append({"text_run": {"content": text[pos:], "text_element_style": {}}})
    if not elements:
        elements.append({"text_run": {"content": " ", "text_element_style": {}}})
    return elements


def text_block(text, block_type=2):
    return {"block_type": block_type,
            "text": {"elements": text_runs(text), "style": {}}}


def heading_block(text, level):
    # 飞书标题：block_type=2+level，字段名 heading{level}（非 text）
    return {"block_type": 2 + level,
            f"heading{level}": {"elements": text_runs(text), "style": {}}}


def code_block(code):
    return {"block_type": 14, "code": {"elements": text_runs(code), "style": {"language": 1}}}  # 1=PlainText


def parse_md(md):
    blocks = []
    lines = md.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        s = line.rstrip()

        # 代码块
        if s.startswith("```"):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].rstrip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # 跳过结束 ```
            blocks.append(code_block("\n".join(code_lines)))
            continue

        # 分隔线
        if re.match(r"^-{3,}$|^\*{3,}$|^_{3,}$", s):
            blocks.append({"block_type": 22, "divider": {}})
            i += 1
            continue

        # 标题
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            level = min(len(m.group(1)), 9)
            blocks.append(heading_block(m.group(2), level))
            i += 1
            continue

        # 引用 -> 用文本块 + 斜体（飞书直接建 quote block 不稳）
        if s.startswith("> "):
            quote_text = s[2:]
            runs = [{"text_run": {"content": c["text_run"]["content"],
                                  "text_element_style": {**c["text_run"]["text_element_style"], "italic": True}}}
                    for c in text_runs(quote_text)]
            blocks.append({"block_type": 2, "text": {"elements": runs, "style": {}}})
            i += 1
            continue

        # 无序列表
        m = re.match(r"^[-*]\s+(.*)$", s)
        if m:
            blocks.append({"block_type": 12, "bullet": {"elements": text_runs(m.group(1)), "style": {}}})
            i += 1
            continue

        # 有序列表
        m = re.match(r"^\d+\.\s+(.*)$", s)
        if m:
            blocks.append({"block_type": 13, "ordered": {"elements": text_runs(m.group(1)), "style": {}}})
            i += 1
            continue

        # 表格 -> 代码块（飞书 table block 复杂，个人版用代码块保留可读性）
        if s.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s|:-]+\|$", lines[i + 1].strip()):
            tbl = [s]
            i += 2  # 跳过分隔行
            while i < len(lines) and lines[i].rstrip().startswith("|"):
                tbl.append(lines[i].rstrip())
                i += 1
            blocks.append(code_block("\n".join(tbl)))
            continue

        # 空行跳过
        if not s.strip():
            i += 1
            continue

        # 普通段落
        blocks.append(text_block(s))
        i += 1
    return blocks


md = open(MD_PATH, encoding="utf-8").read()
blocks = parse_md(md)
print(f"[3] 解析 md 完成，共 {len(blocks)} 个 block")

# ---------- 逐个写入 + 容错定位 ----------
url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children"
total = len(blocks)
written = 0
failed = []
for idx, blk in enumerate(blocks):
    st, r = http("POST", url, {"children": [blk], "index": -1}, headers=auth)
    if r.get("code") != 0:
        failed.append((idx, blk.get("block_type"), r.get("code"), r.get("msg")))
        print(f"    [跳过] idx={idx} type={blk.get('block_type')} code={r.get('code')} {r.get('msg')}")
        continue
    written += 1
print(f"[4] 写入完成 {written}/{total} 成功，{len(failed)} 个跳过 -> https://feishu.cn/docx/{doc_id}")
if failed:
    print("    失败类型汇总:", sorted(set(f[1] for f in failed)))
