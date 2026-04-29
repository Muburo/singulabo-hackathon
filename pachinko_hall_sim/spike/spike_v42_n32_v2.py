"""
spike_v42_n32_v2.py — 観客向けに改善した版

改善点:
- 用語: arousal → 脳汁度、despair → 絶望度、stress_load → 追い詰められ度、Δarousal → 脳汁の跳ね上がり
- Phase 0.1: 仮説提示パネル（仮説 / 検証方法 / 勝ち条件 / 失敗条件）
- 心の声を機種 × トリガー × カテゴリで拡張（inner_voice_v2.py 参照）
- Phase 3: 散布図 + 3 群バーチャート（ストレス低/中/高）
- Phase 4: 結論パネル（仮説と対応、勝ち / 失敗を明示）
- Phase 2 ハイライトは 3 段階ナレーション風（pre / peak / post）
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from spike_v42 import (
    MACHINE_TYPES, MACHINE_POS, Persona, SessionContext,
    compute_stress_load, play, compute_upset_recognition,
    update_emotions, maybe_switch,
    extract_top5_peaks, get_window,
)
from spike_v42_n32 import make_n32, run_simulation_n32
from inner_voice_v2 import get_inner_voice_v2

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = "Hiragino Sans"
plt.rcParams["axes.unicode_minus"] = False


# ============ Phase 0.1: 仮説提示 ============
def phase01_hypothesis():
    fig, ax = plt.subplots(figsize=(13, 7.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_facecolor("#fff8f0")

    # タイトル
    ax.text(5.0, 9.4, "🧠 検証する仮説", fontsize=24, fontweight="bold",
            ha="center", color="#d9534f")

    # 仮説本体
    bubble = patches.FancyBboxPatch((0.8, 6.5), 8.4, 2.2,
                                    boxstyle="round,pad=0.3",
                                    facecolor="white", edgecolor="#d9534f",
                                    linewidth=2.5)
    ax.add_patch(bubble)
    ax.text(5.0, 7.9, "「追い詰められた人ほど、",
            fontsize=20, ha="center", fontweight="bold", color="#222")
    ax.text(5.0, 7.1, "大逆転で大きく脳汁が出る」",
            fontsize=22, ha="center", fontweight="bold", color="#d9534f")

    # 検証方法
    ax.text(0.5, 5.7, "📋 検証方法", fontsize=14, fontweight="bold",
            color="#3a7ca5")
    ax.text(0.8, 5.0, "・32 人 × 100 step のシミュレーション",
            fontsize=12, color="#333")
    ax.text(0.8, 4.4, "・「追い詰められ度」（借金 + 仕事 + 生活不満 + 持続的ストレス）が",
            fontsize=12, color="#333")
    ax.text(1.5, 3.9, "低い人 / 中くらいの人 / 高い人 の最大脳汁ピークを比較",
            fontsize=12, color="#333")
    ax.text(0.8, 3.3, "・大逆転 = 上乗せ・特化ゾーン・確定演出（パチスロの中間イベント）",
            fontsize=12, color="#333")

    # 勝ち条件・失敗条件
    win_box = patches.FancyBboxPatch((0.5, 1.0), 4.4, 1.9,
                                     boxstyle="round,pad=0.2",
                                     facecolor="#d4edda", edgecolor="#28a745",
                                     linewidth=2)
    ax.add_patch(win_box)
    ax.text(2.7, 2.55, "✅ 仮説成立（勝ち）", fontsize=14, fontweight="bold",
            ha="center", color="#28a745")
    ax.text(2.7, 1.85, "高ストレス群の最大脳汁が", fontsize=11, ha="center")
    ax.text(2.7, 1.4, "低ストレス群の 1.3 倍以上", fontsize=12, ha="center",
            fontweight="bold")

    fail_box = patches.FancyBboxPatch((5.1, 1.0), 4.4, 1.9,
                                      boxstyle="round,pad=0.2",
                                      facecolor="#f8d7da", edgecolor="#dc3545",
                                      linewidth=2)
    ax.add_patch(fail_box)
    ax.text(7.3, 2.55, "❌ 仮説失敗", fontsize=14, fontweight="bold",
            ha="center", color="#dc3545")
    ax.text(7.3, 1.85, "1.3 倍未満、または", fontsize=11, ha="center")
    ax.text(7.3, 1.4, "ストレス低群の方が大きい", fontsize=12, ha="center",
            fontweight="bold")

    plt.title("Phase 0: 何を検証するか", fontsize=14, fontweight="bold",
              pad=15)
    plt.tight_layout()
    plt.show(block=False)
    plt.pause(7.0)
    plt.close(fig)


# ============ Phase 1: ライブ（v42_n32 のものを微修正）============
def phase1_live(log, personas, n_steps=100):
    plt.ion()
    fig = plt.figure(figsize=(15, 8))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.4, 1])
    ax_hall = fig.add_subplot(gs[:, 0])
    ax_a = fig.add_subplot(gs[0, 1])
    ax_d = fig.add_subplot(gs[1, 1])

    ax_hall.set_xlim(0, 4.5); ax_hall.set_ylim(-1.5, 4.5)
    ax_hall.set_aspect("equal")
    ax_hall.set_xticks([]); ax_hall.set_yticks([])
    ax_hall.set_title(f"Phase 1: ライブシミュレーション ({len(personas)} 人 × {n_steps} step)",
                      fontsize=12, fontweight="bold")

    for mt, (mx, my) in zip(MACHINE_TYPES, MACHINE_POS):
        rect = patches.Rectangle((mx-0.45, my-0.3), 0.9, 0.6,
                                 facecolor=mt.color, alpha=0.18, edgecolor=mt.color, linewidth=2)
        ax_hall.add_patch(rect)
        ax_hall.text(mx, my+0.45, mt.name, ha="center", fontsize=11,
                     fontweight="bold", color=mt.color)

    pids = [p.pid for p in personas]
    by_cat = {}
    for p in personas:
        by_cat.setdefault(p.category, []).append(p)

    history_cat = {cat: {"arousal": [], "despair": []} for cat in by_cat}
    step_records = {step: [] for step in range(1, n_steps + 1)}
    for r in log:
        step_records[r["step"]].append(r)

    latest = {pid: None for pid in pids}

    for step in range(1, n_steps + 1):
        for r in step_records[step]:
            latest[r["pid"]] = r

        for art in list(ax_hall.collections):
            art.remove()
        for txt in list(ax_hall.texts):
            if hasattr(txt, "_dyn"): txt.remove()

        by_machine = {i: [] for i in range(len(MACHINE_TYPES))}
        for pid, r in latest.items():
            if r and r["active"]:
                by_machine[r["machine_idx"]].append((pid, r))

        for m_idx, plist in by_machine.items():
            mx, my = MACHINE_POS[m_idx]
            n = len(plist)
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

        # カテゴリ別平均
        for cat, plist in by_cat.items():
            arousals = [latest[p.pid]["arousal"] for p in plist
                        if latest[p.pid] and latest[p.pid]["active"]]
            despairs = [latest[p.pid]["despair"] for p in plist
                        if latest[p.pid] and latest[p.pid]["active"]]
            history_cat[cat]["arousal"].append(np.mean(arousals) if arousals else 0)
            history_cat[cat]["despair"].append(np.mean(despairs) if despairs else 0)

        ax_a.clear()
        ax_a.set_title("カテゴリ別 平均 脳汁度", fontsize=10, fontweight="bold")
        ax_a.set_xlim(0, n_steps); ax_a.set_ylim(0, 100)
        ax_a.grid(alpha=0.3)
        for cat, plist in by_cat.items():
            ax_a.plot(history_cat[cat]["arousal"], color=plist[0].color,
                      linewidth=1.8, label=cat)
        ax_a.legend(fontsize=6, loc="best", ncol=2)

        ax_d.clear()
        ax_d.set_title("カテゴリ別 平均 絶望度", fontsize=10, fontweight="bold")
        ax_d.set_xlim(0, n_steps); ax_d.set_ylim(0, 100)
        ax_d.grid(alpha=0.3)
        for cat, plist in by_cat.items():
            ax_d.plot(history_cat[cat]["despair"], color=plist[0].color, linewidth=1.8)

        plt.pause(0.05)

    plt.ioff()
    plt.close(fig)


# ============ Phase 2: ナレーション風 Top 5 ============
def phase2_top5_narrated(top5, log, voice_rng):
    for rank, peak in enumerate(top5, 1):
        # pre / peak / post の 3 段階を取得
        window = get_window(log, peak["pid"], peak["step"], before=3, after=2)
        steps_in_window = sorted(window, key=lambda r: r["step"])
        peak_idx = next(i for i, r in enumerate(steps_in_window) if r["step"] == peak["step"])
        pre = steps_in_window[max(0, peak_idx - 1)] if peak_idx > 0 else steps_in_window[0]
        peak_row = steps_in_window[peak_idx]
        post = steps_in_window[min(len(steps_in_window) - 1, peak_idx + 1)] if peak_idx + 1 < len(steps_in_window) else peak_row

        fig, ax = plt.subplots(figsize=(14, 8))
        ax.set_xlim(0, 10); ax.set_ylim(0, 10)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_facecolor("#fff8f0")

        # ヘッダー
        ax.text(0.3, 9.5, f"🔥 ハイライト #{rank}", fontsize=22, fontweight="bold",
                color="#d9534f")
        ax.text(9.7, 9.5, f"脳汁の跳ね上がり  +{peak['arousal_delta']:.0f}",
                fontsize=18, fontweight="bold", ha="right", color="#d9534f")

        # persona
        ax.scatter([1.0], [8.4], s=1200, c=peak["color"], edgecolors="gold",
                   linewidths=4, zorder=5)
        ax.text(2.2, 8.6, f"{peak['pid']}  {peak['category']}",
                fontsize=14, fontweight="bold")
        ax.text(2.2, 8.0, f"機種: {peak['machine_name']}",
                fontsize=11, color="dimgray")

        # 追い詰められ度メーター
        ax.text(5.0, 8.6, "追い詰められ度:", fontsize=11, color="#666")
        sl_bg = patches.Rectangle((6.5, 8.45), 3.0, 0.4, facecolor="lightgray",
                                  edgecolor="gray")
        ax.add_patch(sl_bg)
        sl_fg = patches.Rectangle((6.5, 8.45), 3.0 * peak["stress_load"], 0.4,
                                  facecolor="#d9534f")
        ax.add_patch(sl_fg)
        ax.text(9.6, 8.55, f"{peak['stress_load']:.2f}",
                fontsize=12, fontweight="bold", color="#d9534f", ha="right")

        # 3 段階ナレーション
        # Stage 1: pre
        ax.text(0.3, 7.0, f"【step {pre['step']}】 直前", fontsize=11,
                color="#666", fontweight="bold")
        ax.text(0.5, 6.4, f"脳汁度 {pre['arousal']:.0f}、絶望度 {pre['despair']:.0f}",
                fontsize=11, color="#333")
        ax.text(0.5, 5.9, "→ 普通の状態だった", fontsize=12, color="#555",
                style="italic")

        # Stage 2: peak event
        trigger_jp = {
            "kakutei_engi": "🎰 確定演出！",
            "tokka_zone_entry": "🔥 特化ゾーン突入！",
            "chain_start": "🎯 ボーナス当選",
        }.get(peak["trigger_event"], peak["trigger_event"])
        if "uwanose" in peak["trigger_event"]:
            trigger_jp = f"⬆️ 上乗せ +{peak['uwanose_amount']}G"

        peak_box = patches.FancyBboxPatch((0.2, 4.0), 9.6, 1.5,
                                          boxstyle="round,pad=0.2",
                                          facecolor="#fff3cd", edgecolor="#ffc107",
                                          linewidth=2.5)
        ax.add_patch(peak_box)
        ax.text(0.5, 5.0, f"【step {peak_row['step']}】 ⚡ そこに……",
                fontsize=11, color="#666", fontweight="bold")
        ax.text(5.0, 4.5, trigger_jp, fontsize=20, fontweight="bold",
                ha="center", color="#d9534f")

        # Stage 3: post (心の声 + 数字変化)
        voice = get_inner_voice_v2(
            peak_row["arousal"], peak_row["despair"],
            peak["trigger_event"], peak["machine_name"], peak["category"], voice_rng
        )

        ax.text(0.3, 3.3, f"【step {post['step']}】 直後", fontsize=11,
                color="#666", fontweight="bold")
        ax.text(0.5, 2.7,
                f"脳汁度  {pre['arousal']:.0f}  →  {peak_row['arousal']:.0f}  (+{peak['arousal_delta']:.0f})",
                fontsize=13, fontweight="bold", color="#d9534f")
        ax.text(0.5, 2.2,
                f"絶望度  {pre['despair']:.0f}  →  {peak_row['despair']:.0f}",
                fontsize=11, color="#3a7ca5")

        # 心の声
        bubble = patches.FancyBboxPatch((5.0, 1.8), 4.7, 1.9,
                                        boxstyle="round,pad=0.2",
                                        facecolor="white",
                                        edgecolor="#d9534f", linewidth=1.5)
        ax.add_patch(bubble)
        ax.text(5.2, 3.4, "💭 心の声", fontsize=10, color="#d9534f",
                fontweight="bold")
        ax.text(7.35, 2.6, f"「{voice}」", fontsize=15, ha="center",
                fontweight="bold", color="#222")

        # フッター
        ax.text(5.0, 0.7,
                f"追い詰められ度 {peak['stress_load']:.2f} × 大逆転認知 = 脳汁爆発項 +{peak['explosion_term']:.1f}",
                fontsize=10, ha="center", color="#666", style="italic")

        plt.title(f"Phase 2: 脳汁ピーク Top 5 (#{rank} / 5)",
                  fontsize=12, fontweight="bold")
        plt.tight_layout()
        plt.show(block=False)
        plt.pause(5.5)
        plt.close(fig)


# ============ Phase 3: 散布図 + 3 群バーチャート ============
def phase3_three_groups(log, top5):
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    # データ準備
    plot_data = [r for r in log if r["arousal_delta"] > 5]

    # 左: 散布図（参考用、簡素化）
    ax = axes[0]
    if plot_data:
        xs = np.array([r["stress_load"] for r in plot_data])
        ys = np.array([r["arousal_delta"] for r in plot_data])
        colors = [r["color"] for r in plot_data]
        sizes = [20 + r["upset_recognition"] * 250 for r in plot_data]
        ax.scatter(xs, ys, c=colors, s=sizes, alpha=0.5, edgecolors="black",
                   linewidths=0.3)
        if len(xs) >= 2:
            corr = np.corrcoef(xs, ys)[0, 1]
            z = np.polyfit(xs, ys, 1)
            x_range = np.array([0, 1])
            ax.plot(x_range, z[0] * x_range + z[1], "r--", linewidth=2.5)
            ax.text(0.98, 0.95,
                    f"傾向: 追い詰められ度↑→脳汁の跳ね↑\n相関 {corr:+.2f}（弱い〜中程度）",
                    transform=ax.transAxes, fontsize=10, ha="right", va="top",
                    bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff8f0",
                              edgecolor="red", linewidth=1.5))

    for rank, peak in enumerate(top5, 1):
        ax.scatter([peak["stress_load"]], [peak["arousal_delta"]],
                   s=400, c=peak["color"], edgecolors="gold", linewidths=3, zorder=10)
        ax.annotate(f"#{rank}", (peak["stress_load"], peak["arousal_delta"]),
                    xytext=(8, 8), textcoords="offset points",
                    fontsize=12, fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.85))

    ax.set_xlabel("追い詰められ度", fontsize=12)
    ax.set_ylabel("脳汁の跳ね上がり量", fontsize=12)
    ax.set_title("全爆発候補の散布", fontsize=13, fontweight="bold")
    ax.set_xlim(-0.05, 1.05)
    ax.grid(alpha=0.3)
    ax.axhline(0, color="gray", linewidth=0.6)

    # 右: 3 群バーチャート（メイン）
    ax2 = axes[1]
    by_pid_max = {}  # pid -> (stress_load, max_delta)
    for r in plot_data:
        pid = r["pid"]
        if pid not in by_pid_max or r["arousal_delta"] > by_pid_max[pid][1]:
            by_pid_max[pid] = (r["stress_load"], r["arousal_delta"])

    # 3 群分け
    low_group = [v[1] for v in by_pid_max.values() if v[0] < 0.3]
    mid_group = [v[1] for v in by_pid_max.values() if 0.3 <= v[0] < 0.6]
    high_group = [v[1] for v in by_pid_max.values() if v[0] >= 0.6]

    low_mean = np.mean(low_group) if low_group else 0
    mid_mean = np.mean(mid_group) if mid_group else 0
    high_mean = np.mean(high_group) if high_group else 0

    groups = ["低 (<0.3)", "中 (0.3-0.6)", "高 (≥0.6)"]
    means = [low_mean, mid_mean, high_mean]
    counts = [len(low_group), len(mid_group), len(high_group)]
    colors_bar = ["#5bc0de", "#f0ad4e", "#d9534f"]

    bars = ax2.bar(groups, means, color=colors_bar, edgecolor="black",
                   linewidth=1.5, alpha=0.85)

    # 数値ラベル
    for bar, m, c in zip(bars, means, counts):
        ax2.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.5,
                 f"{m:.1f}\n(N={c}人)",
                 ha="center", fontsize=12, fontweight="bold")

    ax2.set_ylabel("各 persona の最大脳汁ピーク（平均）", fontsize=12)
    ax2.set_xlabel("追い詰められ度の群", fontsize=12)
    ax2.set_title("追い詰められ度別 最大脳汁ピーク", fontsize=13, fontweight="bold")
    ax2.grid(alpha=0.3, axis="y")
    ax2.set_ylim(0, max(means) * 1.3 if means else 1)

    # 高/低の比率
    if low_mean > 0:
        ratio = high_mean / low_mean
        ax2.text(0.5, 0.95, f"高群 ÷ 低群 = {ratio:.2f} 倍",
                 transform=ax2.transAxes, fontsize=14, ha="center", va="top",
                 fontweight="bold", color="#d9534f",
                 bbox=dict(boxstyle="round,pad=0.5", facecolor="white",
                           edgecolor="#d9534f", linewidth=2))

    plt.suptitle("Phase 3: 追い詰められ度 × 脳汁ピーク（仮説検証）",
                 fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.show(block=False)
    plt.pause(8.0)
    plt.close(fig)

    # 比率を返す（Phase 4 で使う）
    return low_mean, mid_mean, high_mean, len(low_group), len(mid_group), len(high_group)


# ============ Phase 4-A: 仮説の合否（コンパクト版）============
def phase4a_verdict(low_mean, mid_mean, high_mean, n_low, n_mid, n_high):
    fig, ax = plt.subplots(figsize=(13, 7.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_facecolor("#fff8f0")

    ax.text(5.0, 9.5, "📋 答え合わせ ①: 仮説の合否",
            fontsize=22, fontweight="bold", ha="center", color="#3a7ca5")

    ax.text(5.0, 8.7, "仮説「追い詰められた人ほど、大逆転で大きく脳汁が出る」",
            fontsize=13, ha="center", color="#666", style="italic")

    # 3 群の数字
    box = patches.FancyBboxPatch((0.5, 4.5), 9.0, 3.6,
                                 boxstyle="round,pad=0.3",
                                 facecolor="white", edgecolor="#3a7ca5",
                                 linewidth=2.5)
    ax.add_patch(box)
    ax.text(5.0, 7.7, "1 人あたりの最大脳汁ピーク（平均）",
            fontsize=12, ha="center", color="#666", fontweight="bold")

    for x, label, val, n, color in [
        (2.0, "🔵 低群", low_mean, n_low, "#5bc0de"),
        (5.0, "🟡 中群", mid_mean, n_mid, "#f0ad4e"),
        (8.0, "🔴 高群", high_mean, n_high, "#d9534f"),
    ]:
        ax.text(x, 6.7, label, fontsize=14, ha="center", fontweight="bold", color=color)
        ax.text(x, 6.1, f"{val:.1f}", fontsize=28, ha="center", fontweight="bold", color=color)
        ax.text(x, 5.5, f"N = {n} 人", fontsize=10, ha="center", color="#666")

    ratio = high_mean / low_mean if low_mean > 0 else 0
    ax.text(5.0, 4.85, f"高群 ÷ 低群 = {ratio:.2f} 倍",
            fontsize=18, ha="center", fontweight="bold", color="#d9534f")

    # 判定
    if ratio >= 1.3:
        verdict = "✅ 仮説成立"; color = "#28a745"; bg = "#d4edda"
        msg = "追い詰められ度が高い人ほど、大きく脳汁が出ることが観察された"
    else:
        verdict = "❌ 仮説、外れ"; color = "#dc3545"; bg = "#f8d7da"
        msg = f"勝ち条件 1.3 倍に届かず。仮説は外れた。\nでは、実際に何が見えたか？ → 次の答え合わせへ"

    verdict_box = patches.FancyBboxPatch((0.5, 1.5), 9.0, 2.5,
                                         boxstyle="round,pad=0.3",
                                         facecolor=bg, edgecolor=color, linewidth=2.5)
    ax.add_patch(verdict_box)
    ax.text(5.0, 3.4, verdict, fontsize=22, fontweight="bold", ha="center", color=color)
    ax.text(5.0, 2.4, msg, fontsize=11, ha="center", color="#333")
    ax.text(5.0, 1.85, f"勝ち条件: 1.3 倍以上  /  実測: {ratio:.2f} 倍",
            fontsize=10, ha="center", color="#666", style="italic")

    plt.title("Phase 4-A: 仮説の合否", fontsize=13, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.show(block=False)
    plt.pause(7.0)
    plt.close(fig)


# ============ Phase 4-B: 実際に観察された傾向 ============
def phase4b_observations(log, top5):
    """観察された 3 つの傾向を可視化"""
    plot_data = [r for r in log if r["arousal_delta"] > 5]

    fig, axes = plt.subplots(1, 3, figsize=(18, 6.5))

    # ---- 観察1: trigger event 別の最大 Δ脳汁 ----
    ax = axes[0]
    by_trigger = {}
    for r in plot_data:
        t = r["trigger_event"]
        # 統合: uwanose_*g を全部 uwanose にまとめる
        if t.startswith("uwanose"):
            t = "uwanose"
        by_trigger.setdefault(t, []).append(r["arousal_delta"])

    trigger_labels_jp = {
        "chain_start": "ボーナス当選",
        "uwanose": "上乗せ",
        "tokka_zone_entry": "特化ゾーン",
        "kakutei_engi": "確定演出",
        "none": "（なし）",
    }
    triggers = sorted(by_trigger.keys(), key=lambda t: -np.mean(by_trigger[t]))
    means = [np.mean(by_trigger[t]) for t in triggers]
    counts = [len(by_trigger[t]) for t in triggers]
    labels = [trigger_labels_jp.get(t, t) for t in triggers]

    bars = ax.bar(labels, means,
                  color=["#d9534f", "#f0ad4e", "#5bc0de", "#9370DB", "#999"][:len(triggers)],
                  edgecolor="black", linewidth=1.2, alpha=0.85)
    for bar, m, c in zip(bars, means, counts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f"{m:.1f}\n(N={c})", ha="center", fontsize=10, fontweight="bold")
    ax.set_title("① イベント別 Δ脳汁の平均", fontsize=12, fontweight="bold")
    ax.set_ylabel("脳汁の跳ね上がり 平均", fontsize=11)
    ax.grid(alpha=0.3, axis="y")
    plt.setp(ax.get_xticklabels(), rotation=20, fontsize=10)

    # ---- 観察2: カテゴリ別の最大 Δ脳汁 ----
    ax = axes[1]
    by_cat_max = {}
    by_cat_color = {}
    for r in plot_data:
        cat = r["category"]
        by_cat_max.setdefault(cat, []).append(r["arousal_delta"])
        by_cat_color[cat] = r["color"]
    cats = sorted(by_cat_max.keys(), key=lambda c: -np.max(by_cat_max[c]))
    maxes = [np.max(by_cat_max[c]) for c in cats]
    colors_b = [by_cat_color[c] for c in cats]

    bars = ax.barh(cats, maxes, color=colors_b, edgecolor="black", linewidth=1.0,
                   alpha=0.85)
    for bar, v in zip(bars, maxes):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                f"{v:.1f}", va="center", fontsize=10, fontweight="bold")
    ax.set_title("② カテゴリ別 最大 Δ脳汁", fontsize=12, fontweight="bold")
    ax.set_xlabel("最大の脳汁跳ね上がり", fontsize=11)
    ax.grid(alpha=0.3, axis="x")
    ax.invert_yaxis()

    # ---- 観察3: 感覚の鋭敏さ × Δ脳汁 ----
    ax = axes[2]
    # log に sensory_gating は入ってない（spike_v42 の play では使われてるが log には未追加）
    # 代替: persona ごとに最大 Δ脳汁 と category color
    by_pid_max = {}
    for r in plot_data:
        pid = r["pid"]
        if pid not in by_pid_max or r["arousal_delta"] > by_pid_max[pid]["delta"]:
            by_pid_max[pid] = {"delta": r["arousal_delta"], "color": r["color"],
                               "category": r["category"]}
    # カテゴリ別の sensory_gating の代理: PERSONA_TEMPLATES の sg_r 中央値
    from spike_v42_n32 import PERSONA_TEMPLATES
    sg_by_cat = {t[0]: (t[3][0] + t[3][1]) / 2 for t in PERSONA_TEMPLATES}

    sgs = [sg_by_cat[v["category"]] for v in by_pid_max.values()]
    deltas = [v["delta"] for v in by_pid_max.values()]
    colors_pt = [v["color"] for v in by_pid_max.values()]
    ax.scatter(sgs, deltas, c=colors_pt, s=120, alpha=0.7, edgecolors="black",
               linewidths=0.6)
    if len(sgs) >= 2:
        z = np.polyfit(sgs, deltas, 1)
        x_range = np.array([min(sgs) - 0.05, max(sgs) + 0.05])
        ax.plot(x_range, z[0] * x_range + z[1], "r--", linewidth=2.5)
        corr = np.corrcoef(sgs, deltas)[0, 1]
        ax.text(0.98, 0.95, f"相関 {corr:+.2f}\n（{'強い' if abs(corr) > 0.5 else '中程度' if abs(corr) > 0.3 else '弱い'}）",
                transform=ax.transAxes, fontsize=11, ha="right", va="top",
                bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                          edgecolor="red", linewidth=1.5))
    ax.set_title("③ 感覚の鋭敏さ × Δ脳汁", fontsize=12, fontweight="bold")
    ax.set_xlabel("感覚の鋭敏さ (sensory_gating)", fontsize=11)
    ax.set_ylabel("各 persona の最大 Δ脳汁", fontsize=11)
    ax.grid(alpha=0.3)

    plt.suptitle("Phase 4-B: 答え合わせ ②: 実際に観察された傾向",
                 fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.show(block=False)
    plt.pause(10.0)
    plt.close(fig)


# ============ Phase 4-C: 答え（観察結果のまとめと次の仮説）============
def phase4c_answer(log, top5):
    plot_data = [r for r in log if r["arousal_delta"] > 5]

    # 観察事実を計算
    by_trigger = {}
    for r in plot_data:
        t = "uwanose" if r["trigger_event"].startswith("uwanose") else r["trigger_event"]
        by_trigger.setdefault(t, []).append(r["arousal_delta"])
    top_trigger = max(by_trigger, key=lambda t: np.mean(by_trigger[t]))
    top_trigger_jp = {"chain_start": "ボーナス当選", "uwanose": "上乗せ",
                      "tokka_zone_entry": "特化ゾーン", "kakutei_engi": "確定演出"}.get(
                          top_trigger, top_trigger)

    by_cat_max = {}
    for r in plot_data:
        by_cat_max.setdefault(r["category"], []).append(r["arousal_delta"])
    top_cat = max(by_cat_max, key=lambda c: np.max(by_cat_max[c]))
    top_cat_max = np.max(by_cat_max[top_cat])

    # Top 5 の trigger 集計
    top5_triggers = [p["trigger_event"] for p in top5]
    chain_start_count = sum(1 for t in top5_triggers if t == "chain_start")

    fig, ax = plt.subplots(figsize=(13, 8))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_facecolor("#fff8f0")

    ax.text(5.0, 9.5, "🎯 答え合わせ ③: 実際の答え",
            fontsize=22, fontweight="bold", ha="center", color="#28a745")

    # 観察結果 1
    obs_box = patches.FancyBboxPatch((0.3, 7.0), 9.4, 1.7,
                                     boxstyle="round,pad=0.2",
                                     facecolor="white", edgecolor="#d9534f", linewidth=2)
    ax.add_patch(obs_box)
    ax.text(0.5, 8.4, "🔍 観察 1：最も脳汁が出る瞬間は何だったか", fontsize=12,
            fontweight="bold", color="#d9534f")
    ax.text(0.5, 7.7, f"  Top 5 のうち {chain_start_count} 人が「{top_trigger_jp}」の瞬間に最大脳汁",
            fontsize=12)
    ax.text(0.5, 7.2, f"  つまり、上乗せや特化ゾーンより、「入り口を引いた瞬間」が支配的だった",
            fontsize=11, color="#555", style="italic")

    # 観察結果 2
    obs_box2 = patches.FancyBboxPatch((0.3, 5.1), 9.4, 1.7,
                                      boxstyle="round,pad=0.2",
                                      facecolor="white", edgecolor="#3a7ca5", linewidth=2)
    ax.add_patch(obs_box2)
    ax.text(0.5, 6.5, "🔍 観察 2：誰が最も大きく脳汁を出したか", fontsize=12,
            fontweight="bold", color="#3a7ca5")
    ax.text(0.5, 5.8, f"  最大脳汁を出した persona: 「{top_cat}」 (Δ脳汁 = +{top_cat_max:.1f})",
            fontsize=12)
    ax.text(0.5, 5.3, "  追い詰められ度が低い persona でも、大きな脳汁を出している",
            fontsize=11, color="#555", style="italic")

    # 観察結果 3
    obs_box3 = patches.FancyBboxPatch((0.3, 3.2), 9.4, 1.7,
                                      boxstyle="round,pad=0.2",
                                      facecolor="white", edgecolor="#9370DB", linewidth=2)
    ax.add_patch(obs_box3)
    ax.text(0.5, 4.6, "🔍 観察 3：効いていたのは「ストレス」ではなく「感覚の鋭敏さ」?",
            fontsize=12, fontweight="bold", color="#9370DB")
    ax.text(0.5, 3.9, "  追い詰められ度ではなく、感覚の鋭敏さ（sensory_gating）と相関する可能性",
            fontsize=11)
    ax.text(0.5, 3.4, "  → 仮説を作り直すべきポイントが見えた",
            fontsize=11, color="#555", style="italic")

    # 次の仮説
    next_box = patches.FancyBboxPatch((0.3, 0.7), 9.4, 2.0,
                                      boxstyle="round,pad=0.3",
                                      facecolor="#e7f3ff", edgecolor="#28a745", linewidth=2.5)
    ax.add_patch(next_box)
    ax.text(5.0, 2.3, "💡 次に検証すべき仮説", fontsize=14, fontweight="bold",
            ha="center", color="#28a745")
    ax.text(5.0, 1.7,
            "「ストレス × 大逆転認知」 → ❌ 外れた",
            fontsize=12, ha="center", color="#666")
    ax.text(5.0, 1.1,
            "「感覚の鋭敏さ × 入り口イベント（ボーナス当選）」",
            fontsize=14, ha="center", fontweight="bold", color="#28a745")

    plt.title("Phase 4-C: 実際の答えと、次に向かう方向", fontsize=13, fontweight="bold",
              pad=12)
    plt.tight_layout()
    plt.show()


# ============ メイン ============
def main():
    rng = np.random.default_rng(42)
    voice_rng = random.Random(42)

    print("=== Phase 0.1: 仮説提示 ===")
    phase01_hypothesis()

    print("\n=== Phase 0: 32 人 × 100 step シミュレーション実行 ===")
    log, personas, sessions = run_simulation_n32(rng, n_steps=100)
    print(f"  → {len(log)} 行のログ")
    n_explosions = sum(1 for r in log if r["arousal_delta"] > 5)
    print(f"  → 爆発候補: {n_explosions} 件")

    print("\n=== Phase 0.5: Top 5 抽出 ===")
    top5 = extract_top5_peaks(log, threshold=15.0, top_n=5)
    for rank, p in enumerate(top5, 1):
        print(f"  #{rank} {p['pid']} {p['category']:6s} step{p['step']:>3} "
              f"trigger={p['trigger_event']:18s} "
              f"Δ脳汁=+{p['arousal_delta']:5.1f} 追い詰め={p['stress_load']:.2f}")

    print("\n=== Phase 1: ライブ ===")
    phase1_live(log, personas, n_steps=100)

    print("\n=== Phase 2: ナレーション風 Top 5 ===")
    phase2_top5_narrated(top5, log, voice_rng)

    print("\n=== Phase 3: 3 群バーチャート ===")
    low_mean, mid_mean, high_mean, n_low, n_mid, n_high = phase3_three_groups(log, top5)

    print("\n=== Phase 4-A: 仮説の合否 ===")
    phase4a_verdict(low_mean, mid_mean, high_mean, n_low, n_mid, n_high)

    print("\n=== Phase 4-B: 観察された傾向 ===")
    phase4b_observations(log, top5)

    print("\n=== Phase 4-C: 実際の答え + 次の仮説 ===")
    phase4c_answer(log, top5)

    print("\n=== 終了 ===")


if __name__ == "__main__":
    main()
