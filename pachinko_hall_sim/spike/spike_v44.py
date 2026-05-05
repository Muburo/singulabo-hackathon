"""
spike_v44.py — v4.5 Step 2: 物理エンジン（6 機種版）

v4.5 仕様（CLAUDE.md L1275-L1404 / docs/chatgpt-response-v4-4.md §2）の物理エンジン:
- 6 機種 MachineType ベタ書き（PURE_A / MIDDLE_45 / BAKURETSU_AT / ART_2010 / CHAIN_OKI / GOD_2000）
- 48 セル配分（各属性 125 人を 21+21+21+21+21+20 で 6 機種に）
- play 関数（chain_mode none/chain 分岐、v43 から maybe_switch 削除）
- 校正シミュレーション（1000 人 × 50 step → 機種別 hit_rate / target_return / payout 実測）

含めない（5/3 PM 以降）:
- 興奮量計算（compute_brain_delta）
- streak_bonus / chain_anxiety / disappointment_stress / miren_uchi_policy / afterglow
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from math import log, sqrt

import numpy as np

from spike_v44_personas import (
    ATTRIBUTES,
    Persona,
    generate_population,
)


# ============ MachineType（v4.5 仕様、ベタ書き SSoT）============

@dataclass
class MachineType:
    code: str
    display_name: str
    representatives: tuple[str, ...]
    chain_mode: str                              # "none" or "chain"
    p_initial_hit: float
    continue_prob: float
    payout_mean: float
    payout_std: float
    payout_cap: float
    stake: int
    bonus_excitement_multiplier: float
    chain_start_impact: float
    continuation_excitement_multiplier: float
    streak_gap_steps: int
    streak_onset: int
    streak_bonus_multiplier: float
    chain_anxiety_profile: str
    event_probs: dict = field(default_factory=dict)
    event_impacts: dict = field(default_factory=dict)
    # 派生
    payout_mu: float = 0.0
    payout_sigma: float = 0.0

    def __post_init__(self) -> None:
        # 対数正規の mu/sigma を mean/std から逆算
        m, s = self.payout_mean, self.payout_std
        if m > 0:
            sigma_sq = log(1.0 + (s * s) / (m * m))
            self.payout_sigma = sqrt(sigma_sq)
            self.payout_mu = log(m) - sigma_sq / 2.0
        # event_impacts に chain_start を chain_start_impact から自動同期（v43 と同じ）
        if "chain_start" not in self.event_impacts:
            self.event_impacts = dict(self.event_impacts)
            self.event_impacts["chain_start"] = self.chain_start_impact


MACHINES: list[MachineType] = [
    MachineType(
        code="NORMAL_BONUS",
        display_name="ノーマル・ボーナス型",
        representatives=("ジャグラー", "ハナハナ", "ニューパルサー", "クランキーコンドル"),
        chain_mode="none",
        p_initial_hit=0.215,
        continue_prob=0.00,
        payout_mean=1880, payout_std=880, payout_cap=7200,
        stake=400,
        bonus_excitement_multiplier=0.85,
        chain_start_impact=0.18,
        continuation_excitement_multiplier=0.00,
        streak_gap_steps=2, streak_onset=4, streak_bonus_multiplier=1.35,
        chain_anxiety_profile="none_or_low",
        event_probs={},
        event_impacts={},
    ),
    MachineType(
        code="LATE_4G_MASS",
        display_name="4号機中期・大量獲得型",
        representatives=("北斗の拳", "吉宗", "主役は銭形", "押忍！番長"),
        chain_mode="chain",
        p_initial_hit=0.055,
        continue_prob=0.60,
        payout_mean=3280, payout_std=2800, payout_cap=32000,
        stake=400,
        bonus_excitement_multiplier=1.35,
        chain_start_impact=0.45,
        continuation_excitement_multiplier=0.85,
        streak_gap_steps=1, streak_onset=5, streak_bonus_multiplier=1.15,
        chain_anxiety_profile="milestone_pressure",
        event_probs={
            "uwanose_light": 0.030, "uwanose_heavy": 0.0040,
            "tokka_light": 0.012, "tokka_heavy": 0.0015,
            "kakutei_engi": 0.0008,
        },
        event_impacts={
            "uwanose_light": 0.40, "uwanose_heavy": 1.05,
            "tokka_light": 0.70, "tokka_heavy": 1.25,
            "kakutei_engi": 1.40,
        },
    ),
    MachineType(
        code="BURST_AT_4G",
        display_name="4号機・爆裂AT型",
        representatives=("獣王", "サラリーマン金太郎", "アラジンA", "猛獣王"),
        chain_mode="chain",
        p_initial_hit=0.018,
        continue_prob=0.72,
        payout_mean=6600, payout_std=10800, payout_cap=80000,
        stake=400,
        bonus_excitement_multiplier=2.25,
        chain_start_impact=0.82,
        continuation_excitement_multiplier=0.80,
        streak_gap_steps=1, streak_onset=4, streak_bonus_multiplier=0.85,
        chain_anxiety_profile="entry_rare_betrayal_high",
        event_probs={
            "uwanose_light": 0.025, "uwanose_heavy": 0.0060,
            "tokka_light": 0.010, "tokka_heavy": 0.0030,
            "kakutei_engi": 0.0015,
        },
        event_impacts={
            "uwanose_light": 0.55, "uwanose_heavy": 1.25,
            "tokka_light": 0.80, "tokka_heavy": 1.55,
            "kakutei_engi": 1.75,
        },
    ),
    MachineType(
        code="SELF_TRIGGER_5G",
        display_name="5号機・自力契機型",
        representatives=("押忍！サラリーマン番長", "モンキーターン", "修羅の刻", "戦国乙女"),
        chain_mode="chain",
        p_initial_hit=0.030,
        continue_prob=0.83,
        payout_mean=2680, payout_std=2600, payout_cap=40000,
        stake=400,
        bonus_excitement_multiplier=1.70,
        chain_start_impact=0.55,
        continuation_excitement_multiplier=0.75,
        streak_gap_steps=1, streak_onset=7, streak_bonus_multiplier=0.75,
        chain_anxiety_profile="accident_entrance",
        event_probs={
            "uwanose_light": 0.055, "uwanose_heavy": 0.0060,
            "tokka_light": 0.035, "tokka_heavy": 0.0040,
            "kakutei_engi": 0.0010,
        },
        event_impacts={
            "uwanose_light": 0.45, "uwanose_heavy": 1.10,
            "tokka_light": 0.75, "tokka_heavy": 1.35,
            "kakutei_engi": 1.55,
        },
    ),
    MachineType(
        code="LOOP_CHAIN_5G",
        display_name="5号機・連チャン高継続型",
        representatives=("沖ドキ！", "リノ", "南国育ち"),
        chain_mode="chain",
        p_initial_hit=0.035,
        continue_prob=0.82,
        payout_mean=2480, payout_std=3000, payout_cap=48000,
        stake=400,
        bonus_excitement_multiplier=1.65,
        chain_start_impact=0.65,
        continuation_excitement_multiplier=0.95,
        streak_gap_steps=1, streak_onset=5, streak_bonus_multiplier=1.25,
        chain_anxiety_profile="no_guarantee_high",
        event_probs={
            "uwanose_light": 0.060, "uwanose_heavy": 0.018,
            "tokka_light": 0.010, "tokka_heavy": 0.0030,
            "kakutei_engi": 0.0010,
        },
        event_impacts={
            "uwanose_light": 0.55, "uwanose_heavy": 0.95,
            "tokka_light": 1.15, "tokka_heavy": 1.45,
            "kakutei_engi": 1.60,
        },
    ),
    MachineType(
        code="GOD_ORIGIN",
        display_name="初代GOD・別格型",
        representatives=("ミリオンゴッド 初代", "ゴールドXR"),
        chain_mode="chain",
        p_initial_hit=0.006,
        continue_prob=0.52,
        payout_mean=32000, payout_std=36000, payout_cap=88000,
        stake=400,
        bonus_excitement_multiplier=4.40,
        chain_start_impact=0.95,
        continuation_excitement_multiplier=0.70,
        streak_gap_steps=1, streak_onset=3, streak_bonus_multiplier=0.45,
        chain_anxiety_profile="god_afterglow",
        event_probs={
            "uwanose_light": 0.010, "uwanose_heavy": 0.0040,
            "tokka_light": 0.005, "tokka_heavy": 0.0020,
            "kakutei_engi": 0.0015,
        },
        event_impacts={
            "uwanose_light": 0.50, "uwanose_heavy": 1.35,
            "tokka_light": 0.90, "tokka_heavy": 1.75,
            "kakutei_engi": 2.10,
        },
    ),
]

MACHINES_BY_CODE: dict[str, MachineType] = {m.code: m for m in MACHINES}


# ============ 48 セル配分 ============

def assign_machines(personas: list[Persona], seed: int = 42) -> None:
    """各属性 125 人を 6 機種に 21+21+21+21+21+20 で配分（in-place）。

    v4.5 仕様（CLAUDE.md L1344-L1348）は各属性 125 人を固定前提。125 人以外を渡されたら
    assigned_machine が一部空文字のままになり、後段の run_calibration で KeyError になるため、
    入口で fail fast する。
    """
    counts = [21, 21, 21, 21, 21, 20]
    expected_per_attr = sum(counts)  # 125
    machine_codes = [m.code for m in MACHINES]
    rng = np.random.default_rng(seed)

    by_attr: dict[str, list[Persona]] = defaultdict(list)
    for p in personas:
        by_attr[p.attribute_code].append(p)

    for attr_code, members in by_attr.items():
        if len(members) != expected_per_attr:
            raise ValueError(
                f"v4.5 48-cell grid expects {expected_per_attr} personas per attribute, "
                f"got {len(members)} for {attr_code!r}"
            )
        order = list(range(len(members)))
        rng.shuffle(order)
        idx = 0
        for mcode, c in zip(machine_codes, counts):
            for k in order[idx:idx + c]:
                members[k].assigned_machine = mcode
            idx += c


# ============ PersonaState（動的状態、step ごとに更新）============

@dataclass
class PersonaState:
    """play() で書き換えられる動的状態。Persona（静的）から分離。"""
    cash: int
    chain_active: bool = False
    chain_step_count: int = 0
    tokka_zone_active: bool = False
    tokka_zone_remaining: int = 0
    miss_streak: int = 0
    win_streak: int = 0


def make_states(personas: list[Persona]) -> dict[str, PersonaState]:
    return {p.pid: PersonaState(cash=p.initial_cash) for p in personas}


# ============ play 関数（v43 の play から maybe_switch を削除）============

EVENT_ORDER = ("kakutei_engi", "tokka_heavy", "tokka_light", "uwanose_heavy", "uwanose_light")


def play(persona: Persona, state: PersonaState, mt: MachineType, rng: np.random.Generator) -> dict:
    """1 step の抽選 + chain_active 中の中間イベント抽選。"""
    state.cash -= mt.stake
    hit, payout = False, 0
    trigger_event = "none"
    uwanose_amount = 0
    chain_just_started = False
    tokka_zone_entry = False
    kakutei_engi = False
    chain_active_hit_step = False  # 中間イベント実効率の母数用

    if mt.chain_mode == "none":
        # PURE_A: 当たれば trigger_event = "chain_start"（連荘なし）
        if rng.random() < mt.p_initial_hit:
            hit = True
            payout = min(rng.lognormal(mt.payout_mu, mt.payout_sigma), mt.payout_cap)
            chain_just_started = True
            trigger_event = "chain_start"
        state.chain_active = False
        state.chain_step_count = 0
        state.tokka_zone_active = False

    else:
        if state.chain_active:
            cont_prob = 0.95 if state.tokka_zone_active else mt.continue_prob
            if rng.random() < cont_prob:
                hit = True
                payout = min(rng.lognormal(mt.payout_mu, mt.payout_sigma), mt.payout_cap)
                state.chain_step_count += 1
                chain_active_hit_step = True

                # 中間イベント抽選（chain_active hit step あたりの実効確率として運用）
                roll = rng.random()
                cumulative = 0.0
                for evt in EVENT_ORDER:
                    p = mt.event_probs.get(evt, 0.0)
                    if p <= 0:
                        continue
                    cumulative += p
                    if roll < cumulative:
                        trigger_event = evt
                        if evt == "kakutei_engi":
                            kakutei_engi = True
                            state.tokka_zone_active = True
                            state.tokka_zone_remaining = int(rng.integers(20, 40))
                            uwanose_amount = int(rng.choice([300, 500, 750]))
                        elif evt == "tokka_heavy":
                            tokka_zone_entry = True
                            state.tokka_zone_active = True
                            state.tokka_zone_remaining = int(rng.integers(20, 40))
                        elif evt == "tokka_light":
                            tokka_zone_entry = True
                            state.tokka_zone_active = True
                            state.tokka_zone_remaining = int(rng.integers(8, 18))
                        elif evt == "uwanose_heavy":
                            uwanose_amount = int(rng.choice([300, 500, 750, 1000]))
                        elif evt == "uwanose_light":
                            uwanose_amount = int(rng.choice([50, 100, 150, 200]))
                        break
            else:
                # 連荘終了
                state.chain_active = False
                state.chain_step_count = 0
                state.tokka_zone_active = False
                state.tokka_zone_remaining = 0
        else:
            if rng.random() < mt.p_initial_hit:
                hit = True
                payout = min(rng.lognormal(mt.payout_mu, mt.payout_sigma), mt.payout_cap)
                state.chain_active = True
                state.chain_step_count = 1
                chain_just_started = True
                trigger_event = "chain_start"

    # 特化ゾーンの残り step を 1 減らす
    if state.tokka_zone_active and state.tokka_zone_remaining > 0:
        state.tokka_zone_remaining -= 1
        if state.tokka_zone_remaining <= 0:
            state.tokka_zone_active = False

    state.cash += int(payout)
    if hit:
        state.miss_streak = 0
        state.win_streak += 1
    else:
        state.miss_streak += 1
        state.win_streak = 0

    return {
        "hit": hit,
        "payout": int(payout),
        "trigger_event": trigger_event,
        "uwanose_amount": uwanose_amount,
        "chain_just_started": chain_just_started,
        "tokka_zone_entry": tokka_zone_entry,
        "kakutei_engi": kakutei_engi,
        "chain_active_hit_step": chain_active_hit_step,
    }


# ============ 校正シミュレーション ============

def run_calibration(personas: list[Persona], n_steps: int = 50, seed: int = 1234) -> dict:
    """1000 人 × n_steps を走らせ、機種別の実測 stat を集計。"""
    for p in personas:
        if p.assigned_machine not in MACHINES_BY_CODE:
            raise ValueError(
                f"persona {p.pid} has invalid assigned_machine={p.assigned_machine!r}; "
                "did you call assign_machines() first?"
            )
    states = make_states(personas)
    rng = np.random.default_rng(seed)

    stats: dict[str, dict] = {
        m.code: {
            "n_personas": 0, "n_steps": 0, "n_hits": 0,
            "total_stake": 0, "total_payout": 0,
            "payouts": [],
            "events": defaultdict(int),
            "chain_active_hit_steps": 0,
        }
        for m in MACHINES
    }
    for p in personas:
        stats[p.assigned_machine]["n_personas"] += 1

    for p in personas:
        mt = MACHINES_BY_CODE[p.assigned_machine]
        s = states[p.pid]
        for _ in range(n_steps):
            r = play(p, s, mt, rng)
            agg = stats[p.assigned_machine]
            agg["n_steps"] += 1
            agg["total_stake"] += mt.stake
            agg["total_payout"] += r["payout"]
            if r["hit"]:
                agg["n_hits"] += 1
                agg["payouts"].append(r["payout"])
            if r["chain_active_hit_step"]:
                agg["chain_active_hit_steps"] += 1
            if r["trigger_event"] not in ("none", "chain_start"):
                agg["events"][r["trigger_event"]] += 1
    return stats


def summarize_calibration(stats: dict) -> None:
    """機種別の実測 vs ターゲット表示。

    targets は docs/chatgpt-response-v4-4.md §2 の YAML 仕様の値。payout_mean は payout_cap 適用前の
    raw lognormal 平均、target_return も raw 前提の理論回収率。payout_cap で頭打ちになる機種
    （特に GOD_2000、cap 220k vs mean 80k）では capped 実測 payout_mean / target_return が下回る。
    これは v4.5 物理エンジンの既知の calibration 課題で、5/3 PM の calibration step で
    raw mean 補正 or capped 想定の target_return 再計算で詰める。
    """
    targets = {
        "NORMAL_BONUS":    (0.215, 1.01,  4700),
        "LATE_4G_MASS":    (0.121, 0.99,  8200),
        "BURST_AT_4G":     (0.060, 1.00, 16500),
        "SELF_TRIGGER_5G": (0.150, 1.00,  6700),
        "LOOP_CHAIN_5G":   (0.163, 1.01,  6200),
        "GOD_ORIGIN":      (0.012, 0.99, 80000),
    }
    print(f"\n{'機種':<14} {'人数':>5} {'hit率':>9} (target) {'回収率':>9} (target) {'payout平均':>12} (target)")
    print("-" * 96)
    for m in MACHINES:
        s = stats[m.code]
        if s["n_steps"] == 0:
            continue
        hit_rate = s["n_hits"] / s["n_steps"]
        target_return = (s["total_payout"] / s["total_stake"]) if s["total_stake"] > 0 else 0
        payout_mean = (sum(s["payouts"]) / len(s["payouts"])) if s["payouts"] else 0
        thr, ttr, tpm = targets[m.code]
        print(f"{m.code:<14} {s['n_personas']:>5} "
              f"{hit_rate:>9.4f} ({thr:.4f}) "
              f"{target_return:>9.3f} ({ttr:.2f})   "
              f"{payout_mean:>12.0f} ({tpm:.0f})")

    # 中間イベント実効率（chain_active hit step あたり）
    print(f"\n{'機種':<14} {'event':<15} {'実測実効率':>12} (spec)")
    print("-" * 56)
    for m in MACHINES:
        s = stats[m.code]
        denom = s["chain_active_hit_steps"]
        if denom == 0:
            continue
        for evt in ("kakutei_engi", "tokka_heavy", "tokka_light", "uwanose_heavy", "uwanose_light"):
            spec = m.event_probs.get(evt, 0.0)
            if spec <= 0:
                continue
            count = s["events"].get(evt, 0)
            rate = count / denom
            print(f"{m.code:<14} {evt:<15} {rate:>12.5f} ({spec:.4f})")


def main() -> None:
    print("=== Step 1: 1000 人生成（spike_v44_personas）===")
    personas = generate_population(n_per_attr=125, seed=42)
    print(f"生成個体数: {len(personas)}")

    print("\n=== Step 2: 48 セル配分 ===")
    assign_machines(personas, seed=42)
    by_cell = defaultdict(int)
    for p in personas:
        by_cell[(p.attribute_code, p.assigned_machine)] += 1
    header = f"{'属性':<14} " + " ".join(f"{m.code:>13}" for m in MACHINES) + f"  {'計':>5}"
    print(header)
    print("-" * len(header))
    for attr in ATTRIBUTES:
        row_total = sum(by_cell[(attr.code, m.code)] for m in MACHINES)
        line = f"{attr.code:<14} "
        line += " ".join(f"{by_cell[(attr.code, m.code)]:>13}" for m in MACHINES)
        line += f"  {row_total:>5}"
        print(line)

    print("\n=== Step 3: 校正シミュレーション (1000 人 × 50 step) ===")
    stats = run_calibration(personas, n_steps=50, seed=1234)
    summarize_calibration(stats)

    print("\n注:")
    print("- target は docs/chatgpt-response-v4-4.md §2 の payout_cap 適用前の raw spec。")
    print("  capped 実測は payout_cap が効く機種（特に GOD_2000、cap 220k vs raw mean 80k）で")
    print("  raw target を下回る。raw mean 補正 or capped 想定の target_return 再計算は")
    print("  5/3 PM の calibration step で詰める想定（v4.5 既知課題）。")
    print("- ターゲット hit_rate は『初当たり + 連チャン継続』を含む実測ベース。")
    print("- n=50 step だと低頻度機種（GOD_2000 等）は実測がぶれる。本格 calibration は n_steps を増やす。")


if __name__ == "__main__":
    main()
