# Singulabo Hackathon — プロジェクト仕様書（v4 確定版）

シンギュラボのハッカソン提出用プロジェクト。
ChatGPT Pro v4 相談（2026-04-26）を経て **配布コードを捨てて新規実装** する方針に転換。
物理は rule-based で安定、LLM は間引いて使う段階拡張プラン。

## 基本情報

| 項目 | 値 |
|------|-----|
| 開始日 | 2026-04-18 |
| 提出締切 | 2026-05-07 |
| id | `singulabo-hackathon` |
| 方針 | **🔬 物理実験シミュレーター路線**（rule-based physics + 間引き LLM） |
| 仕様の出典 | [docs/chatgpt-response-v4.md](docs/chatgpt-response-v4.md) |

## 動機と仮説

### 動機
ユーザーが15年間ギャンブル依存症だった経験の「答え合わせ」。
パチンコホールに **複数種類×複数台の台** を並べ、ペルソナを 10〜100人配置して
「**どういう属性の人が、どういう感情を持つか**」を観察する物理実験。

### 仮説
> **stress × comeback-cue × continuity** の相互作用で arousal/despair が変動し、
> 持続期待の時間構造（AT 短 spike vs ART 長 tether）が中毒性の質を変える。
> さらに **path dependency（生活がパチに最適化された年数）** が滞在時間と離脱判断を支配する。

### 観察アウトカム
- カテゴリ別 arousal / despair の時間推移
- 4象限（高A高D / 高A低D / 低A高D / 低A低D）別の滞在時間と離脱パターン
- 機種間の continue_rate / mean_dwell_steps / cue_memory 持続
- LLM 自己申告（reported_arousal/despair）と canonical state のズレ

## 核心メッセージ（企画の一行説明）

> **物理状態としての感情と、本人の自己申告を分けて記録する。
> 同じ損失でも属性によって報告がズレることを観察可能にする。**

## 守るべき哲学（4 つ）

1. **LLM には数値のみ渡す**（「危険」「嬉しい」等の定性ラベル禁止）
2. **物理・抽選・感情の canonical state は rule-based**（再現性・発散防止）
3. **LLM は行動決定 + 自己申告のみ**（5 step ごとに間引く）
4. **感情は 2 系統で記録**:
   - `rule_arousal/despair` = シミュレーション上の正式な状態
   - `llm_reported_arousal/despair` = persona が自己申告した観察値

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

## 機種設計（3世代）

| machine_type_id | 機種 | p_initial_hit | continue_prob | stake | payout_mean | payout_std | cue_decay_steps | 狙い |
|----|------|--------------|--------------|-------|-------------|-----------|----------------|------|
| 0 | AT 爆裂 | 0.08 | 0.35 | 1000 | 3500 | 1600 | 1 | 短期で大きく振れる |
| 1 | Hokuto（4.5号機） | 0.07 | 0.58 | 1000 | 2500 | 1000 | 2 | 中間的 |
| 2 | ART 爆裂 | 0.06 | 0.82 | 1000 | 1200 | 500 | 4 | 長く引っ張る（本命） |

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
```

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

## 感情モデル

### 入力特徴量

```python
loss_ratio = max(0, (initial_cash - cash) / initial_cash)
loss_signal = tanh(max(0, -net_delta) / 3000)
gain_signal = tanh(max(0, net_delta) / 5000)
hammari_signal = 1 - exp(-miss_streak / 8)
cash_low_signal = 1.0 if cash <= 3000 else 0.0
cue_signal = cue_memory
```

### arousal 更新

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

ハマりでも arousal が完全には下がらない（焦燥や期待として上がる場合あり）。

### despair 更新

```python
delta_despair = (
    + 16.0 * loss_signal
    + 12.0 * loss_ratio
    +  8.0 * cash_low_signal
    +  5.0 * hammari_signal
    - 10.0 * gain_signal
)
delta_despair *= (0.7 + base_despair / 100.0)  # despair trait 増幅
delta_despair += 4.0 * persona.time_cost_efficiency * hammari_signal
delta_despair -= 0.03 * (despair - base_despair)  # 自然減衰
despair = clip(despair + delta_despair + noise, 0, 100)
```

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

### LLM prompt 設計（数値のみ）

入力例:
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
  "current_machine": {"machine_type_id": 2, "machine_miss_streak": 12, "cue_level": 0.44, "recent_hit_count": 1},
  "candidate_machine_summary": [...],
  "valid_actions": [0, 1, 2, 3]
}
```

出力 schema（reason は入れない、JSON 崩れ防止）:
```json
{"action": 0, "target_machine_type_id": 2, "reported_arousal": 91, "reported_despair": 73, "confidence": 0.74}
```

## ログ schema（1 step 1 row）

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
  "cash": 7000,
  "arousal": 84.2, "despair": 71.5,
  "llm_reported_arousal": 88, "llm_reported_despair": 69,
  "miss_streak": 8, "win_streak": 0,
  "cue_memory": 0.53, "time_in_hall": 17,
  "interruptibility": 0.22, "sensory_gating_factor": 0.91,
  "stigma_barrier": 0.74, "payday_sensitivity": 0.63,
  "time_cost_efficiency": 0.41, "path_dependency_score": 0.95,
  "addiction_load": 0.82
}
```

## 可視化仕様（5種）

1. **属性別 arousal 推移**: x=step, y=mean arousal, group=category or quadrant
2. **属性別 despair 推移**: 同上、despair
3. **最終状態 scatter**: x=final arousal, y=final despair, point=persona, color=category, size=total_spent
4. **個別 persona timeline**: x=step, y1=cash, y2=arousal, y3=despair, marker=hit/leave/cash_zero
5. **ホール俯瞰動画**: machines=grid 上の固定点、persona=machine 上に表示、marker size=arousal、frame=step（matplotlib animation）

## マイルストーン（Day1-11）

| Day | 日付 | 目標 | 順調判定 |
|-----|------|------|---------|
| Day0 | 4/26 | 仕様凍結、スケルトン作成、persona JSONL 生成 | CLAUDE.md / pachinko_hall_sim/ / data/persona_cards.jsonl 揃う |
| Day1 | 4/27 | dataclass / persona loader / machine config | LLM なしで 3 persona × 10 step が回る |
| Day2 | 4/28 | Machine 物理実装 | 当たり・外れ・連荘・ハマり・残金増減が log に出る |
| Day3 | 4/29 | emotion rule 実装 | arousal / despair が 0-100 に収まり、発散しない |
| Day4 | 4/30 | LLM wrapper 実装 | qwen3:4b が JSON で action を返す。失敗時 fallback |
| Day5 | 5/1 | **MVP 完走** | 10 persona × 30 step、log + グラフ + 簡易動画 |
| Day6 | 5/2 | 中間規模へ拡張 | 30 persona × 50 step が完走 |
| Day7 | 5/3 | 可視化強化 | 属性別グラフ、個別ケース、ホール動画揃う |
| Day8 | 5/4 | 実験条件比較 | 2-3 条件回し、提出に使う run を選ぶ |
| Day9 | 5/5 | 解説文章作成 | 企画意図・仕様・結果・限界が書けている |
| Day10 | 5/6 | パッケージング | README、実行手順、動画、図表、コード整理 |
| Day11 | 5/7 | 提出 | 新機能追加禁止 |

### 危険判定ライン

| 日付 | 状態 | 判断 |
|------|------|------|
| 5/1 時点で 10 × 30 が完走しない | 危険 | LLM 外し、rule-only + post-process LLM に縮退 |
| 5/3 時点で動画が出ない | やや危険 | 動画簡素化、グラフとケーススタディ重視 |
| 5/5 時点で 30 × 50 が不安定 | 危険 | 10 × 30 を完成版として磨く |
| 5/6 に新機能を足したい | 禁止 | バグを増やすだけ |

### 縮退順序

1. active 数を減らす（30 → 24 → 12 → 8）
2. step 数を 30 に落とす
3. 機種を 2 種類に（AT vs ART）
4. 行動決定を rule-only に
5. LLM を post-process だけに

## ハマる罠（12個）

| # | 罠 | 対策 |
|---|----|------|
| 1 | LLM JSON が崩れる | JSON 抽出、schema validation、fallback rule 必須 |
| 2 | 毎 step LLM | 5 step ごと、またはイベント時のみ |
| 3 | 感情遷移が発散 | clip(0,100)、変化量上限、減衰項 |
| 4 | 台の物理をリアルにしすぎる | 抽象モデルにする |
| 5 | 169 cards 全投入 | stratified sample 10 → 30 |
| 6 | 14経路を全部 dynamic | `addiction_load` に圧縮 |
| 7 | 可視化を後回し | Day5 で簡易動画まで作る |
| 8 | seed を固定しない | `--seed` 必須 |
| 9 | ログ設計が雑 | 1 step 1 row の JSONL/CSV |
| 10 | LLM 出力を信じすぎる | canonical state は rule-based |
| 11 | qwen3:30b を使いたくなる | 4b 主軸 |
| 12 | 配布コードに寄せすぎる | `reference/` は触らない、参考用に残すだけ |

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

## 実装優先順位（絶対この順番）

1. LLM なし simulation（rule-only）
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
- ケイゴが手を動かす機会を残す（venv 構築・実装着手・コマンド実行）
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

## 関連ドキュメント

- [**docs/chatgpt-response-v4.md**](docs/chatgpt-response-v4.md) ★ 仕様の出典
- [docs/相談プロンプト-v4.md](docs/相談プロンプト-v4.md)
- [docs/chatgpt-response-v3.md](docs/chatgpt-response-v3.md)（旧路線、参考用）
- [docs/multi-path-addiction-model.md](docs/multi-path-addiction-model.md)（14経路モデル原典）
- [reports/R1-R3-aggregation.md](reports/R1-R3-aggregation.md)（persona 統計）
- [子ノート](../../../../../Documents/キャルちゃんリンク/100_Notes/1.2026年/singulabo-hackathon.md)
