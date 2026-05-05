"""
spike_v44_demo.py — v4.5 仮説検証デモ動画（Phase 1-6 統合、〜2 分）

横塚の仮説検証ストーリーを 1 本の mp4 で見せる。
構成（CLAUDE.md L1362-L1373）:
  Phase 1 (12s): 仮説提示
  Phase 2 (12s): 8 属性 × 6 機種 = 48 セル格子の説明
  Phase 3 (15s): シミュ実行（48 代表ドットが 50 step 早回しで光る）
  Phase 4 (30s): 最高幸福ランキング Top 5（カード切り替え）
  Phase 5 (25s): 最高ストレスランキング Top 5
  Phase 6 (15s): 仮説答え合わせ（C × 6 機種の Δ脳汁ヒートマップ）

合計: ~109 秒。fps=10。

簡易実装（5/3 PM の 5 つの新規概念は未統合）:
- 興奮量: hit_body + big_gain_log + dopamine_burst（pre_stress 効く）
- ストレス: tanh 飽和 + 慣性 0.72:0.28（v4.4 簡易）
- 幸福度: 0.65×Δ脳汁 + 0.25×脳汁 + 0.90×ストレス解放 + イベボーナス − 0.10×pre_stress

出力: outputs/spike_v44_demo.mp4
"""
from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass, field
from math import log10, tanh
from pathlib import Path

import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FFMpegWriter, FuncAnimation
from matplotlib.colors import LinearSegmentedColormap

from spike_llm_voice import generate_inner_voice
from spike_v44 import (
    MACHINES,
    MACHINES_BY_CODE,
    PersonaState,
    assign_machines,
    make_states,
    play,
)
from spike_v44_personas import ATTRIBUTES, Persona, generate_population

matplotlib.rcParams["font.family"] = ["Hiragino Sans", "Hiragino Maru Gothic Pro", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False


# ============ 属性別カラー ============

ATTR_COLOR = {
    "A_NEWBIE":   "#7FE07F",    # 新人 — 緑
    "B_REGULAR":  "#5A9BD4",    # 常連 — 青
    "C_CHASE":    "#E04545",    # 追い上げ — 赤（仮説対象）
    "D_AFTER5":   "#F0A030",    # 仕事帰り — 橙
    "E_LEISURE":  "#7CD4E0",    # 悠々自適 — 水色
    "F_SENIOR":   "#A878D4",    # シニア — 紫
    "G_BREATHER": "#F08FB8",    # 息抜き — ピンク
    "H_PRO":      "#E0D245",    # パチプロ — 黄
}
ATTR_DISPLAY = {a.code: a.display_name for a in ATTRIBUTES}
MACHINE_DISPLAY = {m.code: m.display_name for m in MACHINES}

# v4.6.3: 第三者向けの 1 行紹介（Phase 2 で機種ヘッダ下に表示）
# v4.6.15: SELF_TRIGGER_5G を「事故待ち・爆裂」に更新（横塚指示）
MACHINE_TAGLINE = {
    "NORMAL_BONUS":     "コツコツ・爆発なし",
    "LATE_4G_MASS":     "大量獲得・中毒性高",
    "BURST_AT_4G":      "入れば爆裂",
    "SELF_TRIGGER_5G":  "事故待ち・爆裂",
    "LOOP_CHAIN_5G":    "続くが保証なし",
    "GOD_ORIGIN":       "桁違い・別格",
}

# v4.6.11: 機種カテゴリのモデルとなる代表機種（横塚指示で更新）
MACHINE_EXAMPLES = {
    "NORMAL_BONUS":     "ジャグラー / ハナハナ / ニューパルサー",
    "LATE_4G_MASS":     "北斗の拳 / 吉宗 / 主役は銭形",
    "BURST_AT_4G":      "獣王 / アラジンA / 猛獣王",
    "SELF_TRIGGER_5G":  "サラリーマン番長 / 戦国乙女 / 修羅の刻",
    "LOOP_CHAIN_5G":    "沖ドキ！ / リノ / 南国育ち",
    "GOD_ORIGIN":       "ミリオンゴッド初代 / ゴールドXR",
}

# v4.6.15: 機種ごとの固有カラー（Phase machines で 6 色に色分け、横塚指示）
MACHINE_COLOR = {
    "NORMAL_BONUS":     "#7FE07F",  # 緑 — 伝統・安定
    "LATE_4G_MASS":     "#A878D4",  # 紫 — 中毒性・ゲーム性
    "BURST_AT_4G":      "#F0A030",  # 橙 — 爆裂・ハイリスク
    "SELF_TRIGGER_5G":  "#5A9BD4",  # 青 — 5号機・規制下
    "LOOP_CHAIN_5G":    "#7CD4E0",  # 水色 — 連チャン継続
    "GOD_ORIGIN":       "#E04545",  # 赤 — 別格・伝説
}


def clip(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


# ============ 収支表示ヘルパ（v4.6: 万円四捨五入、最終所持・払出表記は廃止）============

def format_balance(amount: int) -> str:
    """収支を「+N 万円 / -N 万円 / ±0」表示に整形（万円単位四捨五入）。"""
    man = round(amount / 10000)
    if man > 0:
        return f"+{man} 万円"
    if man < 0:
        return f"−{abs(man)} 万円"
    return "±0"


# v4.6: 内部 trigger_event 名を動画用日本語ラベルに対応させる辞書。
EVENT_JP = {
    "chain_start":  "初当たり",
    "kakutei_engi": "神光った！（確定演出）",
    "tokka_heavy":  "重い特化ゾーン突入",
    "tokka_light":  "軽い特化ゾーン突入",
    "uwanose_heavy": "大量上乗せ",
    "uwanose_light": "上乗せ",
    "none":         "—",
}


# ============ 興奮量・ストレス・幸福度（最小実装）============

def dopamine_sensitivity(p: Persona) -> float:
    return max(0.70, min(1.25, 0.75 + 0.45 * p.sensory_amplitude))


def compute_brain_delta(p: Persona, mt, event: dict, pre_stress: float, brain_arousal: float) -> float:
    payout = event["payout"]
    event_impact = mt.event_impacts.get(event["trigger_event"], 0.0)

    if event["chain_just_started"]:
        hit_body = 22.0 * mt.bonus_excitement_multiplier
    elif event["hit"]:
        hit_body = 12.0 * mt.continuation_excitement_multiplier
    else:
        hit_body = 0.0

    gain_signal = tanh(max(0, payout - mt.stake) / 7000.0)
    gain_body = 8.0 * gain_signal

    big_gain_log = max(0.0, log10(max(payout, 5000) / 5000.0)) if payout > 0 else 0.0
    big_gain_arousal = 10.0 * big_gain_log * mt.bonus_excitement_multiplier

    dopamine_burst = 35.0 * event_impact * (0.5 + 1.5 * pre_stress) * dopamine_sensitivity(p)

    decay = 0.05 * brain_arousal
    return hit_body + gain_body + big_gain_arousal + dopamine_burst - decay


def update_stress(p: Persona, state: PersonaState, event: dict, prev_stress: float) -> tuple[float, float]:
    """戻り値: (new_stress, stress_release)。stress_release は前 step からの解放量（正値）。"""
    net_loss = max(0, p.initial_cash - state.cash)
    target_stress = p.base_stress + (1 - p.base_stress) * tanh(net_loss / max(1000, p.personal_threshold))
    if event["hit"]:
        relief = 0.15 if event["chain_just_started"] else 0.05
        target_stress = max(p.stress_floor, target_stress - relief)
    new_stress = 0.72 * prev_stress + 0.28 * target_stress
    new_stress = clip(new_stress, p.stress_floor, 1.0)
    stress_release = max(0.0, prev_stress - new_stress)
    return new_stress, stress_release


def compute_happiness(brain_delta, brain_arousal, stress_release, pre_stress, event_impact):
    event_bonus = 5.0 * event_impact if event_impact > 0 else 0.0
    return (
        0.65 * brain_delta
        + 0.25 * brain_arousal
        + 0.90 * stress_release * 100.0
        + event_bonus
        - 0.10 * pre_stress * 50.0
    )


# ============ シミュレーション ============

@dataclass
class StepRecord:
    pid: str
    step: int
    machine: str
    attribute: str
    hit: bool
    payout: int
    trigger_event: str
    brain_delta: float
    brain_arousal: float
    stress: float
    pre_stress: float
    happiness: float
    chain_active: bool
    chain_step_count: int
    cash: int


def run_full_simulation(personas: list[Persona], n_steps: int = 50, seed: int = 1234) -> list[StepRecord]:
    states = make_states(personas)
    rng = np.random.default_rng(seed)

    arousal_by_pid: dict[str, float] = {p.pid: 0.0 for p in personas}
    stress_by_pid: dict[str, float] = {p.pid: p.base_stress for p in personas}

    records: list[StepRecord] = []
    for step in range(1, n_steps + 1):
        for p in personas:
            mt = MACHINES_BY_CODE[p.assigned_machine]
            s = states[p.pid]
            pre_stress = stress_by_pid[p.pid]
            event = play(p, s, mt, rng)
            brain_delta = compute_brain_delta(p, mt, event, pre_stress, arousal_by_pid[p.pid])
            brain_delta = max(0.0, brain_delta) if event["hit"] else max(-2.0, brain_delta)
            arousal_by_pid[p.pid] = clip(arousal_by_pid[p.pid] + brain_delta * 0.5, 0.0, 100.0)
            new_stress, stress_release = update_stress(p, s, event, pre_stress)
            stress_by_pid[p.pid] = new_stress
            event_impact = mt.event_impacts.get(event["trigger_event"], 0.0)
            happiness = compute_happiness(brain_delta, arousal_by_pid[p.pid],
                                          stress_release, pre_stress, event_impact)
            records.append(StepRecord(
                pid=p.pid, step=step, machine=p.assigned_machine, attribute=p.attribute_code,
                hit=event["hit"], payout=event["payout"], trigger_event=event["trigger_event"],
                brain_delta=brain_delta, brain_arousal=arousal_by_pid[p.pid],
                stress=new_stress, pre_stress=pre_stress, happiness=happiness,
                chain_active=s.chain_active, chain_step_count=s.chain_step_count, cash=s.cash,
            ))
    return records


# ============ 集計 ============

@dataclass
class PersonaSummary:
    pid: str
    attribute: str
    machine: str
    total_happiness: float
    max_brain_delta: float
    max_brain_step: int
    max_stress: float
    max_stress_step: int
    final_cash: int
    initial_cash: int
    net_balance: int          # final_cash - initial_cash
    peak_payout: int
    peak_event: str
    peak_pre_stress: float


def summarize_personas(personas: list[Persona], records: list[StepRecord]) -> list[PersonaSummary]:
    by_pid: dict[str, list[StepRecord]] = defaultdict(list)
    for r in records:
        by_pid[r.pid].append(r)

    summaries: list[PersonaSummary] = []
    p_by_pid = {p.pid: p for p in personas}
    for pid, rs in by_pid.items():
        p = p_by_pid[pid]
        total_happiness = sum(r.happiness for r in rs)
        peak_idx = max(range(len(rs)), key=lambda i: rs[i].brain_delta)
        peak = rs[peak_idx]
        max_stress_idx = max(range(len(rs)), key=lambda i: rs[i].stress)
        max_stress_r = rs[max_stress_idx]
        final_cash = rs[-1].cash
        summaries.append(PersonaSummary(
            pid=pid, attribute=p.attribute_code, machine=p.assigned_machine,
            total_happiness=total_happiness,
            max_brain_delta=peak.brain_delta, max_brain_step=peak.step,
            max_stress=max_stress_r.stress, max_stress_step=max_stress_r.step,
            final_cash=final_cash,
            initial_cash=p.initial_cash,
            net_balance=final_cash - p.initial_cash,
            peak_payout=peak.payout, peak_event=peak.trigger_event,
            peak_pre_stress=peak.pre_stress,
        ))
    return summaries


def attribute_stress_means(summaries: list[PersonaSummary]) -> dict[str, float]:
    """属性別 max_stress 平均（仮説検証: どの属性が最もストレスかかってるか）。"""
    by_attr: dict[str, list[float]] = defaultdict(list)
    for s in summaries:
        by_attr[s.attribute].append(s.max_stress)
    return {k: float(np.mean(v)) for k, v in by_attr.items()}


def attribute_aggregate_stats(
    summaries: list[PersonaSummary],
    records: list[StepRecord],
) -> dict[str, dict[str, float]]:
    """属性別 max ストレス / 平均ストレス / 平均 Δ脳汁（v4.6.1 仮説答え合わせ用）。"""
    by_attr_summary: dict[str, list[PersonaSummary]] = defaultdict(list)
    for s in summaries:
        by_attr_summary[s.attribute].append(s)
    by_attr_stress: dict[str, list[float]] = defaultdict(list)
    by_attr_brain: dict[str, list[float]] = defaultdict(list)
    for r in records:
        by_attr_stress[r.attribute].append(r.stress)
        if r.hit:
            by_attr_brain[r.attribute].append(r.brain_delta)
    out: dict[str, dict[str, float]] = {}
    for a in ATTRIBUTES:
        ss = by_attr_summary.get(a.code, [])
        if not ss:
            continue
        brains = by_attr_brain.get(a.code, [0.0])
        out[a.code] = {
            "max_stress":  float(np.mean([s.max_stress for s in ss])),
            "mean_stress": float(np.mean(by_attr_stress.get(a.code, [0.0]))),
            "mean_brain":  float(np.mean(brains)),
            "max_brain":   float(max(brains) if brains else 0.0),
            "peak_count":  int(sum(1 for v in brains if v >= 50)),
        }
    return out


def top_brain_peaks(records: list[StepRecord], top_n: int = 5) -> list[StepRecord]:
    """全 records から Δ脳汁ピーク Top N（同一 persona 重複なし）。"""
    seen: set[str] = set()
    out: list[StepRecord] = []
    for r in sorted(records, key=lambda x: -x.brain_delta):
        if r.pid in seen:
            continue
        seen.add(r.pid)
        out.append(r)
        if len(out) >= top_n:
            break
    return out


def factor_brain_means(records: list[StepRecord]) -> dict[str, dict[str, float]]:
    """要因別 Δ脳汁の束集計（v4.6.4: 横塚指摘『瞬間だけだと特化ゾーンが過小評価』）。

    各「契機」（chain_start / tokka_heavy / tokka_light / kakutei_engi）を発火点として、
    その契機が引き起こした連チャンの脳汁累積を契機に紐付ける。
    上乗せ（uwanose_*）と連チャン中の通常 hit は、現在の契機に積算する。

    結果として「特化ゾーン突入 1 回あたりの累積脳汁」が、突入後の連チャン分まで含まれる。
    """
    by_pid: dict[str, list[StepRecord]] = defaultdict(list)
    for r in records:
        by_pid[r.pid].append(r)

    factor_bursts: dict[str, list[float]] = defaultdict(list)

    def factor_label(rec: StepRecord) -> str:
        if rec.trigger_event == "chain_start":
            return f"{MACHINE_DISPLAY[rec.machine]} 初当たり"
        if rec.trigger_event in ("kakutei_engi", "tokka_heavy", "tokka_light"):
            return EVENT_JP[rec.trigger_event]
        return ""

    for pid, rs in by_pid.items():
        rs.sort(key=lambda x: x.step)
        current_label: str | None = None
        current_sum: float = 0.0
        for r in rs:
            if r.trigger_event in ("chain_start", "kakutei_engi",
                                   "tokka_heavy", "tokka_light"):
                # 既存の契機があれば確定して flush
                if current_label is not None:
                    factor_bursts[current_label].append(current_sum)
                current_label = factor_label(r)
                current_sum = r.brain_delta
            elif r.hit and current_label is not None:
                # 連チャン継続中の通常 hit / 上乗せは現契機に積算
                current_sum += r.brain_delta
            elif not r.chain_active and current_label is not None:
                # 連チャン終了（ハズレ確定）→ 現契機を flush
                factor_bursts[current_label].append(current_sum)
                current_label = None
                current_sum = 0.0
        # session 末尾の未確定契機を flush
        if current_label is not None:
            factor_bursts[current_label].append(current_sum)

    out: dict[str, dict[str, float]] = {}
    for label, bursts in factor_bursts.items():
        if not bursts:
            continue
        out[label] = {
            "mean":  float(np.mean(bursts)),
            "max":   float(max(bursts)),
            "count": len(bursts),
        }
    return out


def hypothesis_counter_evidence(
    records: list[StepRecord],
    brain_peaks: list[StepRecord],
) -> dict[str, object]:
    """仮説への反証材料を集計（v4.6.5: 横塚指示『自己成就回避』）。

    軸:
      1) Top 5 の中、中毒者でない個人は何人いるか
      2) 同機種（初代GOD）の属性別 max Δ脳汁の差（機種効果 vs 属性効果）
      3) 低ストレス（pre_stress < 0.3）でも +50 以上の脳汁ピークは何件起きたか
    """
    top5 = brain_peaks[:5]
    non_chase_in_top5 = [r for r in top5 if r.attribute != "C_CHASE"]

    god_max_by_attr: dict[str, float] = defaultdict(float)
    for r in records:
        if r.machine == "GOD_ORIGIN" and r.hit:
            if r.brain_delta > god_max_by_attr[r.attribute]:
                god_max_by_attr[r.attribute] = r.brain_delta

    low_stress_peaks = [r for r in records
                        if r.hit and r.pre_stress < 0.3 and r.brain_delta >= 50]

    god_max_top = max(god_max_by_attr.values()) if god_max_by_attr else 0.0
    god_max_min = min(god_max_by_attr.values()) if god_max_by_attr else 0.0

    return {
        "non_chase_in_top5_count": len(non_chase_in_top5),
        "non_chase_in_top5_sample": non_chase_in_top5[:1],   # 1 件サンプル
        "god_max_top": god_max_top,
        "god_max_min": god_max_min,
        "god_max_ratio": (god_max_top / god_max_min) if god_max_min > 0 else 0.0,
        "low_stress_peaks_count": len(low_stress_peaks),
        "low_stress_peaks_sample": low_stress_peaks[:1],
    }


def fmt_cash_jp(cash: int) -> str:
    """円数を「X 万 Y 千円」形式に整える（千円未満切り捨て、v4.6.14 横塚指示）。"""
    man = cash // 10000
    sen = (cash % 10000) // 1000
    if man > 0 and sen > 0:
        return f"{man} 万 {sen} 千円"
    if man > 0:
        return f"{man} 万円"
    return f"{max(1, sen)} 千円"


def gen_persona_story(p: Persona, r: StepRecord, rank: int = 0) -> list[str]:
    """属性別の個人ストーリー（v4.6.14 横塚指示で書き直し）。

    rank: 1/2/3 のいずれか（Phase 5 のランクに応じて借金額・所持金・文言が変わる）
    """
    cash = p.initial_cash
    threshold = p.personal_threshold
    if p.attribute_code == "C_CHASE":
        # 借金額をランクごとに段階化
        base_debt = int(threshold * 12 / 10000)
        if rank == 1:
            debt = max(150, min(280, int(base_debt * 1.9)))
        elif rank == 2:
            debt = max(100, min(220, int(base_debt * 1.4)))
        elif rank == 3:
            debt = max(60, min(180, base_debt))
        else:
            debt = min(250, max(80, base_debt))

        # v4.6.14: ランクごとに所持金の「物語」を作る（端数なし、第三者にも伝わる）
        if rank == 1:
            return [
                f"借金 約 {debt} 万円を抱える「中毒者」。",
                "今日も借金で工面した 10 万円を握りしめ、台の前へ。",
                "これ以上借金はしたくない。だが、もう打たずにはいられない…",
            ]
        elif rank == 2:
            return [
                f"借金 約 {debt} 万円を抱える「中毒者」。",
                "今月の家賃にも手をつけ、残ったのは 8 万円。",
                "止め時が分からないまま、台に賭ける…",
            ]
        elif rank == 3:
            return [
                f"借金 約 {debt} 万円を抱える「中毒者」。",
                "今月の生活費を含めた最後の 5 万円を握りしめ、台の前へ。",
                "重く追い詰められた気持ちのまま、台に賭ける…",
            ]
        else:
            return [
                f"借金 約 {debt} 万円を抱える「中毒者」。",
                f"今日も最後の {fmt_cash_jp(cash)} を握りしめ、台の前へ。",
                "もう止め時が分からない…",
            ]

    if p.attribute_code == "G_BREATHER":
        cash_jp = fmt_cash_jp(cash)
        # v4.6.14: 機種が GOD なら「ゴッドの衝撃が忘れられない」物語に
        if r.machine == "GOD_ORIGIN":
            return [
                f"家計から {cash_jp} を抜いてホールに来た「主婦」。",
                "かつてゴッドで体験した「一撃 5,000 枚」の衝撃が忘れられない。",
                "息抜きのつもりが、心はあの記憶を追いかけて…",
            ]
        return [
            f"家計から {cash_jp} を抜いてホールに来た「主婦」。",
            "日常から離れたい一心で、息抜きのつもりで打っていた。",
            "そんな時、思いがけず…",
        ]
    cash_jp = fmt_cash_jp(cash)
    if p.attribute_code == "D_AFTER5":
        return [
            f"仕事帰りの「アフター5層」。所持金 {cash_jp}。",
            "今日の業務ストレスを発散しに来店、限られた時間で打つ。",
            "残り時間も少ない中…",
        ]
    if p.attribute_code == "A_NEWBIE":
        return [
            f"はじめての店で慎重に打つ「初心者」。所持金 {cash_jp}。",
            "何が起きるか分からず、ドキドキしながら 1 G ずつ。",
            "そんな中、突然…",
        ]
    if p.attribute_code == "B_REGULAR":
        return [
            f"月数回通う「ライトユーザー」。所持金 {cash_jp}。",
            "特別な期待はせず、慣れた台で淡々と打っていた。",
            "そんな時…",
        ]
    if p.attribute_code == "E_LEISURE":
        return [
            f"経済的余裕がある「悠々自適」。所持金 {cash_jp}。",
            "勝ち負けにこだわらない、暇つぶしの静かな打ち方。",
            "そんな打ち方の最中…",
        ]
    if p.attribute_code == "F_SENIOR":
        return [
            f"退職後の「シニア」。所持金 {cash_jp}、年金で打ちに来る。",
            "朝から夕方まで、慣れた手つきで黙々と。",
            "そんな静かな時間に…",
        ]
    if p.attribute_code == "H_PRO":
        return [
            f"期待値で立ち回る「パチプロ」。所持金 {cash_jp}、高設定狙い。",
            "感情をコントロールしているはずだったが…",
        ]
    return [f"{ATTR_DISPLAY[p.attribute_code]}。所持金 {cash_jp}。"]


def chase_machine_brain_means(records: list[StepRecord]) -> dict[str, dict[str, float]]:
    """C_CHASE 属性の機種別 Δ脳汁平均（hit step のみ）。"""
    by_attr_machine: dict[tuple[str, str], list[float]] = defaultdict(list)
    for r in records:
        if r.hit:
            by_attr_machine[(r.attribute, r.machine)].append(r.brain_delta)
    out: dict[str, dict[str, float]] = defaultdict(dict)
    for (attr, mc), deltas in by_attr_machine.items():
        out[attr][mc] = float(np.mean(deltas)) if deltas else 0.0
    return out


# ============ 動画ビルド ============

FPS = 10
# v4.6.1: 半日/1日切り替え可能（横塚指示）
DURATION_MODE = "full_day"  # "half_day" or "full_day"
DURATION_LABELS = {
    "half_day": ("半日", 4000),
    "full_day": ("1日", 8000),
}
DURATION_NAME, TOTAL_G = DURATION_LABELS[DURATION_MODE]

# v4.6.1: 幸福度ランキング廃止、脳汁一点に絞る（横塚指示）
# v4.6.7: Phase 7 圧縮 + Phase 3 拡張で吹き出しの読み時間確保（横塚指示）
PHASES = [
    ("phase1", 15),         # 仮説提示 + 脳汁の定義（v4.6.14: 余韻 +2s）
    ("phase_attrs", 8),     # v4.6.13: 8 属性の人物紹介
    ("phase_machines", 8),  # v4.6.14: 6 機種の機種紹介（横塚指示）
    ("phase2", 11),         # 48 セル格子（一括表示 + 機種上の説明）
    ("phase3", 20),         # シミュ実行 + LLM 吹き出し
    ("phase4", 13),         # 属性別 脳汁ランキング
    ("phase5", 21),         # 個人 Top 3 詳細解説
    ("phase6", 8),          # 「機種の特徴」抽象化
    ("phase7", 8),          # 多面的検証（人 × 機種）
    ("phase8", 8),          # 結論（人 × 機種の合作）
    ("phase9", 32),         # v4.6.20: AI が生んだ 8 つの感情（Persona Reaction Probe 全 40 件）
    ("phase10", 33),        # v4.6.24: 説明スライド 8 秒 + 5 状況シーン × 5 秒
]


# ============ Phase 10: シーン台本（第三者向け、自然文の状況描写） ============

PHASE10_SCENARIO = {
    10: (
        "打ち始めて 10 ゲーム経過",
        "ホールはまだ静か、特に変わった様子はない。",
        "8 人それぞれ少し当てて少し外し、まだ流れは見えない。",
    ),
    20: (
        "20 ゲーム経過、近くの台で派手な演出",
        "周囲の台で、いつもより派手な演出が出た。",
        "自分の台はまだ静か。流れが来るか、それとも無関係か。",
    ),
    30: (
        "30 ゲーム経過、外れが続いて空気が重い",
        "ホール全体に、外れが続く沈んだ空気が漂う。",
        "手元の現金もそれぞれ削れている。続けるか、休むか、移るか、撤退するか。",
    ),
    40: (
        "40 ゲーム経過、周囲でざわつき",
        "周囲の台で、誰かが大きく当たったらしい。",
        "自分にも流れが来ているのか、それとも他人事なのか、判断が分かれる場面。",
    ),
    50: (
        "50 ゲーム経過、閉店間近",
        "閉店時刻が近づき、撤退する人もちらほら出てきた。",
        "今日の収支をどう締めくくるか、それぞれの判断がはっきり分かれる。",
    ),
}


def linguify_recent_pattern(recent_10: str) -> str:
    """直近 10 回の ○× を自然文に変換。"""
    cleaned = recent_10.replace("?", "")
    if not cleaned:
        return "直近の記録なし"
    n_total = len(cleaned)
    n_hit = cleaned.count("○")
    n_miss = cleaned.count("×")

    # 末尾の連続外れ/連続当たりを検出
    trailing_miss = 0
    for c in reversed(cleaned):
        if c == "×":
            trailing_miss += 1
        else:
            break
    trailing_hit = 0
    for c in reversed(cleaned):
        if c == "○":
            trailing_hit += 1
        else:
            break

    if n_hit == 0:
        return f"直近 {n_total} 回連続して外れ、まだ一度も当たっていない"
    if n_miss == 0:
        return f"直近 {n_total} 回連続して当たり、連チャン中"

    base = f"直近 {n_total} 回中、当たり {n_hit} 回・外れ {n_miss} 回"
    if trailing_miss >= 4:
        return f"{base}（直近 {trailing_miss} 連続外れ中）"
    if trailing_hit >= 2:
        return f"{base}（直近 {trailing_hit} 連続当たり中）"
    if trailing_miss >= 2:
        return f"{base}（最後の {trailing_miss} 回は外れ）"
    return base



# ============ Phase 9: Persona Reaction Probe 観察ページ ============

PHASE9_PERSONA_ORDER = [
    ("A_NEWBIE",   "P1_newbie"),
    ("B_REGULAR",  "P2_light"),
    ("C_CHASE",    "P3_chase"),
    ("D_AFTER5",   "P4_after5"),
    ("E_LEISURE",  "P5_leisure"),
    ("F_SENIOR",   "P6_senior"),
    ("G_BREATHER", "P7_breather"),
    ("H_PRO",      "P8_pro"),
]


def load_llm_sidecar() -> dict:
    """旧 sidecar データ（時間軸版）。後方互換のため残す。"""
    outputs_dir = Path(__file__).resolve().parents[1] / "outputs"
    candidates = sorted(outputs_dir.glob("llm_sidecar_*.json"))
    if not candidates:
        return {"data": []}
    with candidates[-1].open("r", encoding="utf-8") as f:
        return json.load(f)


def load_llm_situations() -> dict:
    """outputs/llm_situations_*.json をロード（状況軸版）。最新日付のものを採用。

    Phase 10 で使用。5 つの状況シーン × 8 代表 = 40 件の判断観察。
    """
    outputs_dir = Path(__file__).resolve().parents[1] / "outputs"
    candidates = sorted(outputs_dir.glob("llm_situations_*.json"))
    if not candidates:
        return {"scenes": []}
    with candidates[-1].open("r", encoding="utf-8") as f:
        return json.load(f)


# Phase 3.5: アクション色とラベル
PHASE3_5_ACTION_COLOR = {
    "continue": "#7AC8FF",  # 青寄り — 続行
    "chase":    "#E04545",  # 赤 — 取り返し
    "rest":     "#F0D040",  # 黄 — 休む
    "switch":   "#7FE07F",  # 緑 — 台移動
    "quit":     "#A0A0AC",  # グレー — 撤退
}
PHASE3_5_ACTION_LABEL = {
    "continue": "続行",
    "chase":    "追う",
    "rest":     "休む",
    "switch":   "台移動",
    "quit":     "撤退",
}


def load_persona_probe() -> dict:
    """outputs/persona_probe_*.json をロード。最新日付のものを採用。"""
    outputs_dir = Path(__file__).resolve().parents[1] / "outputs"
    candidates = sorted(outputs_dir.glob("persona_probe_*.json"))
    if not candidates:
        return {}
    latest = candidates[-1]
    with latest.open("r", encoding="utf-8") as f:
        data = json.load(f)
    # persona_id → list[scene_result]（場面順）に整形
    scene_order = [s["id"] for s in data.get("scenes", [])]
    by_persona: dict[str, list[dict]] = {}
    for r in data.get("results", []):
        pid = r["persona_id"]
        by_persona.setdefault(pid, []).append(r)
    # 場面順にソート
    for pid in by_persona:
        by_persona[pid] = sorted(
            by_persona[pid],
            key=lambda r: scene_order.index(r["scene_id"]) if r["scene_id"] in scene_order else 99,
        )
    return {
        "by_persona": by_persona,
        "personas": {p["id"]: p for p in data.get("personas", [])},
        "scenes": {s["id"]: s for s in data.get("scenes", [])},
    }



def phase_frame_ranges():
    """各 phase の (開始 frame, 終了 frame, 名前) を返す。"""
    out = []
    cursor = 0
    for name, secs in PHASES:
        n = secs * FPS
        out.append((name, cursor, cursor + n))
        cursor += n
    return out, cursor


def pick_representatives(personas: list[Persona]) -> list[Persona]:
    """各 (attribute, machine) セルから 1 人ずつ → 8 × 6 = 48 人。"""
    by_cell: dict[tuple[str, str], list[Persona]] = defaultdict(list)
    for p in personas:
        by_cell[(p.attribute_code, p.assigned_machine)].append(p)
    reps = []
    for a in ATTRIBUTES:
        for m in MACHINES:
            members = by_cell[(a.code, m.code)]
            if members:
                # z 中央値の人を代表に（極端な z は避ける）
                members_sorted = sorted(members, key=lambda x: abs(x.z))
                reps.append(members_sorted[0])
    return reps


# ============ Phase 3 ポップアップ吹き出し（v4.6 LLM 統合）============

# 機種コード → 動画用の機種ラベル（spike_llm_voice.py 用）
MACHINE_VOICE_LABEL = {
    "NORMAL_BONUS":     "ノーマル機（コツコツ）",
    "LATE_4G_MASS":     "4号機後期（大量獲得）",
    "BURST_AT_4G":      "4号機・爆裂AT",
    "SELF_TRIGGER_5G":  "5号機・自力契機",
    "LOOP_CHAIN_5G":    "5号機・連チャン高継続",
    "GOD_ORIGIN":       "初代GOD（別格）",
}

# 属性コード → カテゴリ + 性別分布 + 年齢範囲（v4.6.8: バリエーション化、横塚指示）
# male_prob = 男性が選ばれる確率。残りは女性。
# age_range = (min, max)、その範囲から rng で 1 値サンプル
# category: プロンプトに直接入る属性ラベル（中立な表現）
# life_themes: その属性が普段から考えがちなテーマのヒント（プロンプトでバリエーション源として使う）
VOICE_PROFILE = {
    "A_NEWBIE": {
        "category": "パチスロ初心者", "male_prob": 0.55, "age_range": (20, 30),
        "life_themes": "初めて触る台への戸惑い、新鮮な驚き、友達への自慢、SNS への投稿欲、初めての勝ち負けの感覚",
    },
    "B_REGULAR": {
        "category": "ライトユーザー", "male_prob": 0.65, "age_range": (28, 45),
        "life_themes": "週末の小さな楽しみ、軽い遊び感覚、無理しない範囲、たまの息抜き、明日の仕事のこと",
    },
    "C_CHASE": {
        "category": "中毒者", "male_prob": 0.75, "age_range": (30, 55),
        "life_themes": "止められないという葛藤、家族への後ろめたさ、生活との衝突、勝てば全部解決という願望、自分でも止め時が分からない感覚",
    },
    "D_AFTER5": {
        "category": "仕事帰りのサラリーマン／OL", "male_prob": 0.65, "age_range": (28, 45),
        "life_themes": "今日の仕事の疲れ、上司への愚痴、終電までの時間、仕事のストレス発散、明日への活力",
    },
    "E_LEISURE": {
        "category": "経済的余裕のあるシニア層", "male_prob": 0.55, "age_range": (50, 65),
        "life_themes": "お金よりも刺激そのもの、ゆったり楽しむ余裕、趣味としての一打、孫や家族の話題、時間の使い方",
    },
    "F_SENIOR": {
        "category": "年金生活のシニア", "male_prob": 0.55, "age_range": (65, 78),
        "life_themes": "今日の予定、健康のこと、若い頃の思い出、午後のお茶、近所の話、ささやかな楽しみ",
    },
    "G_BREATHER": {
        "category": "主婦", "male_prob": 0.0, "age_range": (35, 55),
        "life_themes": "家事からの解放感、夕飯の支度、子供のこと、夫の帰りまでの時間、自分だけの時間、お小遣いの範囲",
    },
    "H_PRO": {
        "category": "パチプロ", "male_prob": 0.85, "age_range": (25, 42),
        "life_themes": "期待値計算、収支管理、台選びの理屈、感情よりロジック、長期目線、月の数字",
    },
}


@dataclass
class VoiceBubble:
    """Phase 3 で表示するポップアップ吹き出し 1 つ。"""
    rep_idx_in_machine: int  # 機種枠内での横位置 index (0-7)
    machine: str             # 機種コード
    attribute: str           # 属性コード
    appear_step: int         # 出現する step (1-50)
    duration_steps: float    # 表示する step 数（≈ 1.8 step ≈ 0.75 秒）
    text: str                # セリフ本文
    label: str               # 「中毒者×初代GOD」表示用


def pick_voice_targets(
    records: list[StepRecord],
    reps: list[Persona],
    n_voices: int = 18,
    seed: int = 7,
    exclusion_window: float = 7.0,  # この step 数以内に同機種で別 bubble を出さない
) -> list[StepRecord]:
    """records から「画として面白い瞬間」を n_voices 個ピック。

    優先順位:
      1) 確定演出 / 重い特化ゾーン突入（強い event）
      2) 高 Δ脳汁ピーク（≥ 50）
      3) 中毒者 × 高ストレス × hit
      4) 大ハマり中の絶望（hit なしが続く + cash 減少）
      5) 大量上乗せ・軽い特化ゾーン
    重なり禁止: 同じ機種で exclusion_window step 以内に別 bubble を出さない（横塚指示）。
    """
    rng = np.random.default_rng(seed)
    rep_pids = {p.pid for p in reps}
    rep_records = [r for r in records if r.pid in rep_pids]

    candidates: list[tuple[int, StepRecord]] = []  # (priority, record) — 高い方を優先

    for r in rep_records:
        # 1) 強い event
        if r.trigger_event == "kakutei_engi":
            candidates.append((100, r))
        elif r.trigger_event == "tokka_heavy":
            candidates.append((90, r))
        # 5) 上乗せ・軽い特化
        elif r.trigger_event == "uwanose_heavy":
            candidates.append((75, r))
        elif r.trigger_event in ("uwanose_light", "tokka_light"):
            candidates.append((55, r))
        # 2) 高 Δ脳汁
        elif r.hit and r.brain_delta >= 70:
            candidates.append((85, r))
        elif r.hit and r.brain_delta >= 50:
            candidates.append((65, r))
        # 3) 中毒者 × 高ストレス × hit
        elif r.attribute == "C_CHASE" and r.pre_stress > 0.75 and r.hit:
            candidates.append((70, r))
        # 4) 大ハマり中の絶望
        elif (not r.hit) and r.pre_stress > 0.80 and r.cash < 5000:
            candidates.append((45, r))

    # 高優先度から、機種ごとの占有時間を見つつピック
    # 属性ごとの上限（1 属性が支配的にならないように、3 件まで）
    attr_cap = 3
    candidates.sort(key=lambda x: (-x[0], rng.random()))
    picked: list[StepRecord] = []
    machine_occupied: dict[str, list[int]] = defaultdict(list)  # 機種 → 採択済み step リスト
    attr_count: dict[str, int] = defaultdict(int)
    for prio, r in candidates:
        # 同機種で時間的に重なる bubble は排除（読みやすさ優先）
        if any(abs(s - r.step) < exclusion_window for s in machine_occupied[r.machine]):
            continue
        # 同 pid は 1 セリフだけ
        if any(pp.pid == r.pid for pp in picked):
            continue
        # 属性の偏り防止
        if attr_count[r.attribute] >= attr_cap:
            continue
        picked.append(r)
        machine_occupied[r.machine].append(r.step)
        attr_count[r.attribute] += 1
        if len(picked) >= n_voices:
            break
    picked.sort(key=lambda r: r.step)
    return picked


def pregenerate_voices(
    targets: list[StepRecord],
    reps: list[Persona],
) -> list[VoiceBubble]:
    """LLM (qwen3:4b) で吹き出しテキストを事前生成。約 0.3-0.5 秒/call × 32 = 10-16 秒。"""
    p_by_pid = {p.pid: p for p in reps}

    # 機種ごとの代表 index（draw_phase3 と同じ並び順 = reps の順）
    machine_rep_order: dict[str, list[str]] = defaultdict(list)
    for p in reps:
        machine_rep_order[p.assigned_machine].append(p.pid)
    machine_idx: dict[str, int] = {
        pid: i
        for m, pids in machine_rep_order.items()
        for i, pid in enumerate(pids)
    }

    history: list[str] = []
    bubbles: list[VoiceBubble] = []
    rng = np.random.default_rng(11)  # 性別・年齢サンプル用（再現性確保）
    print(f"  LLM 吹き出し事前生成: {len(targets)} 個（qwen3.5:35b）...")
    for i, r in enumerate(targets, 1):
        p = p_by_pid[r.pid]
        prof = VOICE_PROFILE[r.attribute]
        # 属性ごとの分布から性別・年齢を都度サンプリング（バリエーション）
        gender = "男性" if rng.random() < prof["male_prob"] else "女性"
        age_lo, age_hi = prof["age_range"]
        age = int(rng.integers(age_lo, age_hi + 1))
        ev_jp = EVENT_JP.get(r.trigger_event, r.trigger_event)
        # ハマり中の場合は trigger_event が "none" でも「ハマり継続」と書く
        if not r.hit and r.pre_stress > 0.80:
            ev_jp = "なし（ハマり継続・残金わずか）"
        ctx = {
            "category": prof["category"],
            "age": age,
            "gender": gender,
            "life_themes": prof.get("life_themes", ""),
            "machine": MACHINE_VOICE_LABEL[r.machine],
            "cash": r.cash,
            "miss_streak": 0,  # 簡略化（必要なら records から計算）
            "arousal": r.brain_arousal,
            "despair": min(100, r.pre_stress * 100),
            "stress_load": r.pre_stress,
            "trigger_event": ev_jp,
        }
        try:
            voice, elapsed = generate_inner_voice(ctx, voice_history=history)
            history.append(voice)
            if i % 5 == 0 or i == len(targets):
                print(f"    {i}/{len(targets)} 完了（最新 {elapsed:.2f}s）")
        except Exception as e:
            voice = "—"
            print(f"    ⚠️ {i} 失敗: {e}")
        # セリフが長すぎたら 25 字で切る（吹き出しはみ出し防止）
        if len(voice) > 25:
            voice = voice[:24] + "…"
        label = f"{ATTR_DISPLAY[r.attribute]}×{MACHINE_DISPLAY[r.machine]}"
        bubbles.append(VoiceBubble(
            rep_idx_in_machine=machine_idx.get(r.pid, 0),
            machine=r.machine,
            attribute=r.attribute,
            appear_step=r.step,
            duration_steps=6.0,   # ≈ 2.9 秒（Phase3=24s, 50step → 1step=0.48s）
            text=voice,
            label=label,
        ))
    return bubbles


def render_demo(
    personas: list[Persona],
    records: list[StepRecord],
    summaries: list[PersonaSummary],
    out_path: Path,
) -> None:
    ranges, total_frames = phase_frame_ranges()
    reps = pick_representatives(personas)
    rep_pids = {p.pid for p in reps}

    # 代表者の records を pid × step でひける形に
    rep_records: dict[tuple[str, int], StepRecord] = {}
    for r in records:
        if r.pid in rep_pids:
            rep_records[(r.pid, r.step)] = r

    # v4.6.1: 幸福度・ストレスランキングは廃止、脳汁一点に絞る
    brain_peaks_top5 = top_brain_peaks(records, top_n=5)
    p_by_pid = {p.pid: p for p in personas}
    aggregate = attribute_aggregate_stats(summaries, records)
    factor_means = factor_brain_means(records)  # v4.6.3: 要因別ランキング用
    counter = hypothesis_counter_evidence(records, brain_peaks_top5)  # v4.6.5: 反証材料

    # v4.6.6: Phase 3 ポップアップ吹き出し用 LLM 事前生成
    voice_targets = pick_voice_targets(records, reps, n_voices=18, seed=7)
    voice_bubbles = pregenerate_voices(voice_targets, reps)
    # step → bubbles へのインデックス（Phase 3 の draw 内で活発な吹き出しを引く）
    bubbles_by_step: dict[int, list[VoiceBubble]] = defaultdict(list)
    for b in voice_bubbles:
        bubbles_by_step[b.appear_step].append(b)

    # === Figure ===
    fig = plt.figure(figsize=(16, 9), dpi=110, facecolor="#0A0A12")
    ax = fig.add_axes([0, 0, 1, 1], facecolor="#0A0A12")
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # ── Phase 共通描画ヘルパ ─────────────────────
    def clear():
        ax.cla()
        ax.set_xlim(0, 16)
        ax.set_ylim(0, 9)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_facecolor("#0A0A12")
        for spine in ax.spines.values():
            spine.set_visible(False)

    def draw_phase1(local_frame, total):
        clear()
        # フェードイン
        alpha_t = min(1.0, local_frame / (FPS * 1.5))
        ax.text(8, 8.3, "パチスロ実践！脳汁が出る瞬間のシミュレーション",
                ha="center", va="center", color=(1, 1, 1, alpha_t),
                fontsize=22, fontweight="bold")
        # 0-3 秒: 脳汁の定義
        if local_frame < FPS * 6:
            sub_alpha = min(1.0, max(0.0, (local_frame - FPS * 0.5) / (FPS * 1.0)))
            ax.text(8, 7.0, "【脳汁とは何か】",
                    ha="center", va="center", color="#FFD700",
                    fontsize=20, fontweight="bold", alpha=sub_alpha)
            ax.text(8, 5.7,
                    "パチスロを打つ人の脳内で起きる、強烈な快感反応のこと",
                    ha="center", va="center", color="white", fontsize=15, alpha=sub_alpha)
            ax.text(8, 4.5,
                    "本シミュは 4 つの要素で計算（数値化）:",
                    ha="center", va="center", color=(0.85, 0.85, 0.9), fontsize=13, alpha=sub_alpha)
            ax.text(8, 3.6,
                    "①当たりの身体反応  ②大量取得感  ③期待が裏切られず叶った瞬間  ④異常な連チャン",
                    ha="center", va="center", color=(0.95, 0.95, 1.0), fontsize=12, alpha=sub_alpha)
            # v4.6.13: 第三者向けの補足（横塚指示で C 案採用）
            ax.text(8, 2.7,
                    "※ いずれも、実際にパチスロを打った人なら一度は体験する「脳が震える瞬間」",
                    ha="center", va="center", color=(0.75, 0.75, 0.85),
                    fontsize=11, style="italic", alpha=sub_alpha)
        # 6-16 秒: 仮説（3 段論法、v4.6.11 横塚指示）
        else:
            f2 = local_frame - FPS * 6
            sub_alpha = min(1.0, f2 / (FPS * 1.0))
            ax.text(8, 7.6, "【仮説】",
                    ha="center", va="center", color="#FFD700",
                    fontsize=22, fontweight="bold", alpha=sub_alpha)

            # ① 前提: 脳汁が最大化する条件
            ax.text(2.5, 6.55, "①",
                    ha="center", va="center", color="#FFD700",
                    fontsize=20, fontweight="bold", alpha=sub_alpha)
            ax.text(3.5, 6.55,
                    "ストレスが極限まで高まった瞬間に「爆発の兆し」が見えたとき、",
                    ha="left", va="center", color="white", fontsize=14, alpha=sub_alpha)
            ax.text(3.5, 6.05,
                    "脳汁（ドーパミン）は最大化する。",
                    ha="left", va="center", color="white",
                    fontsize=14, fontweight="bold", alpha=sub_alpha)

            # ② 観察: 最もストレスを抱えているのは中毒者
            if f2 > FPS * 1.5:
                a2 = min(1.0, (f2 - FPS * 1.5) / (FPS * 1.0))
                ax.text(2.5, 5.0, "②",
                        ha="center", va="center", color="#FFD700",
                        fontsize=20, fontweight="bold", alpha=a2)
                ax.text(3.5, 5.0,
                        "そして、最もストレスを抱えているのは「中毒者」である。",
                        ha="left", va="center", color="white", fontsize=14, alpha=a2)

            # ③ 仮説: ゆえに、最も脳汁を出す瞬間は… (v4.6.12 横塚指示で2行展開)
            if f2 > FPS * 3.0:
                a3 = min(1.0, (f2 - FPS * 3.0) / (FPS * 1.0))
                ax.text(2.5, 3.95, "③",
                        ha="center", va="center", color=ATTR_COLOR["C_CHASE"],
                        fontsize=20, fontweight="bold", alpha=a3)
                ax.text(3.5, 4.20,
                        "ゆえに、最も脳汁が出る瞬間は、",
                        ha="left", va="center", color=ATTR_COLOR["C_CHASE"],
                        fontsize=15, fontweight="bold", alpha=a3)
                ax.text(3.5, 3.65,
                        "「中毒者」がさらに大きなストレスを抱え、爆発の兆しを感じたときではないか？",
                        ha="left", va="center", color=ATTR_COLOR["C_CHASE"],
                        fontsize=13, fontweight="bold", alpha=a3)

            # 中毒者の定義 + 検証規模
            if f2 > FPS * 4.5:
                a4 = min(1.0, (f2 - FPS * 4.5) / (FPS * 1.0))
                ax.text(8, 2.85, "本シミュにおける「中毒者」の定義",
                        ha="center", va="center", color=ATTR_COLOR["C_CHASE"],
                        fontsize=12, fontweight="bold", alpha=a4)
                ax.text(8, 2.35,
                        "①  パチスロが日常の中心　　②  借金を抱えるほど打ち込む　　③  何よりもパチスロを優先",
                        ha="center", va="center", color="white", fontsize=11, alpha=a4)
                ax.text(8, 1.50,
                        f"1000 人 × {DURATION_NAME} {TOTAL_G:,}G を一斉シミュレーションして検証",
                        ha="center", va="center", color=(0.85, 0.85, 0.9),
                        fontsize=13, style="italic", alpha=a4)

    # v4.6.13: 属性紹介ページ（横塚指示で Phase 2 の前に追加）
    ATTR_DESCRIPTIONS = {
        "A_NEWBIE":   "はじめての店で慎重に打つ若者層。新鮮な驚きと戸惑いを抱えながら 1G ずつ。",
        "B_REGULAR":  "月数回通うライト層。軽い遊び感覚で、無理しない範囲を楽しむ常連。",
        "C_CHASE":    "借金を抱え、生活に支障が出るほど打ち込む依存層。何よりもパチスロを優先。",
        "D_AFTER5":   "仕事帰りにストレス発散で打つサラリーマン／OL。終電までの時間が勝負。",
        "E_LEISURE":  "経済的余裕のある層。お金よりも刺激そのものを楽しむ、ゆとりある打ち方。",
        "F_SENIOR":   "年金生活のシニア。健康的な日々の楽しみ、慣れた手つきで黙々と。",
        "G_BREATHER": "家事の合間の息抜き、家計の小遣いの範囲で打つ主婦。日常からの解放感。",
        "H_PRO":      "期待値計算と収支管理で立ち回るパチプロ。感情よりロジック、長期目線。",
    }

    def draw_phase_attrs(local_frame, total):
        """8 属性の人物紹介（v4.6.13: 横塚指示、v4.6.14: サンプリング説明追加）。"""
        clear()
        # フェードイン
        a_t = min(1.0, local_frame / (FPS * 1.0))
        ax.text(8, 8.65, "8 属性の人物紹介",
                ha="center", va="center", color="#FFD700",
                fontsize=22, fontweight="bold", alpha=a_t)
        ax.text(8, 7.95,
                "シミュには 1,000 人が登場し、各属性は約 125 人ずつの「集団」を表す",
                ha="center", va="center", color=(0.85, 0.85, 0.9),
                fontsize=12, alpha=a_t)
        ax.text(8, 7.45,
                "（同じ属性でも、感受性・所持金・打ち方は人ごとに異なる）",
                ha="center", va="center", color=(0.7, 0.7, 0.85),
                fontsize=10.5, style="italic", alpha=a_t)

        # 8 属性を 2 列 × 4 行で配置
        col_x = [0.5, 8.3]    # 左列・右列の左端
        col_w = 7.2
        row_y = [6.7, 5.05, 3.40, 1.75]  # 上から下へ
        row_h = 1.45

        # ATTRIBUTES の順番でカード生成
        for i, a in enumerate(ATTRIBUTES):
            col_idx = i % 2
            row_idx = i // 2
            x = col_x[col_idx]
            y = row_y[row_idx]
            color = ATTR_COLOR[a.code]
            # 背景は属性色を 18% に暗くした版（hex → rgb 経由）
            from matplotlib.colors import to_rgb
            r_, g_, b_ = to_rgb(color)
            bg_color = (r_ * 0.18, g_ * 0.18, b_ * 0.18)

            # フェードイン段階表示（左列→右列、上→下）
            appear_at = i * 0.35
            if local_frame < FPS * appear_at:
                continue
            card_alpha = min(1.0, (local_frame - FPS * appear_at) / (FPS * 0.6))

            # 角丸ボックス
            ax.add_patch(patches.FancyBboxPatch(
                (x, y - row_h + 0.05), col_w, row_h,
                boxstyle="round,pad=0.04,rounding_size=0.15",
                linewidth=1.8, edgecolor=color,
                facecolor=bg_color,
                alpha=card_alpha * 0.85))

            # 属性ドット（左上）
            ax.plot(x + 0.4, y - 0.32, "o",
                    markersize=14, color=color, alpha=card_alpha * 0.95)
            # 属性名
            ax.text(x + 0.85, y - 0.32, a.display_name,
                    ha="left", va="center", color=color,
                    fontsize=13.5, fontweight="bold", alpha=card_alpha)
            # 説明文
            ax.text(x + 0.4, y - 0.95, ATTR_DESCRIPTIONS.get(a.code, ""),
                    ha="left", va="center", color="white",
                    fontsize=10, alpha=card_alpha)

    # v4.6.15: 6 機種の説明文（横塚指示で全面差し替え）
    MACHINE_DESCRIPTIONS = {
        "NORMAL_BONUS":
            "ボーナス当選のみでメダルが純増する伝統的なタイプ。爆発力はないが、安定して積み上げる楽しさがある王道機種群。",
        "BURST_AT_4G":
            "規制以前の「4号機」世代の代表格。AT 初当たりは遠いが、一度 AT に入れば数千枚の出玉が狙えるハイリスク・ハイリターン型。",
        "LATE_4G_MASS":
            "この世代の最大の魅力はストック機能。当選を内部に蓄積し放出する仕組みで多彩なゲーム性と連チャン性を両立、2000 年代中期のブームを牽引。",
        "SELF_TRIGGER_5G":
            "2010 年以降の 5 号機の尖った仕様を追求した世代。基本は出玉が振るわないが、上乗せ特化が発生すると終日終わらない状態に突入。通称「事故待ち」。",
        "LOOP_CHAIN_5G":
            "連チャンの継続性が魅力。一度引けば続くが、途切れる瞬間は突然訪れる。高継続中のイケイケ感と、いつ終わるかわからない不安が同居する。",
        "GOD_ORIGIN":
            "1/8,192 で「一撃 5,000 枚」が約束された伝説機。圧倒的な爆発力ゆえに多くの依存症問題を生み、後に規制対象となった、パチスロ史上最も極端な存在。",
    }

    def draw_phase_machines(local_frame, total):
        """6 機種の機種紹介（v4.6.14: 横塚指示で 8 属性紹介の次に追加）。"""
        clear()
        a_t = min(1.0, local_frame / (FPS * 1.0))
        ax.text(8, 8.65, "6 機種の機種紹介",
                ha="center", va="center", color="#FFD700",
                fontsize=22, fontweight="bold", alpha=a_t)
        ax.text(8, 7.95,
                "本シミュは、パチスロ史を彩った代表的な 6 タイプの機種を扱う",
                ha="center", va="center", color=(0.85, 0.85, 0.9),
                fontsize=12, alpha=a_t)
        ax.text(8, 7.45,
                "（同じ機種カテゴリでも、引きと展開は人ごとに異なる）",
                ha="center", va="center", color=(0.7, 0.7, 0.85),
                fontsize=10.5, style="italic", alpha=a_t)

        # 6 機種を 2 列 × 3 行で配置（v4.6.15: 高さ拡張で 2 行説明に対応）
        col_x = [0.5, 8.3]
        col_w = 7.2
        row_y = [6.6, 4.45, 2.30]
        row_h = 2.05

        for i, m in enumerate(MACHINES):
            col_idx = i % 2
            row_idx = i // 2
            x = col_x[col_idx]
            y = row_y[row_idx]

            # v4.6.15: 機種ごとに固有のカラー（横塚指示で 6 色に分離）
            edge_color = MACHINE_COLOR.get(m.code, "#FFD700")
            from matplotlib.colors import to_rgb
            r_, g_, b_ = to_rgb(edge_color)
            bg_color = (r_ * 0.15, g_ * 0.15, b_ * 0.15)

            appear_at = i * 0.4
            if local_frame < FPS * appear_at:
                continue
            card_alpha = min(1.0, (local_frame - FPS * appear_at) / (FPS * 0.6))

            # 角丸ボックス
            ax.add_patch(patches.FancyBboxPatch(
                (x, y - row_h + 0.05), col_w, row_h,
                boxstyle="round,pad=0.04,rounding_size=0.15",
                linewidth=1.8, edgecolor=edge_color,
                facecolor=bg_color,
                alpha=card_alpha * 0.9))

            # 機種名（タイトル）
            ax.text(x + 0.4, y - 0.35, m.display_name,
                    ha="left", va="center", color=edge_color,
                    fontsize=13, fontweight="bold", alpha=card_alpha)
            # タグライン
            ax.text(x + col_w - 0.4, y - 0.35,
                    MACHINE_TAGLINE.get(m.code, ""),
                    ha="right", va="center", color="white",
                    fontsize=11, fontweight="bold", alpha=card_alpha)
            # 説明文を「。」で分割して 2 行表示（横塚指示で右端見切れ防止）
            desc = MACHINE_DESCRIPTIONS.get(m.code, "")
            desc_parts = [s.strip() + "。" for s in desc.split("。") if s.strip()]
            for li, line in enumerate(desc_parts[:2]):
                ax.text(x + 0.4, y - 0.90 - li * 0.42, line,
                        ha="left", va="center", color=(0.95, 0.95, 1.0),
                        fontsize=9.2, alpha=card_alpha)
            # 代表機種
            ax.text(x + 0.4, y - 1.78,
                    f"例: {MACHINE_EXAMPLES.get(m.code, '')}",
                    ha="left", va="center", color=(0.7, 0.7, 0.85),
                    fontsize=9, style="italic", alpha=card_alpha)

    def draw_phase2(local_frame, total):
        """48 セル格子（一括表示 + 機種上の説明、v4.6.3）。"""
        clear()
        ax.text(8, 8.55, "8 属性 × 6 機種 = 48 セル格子",
                ha="center", va="center", color="white", fontsize=22, fontweight="bold")
        ax.text(8, 8.0,
                "各セルに 21 人ずつ、合計 1,008 人を一斉に打たせて観察する",
                ha="center", va="center", color=(0.85, 0.85, 0.9), fontsize=12)

        # 機種ヘッダ（v4.6.10: 機種名 + タグライン + モデル機種例の 3 段）
        col_w = 2.1
        col_x0 = 2.2
        for i, m in enumerate(MACHINES):
            cx = col_x0 + i * col_w
            ax.text(cx, 7.30, m.display_name,
                    ha="center", va="center", color="#FFD700",
                    fontsize=9.5, fontweight="bold")
            ax.text(cx, 6.85, MACHINE_TAGLINE.get(m.code, ""),
                    ha="center", va="center", color=(1.0, 1.0, 0.95),
                    fontsize=10.5, fontweight="bold")
            # モデル機種例（小さく薄く、参考情報として）
            ax.text(cx, 6.40, MACHINE_EXAMPLES.get(m.code, ""),
                    ha="center", va="center", color=(0.65, 0.65, 0.78),
                    fontsize=7.5, style="italic")

        # 行（属性）+ ドット（v4.6.3: 一括表示、appear_at ロジック削除）
        cell_dots = 21
        cols_per_cell = 7
        for ai, a in enumerate(ATTRIBUTES):
            row_y = 6.0 - ai * 0.65
            ax.text(1.6, row_y, a.display_name, ha="right", va="center",
                    color=ATTR_COLOR[a.code], fontsize=10, fontweight="bold")
            for mi, m in enumerate(MACHINES):
                cx = col_x0 + mi * col_w
                for k in range(cell_dots):
                    dx = (k % cols_per_cell - 3) * 0.20
                    dy = (k // cols_per_cell - 1) * 0.18
                    ax.plot(cx + dx, row_y + dy, "o",
                            markersize=3.4, color=ATTR_COLOR[a.code], alpha=0.85)

        ax.text(8, 0.85,
                "1 ドット = 1 人",
                ha="center", va="center", color="white",
                fontsize=12, fontweight="bold")
        ax.text(8, 0.30,
                "全員が同時に 1 日 8,000G を打ち、誰がどう脳汁を出すかを比較する",
                ha="center", va="center", color=(0.7, 0.7, 0.8),
                fontsize=11, style="italic")

    def draw_phase3(local_frame, total):
        clear()
        # 50 step を total フレームで早回し（DURATION_MODE 依存）
        step = int(np.clip(local_frame / total * 50, 1, 50))
        g_per_step = TOTAL_G / 50
        approx_g = int(step * g_per_step)
        ax.text(8, 8.4,
                f"シミュレーション実行中  {DURATION_NAME} {approx_g:,}G / {TOTAL_G:,}G",
                ha="center", va="center", color="white", fontsize=18, fontweight="bold")

        # 6 機種を 3 列 × 2 段で配置（v4.6 リネーム後の内部 ID）
        layout = [
            ("NORMAL_BONUS",    3.0, 6.0),
            ("LATE_4G_MASS",    8.0, 6.0),
            ("BURST_AT_4G",    13.0, 6.0),
            ("SELF_TRIGGER_5G", 3.0, 2.5),
            ("LOOP_CHAIN_5G",   8.0, 2.5),
            ("GOD_ORIGIN",     13.0, 2.5),
        ]
        max_brain_so_far = 0.0
        n_chain_active = 0
        n_hit_this_step = 0
        latest_event = ""

        for code, cx, cy in layout:
            mt = MACHINES_BY_CODE[code]
            # 機種枠
            rect = patches.Rectangle((cx - 1.8, cy - 1.2), 3.6, 2.4,
                                     facecolor="#22223A", edgecolor="#FFD700",
                                     linewidth=1.3, alpha=0.6)
            ax.add_patch(rect)
            ax.text(cx, cy + 1.4, MACHINE_DISPLAY[code], ha="center", va="center",
                    color="#FFD700", fontsize=11, fontweight="bold")
            # v4.6: 内部 ID（英語コード）は動画に出さない方針

            # この機種に配属された 8 属性の代表ドット
            cell_reps = [r for r in reps if r.assigned_machine == code]
            for k, p in enumerate(cell_reps):
                # 8 属性を横一列
                px = cx - 1.4 + k * 0.4
                py = cy
                rec = rep_records.get((p.pid, step))
                if rec is None:
                    continue
                color = ATTR_COLOR[p.attribute_code]
                size = 60
                edge = "none"
                edge_w = 0.0
                if rec.hit:
                    n_hit_this_step += 1
                    size = 200 + min(rec.brain_delta * 4, 350)
                    if rec.trigger_event not in ("none", "chain_start"):
                        edge = "#FFFFFF"
                        edge_w = 2.0
                    if rec.brain_delta > max_brain_so_far:
                        max_brain_so_far = rec.brain_delta
                        latest_event = (
                            f"step{step}: {ATTR_DISPLAY[p.attribute_code]} × {MACHINE_DISPLAY[code]} "
                            f"+{rec.brain_delta:.0f}"
                        )
                elif rec.chain_active:
                    size = 110
                    edge = ATTR_COLOR[p.attribute_code]
                    edge_w = 1.0
                    n_chain_active += 1
                ax.scatter([px], [py], s=size, c=color, edgecolors=edge, linewidths=edge_w, zorder=5)

        # v4.6.6: LLM ポップアップ吹き出し（該当 step の人物のドット近傍に出す）
        machine_pos = {code: (cx, cy) for code, cx, cy in layout}
        step_f = local_frame / total * 50.0
        for b in voice_bubbles:
            elapsed = step_f - b.appear_step
            if elapsed < 0 or elapsed > b.duration_steps:
                continue
            # フェード in/out
            fade = 0.35
            if elapsed < fade:
                alpha = elapsed / fade
            elif elapsed > b.duration_steps - fade:
                alpha = max(0.0, (b.duration_steps - elapsed) / fade)
            else:
                alpha = 1.0
            if alpha <= 0:
                continue
            cx, cy = machine_pos[b.machine]
            px = cx - 1.4 + b.rep_idx_in_machine * 0.4
            py = cy
            # 吹き出しサイズ（本文 1 行のみ、コンパクト）
            text_w = max(1.7, min(4.6, len(b.text) * 0.20 + 0.5))
            text_h = 0.46
            # 上段機種は下方向に、下段機種は上方向に出す（機種ヘッダ衝突回避）
            is_upper = cy > 5.0
            if is_upper:
                bubble_y = py - 0.68
                tail_base_y = bubble_y + text_h / 2 - 0.01
                tail_tip_y = py - 0.18
            else:
                bubble_y = py + 0.68
                tail_base_y = bubble_y - text_h / 2 + 0.01
                tail_tip_y = py + 0.18
            # v4.6.14: bubble x 中心を画面内にクランプ（右端見切れ防止、横塚指示）
            half_w = text_w / 2
            margin = 0.25
            bubble_x = px
            if bubble_x - half_w < margin:
                bubble_x = margin + half_w
            elif bubble_x + half_w > 16.0 - margin:
                bubble_x = 16.0 - margin - half_w
            # 角丸ボックス本体（不透明 + 太枠で属性カラー）
            box = patches.FancyBboxPatch(
                (bubble_x - half_w, bubble_y - text_h / 2),
                text_w, text_h,
                boxstyle="round,pad=0.04,rounding_size=0.16",
                facecolor="#FFFFFF",
                edgecolor=ATTR_COLOR[b.attribute],
                linewidth=2.5,
                alpha=alpha,
                zorder=10,
            )
            ax.add_patch(box)
            # しっぽ（吹き出し底辺中央 → ドット方向、横ずれは斜めで対応）
            tail = patches.Polygon(
                [(bubble_x - 0.10, tail_base_y),
                 (bubble_x + 0.10, tail_base_y),
                 (px, tail_tip_y)],
                facecolor="#FFFFFF",
                edgecolor=ATTR_COLOR[b.attribute],
                linewidth=1.8,
                alpha=alpha,
                zorder=10,
            )
            ax.add_patch(tail)
            # セリフ本文のみ（属性は枠色、機種は出現位置で判別）
            ax.text(bubble_x, bubble_y, b.text, ha="center", va="center",
                    color="#101020", fontsize=10, fontweight="bold",
                    alpha=alpha, zorder=11)

        # v4.6.8: 左下・右下のステータスは第三者にわかりにくいため削除（横塚指示）

    def draw_ranking_card(rank: int, s: PersonaSummary, kind: str, alpha: float):
        # kind: "happy" or "stress"
        title = "最高幸福ランキング" if kind == "happy" else "最高ストレスランキング"
        primary = (
            f"{rank}位  {ATTR_DISPLAY[s.attribute]} × {MACHINE_DISPLAY[s.machine]}"
        )
        ax.text(8, 8.0, title, ha="center", va="center",
                color="#FFD700", fontsize=20, fontweight="bold", alpha=alpha)
        ax.text(8, 6.8, primary, ha="center", va="center",
                color=ATTR_COLOR[s.attribute], fontsize=24, fontweight="bold", alpha=alpha)

        balance_label = format_balance(s.net_balance)
        event_label = EVENT_JP.get(s.peak_event, s.peak_event)
        if kind == "happy":
            ax.text(8, 5.6,
                    f"その日の収支  {balance_label}",
                    ha="center", va="center", color="white", fontsize=22, fontweight="bold", alpha=alpha)
            ax.text(8, 4.7,
                    f"ピーク Δ脳汁  +{s.max_brain_delta:.0f}  ({TOTAL_G:,}G 中の最高瞬間)",
                    ha="center", va="center", color=(0.85, 0.85, 0.9), fontsize=15, alpha=alpha)
            ax.text(8, 3.9,
                    f"その瞬間: {event_label}",
                    ha="center", va="center", color=(0.85, 0.85, 0.9), fontsize=14, alpha=alpha)
            ax.text(8, 3.1,
                    f"その時のストレス  {s.peak_pre_stress:.2f}",
                    ha="center", va="center", color=(0.7, 0.7, 0.8), fontsize=13, alpha=alpha)
        else:
            ax.text(8, 5.6,
                    f"max ストレス  {s.max_stress:.2f}",
                    ha="center", va="center", color="white", fontsize=22, fontweight="bold", alpha=alpha)
            ax.text(8, 4.7,
                    f"ピーク Δ脳汁  +{s.max_brain_delta:.0f}",
                    ha="center", va="center", color=(0.85, 0.85, 0.9), fontsize=15, alpha=alpha)
            ax.text(8, 3.9,
                    f"その日の収支  {balance_label}",
                    ha="center", va="center", color=(0.85, 0.85, 0.9), fontsize=14, alpha=alpha)

        # 大きな属性カラーのドット（v4.6: 日本語表示名のみ）
        ax.scatter([8], [1.8], s=2400, c=ATTR_COLOR[s.attribute], alpha=alpha * 0.85)
        ax.text(8, 1.8, ATTR_DISPLAY[s.attribute], ha="center", va="center",
                color="black", fontsize=13, fontweight="bold", alpha=alpha)

    def draw_phase4(local_frame, total):
        """属性別 脳汁ランキング（v4.6.2: 横塚再指示）。"""
        clear()
        ax.text(8, 8.3, "属性別 脳汁ランキング",
                ha="center", va="center", color="#FFD700",
                fontsize=22, fontweight="bold")
        ax.text(8, 7.7, "「最も脳汁が出ていた属性」を平均 Δ脳汁 で並べる",
                ha="center", va="center", color=(0.85, 0.85, 0.9), fontsize=12)

        attr_order = sorted(aggregate.items(), key=lambda x: -x[1]["mean_brain"])
        max_v = max((v["mean_brain"] for _, v in attr_order), default=1.0) or 1.0

        for i, (acode, vals) in enumerate(attr_order):
            y = 6.7 - i * 0.65
            # 順位
            rank_color = "#FFD700" if i == 0 else ("#CCCCCC" if i == 1 else
                          ("#CD7F32" if i == 2 else (0.6, 0.6, 0.7)))
            ax.text(0.5, y, f"{i+1}位",
                    ha="left", va="center", color=rank_color,
                    fontsize=14, fontweight="bold")
            # 属性
            ax.text(2.0, y, ATTR_DISPLAY[acode],
                    ha="left", va="center", color=ATTR_COLOR[acode],
                    fontsize=13, fontweight="bold")
            # 平均 Δ脳汁 棒グラフ
            bar_w = (vals["mean_brain"] / max_v) * 8.0
            ax.barh([y], [bar_w], left=4.5, height=0.36,
                    color=ATTR_COLOR[acode], alpha=0.85)
            ax.text(4.6 + bar_w, y, f"平均 +{vals['mean_brain']:.0f}",
                    ha="left", va="center", color="white",
                    fontsize=11, fontweight="bold")
            # max 脳汁 / ピーク回数
            ax.text(13.7, y, f"max +{vals['max_brain']:.0f}　ピーク {vals['peak_count']} 回",
                    ha="left", va="center", color=(0.7, 0.7, 0.8), fontsize=9)

        # v4.6.12: 重なる矢印を削除（横塚指示）。代わりに第三者向けの読み方ガイドを下部に追加。
        ax.text(8, 1.30, "── 数値の読み方 ──",
                ha="center", va="center", color="#FFD700",
                fontsize=11, fontweight="bold")
        ax.text(8, 0.80,
                "平均 = 1G あたりの脳汁の出やすさ　／　max = その属性で起きた一発の最高ピーク　／　ピーク回数 = +50 以上の発生数",
                ha="center", va="center", color=(0.85, 0.85, 0.9), fontsize=10)
        ax.text(8, 0.30,
                "→ バーが長いほど「日常的に脳汁が出やすかった属性」",
                ha="center", va="center", color=(0.7, 0.7, 0.85),
                fontsize=10, style="italic")

    def stress_label(pre_stress: float) -> str:
        if pre_stress > 0.85:
            return "極度のストレス（マックス級）"
        if pre_stress > 0.65:
            return "高ストレス"
        if pre_stress > 0.35:
            return "中程度"
        return "平常"

    def interpret_peak(r: StepRecord, p: Persona) -> str:
        """1 行解釈（簡素な決まり文句）。"""
        if r.attribute == "C_CHASE" and r.pre_stress > 0.85:
            return "ストレス極限 × 爆発の兆し → 期待が増幅された結果の脳汁ピーク"
        if r.trigger_event == "kakutei_engi":
            return "確定演出 → 桁違いの興奮、脳汁が一気に弾けた"
        if r.machine == "GOD_ORIGIN":
            return "初代GODの別格な払出 → 人生変わる級の爆発"
        if r.trigger_event in ("tokka_heavy", "uwanose_heavy"):
            return "重い特化ゾーン突入 → 連チャンの予感が脳汁を伸ばす"
        return f"{ATTR_DISPLAY[r.attribute]} の感受性 × イベントの意味づけ"

    def draw_individual_top_card(rank: int, r: StepRecord, alpha: float):
        """個人 Top 3 の詳細カード（v4.6.3: ストーリー強化、横塚指示）。"""
        p = p_by_pid[r.pid]
        attr_jp = ATTR_DISPLAY[r.attribute]
        machine_jp = MACHINE_DISPLAY[r.machine]
        event_jp = EVENT_JP.get(r.trigger_event, r.trigger_event)
        # v4.6.16: GOD_ORIGIN 機種の「初当たり」は「GODゲーム当選」表記に（横塚指示）
        if r.machine == "GOD_ORIGIN" and event_jp == "初当たり":
            event_jp = "GODゲーム当選"
        rank_color = "#FFD700" if rank == 1 else ("#CCCCCC" if rank == 2 else "#CD7F32")

        # ヘッダ
        ax.text(8, 8.5, f"{rank}位 — 最も脳汁を出した個人",
                ha="center", va="center", color=rank_color,
                fontsize=20, fontweight="bold", alpha=alpha)
        ax.text(8, 7.7, f"{attr_jp} × {machine_jp}",
                ha="center", va="center", color=ATTR_COLOR[r.attribute],
                fontsize=22, fontweight="bold", alpha=alpha)
        ax.text(8, 6.85, f"Δ脳汁 +{r.brain_delta:.0f}",
                ha="center", va="center", color="white",
                fontsize=28, fontweight="bold", alpha=alpha)

        # ストーリー 3 行（属性別、借金あり等の文脈）— どういう属性の人か
        story = gen_persona_story(p, r, rank=rank)
        for i, line in enumerate(story):
            ax.text(8, 5.5 - i * 0.7, line,
                    ha="center", va="center", color=(1.0, 0.95, 0.85),
                    fontsize=15, alpha=alpha)

        # v4.6.8: 第三者向けに簡素化（横塚指示）— 個人パラメータ・step 等の詳細は PDF へ
        # 「どういう瞬間に最も興奮したか」だけ大きく見せる
        ax.text(8, 2.95, "その瞬間に起きたこと",
                ha="center", va="center", color="#FFD700",
                fontsize=14, fontweight="bold", alpha=alpha)
        ax.text(8, 2.20, event_jp,
                ha="center", va="center", color="white",
                fontsize=22, fontweight="bold", alpha=alpha)
        # v4.6.10: GOD_ORIGIN 機種の場合は伝説の解説を差し込む（横塚指示）
        if r.machine == "GOD_ORIGIN":
            ax.text(8, 1.30,
                    "初代GOD：1/8,192 で「一撃 5,000 枚」が約束された、2000 年代のプレミアムフラグ",
                    ha="center", va="center", color=(1.0, 0.85, 0.4),
                    fontsize=12, fontweight="bold", alpha=alpha)
            ax.text(8, 0.75,
                    "ハマっても、出れば人生を変える ─ 依存症患者を多く生んだ、伝説の契機",
                    ha="center", va="center", color=(0.95, 0.85, 0.55),
                    fontsize=11, style="italic", alpha=alpha)
        else:
            ax.text(8, 0.85, interpret_peak(r, p),
                    ha="center", va="center", color=(1.0, 0.85, 0.4),
                    fontsize=13, fontweight="bold", style="italic", alpha=alpha)

    def draw_phase5(local_frame, total):
        """個人 Top 3 詳細解説。3位 → 2位 → 1位 の順で 9 秒/枚。"""
        clear()
        n_per_card = total / 3.0
        rank_idx = int(min(local_frame // n_per_card, 2))
        local_in_card = local_frame - rank_idx * n_per_card
        if local_in_card < FPS * 0.5:
            alpha = local_in_card / (FPS * 0.5)
        elif local_in_card > n_per_card - FPS * 0.5:
            alpha = max(0.0, (n_per_card - local_in_card) / (FPS * 0.5))
        else:
            alpha = 1.0
        # 3 → 2 → 1 の順で見せる
        display_rank = 3 - rank_idx
        if display_rank - 1 < len(brain_peaks_top5):
            draw_individual_top_card(display_rank, brain_peaks_top5[display_rank - 1], alpha)

    def draw_phase6(local_frame, total):
        """脳汁が出やすかった「機種の特徴」を 2 つの抽象要素で示す（v4.6.8: 横塚指示）。

        数値ランキングをやめ、第三者にも伝わる抽象化:
          要素①: 一撃の爆発力（ミリオンゴッド級の大量払い出し）
          要素②: 滅多に出ない「引き金」（確定演出・特化ゾーン突入）
        """
        clear()
        ax.text(8, 8.4, "脳汁が出やすかった「機種の特徴」",
                ha="center", va="center", color="#FFD700",
                fontsize=22, fontweight="bold")
        ax.text(8, 7.7,
                "数字よりも、共通する 2 つの要素を見てほしい",
                ha="center", va="center", color=(0.85, 0.85, 0.9),
                fontsize=12, style="italic")

        # 要素①: 一撃の爆発力
        ax.add_patch(patches.FancyBboxPatch(
            (0.7, 4.4), 6.9, 2.5,
            boxstyle="round,pad=0.05,rounding_size=0.18",
            linewidth=2.2, edgecolor="#E04545",
            facecolor=(0.20, 0.06, 0.06), alpha=0.85))
        ax.text(4.15, 6.45, "要素 ①  一撃の爆発力",
                ha="center", va="center", color="#FF6060",
                fontsize=15, fontweight="bold")
        ax.text(4.15, 5.75, "5,000 枚クラスの大量払い出し",
                ha="center", va="center", color="white",
                fontsize=12, fontweight="bold")
        ax.text(4.15, 5.20, "桁違いの取得感が、脳を揺さぶる",
                ha="center", va="center", color=(0.85, 0.85, 0.9), fontsize=11)
        ax.text(4.15, 4.65, "→ 初代GOD（ミリオンゴッド）系で顕著",
                ha="center", va="center", color="#FFD700",
                fontsize=10, fontweight="bold", style="italic")

        # 要素②: 滅多に出ない引き金
        ax.add_patch(patches.FancyBboxPatch(
            (8.4, 4.4), 6.9, 2.5,
            boxstyle="round,pad=0.05,rounding_size=0.18",
            linewidth=2.2, edgecolor="#FFD700",
            facecolor=(0.18, 0.15, 0.04), alpha=0.85))
        ax.text(11.85, 6.45, "要素 ②  滅多に来ない「引き金」",
                ha="center", va="center", color="#FFE060",
                fontsize=15, fontweight="bold")
        ax.text(11.85, 5.75, "確定演出・特化ゾーン突入・連チャン",
                ha="center", va="center", color="white",
                fontsize=12, fontweight="bold")
        ax.text(11.85, 5.20, "レアだからこそ、出た瞬間が爆発の合図",
                ha="center", va="center", color=(0.85, 0.85, 0.9), fontsize=11)
        ax.text(11.85, 4.65, "→ どの機種でも、それだけで脳汁を呼ぶ",
                ha="center", va="center", color="#FFD700",
                fontsize=10, fontweight="bold", style="italic")

        # 結論
        if local_frame > FPS * 5:
            ax.add_patch(patches.FancyBboxPatch(
                (1.4, 1.2), 13.2, 2.5,
                boxstyle="round,pad=0.05,rounding_size=0.2",
                linewidth=2.5, edgecolor="#FFD700",
                facecolor=(0.10, 0.10, 0.20), alpha=0.92))
            ax.text(8, 3.05, "つまり",
                    ha="center", va="center", color="#FFD700",
                    fontsize=13, fontweight="bold")
            ax.text(8, 2.40,
                    "「爆発の天井」と「滅多に来ない引き金」",
                    ha="center", va="center", color="white",
                    fontsize=15, fontweight="bold")
            ax.text(8, 1.65,
                    "この 2 つが揃った機種で、脳汁は最も激しく出る",
                    ha="center", va="center", color=(0.95, 0.95, 1.0),
                    fontsize=13, fontweight="bold")

    def draw_phase7(local_frame, total):
        """多面的な仮説検証（v4.6.8: 横塚指示で「人の心理 vs 機種の力」の二面構成に再設計）。"""
        clear()

        # ── 心理側スコアの計算 ──
        attr_order_stress = sorted(aggregate.items(), key=lambda x: -x[1]["max_stress"])
        attr_order_brain = sorted(aggregate.items(), key=lambda x: -x[1]["mean_brain"])
        chase_stress_top = (attr_order_stress[0][0] == "C_CHASE") if attr_order_stress else False
        chase_brain_rank = next(
            (i for i, (a, _) in enumerate(attr_order_brain) if a == "C_CHASE"), -1) + 1
        chase_in_top5 = sum(1 for r in brain_peaks_top5 if r.attribute == "C_CHASE")
        psy_passed = [chase_stress_top, chase_brain_rank <= 3, chase_in_top5 >= 1]
        psy_score = sum(psy_passed)

        # ── 機種側スコアの計算 ──
        non_chase_top5 = counter["non_chase_in_top5_count"]  # 中毒者でない人が Top5 に何人
        god_ratio = counter["god_max_ratio"]  # 同 GOD での属性差倍率
        ls_count = counter["low_stress_peaks_count"]  # 低ストレス × 高脳汁 件数
        machine_passed = [non_chase_top5 >= 1, god_ratio < 1.6, ls_count >= 5]
        machine_score = sum(machine_passed)

        # ── タイトル ──
        ax.text(8, 8.5, "仮説の答え合わせ",
                ha="center", va="center", color="#FFD700",
                fontsize=22, fontweight="bold")
        ax.text(8, 7.85,
                "横塚の仮説:「脳汁の主役は人の心理（属性 × ストレス × 兆し）」",
                ha="center", va="center", color=(0.85, 0.85, 0.9),
                fontsize=12, style="italic")
        ax.text(8, 7.35,
                "「人の心理」と「機種の力」、両方から多面的に見る",
                ha="center", va="center", color=(0.7, 0.7, 0.85), fontsize=11)

        # ── 左パネル: 人の心理側 ──
        ax.add_patch(patches.FancyBboxPatch(
            (0.5, 1.7), 7.1, 5.2,
            boxstyle="round,pad=0.05,rounding_size=0.18",
            linewidth=2.0, edgecolor="#7AC8FF",
            facecolor=(0.05, 0.10, 0.18), alpha=0.85))
        ax.text(4.05, 6.55, "【 人の心理 】の貢献",
                ha="center", va="center", color="#7AC8FF",
                fontsize=14, fontweight="bold")

        psy_items = [
            ("中毒者は最もストレスを抱えていたか", chase_stress_top),
            ("中毒者は脳汁の上位常連だったか", chase_brain_rank <= 3),
            ("ピーク Top5 に中毒者はいたか", chase_in_top5 >= 1),
        ]
        for i, (q, passed) in enumerate(psy_items):
            y = 5.75 - i * 0.7
            mark = "○" if passed else "△"
            mark_color = "#7FE07F" if passed else "#F0A030"
            ax.text(0.95, y, mark, ha="left", va="center",
                    color=mark_color, fontsize=18, fontweight="bold")
            ax.text(1.7, y, q, ha="left", va="center",
                    color="white", fontsize=11, fontweight="bold")

        ax.text(4.05, 3.0, f"{psy_score} / 3 軸 支持",
                ha="center", va="center", color="#7AC8FF",
                fontsize=18, fontweight="bold")
        ax.text(4.05, 2.35, "中毒者はストレスを抱えやすく、",
                ha="center", va="center", color=(0.9, 0.9, 1.0), fontsize=11)
        ax.text(4.05, 1.95, "脳汁も出やすい傾向はある。ただ、それだけでは…",
                ha="center", va="center", color=(0.9, 0.9, 1.0),
                fontsize=11, style="italic")

        # ── 右パネル: 機種の力 ──
        ax.add_patch(patches.FancyBboxPatch(
            (8.4, 1.7), 7.1, 5.2,
            boxstyle="round,pad=0.05,rounding_size=0.18",
            linewidth=2.0, edgecolor="#FFA640",
            facecolor=(0.18, 0.10, 0.04), alpha=0.85))
        ax.text(11.95, 6.55, "【 機種の力 】の貢献",
                ha="center", va="center", color="#FFA640",
                fontsize=14, fontweight="bold")

        machine_items = [
            ("脳汁ピーク Top5 に\n中毒者でない人もいた", non_chase_top5 >= 1,
             f"→ {non_chase_top5} 人"),
            ("同じ初代GOD でも\n属性差より機種効果が大きい", god_ratio < 1.6,
             f"→ 属性差は {god_ratio:.1f} 倍"),
            ("ストレスが低くても\n大爆発する人がいた", ls_count >= 5,
             f"→ {ls_count} 件確認"),
        ]
        for i, (q, passed, detail) in enumerate(machine_items):
            y = 5.85 - i * 0.7
            mark = "○" if passed else "△"
            mark_color = "#FFA640" if passed else "#7FE07F"
            ax.text(8.85, y, mark, ha="left", va="center",
                    color=mark_color, fontsize=18, fontweight="bold")
            ax.text(9.6, y + 0.13, q.split("\n")[0], ha="left", va="center",
                    color="white", fontsize=11, fontweight="bold")
            if "\n" in q:
                ax.text(9.6, y - 0.18, q.split("\n")[1], ha="left", va="center",
                        color="white", fontsize=11, fontweight="bold")
            ax.text(15.3, y, detail, ha="right", va="center",
                    color=(0.9, 0.85, 0.7), fontsize=10, style="italic")

        ax.text(11.95, 3.0, f"{machine_score} / 3 軸 反論あり",
                ha="center", va="center", color="#FFA640",
                fontsize=18, fontweight="bold")
        ax.text(11.95, 2.35, "機種そのものの構造も、",
                ha="center", va="center", color=(1.0, 0.95, 0.85), fontsize=11)
        ax.text(11.95, 1.95, "それだけで脳汁を呼んでいた",
                ha="center", va="center", color=(1.0, 0.95, 0.85),
                fontsize=11, style="italic")

        # ── 中央の橋渡しメッセージ ──
        if local_frame > FPS * 5:
            ax.text(8, 0.95,
                    "→ 仮説は部分的に支持されたが、機種の力も無視できない",
                    ha="center", va="center", color="#FFD700",
                    fontsize=13, fontweight="bold", style="italic")
            ax.text(8, 0.4,
                    "では、本当の脳汁の正体は何か？",
                    ha="center", va="center", color="white",
                    fontsize=12, fontweight="bold")

    # ── update 関数 ────────────────────────────────
    def draw_phase8(local_frame, total):
        """結論（v4.6.8: 横塚指示で「反論」から「結論」セクションに書き換え）。

        第三者でも一目でわかる結論プレゼンテーション。
        反論軸の数値は「人 × 機種の合作」というメッセージに昇華する。
        """
        clear()
        ax.text(8, 8.5, "結論",
                ha="center", va="center", color="#FFD700",
                fontsize=26, fontweight="bold")
        ax.text(8, 7.85,
                "1,000 人 × 6 機種 × 50 ステップのシミュレーションが教えてくれたこと",
                ha="center", va="center", color=(0.85, 0.85, 0.9),
                fontsize=12, style="italic")

        # ── 左: 人の心理だけでは足りない ──
        ax.add_patch(patches.FancyBboxPatch(
            (0.5, 4.4), 7.1, 2.8,
            boxstyle="round,pad=0.05,rounding_size=0.18",
            linewidth=2.0, edgecolor="#7AC8FF",
            facecolor=(0.05, 0.10, 0.18), alpha=0.85))
        ax.text(4.05, 6.75, "人の心理 だけでは",
                ha="center", va="center", color="#7AC8FF",
                fontsize=14, fontweight="bold")
        ax.text(4.05, 6.05, "脳汁ピークは説明できない",
                ha="center", va="center", color="white",
                fontsize=15, fontweight="bold")
        ax.text(4.05, 5.20, "中毒者でなくても爆発する人はいたし、",
                ha="center", va="center", color=(0.9, 0.9, 1.0), fontsize=11)
        ax.text(4.05, 4.75, "ストレスが低くても大爆発は起きた",
                ha="center", va="center", color=(0.9, 0.9, 1.0), fontsize=11)

        # ── 右: 機種の力も、それだけで脳汁を呼ぶ ──
        ax.add_patch(patches.FancyBboxPatch(
            (8.4, 4.4), 7.1, 2.8,
            boxstyle="round,pad=0.05,rounding_size=0.18",
            linewidth=2.0, edgecolor="#FFA640",
            facecolor=(0.18, 0.10, 0.04), alpha=0.85))
        ax.text(11.95, 6.75, "機種の構造 もまた",
                ha="center", va="center", color="#FFA640",
                fontsize=14, fontweight="bold")
        ax.text(11.95, 6.05, "それだけで脳汁を呼んでいた",
                ha="center", va="center", color="white",
                fontsize=15, fontweight="bold")
        ax.text(11.95, 5.20, "「爆発の天井」と「滅多に来ない引き金」が",
                ha="center", va="center", color=(1.0, 0.95, 0.85), fontsize=11)
        ax.text(11.95, 4.75, "それ自体で脳汁を呼び寄せた",
                ha="center", va="center", color=(1.0, 0.95, 0.85), fontsize=11)

        # ── 中央の橋渡し（× 記号で対話を表現） ──
        if local_frame > FPS * 3:
            ax.text(8, 5.8, "×",
                    ha="center", va="center", color="#FFD700",
                    fontsize=36, fontweight="bold")

        # ── 真の知見 ──
        if local_frame > FPS * 5:
            ax.add_patch(patches.FancyBboxPatch(
                (1.0, 1.0), 14.0, 2.8,
                boxstyle="round,pad=0.05,rounding_size=0.22",
                linewidth=2.6, edgecolor="#FFD700",
                facecolor=(0.10, 0.10, 0.20), alpha=0.93))
            ax.text(8, 3.25, "【 真の知見 】",
                    ha="center", va="center", color="#FFD700",
                    fontsize=13, fontweight="bold")
            ax.text(8, 2.50,
                    "両者が交差した瞬間に、最大の興奮が生まれる",
                    ha="center", va="center", color="white",
                    fontsize=17, fontweight="bold")
            ax.text(8, 1.55,
                    "パチスロホールの脳汁は、「人」と「機種」の合作である",
                    ha="center", va="center", color=(0.95, 0.95, 1.0),
                    fontsize=13, fontweight="bold", style="italic")

    # ── Phase 10: 同じ状況、違う判断 — 状況軸での観察 ──
    situations_data = load_llm_situations()

    SCENE_COLORS = ["#E04545", "#FFD700", "#7AC8FF", "#F0A030", "#A878D4"]
    SCENE_LABELS_FOR_INTRO = [
        "大きく負けている",
        "大きく勝った直後",
        "収支がトントン",
        "連敗が続く",
        "連チャン終了直後",
    ]
    INTRO_SECS = 8
    SCENE_SECS = 5

    def draw_phase10_intro(local_frame: int):
        """Phase 10 の説明スライド（8 秒）。"""
        fade_alpha = min(1.0, local_frame / (FPS * 0.5))

        # タイトル
        ax.text(8, 8.10, "これから観察するもの",
                ha="center", va="center", color="#FFD700",
                fontsize=26, fontweight="bold", alpha=fade_alpha)
        # 区切り線
        ax.plot([4.0, 12.0], [7.55, 7.55], color="#3A3A50",
                linewidth=1.0, alpha=fade_alpha)

        # 説明文 3 行
        ax.text(8, 6.95, "5 つの状況シーンに、8 人の代表（属性ごと 1 人）を置く。",
                ha="center", va="center", color="white",
                fontsize=14, alpha=fade_alpha)
        ax.text(8, 6.40, "同じ状況を見せたとき、属性ごとに判断がどう分かれるかを観察する。",
                ha="center", va="center", color="white",
                fontsize=14, alpha=fade_alpha)
        # 段階的に出る LLM クレジット
        if local_frame > FPS * 1.5:
            credit_alpha = min(1.0, (local_frame - FPS * 1.5) / (FPS * 0.6))
            ax.text(8, 5.70, "すべての判断は LLM によるもの。",
                    ha="center", va="center", color=(0.95, 0.85, 0.6),
                    fontsize=13, fontweight="bold",
                    alpha=credit_alpha * fade_alpha, style="italic")

        # 5 状況のリスト（段階的に出現）
        list_header_alpha = min(1.0, max(0.0, (local_frame - FPS * 2.5) / (FPS * 0.6)))
        ax.text(8, 4.65, "これから観察する 5 つの状況",
                ha="center", va="center", color=(0.7, 0.85, 1.0),
                fontsize=12, fontweight="bold", alpha=list_header_alpha * fade_alpha)

        for i, label in enumerate(SCENE_LABELS_FOR_INTRO):
            item_appear = FPS * (3.2 + i * 0.5)
            item_alpha = min(1.0, max(0.0, (local_frame - item_appear) / (FPS * 0.4)))
            color = SCENE_COLORS[i]
            y = 3.85 - i * 0.65
            # 番号バッジ
            ax.add_patch(patches.Circle(
                (5.0, y), 0.22,
                linewidth=1.6, edgecolor=color,
                facecolor=(0.10, 0.10, 0.18),
                alpha=0.85 * item_alpha * fade_alpha))
            ax.text(5.0, y, f"{i + 1}",
                    ha="center", va="center", color=color,
                    fontsize=12, fontweight="bold",
                    alpha=item_alpha * fade_alpha)
            # ラベル
            ax.text(5.55, y, label,
                    ha="left", va="center", color="white",
                    fontsize=13, alpha=item_alpha * fade_alpha)

    def draw_phase10(local_frame, total):
        """8 秒の説明 + 5 状況シーン × 5 秒の判断観察 = 33 秒。"""
        clear()
        INTRO_FRAMES = FPS * INTRO_SECS

        if local_frame < INTRO_FRAMES:
            draw_phase10_intro(local_frame)
            return

        scene_local = local_frame - INTRO_FRAMES
        CP_FRAMES = FPS * SCENE_SECS
        cp_idx = min(scene_local // CP_FRAMES, 4)
        cp_local = scene_local - cp_idx * CP_FRAMES
        fade_alpha = min(1.0, cp_local / (FPS * 0.5))

        scenes = situations_data.get("scenes", [])
        if cp_idx >= len(scenes):
            return
        scene = scenes[cp_idx]
        situations = scene.get("situations", [])
        decisions = scene.get("decisions", [])

        # ── タイトル ──
        ax.text(8, 8.62, "同じ状況、違う判断 — 8 人はどう動くか",
                ha="center", va="center", color="#FFD700",
                fontsize=22, fontweight="bold", alpha=fade_alpha)
        ax.text(8, 8.18,
                "状況だけが与えられたとき、属性ごとに判断はどう分かれるか",
                ha="center", va="center", color=(0.85, 0.85, 0.9),
                fontsize=11, style="italic", alpha=fade_alpha)

        # ── 状況描写（リッチ） ──
        ax.text(0.5, 7.55, f"シーン {cp_idx + 1} / 5",
                ha="left", va="center", color="#7AC8FF",
                fontsize=11, fontweight="bold", alpha=fade_alpha)
        ax.text(15.5, 7.55, scene.get("label", ""),
                ha="right", va="center", color=(0.95, 0.85, 0.6),
                fontsize=11, fontweight="bold", alpha=fade_alpha)
        # 状況タイトル
        ax.text(8, 7.05, scene.get("title", ""),
                ha="center", va="center", color="white",
                fontsize=13, fontweight="bold", alpha=fade_alpha)
        # 状況の説明（自然文）
        ax.text(8, 6.60, scene.get("description", ""),
                ha="center", va="center", color=(0.85, 0.85, 0.95),
                fontsize=10.5, alpha=fade_alpha)
        # 区切り線
        ax.plot([0.4, 15.6], [6.25, 6.25], color="#3A3A50",
                linewidth=0.8, alpha=fade_alpha)

        # ── 8 人カード（4 列 × 2 行）──
        col_w = 3.7
        row_h = 2.85
        col_xs = [0.4, 4.2, 8.0, 11.8]
        row_ys = [3.20, 0.30]  # 上段, 下段

        n = min(len(situations), len(decisions), 8)
        for i in range(n):
            sit = situations[i]
            dec = decisions[i] if i < len(decisions) else {}
            attr_code = sit.get("attr_code", "?")
            color = ATTR_COLOR.get(attr_code, "#FFFFFF")

            row = i // 4
            col = i % 4
            x0 = col_xs[col]
            y0 = row_ys[row]

            # カード背景
            ax.add_patch(patches.FancyBboxPatch(
                (x0, y0), col_w, row_h,
                boxstyle="round,pad=0.04,rounding_size=0.10",
                linewidth=1.4, edgecolor=color,
                facecolor=(0.07, 0.07, 0.12), alpha=0.85 * fade_alpha))

            # 属性名
            ax.text(x0 + 0.18, y0 + row_h - 0.30, sit.get("name", "?"),
                    ha="left", va="center", color=color,
                    fontsize=14, fontweight="bold", alpha=fade_alpha)

            # action ラベル（右上）
            action = dec.get("action", "")
            a_color = PHASE3_5_ACTION_COLOR.get(action, "#FFFFFF")
            a_label = PHASE3_5_ACTION_LABEL.get(action, action)
            ax.add_patch(patches.FancyBboxPatch(
                (x0 + col_w - 1.05, y0 + row_h - 0.55), 0.90, 0.42,
                boxstyle="round,pad=0.02,rounding_size=0.08",
                linewidth=1.2, edgecolor=a_color,
                facecolor=a_color, alpha=0.18 * fade_alpha))
            ax.text(x0 + col_w - 0.60, y0 + row_h - 0.34, a_label,
                    ha="center", va="center", color=a_color,
                    fontsize=11, fontweight="bold", alpha=fade_alpha)

            # 機種 + 収支（コンパクト）
            ax.text(x0 + 0.18, y0 + row_h - 0.78, sit.get("machine", "?"),
                    ha="left", va="center", color=(0.7, 0.7, 0.8),
                    fontsize=8.5, alpha=fade_alpha)
            cash_state = sit.get("cash_state", "")
            ax.text(x0 + 0.18, y0 + row_h - 1.05, cash_state,
                    ha="left", va="center", color=(0.85, 0.85, 0.95),
                    fontsize=8.5, alpha=fade_alpha)

            # 直近の状況を自然文で（データ側で linguify 済みの recent_text を使う）
            recent_text = sit.get("recent_text") or linguify_recent_pattern(sit.get("recent_10", ""))
            ax.text(x0 + 0.18, y0 + row_h - 1.32, recent_text,
                    ha="left", va="center", color=(0.7, 0.85, 0.7),
                    fontsize=8.5, alpha=fade_alpha)

            # 心の声
            voice = dec.get("voice", "")
            ax.text(x0 + 0.18, y0 + row_h - 1.78, f"「{voice}」",
                    ha="left", va="center", color="white",
                    fontsize=11, fontweight="bold", alpha=fade_alpha)

            # 解釈（belief）
            belief = dec.get("belief", "")
            if belief:
                ax.text(x0 + 0.18, y0 + row_h - 2.18, f"解釈: {belief}",
                        ha="left", va="center", color=(0.95, 0.85, 0.6),
                        fontsize=8.5, style="italic", alpha=fade_alpha)

            # 判断理由（reason）
            reason = dec.get("reason", "")
            if reason:
                ax.text(x0 + 0.18, y0 + row_h - 2.55, reason,
                        ha="left", va="center", color=(0.65, 0.65, 0.75),
                        fontsize=8, alpha=fade_alpha)

        # ── フッター ──
        ax.text(8, 0.10,
                "LLM が見られるのは「属性・現在の所持金・直近の流れ・ホールの雰囲気・本人の状態」のみ。次の抽選結果は知らない。",
                ha="center", va="center", color=(0.55, 0.55, 0.65),
                fontsize=8, style="italic", alpha=fade_alpha)

    # ── Phase 9: AI が生んだ 8 つの感情（Persona Reaction Probe 観察） ──
    probe_data = load_persona_probe()
    PAGE_FRAMES = FPS * 4  # 1 ページ 4 秒

    def draw_phase9(local_frame, total):
        """各ペルソナ 1 ページ × 8 = 32 秒。5 場面のコメントを忠実に並べる。"""
        clear()
        page_idx = min(local_frame // PAGE_FRAMES, 7)
        page_local = local_frame - page_idx * PAGE_FRAMES
        fade_alpha = min(1.0, page_local / (FPS * 0.4))

        attr_code, persona_id = PHASE9_PERSONA_ORDER[page_idx]
        color = ATTR_COLOR.get(attr_code, "#FFFFFF")
        persona = probe_data.get("personas", {}).get(persona_id, {})
        scenes_for_p = probe_data.get("by_persona", {}).get(persona_id, [])

        # ── 上部タイトル ──
        ax.text(8, 8.55, "AI が生んだ 8 つの感情",
                ha="center", va="center", color="#FFD700",
                fontsize=22, fontweight="bold", alpha=fade_alpha)
        ax.text(8, 8.05,
                "同じ群衆の中で、属性ごとに違う心が立ち上がる ── 観察の判断は人間に委ねる",
                ha="center", va="center", color=(0.85, 0.85, 0.9),
                fontsize=11, style="italic", alpha=fade_alpha)

        # ── ページインジケータ ──
        ax.text(15.5, 8.55, f"{page_idx + 1} / 8",
                ha="right", va="center", color=(0.6, 0.6, 0.7),
                fontsize=11, alpha=fade_alpha)

        # ── ペルソナヘッダ ──
        ax.add_patch(patches.FancyBboxPatch(
            (0.4, 6.85), 15.2, 0.95,
            boxstyle="round,pad=0.04,rounding_size=0.12",
            linewidth=1.6, edgecolor=color,
            facecolor=(0.10, 0.10, 0.18), alpha=0.85 * fade_alpha))
        ax.text(0.7, 7.32, persona.get("name", "?"),
                ha="left", va="center", color=color,
                fontsize=20, fontweight="bold", alpha=fade_alpha)
        sub = f"{persona.get('age', '?')} 歳・{persona.get('gender', '?')}・{persona.get('style', '')}"
        ax.text(5.8, 7.32, sub,
                ha="left", va="center", color=(0.85, 0.85, 0.95),
                fontsize=10, alpha=fade_alpha)

        # ── 5 場面 × コメント ──
        # 表ヘッダ
        ax.text(0.7, 6.30, "場面",
                ha="left", va="center", color="#88AAFF",
                fontsize=10, fontweight="bold", alpha=fade_alpha)
        ax.text(4.0, 6.30, "心の声",
                ha="left", va="center", color="#88AAFF",
                fontsize=10, fontweight="bold", alpha=fade_alpha)
        ax.text(11.5, 6.30, "感情",
                ha="left", va="center", color="#88AAFF",
                fontsize=10, fontweight="bold", alpha=fade_alpha)
        ax.text(13.7, 6.30, "意図",
                ha="left", va="center", color="#88AAFF",
                fontsize=10, fontweight="bold", alpha=fade_alpha)
        # 区切り線
        ax.plot([0.5, 15.5], [6.05, 6.05], color="#3A3A50",
                linewidth=0.8, alpha=fade_alpha)

        # 5 行表示
        n_scenes = min(len(scenes_for_p), 5)
        for i in range(n_scenes):
            r = scenes_for_p[i]
            scene_label = r.get("scene_label", "?")
            output = r.get("output", {})
            voice = output.get("voice", "—")
            emotion = output.get("emotion", "—")
            action_intent = output.get("action_intent", "—")
            y = 5.55 - i * 0.95

            # 場面ラベル（カラーバー）
            ax.add_patch(patches.Rectangle(
                (0.5, y - 0.32), 0.10, 0.64,
                linewidth=0, facecolor=color, alpha=0.85 * fade_alpha))
            ax.text(0.78, y, scene_label,
                    ha="left", va="center", color="white",
                    fontsize=10.5, fontweight="bold", alpha=fade_alpha)

            # 心の声
            ax.text(4.0, y, f"「{voice}」",
                    ha="left", va="center", color="white",
                    fontsize=12.5, alpha=fade_alpha)

            # emotion
            ax.text(11.5, y, emotion,
                    ha="left", va="center", color=(0.95, 0.85, 0.6),
                    fontsize=10.5, alpha=fade_alpha)

            # action_intent
            ax.text(13.7, y, action_intent,
                    ha="left", va="center", color=(0.85, 0.95, 0.85),
                    fontsize=10.5, alpha=fade_alpha)

        # ── フッター ──
        ax.text(8, 0.45,
                "Persona Reaction Probe — 5 場面 × 8 ペルソナ = 40 件、すべて忠実に表示",
                ha="center", va="center", color=(0.55, 0.55, 0.65),
                fontsize=9, style="italic", alpha=fade_alpha)

    phase_dispatch = {
        "phase1": draw_phase1,
        "phase_attrs": draw_phase_attrs,        # v4.6.13: 8 属性の人物紹介
        "phase_machines": draw_phase_machines,  # v4.6.14: 6 機種の機種紹介
        "phase2": draw_phase2,
        "phase3": draw_phase3,
        "phase4": draw_phase4,
        "phase5": draw_phase5,
        "phase6": draw_phase6,
        "phase7": draw_phase7,
        "phase8": draw_phase8,
        "phase9": draw_phase9,                  # v4.6.20: AI が生んだ 8 つの感情
        "phase10": draw_phase10,                # v4.6.22: LLM に未来は見せない
    }

    def update(frame):
        for name, start, end in ranges:
            if start <= frame < end:
                phase_dispatch[name](frame - start, end - start)
                break
        return []

    print(f"  total frames: {total_frames}（{total_frames / FPS:.1f} 秒）")
    anim = FuncAnimation(fig, update, frames=total_frames, interval=1000 // FPS, blit=False)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    writer = FFMpegWriter(fps=FPS, bitrate=3200, codec="libx264")
    anim.save(str(out_path), writer=writer)
    plt.close(fig)


# ============ ターミナル要約（おまけ）============

def print_summary(summaries: list[PersonaSummary], records: list[StepRecord]) -> None:
    print("\n=== 属性別 max ストレス平均（仮説検証 ①）===")
    for acode, v in sorted(attribute_stress_means(summaries).items(), key=lambda x: -x[1]):
        marker = "  ← 仮説対象 C" if acode == "C_CHASE" else ""
        print(f"  {ATTR_DISPLAY[acode]:<10}  max stress 平均 {v:.3f}{marker}")

    print("\n=== 中毒者 × 機種別 Δ脳汁平均（仮説検証 ②）===")
    cmb = chase_machine_brain_means(records).get("C_CHASE", {})
    for mcode, v in sorted(cmb.items(), key=lambda x: -x[1]):
        print(f"  {mcode:<18}  +{v:.1f}")

    print("\n=== 最高幸福ランキング Top 5 ===")
    for i, s in enumerate(sorted(summaries, key=lambda x: -x.total_happiness)[:5], 1):
        print(f"  {i}. {s.pid:<20} {ATTR_DISPLAY[s.attribute]:<10} × {s.machine:<13} "
              f"幸福 {s.total_happiness:>+7.0f}  Δ脳汁 +{s.max_brain_delta:.0f}")

    print("\n=== 最高ストレスランキング Top 5 ===")
    for i, s in enumerate(sorted(summaries, key=lambda x: -x.max_stress)[:5], 1):
        print(f"  {i}. {s.pid:<20} {ATTR_DISPLAY[s.attribute]:<10} × {s.machine:<13} "
              f"max stress {s.max_stress:.3f} (step{s.max_stress_step})")


# ============ メイン ============

def main() -> None:
    print("=== Step 1: 1000 人生成 + 48 セル配分 ===")
    personas = generate_population(n_per_attr=125, seed=42)
    assign_machines(personas, seed=42)

    print("\n=== Step 2: 50 step フルシミュレーション（興奮量 + ストレス + 幸福度）===")
    records = run_full_simulation(personas, n_steps=50, seed=1234)
    print(f"  records: {len(records)}")

    print("\n=== Step 3: 集計 ===")
    summaries = summarize_personas(personas, records)

    print_summary(summaries, records)

    print("\n=== Step 4: 動画書き出し（Phase 1-6 統合）===")
    out_path = Path(__file__).resolve().parents[1] / "outputs" / "spike_v44_demo.mp4"
    print(f"  出力先: {out_path}")
    render_demo(personas, records, summaries, out_path)
    print(f"  完了: {out_path}")


if __name__ == "__main__":
    main()
