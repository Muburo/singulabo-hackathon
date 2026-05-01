"""
spike_v43.py — v4.3 仕様の Step 1（schema 固定）

v4.2 で観察された歪み（機種別質感差なし、上乗せ・特化の軽重なし、stress_load 固定、
sensory_gating の命名と動作の乖離、Top 5 が物語化しない）を補正するための schema 拡張。

Step 1（このファイル）で固めた schema:
- MachineType に bonus_excitement_multiplier / chain_start_impact /
  continuation_excitement_multiplier / event_impacts / event_probs を追加
- 4 機種を ChatGPT Pro v4.3 案にリブランド（PURE_A / ART_45 / ART_2010 / GOD_OKI）
- Persona の sensory_gating → sensory_amplitude にリネーム
- dopamine_sensitivity 派生ヘルパー追加
- trigger_event を light/heavy に拡張（uwanose_light/heavy, tokka_light/heavy, kakutei_engi）
- update_emotions を「身体反応 + dopamine_burst（event_impact 駆動）」に分離

未着手（後続 Step）:
- light/heavy の物理影響（chain_stock, force_next_hit）         → Step 2
- stress_load 動的更新（baseline_stress + situational_stress）  → Step 3
- raw_top5 / stratified_highlights 分離                        → Step 5
- LLM voice 統合                                              → Step 6
"""
import random
from dataclasses import dataclass, field
from math import exp, log, sqrt, tanh

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = "Hiragino Sans"
plt.rcParams["axes.unicode_minus"] = False


# ============ 機種パラメータ（v4.3 機種別質感差込み）============
@dataclass
class MachineType:
    name: str
    color: str
    chain_mode: str          # "none" / "chain"
    p_initial_hit: float
    continue_prob: float
    payout_mean: float
    payout_std: float
    payout_cap: float
    # v4.3 機種別の興奮度倍率（ChatGPT Pro v4.3 案）
    bonus_excitement_multiplier: float = 1.0   # chain_start 時の身体反応スケール
    chain_start_impact: float = 0.40           # 大逆転認知（意味づけ）の重み
    continuation_excitement_multiplier: float = 0.7  # 連荘中の小当たり身体反応
    # v4.3 中間イベント抽選確率（chain_active=True で eligible、kakutei は any step 可）
    event_probs: dict = field(default_factory=dict)
    # v4.3 trigger_event ごとの大逆転認知の重み（dopamine_burst の event_impact）
    # NOTE: chain_start エントリは __post_init__ で chain_start_impact から自動同期される。
    event_impacts: dict = field(default_factory=dict)
    stake: int = 1000

    def __post_init__(self):
        # v4.3: chain_start_impact を SSoT として event_impacts["chain_start"] に同期
        # （手書きで両方に書くと二重 SSoT になり、調整時に齟齬が出るため）
        self.event_impacts["chain_start"] = self.chain_start_impact

    @property
    def payout_mu(self):
        return log(self.payout_mean) - 0.5 * log(1 + (self.payout_std / self.payout_mean) ** 2)

    @property
    def payout_sigma(self):
        return sqrt(log(1 + (self.payout_std / self.payout_mean) ** 2))


# ChatGPT Pro v4.3 提案値: 100 step 内で物語が出る校正値（実機確率の忠実再現ではない）
MACHINE_TYPES = [
    MachineType(
        name="PURE_A", color="#5cb85c", chain_mode="none",
        p_initial_hit=0.200, continue_prob=0.00,
        payout_mean=5000, payout_std=2000, payout_cap=20000,
        bonus_excitement_multiplier=0.65,
        chain_start_impact=0.20,
        continuation_excitement_multiplier=0.55,
        # 純A は中間イベントなし（実機でもジャグラーのプレミア告知は当たり確定告知に過ぎず、
        # 興奮の爆発は伴わない。横塚の実機判断 2026-05-01 で削除）
        event_probs={},
        event_impacts={},  # chain_start は __post_init__ で自動同期
    ),
    MachineType(
        name="ART_45", color="#f0ad4e", chain_mode="chain",
        p_initial_hit=0.060, continue_prob=0.58,
        payout_mean=8300, payout_std=5600, payout_cap=80000,
        bonus_excitement_multiplier=1.00,
        chain_start_impact=0.35,
        continuation_excitement_multiplier=0.70,
        event_probs={
            "uwanose_light": 0.025, "uwanose_heavy": 0.002,
            "tokka_light":   0.010, "tokka_heavy":   0.0008,
            "kakutei_engi":  0.0004,
        },
        event_impacts={
            "uwanose_light": 0.35, "uwanose_heavy": 0.90,
            "tokka_light":   0.55, "tokka_heavy":   1.10,
            "kakutei_engi":  1.20,
        },  # chain_start は __post_init__ で chain_start_impact から自動同期
    ),
    MachineType(
        name="ART_2010", color="#5bc0de", chain_mode="chain",
        p_initial_hit=0.030, continue_prob=0.83,
        payout_mean=6700, payout_std=4000, payout_cap=60000,
        bonus_excitement_multiplier=1.35,
        chain_start_impact=0.52,
        continuation_excitement_multiplier=0.75,
        event_probs={
            "uwanose_light": 0.045, "uwanose_heavy": 0.006,
            "tokka_light":   0.030, "tokka_heavy":   0.003,
            "kakutei_engi":  0.0009,
        },
        event_impacts={
            "uwanose_light": 0.42, "uwanose_heavy": 1.05,
            "tokka_light":   0.65, "tokka_heavy":   1.25,
            "kakutei_engi":  1.45,
        },  # chain_start は __post_init__ で chain_start_impact から自動同期
    ),
    MachineType(
        name="GOD_OKI", color="#d9534f", chain_mode="chain",
        p_initial_hit=0.025, continue_prob=0.50,
        payout_mean=21000, payout_std=25000, payout_cap=120000,
        bonus_excitement_multiplier=2.20,
        chain_start_impact=0.75,
        continuation_excitement_multiplier=0.65,
        event_probs={
            "uwanose_light": 0.015, "uwanose_heavy": 0.005,
            "tokka_light":   0.008, "tokka_heavy":   0.004,
            "kakutei_engi":  0.0012,
        },
        event_impacts={
            "uwanose_light": 0.35, "uwanose_heavy": 1.15,
            "tokka_light":   0.60, "tokka_heavy":   1.45,
            "kakutei_engi":  1.65,
        },  # chain_start は __post_init__ で chain_start_impact から自動同期
    ),
]


# ============ persona ============
@dataclass
class Persona:
    pid: str
    category: str
    color: str
    cash: int
    sensory_amplitude: float   # v4.3: 旧 sensory_gating（命名と動作の乖離を解消）
    base_arousal: float
    base_despair: float
    base_stress: float        # v4.2: 持続的ストレス傾向
    arousal: float = 0.0
    despair: float = 0.0
    machine_idx: int = 0
    chain_active: bool = False
    chain_step_count: int = 0
    miss_streak: int = 0
    win_streak: int = 0
    active: bool = True
    # 特化ゾーン
    tokka_zone_active: bool = False
    tokka_zone_remaining: int = 0


@dataclass
class SessionContext:
    """その日の状況（stress_load の構成要素）"""
    pid: str
    borrow_burden: float
    work_stress: float
    life_dissatisfaction: float
    social_commitment_density: float = 0.0
    commitment_intensity: float = 0.0


def make_personas_and_sessions():
    """8 persona、stress_load の幅広い分布"""
    personas = [
        Persona("p01", "依存症末期", "#8B0000", 30000, 0.95, 70, 75, base_stress=0.75),
        Persona("p02", "中年現役",   "#FF6347", 40000, 0.80, 55, 50, base_stress=0.55),
        Persona("p03", "主婦",       "#FFB6C1", 15000, 0.70, 50, 45, base_stress=0.40),
        Persona("p04", "女子大生",   "#DA70D6", 10000, 0.85, 60, 40, base_stress=0.30),
        Persona("p05", "不労所得",   "#4682B4", 80000, 0.60, 45, 30, base_stress=0.10),
        Persona("p06", "年金高齢",   "#808080", 20000, 0.50, 40, 55, base_stress=0.45),
        Persona("p07", "夜職女性",   "#9370DB", 50000, 0.85, 65, 55, base_stress=0.65),
        Persona("p08", "退職前男性", "#2F4F4F", 35000, 0.70, 50, 50, base_stress=0.50),
    ]
    sessions = {
        "p01": SessionContext("p01", borrow_burden=0.85, work_stress=0.50, life_dissatisfaction=0.80),
        "p02": SessionContext("p02", borrow_burden=0.40, work_stress=0.85, life_dissatisfaction=0.55),
        "p03": SessionContext("p03", borrow_burden=0.20, work_stress=0.30, life_dissatisfaction=0.55),
        "p04": SessionContext("p04", borrow_burden=0.10, work_stress=0.40, life_dissatisfaction=0.40),
        "p05": SessionContext("p05", borrow_burden=0.05, work_stress=0.10, life_dissatisfaction=0.15),
        "p06": SessionContext("p06", borrow_burden=0.30, work_stress=0.10, life_dissatisfaction=0.50),
        "p07": SessionContext("p07", borrow_burden=0.70, work_stress=0.65, life_dissatisfaction=0.60),
        "p08": SessionContext("p08", borrow_burden=0.45, work_stress=0.70, life_dissatisfaction=0.45),
    }
    return personas, sessions


def compute_stress_load(persona, session):
    """v4.2: stress_load の合成"""
    return min(1.0, max(0.0,
        0.30 * persona.base_stress
      + 0.30 * session.borrow_burden
      + 0.20 * session.work_stress
      + 0.10 * session.life_dissatisfaction
      + 0.10 * session.social_commitment_density * session.commitment_intensity
    ))


# ============ 物理（v4.2: 中間イベント込み）============
def play(persona, mt, rng):
    """1 step の抽選 + 中間イベント"""
    persona.cash -= mt.stake
    hit, payout = False, 0
    trigger_event = "none"
    uwanose_amount = 0
    chain_just_started = False
    tokka_zone_entry = False
    kakutei_engi = False

    if mt.chain_mode == "none":
        # 純A: 当たれば trigger_event = "chain_start"（連荘なしなので chain_active は false 継続）
        # 中間イベントなし（純Aは「単発の入り口」が主役、ChatGPT Pro v4.3 案）
        if rng.random() < mt.p_initial_hit:
            hit = True
            payout = min(rng.lognormal(mt.payout_mu, mt.payout_sigma), mt.payout_cap)
            chain_just_started = True
            trigger_event = "chain_start"
        persona.chain_active = False
        persona.chain_step_count = 0
        persona.tokka_zone_active = False
    else:
        if persona.chain_active:
            # 連荘中: 特化ゾーンが active なら継続率を上書き
            cont_prob = 0.95 if persona.tokka_zone_active else mt.continue_prob
            if rng.random() < cont_prob:
                hit = True
                payout = min(rng.lognormal(mt.payout_mu, mt.payout_sigma), mt.payout_cap)
                persona.chain_step_count += 1

                # 中間イベント抽選（v4.3: event_probs テーブル方式、light/heavy 分離）
                # NOTE: event_probs は「chain_active かつ hit 成功 step」あたりの実効確率として運用。
                # ChatGPT Pro v4.3 案の「chain_active step あたり」よりは出現頻度が低い
                # （実機のセオリー「上乗せ抽選は当たり確定後」に揃えた解釈）。
                # 設計表記値と実効値の差は calibration（Step 4）で実測値を出して説明する。
                roll = rng.random()
                cumulative = 0.0
                for evt in ("kakutei_engi", "tokka_heavy", "tokka_light",
                            "uwanose_heavy", "uwanose_light"):
                    p = mt.event_probs.get(evt, 0.0)
                    if p <= 0:
                        continue
                    cumulative += p
                    if roll < cumulative:
                        trigger_event = evt
                        if evt == "kakutei_engi":
                            kakutei_engi = True
                            persona.tokka_zone_active = True
                            persona.tokka_zone_remaining = int(rng.integers(20, 40))
                            uwanose_amount = int(rng.choice([300, 500, 750]))
                        elif evt == "tokka_heavy":
                            tokka_zone_entry = True
                            persona.tokka_zone_active = True
                            persona.tokka_zone_remaining = int(rng.integers(20, 40))
                        elif evt == "tokka_light":
                            tokka_zone_entry = True
                            persona.tokka_zone_active = True
                            persona.tokka_zone_remaining = int(rng.integers(8, 18))
                        elif evt == "uwanose_heavy":
                            uwanose_amount = int(rng.choice([300, 500, 750, 1000]))
                        elif evt == "uwanose_light":
                            uwanose_amount = int(rng.choice([50, 100, 150, 200]))
                        break
            else:
                persona.chain_active = False
                persona.chain_step_count = 0
                persona.tokka_zone_active = False
                persona.tokka_zone_remaining = 0
        else:
            if rng.random() < mt.p_initial_hit:
                hit = True
                payout = min(rng.lognormal(mt.payout_mu, mt.payout_sigma), mt.payout_cap)
                persona.chain_active = True
                persona.chain_step_count = 1
                chain_just_started = True
                trigger_event = "chain_start"

    # 特化ゾーンの残り step を減らす
    if persona.tokka_zone_active and persona.tokka_zone_remaining > 0:
        persona.tokka_zone_remaining -= 1
        if persona.tokka_zone_remaining <= 0:
            persona.tokka_zone_active = False

    persona.cash += int(payout)
    if hit:
        persona.miss_streak = 0
        persona.win_streak += 1
    else:
        persona.miss_streak += 1
        persona.win_streak = 0

    return {
        "hit": hit,
        "payout": int(payout),
        "trigger_event": trigger_event,
        "uwanose_amount": uwanose_amount,
        "chain_just_started": chain_just_started,
        "tokka_zone_entry": tokka_zone_entry,
        "kakutei_engi": kakutei_engi,
    }


def dopamine_sensitivity(persona):
    """v4.3: sensory_amplitude から大逆転認知への感受性を派生（0.70〜1.25）"""
    return max(0.70, min(1.25, 0.75 + 0.45 * persona.sensory_amplitude))


def update_emotions(persona, event_info, mt, initial_cash, stress_load):
    """
    v4.3 感情モデル: 「身体反応」と「dopamine_burst（意味づけ）」を分離

    - hit_body_arousal: 機種別の身体反応（chain_start vs 連荘中の小当たり）
    - dopamine_burst:   trigger_event の event_impact × stress_load × dopamine_sensitivity
    """
    chain_just_started = event_info["chain_just_started"]
    trigger_event = event_info["trigger_event"]
    net_delta = event_info["payout"] - mt.stake
    gain_signal = tanh(max(0, net_delta) / 5000)
    loss_signal = tanh(max(0, -net_delta) / 3000)
    hammari_signal = 1 - exp(-persona.miss_streak / 12)
    cash_low = 1.0 if persona.cash <= 3000 else 0.0
    loss_ratio = max(0, (initial_cash - persona.cash) / max(1, initial_cash))

    # ---- arousal: 身体反応 + 一般項（背景） ----
    if chain_just_started:
        hit_body_arousal = 22.0 * mt.bonus_excitement_multiplier
    elif event_info["hit"]:
        hit_body_arousal = 12.0 * mt.continuation_excitement_multiplier
    else:
        hit_body_arousal = 0.0

    background = (
        + hit_body_arousal
        + 10.0 * gain_signal
        +  4.0 * hammari_signal
        -  3.0 * cash_low
    )
    # v4.3 B-lite: 背景項には弱めの感覚増幅（0.85〜1.15）を掛ける
    # 爆発項には dopamine_sensitivity を掛ける（dopamine_burst 内で既に適用）
    # → sensory_amplitude が二重に効く問題を回避（Codex P3 指摘）
    background_amplitude = 0.85 + 0.30 * persona.sensory_amplitude
    background *= background_amplitude

    # ---- arousal: dopamine_burst（大逆転認知 × stress × 感受性）----
    event_impact = mt.event_impacts.get(trigger_event, 0.0)
    dopamine_burst = (
        35.0
        * event_impact
        * (0.5 + 1.5 * stress_load)
        * dopamine_sensitivity(persona)
    )

    raw_da = background + dopamine_burst
    raw_da -= 0.05 * (persona.arousal - persona.base_arousal)
    persona.arousal = max(0.0, min(100.0, persona.arousal + raw_da))

    # ---- despair ----
    raw_dd = (
        + 16.0 * loss_signal
        + 12.0 * loss_ratio
        +  8.0 * cash_low
        +  5.0 * hammari_signal
        - 10.0 * gain_signal
    )
    # v4.2 から維持: stress_load で増幅、大逆転認知（event_impact）で救済
    raw_dd *= (1.0 + 0.6 * stress_load)
    raw_dd -= 8.0 * event_impact * stress_load

    raw_dd *= (0.7 + persona.base_despair / 100.0)
    persona.despair = max(0.0, min(100.0, persona.despair + raw_dd
                                          - 0.03 * (persona.despair - persona.base_despair)))

    return dopamine_burst


def maybe_switch(persona, n_machines, rng, hit):
    if persona.cash <= 0:
        persona.active = False
        return
    if hit and rng.random() < 0.15:  # 連荘中は移動しにくい
        if not persona.chain_active:
            new_idx = rng.integers(0, n_machines)
            if new_idx != persona.machine_idx:
                persona.machine_idx = int(new_idx)
                persona.chain_active = False


# ============ 心の声テンプレ（v4.2: trigger 連動）============
INNER_VOICE = {
    "kakutei_engi": ["確定！？　うそだろ", "もう、終わらない", "天井超えた、最高", "神様、ありがとう"],
    "tokka_zone_entry": ["特化ゾーンきた", "うわ、終わらない", "まだ続く！？", "やばい、止まらない"],
    "uwanose": ["上乗せきた", "200 上乗せ、おかわり", "まだ伸びる", "もうちょっと、もうちょっと"],
    "chain_start": ["きた、当たった", "ようやくか", "頼む、伸びてくれ", "ここから"],
    "焦燥": ["もう光るしかない", "頼む、一回だけ", "ここまで来て止まれない"],
    "熱狂": ["来る、絶対来る", "今日はイケる", "光れ、光れ"],
    "絶望": ["もう、お金が", "終わった、無理", "やめておけば"],
    "解離": ["...", "ふっ、またか", "（無感情）"],
    "凪": ["ふーん", "まあ、こんなもん"],
    "倦怠": ["退屈だな"],
    "普通": ["うーん", "...どうかな"],
}


def classify_state(arousal, despair):
    if arousal >= 75 and despair >= 65: return "焦燥"
    if arousal >= 75: return "熱狂"
    if despair >= 70 and arousal < 45: return "解離"
    if despair >= 65: return "絶望"
    if arousal < 35 and despair < 35: return "凪"
    if arousal < 35: return "倦怠"
    return "普通"


def get_inner_voice(arousal, despair, trigger_event, voice_rng):
    # trigger event 優先
    if "kakutei" in trigger_event:
        return voice_rng.choice(INNER_VOICE["kakutei_engi"])
    if "tokka" in trigger_event:
        return voice_rng.choice(INNER_VOICE["tokka_zone_entry"])
    if "uwanose" in trigger_event:
        return voice_rng.choice(INNER_VOICE["uwanose"])
    if "chain_start" in trigger_event:
        return voice_rng.choice(INNER_VOICE["chain_start"])
    state = classify_state(arousal, despair)
    return voice_rng.choice(INNER_VOICE[state])


# ============ シミュレーション ============
def run_simulation(rng, n_steps=50):
    personas, sessions = make_personas_and_sessions()
    initial_cash_map = {p.pid: p.cash for p in personas}
    for p in personas:
        p.arousal = p.base_arousal
        p.despair = p.base_despair
        p.machine_idx = int(rng.integers(0, len(MACHINE_TYPES)))

    log = []  # 1 step 1 row

    for step in range(1, n_steps + 1):
        for p in personas:
            if not p.active:
                continue

            mt = MACHINE_TYPES[p.machine_idx]
            session = sessions[p.pid]
            stress_load = compute_stress_load(p, session)

            prev_a = p.arousal
            prev_d = p.despair

            event_info = play(p, mt, rng)
            dopamine_burst = update_emotions(
                p, event_info, mt, initial_cash_map[p.pid], stress_load
            )

            arousal_delta = p.arousal - prev_a
            despair_delta = p.despair - prev_d
            event_impact = mt.event_impacts.get(event_info["trigger_event"], 0.0)

            log.append({
                "step": step,
                "pid": p.pid,
                "category": p.category,
                "color": p.color,
                "machine_idx": p.machine_idx,
                "machine_name": mt.name,
                "cash": p.cash,
                "arousal": p.arousal,
                "despair": p.despair,
                "arousal_delta": arousal_delta,
                "despair_delta": despair_delta,
                "trigger_event": event_info["trigger_event"],
                "uwanose_amount": event_info["uwanose_amount"],
                "hit": event_info["hit"],
                "chain_just_started": event_info["chain_just_started"],   # v4.3 罠1
                "payout": event_info["payout"],
                "stress_load": stress_load,
                "event_impact": event_impact,                              # v4.3: 旧 upset_recognition の置き換え（0〜1.65）
                "upset_recognition": min(1.0, event_impact),               # v4.2 系可視化との後方互換（0〜1 clamp）
                "explosion_term": dopamine_burst,                          # 旧名は維持（可視化が参照）
                "dopamine_burst": dopamine_burst,                          # v4.3 正式名
                "miss_streak": p.miss_streak,
                "chain_active": p.chain_active,
                "active": p.active,
            })

            maybe_switch(p, len(MACHINE_TYPES), rng, event_info["hit"])

    return log, personas, sessions


def extract_top5_peaks(log, threshold=20.0, top_n=5):
    candidates = sorted(
        [r for r in log if r["arousal_delta"] >= threshold],
        key=lambda r: r["arousal_delta"], reverse=True
    )
    selected = []
    for row in candidates:
        if len(selected) >= top_n:
            break
        is_dup = any(
            s["pid"] == row["pid"] and abs(s["step"] - row["step"]) <= 3
            for s in selected
        )
        if not is_dup:
            selected.append(row)
    return selected


def get_window(log, pid, step, before=5, after=5):
    return [
        r for r in log
        if r["pid"] == pid and (step - before) <= r["step"] <= (step + after)
    ]


# ============ 可視化 ============
MACHINE_POS = [(1, 2.5), (3, 2.5), (1, 0.8), (3, 0.8)]


def phase1_live(log, personas, n_steps=50):
    """ライブシミュレーション表示"""
    plt.ion()
    fig = plt.figure(figsize=(15, 8))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.4, 1])
    ax_hall = fig.add_subplot(gs[:, 0])
    ax_a = fig.add_subplot(gs[0, 1])
    ax_d = fig.add_subplot(gs[1, 1])

    ax_hall.set_xlim(0, 4.5); ax_hall.set_ylim(-1, 4)
    ax_hall.set_aspect("equal")
    ax_hall.set_xticks([]); ax_hall.set_yticks([])
    ax_hall.set_title("Phase 1: ライブシミュレーション (v4.2)", fontsize=13, fontweight="bold")

    for mt, (mx, my) in zip(MACHINE_TYPES, MACHINE_POS):
        rect = patches.Rectangle((mx-0.45, my-0.3), 0.9, 0.6,
                                 facecolor=mt.color, alpha=0.18, edgecolor=mt.color, linewidth=2)
        ax_hall.add_patch(rect)
        ax_hall.text(mx, my+0.45, mt.name, ha="center", fontsize=11,
                     fontweight="bold", color=mt.color)

    # step 別にスナップショット作成
    pids = [p.pid for p in personas]
    snaps = {step: {} for step in range(0, n_steps + 1)}
    for r in log:
        snaps[r["step"]][r["pid"]] = r

    history = {pid: {"arousal": [], "despair": []} for pid in pids}

    for step in range(1, n_steps + 1):
        # dot 更新
        for art in list(ax_hall.collections):
            art.remove()
        for txt in list(ax_hall.texts):
            if hasattr(txt, "_dyn"): txt.remove()

        # この step の状態（履歴の最後を見る）
        state_now = {}
        for pid in pids:
            recent = [r for r in log if r["pid"] == pid and r["step"] <= step]
            if recent:
                state_now[pid] = recent[-1]

        # 機種別グルーピング
        by_machine = {i: [] for i in range(len(MACHINE_TYPES))}
        for pid, r in state_now.items():
            if r["active"]:
                by_machine[r["machine_idx"]].append((pid, r))

        for m_idx, plist in by_machine.items():
            mx, my = MACHINE_POS[m_idx]
            for k, (pid, r) in enumerate(plist):
                offset = (k - (len(plist) - 1) / 2) * 0.32
                x, y = mx + offset, my - 0.55
                size = 200 + r["arousal"] * 8
                # trigger event ある step は金色
                edge = "gold" if r["trigger_event"] not in ("none", "chain_start") else "black"
                ew = 4 if edge == "gold" else 1
                ax_hall.scatter([x], [y], s=size, c=r["color"],
                                edgecolors=edge, linewidths=ew, zorder=5)
                # arousal_delta が大きい step は浮かべる文字
                if r["arousal_delta"] > 20:
                    t = ax_hall.text(x, y + 0.25, f"+{r['arousal_delta']:.0f}",
                                     fontsize=11, fontweight="bold", color="red",
                                     ha="center")
                    t._dyn = True
                lab = ax_hall.text(x, y - 0.28, pid, fontsize=7, ha="center",
                                   color="dimgray")
                lab._dyn = True

        title = ax_hall.text(2.25, 3.85, f"step {step:>2} / {n_steps}",
                             fontsize=14, fontweight="bold", ha="center")
        title._dyn = True

        # arousal 推移
        for pid in pids:
            recent = [r for r in log if r["pid"] == pid and r["step"] <= step]
            if recent:
                history[pid]["arousal"] = [r["arousal"] for r in recent]
                history[pid]["despair"] = [r["despair"] for r in recent]

        ax_a.clear()
        ax_a.set_title("興奮度（v4.2: 爆発項込み）", fontsize=10, fontweight="bold")
        ax_a.set_xlim(0, n_steps); ax_a.set_ylim(0, 100)
        ax_a.grid(alpha=0.3)
        for pid in pids:
            p_obj = next(p for p in personas if p.pid == pid)
            ax_a.plot(history[pid]["arousal"], color=p_obj.color, linewidth=1.5,
                      label=f"{pid} {p_obj.category}")
        ax_a.legend(fontsize=6, loc="best", ncol=2)

        ax_d.clear()
        ax_d.set_title("絶望度", fontsize=10, fontweight="bold")
        ax_d.set_xlim(0, n_steps); ax_d.set_ylim(0, 100)
        ax_d.grid(alpha=0.3)
        for pid in pids:
            p_obj = next(p for p in personas if p.pid == pid)
            ax_d.plot(history[pid]["despair"], color=p_obj.color, linewidth=1.5)

        plt.pause(0.15)

    plt.ioff()
    plt.close(fig)


def phase2_top5(top5, log, sessions, voice_rng):
    """Top 5 ハイライトを 1 つずつ表示"""
    for rank, peak in enumerate(top5, 1):
        fig, ax = plt.subplots(figsize=(13, 7))
        ax.set_xlim(0, 10); ax.set_ylim(0, 10)
        ax.set_xticks([]); ax.set_yticks([])

        # 背景グラデ
        ax.set_facecolor("#fff8f0")

        # ヘッダー
        ax.text(0.3, 9.5, f"🔥 HIGHLIGHT #{rank}", fontsize=22, fontweight="bold",
                color="#d9534f")
        ax.text(9.7, 9.5, f"Δarousal  +{peak['arousal_delta']:.0f}",
                fontsize=20, fontweight="bold", ha="right", color="#d9534f")

        # persona dot + 情報
        ax.scatter([1.2], [7.5], s=2000, c=peak["color"], edgecolors="gold",
                   linewidths=4, zorder=5)
        ax.text(2.5, 7.8, f"{peak['pid']}  {peak['category']}",
                fontsize=15, fontweight="bold")
        ax.text(2.5, 7.2, f"step {peak['step']} / 機種: {peak['machine_name']}",
                fontsize=11, color="dimgray")

        # stress_load メーター
        ax.text(0.3, 6.3, "stress_load", fontsize=11, color="#666")
        sl_bg = patches.Rectangle((2.5, 6.2), 6.0, 0.4, facecolor="lightgray",
                                  edgecolor="gray")
        ax.add_patch(sl_bg)
        sl_fg = patches.Rectangle((2.5, 6.2), 6.0 * peak["stress_load"], 0.4,
                                  facecolor="#d9534f")
        ax.add_patch(sl_fg)
        ax.text(8.7, 6.32, f"{peak['stress_load']:.2f}",
                fontsize=11, fontweight="bold", color="#d9534f")

        # trigger event
        trigger_label = peak["trigger_event"]
        trigger_jp = {
            "kakutei_engi": "🎰 確定演出！",
            "tokka_zone_entry": "🔥 特化ゾーン突入！",
            "chain_start": "🎯 ボーナス当選",
        }.get(trigger_label, trigger_label)
        if "uwanose" in trigger_label:
            trigger_jp = f"⬆️ 上乗せ +{peak['uwanose_amount']}G"
        ax.text(0.3, 5.5, "trigger event:", fontsize=11, color="#666")
        ax.text(2.5, 5.5, trigger_jp, fontsize=14, fontweight="bold",
                color="#d9534f")

        # arousal/despair の変化
        window = get_window(log, peak["pid"], peak["step"], before=5, after=3)
        steps = [r["step"] for r in window]
        arousals = [r["arousal"] for r in window]
        despairs = [r["despair"] for r in window]

        # mini sparkline area: 0.3〜4.5 横、3.0〜4.5 縦
        if steps:
            # arousal sparkline
            x_norm = [(s - min(steps)) / max(1, max(steps) - min(steps)) * 4.0 + 0.5
                      for s in steps]
            y_a = [3.5 + a / 100 * 1.0 for a in arousals]
            ax.plot(x_norm, y_a, color="#d9534f", linewidth=2.5, marker="o",
                    markersize=4)
            # despair sparkline
            y_d = [2.0 + d / 100 * 1.0 for d in despairs]
            ax.plot(x_norm, y_d, color="#3a7ca5", linewidth=2.5, marker="s",
                    markersize=4)

            # ピーク位置をマーク
            peak_idx = steps.index(peak["step"])
            ax.scatter([x_norm[peak_idx]], [y_a[peak_idx]], s=200,
                       c="gold", edgecolors="red", linewidths=2, zorder=10)

        ax.text(0.3, 4.7, "arousal (赤) / despair (青) 推移",
                fontsize=10, color="#666")
        ax.text(0.3, 4.55, f"  arousal: {arousals[0]:.0f} → {peak['arousal']:.0f}  /  "
                f"despair: {despairs[0]:.0f} → {peak['despair']:.0f}",
                fontsize=10, color="#333")

        # 心の声
        voice = get_inner_voice(peak["arousal"], peak["despair"],
                                peak["trigger_event"], voice_rng)
        bubble = patches.FancyBboxPatch((5.0, 1.8), 4.7, 2.2,
                                        boxstyle="round,pad=0.2",
                                        facecolor="white",
                                        edgecolor="#d9534f", linewidth=1.5)
        ax.add_patch(bubble)
        ax.text(5.2, 3.7, "💭 心の声", fontsize=10, color="#d9534f",
                fontweight="bold")
        ax.text(7.35, 2.7, f"「{voice}」", fontsize=14, ha="center",
                fontweight="bold", color="#222")

        # フッター
        ax.text(5.0, 0.5, f"stress_load × upset_recognition の積で爆発項 +{peak['explosion_term']:.1f}",
                fontsize=10, ha="center", color="#666", style="italic")

        plt.title(f"Phase 2: Top 5 ハイライト (#{rank} / 5)",
                  fontsize=12, fontweight="bold")
        plt.tight_layout()
        plt.show(block=False)
        plt.pause(4.5)
        plt.close(fig)


def phase3_scatter(log, top5):
    """stress_load × Δarousal 散布図（仮説検証）"""
    fig, ax = plt.subplots(figsize=(12, 7))

    # 全 step の arousal_delta > 5 を点で
    plot_data = [r for r in log if r["arousal_delta"] > 5]
    if plot_data:
        xs = [r["stress_load"] for r in plot_data]
        ys = [r["arousal_delta"] for r in plot_data]
        colors = [r["color"] for r in plot_data]
        sizes = [30 + r["upset_recognition"] * 200 for r in plot_data]

        ax.scatter(xs, ys, c=colors, s=sizes, alpha=0.5, edgecolors="black",
                   linewidths=0.5)

        # 回帰直線
        if len(xs) >= 2:
            z = np.polyfit(xs, ys, 1)
            x_range = np.array([0, 1])
            ax.plot(x_range, z[0] * x_range + z[1], "r--", linewidth=2.5,
                    label=f"回帰: y = {z[0]:.1f}x + {z[1]:.1f}")
            ax.legend(fontsize=11)

    # Top 5 を強調
    for rank, peak in enumerate(top5, 1):
        ax.scatter([peak["stress_load"]], [peak["arousal_delta"]],
                   s=400, c=peak["color"], edgecolors="gold", linewidths=3,
                   zorder=10)
        ax.annotate(f"#{rank} {peak['pid']}",
                    (peak["stress_load"], peak["arousal_delta"]),
                    xytext=(10, 10), textcoords="offset points",
                    fontsize=11, fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow",
                              alpha=0.7))

    ax.set_xlabel("stress_load (借金 + 仕事ストレス + 生活不満 + 持続的ストレス)",
                  fontsize=12)
    ax.set_ylabel("Δarousal (1 step での興奮度上昇)", fontsize=12)
    ax.set_title("Phase 3: ストレス × 興奮ピークの相関（仮説検証）",
                 fontsize=14, fontweight="bold")
    ax.set_xlim(-0.05, 1.05)
    ax.grid(alpha=0.3)
    ax.axhline(0, color="gray", linewidth=0.8)

    # 字幕
    ax.text(0.5, ax.get_ylim()[1] * 0.95,
            "「stress_load が高いほど、Δarousal が大きい傾向」が回帰直線で見えるか？",
            fontsize=11, ha="center", style="italic", color="#666",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#fff8f0",
                      edgecolor="#d9534f"))

    plt.tight_layout()
    plt.show()


# ============ メイン ============
def main():
    rng = np.random.default_rng(42)
    voice_rng = random.Random(42)

    print("=== Phase 0: シミュレーション実行中 ===")
    log, personas, sessions = run_simulation(rng, n_steps=50)
    print(f"  → {len(log)} 行のログを取得")

    print("\n=== Phase 0.5: Top 5 ピーク抽出 ===")
    top5 = extract_top5_peaks(log, threshold=15.0, top_n=5)
    print(f"  → {len(top5)} ピーク検出")
    for rank, p in enumerate(top5, 1):
        print(f"  #{rank} {p['pid']} {p['category']} step{p['step']} "
              f"trigger={p['trigger_event']} Δarousal=+{p['arousal_delta']:.0f} "
              f"stress={p['stress_load']:.2f}")

    print("\n=== Phase 1: ライブシミュレーション再生 ===")
    phase1_live(log, personas, n_steps=50)

    print("\n=== Phase 2: Top 5 ハイライト ===")
    phase2_top5(top5, log, sessions, voice_rng)

    print("\n=== Phase 3: 散布図（仮説検証）===")
    phase3_scatter(log, top5)

    print("\n=== 終了 ===")


if __name__ == "__main__":
    main()
