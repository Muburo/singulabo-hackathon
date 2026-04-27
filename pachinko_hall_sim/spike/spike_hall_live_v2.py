"""
spike_hall_live_v2.py — ダッシュボード版

改善点:
- 日本語フォント（Hiragino Sans）で北斗・沖スロが正しく表示
- 各 persona の下に「興奮度メーター（赤）」「絶望度メーター（青）」を表示
- 表情ラベル（興奮 / 焦り / 絶望 / 退屈 / 普通）を dot 上部に表示
- 右側グラフは 3 種（興奮度・絶望度・残金）、タイトルとラベルを日本語化
- 凡例にカテゴリ名を併記
"""
from dataclasses import dataclass
from math import exp, log, sqrt, tanh

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

# 日本語フォント設定（Mac）
plt.rcParams["font.family"] = "Hiragino Sans"
plt.rcParams["axes.unicode_minus"] = False


# ============ 機種パラメータ（v4.1） ============
@dataclass
class MachineType:
    name: str
    color: str
    chain_mode: str
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
    color: str
    cash: int
    sensory_gating: float
    base_arousal: float
    base_despair: float
    arousal: float = 0.0
    despair: float = 0.0
    machine_idx: int = 0
    chain_active: bool = False
    miss_streak: int = 0
    active: bool = True


def make_personas():
    return [
        Persona("p01", "依存症末期", "#8B0000", 30000, 0.95, 70, 75),
        Persona("p02", "中年現役",   "#FF6347", 40000, 0.80, 55, 50),
        Persona("p03", "主婦",       "#FFB6C1", 15000, 0.70, 50, 45),
        Persona("p04", "女子大生",   "#DA70D6", 10000, 0.85, 60, 40),
        Persona("p05", "不労所得",   "#4682B4", 80000, 0.60, 45, 30),
        Persona("p06", "年金高齢",   "#808080", 20000, 0.50, 40, 55),
    ]


# ============ 抽選 + 感情更新 ============
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


def update_emotions(persona, hit, payout, stake, initial_cash):
    hit_signal = 1.0 if hit else 0.0
    net_delta = payout - stake
    gain_signal = tanh(max(0, net_delta) / 5000)
    loss_signal = tanh(max(0, -net_delta) / 3000)
    hammari_signal = 1 - exp(-persona.miss_streak / 12)
    cash_low = 1.0 if persona.cash <= 3000 else 0.0
    loss_ratio = max(0, (initial_cash - persona.cash) / max(1, initial_cash))

    # arousal
    da = (
        + 22.0 * hit_signal
        + 10.0 * gain_signal
        +  4.0 * hammari_signal
        -  3.0 * cash_low
    )
    da *= persona.sensory_gating
    da -= 0.05 * (persona.arousal - persona.base_arousal)
    persona.arousal = max(0.0, min(100.0, persona.arousal + da))

    # despair
    dd = (
        + 16.0 * loss_signal
        + 12.0 * loss_ratio
        +  8.0 * cash_low
        +  5.0 * hammari_signal
        - 10.0 * gain_signal
    )
    dd *= (0.7 + persona.base_despair / 100.0)
    dd -= 0.03 * (persona.despair - persona.base_despair)
    persona.despair = max(0.0, min(100.0, persona.despair + dd))


def emotion_label(arousal, despair):
    """状態を 1 文字で表現"""
    if arousal >= 75 and despair >= 65:
        return "焦"  # 焦燥（興奮 + 絶望）
    if arousal >= 75:
        return "熱"  # 熱中
    if despair >= 70:
        return "鬱"  # 絶望
    if arousal < 35 and despair < 35:
        return "凪"  # 落ち着き
    if arousal < 35:
        return "倦"  # 倦怠
    return "・"  # 普通


def maybe_switch(persona, n_machines, rng, hit):
    if persona.cash <= 0:
        persona.active = False
        return
    if hit and rng.random() < 0.3:
        new_idx = rng.integers(0, n_machines)
        if new_idx != persona.machine_idx:
            persona.machine_idx = int(new_idx)
            persona.chain_active = False


# ============ 描画 ============
MACHINE_POS = [(1, 2.5), (3, 2.5), (1, 0.8), (3, 0.8)]


def setup_figure():
    fig = plt.figure(figsize=(15, 8))
    gs = fig.add_gridspec(3, 2, width_ratios=[1.6, 1])

    ax_hall = fig.add_subplot(gs[:, 0])
    ax_a = fig.add_subplot(gs[0, 1])
    ax_d = fig.add_subplot(gs[1, 1])
    ax_c = fig.add_subplot(gs[2, 1])

    # ホール
    ax_hall.set_xlim(0, 4.5)
    ax_hall.set_ylim(-1.0, 4.0)
    ax_hall.set_aspect("equal")
    ax_hall.set_title("パチンコホール俯瞰  (1 step ≈ 4 分の遊技)",
                      fontsize=14, fontweight="bold")
    ax_hall.set_xticks([])
    ax_hall.set_yticks([])

    for mt, (mx, my) in zip(MACHINE_TYPES, MACHINE_POS):
        rect = patches.Rectangle((mx - 0.45, my - 0.3), 0.9, 0.6,
                                 linewidth=2.5, edgecolor=mt.color,
                                 facecolor=mt.color, alpha=0.18)
        ax_hall.add_patch(rect)
        ax_hall.text(mx, my + 0.45, mt.name, ha="center", fontsize=12,
                     fontweight="bold", color=mt.color)

    # 凡例（読み方）
    legend_text = (
        "【dot の見方】\n"
        " サイズ = 興奮度（大きいほど興奮）\n"
        " 縁色 = 絶望度（赤いほど絶望）\n"
        " 上の文字 = 状態（熱/焦/鬱/凪/倦）\n"
        " 下のバー = 興奮度(赤)・絶望度(青)"
    )
    ax_hall.text(0.05, -0.95, legend_text, fontsize=9,
                 verticalalignment="bottom",
                 bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.8))

    return fig, ax_hall, ax_a, ax_d, ax_c


def despair_to_edge_color(despair):
    """絶望度→縁色: gray → purple → crimson"""
    t = despair / 100.0
    if t < 0.5:
        # gray → purple
        r = 0.5 + (0.5 - 0.5) * (t / 0.5)
        g = 0.5 - 0.3 * (t / 0.5)
        b = 0.5 + 0.3 * (t / 0.5)
    else:
        s = (t - 0.5) / 0.5
        r = 0.5 + 0.4 * s
        g = 0.2 - 0.2 * s
        b = 0.8 - 0.6 * s
    return (max(0, min(1, r)), max(0, min(1, g)), max(0, min(1, b)))


def draw_personas(ax, personas, step, hit_pids):
    # dynamic な要素を消す
    for art in list(ax.collections):
        art.remove()
    for txt in list(ax.texts):
        if hasattr(txt, "_dyn"):
            txt.remove()
    for patch in list(ax.patches):
        if hasattr(patch, "_dyn"):
            patch.remove()

    by_machine = {i: [] for i in range(len(MACHINE_TYPES))}
    for p in personas:
        if p.active:
            by_machine[p.machine_idx].append(p)

    for m_idx, plist in by_machine.items():
        mx, my = MACHINE_POS[m_idx]
        for k, p in enumerate(plist):
            offset_x = (k - (len(plist) - 1) / 2) * 0.32
            x = mx + offset_x
            y = my - 0.55

            # dot
            size = 200 + p.arousal * 8
            edge = "gold" if p.pid in hit_pids else despair_to_edge_color(p.despair)
            edge_w = 4 if p.pid in hit_pids else 2
            ax.scatter([x], [y], s=size, c=p.color,
                       edgecolors=edge, linewidths=edge_w, zorder=5)

            # 状態ラベル（dot の上）
            face = emotion_label(p.arousal, p.despair)
            face_color = "red" if face in ["焦", "鬱"] else (
                "orange" if face == "熱" else "gray"
            )
            t1 = ax.text(x, y + 0.18, face, fontsize=14, fontweight="bold",
                         ha="center", color=face_color)
            t1._dyn = True

            # pid + カテゴリラベル（dot の下）
            t2 = ax.text(x, y - 0.30, f"{p.pid}\n{p.category}",
                         fontsize=7, ha="center", color="dimgray")
            t2._dyn = True

            # 興奮度メーター（赤）
            bar_w = 0.25 * (p.arousal / 100.0)
            r1 = patches.Rectangle((x - 0.125, y - 0.45), 0.25, 0.04,
                                   facecolor="lightgray", edgecolor="gray", linewidth=0.5)
            r1._dyn = True
            ax.add_patch(r1)
            r2 = patches.Rectangle((x - 0.125, y - 0.45), bar_w, 0.04,
                                   facecolor="#d9534f", edgecolor="none")
            r2._dyn = True
            ax.add_patch(r2)

            # 絶望度メーター（青）
            bar_w = 0.25 * (p.despair / 100.0)
            r3 = patches.Rectangle((x - 0.125, y - 0.50), 0.25, 0.04,
                                   facecolor="lightgray", edgecolor="gray", linewidth=0.5)
            r3._dyn = True
            ax.add_patch(r3)
            r4 = patches.Rectangle((x - 0.125, y - 0.50), bar_w, 0.04,
                                   facecolor="#3a7ca5", edgecolor="none")
            r4._dyn = True
            ax.add_patch(r4)

    # 退場
    leavers = [p for p in personas if not p.active]
    for k, p in enumerate(leavers):
        x = 0.3 + k * 0.45
        y = 3.6
        ax.scatter([x], [y], s=120, c="lightgray", edgecolors="gray",
                   linewidths=0.8, zorder=4)
        t = ax.text(x, y - 0.22, f"{p.pid}\n退場", fontsize=7,
                    ha="center", color="gray")
        t._dyn = True

    # step 表示
    title = ax.text(2.25, 3.85, f"step {step:>2} / 30",
                    fontsize=15, fontweight="bold", color="black",
                    ha="center")
    title._dyn = True

    # 「退場エリア」ラベル
    if leavers:
        label = ax.text(0.05, 3.78, "退場 →", fontsize=8, color="gray")
        label._dyn = True


def update_line_graphs(ax_a, ax_d, ax_c, personas, history, n_steps):
    for ax, title, ylabel, ylim, key in [
        (ax_a, "興奮度（高いほど熱中・焦燥）", "arousal", (0, 100), "arousal"),
        (ax_d, "絶望度（高いほど追い込まれている）", "despair", (0, 100), "despair"),
        (ax_c, "残金（円） — 0 円で退場", "cash", None, "cash"),
    ]:
        ax.clear()
        ax.set_title(title, fontsize=10, fontweight="bold")
        ax.set_xlim(0, n_steps)
        if ylim:
            ax.set_ylim(*ylim)
        ax.grid(alpha=0.3)
        ax.set_xlabel("step", fontsize=8)
        for p in personas:
            ax.plot(history[p.pid][key], color=p.color,
                    label=f"{p.pid} {p.category}", linewidth=1.7)
        ax.legend(fontsize=6.5, loc="best", ncol=2)
        if key == "cash":
            ax.axhline(0, color="gray", linestyle="--", alpha=0.5)


# ============ メイン ============
def main():
    plt.ion()
    rng = np.random.default_rng(42)

    personas = make_personas()
    initial_cash_map = {p.pid: p.cash for p in personas}
    for p in personas:
        p.arousal = p.base_arousal
        p.despair = p.base_despair
        p.machine_idx = int(rng.integers(0, len(MACHINE_TYPES)))

    fig, ax_hall, ax_a, ax_d, ax_c = setup_figure()

    history = {
        p.pid: {"arousal": [p.arousal], "despair": [p.despair], "cash": [p.cash]}
        for p in personas
    }

    draw_personas(ax_hall, personas, 0, set())
    update_line_graphs(ax_a, ax_d, ax_c, personas, history, 30)
    plt.tight_layout()
    plt.pause(2.0)

    N_STEPS = 30
    for step in range(1, N_STEPS + 1):
        hit_pids = set()
        for p in personas:
            if not p.active:
                history[p.pid]["arousal"].append(p.arousal)
                history[p.pid]["despair"].append(p.despair)
                history[p.pid]["cash"].append(p.cash)
                continue
            mt = MACHINE_TYPES[p.machine_idx]
            hit, payout = play(p, mt, rng)
            update_emotions(p, hit, payout, mt.stake, initial_cash_map[p.pid])
            if hit:
                hit_pids.add(p.pid)
            maybe_switch(p, len(MACHINE_TYPES), rng, hit)
            history[p.pid]["arousal"].append(p.arousal)
            history[p.pid]["despair"].append(p.despair)
            history[p.pid]["cash"].append(p.cash)

        draw_personas(ax_hall, personas, step, hit_pids)
        update_line_graphs(ax_a, ax_d, ax_c, personas, history, N_STEPS)
        plt.pause(0.6)

        n_active = sum(1 for p in personas if p.active)
        n_hit = len(hit_pids)
        print(f"step {step:>2}: hits={n_hit} active={n_active}")
        if n_active == 0:
            print(f"\n→ 全員退場、step {step} 終了")
            break

    plt.ioff()
    print("\n=== 終了。ウィンドウを閉じると終わります ===")
    plt.show()


if __name__ == "__main__":
    main()
