# Singulabo Hackathon — プロジェクト仕様書（最終版）

シンギュラボのハッカソン提出用プロジェクト。
DR + ChatGPT Pro v3 相談を経て確定した**段階的群像路線**で実装する。

## 基本情報

| 項目 | 値 |
|------|-----|
| 開始日 | 2026-04-18 |
| 提出締切 | 2026-05-07 |
| 残期間 | 約3週間 |
| id | `singulabo-hackathon` |
| 方針 | **🎭 段階的群像路線**（中間バランス型 → 最終だけフル群像） |

## テーマと仮説

### 動機
ユーザーが15年間ギャンブル依存症だった経験の「答え合わせ」。
パチンコホールにいる多様な人々の内面を LLM に "定量データだけで" 演じさせ、
どんな瞬間に興奮・不幸が生まれるかを観察する。

### 検証仮説
> **stress × comeback-cue の相互作用**の瞬間に、dopamine 相当の salience proxy が跳ね上がる
> さらに、**「継続期待の時間構造」**（短時間 spike 型 vs 長時間 tether 型）が中毒性の質を変える

### 観察アウトカム
- 覚醒語彙の自然発生（「まだいける」「熱い」「取り返せる」）
- 不幸語彙の頻度（「もう無理」「終わった」）
- `continue_rate` / `mean_dwell_steps` / `hall_heat` / `despair_heat`
- 機種間の継続ステップ数の差（AT 短 spike vs ART 長 tether）

## 核心メッセージ（企画の一行説明）

> **stress × comeback-cue で見るパチンコホール群像 — 一撃量ではなく継続期待の時間構造が中毒性の質を変える**

## 守るべき哲学（1 つだけ）

**エージェントには数値データのみを渡す**（`stress_index=0.83` のように名前付き数値）。
「危険」「嬉しい」「中毒者として振る舞え」等の定性指示は一切含めない。
これが配布コードの独自性の核心。ここを壊すと企画の価値が消える。

## ベースコード

`reference/` に配布コード（`2d-multi-places-simulation-on-fire-public`）を格納。
- Ollama 駆動（`localhost:11434`）
- 場所 (`places`) + イベント (`fires`) の構造
- `message` + `action` 生成ループ
- 出力: `messages.jsonl`, `memory_reasoning.jsonl`, `frame_*.png`
- 可視化: `viewer.html`, `generate_video.py`

## 実行環境

| 項目 | 値 |
|------|-----|
| マシン | MacBook Pro (Mac16,5, 2024) |
| チップ | Apple M4 Max（CPU 16 / GPU 40, Metal 4）|
| メモリ | 64 GB unified |
| ストレージ | 2 TB SSD |

## インストール済みモデル

| モデル | サイズ | 用途 |
|--------|-------|------|
| `qwen3:4b-instruct-2507-q4_K_M` | 2.5 GB | **主軸 backbone（全エージェント基本）** |
| `qwen3.5:9b` | 6.6 GB | 比較用（thinking 切れないので限定的） |
| `qwen3:30b` | 18 GB | **前景 6-8 人用** |
| `qwen3.5:35b-a3b` | 23 GB | 5/03 以降の最終 polish のみ |
| `*-nothink` エイリアス 3 個 | ±0 | CLI 対話用（API 実装なら不要） |

**注意**: CLI で `SYSTEM "/no_think"` は効かない。本番は **API 経由で `think: false`** を送る。

## 推奨路線: 段階的群像路線

### 大方針（一行）
**設計は 100、運転は 5 から、比較は 1 機種から、最終だけ群像化。**

### スケール設計
- **設計**: 100 persona pool（Claude Code が JSON 生成）
- **運転**: 5 → 12 → 24 → 36（→ 最終だけ 48〜60）
- **機種**: 最初 1 → AT vs ART の 2 → 最終 3 世代
- **モデル**: 最初は全員 4B → 前景 6-8 人だけ 30B

### モデル構成（確定）
- **backbone**: `qwen3:4b-instruct-2507-q4_K_M`
- **foreground 6-8 人**: `qwen3:30b`
- **最終 polish のみ**: `qwen3.5:35b-a3b`（通るなら）

### Ollama 設定（本番 API 実装時）
```python
# /api/chat に投げる共通設定
{
    "think": False,
    "stream": False,
    "keep_alive": -1,
    "options": {
        "num_ctx": 1536,      # background / 2048 / foreground 3072
        "num_predict": 40,    # background / foreground 80
        "temperature": 0.35,  # background / foreground 0.6
    }
}
```

### 環境変数（Ollama server）
```
OLLAMA_NUM_PARALLEL=1           # 最初は 1、安定後 2
OLLAMA_MAX_LOADED_MODELS=1      # 安定後 2
OLLAMA_MAX_QUEUE=256
OLLAMA_FLASH_ATTENTION=1
OLLAMA_KV_CACHE_TYPE=q8_0
OLLAMA_CONTEXT_LENGTH=4096      # または 8192 に明示
```

### 出力フォーマット（soft schema + validator + 1 retry）
```json
// foreground (qwen3:30b)
{
  "action_id": 0-5,
  "target_place_id": 0-8,
  "stake_shift": -1|0|1,
  "continue_prob": 0-100,
  "arousal": 0-100,
  "despair": 0-100,
  "message": "24字以内"
}

// background (qwen3:4b)
{
  "action_id": 0-5,
  "target_place_id": 0-8,
  "continue_prob": 0-100,
  "arousal": 0-100,
  "despair": 0-100,
  "message": "12字以内"
}
```

**JSON strict に期待しない**。validator で検査 → 1 回 retry → 失敗したら quarantine（落とさない）。

## 機種設計（3 世代）

| 機種 | 世代 | `continuity_index` | `cue_decay_steps` |
|------|------|-------------------|------------------|
| AT 爆裂（ミリオンゴッド系） | 2000s | 0.35 | 1 |
| 4.5号機（北斗の拳系） | 2000s後半 | 0.58 | 2 |
| **ART 爆裂** | **2010s** | **0.82** | **4** |

**中核数式**:
```
comeback_cue = 0.45*near_miss + 0.25*drop_from_peak + 0.20*neighbor_win + 0.10*signal
dopamine_proxy = stress_index * comeback_cue + 0.35 * continuity_index * active_run
```

2010s ART の本体は「一度熱に入った後の linger（継続）」を `continuity_index` と `cue_decay_steps` で表現。

## 場所設計

9 place 構成:
- `AT_bank`（capacity=16）
- `Hokuto_bank`（capacity=16）
- `ART_bank`（capacity=20） ← 熱量が可視化で勝つように座席多め
- `entrance`, `walkway`, `smoking`, `rest`, `counter`, `exit`

解析用 run は bank-isolated（1 機種だけ配置）、最終動画は三世代同居ホール。

## ペルソナ設計

**100 persona pool**（Claude Code が HAG 風 quota で生成）。
年齢帯、職業、家族、可処分現金、借入額、依存重症度、羞恥反応、隔離感、衝動性、損失追跡傾向、会話性、来店動機、機種経験、を**全部数値または code 化**。

LLM に渡すのは numeric state のみ。人間閲覧用の `caption_ja` と `seed_memory_ja` は別ファイル。

### 固定 foreground 12 人（密観察）
- コア 5 人（a: 借金学生、b: 主婦、c: 依存症サラリーマン、d: 金なし大学生、e: ルンルン学生）
- + 中年自営、年金生活者、回復期ギャンブラー、カップル同行者、ホール常連、高揚しやすい初心者、無感情な観察者

### 可変 background
pool 100 から run ごとにサンプリング。

## 時間設計

- 48 step（final） / 36 step（pilot）
- 1 step = 15 分 ≒ 40-60 ゲーム相当
- ホール 12 時間営業を 1 run に収める

## 実験条件（必須 6-8 run）

| # | 機種 | stress | cue | 目的 |
|---|------|--------|-----|------|
| 1 | AT | low | low | baseline |
| 2 | AT | high | high | 興奮ピーク |
| 3 | 4.5 | low | low | baseline |
| 4 | 4.5 | high | high | 中間比較 |
| 5 | ART | low | low | baseline |
| 6 | **ART** | **high** | **high** | **本命**（2010s tether） |
| 7 | ART | low | high | persona(e) 変容 1 |
| 8 | ART | high | high | persona(e) 変容 2 |

## 3 週間マイルストーン

### Week 1（4/18-4/24）— 基盤を固める週
**目標**: 5 → 12 → 24 active まで、落ちずに回る。1 機種でよいのでパイプライン完成。

**Day 1 (4/18-19)**: `/api/chat` wrapper 作成
- `think:false`, `stream:false`, `keep_alive:-1`, `num_ctx` 明示
- `generate` ではなく `chat` を使う
- qwen3.5 の hard schema 依存は避ける

**Day 2 (4/20)**: 5 agents × 12 steps が落ちずに完走
- 品質でなく **落ちない** ことを確認
- `messages.jsonl` と動画まで出す

**Day 3 (4/21)**: metrics script + 100 persona pool
- `continue_rate`, `mean_dwell_steps`, `hall_heat` の 3 指標
- Claude Code に 100 persona JSON 生成させる

**ゲート**:
- **4/21**: stock demo + 5-15 agents + 12 steps 完走
- **4/25**: 24 agents / 24-36 steps / 1 run 90 分以内 / bad output 5% 未満

### Week 2（4/25-5/1）— 仮説を見える形にする週
**目標**: AT vs ART の差がログと動画で読める。

- 2×2 実験 runner（low/high stress × low/high cue）
- machine parameter packs
- spotlight overlay
- aggregate plots
- batch seed runner

**ゲート**:
- **4/29**: 2×2 ログで 1 本 publishable な図が出る
- **5/02**: 「図 2-3 枚 + 主張 1 文」を凍結

### Week 3（5/2-5/7）— 提出物を作る週
**目標**: 新発見ではなく、**既に出た差を最も伝わる形に仕上げる**。

- 5/02: config 凍結
- 5/03-04: final runs（35B が通るなら最終 polish）
- 5/05: 動画編集
- 5/06: README / 解説文
- 5/07: 提出

**5/02 以降はモデルを増やさない。**

## Claude Code 分担表

| 担当 | Claude Code | 人間 |
|------|------------|------|
| persona schema 設計 + 100 JSON 生成 | ✅ | レビューのみ |
| `/api/chat` wrapper 実装 | ✅ | |
| runtime の config-driven リファクタ | ✅ | |
| local validator / repair / retry | ✅ | |
| log parser + metrics script | ✅ | |
| viewer overlay（hall_heat, spotlight） | ✅ | |
| machine parameter packs | ✅ | |
| 2×2 実験 runner | ✅ | |
| batch seed runner | ✅ | |
| final render scripts | ✅ | |
| README 草稿 | ✅ | 書き直し |
| 出力のリアリティ判定 | | ✅ |
| 機種パラメタの意味づけ | | ✅ |
| "それっぽい" 表現の選択 | | ✅ |
| core 5 persona の質感チェック | | ✅ |
| 仮説 proxy 調整 | | ✅ |
| 主張の決定 | | ✅ |
| best seed 選択 | | ✅ |
| 動画切り出し | | ✅ |
| 解説文の最終表現 | | ✅ |

## 撤退ゲート & 縮退順序

### ゲート通過基準（再掲）
- 4/21: stock demo 完走
- 4/25: 24 agents / 24-36 step / 90 分以内 / bad 5% 未満
- 4/29: 2×2 ログで 1 本の図
- 5/02: 図 + 主張 凍結

### 時間切れ時の縮退順序
1. **active 数を減らす**（48 → 36 → 24 → 12）
2. **step 数を 36 に落とす**
3. **4.5 号機を切る**（AT vs ART の 2 機種に）
4. **背景 action を rule-based 化**
5. **背景 message を極短文化**
6. **最終的に 8-12 agent の比較動画で守る**

### モデル代替の順
1. qwen3:4b を主軸固定
2. 前景だけ qwen3:30b
3. それでも遅ければ **30B をやめる**
4. 最後だけ 35B-A3B（通るなら）
5. qwen3.6 や MLX 新タグは**締切前の backbone にしない**

**遅いからといって "より新しくて大きいモデル" に逃げない。**

### 最低限の提出ライン（最悪の撤退版）
- base repo を fork したコード
- 8-12 agents
- 2 機種（AT vs ART）
- 30-40 steps
- qwen3:4b only
- 1 本の比較動画
- 1 枚の continue_rate or dwell time 図
- 1 段落の仮説説明

これでも仮説の芯は残る。

## 初心者の罠チェックリスト（必読）

| # | 罠 | 対策 |
|---|----|------|
| 1 | 文脈長を放置する | `num_ctx` を 1536〜4096 に明示 |
| 2 | `think:false` / `stream:false` を毎回明示しない | wrapper で固定設定 |
| 3 | strict schema に期待しすぎる | soft schema + validator + retry |
| 4 | bad output で即 crash | quarantine して走り続ける |
| 5 | モデルをコロコロ変える | wrapper 固定、差し替えは config だけ |
| 6 | 解析を後回し | Day 3 までに metrics script |
| 7 | scale 前に測定器がない | **一番危険** |

## 提出物の形

### 動画構成（90-140 秒）
- **0-12 秒**: タイトル + ホール全景
- **12-30 秒**: 3 島 + 5 人主役紹介
- **30-75 秒**: 群像中盤、hall_heat/despair_heat/continue_rate オーバーレイ、2-3 人スポット
- **75-105 秒**: クライマックス、AT spike vs ART tether 対比、persona(e) 変容
- **105-140 秒**: まとめ + 図 1-2 枚

### 解説文の核心
> 私は自分の実体験から、「最大ストレスと大逆転認知が重なる瞬間に最も強い覚醒が起こるのではないか」という仮説を持っていた。そこで、配布された定量-only マルチエージェント基盤を拡張し、3 世代の機種特性を `continuity` や `cue_decay` といった数値パラメタで operationalize した。結果として、短時間 spike 型と長時間 tether 型では、同じ"当たり"でも群像全体の熱の持続が違って見えた。

### GitHub README 構成
1. 企画概要
2. 仮説
3. ベースコードからの変更点
4. persona schema
5. machine schema
6. 実行方法
7. 出力ファイルの見方
8. 代表結果
9. 制限事項と倫理メモ

## 運用ルール

### 自律実行
- コード実装、Claude Code subagent、作業ジャーナル更新、git commit は確認なしで実行
- 破壊的操作（reference/ の改変、大規模設計変更）はユーザーに確認
- 迷ったら「ゲートを守る」側で判断

### コミット
- calchan:/CLAUDE.md のコミット規約に従う
- `reference/` は基本 touch しない

### ログ
- 作業記録は calchan: 直下の `memory/work-journal.md`
- ハマりは `memory/gotchas.md`

## 関連ドキュメント

- [ChatGPT Pro 初回相談](docs/相談プロンプト.md) + [回答](docs/chatgpt-response.md)
- [相談プロンプト v2](docs/相談プロンプト-v2.md)
- [Deep Research プロンプト](docs/deep-research-prompt.md)
- [ChatGPT Pro v3 相談プロンプト](docs/相談プロンプト-v3.md)
- [**ChatGPT Pro v3 回答（最新・確定版）**](docs/chatgpt-response-v3.md)
- [子ノート](../../../../../Documents/キャルちゃんリンク/100_Notes/1.2026年/singulabo-hackathon.md)
