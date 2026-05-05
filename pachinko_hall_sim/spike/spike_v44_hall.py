"""
spike_v44_hall.py — v4.5 ホール俯瞰早回し動画（48 セル格子）

1000 人 × 50 step を「パンパンパン」と早回しで見せる動画。各ドット 1 人、
8 属性 × 6 機種 = 48 セル格子に配置。当たり時に脳汁強度で発光、連チャン中は残光。

簡易脳汁（5 つの新規概念は未実装、5/3 PM 以降のフェーズで肉付け）:
  brain = 22 * bonus_excite     (chain_just_started)
        + 10 * big_gain_log * bonus_excite

含めない:
- streak_bonus / chain_anxiety / disappointment_stress / miren_uchi / afterglow
- ストレス動的化 / 幸福度 / Top5 ハイライトカット
- LLM voice / Phase 1-6 ナレーション

出力: outputs/spike_v44_hall.mp4（プロジェクトルートからの相対）
"""
from __future__ import annotations

from dataclasses import dataclass
from math import log10
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FFMpegWriter, FuncAnimation
from matplotlib.colors import LinearSegmentedColormap

# 日本語フォント（macOS）。無ければ DejaVu にフォールバックして警告だけ残す。
matplotlib.rcParams["font.family"] = ["Hiragino Sans", "Hiragino Maru Gothic Pro", "DejaVu Sans"]

from spike_v44 import (
    MACHINES,
    MACHINES_BY_CODE,
    PersonaState,
    assign_machines,
    make_states,
    play,
)
from spike_v44_personas import ATTRIBUTES, generate_population, Persona


# ============ レイアウト（48 セル格子）============

# 各セル内: 7 列 × 3 行 = 21 ドット（GOD_2000 のみ 20 → 末尾 1 ドット欠番）
CELL_COLS = 7
CELL_ROWS = 3
CELL_GAP_X = 1  # 機種列の間の余白（ドット単位）
CELL_GAP_Y = 1  # 属性行の間の余白

ATTR_TO_ROW = {a.code: i for i, a in enumerate(ATTRIBUTES)}     # 上→下
MACHINE_TO_COL = {m.code: i for i, m in enumerate(MACHINES)}    # 左→右


@dataclass
class DotPos:
    x: int
    y: int


def assign_dot_positions(personas: list[Persona]) -> dict[str, DotPos]:
    """attribute × machine ごとに 21 人を 7×3 グリッドへ並べ、座標を返す。"""
    positions: dict[str, DotPos] = {}
    by_cell: dict[tuple[str, str], list[Persona]] = {}
    for p in personas:
        by_cell.setdefault((p.attribute_code, p.assigned_machine), []).append(p)

    for (attr_code, machine_code), members in by_cell.items():
        row = ATTR_TO_ROW[attr_code]
        col = MACHINE_TO_COL[machine_code]
        x_origin = col * (CELL_COLS + CELL_GAP_X)
        y_origin = row * (CELL_ROWS + CELL_GAP_Y)
        for i, p in enumerate(members):
            cx = i % CELL_COLS
            cy = i // CELL_COLS
            # 上端を 0 にしたいので y は反転（matplotlib の y=0 が下のため）
            positions[p.pid] = DotPos(x=x_origin + cx, y=y_origin + cy)
    return positions


# ============ 簡易脳汁 ============

def compute_brain_simple(event: dict, mt) -> float:
    """v4.5 興奮量計算式の最小骨格。streak / dopamine_burst / chain_anxiety は未実装。"""
    if event["payout"] <= 0:
        return 0.0
    payout = event["payout"]
    big_gain_log = max(0.0, log10(max(payout, 5000) / 5000.0))

    if event["chain_just_started"]:
        hit_body = 22.0 * mt.bonus_excitement_multiplier
    elif event["hit"]:
        hit_body = 12.0 * mt.continuation_excitement_multiplier
    else:
        hit_body = 0.0

    big_gain_arousal = 10.0 * big_gain_log * mt.bonus_excitement_multiplier
    return hit_body + big_gain_arousal


# ============ シミュレーション（step ごとのフレームデータを生成）============

@dataclass
class FrameSnapshot:
    """1 step 分の表示用スナップショット。"""
    glow: np.ndarray              # ドットごとの発光強度 0〜1（描画用）
    brain_step: np.ndarray        # ドットごとの今 step Δ脳汁（記録用）
    chain_active: np.ndarray      # ドットごとの連チャン中フラグ
    step: int


def simulate_frames(
    personas: list[Persona],
    n_steps: int,
    seed: int = 1234,
    glow_decay: float = 0.55,        # ハズレ時の減衰係数
    chain_floor: float = 0.30,       # 連チャン中の最低 glow
    brain_norm: float = 200.0,       # glow 正規化（GOD raw +200 級を 1.0 とする）
) -> list[FrameSnapshot]:
    states = make_states(personas)
    rng = np.random.default_rng(seed)

    n = len(personas)
    glow = np.zeros(n)
    pid_to_idx = {p.pid: i for i, p in enumerate(personas)}

    frames: list[FrameSnapshot] = []
    for step in range(n_steps):
        brain_step = np.zeros(n)
        chain_active_flags = np.zeros(n, dtype=bool)

        for p in personas:
            mt = MACHINES_BY_CODE[p.assigned_machine]
            s: PersonaState = states[p.pid]
            event = play(p, s, mt, rng)
            idx = pid_to_idx[p.pid]

            if event["hit"]:
                brain = compute_brain_simple(event, mt)
                brain_step[idx] = brain
                # ヒット時は brain 強度で glow を上書き（既存より大きいときだけ）
                glow[idx] = max(glow[idx], min(1.0, 0.30 + brain / brain_norm))
            else:
                # ハズレ時は減衰
                glow[idx] *= glow_decay

            if s.chain_active:
                chain_active_flags[idx] = True
                glow[idx] = max(glow[idx], chain_floor)

        frames.append(FrameSnapshot(
            glow=glow.copy(),
            brain_step=brain_step.copy(),
            chain_active=chain_active_flags.copy(),
            step=step,
        ))
    return frames


# ============ 描画 ============

def make_colormap() -> LinearSegmentedColormap:
    """暗灰 → 黄 → 橙 → 赤 → 白の順で『脳汁強度』を表現。"""
    return LinearSegmentedColormap.from_list(
        "brain", [
            (0.00, (0.18, 0.18, 0.20)),   # 0: 暗灰（待機）
            (0.30, (0.55, 0.45, 0.10)),   # 連チャン残光帯
            (0.55, (0.95, 0.75, 0.10)),   # 通常当たり
            (0.78, (0.98, 0.40, 0.10)),   # 重い当たり
            (0.95, (1.00, 0.20, 0.20)),   # 爆裂
            (1.00, (1.00, 1.00, 1.00)),   # 神（白く飛ぶ）
        ]
    )


def render_animation(
    personas: list[Persona],
    positions: dict[str, DotPos],
    frames: list[FrameSnapshot],
    output_path: Path,
    fps: int = 5,
) -> None:
    cmap = make_colormap()

    # ドット座標を ndarray にまとめる
    n = len(personas)
    xs = np.array([positions[p.pid].x for p in personas], dtype=float)
    ys = np.array([positions[p.pid].y for p in personas], dtype=float)
    # y を反転（A_NEWBIE が上に来るように）
    ys = ys.max() - ys

    fig, ax = plt.subplots(figsize=(14, 9), dpi=120)
    ax.set_facecolor((0.05, 0.05, 0.07))
    fig.patch.set_facecolor((0.05, 0.05, 0.07))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(xs.min() - 1.5, xs.max() + 1.5)
    ax.set_ylim(ys.min() - 1.5, ys.max() + 2.5)
    for spine in ax.spines.values():
        spine.set_color((0.30, 0.30, 0.35))

    # ラベル: 機種列（上）
    for m in MACHINES:
        col = MACHINE_TO_COL[m.code]
        x_center = col * (CELL_COLS + CELL_GAP_X) + (CELL_COLS - 1) / 2
        ax.text(x_center, ys.max() + 1.4, m.code,
                ha="center", va="bottom",
                color=(0.85, 0.85, 0.90), fontsize=9, weight="bold")

    # ラベル: 属性行（左）
    for a in ATTRIBUTES:
        row = ATTR_TO_ROW[a.code]
        y_center = ys.max() - (row * (CELL_ROWS + CELL_GAP_Y) + (CELL_ROWS - 1) / 2)
        ax.text(-1.2, y_center, a.code,
                ha="right", va="center",
                color=(0.85, 0.85, 0.90), fontsize=8)

    title = ax.text(
        (xs.min() + xs.max()) / 2, ys.max() + 2.2,
        "", ha="center", va="bottom",
        color=(1.0, 1.0, 1.0), fontsize=12, weight="bold",
    )

    # 初期 scatter（glow=0 から）
    sizes = np.full(n, 60.0)
    initial_colors = cmap(np.zeros(n))
    scat = ax.scatter(xs, ys, c=initial_colors, s=sizes, edgecolors="none")

    def update(frame_idx: int):
        f = frames[frame_idx]
        glow = np.clip(f.glow, 0.0, 1.0)
        colors = cmap(glow)
        # サイズも軽く脈動させる（光ってる人だけ少し大きく）
        sizes_dyn = 60.0 + 60.0 * glow
        scat.set_color(colors)
        scat.set_sizes(sizes_dyn)
        n_chain = int(f.chain_active.sum())
        n_hit = int((f.brain_step > 0).sum())
        title.set_text(
            f"step {f.step + 1:>2d}/{len(frames)}    "
            f"hit={n_hit:>3d}    連チャン中={n_chain:>3d}    "
            f"max Δ脳汁={f.brain_step.max():.0f}"
        )
        return scat, title

    anim = FuncAnimation(fig, update, frames=len(frames), interval=1000 // fps, blit=False)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    writer = FFMpegWriter(fps=fps, bitrate=2400, codec="libx264")
    anim.save(str(output_path), writer=writer)
    plt.close(fig)


# ============ Top3 脳汁ピーク ============

def report_top_peaks(personas: list[Persona], frames: list[FrameSnapshot], top_n: int = 3) -> None:
    """全 step を走査して raw Δ脳汁の最大ピークを Top N 取得。"""
    by_pid: dict[str, tuple[float, int, str]] = {}
    pid_list = [p.pid for p in personas]
    for f in frames:
        idxs = np.where(f.brain_step > 0)[0]
        for idx in idxs:
            pid = pid_list[idx]
            brain = float(f.brain_step[idx])
            if pid not in by_pid or brain > by_pid[pid][0]:
                by_pid[pid] = (brain, f.step + 1, "")

    p_by_pid = {p.pid: p for p in personas}
    sorted_peaks = sorted(by_pid.items(), key=lambda x: -x[1][0])[:top_n]
    print(f"\n=== Top {top_n} 脳汁ピーク（簡易式、5 つの新規概念なし）===")
    for rank, (pid, (brain, step, _)) in enumerate(sorted_peaks, 1):
        p = p_by_pid[pid]
        machine = p.assigned_machine
        cap_label = "（脳汁 100+）" if brain >= 100 else ""
        print(f"  {rank}. {pid:<22} × {machine:<13} step{step:>2}  raw Δ脳汁 +{brain:>5.0f} {cap_label}")


# ============ メイン ============

def main() -> None:
    print("=== Step 1: 1000 人生成 + 48 セル配分 ===")
    personas = generate_population(n_per_attr=125, seed=42)
    assign_machines(personas, seed=42)

    print("\n=== Step 2: ドット座標計算 ===")
    positions = assign_dot_positions(personas)
    print(f"  配置済みドット: {len(positions)}")

    print("\n=== Step 3: 50 step シミュレーション（フレーム生成）===")
    n_steps = 50
    frames = simulate_frames(personas, n_steps=n_steps, seed=1234)
    print(f"  フレーム数: {len(frames)}")

    print("\n=== Step 4: 動画書き出し ===")
    # spike/spike_v44_hall.py から見て parents[1] = pachinko_hall_sim/
    output_path = Path(__file__).resolve().parents[1] / "outputs" / "spike_v44_hall.mp4"
    print(f"  出力先: {output_path}")
    render_animation(personas, positions, frames, output_path, fps=5)
    print(f"  書き出し完了（{n_steps} step / 5 fps = {n_steps // 5} 秒）")

    report_top_peaks(personas, frames, top_n=3)

    print("\n注:")
    print("- 簡易脳汁式（hit_body + big_gain_log のみ）。streak/anxiety/dopamine_burst は未実装。")
    print("- 5/3 PM の 5 つの新規概念実装後、本式に差し替えると GOD_2000 は raw +200 級が出る想定。")


if __name__ == "__main__":
    main()
