"""システム構成図を生成して system_diagram.png を出力。"""
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

matplotlib.rcParams["font.family"] = "Hiragino Sans"

OUT = Path(__file__).parent / "system_diagram.png"


def add_box(ax, x, y, w, h, text, fc, ec):
    rect = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.6,rounding_size=1.0",
        facecolor=fc, edgecolor=ec, linewidth=1.6,
    )
    ax.add_patch(rect)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=10.5, linespacing=1.5)


def arrow(ax, x1, y1, x2, y2, label=None):
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle="-|>", color="#444",
                        linewidth=1.6, mutation_scale=18),
    )
    if label:
        ax.text((x1 + x2) / 2 + 0.6, (y1 + y2) / 2,
                label, fontsize=9, color="#444")


def main():
    fig, ax = plt.subplots(figsize=(11, 5.2), dpi=220)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.axis("off")

    add_box(ax, 1, 28, 19, 14,
            "入力\n人物 8 属性 × 機種 6 カテゴリ\n約 1,000 エージェント\n初当たり / 連チャン構造",
            fc="#eef3ff", ec="#3b6cdc")

    add_box(ax, 28, 28, 24, 14,
            "数値シミュレーション\nnumpy + 確率モデル\n抽選 / 払出 / 心理 4 値更新\n脳汁・ストレス・幸福・絶望",
            fc="#fff4dd", ec="#e08a1f")

    add_box(ax, 60, 28, 22, 14,
            "観察結果\n属性別 Δ脳汁ランキング\n機種カテゴリ別ピーク\n反証軸（非中毒者・低ストレス）",
            fc="#eaf5ec", ec="#2f8a45")

    add_box(ax, 28, 6, 24, 14,
            "LLM レイヤー\nqwen3.5:35b-a3b-nothink\n結果後の語り（Phase 9）\n結果前の判断（Phase 10）",
            fc="#f3e8ff", ec="#7b3fbf")

    add_box(ax, 60, 6, 22, 14,
            "観察素材（動画末尾）\n心の声 40 件 + 判断 40 件\n人間が監査する語り\n属性差を観察できる判断",
            fc="#eaf5ec", ec="#2f8a45")

    add_box(ax, 86, 17, 13, 14,
            "提出物\nデモ動画 185s\n本資料 PDF",
            fc="#fde7e7", ec="#c63838")

    arrow(ax, 20, 35, 28, 35)
    arrow(ax, 52, 35, 60, 35)
    arrow(ax, 40, 28, 40, 20, label="数値状態")
    arrow(ax, 52, 13, 60, 13)
    arrow(ax, 82, 35, 86, 28)
    arrow(ax, 82, 13, 86, 23)

    ax.text(50, 47.5,
            "システム構成図 — 数値計算で観察し、LLM で語りと判断を補助",
            ha="center", va="center", fontsize=12, fontweight="bold")

    plt.tight_layout()
    plt.savefig(OUT, dpi=220, bbox_inches="tight", facecolor="white")
    print(f"OK: {OUT}")


if __name__ == "__main__":
    main()
