# ChatGPT Pro 回答 v4.2 → v4.3（変数優先度の洗い出しレビュー、2026-04-30）

相談プロンプト: [docs/相談プロンプト-v4-2.md](相談プロンプト-v4-2.md)

---

まず「動画で刺さる質感」と「仮説検証の土台」を分け、仕様由来か集計由来かを切り分けます。そのうえで8日で回せる最小の5変数と実装順に絞ります。

特に新しく足すなら、実機確率の忠実再現ではなく100 step内で物語が出る校正値として、イベント意味と頻度を設計する視点です。

Thought for 7m 25s

結論から言うと、v4.3 は C 推しです。

ただし「ストレス × 大逆転認知を証明しにいく」ではなく、v4.2 で見えた観察結果を、よりフェアな計測条件で再確認する位置づけが一番強いです。

今の歪みは、変数不足というより、

hit / chain_start / 上乗せ / 特化 / 確定演出 が、心理的には別物なのに、モデル上は近すぎる

のが本丸です。

なので v4.3 の方針はこれです。

「当たりの物理」・「イベントの意味」・「動画で見せるハイライト」を分離する。

## 1. 3.1〜3.6 の歪み判定

| 論点 | 判定 | 理由 | v4.3 での扱い |
|------|------|------|--------------|
| 3.1 機種別ボーナス興奮度差がない | 修正必要 | GOD 初当たり、爆裂ART突入、ジャグラーのペカを同列にすると、実機経験者の直感とズレる。 | bonus_excitement_multiplier 導入。ただし 全 hit ではなく chain_start 限定で効かせる。 |
| 3.2 上乗せ・特化の軽重がない | 修正必要 | 「50G乗せ」と「500G乗せ」が同じカテゴリだと、レアイベントの感動が死ぬ。 | uwanose_light/heavy, tokka_light/heavy, kakutei_engi に分ける。 |
| 3.3 stress_load 固定 | 修正必要・最重要 | 「今日の追い詰められ方」が動かないので、仮説検証の土台が弱い。 | baseline_stress + situational_stress の2層にする。 |
| 3.4 sensory_gating の命名と効果が逆 | 修正必要だが軽作業 | gating なのに増幅。説明時に突っ込まれる。 | 最低限 sensory_amplitude に改名。余力で dopamine_sensitivity 分離。 |
| 3.5 Top 5 が物語を作れない | 修正必要 | raw Top 5 は頻度バイアスで chain_start に寄る。動画には不向き。 | raw_top5 と stratified_highlights を分ける。 |
| 3.6 ユーザー自身を投影できない | 別解あり | 刺さるが、モデル改善より優先すると危険。 | フル UI ではなく、Day7 以降に self_persona.yaml だけ作るのが妥当。 |

## 2. Q1-Q8 への直接回答

### Q1. 機種別 bonus_excitement_multiplier は妥当？

妥当。ただし `hit_signal * mt.bonus_excitement_multiplier` は危険です。

理由は、hit_signal が「通常の小当たり・連荘中の当たり・初当たり」を全部含むと、ART中の細かい当たりまで GOD 級に膨らむからです。

おすすめはこれです。

```python
chain_just_started = trigger_event == "chain_start"

if chain_just_started:
    hit_body_arousal = 22.0 * mt.bonus_excitement_multiplier
elif hit:
    hit_body_arousal = 12.0 * mt.continuation_excitement_multiplier
else:
    hit_body_arousal = 0.0
```

そして、大逆転認知側は別で持つ。

```python
event_impact = mt.chain_start_impact  # chain_start 時のみ
dopamine_burst = (
    35.0
    * event_impact
    * (0.5 + 1.5 * pre_event_stress_load)
    * dopamine_sensitivity
)
```

つまり、

- bonus_excitement_multiplier = 光った / 入った / 神が降りた、という身体反応
- chain_start_impact = ここから逆転できるかも、という意味づけ
- stress_load = それがどれだけ救済として刺さるか

に分ける。

ここを分けると、説明がかなり強くなります。

### Q2. 上乗せ・特化ゾーンの二相構造は妥当？

妥当。むしろ v4.3 の主役級です。

ただし、提案の kakutei_engi weight 3.0 は、現行の

```
35.0 * upset_recognition * (0.5 + 1.5 * stress_load)
```

と組み合わせると、簡単に arousal 100 に張り付きます。

なので、やるなら次のどちらか。

**案A：現行式を維持するなら、重みは最大 1.6 前後に抑える**

おすすめ。

```
uwanose_light  = 0.35 - 0.45
uwanose_heavy  = 0.90 - 1.15
tokka_light    = 0.55 - 0.70
tokka_heavy    = 1.10 - 1.45
kakutei_engi   = 1.20 - 1.65
```

**案B：重み 2.0〜3.0 を使いたいなら、burst 側を飽和関数にする**

```python
dopamine_burst = (
    45.0
    * (1.0 - exp(-event_impact))
    * (0.55 + 1.15 * stress_load)
    * dopamine_sensitivity
)
```

ハッカソンでは **案A 推奨**です。理由は、既存コードの変更が少ないから。

### Q3. stress_load 動的更新式は妥当？

方向性は妥当です。ただし、stress_load を直接上下させるより、baseline と situational を分ける方が安全です。

おすすめはこれ。

```python
baseline_stress = clip(
    0.30 * persona.base_stress
    + 0.30 * persona.borrow_burden
    + 0.20 * persona.work_stress
    + 0.20 * persona.life_dissatisfaction,
    0.0,
    1.0,
)

# session 内で動く部分
situational_stress = 0.0
stress_load = baseline_stress
```

各 step 後に更新。

```python
loss_delta_signal = tanh(max(0, -net_delta) / 3000.0)
gain_signal = tanh(max(0, net_delta) / 5000.0)

loss_ratio = max(0.0, (initial_cash - cash) / max(initial_cash, 1))
deep_loss_signal = max(0.0, loss_ratio - 0.30) / 0.70

miss_streak_signal = 1.0 - exp(-miss_streak / mt.stress_hammari_tau)

cash_low_signal = sigmoid((mt.cash_low_threshold - cash) / 2500.0)

time_pressure_signal = sigmoid(
    (step - persona.target_leave_step + 8) / 4.0
)

chain_just_started = trigger_event == "chain_start"
heavy_positive_event = trigger_event in {
    "uwanose_heavy",
    "tokka_heavy",
    "kakutei_engi",
}

delta_situational_stress = (
    + 0.010 * loss_delta_signal
    + 0.012 * deep_loss_signal
    + 0.012 * miss_streak_signal * (1.0 - chain_active)
    + 0.025 * cash_low_signal
    + 0.025 * time_pressure_signal * (1.0 - chain_active)
    + 0.012 * time_pressure_signal * chain_active * mt.torikirezu_anxiety
    - 0.060 * float(chain_just_started)
    - 0.030 * gain_signal
    - 0.020 * float(heavy_positive_event)
)

situational_stress = clip(
    0.92 * situational_stress + delta_situational_stress,
    -0.12,
    0.65,
)

stress_load = clip(
    baseline_stress + situational_stress,
    0.0,
    1.0,
)
```

**重要なのは、arousal 爆発には pre_event_stress_load を使うことです。**

```python
pre_event_stress_load = stress_load

# 先に arousal を更新
# その後に stress_load を更新
```

ボーナス当選で stress が下がるのは自然ですが、当選した瞬間の脳汁は「当たる直前の追い詰められ度」で決まるはずです。ここを逆にすると、当たった瞬間に stress が下がって、爆発が弱まるという変なことが起きます。

### Q4. sensory_gating は A/B/C どれ？

**B 推し。ただし B-lite で十分です。**

フル分離すると、

- sensory_amplitude
- dopamine_sensitivity
- dissociation_gating

の3つになります。

でも残り8日なので、最低限はこれ。

```python
# 旧 sensory_gating_factor
persona.sensory_amplitude
```

そして、爆発項だけに効く派生値を作る。

```python
dopamine_sensitivity = clip(
    0.75 + 0.45 * persona.sensory_amplitude,
    0.70,
    1.25,
)
```

通常の arousal には穏やかに効かせる。

```python
background_amplitude = 0.85 + 0.30 * persona.sensory_amplitude
```

大逆転イベントには強めに効かせる。

```python
dopamine_burst *= dopamine_sensitivity
```

解離が強いと、全体反応は抑える。

```python
dissociation_gate = 1.0 - 0.35 * (dissociation / 100.0)
delta_arousal *= dissociation_gate
```

これで、

- 感覚鋭敏さそのものが強い
- さらに、レアイベントに対する dopamine 感受性としても効く
- ただし解離が強いと反応が鈍る

という説明ができます。

C の削除はおすすめしません。v4.2 で「感覚の鋭敏さ × 入り口イベント」が見えているなら、そこは捨てずに整理する方が良いです。

### Q5. Top 5 抽出を trigger 種別ごとに分散させるべき？

**分散させるべきです。ただし raw Top 5 も残す。**

ここは研究誠実性と動画映えを両立できます。

```
raw_top5:
  arousal_delta 降順の純粋 Top 5。
  chain_start に偏ってもそのまま出す。

stratified_highlights:
  動画用の代表シーン。
  trigger 種別ごとに最大1件ずつ拾う。
```

提出文ではこう書くのが安全です。

> 純粋な arousal_delta Top 5 は chain_start に偏った。これは頻度の高い入口イベントが最大値抽出を支配することを示している。
> 一方、動画では心理的に異なる瞬間を比較するため、trigger 種別ごとの代表ハイライトを提示した。

これは不純ではなく、分析目的が違うだけです。

おすすめの bucket はこれ。

```python
highlight_buckets = [
    "kakutei_engi",
    "tokka_heavy",
    "uwanose_heavy",
    "long_chain",
    "chain_start",
]
```

long_chain は trigger ではなく派生イベントで良いです。

```python
long_chain = (
    machine.chain_active
    and (
        win_streak >= mt.long_chain_threshold
        or current_chain_payout >= mt.long_chain_payout_threshold
    )
)
```

### Q6. ユーザー自身を投影する spike は作るべき？

**フル実装に1日使うのは危険。config だけなら作る価値あり。**

おすすめは UI ではなくこれ。

```yaml
self_persona:
  base_stress: 0.72
  borrow_burden: 0.10
  work_stress: 0.65
  life_dissatisfaction: 0.45
  initial_cash: 30000
  target_machine_type: GOD_OKI
  target_leave_step: 85
```

CLI もこれくらいで十分。

```bash
python run_simulation.py --persona self_persona.yaml --machine GOD_OKI --seed 42
```

ハッカソン動画では、

> 32 persona の集合実験に加えて、自分の今日のストレスを入れるとハイライトが変わる

と言える。これは刺さります。

ただし、優先順位は **Day7 以降の余力枠**です。モデル本体が不安定な状態でここに1日使うのは危ないです。

### Q7. 最低限詰める変数 5 個

提出勝ち筋込みなら、この5個を推します。

| 優先 | 変数 / 機能 | 理由 | 工数 |
|------|------------|------|------|
| 1 | stress_load 動的更新 | 仮説検証の土台。これがないと「今日追い詰められている」が表現できない。 | 半日〜1日 |
| 2 | 上乗せ・特化の light / heavy 二相構造 | 動画で一番効く。レアイベントの感動が出る。 | 1日 |
| 3 | 機種別 bonus_excitement_multiplier | 実機経験者の違和感を最短で潰せる。 | 半日 |
| 4 | Top 5 trigger 分散抽出 | 動画が単調になるのを防ぐ。研究的にも raw と stratified を分ければ誠実。 | 1〜2時間 |
| 5 | ハイライト用 LLM voice 統合 + few-shot 改良 | 2分動画の印象を決める。qwen3:4b でも highlight 5件だけなら安定しやすい。 | 半日 |

ただし、sensory_gating の改名は **5枠に入れずに Day1 で同梱**してください。1時間で済むし、説明事故を防げます。

切る / 後回しはこれ。

| 候補 | 判断 |
|------|------|
| プレイヤー視点 spike | Day7 以降の余力。config だけなら可。 |
| sensory_gating の本格分離 | B-lite で十分。完全な新属性設計は不要。 |
| Phase 2 ハイライト統合だけ | LLM voice とセットでやる。単体だと弱い。 |
| さらに細かい機種分類 | GOD と沖スロ分離は魅力的だが、残り8日では切る。 |

### Q8. 仮説の扱いは A/B/C どれ？

**C 推しです。**

ただし、言い方はこうです。

> v4.2 では「ストレス × 大逆転認知」仮説は支持されなかった。
> しかし同時に、機種差・イベント軽重・stress_load の動性・Top 5 抽出の頻度バイアスという、計測上の歪みも判明した。
> v4.3 ではそれらを補正し、同じ仮説をよりフェアに再検証した。
> その結果、観察された傾向として「感覚鋭敏さ × 入口イベント」、または「動的 stress × レアイベント」のどちらが強く出るかを比較した。

B の「仮説差し替え」は、後出し感が出ます。

A の「v4.2 のまま失敗を動画化」は、誠実だけど弱いです。なぜなら v4.2 のモデル欠損がはっきり見えているから。

なので、C で再検証して、最終ストーリーは結果に応じて A/B どちらにも着地できる形が良いです。

## 3. bonus_excitement_multiplier 数値表

提案値はこれです。

| machine_type | 質感 | bonus_excitement_multiplier | chain_start_impact | continuation_excitement_multiplier |
|--------------|------|----------------------------|-------------------|------------------------------------|
| PURE_A | ジャグラー / 純A。軽い、頻発、「あ、入った」 | 0.65 | 0.20 | 0.55 |
| ART_45 | 4.5号機 ART。初当たりに期待感あり | 1.00 | 0.35 | 0.70 |
| ART_2010 | 2010s 爆裂 ART。突入したら伸びる期待 | 1.35 | 0.52 | 0.75 |
| GOD_OKI | GOD / 沖スロ系。稀・重い・神降臨 | 2.20 | 0.75 | 0.65 |

ユーザー案の「純A 0.5 / 4.5号機 1.0 / 2010s ART 1.5 / GOD 2.5」は方向性としてかなり良いです。

ただし、現行の `35.0 * upset_recognition` があるので、GOD 2.5 はややクリップしやすい。最初は 2.2 くらいが安全です。

どうしても GOD の神感を強めたいなら、bonus_excitement_multiplier を上げるより、chain_start_impact を 0.75 → 0.85 に上げる方が説明しやすいです。

## 4. 上乗せ・特化の確率と重み設計表

**前提として、この確率は実機確率ではなく、100 step シミュレーション内で質感を出すための抽象確率です。**

p は eligible step あたりの発生確率にしてください。

- uwanose_* と tokka_* は基本 chain_active == True のときだけ eligible
- kakutei_engi は機種によって any step でも可
- 純Aは基本なし。プレミア告知だけ極低確率で許可

| trigger_event | PURE_A p / impact | ART_45 p / impact | ART_2010 p / impact | GOD_OKI p / impact |
|---------------|-------------------|-------------------|---------------------|--------------------|
| uwanose_light | 0.000 / — | 0.025 / 0.35 | 0.045 / 0.42 | 0.015 / 0.35 |
| uwanose_heavy | 0.000 / — | 0.002 / 0.90 | 0.006 / 1.05 | 0.005 / 1.15 |
| tokka_light | 0.000 / — | 0.010 / 0.55 | 0.030 / 0.65 | 0.008 / 0.60 |
| tokka_heavy | 0.000 / — | 0.0008 / 1.10 | 0.003 / 1.25 | 0.004 / 1.45 |
| kakutei_engi | 0.0003 / 0.65 | 0.0004 / 1.20 | 0.0009 / 1.45 | 0.0012 / 1.65 |

この表の狙いはこうです。

- 純Aは「単発の入り口」が主役
- 4.5号機は軽い上乗せがそこそこ、重い特化は希少
- 2010s ART は light/heavy の両方が見える
- GOD_OKI は頻度は低いが、入ったときの重さが最大

もう1つ重要なのは、**重いイベントは物理にも影響させる**ことです。

ログ上で「500G上乗せ！」と出たのに次 step で通常落ちすると、動画で一気に嘘っぽくなります。

最低限これを入れると良いです。

```python
if trigger_event == "uwanose_light":
    machine.chain_stock += rng.choice([1, 2, 3])

elif trigger_event == "uwanose_heavy":
    machine.chain_stock += rng.choice([5, 7, 10])

elif trigger_event == "tokka_light":
    machine.tokka_boost_steps += rng.choice([2, 3, 4])

elif trigger_event == "tokka_heavy":
    machine.chain_stock += rng.choice([8, 12, 15])
    machine.tokka_boost_steps += rng.choice([4, 6])

elif trigger_event == "kakutei_engi":
    machine.chain_stock += rng.choice([10, 15, 20])
    machine.force_next_hit = True
```

production code ではなく spike なら、これくらいの抽象で十分です。

## 5. stress_load 動的更新式の最終案

最終案はこの形です。

```python
def update_stress_load(
    persona,
    mt,
    state,
    trigger_event,
    net_delta,
    step,
):
    """
    state:
      cash
      initial_cash
      miss_streak
      chain_active
      situational_stress
      stress_load
    """

    pre_event_stress_load = state.stress_load

    loss_delta_signal = tanh(max(0, -net_delta) / 3000.0)
    gain_signal = tanh(max(0, net_delta) / 5000.0)

    loss_ratio = max(
        0.0,
        (state.initial_cash - state.cash) / max(state.initial_cash, 1)
    )

    deep_loss_signal = clip(
        (loss_ratio - 0.30) / 0.70,
        0.0,
        1.0,
    )

    miss_streak_signal = 1.0 - exp(
        -state.miss_streak / mt.stress_hammari_tau
    )

    cash_low_signal = sigmoid(
        (mt.cash_low_threshold - state.cash) / 2500.0
    )

    time_pressure_signal = sigmoid(
        (step - persona.target_leave_step + 8) / 4.0
    )

    chain_just_started = trigger_event == "chain_start"

    heavy_positive_event = trigger_event in {
        "uwanose_heavy",
        "tokka_heavy",
        "kakutei_engi",
    }

    torikirezu_pressure = (
        time_pressure_signal
        * float(state.chain_active)
        * mt.torikirezu_anxiety
    )

    delta_situational_stress = (
        + 0.010 * loss_delta_signal
        + 0.012 * deep_loss_signal
        + 0.012 * miss_streak_signal * (1.0 - float(state.chain_active))
        + 0.025 * cash_low_signal
        + 0.025 * time_pressure_signal * (1.0 - float(state.chain_active))
        + 0.012 * torikirezu_pressure
        - 0.060 * float(chain_just_started)
        - 0.030 * gain_signal
        - 0.020 * float(heavy_positive_event)
    )

    state.situational_stress = clip(
        0.92 * state.situational_stress + delta_situational_stress,
        -0.12,
        0.65,
    )

    state.stress_load = clip(
        state.baseline_stress + state.situational_stress,
        0.0,
        1.0,
    )

    return pre_event_stress_load, state.stress_load
```

arousal 側では、必ず pre_event_stress_load を使う。

```python
dopamine_burst = (
    35.0
    * event_impact
    * (0.5 + 1.5 * pre_event_stress_load)
    * dopamine_sensitivity
)
```

**この順番がかなり大事です。**

## 6. 最低限詰める変数 5 個 + Day-by-Day

4/30 開始想定なら、こう切るのが現実的です。

### Day1: 4/30 — v4.3 schema 固定・小変更を全部入れる

やること。

- bonus_excitement_multiplier
- chain_start_impact
- continuation_excitement_multiplier
- sensory_gating_factor → sensory_amplitude
- dopamine_sensitivity 派生値
- trigger_event enum 拡張

この日に欲張って LLM や動画は触らない。

成功条件。

- 32 persona × 100 step が LLM なしで完走
- trigger_event がログに出る
- arousal が 0-100 に収まる

### Day2: 5/1 — light/heavy イベント物理 + stress_load 動的化

やること。

- uwanose_light/heavy
- tokka_light/heavy
- kakutei_engi
- chain_stock
- tokka_boost_steps
- situational_stress
- pre_event_stress_load

成功条件。

- 重いイベント後にすぐ通常落ちしない
- stress_load が 100 step 内で上下する
- 当選直前 stress と当選後 relief がログで見える

### Day3: 5/2 — calibration day

ここは地味だけど超重要です。

見る指標。

- trigger_event 別の発生回数
- trigger_event 別の mean / max arousal_delta
- high stress / low stress の arousal_delta 比
- raw_top5 の trigger 分布
- stratified_highlights の trigger 分布
- arousal 100 張り付き率

張り付き率が高い場合。

- dopamine_burst coefficient を下げる
- event_impact を下げる
- bonus_excitement_multiplier を下げる

成功条件。

- raw_top5 は多少 chain_start に寄ってもよい
- stratified では heavy / tokka / kakutei が拾える
- arousal 100 張り付きが 10% 未満

### Day4: 5/3 — Top 5 分散抽出 + LLM voice

やること。

- raw_top5.json
- stratified_highlights.json
- highlight 5件だけ qwen3:4b に心の声生成
- few-shot を2〜3個入れる

LLM prompt は数値と trigger だけ渡す。

```json
{
  "persona_category": "退職前男性",
  "machine_type": "GOD_OKI",
  "trigger_event": "tokka_heavy",
  "cash": 7000,
  "initial_cash": 30000,
  "stress_load": 0.82,
  "arousal_delta": 47.2,
  "despair": 68.5,
  "miss_streak": 14,
  "instruction": "20字から45字の内面独白を1つだけ返す"
}
```

成功条件。

- 5 highlight それぞれに短い心の声が付く
- JSON崩れしても fallback 文がある

### Day5: 5/4 — 本番 run 複数 seed

やること。

- seed 5〜10本
- 32 persona × 100 step
- raw / stratified 両方保存
- 最終動画に使う seed を選ぶ

ここで新機能追加は禁止に近い運用にする。

成功条件。

- 提出に使える seed が1本以上ある
- 集計図が3枚以上ある
- 動画素材が揃う

### Day6: 5/5 — 動画構成

2分動画ならこの構成が強いです。

```
0:00-0:15  問い: 人はなぜ当たりの瞬間に壊れるのか
0:15-0:35  v4.2結果: Top5がchain_startに偏った
0:35-0:55  v4.3補正: 機種差・レアイベント・動的stress
0:55-1:35  5つの代表ハイライト
1:35-1:50  観察結果: stressだけではなく、sensory × event entrance が強い
1:50-2:00  限界と次: 実機再現ではなく心理シミュレーション
```

### Day7: 5/6 — PDF / README / package

やること。

- 解説 PDF
- README
- 実行コマンド
- 代表ログ
- 動画最終書き出し

余力があれば self_persona.yaml を追加。

### Day8: 5/7 — 提出日

新機能追加禁止。

やること。

- 実行確認
- 動画再生確認
- zip / repo 整理
- 解説文の誤字修正

## 7. 見落としている観点 / v4.3 で踏みそうな罠

### 罠1. hit と chain_start を混ぜるとまた壊れる

GOD 初当たりと、連荘中の細かい hit は別物です。

ログには最低限これを分けてください。

```json
{
  "hit": true,
  "trigger_event": "chain_start",
  "chain_just_started": true,
  "chain_active": true,
  "chain_stock": 8
}
```

### 罠2. arousal 100 クリップで差が消える

重みを盛ると、全部 100 になります。

保存すべき値は3つ。

- raw_arousal_delta
- clipped_arousal_delta
- arousal_after

ランキングは raw_arousal_delta で見る。動画表示は arousal_after で良いです。

### 罠3. stress relief の更新順で仮説が死ぬ

当選した瞬間に stress を先に下げると、

> 追い詰められていたから脳汁が出た

が表現できません。

順番は必ずこれ。

```
1. pre_event_stress_load を保存
2. event / arousal 更新
3. stress_load を relief 込みで更新
```

### 罠4. rare event が rare すぎて動画に出ない

p=0.001 は 3200 step で期待 3.2 件ですが、eligible step 限定だと 1件未満になる可能性があります。

対策。

- 統計用: 複数 seed 集計
- 動画用: 代表 seed を選ぶ

これはズルではないです。動画は「代表例の提示」なので、集計結果と分ければOKです。

### 罠5. 上乗せイベントが物理に効かないと嘘っぽい

uwanose_heavy が出たのに次 step で通常落ちしたら、実機経験者は即違和感を持ちます。

最低限 chain_stock を入れるべきです。

### 罠6. Top 5 分散を「Top 5」と呼ぶと研究的に危ない

呼び名を分けてください。

- raw_top5 = 客観的最大値
- stratified_highlights = 動画用の代表シーン

この名前だけでだいぶ守れます。

### 罠7. GOD_OKI が広すぎる

本当は、

- 沖スロ
- GOD
- 荒波AT

は分けたいです。

でも残り8日では切っていいです。代わりに説明文で、

> GOD_OKI は「稀で重い入口イベントを持つ荒波系」の抽象カテゴリ

と書く。

### 罠8. LLM voice が説明しすぎる

心の声は、分析コメントにしない方がいいです。

悪い例。

> 私は現在stress_loadが0.82なので強い報酬予測誤差を感じている。

良い例。

> これ、今日の負け全部ひっくり返せるやつだろ。

qwen3:4b には、**短く、口語、1文だけ、数値を言わない**、と明示するのが安全です。

## 最終推奨

v4.3 の核はこの5つで十分です。

```
1. stress_load 動的化
2. 機種別 bonus_excitement_multiplier
3. 上乗せ・特化 light/heavy
4. raw_top5 / stratified_highlights 分離
5. highlight LLM voice
```

sensory_gating は、

- sensory_gating_factor → sensory_amplitude
- dopamine_sensitivity は派生値

として **Day1 に無料修正扱い**で入れる。

提出ストーリーはこれが一番強いです。

> v4.2 では仮説は外れた。
> ただし、その失敗から「機種差」「イベント軽重」「stress の動性」「Top5抽出バイアス」という歪みが見えた。
> v4.3 ではそれらを補正し、 raw な最大値と、心理的に異なる代表シーンを分けて観察した。
> 結果として、人の脳汁ピークは単なるストレス量だけでなく、感覚鋭敏さ・機種の意味・入口イベントの重さが絡んで立ち上がることが見えた。

これ、かなりハッカソン向きです。
失敗を隠さず、でも失敗で終わらせず、**「観察によってモデルが賢くなった」**という流れになっています。
