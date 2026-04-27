# Singulabo Hackathon — プロジェクト仕様書（v4.1 ChatGPT 再レビュー反映版）

シンギュラボのハッカソン提出用プロジェクト。
ChatGPT Pro v4 相談（2026-04-26）→ 横塚の実機経験で 5 つの歪みを発見 → v4.1 修正案を ChatGPT Pro に再レビュー依頼（2026-04-27）→ 回答反映（2026-04-28）。
物理は rule-based で安定、LLM は間引いて使う段階拡張プラン。**感情は 3 軸（arousal / despair / dissociation）で観察する**。

## 基本情報

| 項目 | 値 |
|------|-----|
| 開始日 | 2026-04-18 |
| 提出締切 | 2026-05-07 |
| id | `singulabo-hackathon` |
| 方針 | **🔬 物理実験シミュレーター路線**（rule-based physics + 間引き LLM + 解離軸） |
| 仕様の出典 | [docs/chatgpt-response-v4.md](docs/chatgpt-response-v4.md) + [docs/chatgpt-response-v4-1.md](docs/chatgpt-response-v4-1.md) |

## 動機と仮説

### 動機
ユーザーが15年間ギャンブル依存症だった経験の「答え合わせ」。
パチンコホールに **複数種類×複数台の台** を並べ、ペルソナを 10〜100人配置して
「**どういう属性の人が、どういう感情を持つか**」を観察する物理実験。

### 仮説
> **stress × comeback-cue × continuity** の相互作用で arousal/despair が変動し、
> 持続期待の時間構造（AT 短 spike vs ART 長 tether）が中毒性の質を変える。
> さらに **path dependency（生活がパチに最適化された年数）** が滞在時間と離脱判断を支配する。
> **dissociation（解離）** が arousal/despair 双方を抑制し、依存症末期や燃え尽き層に特有の「負けても静か」「焦っても観察モード」が出現する。
> **time_pressure × social_commitment_density** が「焦り」「罪悪感」を生み、ART の「帰れない感」を増幅する。

### 観察アウトカム
- カテゴリ別 arousal / despair / **dissociation** の時間推移
- 4象限（高A高D / 高A低D / 低A高D / 低A低D）別の滞在時間と離脱パターン
- 機種間の continue_rate / mean_dwell_steps / cue_memory 持続
- LLM 自己申告（reported_arousal/despair/dissociation）と canonical state のズレ
- **同じ損失でも guilt / deadline_conflict によって感情の出方がズレる**ことの観察

## 核心メッセージ（企画の一行説明）

> **同じ期待値でも、GOD は爆発、ART は拘束、沖スロは未練、4.5号機はゲーム性と波。
> さらに同じ損失でも、焦り・罪悪感・解離によって感情の出方がズレる。
> 物理状態としての感情（rule canonical）と、本人の自己申告（LLM self-report）を分けて記録する。**

## 守るべき哲学（4 つ）

1. **LLM には数値のみ渡す**（「危険」「嬉しい」等の定性ラベル禁止）
2. **物理・抽選・感情の canonical state は rule-based**（再現性・発散防止）
3. **LLM は行動決定 + 自己申告のみ**（5 step ごとに間引く）
4. **感情は 2 系統 × 3 軸で記録**:
   - canonical (rule): `arousal` / `despair` / `dissociation_level`
   - self-report (LLM): `reported_arousal` / `reported_despair` / `reported_dissociation`

これらを壊すと企画の価値が消える。

## 実装スコープ（案A → B 段階拡張）

### 案A（MVP, Day1-5）— 必ず作る
| 項目 | 値 |
|------|-----|
| persona | 10人 |
| step | 30 |
| 機種 | 3種類 × 各2台 = 6台 |
| LLM | 5 step ごとの行動決定のみ |
| 感情 | rule-based canonical + LLM self-report |
| LLM calls | 約60回 |
| 所要時間 | 5〜15分 |

### 案B（本命, Day6-8）
| 項目 | 値 |
|------|-----|
| persona | 30人 |
| step | 50 |
| 機種 | 3種類 × 各4台 = 12台 |
| LLM | 5 step ごと + 重要イベント時 |
| LLM calls | 300〜600回 |
| 所要時間 | 約22.5分 |

### 案C（フル, Day7+ 余力時のみ）
- 100 persona × 100 step / 機種 30台 / LLM 10 step ごと
- 締切では事故リスク高い。案Bが安定してからの追加実験

## 実行環境

| 項目 | 値 |
|------|-----|
| マシン | MacBook Pro (Mac16,5, 2024) |
| チップ | Apple M4 Max（CPU 16 / GPU 40, Metal 4）|
| メモリ | 64 GB unified |
| Python | 3.9.6（`/usr/bin/python3`）|
| venv | `/tmp/sing_venv`（プロジェクトパスにコロン `:` が含まれるため、venv は /tmp に逃がす）|

### Ollama 設定（API 実装時）
```python
# /api/chat への共通設定
{
    "think": False,
    "stream": False,
    "keep_alive": -1,
    "options": {
        "num_ctx": 2048,
        "num_predict": 80,
        "temperature": 0.35,
    }
}
```

### モデル戦略
| モデル | 用途 |
|--------|------|
| `qwen3:4b-instruct-2507-q4_K_M` (2.5GB) | **主軸 backbone**。これだけで完成させる |
| `qwen3:30b` (19GB) | 案C 余力時のみ前景に |
| `qwen3.5:35b-a3b` (23GB) | 5/03 以降の最終 polish のみ |

**遅いからといって "より新しくて大きいモデル" に逃げない**。qwen3:4b 主軸固定。

## ディレクトリ構成

```
projects/singulabo-hackathon/
├── CLAUDE.md                  # 本ファイル（v4 SSoT）
├── README.md
├── docs/                      # 相談プロンプト・回答（v1-v4）、多経路モデル等
│   ├── chatgpt-response-v4.md # ★ 仕様の出典
│   ├── chatgpt-response-v3.md
│   ├── 相談プロンプト-v4.md
│   ├── multi-path-addiction-model.md
│   └── ...
├── persona-cards/             # DR で集めた 169 cards
│   └── all-cards-merged.yaml
├── reports/
│   └── R1-R3-aggregation.md   # persona 統計
├── reference/                 # 配布コード（参考用、触らない）
├── scripts/
│   ├── extract_yaml_cards.py
│   ├── aggregate.py
│   └── sample_personas.py     # 🆕 persona 10人 sampling
└── pachinko_hall_sim/         # 🆕 本体実装
    ├── README.md
    ├── requirements.txt
    ├── data/
    │   └── persona_cards.jsonl # 10人 sampling 結果
    ├── configs/
    │   ├── machines.yaml      # 3機種パラメータ
    │   └── run_mvp.yaml       # 案A 設定
    ├── src/
    │   ├── models.py          # dataclass 定義
    │   ├── persona_loader.py
    │   ├── machine.py         # 抽選物理
    │   ├── emotion.py         # 感情更新ルール
    │   ├── policy_rule.py     # rule-based 行動
    │   ├── policy_llm.py      # LLM 行動 + self-report
    │   ├── llm_client.py      # Ollama wrapper
    │   ├── simulator.py       # メインループ
    │   ├── logger.py          # JSONL ロガー
    │   ├── visualize.py       # matplotlib 可視化
    │   └── run_simulation.py  # CLI エントリポイント
    └── outputs/               # log, plot, animation
```

## 機種設計（4 分類）

**コード上の名称は「機械割」ではなく `target_return_index`** とする（実機再現ではなく抽象モデルの期待値だから）。

`return_index = hit_rate * payout_mean / stake`
- chain あり機種: `hit_rate = p_initial_hit / (1 - continue_prob + p_initial_hit)`
- chain なし機種（純A）: `hit_rate = p_initial_hit`

| id | 機種分類 | chain_mode | p_initial_hit | continue_prob | stake | payout_dist | payout_mean | payout_std | payout_cap | cue_decay | target_return_index | 狙い |
|----|---------|-----------|--------------|--------------|-------|------------|-------------|-----------|-----------|-----------|--------------------|------|
| 0 | 2000s 爆裂AT / GOD系 | chain | 0.025 | 0.50 | 1000 | lognormal | 21000 | 25000 | 120000 | 1 | 約100% | 一撃・破壊・興奮ピーク |
| 1 | 4.5号機（北斗・吉宗・番長代表） | chain | 0.060 | 0.58 | 1000 | lognormal | 8300 | 5600 | 80000 | 2 | 約104% | ゲーム性と波 |
| 2 | 2010s 爆裂ART | chain | 0.030 | 0.83 | 1000 | lognormal or gamma | 6700 | 4000 | 60000 | 5 | 約100% | 拘束・終わらなさ |
| 3 | マイルド純A・沖スロ（ジャグラー/ハナハナ寄せ） | none | 0.200 | 0.00 | 1000 | clipped_normal | 5000 | 2000 | 20000 | 1 | 約100% | 未練・ちょい当たり頻発 |

**重要**:
- ID3 純A は **`chain_mode="none"` 必須**。`continue_prob=0` だけで chain ロジックに流すと、当たり後に死に step が出る
- `payout_cap` は log-normal の暴走から動画を守るため。cap 後の実 return は calibration script で必ず実測する
- ART（ID2）の 30 step 有限 run では低めに見えるが、それは「入口が狭い」「入れば伸びる」の正しい質感。Day5 で差が見えづらければ p_initial_hit=0.035 に上げてもよい

### log-normal パラメータ計算

`np.random.lognormal(mu, sigma)` の引数は背後の正規分布の `mu / sigma` であり、log-normal 自身の平均ではない。`m` が平均、`s` が標準偏差なら:

```python
sigma2 = log(1 + (s / m) ** 2)
sigma = sqrt(sigma2)
mu = log(m) - 0.5 * sigma2
```

ID0 GOD（mean=21000, std=25000）→ mu=9.51097, sigma=0.93948
ID1 4.5号機（mean=8300, std=5600）→ mu=8.84, sigma=0.62（参考値）
ID2 ART（mean=6700, std=4000）→ mu=8.65, sigma=0.55（参考値）

**1 step = 1000円分の遊技**。時間より残金変化が分かりやすい単位。

## 14経路中毒モデルの圧縮

14経路を1つのスカラー `addiction_load` に圧縮:

```python
addiction_load = clip(
    0.45 * path_dependency_score    # ★ 最重要
    + 0.20 * payday_sensitivity
    + 0.15 * (1.0 - interruptibility)
    + 0.10 * sensory_gating_factor
    + 0.10 * time_cost_efficiency,
    0.0, 1.0
)
```

詳細な多経路モデルは [docs/multi-path-addiction-model.md](docs/multi-path-addiction-model.md) を参照（V4 では運用しないが、論文・記事化のとき活用）。

## カテゴリ別 path_dependency_score 仮値

| カテゴリ | path_dependency_score |
|---------|-----------------------|
| 不労所得・地主層 | 0.20 |
| 中年現役男性 | 0.55 |
| 依存症末期 | 0.95 |
| 精神疾患併発 | 0.70 |
| 主婦 | 0.50 |
| OL・社会人女性 | 0.50 |
| 女子大生・若年女性 | 0.35 |
| 年金生活高齢男性 | 0.60 |
| 年金生活高齢女性 | 0.60 |
| 風俗・夜職系女性 | 0.65 |
| 退職前後・早期リタイア男性 | 0.55 |

## 現金モデル（initial_cash + accessible_cash）

「財布薄いが長く打つ」依存症末期の現実味を出すため、現金を 2 層に分ける。

- `initial_cash` = 財布の中の現金（ホール入店時点）
- `accessible_cash` = ATM・借金・カード・生活費流用を含む、そのセッションでアクセス可能な追加資金
- 残金が一定閾値（例: 3000円）を切ると、persona ごとに `accessible_cash` から補充する判断ロジックを通す（rule-based。ただし MVP では「全額一括補充」「stigma_barrier > 0.7 なら補充しない」程度の単純化でよい）

| カテゴリ | initial_cash | accessible_cash / credit_limit |
|---------|--------------|------------------------------|
| 不労所得・地主層 | 50000〜100000 | 100000〜200000 |
| 中年現役男性 | 20000〜40000 | 30000〜80000 |
| 依存症末期 | 10000〜30000 | 50000〜150000 |
| 主婦 | 10000〜20000 | 10000〜50000 |
| OL・社会人女性 | 15000〜30000 | 20000〜60000 |
| 女子大生・若年女性 | 5000〜12000 | 0〜20000 |
| 年金生活高齢 | 10000〜30000 | 0〜30000 |
| 風俗・夜職系女性 | 20000〜60000 | 20000〜100000 |

## 追加 persona / session 属性（v4.1）

### persona 固有
- `time_pressure` (0.0〜1.0) — 時間圧の感じやすさ。生活全般での「焦り傾向」
- `target_leave_step` (int) — このセッションで離脱を予定している step。閉店まで打つ依存症末期は大きく、子供のお迎えがある主婦は小さい

### session context（persona 固有ではなく、その日の状況）
- `social_commitment_density` (0.0〜1.0) — 親の手術中・結婚式当日・子供を1人で待たせている等の「他者への約束密度」
- `commitment_intensity` (0.0〜1.0) — 同 commitment の重み（軽い予定 vs 緊急性高）

これらを persona trait と混同しない。session_context を別 dict で渡し、experiment 条件として独立に振れるようにする。

## Persona Sampling

### 案A（10人）
- 不労所得 1, 中年現役 1, 依存症末期 2, 精神疾患併発 1, 主婦 1
- OL 1, 女子大生 1, 年金生活高齢 1, 風俗 1

### 案B（30人）
各カテゴリから 2-3 人。依存症末期 / 不労所得 / 中年現役男性 / 若年女性 は多め。
カテゴリ別だけでなく **4象限別** でも集計（n=30 だと象限の方が安定）。

### 案C（100人）
169枚から stratified sampling。カテゴリ別比較に説得力出る段階。

## 物理モデル（抽選ロジック）

```python
def play_one_step(persona, machine, machine_type, rng):
    stake = machine_type.stake_per_step
    persona.cash -= stake
    persona.total_spent += stake

    hit, payout = False, 0

    if machine_type.chain_mode == "none":
        # 純A・沖スロ: chain ロジックを通さない
        if rng.random() < machine_type.p_initial_hit:
            hit = True
            payout = sample_payout(machine_type, rng)
        machine.chain_active = False  # 常に非継続状態
    else:
        # chain あり機種（GOD / 4.5号機 / ART）
        if machine.chain_active:
            if rng.random() < machine_type.continue_prob:
                hit = True
                payout = sample_payout(machine_type, rng)
                machine.chain_active = True
            else:
                machine.chain_active = False
        else:
            if rng.random() < machine_type.p_initial_hit:
                hit = True
                payout = sample_payout(machine_type, rng)
                machine.chain_active = True

    persona.cash += payout
    persona.total_payout += payout
    return hit, payout, payout - stake


def sample_payout(machine_type, rng):
    """payout_dist に応じて分布を切り替え、cap で頭打ち"""
    if machine_type.payout_dist == "lognormal":
        sample = rng.lognormal(machine_type.payout_mu, machine_type.payout_sigma)
    elif machine_type.payout_dist == "gamma":
        sample = rng.gamma(machine_type.payout_shape, machine_type.payout_scale)
    elif machine_type.payout_dist == "clipped_normal":
        sample = max(0.0, rng.normal(machine_type.payout_mean, machine_type.payout_std))
    else:
        raise ValueError(machine_type.payout_dist)
    return min(sample, machine_type.payout_cap)
```

### Calibration script 必須

`scripts/calibration_check.py` を最初に書く。各 machine_type を 10000 step 回して `return_index` を実測し、cap 後の平均を確認する。パラメータ変更時は必ずこれで検証する。

### ハマりと cue 計算

```python
if hit:
    persona.win_streak += 1
    persona.miss_streak = 0
    machine.machine_miss_streak = 0
    machine.cue_level = 1.0
else:
    persona.win_streak = 0
    persona.miss_streak += 1
    machine.machine_miss_streak += 1
    machine.cue_level *= exp(-1 / machine_type.cue_decay_steps)

persona.cue_memory = (
    persona.cue_memory * exp(-1 / machine_type.cue_decay_steps)
    + (1.0 if hit else 0.0) * machine_type.continue_prob
)
persona.cue_memory = clip(persona.cue_memory, 0.0, 1.0)
```

## 感情モデル（v4.1: 3 軸 + suppression）

### 入力特徴量

すべて bounded signal（0〜1 または有限範囲）。長時間 run でも暴走しないこと。

```python
# 残金・損益
loss_ratio = max(0.0, (initial_cash - cash) / max(1, initial_cash))
loss_burn = tanh(max(0.0, initial_cash - cash) / max(initial_cash, 20000))
loss_signal = tanh(max(0, -net_delta) / 3000)
gain_signal = tanh(max(0, net_delta) / 5000)
cash_low_signal = 1.0 if cash <= 3000 else 0.0

# ハマり・cue
hammari_signal = 1.0 - exp(-miss_streak / 12.0)
cue_signal = cue_memory

# 時間・拘束
time_fatigue = 1.0 - exp(-time_in_hall / 80.0)

# 焦り（時間圧）
progress = current_step / max(1, target_leave_step)
deadline_progress = clip(progress, 0.0, 1.5)
overrun = clip(progress - 1.0, 0.0, 1.0)
time_pressure_signal = persona.time_pressure * deadline_progress

# 罪悪感（session context）
guilt_signal = session.social_commitment_density * clip(
    0.30 + 0.70 * deadline_progress + 0.50 * overrun,
    0.0, 1.5,
)

# ART の「帰れない感」
if machine.chain_active:
    expected_chain_tail = machine_type.continue_prob / max(0.05, 1.0 - machine_type.continue_prob)
else:
    expected_chain_tail = cue_memory * machine_type.cue_decay_steps
remaining_steps = max(0, target_leave_step - current_step)
deadline_conflict = persona.time_pressure * clip(
    (expected_chain_tail - remaining_steps) / 10.0,
    0.0, 1.0,
)
```

### dissociation_level（解離軸）

低A高D persona は最初から少し解離している。base 値を持たせる:

```python
base_dissociation = clip(
    0.35 * max(0.0, base_despair - base_arousal)
    + 10.0 * addiction_load,
    0.0, 45.0,
)
```

更新式（delta は ±3.0 で cap、bounded signal のみ使用）:

```python
chain_monotony = (
    (1.0 - exp(-win_streak / 4.0)) * machine_type.continue_prob
    if machine.chain_active else 0.0
)
relief_signal = clip(gain_signal + 0.25 * hit_signal, 0.0, 1.0)
break_signal = 1.0 if action == "take_break" else 0.0

delta_dissociation = (
    + 0.90 * loss_burn
    + 0.70 * hammari_signal
    + 0.50 * time_fatigue
    + 0.60 * chain_monotony
    + 0.70 * guilt_signal
    + 0.50 * cash_low_signal
    + 0.50 * persona.addiction_load * loss_burn
    - 1.00 * relief_signal
    - 1.50 * break_signal
    - 0.03 * (dissociation_level - base_dissociation)
)
delta_dissociation = clip(delta_dissociation, -3.0, 3.0)
dissociation_level = clip(
    dissociation_level + delta_dissociation + noise_dissociation,
    0.0, 100.0,
)
```

### suppression（解離による感情鈍化）

完全には消えないが、かなり鈍る（下限 0.30）:

```python
suppression = 1.0 - 0.70 * (dissociation_level / 100.0) ** 1.3
suppression = clip(suppression, 0.30, 1.0)
# dissociation=0 → 1.0 / =50 → 0.72 / =75 → 0.52 / =100 → 0.30
```

### arousal 更新

```python
raw_delta_arousal = (
    + 22.0 * hit_signal
    + 10.0 * gain_signal
    +  6.0 * cue_signal
    +  4.0 * hammari_signal
    +  5.0 * time_pressure_signal * hammari_signal
    +  5.0 * deadline_conflict
    -  3.0 * cash_low_signal
)
raw_delta_arousal *= persona.sensory_gating_factor
delta_arousal = suppression * raw_delta_arousal
delta_arousal -= 0.05 * (arousal - base_arousal)  # 自然減衰
arousal = clip(arousal + delta_arousal + noise_arousal, 0.0, 100.0)
```

### despair 更新

```python
raw_delta_despair = (
    + 16.0 * loss_signal
    + 12.0 * loss_ratio
    +  8.0 * cash_low_signal
    +  5.0 * hammari_signal
    +  4.5 * guilt_signal
    +  3.0 * deadline_conflict * session.social_commitment_density
    - 10.0 * gain_signal
)
raw_delta_despair *= (0.7 + base_despair / 100.0)  # despair trait 増幅
raw_delta_despair += 4.0 * persona.time_cost_efficiency * hammari_signal
delta_despair = suppression * raw_delta_despair
delta_despair -= 0.03 * (despair - base_despair)  # 自然減衰
despair = clip(despair + delta_despair + noise_despair, 0.0, 100.0)
```

### 哲学的含意

- dissociation が高い persona は hit/loss/guilt への反応が鈍る → 「**負けているのに静か**」「**焦っているのに観察モード**」「**悟りっぽい**」が出る
- dissociation 自体は損失・ハマり・拘束・罪悪感で上がる
- guilt は独立軸にせず despair / dissociation の signal として流す（軸を増やしすぎない）
- raw_delta も suppressed delta も両方ログに残す（観察と解釈のため）

## 行動モデル（4択 + LLM/rule）

### 行動の選択肢

```
0 = continue_same_machine
1 = switch_machine
2 = take_break
3 = leave_hall
```

### rule-based fallback

```python
urge_to_continue = (
    + 0.035 * arousal
    + 0.030 * cue_memory * 100
    + 0.025 * addiction_load * 100
    + 0.020 * payday_sensitivity * 100
    - 0.030 * despair
    - 0.025 * interruptibility * 100
    - 0.040 * cash_low_signal * 100
)
p_continue = sigmoid((urge_to_continue - 2.0) / 2.0)

if cash <= 0:
    action = leave_hall
elif cash <= 3000 and despair > 70:
    action = leave_hall or take_break
elif rng.random() < p_continue:
    action = continue_same_machine
elif despair > 65 and interruptibility > 0.6:
    action = take_break
else:
    action = switch_machine
```

### LLM prompt 設計（数値のみ、v4.1）

入力例:
```json
{
  "persona_static": {
    "category_id": 3,
    "arousal_base": 78, "despair_base": 81,
    "interruptibility": 0.22, "sensory_gating_factor": 0.91,
    "stigma_barrier": 0.74, "payday_sensitivity": 0.63,
    "time_cost_efficiency": 0.41, "path_dependency_score": 0.95,
    "addiction_load": 0.82,
    "time_pressure": 0.65, "target_leave_step": 50
  },
  "persona_state": {
    "cash": 6000, "initial_cash": 20000, "accessible_cash": 80000,
    "arousal": 88, "despair": 76, "dissociation_level": 62,
    "miss_streak": 9, "win_streak": 0,
    "time_in_hall": 23, "cue_memory": 0.61
  },
  "session_context": {
    "social_commitment_density": 0.40,
    "commitment_intensity": 0.30,
    "current_step": 23
  },
  "derived_signals": {
    "guilt_signal": 0.42,
    "deadline_conflict": 0.31
  },
  "current_machine": {"machine_type_id": 2, "machine_miss_streak": 12, "cue_level": 0.44, "recent_hit_count": 1},
  "candidate_machine_summary": [...],
  "valid_actions": [0, 1, 2, 3]
}
```

出力 schema（reason は入れない、JSON 崩れ防止）:
```json
{"action": 0, "target_machine_type_id": 2, "reported_arousal": 91, "reported_despair": 73, "reported_dissociation": 65, "confidence": 0.74}
```

## ログ schema（1 step 1 row, v4.1）

```json
{
  "run_id": "mvp_seed_42",
  "step": 17,
  "persona_id": "R3_012",
  "category": "依存症末期",
  "machine_id": "ART_03",
  "machine_type_id": 2,
  "action": 0,
  "action_source": "rule" | "llm" | "fallback",
  "hit": false, "payout": 0, "stake": 1000, "net_delta": -1000,
  "cash": 7000, "accessible_cash": 80000, "cash_refilled_this_step": false,
  "arousal": 84.2, "despair": 71.5, "dissociation_level": 62.4,
  "raw_delta_arousal": 4.2, "raw_delta_despair": 6.8, "raw_delta_dissociation": 0.9,
  "suppression": 0.61,
  "llm_reported_arousal": 88, "llm_reported_despair": 69, "llm_reported_dissociation": 65,
  "miss_streak": 8, "win_streak": 0,
  "cue_memory": 0.53, "time_in_hall": 17,
  "guilt_signal": 0.42, "deadline_conflict": 0.31, "time_pressure_signal": 0.34,
  "interruptibility": 0.22, "sensory_gating_factor": 0.91,
  "stigma_barrier": 0.74, "payday_sensitivity": 0.63,
  "time_cost_efficiency": 0.41, "path_dependency_score": 0.95,
  "addiction_load": 0.82,
  "time_pressure": 0.65, "target_leave_step": 50,
  "social_commitment_density": 0.40
}
```

**ログ設計の原則**:
- `raw_delta_*` と suppression 後の delta を両方残す（解離による鈍化の観察用）
- `guilt_signal` / `deadline_conflict` / `time_pressure_signal` などの中間 signal もログに残す（提出時の解説で「同じ損失でも guilt によってズレる」を可視化するため）

## 可視化仕様（6種, v4.1）

1. **属性別 arousal 推移**: x=step, y=mean arousal, group=category or quadrant
2. **属性別 despair 推移**: 同上、despair
3. **属性別 dissociation 推移**: 同上、dissociation_level（v4.1 追加）
4. **最終状態 3軸 scatter**: x=final arousal, y=final despair, **z=final dissociation（または点サイズ/色強度で表現）**, color=category, size=total_spent
5. **個別 persona timeline**: x=step, y1=cash, y2=arousal, y3=despair, **y4=dissociation_level**, marker=hit/leave/cash_zero/cash_refill
6. **ホール俯瞰動画**: machines=grid 上の固定点、persona=machine 上に表示、marker size=arousal、**marker alpha=1-suppression（解離してる人は薄く描く）**、frame=step（matplotlib animation）

## 動画演出方針（ハイブリッド方式, 2026-04-28 確定）

提出動画は **「全 persona を見せる」のではなく「3 主役にスポットライトする」**。spike_hybrid.py で概念実証済み。

### 主役 3 人の事後選定

シミュレーションを 1 回完走させてから、履歴を読んで以下のロジックで主役を決める。

| 役 | 選定基準 | キャッチコピー候補 |
|---|---------|-------------------|
| 🔥 最熱狂 | 全期間で **arousal ピーク**最大 | 「当たらないのに興奮し続けた」 |
| 💀 最絶望 | 全期間で **despair ピーク**最大 | 「焦りで判断が壊れた」 |
| 🧊 最解離 | 全期間で **despair − arousal ギャップ**最大 | 「負けてるのに静か」 |

選定が重複したら次点へ。3 人とも違う persona / カテゴリ になるよう調整する。

### レイアウト（提出動画想定）

```
┌────────────────────────┬──────────────────┐
│  左：ホール俯瞰          │  右上：🔥 最熱狂   │
│   ・全 persona dot     │   ・dot + 状態    │
│   ・3 主役にゴールド    │   ・興奮/絶望メーター│
│     破線リング         │   ・残金 + 機種    │
│   ・機種 4 つ grid     │   ・💭 心の声     │
│                       ├──────────────────┤
│                       │  右中：💀 最絶望   │
│                       ├──────────────────┤
│                       │  右下：🧊 最解離   │
└────────────────────────┴──────────────────┘
```

### 各スポットライト枠の表示要素

- **dot**: サイズ = arousal、縁色 = despair（gray→purple→crimson）
- **状態ラベル**: 熱 / 焦 / 鬱 / 凪 / 倦 / ・ の 1 文字（classify_state ロジック）
- **興奮度メーター**（赤バー）+ 数値
- **絶望度メーター**（青バー）+ 数値
- **残金**: 数値（円表記）+ **現在の機種名**
- **💭 心の声**: 吹き出し風の囲みで 1 文表示

### 心の声の生成（Phase 別）

| Phase | 実装 | 状態 |
|-------|------|------|
| spike (今) | 状態カテゴリ別の固定セリフ辞書、ランダム選択 | 5-7 種類のステレオタイプ、繰り返しが目立つ |
| 本番（Day4-7）| LLM（qwen3:4b）で persona 属性 + 数値状態 + 機種から動的生成 | 自然な口語、persona 個性が出る |

### 心の声 LLM prompt 設計（本番実装の要件）

```
あなたは {category}（{age}歳、{gender}）。
今、{machine_name} の前で {step} 回目の遊技。
残金 {cash}円（最初は {initial_cash}円）、
miss_streak {miss_streak}、
興奮度 {arousal:.0f}/100、絶望度 {despair:.0f}/100。

今の気持ちを **30 字以内、一人称、句点なし** で書いてください。
人名・地名・固有名詞は禁止。
```

要件：
- temperature 0.5〜0.7 で多様性確保
- 同じ表現の繰り返しを抑制（recent voices を prompt に渡して "違うことを言って"）
- 5 step ごとに取得（毎 step は重い）
- 印象的な瞬間（cash 0、初当たり、退場、解離ピーク）には強制発話

### 動画の構成（2 分目安）

```
[0:00-0:15] タイトル「鶴子 / パチスロ実践！人の心理シミュレーション」+ 一行説明
[0:15-0:30] セットアップ: ホール、機種 4 種、persona 6-10 人
[0:30-0:45] 「3 人をピックアップします」字幕、主役 3 人の紹介
[0:45-1:45] step 1-30 を 4 倍速で、心の声と数値が並走
[1:45-2:00] 結果: 3 主役の最終状態 + ホール全体の 3 軸 scatter
[2:00] 締め: 「物理は同じでも、感じ方は違う」字幕、限界・倫理の一言
```

### 何を見せたいかの哲学

- **物理 ≠ 自己申告 ≠ 心の声 のズレ**を観客に体感させる
- 「同じ機種でも、属性によって体験が違う」ではなく **「同じ環境にいても、感じ方が違う」** に主軸
- 3 主役は **同じ機種** で揃える方が「**人が違う**」を強調できる（v4.1 では同じ GOD で 3 人並べる案も検討）
- **観客は審査員**。データサイエンティストではないので、グラフより **物語と心の声**で刺す

## マイルストーン（Day0-11, v4.1 ChatGPT 案）

Day1（4/27）は v4.1 仕様確定で消費されたため、Day1 と Day2 を 4/28 にまとめる。

| Day | 日付 | 目標 | 順調判定 |
|-----|------|------|---------|
| Day0 | 4/26 | v4 仕様凍結、スケルトン作成、persona JSONL 生成 | CLAUDE.md / pachinko_hall_sim/ / data/persona_cards.jsonl 揃う |
| Day1 | 4/27 | v4 → v4.1 仕様レビュー | ChatGPT v4.1 回答受領、CLAUDE.md v4.1 反映 |
| **Day2** | **4/28** | **CLAUDE.md v4.1 反映 + spike 4 本で動画イメージ確定** | **spike_god / spike_hall_live / spike_hall_live_v2 / spike_hybrid 完成。横塚が画面で動きを確認、ハイブリッド方式（事後選定 3 主役）を確定** |
| **Day3** | **4/29** | **本番実装着手: machines.yaml 4機種化 + calibration + dataclass + persona_loader + machine.py + emotion.py** | **calibration_check.py で return_index 実測。10 persona × 30 step × 4機種 が LLM なしで完走、log.jsonl が出る** |
| Day4 | 4/30 | LLM wrapper + 心の声 prompt 設計 + 可視化雛形 | qwen3:4b が JSON で action を返す。心の声 prompt の動作確認。fallback 経路完成 |
| Day5 | 5/1 | **案A MVP 完走 + ハイブリッド可視化** | 10 persona × 30 step、log、3 軸グラフ、ハイブリッド可視化（事後選定 3 主役）の MP4 が出る |
| Day6 | 5/2 | 案B 30 persona × 100 step rule-only + 心の声 LLM 統合 | 30×100 が安定。心の声が persona 属性ごとに違う表現で出る |
| Day7 | 5/3 | LLM 間引き導入 + 動画強化 | 30×100 で LLM 10 step 間隔、心の声は 5 step 間隔が完走 |
| Day8 | 5/4 | 比較実験 + 提出 run 固定 | baseline / ART-heavy / time-pressure-heavy の 3 条件を回し、提出に使う 1 run を選ぶ |
| Day9 | 5/5 | 解説文章作成 + 動画タイトル/字幕 | 「実機再現ではなく世代差の質感観察」「canonical と self-report と心の声のズレ」を 4-6 ページに圧縮 |
| Day10 | 5/6 | パッケージング | README、実行コマンド、出力例、動画ファイル名規則、PDF 化、GitHub 整備 |
| Day11 | 5/7 17:00 | **提出** | Google Form に MP4 + PDF + GitHub URL。新機能追加禁止 |

### 危険判定ライン

| 日付 | 状態 | 判断 |
|------|------|------|
| 5/1 時点で 10 × 30 が完走しない | 危険 | LLM 外し、rule-only + post-process LLM に縮退 |
| 5/3 時点で動画が出ない | やや危険 | 動画簡素化、グラフとケーススタディ重視 |
| 5/5 時点で 30 × 100 が不安定 | 危険 | 10 × 30 を完成版として磨く |
| 5/6 に新機能を足したい | 禁止 | バグを増やすだけ |

### 縮退順序

1. dissociation を log だけにして suppression を一時 OFF
2. active 数を減らす（30 → 24 → 12 → 8）
3. 30×100 を 20×80 に落とす
4. 機種を 2 種類に（GOD vs ART）
5. 行動決定を rule-only に
6. LLM を self-report post-process のみに
7. 動画は個別 timeline 3 本 + 最終 scatter を主力にする

## ハマる罠（v4.1 更新版）

### 既存の罠（v4 から継続）

| # | 罠 | 対策 |
|---|----|------|
| 1 | LLM JSON が崩れる | JSON 抽出、schema validation、fallback rule 必須 |
| 2 | 毎 step LLM | 5 step ごと、またはイベント時のみ |
| 3 | 感情遷移が発散 | clip(0,100)、変化量上限、減衰項、bounded signal |
| 4 | 台の物理をリアルにしすぎる | 抽象モデルにする |
| 5 | 169 cards 全投入 | stratified sample 10 → 30 |
| 6 | 14経路を全部 dynamic | `addiction_load` に圧縮 |
| 7 | 可視化を後回し | Day5 で簡易動画まで作る |
| 8 | seed を固定しない | `--seed` 必須 |
| 9 | ログ設計が雑 | 1 step 1 row の JSONL/CSV、raw_delta も残す |
| 10 | LLM 出力を信じすぎる | canonical state は rule-based |
| 11 | qwen3:30b を使いたくなる | 4b 主軸 |
| 12 | 配布コードに寄せすぎる | `reference/` は触らない、参考用に残すだけ |

### v4.1 で新たに踏みそうな罠

| # | 罠 | 症状 | 対策 |
|---|----|------|------|
| 13 | GOD の平均だけ上げて満足 | return_index がまだ低い | 必ず `p / (1 - q + p) * mean / stake` で確認、calibration_check.py で実測 |
| 14 | log-normal が動画を壊す | 1人だけ20万円勝ち、全部その人の絵になる | `payout_cap` を入れる、または y軸を分ける |
| 15 | cap 後に平均が下がる | 校正したはずなのに負けすぎる | 10000回 calibration script で cap 後の実 return を確認 |
| 16 | dissociation が全員 100 | 感情線が全部鈍る | 非有界項を使わない、delta cap ±3.0 |
| 17 | guilt が強すぎる | commitment 高い persona が全員 despair 100 | guilt_signal を clip、重みは 4.5 から開始 |
| 18 | time_pressure が離脱だけを促す | ART の「帰れない」が出ない | `deadline_conflict` と `expected_chain_tail` を入れる |
| 19 | 純Aが chain ロジックで歪む | 当たり後に謎の死に step が出る | `chain_mode="none"` 必須 |
| 20 | initial_cash が少ない人が即退場 | 依存症末期の長時間滞在が出ない | `accessible_cash` / credit_limit を追加 |
| 21 | 4機種になって可視化が散る | 10 persona ではカテゴリ差が読めない | Day5 はカテゴリ別より個別ケース重視 |
| 22 | 200 step に LLM を入れすぎる | 実行時間と JSON 崩れが増える | 200 step は rule-only または LLM 10〜20 step 間隔 |
| 23 | 提出文章で実機再現を謳いすぎる | スペック警察に刺される | 「世代差の質感観察」と明記、機械割→target_return_index |
| 24 | 依存症描写がセンセーショナル化 | 企画意図が誤解される | 限界・倫理・抽象モデルであることを書く |
| 25 | session context と persona trait の混同 | 親の手術中・結婚式当日が「人格」になる | session_context を別 dict にする |

## Claude Code 分担表

### Claude Code に書かせる
- dataclass 定義（`models.py`）
- machine physics（seed 固定、単体テスト付き）
- emotion rule（0-100 clip、発散防止）
- simulator loop（LLM なしで動くように先に作る）
- JSONL logger（1 step 1 row）
- CSV export
- matplotlib 可視化
- Ollama wrapper（timeout / retry / fallback 必須）
- JSON parser / validator（壊れたら fallback）
- CLI（`--config --seed --no-llm`）
- README 雛形

### 自分で判断する
- どの persona を選ぶか
- machine パラメータ（観察したい現象に合わせて）
- 感情式の重み（実験の哲学）
- どのグラフを提出するか
- 結果の解釈
- 169 cards / 14経路モデルの説明（DR 文脈）
- 最終 README / 解説文

## 実装優先順位（絶対この順番, v4.1）

1. **calibration_check.py**（最初に書く。machine_type の return_index を実測）
2. dataclass 定義（`models.py`）
3. machine physics（chain_mode 対応、純A は no-chain）
4. LLM なし simulation（rule-only）
5. emotion rule（3 軸: arousal / despair / dissociation, suppression）
6. JSONL logging（raw_delta も残す）
7. basic plots（カテゴリ別 3 軸推移）
8. LLM action
9. LLM self-report（3 軸）
10. animation（解離している人は薄く）
11. case study
12. comparison experiments

LLM wrapper を先に作ると詰まる。**まず rule-only で「物理実験」が動くことが最優先**。
パラメータ変更時は **必ず calibration_check** を回してから感情モデルに進む。

## 提出物

### 構成
1. ソースコード（GitHub）
2. シミュレーション結果の可視化動画
3. 解説文章

### 解説文章の核心構成
1. 問題意識: 「人が場所を選ぶ空間」ではなく「台の確率物理 × persona の感情状態が相互作用する場」としてモデル化
2. 物理モデル: 当たり / 連荘 / ハマり / cue decay
3. persona モデル: 数値属性のみで定義
4. LLM の役割: 物理を決めない、numeric state のみで行動決定 + 自己申告
5. 観察結果: 高 addiction_load 群は cue 持続台で滞在しやすい等
6. **限界**: 実機再現でなく抽象物理モデル / カテゴリ別 n 限定 / LLM 自己申告の安定性課題

**限界を書いた方が、むしろ実験として誠実に見える**。

## 運用ルール

### 自律実行
- コード実装、Claude Code subagent、作業ジャーナル更新、git commit は確認なし
- 破壊的操作（reference/ の改変、大規模設計変更）はユーザーに確認
- 迷ったら「ゲートを守る」側で判断

### ハッカソン伴走モード（feedback memory より）
- ユーザーが手を動かす機会を残す（venv 構築・実装着手・コマンド実行）
- 「やっておいて」と明示されても学習目的タスクでは「手を動かす方が学べるけどどっちがいい？」と一度聞く
- 業務タスク（分析・レポート・git 操作）の自律実行ルールとは切り離して運用

### コミット
- calchan:/CLAUDE.md のコミット規約に従う
- `reference/` は基本 touch しない

### ログ
- 作業記録: calchan:/memory/work-journal.md
- ハマり: calchan:/memory/gotchas.md

### 環境メモ
- venv は `/tmp/sing_venv` に置く（プロジェクトパスにコロン `:` が含まれて pip が壊れるため）
- 実行: `/tmp/sing_venv/bin/python <script>`

## 進捗ログ

### 2026-04-28（Day1 + Day2 統合）— 動画イメージ確定

**やったこと**:
- ChatGPT Pro v4.1 再レビュー回答受領、CLAUDE.md を v4.1 全面書き換え（318 行追加）
- `docs/chatgpt-response-v4-1.md` 新規作成（フル回答保存）
- ハッカソン提出仕様確定（チーム名「鶴子」、作品名「パチスロ実践！人の心理シミュレーション」、ファイル命名規則、Google Form 提出）
- spike を 4 本書いて画面で動作確認:
  1. `spike_god.py` — 1 persona × 30 step × GOD のみ。「30 step は短い、当たらない run も普通」を体感
  2. `spike_hall_live.py` — 6 persona × 4 機種のホール俯瞰ライブ表示（日本語フォント問題を確認）
  3. `spike_hall_live_v2.py` — 日本語フォント修正、3 軸感情、メーター付き、状態ラベル付き
  4. `spike_hybrid.py` — 事後選定で 3 主役決定、スポットライト枠 + 心の声（テンプレ辞書）
- 動画演出方針を **ハイブリッド方式**（最熱狂 + 最絶望 + 最解離の 3 主役スポットライト）で確定

**学び**:
- 仕様詰めより**動かす**のが先。spike を見ないと感覚が掴めない
- **全員表示は情報過多**。3 主役にスポットライト + 全体俯瞰の構成が正解
- 心の声 5-7 種類のステレオタイプは表現力不足、本番は LLM 必須
- 「**何を見せるか**」が動画の良し悪しを決める（**何を作るか**より上位の問い）
- 「**同じ環境にいても、感じ方が違う**」が企画の核。物理 ≠ 自己申告 ≠ 心の声 のズレを観客に体感させる

**残課題**: Day3（4/29）で本番実装着手。machines.yaml 4 機種化、calibration_check.py、dataclass、persona_loader、machine.py、emotion.py まで。

### 2026-04-27 — v4 仕様の歪みを実機経験で矯正

- v4 仕様（ChatGPT Pro 確定）を Phase 1 着手前にレビュー、横塚の実機経験で 5 つの歪みを発見
- 最大の発見: GOD の payout_mean 5500 だと**機械割 22%**で全 run 大負け確定、興奮ピーク観測不能
- 修正案つきで再レビューを ChatGPT Pro に依頼、回答待ちで Day1 終了

### 2026-04-26 — Day0 完了

- 配布コード stock demo を実機検証 → 「配布コードはスキャフォールドにならない」と判明（男女が bar に出入りする話 vs パチの物理ループ）
- ChatGPT Pro v4 相談で「物理実験シミュレーター仕様」確定
- CLAUDE.md を v4 で全書き換え、`pachinko_hall_sim/` スケルトン作成、169 cards から 10 人 stratified sampling

## 次の深掘り課題（提出までに考え抜く）

シミュレーションを「動くもの」にするのは技術問題。**何をシミュレーションして、どう見せるか** は別の問題。
ここは spike では答えが出ない。Day3-Day8 で実装と並行して詰める。

### Q1. 何をシミュレーションするか

| 軸 | 候補 | 検討メモ |
|---|------|---------|
| persona 数 | 10 / 30 / 100 | 動画には 10 で十分。統計には 30。100 は計算時間と引き換え |
| 機種数 | 4 機種 × 1 台 / 4 × 4 / 8 × 2 | 「機種差を見せたい」なら多種類、「人差を見せたい」なら少種類 |
| step 数 | 30 / 50 / 100 | 30 は感情観察、100 は機種差観察。30 で MVP、100 で本番 run |
| 機種を揃えるか | 全員同じ機種 / バラバラ | 同じ機種だと「人が違う」が伝わる、バラバラだと「環境が違う」が伝わる |
| LLM 間引き | 5 / 10 / 20 step | 30 step なら 5、100 step なら 10〜20 |

### Q2. どう見せるか

| 問い | 選択肢 | 仮の方針 |
|-----|-------|---------|
| 主役選定基準 | 極値（最熱狂/絶望/解離）/ 4 象限代表 / ズレ最大 | **極値（spike_hybrid 方式）から開始**、Day7 で見直し |
| 物語 vs 統計 | 個別 persona の心情ドラマ / カテゴリ別統計 | **物語 7：統計 3** で動画を組む |
| 演出の派手さ | フラッシュ・吹き出し全開 / 落ち着いた科学実験感 | **真ん中**。ヒットフラッシュは入れる、過剰な装飾はしない |
| LLM の見せ方 | 行動決定だけ / 心の声で前面に | **心の声を主軸**に置く。これが企画の差別化 |
| 機種差を伝えるか | 4 機種並列で比較 / 1 機種に集中 | Day8 の比較実験で **1 機種集中の run** と **機種比較の run** の 2 本を作って選ぶ |

### Q3. 心の声をどう人間の感情に近づけるか

現在の擬似版（5-7 種類のテンプレ辞書）の限界：
- カテゴリ間で同じセリフ（依存症末期も主婦も同じ「もう光るしかない」）
- 機種への言及がない（GOD でも沖スロでも同じセリフ）
- step が進んでも語彙が変わらない（最初の絶望と最後の絶望が同じ）

本番（LLM 版）で実現したいこと:
- **persona 属性の語彙差**: 依存症末期は「もう、止められない」、主婦は「子どもの帰りに間に合わない」、不労所得は「まあ、遊びだから」
- **機種への言及**: GOD は「光れ、光れ」、ART は「終わりが見えない」、沖スロは「あと 1 回だけ」
- **時間進行の語彙差**: 序盤は楽観、中盤は迷い、終盤は諦めか執着か
- **メタ認知の有無**: 「冷静に考えてるはずなのに、手が止まらない」みたいな自己観察

prompt 設計の指針（Day4 で実装）:
- temperature 0.5〜0.7
- recent voices を prompt に渡して "違うことを言って" 制約
- カテゴリ別の語彙ヒント（few-shot example を prompt に埋める）
- 印象的な瞬間（cash 0、初当たり、退場、解離ピーク）には強制発話

## 関連ドキュメント

- [**docs/chatgpt-response-v4-1.md**](docs/chatgpt-response-v4-1.md) ★ v4.1 ChatGPT 再レビュー回答（2026-04-28、現行 SSoT）
- [docs/chatgpt-response-v4.md](docs/chatgpt-response-v4.md)（v4 原案）
- [docs/相談プロンプト-v4.md](docs/相談プロンプト-v4.md)
- [docs/chatgpt-response-v3.md](docs/chatgpt-response-v3.md)（旧路線、参考用）
- [docs/multi-path-addiction-model.md](docs/multi-path-addiction-model.md)（14経路モデル原典）
- [reports/R1-R3-aggregation.md](reports/R1-R3-aggregation.md)（persona 統計）
- [子ノート](../../../../../Documents/キャルちゃんリンク/100_Notes/1.2026年/singulabo-hackathon.md)
