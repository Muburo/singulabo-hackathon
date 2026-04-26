# ChatGPT Pro 回答 v4（仕様確定、2026-04-26）

v4 プロンプトへの回答。「締切までに動く実験」と「研究として欲張る実験」を分け、配布コードを捨てて新規の小さなシミュレーターとして設計する方針。

---

## 結論（一行）

> **物理・抽選・感情遷移の本体は rule-based で安定させる。LLM は "毎 step の神" にせず、行動決定と自己申告を間引いて使う。まず 10 persona × 30 step を Day5 までに完走させ、その後 30 persona × 50 step に拡張する。**

---

## 1. Q1-Q7 への直接回答

### Q1. 11日で実装可能な仕様にするには、どこを削るべきか

**削るべきもの（優先順）**:

| 削る対象 | 理由 | 代替 |
|---------|------|------|
| 100 persona × 100 step × 毎 step LLM | LLM call 数が爆発する | 30 persona × 50 step、LLM は 5 step ごと or イベント時 |
| 実機レベルの正確なパチスロ仕様 | 仕様調査と実装が重い | 「当たり・連荘・ハマり・純増」を抽象化した物理モデル |
| 14経路中毒モデルの全動的実装 | 11日では複雑すぎる | 14経路を `addiction_load` などの合成スカラーに圧縮 |
| 隣人会話・社会的相互作用 | 実験軸が増えすぎる | 独白や短文生成は post-process にする |
| LLM に感情状態を完全支配させる | JSON 崩れ・発散・再現性低下 | rule-based 感情を canonical state、LLM は self-report として別記録 |
| 30b / 35b モデルを主軸にする | 遅い、デバッグが重い | qwen3:4b を本線、重いモデルは最終デモ用に数件だけ |

**残すべきもの**:

| 残すもの | 理由 |
|---------|------|
| 台の抽選物理 | 企画の核 |
| persona の残金・arousal・despair・滞在時間 | 観察対象そのもの |
| 機種差：AT / Hokuto / ART | 実験としての比較軸 |
| 169 cards からの sampling | DR の蓄積を活かせる |
| JSONL / CSV log | 後で可視化・分析・説明文に使える |
| 最低限の LLM 行動決定 | 配布コード継承の「numeric state から意思決定」要素 |

### Q2. 台の物理の最小モデル

**最小限必要なパラメータは 6 個**:

| パラメータ | 意味 | 必須度 |
|----------|------|-------|
| `p_initial_hit` | 通常時に当たる確率 | 必須 |
| `continue_prob` | 当たり後に連荘する確率 | 必須 |
| `stake_per_step` | 1 step あたり投資額 | 必須 |
| `payout_mean` | 当たり時の平均払戻 | 必須 |
| `payout_std` | 払戻のばらつき | 準必須 |
| `cue_decay_steps` | 当たり・演出記憶が何 step 残るか | 必須 |

- 「ハマり」は `miss_streak` を数えれば自然に出る
- 「連荘」は `continue_prob` だけで十分
- 「純増」は `net_money_delta = payout - stake` でよい
- 提出物では「実機再現ではなく、依存・感情・台特性を観察する**抽象物理モデル**」と説明すれば成立

**3機種の仮パラメータ例**:

| 機種 | p_initial_hit | continue_prob | stake_per_step | payout_mean | payout_std | cue_decay_steps | 狙い |
|------|--------------|---------------|---------------|-------------|------------|-----------------|------|
| AT 爆裂 | 0.08 | 0.35 | 1000 | 3500 | 1600 | 1 | 短期で大きく振れる |
| Hokuto | 0.07 | 0.58 | 1000 | 2500 | 1000 | 2 | 中間的 |
| ART 爆裂 | 0.06 | 0.82 | 1000 | 1200 | 500 | 4 | 長く引っ張る |

### Q3. persona 数 × step 数のスイートスポット

stock demo 実測値: 2 agents × 5 step = 45秒 → **1 LLM call ≒ 4.5秒** と仮定。

| 規模 | agent-step | 毎 step LLM | 5 step ごと LLM | 結果の意味 |
|------|-----------|------------|----------------|----------|
| 10 persona × 30 step | 300 | 約22.5分 | 約4.5分 | MVP 成立。個別ドラマ向き |
| 30 persona × 50 step | 1500 | 約1.9時間 | **約22.5分** | 推奨。属性差が見え始める |
| 100 persona × 100 step | 10000 | 約12.5時間 | 約2.5時間 | 統計的には良いが事故りやすい |

**スイートスポット = 30 persona × 50 step、LLM は 5 step ごと + 重要イベント時**

ただし **Day5 までは絶対に 10 × 30 で完成**。最初から 30 × 50 に行くとバグの原因切り分け不能。

### Q4. LLM と rule-based の役割分担

| 領域 | 担当 | 理由 |
|------|------|------|
| 抽選結果 | rule-based | ここを LLM にすると物理実験でなくなる |
| 残金増減 | rule-based | 再現性が必要 |
| arousal / despair の **canonical state** | rule-based | 発散を防ぐ |
| 行動決定 | LLM + fallback rule | LLM の個性を使える |
| 感情の **自己申告** | LLM、ただし canonical とは別保存 | 「本人はどう感じたと言うか」を観測 |
| 独白・発話 | post-process の LLM | 本体 loop に入れると遅い |
| 可視化用の説明文 | post-process の LLM | ログから生成すれば十分 |

**重要**: arousal / despair を 2 系統に分ける。

```
rule_arousal, rule_despair       = シミュレーション上の正式な状態
llm_reported_arousal, llm_reported_despair = persona が自己申告した観察値
```

ハッカソン的に強い:
> 「物理状態としての感情」と「本人の自己申告」を分けて記録した。これにより、同じ損失でも属性によって報告がずれるかを観察できる。

### Q5. 観察出力の最小セット

| 出力 | 必須度 | 内容 |
|------|-------|------|
| `simulation_log.jsonl` or `.csv` | 必須 | persona × step の全状態 |
| 属性別 arousal / despair 推移 | 必須 | カテゴリ別、または 4象限別の線グラフ |
| ホール俯瞰動画 | 必須寄り | 台と persona の位置、感情・残金の変化 |
| 個別 persona のケーススタディ | 必須寄り | 3人程度の残金・arousal・despair・当たり履歴 |

**強い提出物の構成**:
1. 全体グラフ（カテゴリ別 arousal/despair 推移）
2. ホール動画（台移動、当たり/ハマりで状態変化）
3. **3人のドラマ**:
   - 不労所得・地主層: 低 A / 低 D のまま退場
   - 依存症末期: 損失増えても cue_memory で滞在継続
   - 若年女性: 高 A だが despair は一時的に低い
4. 説明文「LLM は数値状態のみを受け取り、行動決定と自己申告を行った」

### Q6. 残り11日のマイルストーン

| Day | 日付 | 目標 | 順調判定 |
|-----|------|------|---------|
| Day0 | 4/26 | 仕様凍結、ファイル構成決定 | Claude Code に渡す仕様が文章化 |
| Day1 | 4/27 | dataclass / persona loader / machine config | LLM なしで 3 persona × 10 step が回る |
| Day2 | 4/28 | Machine 物理実装 | 当たり・外れ・連荘・ハマり・残金増減が log に出る |
| Day3 | 4/29 | emotion rule 実装 | arousal / despair が 0-100 に収まり、発散しない |
| Day4 | 4/30 | LLM wrapper 実装 | qwen3:4b が JSON で action を返す。失敗時 fallback あり |
| Day5 | 5/1 | **MVP 完走** | 10 persona × 30 step、log + グラフ + 簡易動画 |
| Day6 | 5/2 | 中間規模へ拡張 | 30 persona × 50 step が完走 |
| Day7 | 5/3 | 可視化強化 | 属性別グラフ、個別ケース、ホール動画が揃う |
| Day8 | 5/4 | 実験条件比較 | 2-3 条件を回し、提出に使う run を選ぶ |
| Day9 | 5/5 | 解説文章作成 | 企画意図・仕様・結果・限界が書けている |
| Day10 | 5/6 | パッケージング | README、実行手順、動画、図表、コード整理 |
| Day11 | 5/7 | 提出 | 新機能追加禁止 |

**危険判定ライン**:

| 日付 | 状態 | 判断 |
|------|------|------|
| 5/1 時点で 10 × 30 が完走しない | 危険 | LLM を外し、rule-only + post-process LLM に縮退 |
| 5/3 時点で動画が出ない | やや危険 | 動画簡素化、グラフとケーススタディ重視 |
| 5/5 時点で 30 × 50 が不安定 | 危険 | 10 × 30 を完成版として磨く |
| 5/6 に新しい物理機能を足したい | 禁止 | バグを増やすだけ |

### Q7. ハマりやすい罠

| 罠 | 何が起きるか | 対策 |
|----|------------|------|
| LLM JSON が崩れる | parse error で simulation 停止 | JSON 抽出、schema validation、fallback rule 必須 |
| 毎 step LLM | 実験が数時間〜半日 | 5 step ごと、またはイベント時のみ |
| 感情遷移が発散 | arousal/despair が常に 100 | clip(0,100)、変化量上限、減衰項 |
| 台の物理をリアルにしすぎる | 実装が終わらない | 抽象モデルにする |
| 169 cards 全投入 | デバッグ不能 | stratified sample 10 → 30 |
| 14経路を全部 dynamic | 複雑すぎる | `addiction_load` に圧縮 |
| 可視化を後回し | 結果が見えず提出物が弱い | Day5 で簡易動画まで作る |
| seed を固定しない | 再現できない | `--seed` 必須 |
| ログ設計が雑 | 後でグラフが作れない | 1 step 1 row の JSONL/CSV |
| LLM 出力を信じすぎる | 物理実験でなく物語生成 | canonical state は rule-based |
| qwen3:30b を使いたくなる | デバッグ速度が落ちる | 4b 主軸 |
| 配布コードに寄せすぎる | 本来の loop が作れない | 時間 loop / wrapper / 可視化パターンだけ借りる |

---

## 2. 推奨仕様 3案

### 案A: 最小仕様（MVP、必ず作る）

| 項目 | 内容 |
|------|------|
| persona | 10人 |
| step | 30 |
| machine | 3種類 × 各2台 = 6台 |
| LLM | 5 step ごとの行動決定のみ |
| 感情 | rule-based canonical + LLM self-report |
| 出力 | log、属性別グラフ、簡易ホール動画、3人のケース |
| LLM calls | 約60回 |
| 所要時間 | 5〜15分 |
| 推奨度 | 必ず作る |

### 案B: 中間仕様（本命）

| 項目 | 内容 |
|------|------|
| persona | 30人 |
| step | 50 |
| machine | 3種類 × 各4台 = 12台 |
| LLM | 5 step ごと + 重要イベント時 |
| 感情 | rule-based canonical + LLM self-report |
| 出力 | log、カテゴリ/象限別グラフ、ホール動画、ケーススタディ、比較実験 |
| LLM calls | 300〜600回 |
| 所要時間 | 約22.5分 + イベント分 |
| 推奨度 | 本命 |

### 案C: フル仕様（余力があれば追加実験）

| 項目 | 内容 |
|------|------|
| persona | 100人 |
| step | 100 |
| machine | 3種類 × 各10台 = 30台 |
| LLM | 10 step ごと、またはイベント時のみ |
| 所要時間 | 約75分（10 step ごと） |
| 推奨度 | Day7 以降に余力があれば |

---

## 3. 仕様ライン（11日で動く / これ以上は危険）

**11日で動くライン**:
- 30 persona / 50 step / 3 machine types / 12 machines
- LLM action every 5 steps + LLM self-report logged separately
- rule-based physics / rule-based canonical emotion
- CSV/JSONL log / 3-5 visualizations / 1 hall animation / 3 persona case studies

**危険ライン**:
- 100 persona × 100 step × every-step LLM
- 30b / 35b 主軸
- 隣人会話を simulation loop に入れる
- 14経路中毒モデルを全部 dynamic
- 実機スペック正確再現
- Unity / Web UI

---

## 4. 実装仕様（具体）

### 4.1 ディレクトリ構成

```
pachinko_hall_sim/
  README.md
  requirements.txt
  data/
    persona_cards.jsonl
  configs/
    machines.yaml
    run_mvp.yaml
    run_mid.yaml
  src/
    models.py
    persona_loader.py
    machine.py
    emotion.py
    policy_rule.py
    policy_llm.py
    llm_client.py
    simulator.py
    logger.py
    visualize.py
    run_simulation.py
  outputs/
    .gitkeep
```

### 4.2 状態モデル

**PersonaCard（静的属性）**:
```python
PersonaCard:
    persona_id: str
    category: str
    age: int | None
    arousal_range: tuple[int, int]
    despair_range: tuple[int, int]
    interruptibility: float
    sensory_gating_factor: float
    stigma_barrier: float
    payday_sensitivity: float
    time_cost_efficiency: float
    path_dependency_score: float  # 0-1
    addiction_load: float         # 0-1
```

カテゴリ別 `path_dependency_score` 仮値:

| カテゴリ | path_dependency_score |
|---------|-----------------------|
| 不労所得・地主層 | 0.20 |
| 中年現役男性 | 0.55 |
| 依存症末期 | 0.95 |
| 精神疾患併発 | 0.70 |
| 主婦 | 0.50 |
| 女子大生・若年女性 | 0.35 |
| 年金生活高齢者 | 0.60 |

**PersonaState（動的状態）**:
```python
PersonaState:
    persona_id: str
    current_machine_id: str | None
    cash: int
    initial_cash: int
    arousal: float
    despair: float
    llm_reported_arousal: float | None
    llm_reported_despair: float | None
    win_streak: int
    miss_streak: int
    total_hits: int
    total_misses: int
    total_spent: int
    total_payout: int
    time_in_hall: int
    cue_memory: float
    status: str  # "playing", "break", "left"
```

**MachineState**:
```python
MachineState:
    machine_id: str
    machine_type_id: int
    occupied_by: str | None
    chain_active: bool
    machine_miss_streak: int
    recent_hit_count: int
    cue_level: float
    total_plays: int
    total_hits: int
    total_payout: int
```

---

## 5. 台の物理モデル

### 5.1 1 step の単位

**1 step = 1000円分の遊技** がおすすめ（時間より残金変化が分かりやすい）

### 5.2 抽選ロジック

```python
def play_one_step(persona, machine, machine_type, rng):
    stake = machine_type.stake_per_step
    persona.cash -= stake
    persona.total_spent += stake

    hit = False
    payout = 0

    if machine.chain_active:
        if rng.random() < machine_type.continue_prob:
            hit = True
            payout = sample_payout(machine_type, rng)
            machine.chain_active = True
        else:
            hit = False
            machine.chain_active = False
    else:
        if rng.random() < machine_type.p_initial_hit:
            hit = True
            payout = sample_payout(machine_type, rng)
            machine.chain_active = True

    persona.cash += payout
    persona.total_payout += payout
    net_delta = payout - stake
    return hit, payout, net_delta
```

### 5.3 ハマりと cue

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

---

## 6. 感情遷移モデル

### 6.1 入力特徴量

```python
loss_ratio = max(0, (initial_cash - cash) / initial_cash)
loss_signal = tanh(max(0, -net_delta) / 3000)
gain_signal = tanh(max(0, net_delta) / 5000)
hammari_signal = 1 - exp(-miss_streak / 8)
cash_low_signal = 1.0 if cash <= 3000 else 0.0
cue_signal = cue_memory
```

### 6.2 arousal 更新式

```python
delta_arousal = (
    + 22.0 * hit_signal
    + 10.0 * gain_signal
    +  6.0 * cue_signal
    +  4.0 * hammari_signal
    -  3.0 * cash_low_signal
)
delta_arousal *= persona.sensory_gating_factor
delta_arousal -= 0.05 * (arousal - base_arousal)  # 自然減衰
arousal = clip(arousal + delta_arousal + noise, 0, 100)
```

ハマりでも arousal が完全には下がらない（焦燥や期待として上がる場合あり）

### 6.3 despair 更新式

```python
delta_despair = (
    + 16.0 * loss_signal
    + 12.0 * loss_ratio
    +  8.0 * cash_low_signal
    +  5.0 * hammari_signal
    - 10.0 * gain_signal
)
delta_despair *= (0.7 + base_despair / 100.0)  # despair trait による増幅
delta_despair += 4.0 * persona.time_cost_efficiency * hammari_signal
delta_despair -= 0.03 * (despair - base_despair)  # 自然減衰
despair = clip(despair + delta_despair + noise, 0, 100)
```

### 6.4 依存負荷の圧縮（14経路 → スカラー）

```python
addiction_load = clip(
    0.45 * path_dependency_score
    + 0.20 * payday_sensitivity
    + 0.15 * (1.0 - interruptibility)
    + 0.10 * sensory_gating_factor
    + 0.10 * time_cost_efficiency,
    0.0, 1.0
)
```

`path_dependency_score` を最重要にして重み 0.45。

---

## 7. 行動決定モデル

### 7.1 行動の選択肢（4択）

```
0 = continue_same_machine
1 = switch_machine
2 = take_break
3 = leave_hall
```

### 7.2 rule-based fallback

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

### 7.3 LLM prompt（数値のみ）

**入力例**:
```json
{
  "persona_static": {
    "category_id": 3,
    "arousal_base": 78, "despair_base": 81,
    "interruptibility": 0.22, "sensory_gating_factor": 0.91,
    "stigma_barrier": 0.74, "payday_sensitivity": 0.63,
    "time_cost_efficiency": 0.41, "path_dependency_score": 0.95,
    "addiction_load": 0.82
  },
  "persona_state": {
    "cash": 6000, "initial_cash": 20000,
    "arousal": 88, "despair": 76,
    "miss_streak": 9, "win_streak": 0,
    "time_in_hall": 23, "cue_memory": 0.61
  },
  "current_machine": {
    "machine_type_id": 2, "machine_miss_streak": 12,
    "cue_level": 0.44, "recent_hit_count": 1
  },
  "candidate_machine_summary": [
    {"machine_type_id": 0, "available_count": 2, "avg_miss_streak": 4.5, "avg_cue_level": 0.1},
    {"machine_type_id": 1, "available_count": 1, "avg_miss_streak": 7.0, "avg_cue_level": 0.3},
    {"machine_type_id": 2, "available_count": 1, "avg_miss_streak": 11.0, "avg_cue_level": 0.5}
  ],
  "valid_actions": [0, 1, 2, 3]
}
```

**出力 schema（reason 入れない、JSON 崩れ防止）**:
```json
{
  "action": 0,
  "target_machine_type_id": 2,
  "reported_arousal": 91,
  "reported_despair": 73,
  "confidence": 0.74
}
```

---

## 8. 観察ログ schema（1 step 1 row）

```json
{
  "run_id": "mid_seed_42",
  "step": 17,
  "persona_id": "R3_012",
  "category": "依存症末期",
  "machine_id": "ART_03",
  "machine_type_id": 2,
  "action": 0,
  "hit": false,
  "payout": 0,
  "stake": 1000,
  "net_delta": -1000,
  "cash": 7000,
  "arousal": 84.2,
  "despair": 71.5,
  "llm_reported_arousal": 88,
  "llm_reported_despair": 69,
  "miss_streak": 8,
  "win_streak": 0,
  "cue_memory": 0.53,
  "time_in_hall": 17,
  "interruptibility": 0.22,
  "sensory_gating_factor": 0.91,
  "stigma_barrier": 0.74,
  "payday_sensitivity": 0.63,
  "time_cost_efficiency": 0.41,
  "path_dependency_score": 0.95,
  "addiction_load": 0.82
}
```

---

## 9. 可視化仕様

### 最小可視化（5種）

1. **属性別 arousal 推移**: x=step, y=mean arousal, group=category or quadrant
2. **属性別 despair 推移**: 同上、despair
3. **最終状態 scatter**: x=final arousal, y=final despair, point=persona, color=category, size=total_spent
4. **個別 persona timeline**: x=step, y1=cash, y2=arousal, y3=despair, marker=hit/leave/cash_zero
5. **ホール俯瞰動画**: machines=grid 上の固定点、persona=machine 上に表示、marker size=arousal、frame=step

matplotlib animation で十分。

---

## 10. 実験条件の候補

中間仕様まで動いたら、比較実験 2-3 個入れる。

### Experiment A: baseline
- 30 persona / 50 step / AT 4, Hokuto 4, ART 4 / payday=0

### Experiment B: ART-heavy hall
- 30 persona / 50 step / AT 2, Hokuto 3, ART 7 / payday=0
- **仮説**: cue_decay_steps が長い ART が多いと、高 addiction_load 群の arousal が持続

### Experiment C: payday condition
- 30 persona / 50 step / AT 4, Hokuto 4, ART 4 / payday=1
```python
initial_cash += int(10000 * payday_sensitivity)
addiction_load += 0.05 * payday_sensitivity
```
- **仮説**: payday_sensitivity が高い persona は滞在時間が伸び、despair spike が後半にずれ込む

---

## 11. Claude Code 分担表

### Claude Code に書かせる

| 作業 | 指示 |
|------|------|
| dataclass 定義 | `models.py` に集約 |
| machine physics | seed 固定、単体テスト付き |
| emotion rule | 0-100 clip、発散防止 |
| simulator loop | LLM なしで動くように先に作る |
| JSONL logger | 1 step 1 row |
| CSV export | pandas で十分 |
| matplotlib 可視化 | 後から調整可能 |
| Ollama wrapper | timeout / retry / fallback 必須 |
| JSON parser / validator | 壊れたら fallback |
| CLI | `--config --seed --no-llm` |
| README 雛形 | 最後に自分で直す |

### 自分で判断する

| 作業 | 理由 |
|------|------|
| どの persona を選ぶか | 企画の意味に直結 |
| machine パラメータ | 何を観察したいかの設計判断 |
| 感情式の重み | 実験の哲学 |
| どのグラフを提出するか | ストーリー設計 |
| 結果の解釈 | ここが一番重要 |
| 169 cards / 14経路モデルの説明 | DR の文脈は自分が一番分かっている |
| 最終 README / 解説文 | 審査・読者に伝える部分 |

---

## 12. Claude Code への実装依頼プロンプト例

### Phase 1: simulation engine（LLM なし）

```
You are implementing a pachinko hall simulation from scratch.

Do not use the existing stock demo as scaffold except for general ideas.
Implement a deterministic simulation engine first, without LLM.

Requirements:
- Python 3.9 compatible.
- Use dataclasses, numpy, pandas, matplotlib only.
- One simulation step = one fixed-cost play session.
- PersonaCard, PersonaState, MachineType, MachineState.
- Machine physics: initial hit prob, chain prob, stake, payout mean/std, miss streak, cue decay
- Persona state: cash, arousal 0-100, despair 0-100, win/miss streak, cue_memory, time_in_hall
- Emotion rule-based, clipped 0-100
- One JSONL row per persona per step
- CLI: python -m src.run_simulation --config configs/run_mvp.yaml --seed 42 --no-llm
- Plots: outputs/<run_id>/arousal_by_category.png, despair_by_category.png, persona_timeline_<id>.png
- Smoke test: 3 personas, 3 machines, 10 steps, no LLM
```

### Phase 2: LLM wrapper（後で追加）

```
Add Ollama /api/chat integration.
- Model: qwen3:4b-instruct-2507-q4_K_M
- Options: think:false, stream:false
- LLM called only every policy_interval steps or on important events
- Input: numeric JSON
- Output: strict JSON {action, target_machine_type_id, reported_arousal, reported_despair, confidence}
- Parse fail → rule-based fallback
- Log action source: "llm" or "fallback"
- Cache: outputs/<run_id>/llm_cache.jsonl
```

---

## 13. 169 cards の活かし方

### MVP sampling（10人）
- 不労所得・地主層: 1
- 中年現役男性: 1
- 依存症末期: 2
- 精神疾患併発: 1
- 主婦: 1
- OL・社会人女性: 1
- 女子大生・若年女性: 1
- 年金生活高齢者: 1
- 風俗・夜職系女性: 1

### 中間 sampling（30人）
各カテゴリから 2-3 人。依存症末期 / 不労所得 / 中年現役男性 / 若年女性は多め。
カテゴリ別だけでなく **4象限別**でも集計（n=30 だと象限の方が安定）。

### フル sampling（100人）
169枚から stratified sampling。カテゴリ別比較に説得力出る段階。

---

## 14. 提出物としてのストーリー

解説文章の構成:

1. **問題意識**: パチンコホールを「人が場所を選ぶ空間」ではなく「台の確率物理と persona の感情状態が相互作用する場」としてモデル化
2. **物理モデル**: 各台に当たり確率、連荘確率、払戻、cue decay。ハマりは miss_streak、連荘は continue_prob
3. **persona モデル**: 各 persona が arousal/despair の初期レンジ + interruptibility, sensory_gating_factor, stigma_barrier, payday_sensitivity, time_cost_efficiency
4. **LLM の役割**: LLM は物理を決めない。numeric state のみを入力として、行動選択と感情自己申告を返す
5. **観察結果**:
   - 高 addiction_load 群は cue_memory が残る台で滞在しやすい
   - 低 arousal / 低 despair 群は早期離脱しやすい
   - 高 arousal / 高 despair 群では、損失と継続が同時に発生する
6. **限界**:
   - 実機スペックの再現ではなく、抽象物理モデル
   - カテゴリ別 n は限定的
   - LLM の自己申告は安定性に課題

**限界を書いた方が、むしろ実験として誠実に見える**。

---

## 15. 実装優先順位（絶対この順番）

1. LLM なし simulation
2. machine physics
3. emotion rule
4. JSONL logging
5. basic plots
6. LLM action
7. LLM self-report
8. animation
9. case study
10. comparison experiments

LLM wrapper を先に作ると詰まる。**まず rule-only で「物理実験」が動くことが最優先**。

---

## 16. 最終判断用まとめ

| 案 | 選ぶ理由 |
|----|---------|
| 最小案 | とにかく提出可能性を最大化 |
| **中間案** | **本命。観察可能性と実装可能性のバランス** |
| フル案 | Day7 以降の追加実験。最初から狙うと危険 |

**仕様ライン**:
- Day5 までに 10 persona × 30 step を完成
- Day6-8 で 30 persona × 50 step に拡張
- 100 persona は提出用本体ではなく、余力があれば "追加実験"

これが一番安全で、DR の蓄積も活かせるライン。
