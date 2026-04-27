"""
spike_hall_live.py — 動く絵をリアルタイムで見るためのスパイク

4 機種 × 各 1 台（合計 4 台）に persona 6 人を配置し、
step ごとに抽選 → 残金更新 → 感情更新 → 描画更新 を繰り返す。
matplotlib のライブ表示（plt.pause）で、リアルタイムに動いてる絵を見る。

これは「動画にする前の生のシミュレーション」をモニターで見るためのもの。
本番ロジックではない。
"""
from dataclasses import dataclass, field
from math import exp, log, sqrt, tanh

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np


# ============ 機種パラメータ（v4.1） ============
@dataclass
class MachineType:
    name: str
    color: str
    chain_mode: str  # "chain" or "none"
    p_initial_hit: float
    continue_prob: float
    payout_mean: float
    payout_std: float
    payout_cap: float
    stake: int = 1000

    @property
    def payout_mu(self):
        sigma2 = log(1 + (self.payout_std / self.payout_mean) ** 2)
        return log(self.payout_mean) - 0.5 * sigma2

    @property
    def payout_sigma(self):
        sigma2 = log(1 + (self.payout_std / self.payout_mean) ** 2)
        return sqrt(sigma2)


MACHINE_TYPES = [
    MachineType("GOD",   "#d9534f", "chain", 0.025, 0.50, 21000, 25000, 120000),
    MachineType("北斗",  "#f0ad4e", "chain", 0.060, 0.58,  8300,  5600,  80000),
    MachineType("ART",   "#5bc0de", "chain", 0.030, 0.83,  6700,  4000,  60000),
    MachineType("沖スロ", "#5cb85c", "none",  0.200, 0.00,  5000,  2000,  20000),
]


# ============ persona ============
@dataclass
class Persona:
    pid: str
    category: str
    color: str  # 4 象限ベースの色
    cash: int
    sensory_gating: float
    base_arousal: float
    arousal: float = 0.0
    machine_idx: int = 0
    chain_active: bool = False
    miss_streak: int = 0
    active: bool = True
    last_hit_step: int = -1


def make_personas():
    return [
        Persona("p01", "依存症末期", "#8B0000", 30000, 0.95, 70),
        Persona("p02", "中年現役",   "#FF6347", 40000, 0.80, 55),
        Persona("p03", "主婦",       "#FFB6C1", 15000, 0.70, 50),
        Persona("p04", "女子大生",   "#DA70D6", 10000, 0.85, 60),
        Persona("p05", "不労所得",   "#4682B4", 80000, 0.60, 45),
        Persona("p06", "年金高齢",   "#808080", 20000, 0.50, 40),
    ]


# ============ 抽選 ============
def play(persona, mt, rng):
    persona.cash -= mt.stake
    hit, payout = False, 0
    if mt.chain_mode == "none":
        if rng.random() < mt.p_initial_hit:
            hit = True
            payout = min(rng.lognormal(mt.payout_mu, mt.payout_sigma), mt.payout_cap)
        persona.chain_active = False
    else:
        if persona.chain_active:
            if rng.random() < mt.continue_prob:
                hit = True
                payout = min(rng.lognormal(mt.payout_mu, mt.payout_sigma), mt.payout_cap)
            else:
                persona.chain_active = False
        else:
            if rng.random() < mt.p_initial_hit:
                hit = True
                payout = min(rng.lognormal(mt.payout_mu, mt.payout_sigma), mt.payout_cap)
                persona.chain_active = True
    persona.cash += int(payout)
    if hit:
        persona.miss_streak = 0
    else:
        persona.miss_streak += 1
    return hit, int(payout)


def update_arousal(persona, hit, payout, stake):
    hit_signal = 1.0 if hit else 0.0
    net_delta = payout - stake
    gain_signal = tanh(max(0, net_delta) / 5000)
    hammari_signal = 1 - exp(-persona.miss_streak / 12)
    cash_low = 1.0 if persona.cash <= 3000 else 0.0
    delta = (
        + 22.0 * hit_signal
        + 10.0 * gain_signal
        +  4.0 * hammari_signal
        -  3.0 * cash_low
    )
    delta *= persona.sensory_gating
    delta -= 0.05 * (persona.arousal - persona.base_arousal)
    persona.arousal = max(0.0, min(100.0, persona.arousal + delta))


def maybe_switch(persona, n_machines, rng, hit):
    """簡易行動: cash 0 なら退場、hit 後 30% で switch、それ以外は stay"""
    if persona.cash <= 0:
        persona.active = False
        return
    if hit and rng.random() < 0.3:
        new_idx = rng.integers(0, n_machines)
        if new_idx != persona.machine_idx:
            persona.machine_idx = int(new_idx)
            persona.chain_active = False  # 移動したら chain リセット


# ============ 描画 ============
MACHINE_POS = [
    (1, 2),  # GOD     左上
    (3, 2),  # 北斗     右上
    (1, 0),  # ART     左下
    (3, 0),  # 沖スロ   右下
]


def setup_figure():
    fig = plt.figure(figsize=(13, 7))
    gs = fig.add_gridspec(2, 2, width_ratios=[2, 1.5])

    ax_hall = fig.add_subplot(gs[:, 0])
    ax_arousal = fig.add_subplot(gs[0, 1])
    ax_cash = fig.add_subplot(gs[1, 1])

    # ホール
    ax_hall.set_xlim(0, 4.5)
    ax_hall.set_ylim(-0.7, 3)
    ax_hall.set_aspect("equal")
    ax_hall.set_title("Pachinko Hall — live view", fontsize=14)
    ax_hall.set_xticks([])
    ax_hall.set_yticks([])

    for mt, (mx, my) in zip(MACHINE_TYPES, MACHINE_POS):
        rect = patches.Rectangle((mx - 0.4, my - 0.3), 0.8, 0.6,
                                 linewidth=2, edgecolor=mt.color,
                                 facecolor=mt.color, alpha=0.25)
        ax_hall.add_patch(rect)
        ax_hall.text(mx, my + 0.4, mt.name, ha="center", fontsize=11,
                     fontweight="bold", color=mt.color)

    # 線グラフ
    ax_arousal.set_title("Arousal by persona", fontsize=11)
    ax_arousal.set_xlabel("step")
    ax_arousal.set_ylabel("arousal")
    ax_arousal.set_xlim(0, 30)
    ax_arousal.set_ylim(0, 100)
    ax_arousal.grid(alpha=0.3)

    ax_cash.set_title("Cash by persona", fontsize=11)
    ax_cash.set_xlabel("step")
    ax_cash.set_ylabel("cash (yen)")
    ax_cash.set_xlim(0, 30)
    ax_cash.grid(alpha=0.3)

    return fig, ax_hall, ax_arousal, ax_cash


def draw_persona_dots(ax, personas, step, hit_personas):
    """ホール上に persona を dot で描画。hit したら金色リング付き"""
    # 既存の dynamic 要素削除
    for art in list(ax.collections):
        art.remove()
    for txt in list(ax.texts):
        if hasattr(txt, "_dynamic"):
            txt.remove()

    # 各台ごとに persona をオフセット配置
    by_machine = {i: [] for i in range(len(MACHINE_TYPES))}
    for p in personas:
        if p.active:
            by_machine[p.machine_idx].append(p)

    for m_idx, plist in by_machine.items():
        mx, my = MACHINE_POS[m_idx]
        for k, p in enumerate(plist):
            offset_x = (k - (len(plist) - 1) / 2) * 0.18
            x, y = mx + offset_x, my - 0.45
            size = 80 + p.arousal * 6
            is_hit = p.pid in hit_personas
            edge_color = "gold" if is_hit else "black"
            edge_width = 3 if is_hit else 0.5
            ax.scatter([x], [y], s=size, c=p.color,
                       edgecolors=edge_color, linewidths=edge_width,
                       zorder=5)
            label = ax.text(x, y - 0.18, p.pid, ha="center",
                            fontsize=7, color="dimgray")
            label._dynamic = True

    # 退場した persona は左下に並べる
    leavers = [p for p in personas if not p.active]
    for k, p in enumerate(leavers):
        x = 0.2 + k * 0.25
        y = -0.55
        ax.scatter([x], [y], s=80, c="lightgray",
                   edgecolors="gray", linewidths=0.5, zorder=4)
        label = ax.text(x, y - 0.15, f"{p.pid}\n(out)", ha="center",
                        fontsize=6, color="gray")
        label._dynamic = True

    # step 表示
    title = ax.text(0.5, 2.85, f"step {step:>2} / 30",
                    fontsize=13, fontweight="bold", color="black")
    title._dynamic = True


# ============ メイン ============
def main():
    plt.ion()  # interactive on
    rng = np.random.default_rng(42)

    personas = make_personas()
    for p in personas:
        p.arousal = p.base_arousal
        # 初期配置: ランダムに台を選ぶ
        p.machine_idx = int(rng.integers(0, len(MACHINE_TYPES)))

    fig, ax_hall, ax_arousal, ax_cash = setup_figure()

    arousal_history = {p.pid: [p.arousal] for p in personas}
    cash_history = {p.pid: [p.cash] for p in personas}

    # 初期描画
    draw_persona_dots(ax_hall, personas, 0, set())
    plt.pause(1.5)  # 初期状態を見せる

    N_STEPS = 30
    for step in range(1, N_STEPS + 1):
        hit_personas = set()

        for p in personas:
            if not p.active:
                arousal_history[p.pid].append(p.arousal)
                cash_history[p.pid].append(p.cash)
                continue

            mt = MACHINE_TYPES[p.machine_idx]
            hit, payout = play(p, mt, rng)
            update_arousal(p, hit, payout, mt.stake)
            if hit:
                hit_personas.add(p.pid)
                p.last_hit_step = step

            maybe_switch(p, len(MACHINE_TYPES), rng, hit)

            arousal_history[p.pid].append(p.arousal)
            cash_history[p.pid].append(p.cash)

        # 描画更新
        draw_persona_dots(ax_hall, personas, step, hit_personas)

        ax_arousal.clear()
        ax_arousal.set_title("Arousal by persona", fontsize=11)
        ax_arousal.set_xlim(0, N_STEPS)
        ax_arousal.set_ylim(0, 100)
        ax_arousal.grid(alpha=0.3)
        for p in personas:
            ax_arousal.plot(arousal_history[p.pid], color=p.color,
                            label=p.pid, linewidth=1.8)
        ax_arousal.legend(fontsize=7, loc="upper left", ncol=2)

        ax_cash.clear()
        ax_cash.set_title("Cash by persona", fontsize=11)
        ax_cash.set_xlim(0, N_STEPS)
        ax_cash.grid(alpha=0.3)
        ax_cash.axhline(0, color="gray", linestyle="--", alpha=0.5)
        for p in personas:
            ax_cash.plot(cash_history[p.pid], color=p.color,
                         label=p.pid, linewidth=1.8)
        ax_cash.legend(fontsize=7, loc="upper right", ncol=2)

        plt.pause(0.5)  # 0.5 秒で次の step

        n_active = sum(1 for p in personas if p.active)
        n_hit = len(hit_personas)
        print(f"step {step:>2}: hits={n_hit}, active={n_active}")

        if n_active == 0:
            print(f"\n→ 全員退場、step {step} で終了")
            break

    plt.ioff()
    print("\n=== 終了。画面を閉じると終了します ===")
    plt.show()


if __name__ == "__main__":
    main()
