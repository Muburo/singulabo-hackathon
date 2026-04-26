#!/usr/bin/env python3
"""全ラウンドの persona-cards YAML をマージし、集計レポートを生成。

Usage:
    python3 scripts/aggregate.py
"""

from __future__ import annotations

import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
CARDS_DIR = ROOT / "persona-cards"

FILES = [
    ("R1-women.yaml", "chatgpt", "R1"),
    ("R1-women-gemini.yaml", "gemini", "R1"),
    ("R2-elderly.yaml", "chatgpt", "R2"),
    ("R2-elderly-gemini.yaml", "gemini", "R2"),
    ("R3-extremes.yaml", "chatgpt", "R3"),
    ("R3-extremes-gemini.yaml", "gemini", "R3"),
]

CATEGORY_MAP = {
    "主婦": "主婦",
    "OL・社会人女性": "OL・社会人女性",
    "風俗・夜職系女性": "風俗・夜職系女性",
    "女子大生・若年女性": "女子大生・若年女性",
    "年金生活高齢男性": "年金生活高齢男性",
    "年金生活高齢女性": "年金生活高齢女性",
    "不労所得・地主系": "不労所得・地主層",
    "不労所得・社長引退系": "不労所得・地主層",
    "不労所得・役員系": "不労所得・地主層",
    "金銭プレッシャー希薄な趣味層": "不労所得・地主層",
    "地主・不労所得・経営者引退層": "不労所得・地主層",
    "不労所得・地主層": "不労所得・地主層",
    "不労所得・富裕層補強": "不労所得・地主層",
    "退職前後・早期リタイア男性": "退職前後・早期リタイア男性",
    "依存症末期": "依存症末期",
    "中年現役男性": "中年現役男性",
    "精神疾患併発": "精神疾患併発",
}


def load_all() -> list[dict]:
    cards: list[dict] = []
    for filename, provider, round_label in FILES:
        path = CARDS_DIR / filename
        if not path.exists():
            print(f"  [WARN] {path} not found, skip")
            continue
        with path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not data:
            continue
        for card in data:
            card["_dr_provider"] = provider
            card["_round"] = round_label
            raw_cat = card.get("category", "unknown")
            card["_category_normalized"] = CATEGORY_MAP.get(raw_cat, raw_cat)
        cards.extend(data)
        print(f"  loaded {len(data):3d} from {filename}")
    return cards


def get_emotional(card: dict, key: str):
    es = card.get("emotional_state", {})
    if not isinstance(es, dict):
        return None
    v = es.get(key)
    if isinstance(v, (int, float)):
        return v
    if isinstance(v, str):
        m = re.match(r"(\d+)\s*[-〜～]\s*(\d+)", v)
        if m:
            return (int(m.group(1)) + int(m.group(2))) / 2
        try:
            return int(v)
        except ValueError:
            return None
    return None


def aggregate_emotional(cards: list[dict]) -> dict:
    by_cat = defaultdict(lambda: {"arousal": [], "despair": []})
    for card in cards:
        cat = card.get("_category_normalized", "unknown")
        a = get_emotional(card, "arousal_0_100")
        d = get_emotional(card, "despair_0_100")
        if a is not None:
            by_cat[cat]["arousal"].append(a)
        if d is not None:
            by_cat[cat]["despair"].append(d)
    return by_cat


def fmt_stats(values: list) -> str:
    if not values:
        return "n=0"
    return (
        f"n={len(values):3d} | min={min(values):3.0f} | max={max(values):3.0f} | "
        f"median={statistics.median(values):3.0f} | mean={statistics.mean(values):3.0f}"
    )


def quadrant(a, d) -> str | None:
    if a is None or d is None:
        return None
    h_a = a >= 60
    h_d = d >= 60
    if h_a and h_d:
        return "高A高D"
    if h_a and not h_d:
        return "高A低D"
    if not h_a and h_d:
        return "低A高D"
    return "低A低D"


def aggregate_quadrants(cards: list[dict]) -> dict:
    by_cat_quad = defaultdict(Counter)
    for card in cards:
        cat = card.get("_category_normalized", "unknown")
        a = get_emotional(card, "arousal_0_100")
        d = get_emotional(card, "despair_0_100")
        q = quadrant(a, d)
        if q:
            by_cat_quad[cat][q] += 1
    return by_cat_quad


def report(cards: list[dict]) -> str:
    lines: list[str] = []
    lines.append("# Persona Cards 集計レポート — R1-R3 統合")
    lines.append("")
    lines.append("> 生成日: 2026-04-25 / シンギュラボハッカソン")
    lines.append(f"> 統合対象: {len(cards)} カード（R1-R3 各ラウンド × ChatGPT + Gemini）")

    lines.append("\n## 1. カード総数")
    lines.append("")
    lines.append("| Round | ChatGPT | Gemini | 計 |")
    lines.append("|-------|---------|--------|----|")
    by_rp = defaultdict(lambda: defaultdict(int))
    for c in cards:
        by_rp[c["_round"]][c["_dr_provider"]] += 1
    tcg = tg = 0
    for r in ["R1", "R2", "R3"]:
        cgpt = by_rp[r]["chatgpt"]
        gem = by_rp[r]["gemini"]
        lines.append(f"| {r} | {cgpt} | {gem} | {cgpt + gem} |")
        tcg += cgpt
        tg += gem
    lines.append(f"| **計** | **{tcg}** | **{tg}** | **{tcg + tg}** |")

    lines.append("\n## 2. カテゴリ分布（正規化後）")
    lines.append("")
    lines.append("| カテゴリ | カード数 | 構成比 |")
    lines.append("|---------|---------|-------|")
    by_cat = Counter(c["_category_normalized"] for c in cards)
    total = sum(by_cat.values())
    for cat, n in by_cat.most_common():
        lines.append(f"| {cat} | {n} | {n / total * 100:.1f}% |")

    lines.append("\n## 3. emotional_state 統計（カテゴリ別）")
    by_cat_emo = aggregate_emotional(cards)
    lines.append("\n### 3.1 Arousal（覚醒度）")
    lines.append("```")
    for cat, _ in by_cat.most_common():
        st = by_cat_emo[cat]["arousal"]
        lines.append(f"  {cat:30s} {fmt_stats(st)}")
    lines.append("```")
    lines.append("\n### 3.2 Despair（絶望度）")
    lines.append("```")
    for cat, _ in by_cat.most_common():
        st = by_cat_emo[cat]["despair"]
        lines.append(f"  {cat:30s} {fmt_stats(st)}")
    lines.append("```")

    lines.append("\n## 4. Arousal × Despair 4 象限分布")
    lines.append("")
    lines.append("閾値: Arousal 60 / Despair 60")
    lines.append("")
    lines.append("- 高A高D = パニック持続型（依存症末期・末期主婦の典型）")
    lines.append("- 高A低D = 万能感・興奮型（給料日・連チャン中）")
    lines.append("- 低A高D = 解離・燃え尽き型（うつ・後悔の麻痺）")
    lines.append("- 低A低D = 無感情・安定型（不労所得・地主層）")
    lines.append("")
    by_cat_quad = aggregate_quadrants(cards)
    lines.append("| カテゴリ | 高A高D | 高A低D | 低A高D | 低A低D | 計 |")
    lines.append("|---------|--------|--------|--------|--------|----|")
    quads = ["高A高D", "高A低D", "低A高D", "低A低D"]
    overall = Counter()
    for cat, _ in by_cat.most_common():
        qc = by_cat_quad[cat]
        row = [str(qc[q]) for q in quads]
        total_cat = sum(qc.values())
        lines.append(f"| {cat} | " + " | ".join(row) + f" | {total_cat} |")
        for q in quads:
            overall[q] += qc[q]

    overall_total = sum(overall.values())
    lines.append(f"| **全体** | **{overall['高A高D']}** | **{overall['高A低D']}** | **{overall['低A高D']}** | **{overall['低A低D']}** | **{overall_total}** |")

    lines.append("\n### 全体の 4 象限構成比")
    for q in quads:
        n = overall[q]
        pct = n / overall_total * 100 if overall_total else 0
        lines.append(f"- {q}: {n} ({pct:.1f}%)")

    lines.append("\n## 5. 極端値カード（実装の極限値の根拠）")
    extremes_h = []
    extremes_high_arousal = []
    extremes_low_a_high_d = []
    extremes_low_low = []
    for card in cards:
        a = get_emotional(card, "arousal_0_100")
        d = get_emotional(card, "despair_0_100")
        if a is None or d is None:
            continue
        if a >= 95 and d >= 95:
            extremes_h.append((card, a, d))
        elif a >= 95 and d <= 10:
            extremes_high_arousal.append((card, a, d))
        elif a <= 15 and d >= 95:
            extremes_low_a_high_d.append((card, a, d))
        elif a <= 30 and d <= 5:
            extremes_low_low.append((card, a, d))

    def card_row(card, a, d):
        return f"- `{card.get('id', '?')}` ({card['_round']}/{card['_dr_provider']}) {card['_category_normalized']} — A:{a:.0f} D:{d:.0f}"

    lines.append(f"\n### 5.1 両軸 95+ （Arousal × Despair 同時極大、デスクトップ・パニック持続）{len(extremes_h)} 枚")
    for card, a, d in extremes_h:
        lines.append(card_row(card, a, d))
    lines.append(f"\n### 5.2 高 Arousal × 低 Despair （万能感ピーク）{len(extremes_high_arousal)} 枚")
    for card, a, d in extremes_high_arousal[:10]:
        lines.append(card_row(card, a, d))
    if len(extremes_high_arousal) > 10:
        lines.append(f"  ... 他 {len(extremes_high_arousal) - 10} 枚")
    lines.append(f"\n### 5.3 低 Arousal × 高 Despair （燃え尽き・解離）{len(extremes_low_a_high_d)} 枚")
    for card, a, d in extremes_low_a_high_d:
        lines.append(card_row(card, a, d))
    lines.append(f"\n### 5.4 両軸極小 （無感情ベースライン、不労所得層）{len(extremes_low_low)} 枚")
    for card, a, d in extremes_low_low[:10]:
        lines.append(card_row(card, a, d))
    if len(extremes_low_low) > 10:
        lines.append(f"  ... 他 {len(extremes_low_low) - 10} 枚")

    lines.append("\n## 6. psychiatric_comorbidity 分布（R3 由来）")
    lines.append("")
    psych = Counter()
    for c in cards:
        p = c.get("profile", {}).get("psychiatric_comorbidity") if isinstance(c.get("profile"), dict) else None
        if p is not None:
            psych[str(p)] += 1
    lines.append("| 併発疾患 | カード数 |")
    lines.append("|---------|---------|")
    for p, n in psych.most_common(15):
        lines.append(f"| {p} | {n} |")

    lines.append("\n## 7. 集計の含意（persona pool 100 設計への示唆）")
    lines.append("")
    lines.append("### 7.1 4 象限のカバレッジ")
    lines.append("全 4 象限にカードが揃っており、シミュレーションで「比較動画として機能するコントラスト」が成立する。")
    lines.append("特に **高A高D（パニック持続）と 低A低D（無感情）の両極端**が埋まったことで、")
    lines.append("`stress × comeback_cue` 仮説の極限値テストが可能になった。")
    lines.append("")
    lines.append("### 7.2 不労所得・地主層のベースライン群としての成立")
    extr = (by_cat_quad.get("不労所得・地主層", Counter()))
    if extr:
        lines.append(f"`不労所得・地主層` カテゴリは合計 {sum(extr.values())} 枚で、")
        lines.append(f"うち低A低D が {extr.get('低A低D', 0)} 枚 / 高A高D が {extr.get('高A高D', 0)} 枚。")
        lines.append("「stress なしで打つ」反証サンプルが安定して取れた。")
    lines.append("")
    lines.append("### 7.3 次のステップ")
    lines.append("- `all-cards-merged.yaml` を `persona.yaml` 100 体生成のサンプリング元として使う")
    lines.append("- 各カテゴリの emotional_state 範囲を `arousal_range` / `despair_range` の上下限として転記")
    lines.append("- 極端値カード（5.1〜5.4）を seed_memory_ja の引用候補として活用")
    lines.append("- カテゴリ × 中年現役男性は `comeback_cue` の現役世代パラメータの根拠に使う")

    return "\n".join(lines)


def main() -> None:
    print("=== loading ===")
    cards = load_all()
    print(f"\n総カード数: {len(cards)}")

    merged_path = CARDS_DIR / "all-cards-merged.yaml"
    with merged_path.open("w", encoding="utf-8") as f:
        yaml.dump(cards, f, allow_unicode=True, sort_keys=False, width=200)
    print(f"\n=== merged YAML: {merged_path} ({merged_path.stat().st_size} bytes) ===")

    rpt = report(cards)
    rpt_path = ROOT / "reports" / "R1-R3-aggregation.md"
    rpt_path.parent.mkdir(exist_ok=True)
    with rpt_path.open("w", encoding="utf-8") as f:
        f.write(rpt)
    print(f"\n=== report: {rpt_path} ===")


if __name__ == "__main__":
    main()
