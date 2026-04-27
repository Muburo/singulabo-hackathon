"""
spike_hybrid.py — ハイブリッド方式（最熱狂 + 最絶望 + 最解離）の概念実証

1. 30 step 全 persona を rule-only で回し、履歴を取る
2. 事後選定で 3 主役を決める
   - 主役1: 全期間で最大 arousal に達した人（熱狂）
   - 主役2: 全期間で最大 despair に達した人（絶望）
   - 主役3: 全期間で despair - arousal のギャップ最大（解離）
3. リプレイで可視化
   - 左: ホール俯瞰、3 主役にゴールドリング
   - 右: 3 主役のスポットライト枠（表情・3軸メーター・心の声）
4. 心の声は **本番では LLM、今は辞書テンプレ + ランダム**
"""
import random
from dataclasses import dataclass
from math import exp, log, sqrt, tanh

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = "Hiragino Sans"
plt.rcParams["axes.unicode_minus"] = False


# ============ 機種 ============
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
        return log(self.payout_mean) - 0.5 * log(1 + (self.payout_std / self.payout_mean) ** 2)

    @property
    def payout_sigma(self):
        return sqrt(log(1 + (self.payout_std / self.payout_mean) ** 2))


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


# ============ 物理 + 感情 ============
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
    persona.miss_streak = 0 if hit else persona.miss_streak + 1
    return hit, int(payout)


def update_emotions(persona, hit, payout, stake, initial_cash):
    hit_signal = 1.0 if hit else 0.0
    net_delta = payout - stake
    gain_signal = tanh(max(0, net_delta) / 5000)
    loss_signal = tanh(max(0, -net_delta) / 3000)
    hammari_signal = 1 - exp(-persona.miss_streak / 12)
    cash_low = 1.0 if persona.cash <= 3000 else 0.0
    loss_ratio = max(0, (initial_cash - persona.cash) / max(1, initial_cash))

    da = (22*hit_signal + 10*gain_signal + 4*hammari_signal - 3*cash_low)
    da *= persona.sensory_gating
    da -= 0.05 * (persona.arousal - persona.base_arousal)
    persona.arousal = max(0.0, min(100.0, persona.arousal + da))

    dd = (16*loss_signal + 12*loss_ratio + 8*cash_low + 5*hammari_signal - 10*gain_signal)
    dd *= (0.7 + persona.base_despair / 100.0)
    dd -= 0.03 * (persona.despair - persona.base_despair)
    persona.despair = max(0.0, min(100.0, persona.despair + dd))


def maybe_switch(persona, n_machines, rng, hit):
    if persona.cash <= 0:
        persona.active = False
        return
    if hit and rng.random() < 0.3:
        new_idx = rng.integers(0, n_machines)
        if new_idx != persona.machine_idx:
            persona.machine_idx = int(new_idx)
            persona.chain_active = False


# ============ 擬似心の声（本番では LLM に差し替え）============
INNER_VOICE_DICT = {
    "焦燥": [  # 高A高D
        "もう光るしかない",
        "頼む、一回だけでいい",
        "ここまで来て止まれない",
        "次で当たる、絶対に",
        "やめろ、いや、無理だ",
    ],
    "熱狂": [  # 高A低D
        "来る、絶対来る",
        "もう少し、もう少しで",
        "今日はイケる気がする",
        "光れ、光れ、光れ",
    ],
    "絶望": [  # 中A高D
        "もう、お金が",
        "終わった、もう無理",
        "やめておけばよかった",
        "なんで、なんで",
    ],
    "解離": [  # 高D 低A、または cash 0 寸前で動じない
        "...",
        "ふっ、またか",
        "・・・どうでもいい",
        "（無感情）",
        "ああ、はい",
    ],
    "凪": [  # 低A低D
        "ふーん",
        "まあ、こんなもん",
        "別にいいか",
    ],
    "倦怠": [  # 低A
        "退屈だな",
        "やる気でない",
    ],
    "普通": [
        "うーん",
        "どうかな",
        "...",
    ],
}


def classify_state(arousal, despair):
    if arousal >= 75 and despair >= 65:
        return "焦燥"
    if arousal >= 75:
        return "熱狂"
    if despair >= 70 and arousal < 45:
        return "解離"
    if despair >= 65:
        return "絶望"
    if arousal < 35 and despair < 35:
        return "凪"
    if arousal < 35:
        return "倦怠"
    return "普通"


def get_inner_voice(arousal, despair, rng_voice):
    state = classify_state(arousal, despair)
    return state, rng_voice.choice(INNER_VOICE_DICT[state])


# ============ 描画 ============
MACHINE_POS = [(1, 2.5), (3, 2.5), (1, 0.8), (3, 0.8)]


def setup_figure():
    fig = plt.figure(figsize=(16, 9))
    gs = fig.add_gridspec(3, 2, width_ratios=[1.4, 1])
    ax_hall = fig.add_subplot(gs[:, 0])
    ax_s1 = fig.add_subplot(gs[0, 1])
    ax_s2 = fig.add_subplot(gs[1, 1])
    ax_s3 = fig.add_subplot(gs[2, 1])

    ax_hall.set_xlim(0, 4.5)
    ax_hall.set_ylim(-1.0, 4.0)
    ax_hall.set_aspect("equal")
    ax_hall.set_xticks([])
    ax_hall.set_yticks([])

    for mt, (mx, my) in zip(MACHINE_TYPES, MACHINE_POS):
        rect = patches.Rectangle((mx - 0.45, my - 0.3), 0.9, 0.6,
                                 linewidth=2, edgecolor=mt.color,
                                 facecolor=mt.color, alpha=0.18)
        ax_hall.add_patch(rect)
        ax_hall.text(mx, my + 0.45, mt.name, ha="center", fontsize=11,
                     fontweight="bold", color=mt.color)

    return fig, ax_hall, [ax_s1, ax_s2, ax_s3]


def despair_to_edge(despair):
    t = despair / 100.0
    if t < 0.5:
        return (0.5, 0.5 - 0.3*(t/0.5), 0.5 + 0.3*(t/0.5))
    s = (t - 0.5) / 0.5
    return (max(0, min(1, 0.5 + 0.4*s)), max(0, min(1, 0.2 - 0.2*s)), max(0, min(1, 0.8 - 0.6*s)))


def draw_hall(ax, personas, step, hit_pids, leading_pids):
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
            size = 200 + p.arousal * 8
            is_lead = p.pid in leading_pids
            if p.pid in hit_pids:
                edge = "gold"; ew = 4
            elif is_lead:
                edge = "gold"; ew = 3.5
            else:
                edge = despair_to_edge(p.despair); ew = 2
            ax.scatter([x], [y], s=size, c=p.color, edgecolors=edge,
                       linewidths=ew, zorder=5)
            if is_lead:
                # ハイライトリング
                ring = patches.Circle((x, y), 0.18, fill=False,
                                      edgecolor="gold", linewidth=2.5,
                                      linestyle="--", alpha=0.7)
                ring._dyn = True
                ax.add_patch(ring)
            label = ax.text(x, y - 0.28, f"{p.pid}", fontsize=7,
                            ha="center", color="dimgray")
            label._dyn = True

    leavers = [p for p in personas if not p.active]
    for k, p in enumerate(leavers):
        x = 0.3 + k * 0.45
        y = 3.6
        ax.scatter([x], [y], s=120, c="lightgray", edgecolors="gray",
                   linewidths=0.8, zorder=4)
        t = ax.text(x, y - 0.22, f"{p.pid}\n退場", fontsize=7,
                    ha="center", color="gray")
        t._dyn = True

    title = ax.text(2.25, 3.85, f"step {step:>2} / 30",
                    fontsize=14, fontweight="bold", ha="center")
    title._dyn = True


def draw_spotlight(ax, persona, role_label, role_color,
                   arousal, despair, voice, state, machine_name):
    """主役 1 人の状態パネルを描く"""
    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xticks([])
    ax.set_yticks([])

    # 背景
    bg = patches.Rectangle((0, 0), 10, 10,
                           facecolor=role_color, alpha=0.08, edgecolor=role_color,
                           linewidth=2)
    ax.add_patch(bg)

    # 役名
    ax.text(0.3, 9.2, role_label, fontsize=13, fontweight="bold",
            color=role_color)
    ax.text(9.7, 9.2, f"{persona.pid} {persona.category}", fontsize=9,
            ha="right", color="dimgray")

    # dot + state
    dot_color = persona.color
    edge = despair_to_edge(despair)
    ax.scatter([1.3], [6.8], s=400, c=dot_color, edgecolors=edge,
               linewidths=2.5, zorder=5)
    ax.text(1.3, 5.8, state, fontsize=12, fontweight="bold",
            ha="center", color=role_color)

    # メーター
    ax.text(2.7, 7.6, "興奮度", fontsize=9, color="#d9534f")
    bg1 = patches.Rectangle((4.0, 7.4), 5.0, 0.5, facecolor="lightgray",
                            edgecolor="gray", linewidth=0.8)
    ax.add_patch(bg1)
    fg1 = patches.Rectangle((4.0, 7.4), 5.0 * (arousal / 100), 0.5,
                            facecolor="#d9534f", edgecolor="none")
    ax.add_patch(fg1)
    ax.text(9.7, 7.62, f"{arousal:.0f}", fontsize=9, ha="right",
            color="#d9534f", fontweight="bold")

    ax.text(2.7, 6.6, "絶望度", fontsize=9, color="#3a7ca5")
    bg2 = patches.Rectangle((4.0, 6.4), 5.0, 0.5, facecolor="lightgray",
                            edgecolor="gray", linewidth=0.8)
    ax.add_patch(bg2)
    fg2 = patches.Rectangle((4.0, 6.4), 5.0 * (despair / 100), 0.5,
                            facecolor="#3a7ca5", edgecolor="none")
    ax.add_patch(fg2)
    ax.text(9.7, 6.62, f"{despair:.0f}", fontsize=9, ha="right",
            color="#3a7ca5", fontweight="bold")

    # 残金
    ax.text(2.7, 5.6, f"残金: {persona.cash:>7,} 円  /  台: {machine_name}",
            fontsize=9, color="dimgray")

    # 心の声（吹き出し）
    bubble = patches.FancyBboxPatch((0.5, 1.5), 9.0, 3.2,
                                    boxstyle="round,pad=0.3",
                                    facecolor="white", edgecolor=role_color,
                                    linewidth=1.5)
    ax.add_patch(bubble)
    ax.text(0.9, 4.0, "💭 心の声", fontsize=9, color=role_color,
            fontweight="bold")
    ax.text(5.0, 2.8, f"「{voice}」", fontsize=15, ha="center",
            fontweight="bold", color="#333")


# ============ メイン ============
def run_simulation(rng, rng_voice, n_steps=30):
    """シミュレーションを完走させ、step 別の状態履歴を取る"""
    personas = make_personas()
    initial_cash_map = {p.pid: p.cash for p in personas}
    for p in personas:
        p.arousal = p.base_arousal
        p.despair = p.base_despair
        p.machine_idx = int(rng.integers(0, len(MACHINE_TYPES)))

    # snapshot per step
    snapshots = []  # list of (step, persona_states_dict, hit_pids)
    snapshots.append((0, snapshot_personas(personas), set()))

    for step in range(1, n_steps + 1):
        hit_pids = set()
        for p in personas:
            if not p.active:
                continue
            mt = MACHINE_TYPES[p.machine_idx]
            hit, payout = play(p, mt, rng)
            update_emotions(p, hit, payout, mt.stake, initial_cash_map[p.pid])
            if hit:
                hit_pids.add(p.pid)
            maybe_switch(p, len(MACHINE_TYPES), rng, hit)
        snapshots.append((step, snapshot_personas(personas), hit_pids))
        if all(not p.active for p in personas):
            break
    return snapshots


def snapshot_personas(personas):
    return [
        {
            "pid": p.pid,
            "category": p.category,
            "color": p.color,
            "cash": p.cash,
            "arousal": p.arousal,
            "despair": p.despair,
            "machine_idx": p.machine_idx,
            "active": p.active,
        }
        for p in personas
    ]


def select_leading_three(snapshots):
    """全 step の履歴から 3 主役を選ぶ"""
    pids = [s["pid"] for s in snapshots[0][1]]
    history = {pid: {"arousal": [], "despair": []} for pid in pids}
    for step, states, _ in snapshots:
        for s in states:
            history[s["pid"]]["arousal"].append(s["arousal"])
            history[s["pid"]]["despair"].append(s["despair"])

    # 1. 最熱狂
    peak_a = {pid: max(h["arousal"]) for pid, h in history.items()}
    role1 = max(peak_a, key=peak_a.get)

    # 2. 最絶望
    peak_d = {pid: max(h["despair"]) for pid, h in history.items() if pid != role1}
    role2 = max(peak_d, key=peak_d.get)

    # 3. 最解離（despair 最大時の arousal が低い）
    def dissoc_score(pid):
        h = history[pid]
        gaps = [d - a for a, d in zip(h["arousal"], h["despair"])]
        return max(gaps)
    candidates = [pid for pid in pids if pid not in (role1, role2)]
    role3 = max(candidates, key=dissoc_score)

    return role1, role2, role3


def main():
    rng = np.random.default_rng(42)
    rng_voice = random.Random(42)

    print("Phase 1: シミュレーション完走中...")
    snapshots = run_simulation(rng, rng_voice, n_steps=30)
    print(f"  → {len(snapshots) - 1} step 分の snapshot を取得")

    print("\nPhase 2: 主役 3 人を事後選定...")
    role1, role2, role3 = select_leading_three(snapshots)
    role_labels = {role1: "🔥 最熱狂", role2: "💀 最絶望", role3: "🧊 最解離"}
    role_colors = {role1: "#d9534f", role2: "#3a7ca5", role3: "#6c757d"}
    print(f"  🔥 最熱狂: {role1}")
    print(f"  💀 最絶望: {role2}")
    print(f"  🧊 最解離: {role3}")

    print("\nPhase 3: リプレイ表示...")
    plt.ion()
    fig, ax_hall, ax_spots = setup_figure()
    leading_pids = {role1, role2, role3}

    # 各主役は独立した rng で voice を選ぶ（同じ step でも違うセリフ）
    voice_rngs = {pid: random.Random(hash(pid) & 0xFFFFFFFF) for pid in leading_pids}

    for step, states, hit_pids in snapshots:
        # ホール俯瞰用の Persona オブジェクトを再構築（簡易）
        personas_view = []
        for s in states:
            p = Persona(
                pid=s["pid"], category=s["category"], color=s["color"],
                cash=s["cash"], sensory_gating=0, base_arousal=0, base_despair=0,
                arousal=s["arousal"], despair=s["despair"],
                machine_idx=s["machine_idx"], active=s["active"],
            )
            personas_view.append(p)
        draw_hall(ax_hall, personas_view, step, hit_pids, leading_pids)

        # 主役 3 人のスポットライト
        for ax_spot, pid in zip(ax_spots, [role1, role2, role3]):
            s = next(x for x in states if x["pid"] == pid)
            persona_obj = next(p for p in personas_view if p.pid == pid)
            state_label, voice = get_inner_voice(s["arousal"], s["despair"],
                                                 voice_rngs[pid])
            mt_name = MACHINE_TYPES[s["machine_idx"]].name if s["active"] else "退場"
            draw_spotlight(ax_spot, persona_obj,
                           role_labels[pid], role_colors[pid],
                           s["arousal"], s["despair"], voice, state_label, mt_name)

        plt.tight_layout()
        plt.pause(0.7)
        print(f"  step {step:>2}: hits={len(hit_pids)}")

    plt.ioff()
    print("\n=== 終了。ウィンドウを閉じると終わります ===")
    plt.show()


if __name__ == "__main__":
    main()
