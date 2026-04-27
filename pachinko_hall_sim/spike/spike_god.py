"""
spike_god.py — 最小スパイク
1 persona × 30 step × GOD だけ。感情は arousal のみ。行動は固定（cash > 0 なら打ち続ける）。
シミュレーションがどう動くか「目で見る」ためのお試し。本番コードではない。
"""
from math import exp, log, sqrt, tanh

import matplotlib.pyplot as plt
import numpy as np

# ============ GOD 機種パラメータ（v4.1 ChatGPT 推奨値） ============
P_INITIAL_HIT = 0.025
CONTINUE_PROB = 0.50
STAKE = 1000
PAYOUT_MEAN = 21000
PAYOUT_STD = 25000
PAYOUT_CAP = 120000

# log-normal の mu / sigma を平均・標準偏差から逆算
sigma2 = log(1 + (PAYOUT_STD / PAYOUT_MEAN) ** 2)
PAYOUT_SIGMA = sqrt(sigma2)
PAYOUT_MU = log(PAYOUT_MEAN) - 0.5 * sigma2

# ============ persona（依存症末期っぽい1人） ============
INITIAL_CASH = 30000
SENSORY_GATING = 0.85
BASE_AROUSAL = 50

# ============ シミュレーション設定 ============
N_STEPS = 30
SEED = 42

rng = np.random.default_rng(SEED)

cash = INITIAL_CASH
arousal = BASE_AROUSAL
chain_active = False
miss_streak = 0

cash_hist = [cash]
arousal_hist = [arousal]
hit_hist = []

print(f"=== GOD spike: 1 persona × {N_STEPS} step, seed={SEED} ===")
print(f"return_index = p/(1-q+p)*mean/stake = "
      f"{P_INITIAL_HIT/(1-CONTINUE_PROB+P_INITIAL_HIT)*PAYOUT_MEAN/STAKE:.3f}")
print(f"initial_cash = {INITIAL_CASH:,} 円\n")
print(f"{'step':>4} {'cash':>8} {'arousal':>8} {'hit':>4} {'payout':>8} {'chain':>5}")

for step in range(1, N_STEPS + 1):
    cash -= STAKE

    hit = False
    payout = 0
    if chain_active:
        if rng.random() < CONTINUE_PROB:
            hit = True
            payout = min(rng.lognormal(PAYOUT_MU, PAYOUT_SIGMA), PAYOUT_CAP)
        else:
            chain_active = False
    else:
        if rng.random() < P_INITIAL_HIT:
            hit = True
            payout = min(rng.lognormal(PAYOUT_MU, PAYOUT_SIGMA), PAYOUT_CAP)
            chain_active = True

    cash += payout

    if hit:
        miss_streak = 0
    else:
        miss_streak += 1

    # arousal 更新（シンプル版）
    hit_signal = 1.0 if hit else 0.0
    net_delta = payout - STAKE
    gain_signal = tanh(max(0, net_delta) / 5000)
    hammari_signal = 1 - exp(-miss_streak / 12)
    cash_low_signal = 1.0 if cash <= 3000 else 0.0

    delta = (
        + 22.0 * hit_signal
        + 10.0 * gain_signal
        + 4.0 * hammari_signal
        - 3.0 * cash_low_signal
    )
    delta *= SENSORY_GATING
    delta -= 0.05 * (arousal - BASE_AROUSAL)

    arousal = max(0.0, min(100.0, arousal + delta))

    cash_hist.append(cash)
    arousal_hist.append(arousal)
    hit_hist.append(hit)

    mark = "★" if hit else "·"
    chain_mark = "on" if chain_active else "off"
    print(f"{step:>4} {cash:>8,} {arousal:>8.1f} {mark:>4} {int(payout):>8,} {chain_mark:>5}")

    if cash <= 0:
        print(f"\n→ cash 0、step {step} で強制離脱")
        break

# ============ 結果サマリ ============
total_payout = sum(int(min(0, c-cash_hist[i-1]+STAKE)) for i, c in enumerate(cash_hist[1:], 1))
n_hits = sum(hit_hist)
print(f"\n=== summary ===")
print(f"final cash: {cash:,} 円 (initial {INITIAL_CASH:,} → 差分 {cash - INITIAL_CASH:+,})")
print(f"hit count: {n_hits} / {len(hit_hist)} step ({n_hits/len(hit_hist)*100:.1f}%)")
print(f"final arousal: {arousal:.1f}")

# ============ プロット ============
steps = list(range(len(cash_hist)))

fig, ax1 = plt.subplots(figsize=(11, 5))

ax1.set_xlabel('step')
ax1.set_ylabel('cash (yen)', color='tab:blue')
ax1.plot(steps, cash_hist, color='tab:blue', marker='o', markersize=4, label='cash')
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.axhline(0, color='gray', linestyle='--', alpha=0.5)
ax1.axhline(INITIAL_CASH, color='lightgray', linestyle=':', alpha=0.7, label='initial')

# hit markers
hit_steps = [i + 1 for i, h in enumerate(hit_hist) if h]
hit_cash = [cash_hist[i + 1] for i, h in enumerate(hit_hist) if h]
if hit_steps:
    ax1.scatter(hit_steps, hit_cash, color='gold', s=140, marker='*',
                zorder=5, edgecolor='orange', linewidth=1, label='HIT')

ax2 = ax1.twinx()
ax2.set_ylabel('arousal (0-100)', color='tab:red')
ax2.plot(steps, arousal_hist, color='tab:red', marker='s', markersize=3,
         alpha=0.7, label='arousal')
ax2.tick_params(axis='y', labelcolor='tab:red')
ax2.set_ylim(0, 100)

plt.title(f'GOD spike — 1 persona × {N_STEPS} step (seed={SEED})')
fig.tight_layout()

out_path = 'spike_god_result.png'
plt.savefig(out_path, dpi=120)
print(f"\nplot saved: {out_path}")
