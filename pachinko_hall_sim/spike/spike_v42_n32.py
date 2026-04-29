"""
spike_v42_n32.py — 32 persona × 100 step で仮説検証

spike_v42.py の N=8 では統計が足りなかったので拡大版。
- persona 32 人（カテゴリ 8 種 × 各 4 人、stress_load を変動）
- step 100（中間イベントが十分発生する長さ）
- Phase 1 は簡素化（ホール俯瞰 + カテゴリ別平均グラフ）
- Phase 2 Top 5 ハイライト
- Phase 3 stress_load × Δarousal 散布図（仮説検証の主役）
"""
import random
import sys
from dataclasses import dataclass
from math import exp, log, sqrt, tanh
from pathlib import Path

# spike_v42 の関数を再利用
sys.path.insert(0, str(Path(__file__).parent))
from spike_v42 import (
    MachineType, MACHINE_TYPES, Persona, SessionContext,
    compute_stress_load, play, compute_upset_recognition,
    update_emotions, maybe_switch,
    classify_state, get_inner_voice, INNER_VOICE,
    extract_top5_peaks, get_window,
    MACHINE_POS,
)

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = "Hiragino Sans"
plt.rcParams["axes.unicode_minus"] = False


# ============ 32 persona 生成 ============
PERSONA_TEMPLATES = [
    # (category, color, cash_range, sensory_gating_range, base_a, base_d, base_stress_range)
    ("依存症末期", "#8B0000", (25000, 35000), (0.90, 1.00), 70, 75, (0.65, 0.85)),
    ("中年現役",   "#FF6347", (30000, 50000), (0.75, 0.85), 55, 50, (0.45, 0.65)),
    ("主婦",       "#FFB6C1", (12000, 20000), (0.65, 0.75), 50, 45, (0.30, 0.50)),
    ("女子大生",   "#DA70D6", ( 8000, 14000), (0.80, 0.90), 60, 40, (0.20, 0.40)),
    ("不労所得",   "#4682B4", (60000,100000), (0.55, 0.65), 45, 30, (0.05, 0.20)),
    ("年金高齢",   "#808080", (15000, 25000), (0.45, 0.55), 40, 55, (0.35, 0.55)),
    ("夜職女性",   "#9370DB", (40000, 60000), (0.80, 0.90), 65, 55, (0.55, 0.75)),
    ("退職前男性", "#2F4F4F", (30000, 40000), (0.65, 0.75), 50, 50, (0.40, 0.60)),
]


def make_n32(rng):
    personas = []
    sessions = {}
    pid_counter = 1
    for tmpl in PERSONA_TEMPLATES:
        cat, color, cash_r, sg_r, ba, bd, stress_r = tmpl
        for k in range(4):  # 各カテゴリ 4 人
            pid = f"p{pid_counter:02d}"
            cash = int(rng.uniform(*cash_r))
            sg = float(rng.uniform(*sg_r))
            bs = float(rng.uniform(*stress_r))
            personas.append(Persona(
                pid=pid, category=cat, color=color, cash=cash,
                sensory_gating=sg, base_arousal=ba, base_despair=bd,
                base_stress=bs,
            ))
            # session context は base_stress と相関させる（ストレスフル persona はその日も荒れがち）
            stress_jitter = rng.uniform(-0.15, 0.15)
            sessions[pid] = SessionContext(
                pid=pid,
                borrow_burden=max(0, min(1, bs + stress_jitter)),
                work_stress=max(0, min(1, bs * 0.8 + rng.uniform(-0.2, 0.3))),
                life_dissatisfaction=max(0, min(1, bs * 0.7 + rng.uniform(-0.2, 0.3))),
            )
            pid_counter += 1
    return personas, sessions


# ============ シミュレーション（spike_v42 のコピー、persona maker だけ差し替え）============
def run_simulation_n32(rng, n_steps=100):
    personas, sessions = make_n32(rng)
    initial_cash_map = {p.pid: p.cash for p in personas}
    for p in personas:
        p.arousal = p.base_arousal
        p.despair = p.base_despair
        p.machine_idx = int(rng.integers(0, len(MACHINE_TYPES)))

    log = []

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
            upset = compute_upset_recognition(event_info, p)
            explosion = update_emotions(p, event_info, mt, initial_cash_map[p.pid],
                                        stress_load, upset)

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
                "arousal_delta": p.arousal - prev_a,
                "despair_delta": p.despair - prev_d,
                "trigger_event": event_info["trigger_event"],
                "uwanose_amount": event_info["uwanose_amount"],
                "hit": event_info["hit"],
                "payout": event_info["payout"],
                "stress_load": stress_load,
                "upset_recognition": upset,
                "explosion_term": explosion,
                "miss_streak": p.miss_streak,
                "chain_active": p.chain_active,
                "active": p.active,
            })

            maybe_switch(p, len(MACHINE_TYPES), rng, event_info["hit"])

    return log, personas, sessions


# ============ Phase 1: 簡素化したライブ ============
def phase1_live_compact(log, personas, n_steps=100):
    plt.ion()
    fig = plt.figure(figsize=(15, 8))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.4, 1])
    ax_hall = fig.add_subplot(gs[:, 0])
    ax_a = fig.add_subplot(gs[0, 1])
    ax_d = fig.add_subplot(gs[1, 1])

    ax_hall.set_xlim(0, 4.5); ax_hall.set_ylim(-1.5, 4.5)
    ax_hall.set_aspect("equal")
    ax_hall.set_xticks([]); ax_hall.set_yticks([])
    ax_hall.set_title(f"Phase 1: ライブ ({len(personas)} persona × {n_steps} step)",
                      fontsize=13, fontweight="bold")

    for mt, (mx, my) in zip(MACHINE_TYPES, MACHINE_POS):
        rect = patches.Rectangle((mx-0.45, my-0.3), 0.9, 0.6,
                                 facecolor=mt.color, alpha=0.18, edgecolor=mt.color, linewidth=2)
        ax_hall.add_patch(rect)
        ax_hall.text(mx, my+0.45, mt.name, ha="center", fontsize=11,
                     fontweight="bold", color=mt.color)

    pids = [p.pid for p in personas]
    # カテゴリ別グルーピング
    by_cat = {}
    for p in personas:
        by_cat.setdefault(p.category, []).append(p)

    history_cat = {cat: {"arousal": [], "despair": []} for cat in by_cat}

    # step ごとの最新状態を高速取得するための index
    step_records = {step: [] for step in range(1, n_steps + 1)}
    for r in log:
        step_records[r["step"]].append(r)

    # 各 persona の最新状態を保持（active 含む）
    latest = {pid: None for pid in pids}

    for step in range(1, n_steps + 1):
        for r in step_records[step]:
            latest[r["pid"]] = r

        # 描画クリア
        for art in list(ax_hall.collections):
            art.remove()
        for txt in list(ax_hall.texts):
            if hasattr(txt, "_dyn"): txt.remove()

        # dot 配置
        by_machine = {i: [] for i in range(len(MACHINE_TYPES))}
        for pid, r in latest.items():
            if r and r["active"]:
                by_machine[r["machine_idx"]].append((pid, r))

        for m_idx, plist in by_machine.items():
            mx, my = MACHINE_POS[m_idx]
            n = len(plist)
            # 多い時は 2 行に並べる
            cols = max(1, int(np.ceil(np.sqrt(n))))
            for k, (pid, r) in enumerate(plist):
                row = k // cols
                col = k % cols
                offset_x = (col - (cols - 1) / 2) * 0.18
                offset_y = -0.45 - row * 0.20
                x, y = mx + offset_x, my + offset_y
                size = 30 + r["arousal"] * 2.5
                edge = "gold" if r["trigger_event"] not in ("none", "chain_start") else "black"
                ew = 2 if edge == "gold" else 0.5
                ax_hall.scatter([x], [y], s=size, c=r["color"],
                                edgecolors=edge, linewidths=ew, zorder=5, alpha=0.9)

        title = ax_hall.text(2.25, 4.0, f"step {step:>3} / {n_steps}",
                             fontsize=14, fontweight="bold", ha="center")
        title._dyn = True

        # カテゴリ別平均 (arousal/despair)
        cat_a = {}
        cat_d = {}
        for cat, plist in by_cat.items():
            arousals = [latest[p.pid]["arousal"] for p in plist
                        if latest[p.pid] and latest[p.pid]["active"]]
            despairs = [latest[p.pid]["despair"] for p in plist
                        if latest[p.pid] and latest[p.pid]["active"]]
            cat_a[cat] = np.mean(arousals) if arousals else 0
            cat_d[cat] = np.mean(despairs) if despairs else 0
            history_cat[cat]["arousal"].append(cat_a[cat])
            history_cat[cat]["despair"].append(cat_d[cat])

        ax_a.clear()
        ax_a.set_title("カテゴリ別平均 興奮度", fontsize=10, fontweight="bold")
        ax_a.set_xlim(0, n_steps); ax_a.set_ylim(0, 100)
        ax_a.grid(alpha=0.3)
        for cat, plist in by_cat.items():
            ax_a.plot(history_cat[cat]["arousal"], color=plist[0].color,
                      linewidth=1.8, label=cat)
        ax_a.legend(fontsize=6, loc="best", ncol=2)

        ax_d.clear()
        ax_d.set_title("カテゴリ別平均 絶望度", fontsize=10, fontweight="bold")
        ax_d.set_xlim(0, n_steps); ax_d.set_ylim(0, 100)
        ax_d.grid(alpha=0.3)
        for cat, plist in by_cat.items():
            ax_d.plot(history_cat[cat]["despair"], color=plist[0].color, linewidth=1.8)

        # 軽量化: 0.05 秒
        plt.pause(0.05)

    plt.ioff()
    plt.close(fig)


# ============ Phase 2 (Top 5) は spike_v42 のものを再利用 ============
from spike_v42 import phase2_top5


# ============ Phase 3 散布図（強化版）============
def phase3_scatter_enhanced(log, top5):
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    # 左: 全爆発候補の散布図
    ax = axes[0]
    plot_data = [r for r in log if r["arousal_delta"] > 5]
    if plot_data:
        xs = np.array([r["stress_load"] for r in plot_data])
        ys = np.array([r["arousal_delta"] for r in plot_data])
        colors = [r["color"] for r in plot_data]
        sizes = [20 + r["upset_recognition"] * 250 for r in plot_data]

        ax.scatter(xs, ys, c=colors, s=sizes, alpha=0.5, edgecolors="black",
                   linewidths=0.3)

        # 回帰直線 + 相関係数
        if len(xs) >= 2:
            z = np.polyfit(xs, ys, 1)
            x_range = np.array([0, 1])
            ax.plot(x_range, z[0] * x_range + z[1], "r--", linewidth=2.5,
                    label=f"回帰: y = {z[0]:.2f}x + {z[1]:.2f}")
            corr = np.corrcoef(xs, ys)[0, 1]
            ax.legend(fontsize=10, loc="upper left")
            ax.text(0.98, 0.95, f"相関係数 r = {corr:+.3f}\nN = {len(plot_data)}",
                    transform=ax.transAxes, fontsize=11, ha="right", va="top",
                    bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                              edgecolor="red", linewidth=1.5))

    # Top 5 強調
    for rank, peak in enumerate(top5, 1):
        ax.scatter([peak["stress_load"]], [peak["arousal_delta"]],
                   s=400, c=peak["color"], edgecolors="gold", linewidths=3, zorder=10)
        ax.annotate(f"#{rank}", (peak["stress_load"], peak["arousal_delta"]),
                    xytext=(8, 8), textcoords="offset points",
                    fontsize=13, fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.85))

    ax.set_xlabel("stress_load", fontsize=12)
    ax.set_ylabel("Δarousal", fontsize=12)
    ax.set_title("全爆発候補 (Δarousal > 5) の散布", fontsize=13, fontweight="bold")
    ax.set_xlim(-0.05, 1.05)
    ax.grid(alpha=0.3)
    ax.axhline(0, color="gray", linewidth=0.6)

    # 右: persona 別の集計（box plot 風）
    ax2 = axes[1]
    by_pid = {}
    for r in plot_data:
        by_pid.setdefault(r["pid"], []).append((r["stress_load"], r["arousal_delta"]))

    # 各 persona の (stress_load, mean Δarousal) と max Δarousal
    pid_stress = []
    pid_mean = []
    pid_max = []
    pid_color = []
    pid_label = []
    for pid, vals in by_pid.items():
        if len(vals) < 2:
            continue
        sl = vals[0][0]
        deltas = [v[1] for v in vals]
        pid_stress.append(sl)
        pid_mean.append(np.mean(deltas))
        pid_max.append(np.max(deltas))
        pid_color.append(next(r["color"] for r in plot_data if r["pid"] == pid))
        pid_label.append(pid)

    if pid_stress:
        # 平均
        ax2.scatter(pid_stress, pid_mean, c=pid_color, s=120, alpha=0.7,
                    edgecolors="black", linewidths=0.6, label="persona 平均 Δarousal")
        # 最大
        ax2.scatter(pid_stress, pid_max, c=pid_color, s=200, alpha=0.4,
                    edgecolors="red", linewidths=1.2, marker="^",
                    label="persona 最大 Δarousal")

        # 平均値の回帰
        if len(pid_stress) >= 2:
            z = np.polyfit(pid_stress, pid_mean, 1)
            x_range = np.array([0, 1])
            ax2.plot(x_range, z[0] * x_range + z[1], "b--", linewidth=2,
                     label=f"平均回帰: y = {z[0]:.2f}x + {z[1]:.2f}")
            corr2 = np.corrcoef(pid_stress, pid_mean)[0, 1]
            ax2.text(0.98, 0.95, f"persona 平均の相関 r = {corr2:+.3f}\nN_persona = {len(pid_stress)}",
                     transform=ax2.transAxes, fontsize=11, ha="right", va="top",
                     bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                               edgecolor="blue", linewidth=1.5))

        ax2.legend(fontsize=9, loc="upper left")

    ax2.set_xlabel("stress_load", fontsize=12)
    ax2.set_ylabel("Δarousal (persona ごと集計)", fontsize=12)
    ax2.set_title("persona 別の平均/最大 Δarousal", fontsize=13, fontweight="bold")
    ax2.set_xlim(-0.05, 1.05)
    ax2.grid(alpha=0.3)
    ax2.axhline(0, color="gray", linewidth=0.6)

    plt.suptitle("Phase 3: ストレス × 興奮ピーク相関（仮説検証）",
                 fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.show()


# ============ メイン ============
def main():
    rng = np.random.default_rng(42)
    voice_rng = random.Random(42)

    print("=== Phase 0: 32 persona × 100 step シミュレーション ===")
    log, personas, sessions = run_simulation_n32(rng, n_steps=100)
    print(f"  → {len(log)} 行のログ")
    n_explosions = sum(1 for r in log if r["arousal_delta"] > 5)
    n_big = sum(1 for r in log if r["arousal_delta"] > 15)
    print(f"  → 爆発候補 (Δa>5): {n_explosions} 件、大爆発 (Δa>15): {n_big} 件")

    print("\n=== Phase 0.5: Top 5 ピーク抽出 ===")
    top5 = extract_top5_peaks(log, threshold=15.0, top_n=5)
    for rank, p in enumerate(top5, 1):
        print(f"  #{rank} {p['pid']} {p['category']:6s} step{p['step']:>3} "
              f"trigger={p['trigger_event']:18s} "
              f"Δa=+{p['arousal_delta']:5.1f} stress={p['stress_load']:.2f}")

    print("\n=== Phase 1: ライブ再生 ===")
    phase1_live_compact(log, personas, n_steps=100)

    print("\n=== Phase 2: Top 5 ハイライト ===")
    phase2_top5(top5, log, sessions, voice_rng)

    print("\n=== Phase 3: 散布図（仮説検証）===")
    phase3_scatter_enhanced(log, top5)

    print("\n=== 終了 ===")


if __name__ == "__main__":
    main()
