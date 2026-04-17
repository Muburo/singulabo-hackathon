# Singulabo Hackathon — プロジェクト仕様書

シンギュラボのハッカソン提出用プロジェクト。キャル（Claude Code）がこの CLAUDE.md を読めば自走できるようにする。

## 基本情報

| 項目 | 値 |
|------|-----|
| 開始日 | 2026-04-18 |
| 提出締切 | 2026-05-07 |
| 残期間 | 約3週間 |
| id | `singulabo-hackathon` |

## テーマと仮説

### オリジナルの動機
ユーザーが15年間ギャンブル依存症だった経験の「答え合わせ」。
当時の体感として、**大負け・仕事のストレス・借金プレイ等で最大にストレスがかかっている瞬間に、大逆転の可能性を認知したときが最もドーパミンが出ていた**のではないかという仮説。

### 洗練された検証仮説（ChatGPT Pro 助言で修正）
> **stress 単独ではなく、stress × comeback-cue の相互作用**の瞬間に、
> dopamine-like な salience / anticipation proxy が跳ね上がるのではないか。

2025年の急性ストレス研究では、problem gambling 群で急性ストレス単独では gambling urges は上がらなかったという報告がある。EGM（電子ゲーミングマシン）研究では **near-miss が reward expectancy を高める / loss-chasing が中核症状 / 機械設計自体が salience・prediction error・uncertainty を強める**というのが強いエビデンス。この知見に合わせて仮説を精密化。

### 観察対象
「本当にドーパミンが出たか」ではなく、
**LLM エージェントが `reasoning` / `message` で自発的に高覚醒な言葉を使い、継続行動を強めるか**。
- 「まだいける」「ここで来る」「取り返せる」「焦る」「熱い」系の語彙の自然発生頻度
- `continue` / `quit` の意思決定
- 賭け額の escalation
- 直近損失後の loss-chasing 率

## ベースコード

配布コード: `reference/` に格納（`2d-multi-places-simulation-on-fire-public`）。

- ollama 駆動のローカルLLM
- デフォルト: 20エージェント × 100ステップ × 2回推論 = 約4000回の LLM 呼び出し
- 各エージェントは毎ステップ `message`（会話）→ `action`（移動）を出力
- エージェントには**定量データのみ**を与え、定性ラベルは一切含めない設計哲学
- 場所（places）は収容上限と位置を持つ。火事イベント（fires）は `start_step` で発生

主要ファイル:
- `reference/main.py` — エントリポイント
- `reference/simulation.py` — シミュレーションループ
- `reference/agent.py` — エージェント本体（LLMプロンプト生成）
- `reference/ollama_client.py` — ollama API クライアント
- `reference/config.yaml` — パラメータ定義
- `reference/visualization.py` — 可視化
- `reference/visualization/viewer.html` — ブラウザで結果閲覧
- `reference/visualization/generate_video.py` — MP4動画生成

## 実行環境

| 項目 | 値 |
|------|-----|
| マシン | MacBook Pro (Mac16,5, 2024) |
| チップ | Apple M4 Max |
| CPU | 16コア（P 12 + E 4） |
| GPU | 40コア（Metal 4） |
| メモリ | 64 GB（unified） |
| ストレージ | 2 TB SSD（1.77 TB free） |

## モデル選定戦略（ChatGPT Pro 助言）

### 勝ち筋
**「巨大モデル一点賭け」ではなく「Qwen3 中型 × non-thinking × 短文出力 × 最後だけ上位モデル」の多段戦略。**
用途は「長い思考を1回」ではなく「短い推論を4000回」なので、モデルの賢さより **thinking を切れるか・出力を短く縛れるか・量子化サイズが軽いか** が効く。

### 採用モデル

| 役割 | モデル | サイズ | context | 用途 |
|------|--------|--------|---------|------|
| 動作確認 | `qwen3:4b-instruct-2507-q4_K_M` | 2.5GB | 256K | 最初の wiring 確認、smoke test |
| **本命** | `qwen3:14b-q4_K_M` | 9.3GB | 40K | 本番実験の主力。ここから始める |
| 仕上げ用 | `qwen3:30b-a3b-instruct-2507-q4_K_M` | 19GB | 256K | MoE（30B total / 3B active）。最終 run のみ |
| 比較保険 | `gemma4:26b-a4b-it-q4_K_M` | 18GB | 256K | Qwen と比較したい時の第2候補 |
| 既定比較枠 | `gpt-oss:20b` | 14GB | 128K | 配布コードの既定モデルとの比較 |

### 外すもの
- **70B 量子化**（Llama 3.3 70B q4 = 43GB）: 64GB の headroom が細すぎて 4000-call workload に不安
- **fp16 / bf16**: `qwen3:30b-a3b-instruct-2507-fp16` = 61GB, `gemma4:31b-it-bf16` = 63GB で OS + KV cache + context を考えると危険

### 役割分担の重要テク
**`message` と `action` を同じモデルにしない**。
仮説の本丸は「内面の言語化」なので `message` だけ 14B/30B にして、`action` は 4B かルールベースに落とす。速度と品質を両立させる。

## 進め方（7ステップ）

### Step 1: Ollama セットアップ & 4B 単発確認 【〜4/20】
- [ ] Ollama インストール（macOS Sonoma 14+ の Apple M 系公式サポート済）
- [ ] `ollama serve` 起動
- [ ] `ollama pull qwen3:4b-instruct-2507-q4_K_M`
- [ ] `ollama run qwen3:4b` で単発対話確認
- [ ] **`ollama ps` で `PROCESSOR=100% GPU` を確認**（ここが CPU fallback してたら以降の議論が崩れる）

### Step 2: microbenchmark（stock のまま小規模実行） 【〜4/21】
- [ ] `reference/` をそのまま venv セットアップ、`requirements.txt` 導入
- [ ] `config.yaml` の `num_agents=2, duration=5` に縮小
- [ ] **Qwen3 の場合: `think=false`** を必ず設定（thinking デフォルト有効、切らないと遅い）
- [ ] `keep_alive=-1`（モデルが 5分で unload されるのを防ぐ）
- [ ] `num_predict` を小さく固定（既定 -1 = 無制限なので縛る）
- [ ] 4B と 14B で wall time と平均出力長を測定
- [ ] 余裕があれば 30B-A3B も

**ゲート: 4/21 までに 4B or 14B で stock demo が回ること**（未達なら撤退基準へ）

### Step 3: 出力スキーマ & 観測指標を固定 【〜4/23】
- [ ] `action` は JSON schema で縛る（ollama の structured outputs 使用）
- [ ] `message` は1文だけに強制
- [ ] 観測する感情語彙リストを先に定義（「まだいける」「ここで来る」「取り返せる」「焦る」「熱い」等）
- [ ] `seed` 固定方針を決める（LLM seed + 環境 RNG seed）

### Step 4: モデルを2つに絞る 【〜4/24】
- [ ] smoke test 用: `qwen3:4b`
- [ ] 本番用: `qwen3:14b`
- [ ] 3本以上並走はしない（比較沼回避）

### Step 5: places/fires をパチスロ化 【〜4/29】
最小構造の5要素のみ実装:

1. **`stress_index`** — 累積損失・借金・外部ストレス由来の 0.0〜1.0
2. **可変比率報酬** の基本構造（毎ステップ当たり・ハズレの確率）
3. **`cue_strength`** — near-miss / 大逆転の兆し強度
4. **mode shift** — たまに報酬率が大きく変わる（AT 突入っぽい挙動）
5. **recent losses 記憶** — loss-chasing 行動の判断材料

**捨てるもの**: 設定判別の細密化、実機固有演出、法的払出率の忠実再現、確率収束の長期検証、筐体 UI

変数名は意味的にする（`stress_index=0.83` であって `[0.83]` ではない）。
「定量 only」は無名ベクトルではない。

### Step 6: 2×2 実験条件で pilot 【〜5/01】
4条件:
- 低ストレス × cue なし
- 低ストレス × cue あり
- 高ストレス × cue なし
- **高ストレス × cue あり**（仮説的に最も覚醒が出るはず）

測定アウトカム:
- `continue` / `quit` の比率
- 賭け額の escalation
- 直近損失後の追いかけ率
- `message` 内の覚醒語彙の自然発生頻度

**ゲート: 4/29 までにパチスロ環境最小版 + 2×2 pilot ログ**

### Step 7: Full run → 動画 → 解説文 【〜5/07】
- [ ] 20 agents × 100 steps の full run（仕上げ用に 30B-A3B も1回）
- [ ] `visualization/generate_video.py` で MP4 生成
- [ ] 解説文執筆（README 更新 or 別ドキュメント）
- [ ] GitHub push（private → 提出前に public）

**ゲート: 5/02 までに図1枚 + 代表ログ + 主張1本**

## 撤退ゲート（日付つき）

未達時の縮退先を明確化しておく。

| 期日 | 通過条件 | 未達時の縮退 |
|------|---------|-------------|
| 2026-04-21 | stock demo を 4B/14B で動作 | `action` をルール化、`message` だけ LLM |
| 2026-04-25 | 20ag × 20step pilot を許容時間で | message 長縮小・thinking 切る・LLM呼出頻度削減 |
| 2026-04-29 | パチスロ環境最小版 + 2×2 pilot ログ | 少数 agent のケーススタディへ縮退 |
| 2026-05-02 | 図1枚 + 代表ログ + 主張1本 | 動画/UI 削って結果解釈に全振り |

### 縮退ルート（守るべきは message 側）
1. **LLM は `message` のみ、`action` はルールベース**
2. **LLM は salient event 時のみ**（大負け・near-miss・大逆転 cue の瞬間）
3. **全ルールベース、最後に LLM でログ解釈だけ**

仮説の本丸は「内面言語の創発」なので、`message` 側は最後まで守る。`action` を先に捨てる。

## ハマり罠チェックリスト（初期に必読）

| # | 罠 | 対策 |
|---|----|------|
| 1 | thinking 切り忘れ | Qwen3: `think=false` / gpt-oss: `low`/`med`/`high` のみ（bool 無視） |
| 2 | thinking 痕跡を履歴に再投入 | ログ保存時に thought block を捨てる前処理 |
| 3 | context 積みすぎ | 既定 4096。並列で `NUM_PARALLEL * CONTEXT_LENGTH` 比例で RAM 増 |
| 4 | model unload 時間ロス | `keep_alive=-1` で preload 維持（既定 5分で unload） |
| 5 | 出力長が無制限 | `num_predict` を小さく縛る（既定 -1） |
| 6 | CPU fallback | `ollama ps` の `PROCESSOR=100% GPU` を確認 |
| 7 | 並列叩きすぎで 503 | `OLLAMA_MAX_QUEUE` 調整、`~/.ollama/logs/server.log` 確認 |
| 8 | 定量 only ≠ 無名ベクトル | 変数名は意味的に（`stress_index=0.83` 形式） |

## 運用ルール

### 自律実行
- 作業ジャーナル更新、git commit、ドキュメント整理は確認なしで実行
- 破壊的操作（`reference/` の改変、大規模な設計変更）はユーザーに確認
- 迷ったら最善と思う方で進める

### コミット
- コミットメッセージは calchan:/CLAUDE.md の規約に従う
- `reference/` は基本的に touch しない（改変するなら別ディレクトリにコピーしてから）

### GitHub
- 提出段階で GitHub に push する前提
- private で開始し、提出前に public に切り替える

### ログ
- 作業記録は calchan: 直下の `memory/work-journal.md` に追記
- ハマりは `memory/gotchas.md` へ

## 関連リンク
- ハッカソン配布デモ: `reference/`
- ChatGPT Pro 相談プロンプト: `docs/相談プロンプト.md`
- ChatGPT Pro 回答（元ソース）: `docs/chatgpt-response.md`
- 子ノート: `$OBSIDIAN_VAULT/100_Notes/1.2026年/singulabo-hackathon.md`
