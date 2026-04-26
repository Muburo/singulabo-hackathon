#!/usr/bin/env python3
"""DR の生 Markdown から YAML カードを抽出して統一 YAML ファイルに保存。

使い方:
    python3 scripts/extract_yaml_cards.py persona-cards/R1-women-raw.md persona-cards/R1-women.yaml
"""

import re
import sys
from pathlib import Path

import yaml


def extract_cards(src_md: Path) -> list[dict]:
    """YAML カードを 2 段階戦略で抽出。

    Strategy 1: ```yaml ... ``` フェンスブロック
    Strategy 2: フェンスがなければ、Markdown 見出しで区切られた各セクションを
                走査し、"- id:" から始まる箇所以降を YAML として読む
    """
    content = src_md.read_text(encoding="utf-8")

    content = re.sub(r"[\ue000-\uf8ff]", "", content)
    content = re.sub(r"\s*citeturn\S+", "", content)
    content = re.sub(r'\s*entity\["[^"]*","[^"]*","[^"]*"\]', "", content)
    content = re.sub(r'(["\'])。\s*$', r"\1", content, flags=re.MULTILINE)

    blocks: list[str] = re.findall(r"```yaml\n(.*?)\n```", content, re.DOTALL)

    if not blocks:
        sections = re.split(r"^#{1,6}\s.*$", content, flags=re.MULTILINE)
        for section in sections:
            match = re.search(
                r"^- id:.*", section, flags=re.MULTILINE | re.DOTALL
            )
            if match:
                blocks.append(match.group(0))

    cards: list[dict] = []
    for i, block in enumerate(blocks, 1):
        try:
            parsed = yaml.safe_load(block)
        except yaml.YAMLError as e:
            print(f"  [WARN] block {i} の YAML パース失敗: {e}", file=sys.stderr)
            continue
        if isinstance(parsed, list):
            cards.extend(parsed)
        elif isinstance(parsed, dict):
            cards.append(parsed)
    return cards


def report(cards: list[dict]) -> None:
    print(f"抽出カード数: {len(cards)}")
    by_cat: dict[str, int] = {}
    for c in cards:
        cat = c.get("category", "unknown")
        by_cat[cat] = by_cat.get(cat, 0) + 1
    for cat, n in by_cat.items():
        print(f"  {cat}: {n}")


def main() -> None:
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <src.md> <dst.yaml>")
        sys.exit(1)
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    cards = extract_cards(src)
    report(cards)
    with dst.open("w", encoding="utf-8") as f:
        yaml.dump(cards, f, allow_unicode=True, sort_keys=False, width=200)
    print(f"\n保存先: {dst}")


if __name__ == "__main__":
    main()
