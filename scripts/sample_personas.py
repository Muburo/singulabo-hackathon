#!/usr/bin/env python3
"""169 cards から stratified sampling し、JSONL 出力するスクリプト。

カテゴリ別 prior（v3 R1/R2 DR 由来 + v4 仕様）から
interruptibility / sensory_gating_factor / stigma_barrier /
payday_sensitivity / time_cost_efficiency / path_dependency_score を派生し、
addiction_load を v4 §6.4 の式で計算して JSONL に出力する。

Usage:
    python3 scripts/sample_personas.py \
      --input persona-cards/all-cards-merged.yaml \
      --output pachinko_hall_sim/data/persona_cards.jsonl \
      --n 10 --seed 42
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent


# カテゴリ別 prior レンジ（uniform sampling の min, max）
# v3 CLAUDE.md の R1-R2 DR テーブルおよび v4 chatgpt-response-v4 §4.2 をベースに調整
CATEGORY_PRIORS: dict[str, dict[str, tuple[float, float]]] = {
    "不労所得・地主層": {
        "interruptibility": (0.90, 1.00),
        "sensory_gating_factor": (0.05, 0.15),
        "stigma_barrier": (0.60, 0.90),
        "payday_sensitivity": (0.05, 0.15),
        "time_cost_efficiency": (0.70, 0.90),
        "path_dependency_score": (0.15, 0.25),
    },
    "中年現役男性": {
        "interruptibility": (0.30, 0.50),
        "sensory_gating_factor": (0.60, 0.80),
        "stigma_barrier": (0.30, 0.50),
        "payday_sensitivity": (0.50, 0.70),
        "time_cost_efficiency": (0.40, 0.60),
        "path_dependency_score": (0.50, 0.60),
    },
    "依存症末期": {
        "interruptibility": (0.00, 0.10),
        "sensory_gating_factor": (0.90, 1.00),
        "stigma_barrier": (0.05, 0.20),
        "payday_sensitivity": (0.70, 0.90),
        "time_cost_efficiency": (0.10, 0.30),
        "path_dependency_score": (0.90, 1.00),
    },
    "精神疾患併発": {
        "interruptibility": (0.10, 0.30),
        "sensory_gating_factor": (0.70, 0.90),
        "stigma_barrier": (0.40, 0.70),
        "payday_sensitivity": (0.50, 0.80),
        "time_cost_efficiency": (0.20, 0.40),
        "path_dependency_score": (0.65, 0.75),
    },
    "主婦": {
        "interruptibility": (0.30, 0.50),
        "sensory_gating_factor": (0.60, 0.80),
        "stigma_barrier": (0.50, 0.80),
        "payday_sensitivity": (0.50, 0.70),
        "time_cost_efficiency": (0.40, 0.60),
        "path_dependency_score": (0.45, 0.55),
    },
    "OL・社会人女性": {
        "interruptibility": (0.40, 0.60),
        "sensory_gating_factor": (0.50, 0.70),
        "stigma_barrier": (0.40, 0.60),
        "payday_sensitivity": (0.40, 0.70),
        "time_cost_efficiency": (0.50, 0.70),
        "path_dependency_score": (0.45, 0.55),
    },
    "風俗・夜職系女性": {
        "interruptibility": (0.10, 0.30),
        "sensory_gating_factor": (0.70, 0.90),
        "stigma_barrier": (0.20, 0.40),
        "payday_sensitivity": (0.40, 0.60),
        "time_cost_efficiency": (0.30, 0.50),
        "path_dependency_score": (0.60, 0.70),
    },
    "女子大生・若年女性": {
        "interruptibility": (0.50, 0.70),
        "sensory_gating_factor": (0.60, 0.80),
        "stigma_barrier": (0.60, 0.80),
        "payday_sensitivity": (0.30, 0.50),
        "time_cost_efficiency": (0.50, 0.70),
        "path_dependency_score": (0.30, 0.40),
    },
    "年金生活高齢男性": {
        "interruptibility": (0.60, 0.80),
        "sensory_gating_factor": (0.50, 0.70),
        "stigma_barrier": (0.40, 0.60),
        "payday_sensitivity": (0.60, 0.80),
        "time_cost_efficiency": (0.50, 0.70),
        "path_dependency_score": (0.55, 0.65),
    },
    "年金生活高齢女性": {
        "interruptibility": (0.70, 0.90),
        "sensory_gating_factor": (0.30, 0.50),
        "stigma_barrier": (0.60, 0.80),
        "payday_sensitivity": (0.60, 0.80),
        "time_cost_efficiency": (0.60, 0.80),
        "path_dependency_score": (0.55, 0.65),
    },
    "退職前後・早期リタイア男性": {
        "interruptibility": (0.05, 0.20),
        "sensory_gating_factor": (0.80, 1.00),
        "stigma_barrier": (0.20, 0.40),
        "payday_sensitivity": (0.30, 0.50),
        "time_cost_efficiency": (0.20, 0.40),
        "path_dependency_score": (0.50, 0.60),
    },
}


# 案A 10人 sampling 仕様（CLAUDE.md「Persona Sampling」より）
SAMPLE_SPEC_10 = [
    ("不労所得・地主層", 1),
    ("中年現役男性", 1),
    ("依存症末期", 2),
    ("精神疾患併発", 1),
    ("主婦", 1),
    ("OL・社会人女性", 1),
    ("女子大生・若年女性", 1),
    ("年金生活高齢男性", 1),
    ("風俗・夜職系女性", 1),
]


def get_emotional(card: dict, key: str):
    """emotional_state.<key> を数値に正規化（"60-80" → 70 等）"""
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


def derive_attributes(card: dict, rng: random.Random) -> dict[str, float]:
    cat = card.get("_category_normalized", "unknown")
    priors = CATEGORY_PRIORS.get(cat)
    if priors is None:
        return {k: 0.5 for k in [
            "interruptibility", "sensory_gating_factor", "stigma_barrier",
            "payday_sensitivity", "time_cost_efficiency", "path_dependency_score",
        ]}
    return {k: round(rng.uniform(*v), 3) for k, v in priors.items()}


def compute_addiction_load(attrs: dict[str, float]) -> float:
    return round(
        max(0.0, min(1.0,
            0.45 * attrs["path_dependency_score"]
            + 0.20 * attrs["payday_sensitivity"]
            + 0.15 * (1.0 - attrs["interruptibility"])
            + 0.10 * attrs["sensory_gating_factor"]
            + 0.10 * attrs["time_cost_efficiency"]
        )),
        3,
    )


def to_persona_record(card: dict, rng: random.Random, category_index: dict[str, int]) -> dict:
    a = get_emotional(card, "arousal_0_100")
    d = get_emotional(card, "despair_0_100")
    cat = card.get("_category_normalized", "unknown")

    a_base = float(a) if a is not None else 50.0
    d_base = float(d) if d is not None else 50.0
    arousal_range = [max(0, int(a_base - 10)), min(100, int(a_base + 10))]
    despair_range = [max(0, int(d_base - 10)), min(100, int(d_base + 10))]

    attrs = derive_attributes(card, rng)
    addiction_load = compute_addiction_load(attrs)

    profile = card.get("profile") if isinstance(card.get("profile"), dict) else {}

    return {
        "persona_id": card.get("id", "?"),
        "category": cat,
        "category_id": category_index.get(cat, -1),
        "age_range": profile.get("age_range"),
        "occupation": profile.get("occupation"),
        "addiction_severity": profile.get("addiction_severity"),
        "arousal_base": a_base,
        "despair_base": d_base,
        "arousal_range": arousal_range,
        "despair_range": despair_range,
        "interruptibility": attrs["interruptibility"],
        "sensory_gating_factor": attrs["sensory_gating_factor"],
        "stigma_barrier": attrs["stigma_barrier"],
        "payday_sensitivity": attrs["payday_sensitivity"],
        "time_cost_efficiency": attrs["time_cost_efficiency"],
        "path_dependency_score": attrs["path_dependency_score"],
        "addiction_load": addiction_load,
        "_source_round": card.get("_round"),
        "_source_provider": card.get("_dr_provider"),
        "_inner_monologue_ja": card.get("inner_monologue_ja", ""),
    }


def stratified_sample(cards: list[dict], spec: list[tuple[str, int]], rng: random.Random) -> list[dict]:
    by_cat: dict[str, list[dict]] = {}
    for c in cards:
        cat = c.get("_category_normalized", "unknown")
        by_cat.setdefault(cat, []).append(c)

    sampled: list[dict] = []
    for cat, n in spec:
        candidates = by_cat.get(cat, [])
        if len(candidates) < n:
            print(f"  [WARN] {cat}: required {n} but only {len(candidates)} available", file=sys.stderr)
            n = len(candidates)
        if n == 0:
            continue
        sampled.extend(rng.sample(candidates, n))
    return sampled


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="persona-cards/all-cards-merged.yaml")
    ap.add_argument("--output", default="pachinko_hall_sim/data/persona_cards.jsonl")
    ap.add_argument("--n", type=int, default=10, help="現状 10 のみ対応（案A）")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    rng = random.Random(args.seed)

    in_path = ROOT / args.input
    out_path = ROOT / args.output
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with in_path.open(encoding="utf-8") as f:
        cards = yaml.safe_load(f)
    print(f"loaded {len(cards)} cards from {in_path}")

    if args.n == 10:
        spec = SAMPLE_SPEC_10
    else:
        raise SystemExit(f"--n {args.n} is not supported yet (only 10)")

    sampled = stratified_sample(cards, spec, rng)
    print(f"sampled {len(sampled)} cards")

    category_index = {cat: i for i, cat in enumerate(CATEGORY_PRIORS.keys())}
    records = [to_persona_record(c, rng, category_index) for c in sampled]

    with out_path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"wrote {len(records)} records to {out_path}")

    cnt = Counter(r["category"] for r in records)
    print("\n=== category distribution ===")
    for cat, n in cnt.most_common():
        print(f"  {cat:30s} {n}")

    print("\n=== addiction_load distribution ===")
    loads = sorted(r["addiction_load"] for r in records)
    print(f"  min={loads[0]:.3f}  max={loads[-1]:.3f}  median={loads[len(loads)//2]:.3f}")


if __name__ == "__main__":
    main()
