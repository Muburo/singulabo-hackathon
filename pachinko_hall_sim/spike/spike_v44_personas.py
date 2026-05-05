"""
spike_v44_personas.py — v4.4 Step 1: 8 属性 + 1000 人サンプリング

v4.4 仕様（CLAUDE.md L1120-L1273）の最小着手:
- 8 属性パターンの定義（A 新人 〜 H パチプロ）
- 潜在変数 z（追い詰められやすさ）による相関つきサンプリング
- 各属性 125 人 × 8 = 1000 人生成
- 属性別の平均パラメータを印刷確認

このファイルは段階実装の Step 1。物理エンジン・ストレス動的化・幸福度は
後続 spike_v44_*.py で追加していく。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from math import exp

import numpy as np


def clip(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


# ============ 8 属性パターン定義（v4.4 仕様 L1129-L1145）============

@dataclass
class AttributePattern:
    """8 属性の母集団パラメータ。125 人をここから揺らしてサンプリングする。"""
    code: str                       # コード内部識別子（C_CHASE 等）
    display_name: str               # 動画表示名（追い上げ等）
    description: str                # 軽い説明
    # 平均値
    sens_mean: float
    sens_sd: float
    base_stress_mean: float
    base_stress_sd: float
    threshold_median: float         # personal_threshold（損失飽和の中央値）
    threshold_cv: float             # 対数正規の変動係数
    cash_median: float              # 初期所持金中央値
    cash_cv: float
    stress_floor_mean: float        # ストレスの最低床
    hammari_tau: float              # ハマり指数飽和の時定数
    # 追加軸（dict で属性ごとに保持、未使用は空）
    extras: dict = field(default_factory=dict)


ATTRIBUTES = [
    AttributePattern(
        code="A_NEWBIE", display_name="初心者",
        description="パチンコ屋やパチスロに慣れていない人",
        sens_mean=0.84, sens_sd=0.06,
        base_stress_mean=0.20, base_stress_sd=0.06,
        threshold_median=30000, threshold_cv=0.30,
        cash_median=10000, cash_cv=0.35,
        stress_floor_mean=0.03, hammari_tau=18,
        extras={"novelty_boost": 1.20},
    ),
    AttributePattern(
        code="B_REGULAR", display_name="ライトユーザー",
        description="月に数回程度行く人たち",
        sens_mean=0.52, sens_sd=0.07,
        base_stress_mean=0.50, base_stress_sd=0.08,
        threshold_median=60000, threshold_cv=0.35,
        cash_median=30000, cash_cv=0.40,
        stress_floor_mean=0.18, hammari_tau=14,
        extras={"habituation": 0.80, "recovery_relief_weight": 0.85},
    ),
    AttributePattern(
        code="C_CHASE", display_name="中毒者",
        description="パチスロジャンキー。借金もあり、生活に支障をきたすような打ち方",
        sens_mean=0.92, sens_sd=0.05,
        base_stress_mean=0.78, base_stress_sd=0.07,
        threshold_median=15000, threshold_cv=0.40,
        cash_median=20000, cash_cv=0.45,
        stress_floor_mean=0.48, hammari_tau=8,
        extras={
            "recovery_relief_weight": 1.35,
            "dopamine_sensitivity_boost": 1.10,
        },
    ),
    AttributePattern(
        code="D_AFTER5", display_name="アフター5層",
        description="仕事帰りのサラリーマンなど",
        sens_mean=0.72, sens_sd=0.07,
        base_stress_mean=0.45, base_stress_sd=0.07,
        threshold_median=50000, threshold_cv=0.30,
        cash_median=25000, cash_cv=0.35,
        stress_floor_mean=0.12, hammari_tau=12,
        extras={"time_pressure": 0.85},
    ),
    AttributePattern(
        code="E_LEISURE", display_name="悠々自適",
        description="経済的に余裕、暇つぶしで打つ地主や不動産持ち",
        sens_mean=0.35, sens_sd=0.06,
        base_stress_mean=0.08, base_stress_sd=0.04,
        threshold_median=220000, threshold_cv=0.30,
        cash_median=80000, cash_cv=0.40,
        stress_floor_mean=0.00, hammari_tau=24,
        extras={"emotion_damp": 0.85, "interruptibility": 0.90, "ev_focus": 0.10},
    ),
    AttributePattern(
        code="F_SENIOR", display_name="シニア",
        description="退職後、時間的な余裕が相当ある人たち",
        sens_mean=0.42, sens_sd=0.06,
        base_stress_mean=0.34, base_stress_sd=0.07,
        threshold_median=80000, threshold_cv=0.30,
        cash_median=20000, cash_cv=0.30,
        stress_floor_mean=0.10, hammari_tau=20,
        extras={"long_stay": 1.20},
    ),
    AttributePattern(
        code="G_BREATHER", display_name="主婦",
        description="家事や日常から離れて来てる",
        sens_mean=0.68, sens_sd=0.07,
        base_stress_mean=0.48, base_stress_sd=0.08,
        threshold_median=35000, threshold_cv=0.30,
        cash_median=15000, cash_cv=0.35,
        stress_floor_mean=0.12, hammari_tau=12,
        extras={"relief_weight": 1.20, "time_pressure": 0.65},
    ),
    AttributePattern(
        code="H_PRO", display_name="パチプロ",
        description="期待値で打つ、これで生活",
        sens_mean=0.25, sens_sd=0.05,
        base_stress_mean=0.22, base_stress_sd=0.05,
        threshold_median=120000, threshold_cv=0.30,
        cash_median=120000, cash_cv=0.30,
        stress_floor_mean=0.08, hammari_tau=18,
        extras={
            "emotion_damp": 0.55,
            "interruptibility": 0.65,
            "ev_focus": 0.95,
            "bad_ev_stress": 0.25,
        },
    ),
]


# ============ Persona（サンプリング後の個体）============

@dataclass
class Persona:
    """属性内の個体。125 人 × 8 = 1000 人。"""
    pid: str                         # "C_CHASE_p042" 等
    attribute_code: str
    attribute_display: str
    # 個体パラメータ
    sensory_amplitude: float         # 0〜1
    base_stress: float               # 0〜1
    personal_threshold: float        # 損失飽和の閾値（円）
    initial_cash: int
    stress_floor: float              # 0〜1
    hammari_tau: float
    # 潜在変数 z（追い詰められやすさ、サンプリング元）
    z: float
    # v4.5: 48 セル格子の機種割り当て（assign_machines で in-place 設定）
    assigned_machine: str = ""


# ============ サンプリング ============

def sample_persona_variant(attr: AttributePattern, idx: int, rng: np.random.Generator) -> Persona:
    """
    1 個体をサンプリング。
    潜在変数 z（標準正規）が、sens / stress / threshold / floor を相関させる。
    z が高いほど「追い詰められやすい」個体（C 内では兆しに過敏）。
    """
    z = float(rng.normal(0, 1))

    sens = clip(rng.normal(attr.sens_mean, attr.sens_sd) + 0.03 * z, 0.0, 1.0)
    base_stress = clip(rng.normal(attr.base_stress_mean, attr.base_stress_sd) + 0.06 * z, 0.0, 1.0)

    threshold = attr.threshold_median * exp(
        attr.threshold_cv * float(rng.normal(0, 1)) - 0.20 * z
    )
    threshold = max(1000.0, threshold)  # 数値安定のため下限

    initial_cash = int(attr.cash_median * exp(attr.cash_cv * float(rng.normal(0, 1))))
    initial_cash = max(2000, initial_cash)

    stress_floor = clip(attr.stress_floor_mean + 0.04 * z, 0.0, 1.0)

    return Persona(
        pid=f"{attr.code}_p{idx:03d}",
        attribute_code=attr.code,
        attribute_display=attr.display_name,
        sensory_amplitude=sens,
        base_stress=base_stress,
        personal_threshold=threshold,
        initial_cash=initial_cash,
        stress_floor=stress_floor,
        hammari_tau=attr.hammari_tau,
        z=z,
    )


def generate_population(n_per_attr: int = 125, seed: int = 42) -> list[Persona]:
    """8 属性 × n_per_attr 人を生成、合計 n_per_attr × 8 = 1000 人（既定）。"""
    rng = np.random.default_rng(seed)
    personas: list[Persona] = []
    for attr in ATTRIBUTES:
        for i in range(n_per_attr):
            personas.append(sample_persona_variant(attr, i, rng))
    return personas


# ============ 動作確認: 属性別平均パラメータ ============

def summarize(personas: list[Persona]) -> None:
    """属性別の平均パラメータを表示して、ばらつきが想定通りか確認。"""
    print(f"=== 生成個体数: {len(personas)} ===\n")
    print(f"{'属性':<20} {'sens':>8} {'stress':>8} {'thresh':>10} {'cash':>10} {'floor':>8} {'z':>8}")
    print("-" * 76)

    for attr in ATTRIBUTES:
        members = [p for p in personas if p.attribute_code == attr.code]
        if not members:
            continue
        sens = np.mean([p.sensory_amplitude for p in members])
        stress = np.mean([p.base_stress for p in members])
        thresh = np.mean([p.personal_threshold for p in members])
        cash = np.mean([p.initial_cash for p in members])
        floor = np.mean([p.stress_floor for p in members])
        z = np.mean([p.z for p in members])
        label = f"{attr.code} {attr.display_name}"
        print(f"{label:<20} {sens:>8.3f} {stress:>8.3f} {thresh:>10.0f} {cash:>10.0f} {floor:>8.3f} {z:>+8.3f}")

    print("\n=== 想定との一致確認ポイント ===")
    print("- C_CHASE が sens 最大 (~0.92) かつ stress 最大 (~0.78) かつ floor 最大 (~0.48)")
    print("- E_LEISURE / H_PRO が sens 最小 (~0.35 / ~0.25) かつ stress 最小")
    print("- z 平均は各属性で 0 付近（標準正規からのサンプリング）")


def main() -> None:
    personas = generate_population(n_per_attr=125, seed=42)
    summarize(personas)


if __name__ == "__main__":
    main()
