"""
draft.md → HTML（CSS 埋め込み）→ Chrome headless で PDF 化。

usage:
    python build_pdf.py [出力ファイル名（拡張子なし）]
    省略時は draft.pdf を吐く。
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent
DRAFT = ROOT / "draft.md"
HTML_OUT = ROOT / ".build.html"

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CSS = r"""
@page {
  size: A4;
  margin: 12mm 14mm 12mm 14mm;
}

html, body {
  font-family: "Hiragino Mincho ProN", "Yu Mincho", serif;
  font-size: 9.2pt;
  color: #1a1a1a;
  line-height: 1.45;
  margin: 0;
  padding: 0;
}

h1 {
  font-family: "Hiragino Sans", "Yu Gothic", sans-serif;
  font-size: 14pt;
  margin: 0 0 2pt 0;
  border-bottom: 1.5px solid #222;
  padding-bottom: 3pt;
}

h2 {
  font-family: "Hiragino Sans", "Yu Gothic", sans-serif;
  font-size: 11pt;
  margin: 8pt 0 3pt 0;
  border-left: 3px solid #c33;
  padding-left: 6pt;
  page-break-after: avoid;
}

h3 {
  font-family: "Hiragino Sans", "Yu Gothic", sans-serif;
  font-size: 9.7pt;
  margin: 6pt 0 2pt 0;
  color: #333;
  page-break-after: avoid;
}

p {
  margin: 2pt 0;
}

table {
  border-collapse: collapse;
  width: 100%;
  margin: 3pt 0 5pt 0;
  font-size: 8.4pt;
  page-break-inside: avoid;
}

th, td {
  border: 1px solid #bbb;
  padding: 2pt 5pt;
  vertical-align: top;
  text-align: left;
  line-height: 1.35;
}

th {
  background: #f0f0f0;
  font-family: "Hiragino Sans", sans-serif;
  font-weight: 600;
}

blockquote {
  border-left: 3px solid #c33;
  background: #faf4f4;
  margin: 4pt 0;
  padding: 4pt 8pt;
  font-size: 9pt;
}

blockquote p {
  margin: 1pt 0;
}

ul, ol {
  margin: 2pt 0;
  padding-left: 16pt;
}

li {
  margin: 1pt 0;
}

strong {
  font-family: "Hiragino Sans", sans-serif;
  font-weight: 600;
}

figure {
  margin: 4pt 0;
  page-break-inside: avoid;
  text-align: center;
}

img {
  max-width: 78%;
  display: block;
  margin: 3pt auto;
  page-break-inside: avoid;
}

figcaption, .figcaption {
  text-align: center;
  font-size: 8pt;
  color: #666;
  margin-top: 1pt;
}

hr {
  border: none;
  border-top: 1px solid #ccc;
  margin: 4pt 0;
}

/* 改ページ制御: \newpage を <div class="pagebreak"> に変換 */
.pagebreak {
  page-break-after: always;
}

/* 表の中の col 幅微調整 */
table.attr-table td:first-child { width: 28%; }
table.machine-table td:first-child { width: 24%; }
table.machine-table td:nth-child(2) { width: 38%; }

/* タイトルブロック */
.title-meta {
  font-size: 9.5pt;
  color: #444;
  margin-bottom: 8pt;
}
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
{css}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def md_to_html(md_text: str) -> str:
    # \newpage → 改ページ div
    md_text = md_text.replace("\\newpage", '<div class="pagebreak"></div>')

    html = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "attr_list"],
    )

    # 画像キャプション: <p><img ... alt="図 1: xxx"></p> を <figure> に
    def figure_repl(m: re.Match) -> str:
        alt = m.group("alt")
        src = m.group("src")
        return (
            f'<figure>'
            f'<img src="{src}" alt="{alt}">'
            f'<figcaption>{alt}</figcaption>'
            f'</figure>'
        )

    html = re.sub(
        r'<p><img alt="(?P<alt>[^"]+)" src="(?P<src>[^"]+)"\s*/?></p>',
        figure_repl,
        html,
    )

    return html


def render_pdf(output_stem: str) -> Path:
    md_text = DRAFT.read_text(encoding="utf-8")
    body = md_to_html(md_text)
    html = HTML_TEMPLATE.format(
        title="鶴子 — 解説資料", css=CSS, body=body
    )
    HTML_OUT.write_text(html, encoding="utf-8")

    pdf_path = ROOT / f"{output_stem}.pdf"
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        f"file://{HTML_OUT}",
    ]
    print("rendering:", " ".join(cmd[:2]), "...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("STDOUT:", res.stdout)
        print("STDERR:", res.stderr)
        raise SystemExit(f"chrome headless failed: {res.returncode}")
    return pdf_path


if __name__ == "__main__":
    stem = sys.argv[1] if len(sys.argv) > 1 else "draft"
    out = render_pdf(stem)
    if out.exists():
        size_kb = out.stat().st_size / 1024
        print(f"OK: {out} ({size_kb:.1f} KB)")
    else:
        raise SystemExit("PDF not generated")
