#!/usr/bin/env python3
"""Agent 学习站 — Markdown (Obsidian vault) → static HTML."""
from __future__ import annotations

import html
import os
import re
import shutil
from pathlib import Path

try:
    import markdown
except ImportError as e:
    raise SystemExit(
        "Missing dependency: markdown. Run: pip install -r requirements.txt"
    ) from e

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
DIST = ROOT / "dist"
STATIC = ROOT / "static"
SITE_TITLE = "Agent 学习站"

# Homepage featured cards (title, desc, content-relative target without .md, icon)
FEATURED = [
    ("学习驾驶舱", "本库总控台与进度总览", "00-地图/学习驾驶舱", "🛫"),
    ("Agent学习地图", "学习路线与阶段说明", "00-地图/Agent学习地图", "🗺️"),
    ("阅读打卡", "勾选驱动的阅读进度", "00-地图/阅读打卡", "✅"),
    ("概念", "心智模型与核心概念", "01-概念", "💡"),
    ("实践", "如何开始与最小练习", "02-实践", "🛠️"),
    ("官网索引", "三家官方资料对照入口", "03-资源/官网-Agent介绍/索引", "📚"),
    ("跨厂商", "Skills / MCP 等跨厂商对照", "03-资源/官网-Agent介绍/跨厂商", "🔗"),
]

NAV_SECTIONS = [
    ("入口", [
        ("欢迎", "欢迎"),
        ("学习驾驶舱", "00-地图/学习驾驶舱"),
        ("Agent学习地图", "00-地图/Agent学习地图"),
        ("阅读打卡", "00-地图/阅读打卡"),
    ]),
    ("01 概念", "01-概念"),
    ("02 实践", "02-实践"),
    ("03 资源", [
        ("延伸阅读", "03-资源/延伸阅读"),
        ("官网索引", "03-资源/官网-Agent介绍/索引"),
        ("收集进度", "03-资源/官网-Agent介绍/收集进度"),
    ]),
    ("OpenAI", "03-资源/官网-Agent介绍/OpenAI"),
    ("Anthropic", "03-资源/官网-Agent介绍/Anthropic-Claude"),
    ("Google Gemini", "03-资源/官网-Agent介绍/Google-Gemini"),
    ("跨厂商", "03-资源/官网-Agent介绍/跨厂商"),
    ("日记", "日记"),
]

WIKILINK_RE = re.compile(r"\[\[([^\]]+?)\]\]")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
TASK_OPEN = re.compile(
    r'<li>((?:<p>)?)\[ \]\s*', re.IGNORECASE
)
TASK_DONE = re.compile(
    r'<li>((?:<p>)?)\[x\]\s*', re.IGNORECASE
)


def slug_path(rel: str) -> str:
    """content-relative path (no .md) → URL path under dist."""
    rel = rel.replace("\\", "/").lstrip("/")
    if rel.endswith(".md"):
        rel = rel[:-3]
    return rel


def html_out_path(rel_no_ext: str) -> Path:
    return DIST / f"{slug_path(rel_no_ext)}.html"


def url_for(rel_no_ext: str) -> str:
    return "/" + slug_path(rel_no_ext) + ".html"


def rel_url(from_html: Path, to_rel_no_ext: str) -> str:
    """Relative href from one HTML file to another note."""
    target = html_out_path(to_rel_no_ext)
    return os.path.relpath(target, start=from_html.parent).replace("\\", "/")


def strip_frontmatter(text: str) -> tuple[str, dict]:
    meta: dict = {}
    m = FRONTMATTER_RE.match(text)
    if not m:
        return text, meta
    body = text[m.end() :]
    for line in m.group(1).splitlines():
        if ":" in line and not line.strip().startswith("-"):
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return body, meta


def collect_notes() -> dict[str, Path]:
    """Map content-relative path without .md → absolute Path."""
    notes: dict[str, Path] = {}
    for p in CONTENT.rglob("*.md"):
        rel = p.relative_to(CONTENT).as_posix()
        notes[rel[:-3]] = p
    return notes


def build_wikilink_index(notes: dict[str, Path]) -> dict[str, list[str]]:
    """Key variants → list of note keys (may be ambiguous)."""
    idx: dict[str, list[str]] = {}

    def add(key: str, note: str) -> None:
        key = key.replace("\\", "/")
        idx.setdefault(key, [])
        if note not in idx[key]:
            idx[key].append(note)

    for note in notes:
        add(note, note)
        add(note + ".md", note)
        parts = note.split("/")
        add(parts[-1], note)
        # suffix paths of length 2..n
        for i in range(1, len(parts)):
            add("/".join(parts[i:]), note)
    return idx


def resolve_wikilink(target: str, idx: dict[str, list[str]], current: str, folders: set[str] | None = None) -> str | None:
    target = target.strip().replace("\\", "/")
    if target.endswith(".md"):
        target = target[:-3]
    # heading/block refs: Note#heading — drop fragment for file resolve
    file_part, _, frag = target.partition("#")
    if not file_part:
        return None
    cands = idx.get(file_part) or idx.get(file_part + ".md")
    if not cands:
        # case-insensitive fallback
        lower = {k.lower(): v for k, v in idx.items()}
        cands = lower.get(file_part.lower())
    if not cands:
        # Folder wikilink e.g. [[日记]]
        folders = folders or set()
        if file_part in folders:
            resolved = file_part
            return resolved + ("#" + frag if frag else "")
        # basename folder match
        for f in folders:
            if f.endswith("/" + file_part) or f == file_part:
                return f + ("#" + frag if frag else "")
        return None
    if len(cands) == 1:
        resolved = cands[0]
    else:
        # Prefer same directory / longest common prefix with current
        cur_dir = "/".join(current.split("/")[:-1])
        best = None
        best_score = -1
        for c in cands:
            score = 0
            if cur_dir and c.startswith(cur_dir + "/"):
                score += 100
            # shared prefix length
            cp = os.path.commonprefix([c, current])
            score += len(cp)
            if score > best_score:
                best_score = score
                best = c
        resolved = best or cands[0]
    if frag:
        return resolved + "#" + frag
    return resolved


def rewrite_wikilinks(md: str, idx: dict[str, list[str]], current: str, from_html: Path, folders: set[str] | None = None) -> str:
    def repl(m: re.Match) -> str:
        raw = m.group(1)
        if "|" in raw:
            target, alias = raw.split("|", 1)
        else:
            target, alias = raw, raw
        # display: prefer alias; if alias is same as path, use basename
        display = alias.strip()
        resolved = resolve_wikilink(target, idx, current, folders)
        if not resolved:
            return f'<span class="wikilink-missing" title="未解析: {html.escape(target.strip())}">{html.escape(display)}</span>'
        file_part, _, frag = resolved.partition("#")
        href = rel_url(from_html, file_part)
        if frag:
            # Obsidian heading → rough HTML id (markdown toc style)
            hid = re.sub(r"\s+", "-", frag.strip().lower())
            href += "#" + html.escape(hid)
        if display == target.strip() and "/" in display:
            display = display.rsplit("/", 1)[-1]
        return f'<a href="{href}" class="wikilink">{html.escape(display)}</a>'

    return WIKILINK_RE.sub(repl, md)


def convert_task_lists(html_body: str) -> str:
    html_body = TASK_DONE.sub(
        r'<li class="task-list-item">\1<input type="checkbox" disabled checked> ',
        html_body,
    )
    html_body = TASK_OPEN.sub(
        r'<li class="task-list-item">\1<input type="checkbox" disabled> ',
        html_body,
    )
    return html_body


def md_to_html(md_text: str) -> str:
    # Protect mermaid fences → placeholder after convert
    mermaid_blocks: list[str] = []

    def save_mermaid(m: re.Match) -> str:
        mermaid_blocks.append(m.group(1))
        return f"\n\n@@@MERMAID{len(mermaid_blocks) - 1}@@@\n\n"

    md_text = re.sub(
        r"```mermaid\s*\n(.*?)```", save_mermaid, md_text, flags=re.DOTALL | re.IGNORECASE
    )

    body = markdown.markdown(
        md_text,
        extensions=[
            "markdown.extensions.tables",
            "markdown.extensions.fenced_code",
            "markdown.extensions.nl2br",
            "markdown.extensions.sane_lists",
            "markdown.extensions.smarty",
        ],
        output_format="html5",
    )
    body = convert_task_lists(body)

    for i, src in enumerate(mermaid_blocks):
        placeholder = (
            f'<div class="mermaid-placeholder" data-mermaid="1">'
            f"<strong>Mermaid 图示（源码）</strong>\n{html.escape(src.strip())}</div>"
        )
        body = body.replace(f"<p>@@@MERMAID{i}@@@</p>", placeholder)
        body = body.replace(f"@@@MERMAID{i}@@@", placeholder)
    return body


def note_title(path: Path, meta: dict, body_md: str) -> str:
    if meta.get("title"):
        return meta["title"]
    for line in body_md.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def folder_index_html(folder_key: str, notes: dict[str, Path], from_html: Path) -> str:
    """List child notes for a folder page."""
    items = []
    prefix = folder_key.rstrip("/") + "/"
    children = sorted(
        [k for k in notes if k.startswith(prefix) and "/" not in k[len(prefix) :]]
    )
    # also include nested one level for section folders
    if not children:
        children = sorted(
            k for k in notes if k.startswith(prefix)
        )
        # only direct files + one level?
        children = [k for k in children if k.count("/") == folder_key.count("/") + 1]
    for k in children:
        href = rel_url(from_html, k)
        items.append(f'<li><a href="{href}">{html.escape(Path(k).name)}</a></li>')
    if not items:
        return "<p>此目录暂无笔记。</p>"
    return "<ul>\n" + "\n".join(items) + "\n</ul>"


def nav_html(current_key: str | None, notes: dict[str, Path], from_html: Path) -> str:
    parts: list[str] = []
    for section in NAV_SECTIONS:
        title, spec = section
        parts.append(f'<div class="nav-section"><div class="nav-section-title">{html.escape(title)}</div>')
        if isinstance(spec, list):
            for label, key in spec:
                if key not in notes and not (CONTENT / key).is_dir():
                    # allow folder keys without index
                    if not any(n.startswith(key + "/") for n in notes) and key not in notes:
                        continue
                href = rel_url(from_html, key) if key in notes else (
                    rel_url(from_html, key) if html_out_path(key).exists() or True else "#"
                )
                # folder pages will be generated
                if key not in notes:
                    href = rel_url(from_html, key)
                cls = "active" if current_key == key else ""
                parts.append(f'<a class="{cls}" href="{href}">{html.escape(label)}</a>')
        else:
            # directory: list notes one level
            prefix = spec.rstrip("/") + "/"
            kids = sorted(
                k for k in notes if k.startswith(prefix) and "/" not in k[len(prefix) :]
            )
            for k in kids:
                label = Path(k).name
                href = rel_url(from_html, k)
                cls = "active" if current_key == k else ""
                parts.append(f'<a class="indent {cls}" href="{href}">{html.escape(label)}</a>')
        parts.append("</div>")
    return "\n".join(parts)


def page_shell(
    title: str,
    body: str,
    from_html: Path,
    notes: dict[str, Path],
    current_key: str | None = None,
    wide: bool = False,
    breadcrumb: str = "",
) -> str:
    css_href = os.path.relpath(DIST / "assets" / "style.css", start=from_html.parent).replace(
        "\\", "/"
    )
    home_href = os.path.relpath(DIST / "index.html", start=from_html.parent).replace("\\", "/")
    wrap_cls = "content-wrap wide" if wide else "content-wrap"
    nav = nav_html(current_key, notes, from_html)
    bc = f'<div class="breadcrumb">{breadcrumb}</div>' if breadcrumb else ""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · {SITE_TITLE}</title>
<link rel="stylesheet" href="{css_href}">
</head>
<body>
<div class="overlay" id="overlay" onclick="toggleNav()"></div>
<div class="layout">
<aside class="sidebar" id="sidebar">
  <div class="sidebar-brand">
    <a href="{home_href}">{SITE_TITLE}</a>
    <span class="sub">Obsidian 笔记静态站</span>
  </div>
  {nav}
</aside>
<main class="main">
  <div class="topbar">
    <button class="menu-btn" type="button" onclick="toggleNav()">菜单</button>
    <strong>{SITE_TITLE}</strong>
  </div>
  <div class="{wrap_cls}">
    {bc}
    {body}
    <footer class="footer">内容来自 Obsidian 库 · 由本地静态生成器构建</footer>
  </div>
</main>
</div>
<script>
function toggleNav(){{
  document.getElementById('sidebar').classList.toggle('open');
  document.getElementById('overlay').classList.toggle('show');
}}
</script>
</body>
</html>
"""


def build_homepage(notes: dict[str, Path]) -> None:
    out = DIST / "index.html"
    cards = []
    for title, desc, key, icon in FEATURED:
        if key in notes:
            href = rel_url(out, key)
        else:
            # folder page
            href = rel_url(out, key)
        cards.append(
            f'<a class="card" href="{href}">'
            f'<div class="icon">{icon}</div>'
            f"<h3>{html.escape(title)}</h3>"
            f"<p>{html.escape(desc)}</p></a>"
        )
    body = f"""
<div class="hero">
  <h1>{SITE_TITLE}</h1>
  <p>从 Obsidian 学习库生成的静态站点：驾驶舱、概念、实践与三家官网对照资料。</p>
</div>
<div class="cards">
{''.join(cards)}
</div>
<p><a href="{rel_url(out, '欢迎')}">欢迎页 →</a></p>
"""
    html_doc = page_shell(SITE_TITLE, body, out, notes, wide=True)
    out.write_text(html_doc, encoding="utf-8")


def build_folder_pages(notes: dict[str, Path], folders: set[str]) -> None:
    for folder in sorted(folders):
        out = html_out_path(folder)
        out.parent.mkdir(parents=True, exist_ok=True)
        listing = folder_index_html(folder, notes, out)
        title = Path(folder).name
        body = f"<h1>{html.escape(title)}</h1>\n{listing}"
        out.write_text(
            page_shell(title, body, out, notes, current_key=folder),
            encoding="utf-8",
        )


def build() -> None:
    if not CONTENT.is_dir():
        raise SystemExit(f"Missing content/: {CONTENT}")
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    assets = DIST / "assets"
    assets.mkdir()
    shutil.copy2(STATIC / "style.css", assets / "style.css")

    notes = collect_notes()
    idx = build_wikilink_index(notes)
    print(f"Notes: {len(notes)}")

    # folders that need index pages (featured + nav dirs)
    folders: set[str] = set()
    for _, _, key, _ in FEATURED:
        if key not in notes:
            folders.add(key)
    for _, spec in NAV_SECTIONS:
        if isinstance(spec, str) and spec not in notes:
            folders.add(spec)
    # all parent dirs of notes
    for k in notes:
        parts = k.split("/")
        for i in range(1, len(parts)):
            folders.add("/".join(parts[:i]))

    unresolved = 0
    total_links = 0

    for key, path in sorted(notes.items()):
        raw = path.read_text(encoding="utf-8")
        body_md, meta = strip_frontmatter(raw)
        title = note_title(path, meta, body_md)
        out = html_out_path(key)
        out.parent.mkdir(parents=True, exist_ok=True)

        total_links += len(WIKILINK_RE.findall(body_md))
        rewritten = rewrite_wikilinks(body_md, idx, key, out, folders)
        unresolved += rewritten.count("wikilink-missing")
        html_body = md_to_html(rewritten)
        # drop duplicate H1 if title matches first heading
        crumbs = []
        crumbs.append(
            f'<a href="{os.path.relpath(DIST / "index.html", start=out.parent).replace(chr(92), "/")}">首页</a>'
        )
        parts = key.split("/")
        for i in range(len(parts) - 1):
            fk = "/".join(parts[: i + 1])
            crumbs.append(
                f'<a href="{rel_url(out, fk)}">{html.escape(parts[i])}</a>'
            )
        crumbs.append(html.escape(title))
        breadcrumb = ' <span>/</span> '.join(crumbs)
        meta_line = ""
        if meta.get("updated") or meta.get("updated_at"):
            meta_line = f'<p class="page-meta">更新：{html.escape(meta.get("updated_at") or meta.get("updated", ""))}</p>'
        body = f"<h1>{html.escape(title)}</h1>\n{meta_line}\n{html_body}"
        out.write_text(
            page_shell(title, body, out, notes, current_key=key, breadcrumb=breadcrumb),
            encoding="utf-8",
        )

    build_folder_pages(notes, folders)
    build_homepage(notes)

    print(f"Wrote site → {DIST}")
    print(f"Wikilinks: {total_links} found, unresolved≈{unresolved}")


if __name__ == "__main__":
    build()
