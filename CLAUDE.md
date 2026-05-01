# Singulabo Hackathon — プロジェクト仕様書（v4.2 ストレス × 大逆転認知 反映版）

シンギュラボのハッカソン提出用プロジェクト。
v4 → v4.1 → **v4.2** の進化:
- v4 (2026-04-26): ChatGPT Pro 相談で「物理実験シミュレーター」確定
- v4.1 (2026-04-28): 横塚の実機経験で 5 つの歪みを矯正、ChatGPT 再レビュー反映
- **v4.2 (2026-04-29)**: spike 4 本で動画イメージを掴んだ後、横塚が **本当の答え合わせしたいこと** を言語化 → **「ストレス × 大逆転認知 → ドーパミン爆発」** の検証を仕様の主軸に据える

物理は rule-based、LLM は間引いて使う、感情は 3 軸（arousal / despair / dissociation）で観察。
**ハッカソン提出物の中心は「興奮ピーク Top 5 ハイライト集」**。

## 基本情報

| 項目 | 値 |
|------|-----|
| 開始日 | 2026-04-18 |
| 提出締切 | 2026-05-07 17:00 |
| id | `singulabo-hackathon` |
| チーム名 | 鶴子 |
| 作品名 | パチスロ実践！人の心理シミュレーション |
| 方針 | **🔬 仮説検証実験路線**（ストレス × 大逆転認知 → ドーパミン爆発、Top 5 ハイライト集） |
| 仕様の出典 | [docs/chatgpt-response-v4.md](docs/chatgpt-response-v4.md) + [docs/chatgpt-response-v4-1.md](docs/chatgpt-response-v4-1.md) + 横塚の実機経験（v4.2 で言語化） |

## 動機と仮説

### 動機
横塚が15年間ギャンブル依存症だった経験の「答え合わせ」。
パチンコホールに **複数種類×複数台の台** を並べ、ペルソナを配置して、
**最も興奮した瞬間がいつ・誰に・どんな条件で・どんな機種で発生したか** を観察する仮説検証実験。

### 核心仮説（v4.2 主軸）

> **ストレス × 大逆転認知 = ドーパミン爆発**
>
> 借金・仕事・残金減少などで **ストレスが積み上がっている状態**で、
> AT/ART 当選などの **爆発入り口** に入り、
> さらに **上乗せ・特化ゾーン・確定演出** などで **「もう終わらないかもしれない」** という **大逆転認知** が発生する。
> その瞬間、**arousal が局所最大に達し、ストレスが一気に緩和される**。
> 興奮の振れ幅は **stress_load の高さに比例**して大きくなる。

3 段階の感情遷移:
```
[ストレス積み上げ期] borrow_burden + work_stress + 残金減少 + miss_streak
        ↓
[爆発入り口] AT/ART 当選 → でも「駆け抜け予感」でまだ抑制
        ↓
[大逆転認知] 上乗せ / 特化ゾーン / 確定演出 → 「もう終わらない」予感
        ↓
[ドーパミン爆発] arousal が一気に跳ね上がる（Δarousal が局所最大）
        ↓
[ピーク記録] その瞬間の状態をログ → 後処理で Top 5 を抽出
```

### 補助仮説（v4.1 から継続）

- **dissociation（解離）** が arousal/despair 双方を抑制し、依存症末期に「負けても静か」が出現
- **time_pressure × social_commitment_density** が「焦り」「罪悪感」を生み、ART の「帰れない感」を増幅
- **path dependency** が滞在時間と離脱判断を支配
- **持続期待の時間構造**（AT 短 spike vs ART 長 tether）が中毒性の質を変える

### 観察アウトカム（v4.2 主役）

1. **興奮ピーク Top 5** — 全 run の中で Δarousal が最大だった 5 瞬間
   - 各ピークについて: 直前の状態（pre-peak）、ピーク瞬間（peak）、直後の状態（post-peak）
   - 発生条件: persona 属性、機種、stress_load、miss_streak、トリガーイベント
2. **stress_load × Δarousal の相関** — 「ストレスが高いほど爆発が大きい」の検証
3. **トリガーイベント別の爆発統計** — 上乗せ / 特化ゾーン / 確定演出のうちどれが最も大きい爆発を生むか
4. カテゴリ別 arousal / despair / dissociation の時間推移
5. LLM 自己申告（reported_*）と canonical state のズレ
6. 「**同じ機種・同じイベントでも、stress_load によって感情の振れ幅が違う**」の可視化

## 核心メッセージ（企画の一行説明）

> **ストレスが追い詰められた人ほど、大逆転で大きく爆発する。
> その瞬間を 1000 step のシミュレーションから抽出し、Top 5 ハイライトとして可視化する。**

副メッセージ（補強）:

> 同じ機種・同じ上乗せイベントでも、stress_load によって興奮の振れ幅が違う。
> 物理状態（rule canonical）・自己申告（LLM self-report）・心の声（LLM 自由記述）の 3 層がズレる現象も同時に観察する。

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

### 中間イベント（v4.2 追加）

「ストレス × 大逆転認知 → ドーパミン爆発」を表現するため、chain 中に **段階的な期待値上昇イベント** を発生させる。
chain モードの機種（ID 0-2）のみ対象。純A（ID3）は対象外。

| event_id | イベント名 | chain 中の発生確率 | 効果 | trigger_event ログ値 |
|----------|----------|------------------|------|--------------------|
| 0 | （通常継続）| - | base payout のみ | `none` |
| 1 | **上乗せ** | 0.15 / step | expected_chain_tail を +N step（N=50〜200）| `uwanose_{N}g` |
| 2 | **特化ゾーン突入** | 0.04 / step | 一定 step（10〜30）continue_prob=0.95 に上昇 | `tokka_zone_entry` |
| 3 | **確定演出** | 0.01 / step | 上乗せ確定 + 特化ゾーン同時発動 | `kakutei_engi` |

機種別の差別化:

| 機種 | 上乗せ確率倍率 | 特化ゾーン確率倍率 | 確定演出確率倍率 |
|------|--------------|-------------------|----------------|
| GOD（爆裂AT）| 1.5x | 0.5x | 1.5x（出たら超デカい）|
| 4.5号機 | 1.0x（標準）| 1.0x | 1.0x |
| ART（拘束）| 1.2x | 2.0x（特化ゾーンが多い）| 0.5x |
| 純A | 0 | 0 | 0（中間イベント無し）|

### upset_recognition_signal（大逆転認知シグナル）

各 step で算出する「**今の瞬間どれくらい大逆転を認知しているか**」のスカラー（0.0-1.0）。

```python
upset_recognition = clip(
    + 0.40 * chain_just_started      # この step で chain_active=on になった
    + 0.60 * uwanose_event           # この step で上乗せ発生
    + 1.00 * tokka_zone_entry        # この step で特化ゾーン突入
    + 1.20 * kakutei_engi            # この step で確定演出
    + 0.30 * chain_continued_long    # chain が 5 step 以上続いている
, 0.0, 1.0)
```

これが arousal の更新式に **stress_load との積で** 入る（後述の感情モデルセクション参照）。

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

## 追加 persona / session 属性（v4.1 + v4.2）

### persona 固有
- `time_pressure` (0.0〜1.0) — 時間圧の感じやすさ。生活全般での「焦り傾向」
- `target_leave_step` (int) — このセッションで離脱を予定している step
- `base_stress` (0.0〜1.0, **v4.2**) — 持続的なストレス傾向（依存症末期は高、不労所得は低）

### session context（その日の状況、persona 固有ではない）
- `social_commitment_density` (0.0〜1.0) — 約束密度
- `commitment_intensity` (0.0〜1.0) — 同 commitment の重み
- `borrow_burden` (0.0〜1.0, **v4.2**) — 借金圧（消費者金融、リボ、家族・友人からの借金）
- `work_stress` (0.0〜1.0, **v4.2**) — 仕事の不満・嫌なことの累積
- `life_dissatisfaction` (0.0〜1.0, **v4.2**) — 日々の生活への不満

これらを persona trait と混同しない。session_context を別 dict で渡し、experiment 条件として独立に振れるようにする。

### stress_load の合成（v4.2）

session ごとに **stress_load** を合成して感情更新に流す。これが「ストレス × 大逆転認知」の **「ストレス側」**。

```python
# 持続的ストレス（persona 固有）+ その日のストレス（session）
stress_load = clip(
    0.30 * persona.base_stress           # 慢性的ストレス傾向
  + 0.30 * session.borrow_burden         # 借金圧
  + 0.20 * session.work_stress           # 仕事ストレス
  + 0.10 * session.life_dissatisfaction  # 日常不満
  + 0.10 * session.social_commitment_density * session.commitment_intensity
                                         # 約束破り罪悪感
, 0.0, 1.0)
```

実験条件（experiment design）:
- **baseline**: stress_load の分布を自然に
- **high-stress**: borrow_burden=0.8, work_stress=0.8 で固定（追い詰め condition）
- **low-stress**: borrow_burden=0.1, work_stress=0.1 で固定（余裕 condition）

3 条件で同じ persona を回すと、「**同じ人でも、ストレス状態によって爆発の振れ幅が違う**」が直接観察できる。

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

### arousal 更新（v4.2: upset_recognition × stress_load 追加）

```python
# 既存項
raw_delta_arousal = (
    + 22.0 * hit_signal
    + 10.0 * gain_signal
    +  6.0 * cue_signal
    +  4.0 * hammari_signal
    +  5.0 * time_pressure_signal * hammari_signal
    +  5.0 * deadline_conflict
    -  3.0 * cash_low_signal
)

# v4.2 追加: 大逆転認知 × ストレス積（爆発項）
# stress_load が高いほど、上乗せ・特化ゾーン・確定演出への反応が強くなる
explosion_term = 35.0 * upset_recognition * (0.5 + 1.5 * stress_load)
# stress_load=0 で 17.5 倍率、stress_load=1 で 70 倍率まで増幅可能
# upset_recognition=1 のとき、stress_load=0.8 → +59.5 が arousal に乗る

raw_delta_arousal += explosion_term

raw_delta_arousal *= persona.sensory_gating_factor
delta_arousal = suppression * raw_delta_arousal
delta_arousal -= 0.05 * (arousal - base_arousal)  # 自然減衰
arousal = clip(arousal + delta_arousal + noise_arousal, 0.0, 100.0)
```

### despair 更新（v4.2: stress_load 効果を追加）

ストレスが高いほど、損失・残金不足への絶望が強くなる:

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

# v4.2 追加: stress_load が損失系の項を増幅
stress_amplifier = 1.0 + 0.6 * stress_load  # 1.0 〜 1.6 倍
raw_delta_despair *= stress_amplifier

# v4.2 追加: 大逆転認知が起きると despair が一時的に下がる（救済感）
raw_delta_despair -= 8.0 * upset_recognition * stress_load

raw_delta_despair *= (0.7 + base_despair / 100.0)
raw_delta_despair += 4.0 * persona.time_cost_efficiency * hammari_signal
delta_despair = suppression * raw_delta_despair
delta_despair -= 0.03 * (despair - base_despair)
despair = clip(despair + delta_despair + noise_despair, 0.0, 100.0)
```

### v4.2 の物理的意味

- **stress_load=0.0 の人**: 大逆転認知が起きても arousal は +17.5 程度しか上がらない（淡々と勝つ）
- **stress_load=0.9 の人**: 同じ大逆転認知で arousal +66 まで跳ね上がる（爆発体験）
- **stress_load 高 + 確定演出**: upset_recognition=1.2 まで届くので、Δarousal が +80 を超える瞬間が出現

これが「**追い詰められた人ほど、大逆転で大きく爆発する**」の数式表現。

### 哲学的含意

- **stress_load × upset_recognition の積**が **Δarousal の局所最大** を生む（v4.2 主軸）
- dissociation が高い persona は hit/loss/guilt への反応が鈍る → 「**負けているのに静か**」「**焦っているのに観察モード**」「**悟りっぽい**」が出る
- dissociation 自体は損失・ハマり・拘束・罪悪感で上がる
- guilt は独立軸にせず despair / dissociation の signal として流す（軸を増やしすぎない）
- raw_delta も suppressed delta も両方ログに残す（観察と解釈のため）
- **Δarousal が ±N を超えた step は trigger_event とともにログ → 後処理で Top 5 抽出**

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

## ログ schema（1 step 1 row, v4.2）

```json
{
  "run_id": "mvp_seed_42",
  "step": 17,
  "persona_id": "R3_012",
  "category": "依存症末期",
  "machine_id": "GOD_01",
  "machine_type_id": 0,

  "action": 0,
  "action_source": "rule",

  "hit": true, "payout": 35000, "stake": 1000, "net_delta": 34000,
  "chain_active": true, "chain_step_count": 4,
  "cash": 41000, "accessible_cash": 80000, "cash_refilled_this_step": false,

  "trigger_event": "uwanose_150g",  // v4.2: 中間イベント名 (none/uwanose_*g/tokka_zone_entry/kakutei_engi)
  "uwanose_amount": 150,            // v4.2: 上乗せがあった場合の量
  "expected_chain_tail_remaining": 180,  // 期待残連荘 step 数

  "arousal": 96.4, "despair": 32.5, "dissociation_level": 28.1,
  "arousal_delta": +64.2,           // v4.2: 前 step との差分（ピーク検出用）
  "despair_delta": -28.0,           // v4.2: 同上
  "raw_delta_arousal": 75.5, "raw_delta_despair": -38.2, "raw_delta_dissociation": -3.4,
  "suppression": 0.85,

  "stress_load": 0.78,              // v4.2: 合成済みストレス
  "upset_recognition": 0.85,         // v4.2: 大逆転認知シグナル
  "explosion_term": 53.4,            // v4.2: arousal に乗った爆発項

  "llm_reported_arousal": 91, "llm_reported_despair": 35, "llm_reported_dissociation": 30,
  "llm_inner_voice": "もう、終わらない、終わらないかも",  // v4.2: 心の声テキスト

  "miss_streak": 0, "win_streak": 4,
  "cue_memory": 0.91, "time_in_hall": 17,
  "guilt_signal": 0.42, "deadline_conflict": 0.31, "time_pressure_signal": 0.34,
  "interruptibility": 0.22, "sensory_gating_factor": 0.91,
  "stigma_barrier": 0.74, "payday_sensitivity": 0.63,
  "time_cost_efficiency": 0.41, "path_dependency_score": 0.95,
  "addiction_load": 0.82,
  "time_pressure": 0.65, "target_leave_step": 50,
  "social_commitment_density": 0.40,

  "session_borrow_burden": 0.80,    // v4.2: session context をログに含める
  "session_work_stress": 0.70,
  "session_life_dissatisfaction": 0.60,
  "persona_base_stress": 0.65
}
```

**ログ設計の原則 (v4.2)**:
- `raw_delta_*` と suppression 後の delta を両方残す
- `guilt_signal` / `deadline_conflict` / `time_pressure_signal` などの中間 signal もログ
- **`arousal_delta` を必ず記録**（ピーク検出の主キー）
- **`trigger_event` を必ず記録**（後処理で爆発の原因を分析）
- **`stress_load` と `upset_recognition` をログに残す**（仮説検証の主軸）
- **`llm_inner_voice` テキストもログ**（動画字幕に使う）

## ピーク検出（v4.2 新規）

シミュレーション完走後、ログを走査して **興奮ピーク Top 5** を抽出する。

### 抽出ロジック

```python
def extract_top5_peaks(log_df, threshold=30.0, top_n=5):
    """
    arousal_delta が threshold 以上の step から Top 5 を選ぶ。
    各 persona から複数選ばれてもよいが、同一 persona の連続 step（前後 3 step）は dedup する。
    """
    candidates = log_df[log_df["arousal_delta"] >= threshold].copy()
    candidates = candidates.sort_values("arousal_delta", ascending=False)

    selected = []
    for _, row in candidates.iterrows():
        if len(selected) >= top_n:
            break
        # 同一 persona・近接 step の重複を排除
        is_duplicate = any(
            s["persona_id"] == row["persona_id"]
            and abs(s["step"] - row["step"]) <= 3
            for s in selected
        )
        if not is_duplicate:
            selected.append(row.to_dict())
    return selected
```

### 各ピークに付随するコンテキスト

```python
def build_peak_context(peak, log_df, window=5):
    pid = peak["persona_id"]
    step = peak["step"]
    pre = log_df[(log_df.persona_id == pid) & (log_df.step.between(step-window, step-1))]
    post = log_df[(log_df.persona_id == pid) & (log_df.step.between(step+1, step+window))]
    return {
        "peak": peak,
        "pre_window": pre.to_dict("records"),
        "post_window": post.to_dict("records"),
        "context": {
            "persona_id": pid,
            "category": peak["category"],
            "machine": peak["machine_id"],
            "stress_load": peak["stress_load"],
            "trigger_event": peak["trigger_event"],
            "arousal_before": pre.iloc[-1]["arousal"] if len(pre) > 0 else None,
            "arousal_at_peak": peak["arousal"],
            "delta": peak["arousal_delta"],
        }
    }
```

### 期待される Top 5 の例

| # | persona | カテゴリ | stress_load | machine | trigger | Δarousal |
|---|---------|---------|------------|---------|---------|----------|
| 1 | p01 | 依存症末期 | 0.92 | GOD | kakutei_engi | +78 |
| 2 | p07 | 中年現役 | 0.85 | ART | tokka_zone_entry | +71 |
| 3 | p01 | 依存症末期 | 0.85 | GOD | uwanose_200g | +64 |
| 4 | p12 | 主婦 | 0.55 | 4.5号機 | uwanose_150g | +52 |
| 5 | p05 | 不労所得 | 0.15 | GOD | kakutei_engi | +38 |

→ **stress_load の高い人ほど Δarousal が大きい** が一目で分かる表になる。

## 可視化仕様（6種, v4.1）

1. **属性別 arousal 推移**: x=step, y=mean arousal, group=category or quadrant
2. **属性別 despair 推移**: 同上、despair
3. **属性別 dissociation 推移**: 同上、dissociation_level（v4.1 追加）
4. **最終状態 3軸 scatter**: x=final arousal, y=final despair, **z=final dissociation（または点サイズ/色強度で表現）**, color=category, size=total_spent
5. **個別 persona timeline**: x=step, y1=cash, y2=arousal, y3=despair, **y4=dissociation_level**, marker=hit/leave/cash_zero/cash_refill
6. **ホール俯瞰動画**: machines=grid 上の固定点、persona=machine 上に表示、marker size=arousal、**marker alpha=1-suppression（解離してる人は薄く描く）**、frame=step（matplotlib animation）

## 動画演出方針（v4.2: Top 5 ハイライト + ハイブリッド）

提出動画の **主役は「興奮ピーク Top 5」**。ハイブリッド方式（3 主役スポットライト）は導入部で物語の文脈を作る役。

### 動画の構成（2 分目安, v4.2）

```
[0:00-0:15] タイトル + 仮説提示
            「鶴子 / パチスロ実践！人の心理シミュレーション」
            字幕: 「ストレス × 大逆転認知 → ドーパミン爆発、検証します」

[0:15-0:30] 仕組みを 15 秒で説明
            ・ホール、機種 4 種、persona N 人、stress_load の概念
            ・図 1 枚（v4.2 の核心仮説図、3 段階遷移）

[0:30-1:10] 1 つの典型例（爆発までの物語）40 秒
            ・「依存症末期、stress_load 0.85、GOD で 1.5 万溶かして……」
            ・step 進行を 4 倍速で
            ・爆発瞬間の 5 秒だけ **0.3 倍速スローモーション**
              「step 27、ボーナス当選 → 上乗せ +200G → arousal 32→96」
            ・心の声を吹き出しで「もう光るしかない」→「終わらない！？」

[1:10-1:50] 興奮ピーク Top 5 ハイライト集 40 秒
            ・各ピーク 8 秒
            ・各場面の表示要素:
              - persona ID + カテゴリ
              - stress_load の値（バー）
              - 機種名 + trigger_event
              - Δarousal の数値（フロート文字で派手に）
              - 心の声（テキスト or LLM 生成）
              - 5 step 前後のグラフ（mini sparkline）
            ・順番は #5 → #1 で盛り上がる構成

[1:50-2:10] stress_load × Δarousal の散布図（仮説の検証）
            ・全爆発 step を点で配置
            ・回帰直線を引く
            ・字幕: 「stress が高いほど、爆発は大きい」
            ・3 層のズレ（canonical / self-report / inner voice）も簡潔に触れる

[2:10-2:30] まとめ + 限界
            ・「物理 ≠ 自己申告 ≠ 心の声 の 3 層ズレも観察」
            ・限界: 抽象モデル、N 限定、LLM 自己申告の安定性課題
            ・クレジット
```

### Top 5 ハイライト各場面のレイアウト

```
┌────────────────────────────────────────────────────┐
│  HIGHLIGHT #N                          Δarousal +XX │
├────────────────────────────────────────────────────┤
│                                                     │
│  [persona dot, 大きく中央]                          │
│   p01 依存症末期                                    │
│                                                     │
│  stress_load: ████████░░ 0.85                      │
│  機種: GOD  /  trigger: uwanose_200g                │
│                                                     │
│  💭「もう、終わらない、終わらないかも」               │
│                                                     │
│  arousal:  ━━━━━━━━━━━━━━━━━ (sparkline)          │
│            32 ──────→ 96  (5 step in)              │
│  despair:  ━━━━━━━━━━━━━━━━━                       │
│            68 ──────→ 40                            │
│                                                     │
└────────────────────────────────────────────────────┘
```

### ハイブリッド方式（導入部で活用）

「1 つの典型例」セクション（0:30-1:10）でハイブリッド方式を使う:

| 役 | 選定基準 |
|---|---------|
| 🔥 最熱狂 | 全期間で arousal ピーク最大 |
| 💀 最絶望 | 全期間で despair ピーク最大 |
| 🧊 最解離 | 全期間で despair − arousal ギャップ最大 |

導入で 3 主役を見せて「**こういう人がいるホール**」を観客に印象づけ、本編 Top 5 で「**爆発の瞬間**」を見せる二段構え。

### Top 5 各場面の表示要素（共通）

- **dot**: サイズ = arousal、縁色 = despair（gray→purple→crimson）
- **stress_load メーター**: 大きい横バー（爆発の前提条件として強調）
- **trigger_event**: 「上乗せ +200G」「特化ゾーン突入」「確定演出！」を派手な字幕で
- **Δarousal**: 「+64」みたいな数字をフロート文字で大きく
- **心の声**: 吹き出し（pre-peak / at-peak / post-peak の 3 句で変化）
- **mini sparkline**: ピーク前後 5 step の arousal / despair の推移

### 心の声の生成（Phase 別）

| Phase | 実装 | 状態 |
|-------|------|------|
| spike v1-v2 | 状態カテゴリ別の固定セリフ辞書、ランダム選択 | 5-7 種類のステレオタイプ |
| **本番（Day4-7）**| **LLM（qwen3:4b）で persona 属性 + 数値状態 + 機種 + trigger_event から動的生成** | 自然な口語、persona 個性、trigger イベントへの言及 |

### 心の声 LLM prompt 設計（本番実装の要件, v4.2）

```
あなたは {category}（{age}歳、{gender}）。
今、{machine_name} の前で {step} 回目の遊技。
残金 {cash}円、miss_streak {miss_streak}、
興奮度 {arousal:.0f}/100、絶望度 {despair:.0f}/100、解離度 {dissociation:.0f}/100。

ストレス状態:
- 借金圧 {borrow_burden:.1f}/1.0
- 仕事ストレス {work_stress:.1f}/1.0

直前のイベント: {trigger_event}  // none / uwanose_200g / tokka_zone_entry / kakutei_engi
最近の変化: arousal が {arousal_delta:+.0f} 動いた

今の気持ちを **30 字以内、一人称、句点なし** で書いてください。
人名・地名・固有名詞は禁止。
直前のイベントへの反応を意識してください。
```

要件：
- temperature 0.5〜0.7 で多様性確保
- recent voices を prompt に渡して "違うことを言って" 制約
- ピーク瞬間（Δarousal > 30）には**強制発話**（必ず生成）
- 通常時は 5 step ごとで OK

### 何を見せたいかの哲学（v4.2）

- **「ストレスが追い詰められた人ほど、大逆転で大きく爆発する」を体感させる**
- 「同じ機種・同じイベントでも、stress_load によって振れ幅が違う」を散布図で見せる
- 「物理 ≠ 自己申告 ≠ 心の声」の 3 層ズレを副軸で観察
- 観客は審査員（データサイエンティストではない）。**グラフ < 物語 + 数字の派手な動き + 心の声**
- **「ただ動いてるだけ」を避ける**ため、各ピークに字幕で「何が起きてるか」を言語化する

## マイルストーン（Day0-11, v4.1 ChatGPT 案）

Day1（4/27）は v4.1 仕様確定で消費されたため、Day1 と Day2 を 4/28 にまとめる。

| Day | 日付 | 目標 | 順調判定 |
|-----|------|------|---------|
| Day0 | 4/26 | v4 仕様凍結、スケルトン作成、persona JSONL 生成 | CLAUDE.md / pachinko_hall_sim/ / data/persona_cards.jsonl 揃う |
| Day1 | 4/27 | v4 → v4.1 仕様レビュー | ChatGPT v4.1 回答受領、CLAUDE.md v4.1 反映 |
| Day2 | 4/28 | CLAUDE.md v4.1 反映 + spike 4 本で動画イメージ確定 | spike_god / spike_hall_live / spike_hall_live_v2 / spike_hybrid 完成 |
| **Day3** | **4/29** | **v4.2 仕様化（experiment ブランチ）+ 本番実装着手** | **CLAUDE.md v4.2、中間イベント・stress_load・upset_recognition 仕様確定。machines.yaml 4機種化、calibration_check、dataclass、persona_loader、machine.py、emotion.py まで** |
| Day4 | 4/30 | rule-only simulation 完走 + LLM wrapper + 心の声 prompt 設計 | 10 persona × 30 step × 4機種 + 中間イベント + stress_load 実装、log.jsonl が出る。qwen3:4b が JSON で action と心の声を返す |
| Day5 | 5/1 | **案A MVP + ピーク検出 + ハイブリッド可視化** | 10 persona × 30 step、log、3 軸グラフ、Top 5 ピーク抽出スクリプト、ハイブリッド可視化 MP4 |
| Day6 | 5/2 | 案B 30 persona × 100 step rule-only + 心の声 LLM 統合 | 30×100 が安定。心の声が persona 属性ごとに違う表現で出る。Top 5 抽出が安定する |
| Day7 | 5/3 | **Top 5 ハイライト動画化 + stress_load 散布図** | 各ピークの 8 秒動画クリップが生成される。stress_load × Δarousal 散布図（仮説検証）が完成 |
| Day8 | 5/4 | 比較実験（high-stress / low-stress / baseline）+ 提出 run 固定 | 3 条件を回して、Top 5 が「stress_load 高で爆発が大きい」を示すことを確認。提出に使う run を選ぶ |
| Day9 | 5/5 | 解説文章 + 動画タイトル/字幕 | 「ストレス × 大逆転認知 → ドーパミン爆発」の検証結果を 4-6 ページに圧縮 |
| Day10 | 5/6 | パッケージング | README、実行コマンド、出力例、動画ファイル名規則、PDF 化、GitHub 整備、experiment ブランチを main に merge |
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

### 2026-05-01 — v4.3 schema 固定 + 動画パイプライン MVP + 要件確認

**やったこと**:

1. **ChatGPT Pro v4.3 レビュー受領** — `docs/chatgpt-response-v4-2.md`
   - 結論: C 推し（v4.3 で再検証、仮説差し替えはせず観察結果を強化）
   - 設計の核: 「当たりの物理 / イベントの意味 / 動画ハイライト」を分離
   - 最低限詰める変数 5 個: stress_load 動的化 / bonus_excitement_multiplier / light/heavy 二相 / raw_top5 と stratified 分離 / LLM voice 統合

2. **spike_v43.py 作成** — schema 固定 Step 1（715 行、experiment ブランチ）
   - 4 機種リブランド: **PURE_A / ART_45 / ART_2010 / GOD_OKI**
   - MachineType に追加: `bonus_excitement_multiplier` / `chain_start_impact` / `continuation_excitement_multiplier` / `event_probs` / `event_impacts`
   - `sensory_gating` → `sensory_amplitude` リネーム + `dopamine_sensitivity` 派生
   - trigger_event 拡張: `uwanose_light/heavy` / `tokka_light/heavy` / `kakutei_engi`
   - `update_emotions` を「身体反応 + dopamine_burst（event_impact 駆動）」に分離

3. **Codex レビュー → 5 件指摘を全部修正**
   - event_probs 母集団を「hit 成功 step あたり実効確率」と明文化（calibration で実測値出す方針）
   - **PURE_A から kakutei_engi 完全削除**（横塚判断: 純Aプレミア告知は興奮の爆発を伴わない）
   - `chain_start_impact` を `__post_init__` で `event_impacts["chain_start"]` に自動同期（二重 SSoT 解消）
   - sensory_amplitude を B-lite 適用: 背景項に `background_amplitude = 0.85 + 0.30 * sensory_amplitude`、爆発項には `dopamine_sensitivity` のみ（二重倍率解消）
   - upset_recognition 互換キーを `min(1.0, event_impact)` で clamp（可視化破綻防止）

4. **動作確認**（8 persona × 50 step、seed=42）
   - 完走 OK、arousal クリップなし、Top 5 抽出 OK
   - 散布図 stress_load × Δarousal で **正の傾向**（回帰 y = 29.9x + 19.0）
   - 観察: #2 p05 が stress=0.08 で Δ=39.5（v4.2 と同様、stress 単独では支配しない）

5. **環境セットアップ** — Mac
   - `brew install python@3.12` + `brew install ffmpeg`
   - venv は `~/.venv-singulabo`（**コロン付きパスでは venv 作れない gotcha**、ホームに作る）
   - 毎回 `source ~/.venv-singulabo/bin/activate` 必要

6. **spike_llm_voice.py 動作確認**
   - qwen3:4b-instruct-2507-q4_K_M、6 ケース 0.3 秒/call、本番 600 call ≈ 3 分
   - 表現課題: 「また」連発（4/6）、当たり/上乗せ系（1〜3）の興奮表現薄い、絶望/強気系（4〜6）はそこそこ

7. **spike_v43_video_mvp.py 作成 + 動画書き出し成功** — 130 行
   - matplotlib FuncAnimation + ffmpeg で `outputs/spike_v43_mvp.mp4` 書き出し
   - 8 persona × 50 step、5 fps、10 秒のホール俯瞰動画
   - **動画パイプライン成立確認**（字幕・心の声は未統合、Phase 0.1〜4-C も未統合）

8. **ハッカソン要項を認識** — 横塚から再共有（3-4 回目反省）
   - 提出物: **ソースコード（GitHub 理想）+ 可視化動画 + 簡単な解説文章**
   - 動画長: **1〜2 分**（横塚判断、最長 2 分）
   - 配布コード（2d-multi-places-simulation-on-fire-public）「**改造または拡張**」要件 → 新規実装の場合は解説文章で位置づけ必要
   - 提出ファイル名: `鶴子パチスロ実践！人の心理シミュレーション{デモ動画.mp4|説明資料.pdf}`

**学び**:
- 動作確認なしの実装は危険。**Codex レビュー → 修正 → 動作確認** の順序が肝
- 動画パイプラインは matplotlib FuncAnimation + ffmpeg で機能する。spike_v42_n32_v2.py の Phase 描画資産が活きる
- LLM voice の表現改良は別工程（few-shot、禁止語、用語ヒント、temperature 上げ）
- 配布コードと新規実装の位置づけは**解説文章で言語化**必要、これがないと「配布コード使ってない」判定リスク
- パスにコロンが含まれると python venv 作れない（gotcha 案件、horse へ伝達済み）

**致命リスク（残）**:
- 🔴 GitHub 未 push（private 想定、5 分作業）
- 🔴 解説文章で「配布コード拡張」位置づけ未記述（30 分作業）

**次セッションの最初の判断**:

横塚に **A / B / C のどれで Step を進めるか** 確認する。動画 MVP は立ったから、**残り工数 5〜6 日で 1〜2 分の動画提出版を作る**のがゴール。

| 選択肢 | 内容 | 工数 |
|--------|------|------|
| A. Step 3 順序通り | light/heavy 物理影響（chain_stock 加算）→ stress 動的化 → calibration | 1.5 日 |
| B. Step 7 ジャンプ | LLM voice 統合（spike_v43 のハイライトに qwen3:4b で心の声埋め込み） | 半日 |
| C. Step 9 先行 | 動画本番化（Phase 0.1〜4-C を全部繋いで 1 分動画作る、内容は v4.3 現状ベース） | 1〜2 日 |

俺の推し: **B → C → A** の順。LLM voice 統合で動画イメージを早く立てて、本番動画化、最後に物理 / stress / calibration の調整、という流れ。

**環境メモ**:
- venv: `~/.venv-singulabo`（python3.12 brew、コロン付きパス NG）
- ターミナル開くたび: `source ~/.venv-singulabo/bin/activate`
- ollama: localhost:11434 起動中、qwen3:4b-instruct-2507-q4_K_M 利用可
- ffmpeg: brew install 済
- 動画 MVP: `pachinko_hall_sim/outputs/spike_v43_mvp.mp4`

### 2026-04-29（Day3）— v4.2 仕様化 + spike 5 本実装 + LLM 動作確認

**やったこと**:

1. **v4.2 仕様化** — CLAUDE.md 全面書き換え（experiment ブランチ）
   - 核心仮説を「ストレス × 大逆転認知 → ドーパミン爆発」に格上げ
   - 中間イベント（上乗せ・特化ゾーン・確定演出）追加
   - session context に stress_load 追加
   - 感情モデルに upset_recognition × stress_load の爆発項追加
   - ログ schema に arousal_delta / trigger_event / stress_load / inner_voice 追加
   - ピーク検出セクション新設（Top 5 抽出）
   - 動画演出を Top 5 ハイライト中心に書き換え

2. **spike 5 本実装** — `pachinko_hall_sim/spike/` 配下
   - `spike_v42.py` — 8 persona × 50 step、中間イベント + stress_load + 爆発項 + Top 5
   - `spike_v42_n32.py` — 32 persona × 100 step に拡大
   - `spike_v42_n32_v2.py` — 観客向け改善版
     - 用語日本語化（**「興奮度」→「脳汁度」**、「stress_load」→「追い詰められ度」）
     - Phase 0.1 仮説提示パネル
     - Phase 4 を「結論」から「**答え合わせ**」（3 セクション）に書き換え
       - 4-A: 仮説の合否（高群 ÷ 低群、勝ち / 失敗判定）
       - 4-B: 観察された傾向（trigger 別 / カテゴリ別 / 感覚鋭敏度別）
       - 4-C: 実際の答え + 次の仮説
   - `inner_voice_v2.py` — 機種 × トリガー × カテゴリの心の声辞書
   - `spike_llm_voice.py` — **qwen3:4b で本物の LLM 心の声生成、動作確認 OK**

3. **仮説検証実行** — 32 persona × 100 step の結果
   - **仮説（ストレス × 大逆転認知）は外れた**（高群 ÷ 低群が 1.3 倍に届かず）
   - 観察された傾向:
     - **Top 5 全員が「ボーナス当選」の瞬間**（中間イベントより入り口支配）
     - **追い詰められ度 0.16 の女子大生でも +30.2**（追い詰められ度単独では効かない）
     - 女子大生・夜職女性・退職前男性が上位（**感覚鋭敏度の影響示唆**）
   - 次の仮説候補: **「感覚の鋭敏さ × 入り口イベント」**

4. **LLM 動作確認** — ollama + qwen3:4b
   - サーバー応答 OK、qwen3:4b-instruct-2507-q4_K_M 利用可能
   - 1 call 0.3-1.8 秒（爆速）、本番 600 call なら **約 5 分**
   - **品質課題**: prompt が弱いと「また」連発・カテゴリ差なし・パチスロ用語ゼロ
   - prompt 改良の方向性: few-shot example、禁止語、用語ヒント、temperature 上げ

**学び**:
- 「動かす」と「答え合わせの言語化」が連動する。spike を見せた結果、横塚が**本当の動機**を言語化できた
- **仮説が外れても、観察された傾向こそが「答え合わせ」の本体**。失敗を肯定するパネル設計が動画の説得力を生む
- 動画は「動いてるだけ」では退屈。**ピーク瞬間にスポットライト + 何が起きたかを字幕で言語化**が必須
- 用語の日本語化は超重要（「arousal」→「脳汁度」で観客に刺さる）
- LLM は **動かすこと** より **prompt 設計** が肝。雑に呼ぶと無個性なセリフしか出ない
- **観客視点（横塚の感覚）を持って画面を組まないと、専門家向けデータ可視化に陥る**

**残課題（Day4 以降）**:
- 「画面の見せ方を固める」Step 1-4（次の深掘り課題セクション参照）
- LLM prompt の改良（few-shot、用語ヒント、recent voices avoid）
- 心の声を simulator に統合（spike_v42_n32_v2 の Phase 2 ハイライトに LLM voice を埋める）
- 提出版の動画化（matplotlib FuncAnimation → MP4 via ffmpeg）
- machines.yaml / models.py / persona_loader.py 等の production 実装（spike を解体して整える）

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

横塚の方針: **「外側 → 内側」**。画面の見せ方を固めてから、前提条件（仮説・パラメータ・感情モデル）の細部を詰める。

### 【最優先】画面の見せ方を固める Step 1-4

| Step | やること | 状態 |
|------|---------|------|
| **1. 全体フローレビュー** | Phase 構成（0.1 → 1 → 2 → 3 → 4-A,B,C）の順序・過不足・流れを確認 | ⏳ 次セッション |
| **2. 各 Phase の要素レビュー** | 各画面で見せるもの / 消すものを整理 | ⏳ |
| **3. 用語・字幕の最終調整** | 専門用語の翻訳、字幕の追加、テンポ調整 | ⏳ |
| **4. 動画化（MP4 生成）** | ffmpeg で MP4 出力、タイトル / 字幕 / クリップ尺の調整 | ⏳ |

### 現状の動画フロー（spike_v42_n32_v2.py）

```
Phase 0.1  仮説提示                        7秒
Phase 1   ライブシミュレーション             5秒
Phase 2   Top 5 ハイライト（ナレーション風）  各5.5秒 × 5 = 27秒
Phase 3   3 群バーチャート + 散布図          8秒
Phase 4-A 仮説の合否                       7秒
Phase 4-B 観察された傾向（3 パネル）         10秒
Phase 4-C 実際の答え + 次の仮説              残る
```

合計 約 64 秒。**1〜3 分の動画想定にはちょうど良い**。

### Step 1 のレビュー観点（次セッションで議論）

- **Phase 1 ライブは要る？**（散漫に見えるなら削れる）
- **Top 5 は 5 つで適正？**（多い / 少ない）
- **Phase 3 の散布図と 3 群バーチャート、両方要る？**
- 順序は良いか？（仮説 → 物語 → 検証 → 答え合わせ）

### Step 2 の改善候補

- ヒット時のフラッシュ演出（Phase 2 ハイライトを動画映えさせる）
- スローモーション（爆発瞬間だけ 0.3 倍速）
- 数字のフロート文字（Δ脳汁 +64 みたいな派手な表示）
- 機種ごとの「光り方」差別化

### Step 3 の改善候補

- 字幕ナレーション（「彼は今、追い詰められている」みたいな解釈）
- 章立て（「第1章: ホール入店」）
- パチスロ用語の解説テロップ（観客向け）

### Step 4 の手順

1. matplotlib FuncAnimation で各 Phase を MP4 化
2. ffmpeg で結合
3. タイトル / 字幕 / 終わりクレジットを画像レイヤーで追加
4. ファイル名規則準拠で出力（`鶴子パチスロ実践！人の心理シミュレーションデモ動画.mp4`）

### 【中優先】LLM prompt の改良

`spike_llm_voice.py` で動作確認済み。現状の課題:
- 「また」連発、カテゴリ差なし、パチスロ用語ゼロ

改良方針:
- **Few-shot example**（カテゴリ別の良いセリフを 3-5 個 prompt に埋める）
- **禁止語指定**（「『また』禁止」「『〜だな』禁止」など）
- **パチスロ用語ヒント**（「枠連」「終わらない」「凱旋」「無想転生」「ペカった」等を例示）
- **temperature 0.8〜0.9 + top_p 0.95**
- **recent voices 制約強化**（直近 5 件と全部違う表現）
- **イベント別の prompt 分岐**（GOD と ART で違う prompt）

### 【中優先】心の声を simulator に統合

`spike_v42_n32_v2.py` の Phase 2 ハイライト（5 つ）に、テンプレ辞書ではなく **LLM voice を埋め込む** spike を作る。
所要時間: 30 分〜1 時間。動画として見栄えが大幅向上する。

### 【低優先】production code への解体

spike を spike のままじゃなく、`pachinko_hall_sim/src/` の production 構成に解体:
- `models.py` (dataclass)
- `persona_loader.py`
- `machine.py` (中間イベント込み抽選)
- `emotion.py` (v4.2 式)
- `simulator.py` (メインループ)
- `policy_llm.py` (LLM 行動決定)
- `inner_voice.py` (LLM 心の声生成)
- `peak_detector.py` (Top 5 抽出)
- `visualize.py` (Phase 1〜4)
- `run_simulation.py` (CLI)

ハッカソン提出には **必須ではない**（spike のままでも提出はできる）が、GitHub 公開時の見栄えが上がる。Day10 の余裕で対応。

### 【低優先】仮説の改訂

現状の v4.2 仮説（ストレス × 大逆転認知）は spike で外れた。次の仮説候補:
- **感覚の鋭敏さ × 入り口イベント**
- これを v4.3 として詰めるか、v4.2 のまま「観察された傾向」で押すか
- **ハッカソン的には「v4.2 で仮説検証 → 失敗 → 観察された傾向を答え合わせ」がストーリーとして強い**ので、v4.2 のまま維持して動画で示すのが現実的

### Day4 以降の優先順位

```
Day4 (4/30): 画面の見せ方 Step 1-2 + LLM prompt 改良 + 心の声を Phase 2 に統合
Day5 (5/1):  画面の見せ方 Step 3-4 + MP4 化 + 字幕タイトル
Day6 (5/2):  ハイライト動画の精度向上、提出 run の固定
Day7 (5/3):  説明資料 PDF の執筆開始
Day8-10:     仕様の精度詰め（前提条件レビュー）+ パッケージング
Day11 (5/7): 提出
```

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
