"""
spike_v43_video_mvp.py — 動画パイプライン MVP

目的: spike_v43 の Phase 1（ホール俯瞰）を FuncAnimation 化して MP4 書き出し。
作者が「動画化スタックが本当に立つか」を体感するための最小実装。

使い方:
    python spike_v43_video_mvp.py
    → outputs/spike_v43_mvp.mp4 が出力される

スコープ:
- ホール俯瞰だけ（グラフなし、字幕なし、装飾なし）
- 8 persona × 50 step
- 5 fps（10 秒の動画）
- ffmpeg writer で mp4 出力
"""
import os
import sys

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, FFMpegWriter

# spike_v43 から import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spike_v43 import (
    MACHINE_TYPES, MACHINE_POS,
    run_simulation,
)

plt.rcParams["font.family"] = "Hiragino Sans"
plt.rcParams["axes.unicode_minus"] = False


def make_video(out_path: str, n_steps: int = 50, fps: int = 5, seed: int = 42):
    """ホール俯瞰の MVP 動画を生成"""
    print(f"=== シミュレーション実行 (seed={seed}, n_steps={n_steps}) ===")
    rng = np.random.default_rng(seed)
    log, personas, sessions = run_simulation(rng, n_steps=n_steps)
    print(f"  log: {len(log)} rows, personas: {len(personas)}")

    pids = [p.pid for p in personas]
    # step ごとに各 pid の最新状態を引けるように事前計算
    state_by_step = {}
    for step in range(1, n_steps + 1):
        snap = {}
        for pid in pids:
            recent = [r for r in log if r["pid"] == pid and r["step"] <= step]
            if recent:
                snap[pid] = recent[-1]
        state_by_step[step] = snap

    print(f"  state_by_step: {len(state_by_step)} frames")

    # === Figure セットアップ ===
    fig, ax_hall = plt.subplots(figsize=(12, 7))
    ax_hall.set_xlim(0, 4.5); ax_hall.set_ylim(-1, 4)
    ax_hall.set_aspect("equal")
    ax_hall.set_xticks([]); ax_hall.set_yticks([])
    title = ax_hall.set_title("Phase 1: ライブシミュレーション (v4.3 MVP)", fontsize=14, fontweight="bold")

    # 機種枠を固定描画
    for mt, (mx, my) in zip(MACHINE_TYPES, MACHINE_POS):
        rect = patches.Rectangle((mx-0.45, my-0.3), 0.9, 0.6,
                                 facecolor=mt.color, alpha=0.18,
                                 edgecolor=mt.color, linewidth=2)
        ax_hall.add_patch(rect)
        ax_hall.text(mx, my+0.45, mt.name, ha="center", fontsize=11,
                     fontweight="bold", color=mt.color)

    # step 表示用テキスト（フレームごとに更新）
    step_text = ax_hall.text(0.1, 3.7, "", fontsize=12, fontweight="bold")

    # 動的な描画オブジェクト（フレームごとに作り直す）
    dynamic_artists = []

    def update(frame):
        nonlocal dynamic_artists
        step = frame + 1  # 1-indexed
        # 前フレームの動的アーティストを削除
        for art in dynamic_artists:
            art.remove()
        dynamic_artists = []

        snap = state_by_step.get(step, {})

        # 機種別グルーピング
        by_machine = {i: [] for i in range(len(MACHINE_TYPES))}
        for pid, r in snap.items():
            if r["active"]:
                by_machine[r["machine_idx"]].append((pid, r))

        for m_idx, plist in by_machine.items():
            mx, my = MACHINE_POS[m_idx]
            for k, (pid, r) in enumerate(plist):
                offset = (k - (len(plist) - 1) / 2) * 0.32
                x, y = mx + offset, my - 0.55
                size = 200 + r["arousal"] * 8
                # 中間イベント発火 step は金縁
                edge = "gold" if r["trigger_event"] not in ("none", "chain_start") else "black"
                lw = 3 if edge == "gold" else 1
                sc = ax_hall.scatter([x], [y], s=size, c=r["color"],
                                     edgecolors=edge, linewidths=lw, zorder=5)
                dynamic_artists.append(sc)

        # step 表示更新
        step_text.set_text(f"step {step}/{n_steps}")
        return dynamic_artists + [step_text]

    print(f"=== FuncAnimation 構築 ===")
    ani = FuncAnimation(fig, update, frames=n_steps, interval=1000 // fps, blit=False)

    print(f"=== MP4 書き出し ({out_path}, fps={fps}) ===")
    writer = FFMpegWriter(fps=fps, bitrate=2000)
    ani.save(out_path, writer=writer, dpi=120)
    plt.close(fig)
    print(f"=== 完了: {out_path} ===")


def main():
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
    out_dir = os.path.join(project_root, "outputs")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "spike_v43_mvp.mp4")
    make_video(out_path, n_steps=50, fps=5, seed=42)
    print(f"\n再生してみて: open {out_path}")


if __name__ == "__main__":
    main()
