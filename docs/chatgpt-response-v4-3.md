# ChatGPT Pro 回答 v4.3 → v4.4（属性パターン × 定性まとめ × 仮説の答え合わせ、2026-05-01）

> 投げたプロンプト: `docs/相談プロンプト-v4-3.md`
> 添付: CLAUDE.md / spike_v43.py / chatgpt-response-v4-2.md / R1-R3-aggregation.md

---

## 1. v4.4 方向転換の総評

**採用でいいです。かなり良い方向転換です。**
理由は、v4.3 までの「仮説検証 → 外れたらどうする？」という弱点を、v4.4 では **観察型の群比較** と **当事者仮説の答え合わせ** に分離できているからです。

v4.3 時点でも、設計の核は「当たりの物理 / イベントの意味 / 動画ハイライト」を分離することでした。さらに `stress_load` 動的化、light/heavy イベント、raw_top5 と動画用 highlight の分離、LLM voice 統合が重要課題として整理されています。v4.4 はこの流れを壊さず、「誰の何を観察する動画なのか」を一段クリアにしています。

**強みは3つ。**

1つ目は、**1000人均等配分が動画向き**なこと。リアルなホール分布を再現しにいくと、視聴者は「人数比の結果なのか、心理パターンの結果なのか」を見失います。今回は「8属性を同じ条件で比べる実験」と割り切るほうが強いです。

2つ目は、**仮説が外れても成立する構造**になったこと。Phase 4-5 で8属性の傾向を先に見せ、Phase 6 で「では自分の仮説は？」と締める流れなら、仮説が完全支持されなくても「答え合わせ」になります。

3つ目は、**表現を丸めたことで提出物として安全になった**こと。169 cards の元カテゴリには依存症末期、精神疾患併発、風俗・夜職などかなり生々しいカテゴリが含まれていましたが、v4.4 の8属性は心理パターンに抽象化されています。元データは11カテゴリ・169カードで、不労所得・地主層26、依存症末期17、精神疾患併発16などの分布でした。

**リスクもあります。**

一番大きいのは、**仮説を数式に入れすぎると、答え合わせが自己成就に見える**ことです。現行 v4.3 の `update_emotions` では、`dopamine_burst = event_impact × stress_load × dopamine_sensitivity` という形で、すでに「ストレス × 兆し」が脳汁に効く構造になっています。
なので Phase 6 では「現実の証明」ではなく、**この抽象モデル上で、自分の仮説がどの程度再現されたか**と表現するのが安全です。

もう1つは、**despair を完全に消すと低A高Dの人が消える**こと。169 cards の4象限では、低A高D、つまり反応は鈍いが苦しさは高い層が16枚、全体の9.5%ありました。完全削除ではなく、画面には出さず内部で「反応鈍化」「ストレス床」として残すのがよいです。

結論としてはこうです。

> **v4.4 は採用。**
> ただし、「検証」ではなく **モデル内の観察と答え合わせ** と言う。
> そして `despair` は画面から消しても、内部には「ストレスの床」「反応鈍化」として残す。

---

## 2. Q1: ストレス動的化式の最終案

### 判断

`tanh` は妥当です。プロスペクト理論っぽいS字をそのまま入れるより、**損失ストレスは単調増加・飽和型**で十分です。

ユーザーの言っている、

> 10万円まではめちゃくちゃ痛い。でも一定ラインを超えると10万も20万も変わらない

これは「価値関数のS字」より、**ストレス反応の飽和**として扱うほうが実装も説明もきれいです。

なので基本はこれです。

```python
loss_pressure = tanh(loss_over_safe_budget / personal_threshold)
```

`personal_threshold` は **属性ごとの固定中央値 + 個人差揺らぎ** がよいです。
初期所持金のN%だけで決めると、C. 中毒型の「財布は薄いが、使ってはいけない金にアクセスする」感じが消えます。

### 推奨設計

内部は `0.0〜1.0`、画面表示だけ `0〜100` に変換します。

重要なのは、ストレスを2層にすることです。

```text
base_stress      = その人の慢性的なストレス傾向
situational      = 今日の負け・ハマり・残金・時間圧で動くストレス
stress_load      = base_stress + situational
pre_event_stress = 脳汁更新に使う、イベント直前のストレス
post_event_stress = 当たり・回復後に更新されたストレス
```

**脳汁爆発には必ず `pre_event_stress` を使う。**
ここを間違えると、当たりで先にストレスが下がり、爆発が弱くなるという変な挙動になります。

### 最終擬似コード

```python
from math import exp, tanh

def clip(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))

def sigmoid(x):
    return 1.0 / (1.0 + exp(-x))

def sat_exp(x, tau):
    """0から立ち上がって1に飽和する信号"""
    return 1.0 - exp(-max(0.0, x) / max(tau, 1e-6))


def compute_stress_dynamic(persona, session, t, history):
    """
    内部 stress は 0.0〜1.0。
    画面表示時だけ stress_100 = round(stress * 100)。
    """

    pre_event_stress = clip(history.stress_load)

    net_loss_from_start = max(
        0.0,
        history.initial_cash + history.accessible_used - history.cash
    )

    loss_over_safe_budget = max(
        0.0,
        net_loss_from_start - persona.safe_loss_budget
    )

    loss_pressure = tanh(
        loss_over_safe_budget / max(persona.personal_threshold, 1.0)
    )

    hammari_pressure = sat_exp(history.miss_streak, persona.hammari_tau)

    cash_low_signal = sigmoid(
        (persona.cash_floor - history.cash) / persona.cash_low_scale
    )

    time_pressure_signal = (
        persona.time_pressure
        * sigmoid((t - persona.target_leave_step + 6) / 3.5)
    )

    if history.chain_active:
        low_stock_anxiety = sigmoid((2.0 - history.chain_stock) / 1.5)
        torikirezu_anxiety = (
            time_pressure_signal
            * persona.torikirezu_sensitivity
        )
        chain_anxiety = 0.50 * low_stock_anxiety + 0.50 * torikirezu_anxiety
    else:
        chain_anxiety = 0.0

    recovery_from_bottom = max(
        0.0,
        history.cash - history.lowest_cash_recent
    )
    recovery_signal = tanh(
        recovery_from_bottom / max(persona.personal_threshold, 1.0)
    )
    recovery_signal *= (1.0 - 0.35 * chain_anxiety)

    trigger = history.last_trigger_event
    heavy_positive_event = trigger in {
        "kakutei_engi", "tokka_heavy", "uwanose_heavy",
    }
    chain_start = trigger == "chain_start"

    event_relief = (
        0.08 * float(chain_start)
        + 0.06 * float(heavy_positive_event)
    )

    stress_target = (
        persona.base_stress
        + 0.42 * loss_pressure
        + 0.16 * hammari_pressure * (1.0 - float(history.chain_active))
        + 0.18 * cash_low_signal
        + 0.10 * time_pressure_signal * (1.0 - float(history.chain_active))
        + 0.08 * chain_anxiety
        - 0.22 * recovery_signal
        - event_relief
    )

    stress_next = (
        0.72 * pre_event_stress
        + 0.28 * clip(stress_target)
    )

    stress_next = max(persona.stress_floor, stress_next)

    return clip(pre_event_stress), clip(stress_next)
```

### 係数の意味

* `loss_pressure 0.42`: 一番強い。負け額の心理的痛み。
* `hammari 0.16`: ハマりは効くが、損失ほどではない。
* `cash_low 0.18`: 残金が薄い時の圧。
* `time_pressure 0.10`: D/G向け。Cにも効くが主役ではない。
* `chain_anxiety 0.08`: 連チャン中の「終わるかも」「取りきれないかも」。
* `recovery -0.22`: 勝ち戻しで下がる。ただし連チャン不安があると下がり切らない。
* `event_relief -0.06〜-0.08`: 当たり・重い兆しによる一時的な救済。

### 候補式への回答

元の式：

```python
stress(t) = base_stress
          + 0.7 × tanh(loss_from_baseline / personal_threshold)
          + 0.2 × (hammari_streak / 20)
          - 0.3 × win_recovery_signal
```

方向性はOKですが、修正するならこうです。

```python
stress = base_stress
       + 0.42 * tanh(loss_over_safe_budget / personal_threshold)
       + 0.16 * (1 - exp(-hammari_streak / hammari_tau))
       + 0.18 * cash_low_signal
       - 0.22 * recovery_signal
```

`hammari_streak / 20` はやや雑です。**指数飽和**のほうがいいです。

---

## 3. Q2: 幸福度定義の推奨

### 結論

**A/B/C の中なら C 推奨。** ただし、Cをそのまま使うのではなく、係数を調整した **C改** にしてください。

A `脳汁 - ストレス` はシンプルですが、C. 中毒型の「追い詰められているからこそ爆発が気持ちいい」が潰れます。

B `脳汁 - 0.5 * ストレス` は画面表示用の「今の気分スコア」としては使えます。でもランキング抽出に使うと、属性の個性が弱いです。

C `脳汁 + ストレス急減` が一番物語になります。ただし、`×5` は強すぎる可能性があります。ストレスを0〜100表示にするなら、係数は `0.8〜1.3` くらいから始めるのが安全です。

### 推奨式

「最高幸福」は、単なる幸福ではなく **報酬の跳ね上がり + 解放感** と定義します。

```python
brain_after = arousal_after              # 0〜100
brain_delta = arousal_after - arousal_before
stress_drop = max(0, pre_stress - post_stress) * 100
event_bonus = min(1.0, event_impact) * 8

joy_score = (
    0.65 * brain_delta
  + 0.25 * brain_after
  + 0.90 * stress_drop
  + event_bonus
  - 0.10 * pre_stress * 100
)
```

ポイントは、**高ストレスを強く罰しない**ことです。
高ストレスを強く引くと、C型がランキングに出にくくなります。

動画上の説明はこれで十分です。

> 最高幸福 = 脳汁の跳ね上がり + ストレスからの解放感

### 抽出基準

| 用途                | 指標                                  |
| ----------------- | ----------------------------------- |
| Phase 4 最高幸福ランキング | `max(joy_score)`                    |
| Phase 5 最不幸ランキング  | `max(misery_score)`                 |
| Phase 6 仮説答え合わせ   | `max(Δ脳汁)` と `pre_event_stress` の関係 |

Phase 4 と Phase 6 で基準を分けるのが重要です。
Phase 4 は動画として刺さる「体験の山」を見せる。
Phase 6 は仮説に対してフェアに、`Δ脳汁` を見る。

### 最不幸の定義

`ストレス - 脳汁` だけだと弱いです。残金、ハマり、ストレス上昇を少し足したほうが、シーンとして立ちます。

```python
brain_after = arousal_after
stress_after = post_stress * 100
stress_rise = max(0, post_stress - pre_stress) * 100
loss_pressure_100 = loss_pressure * 100
hammari_pressure_100 = hammari_pressure * 100

misery_score = (
    0.65 * stress_after
  + 0.35 * stress_rise
  + 0.20 * (100 - brain_after)
  + 0.20 * loss_pressure_100
  + 0.10 * hammari_pressure_100
  + 8.0 * cash_low_signal
)
```

画面上は、

> 最不幸 = ストレス最大 + 脳汁低下 + 負け/ハマり

くらいに丸めればOKです。

---

## 4. Q3: 8属性パラメータレンジの修正提案

### 総評

今のレンジで大枠は立ちます。ただし、**E. 悠々自適 vs H. パチプロ** と **B. 常連 vs C. 中毒** は、このままだと少し近いです。

特に H. パチプロは、単に `sens低 / stress低 / threshold高` にすると E と同じ「凪の人」になります。
H は **感情が弱い人** ではなく、**期待値評価で感情を抑える人** として別軸を持たせたほうがいいです。

### 修正版テーブル

| #          |   属性 | sens 平均 | base_stress | threshold 中央値 | stress_floor |         hammari_tau | 追加軸 |
| ---------- | ---: | ------: | ----------: | ------------: | -----------: | ------------------: | --- |
| A 新人       | 0.84 |    0.20 |      30,000 |          0.03 |           18 |     novelty_boost 高 |     |
| B 常連       | 0.52 |    0.50 |      60,000 |          0.18 |           14 |       habituation 高 |     |
| C 追い上げ/中毒  | 0.92 |    0.78 |      15,000 |          0.48 |            8 | recovery快感 高、path 高 |     |
| D アフターファイブ | 0.72 |    0.45 |      50,000 |          0.12 |           12 |     time_pressure 高 |     |
| E 悠々自適     | 0.35 |    0.08 |     220,000 |          0.00 |           24 |  interruptibility 高 |     |
| F シニア常連    | 0.42 |    0.34 |      80,000 |          0.10 |           20 |         long_stay 高 |     |
| G 息抜き      | 0.68 |    0.48 |      35,000 |          0.12 |           12 |     relief_weight 高 |     |
| H パチプロ     | 0.25 |    0.22 |     120,000 |          0.08 |           18 |  emotion_damp 高、EV軸 |     |

### B vs C の差

```python
C.stress_floor = 0.48
C.hammari_tau = 8
C.recovery_relief_weight = 1.35
C.dopamine_sensitivity_boost = 1.10
C.personal_threshold = 15000

B.stress_floor = 0.18
B.hammari_tau = 14
B.recovery_relief_weight = 0.85
B.habituation = 0.80
B.personal_threshold = 60000
```

### E vs H の差

Eは「余裕があるから凪」、Hは「判断基準が期待値だから凪」。

```python
E.emotion_damp = 0.85
E.interruptibility = 0.90
E.ev_focus = 0.10

H.emotion_damp = 0.55
H.interruptibility = 0.65
H.ev_focus = 0.95
H.bad_ev_stress = 0.25
```

H は勝っても爆発しない。ただし、期待値の悪い台を打ち続けていると少しストレスが上がる。
これで E と H が別キャラになります。

### 169 cards との対応

低A高Dの「反応が鈍いがストレスは高い」層は、表示名からは消えても内部サブタイプとして残してください。CやBの一部に、

```python
emotion_damp 高
stress_floor 高
dopamine_sensitivity 低め
```

の個体を混ぜると、元データの幅に近づきます。

### 1000人均等配分

**均等配分でOKです。** むしろ今回の目的には均等配分のほうがよいです。

> これはリアルな人口比ではなく、8つの心理パターンを同じ人数で比べる観察実験です。

### 属性内125人の散らし方

潜在変数 z を使った相関つき散らし。

```python
def sample_persona_variant(attr, rng):
    z = rng.normal(0, 1)  # 追い詰められやすさ / のめり込みやすさ

    sens = clip(rng.normal(attr.sens_mean, attr.sens_sd) + 0.03 * z, 0.0, 1.0)
    base_stress = clip(rng.normal(attr.base_stress_mean, attr.base_stress_sd) + 0.06 * z, 0.0, 1.0)
    threshold = attr.threshold_median * exp(attr.threshold_cv * rng.normal(0, 1) - 0.20 * z)
    initial_cash = attr.cash_median * exp(attr.cash_cv * rng.normal(0, 1))
    stress_floor = clip(attr.stress_floor_mean + 0.04 * z, 0.0, 1.0)

    return {
        "sensory_amplitude": sens,
        "base_stress": base_stress,
        "personal_threshold": threshold,
        "initial_cash": int(initial_cash),
        "stress_floor": stress_floor,
    }
```

C型は `z` が高いほど、sens が少し高い、base_stress が高い、threshold が低い、stress_floor が高い、になり、かなり自然にばらけます。

---

## 5. Q4: Phase 4-5 の演出指針

### 同じ persona で最高幸福・最不幸を取るべきか

**原則は違う persona でOK。**
ただし、Cだけは例外的に **同一 persona の前後物語** を作る価値があります。

| 対象            | 抽出                                       |
| ------------- | ---------------------------------------- |
| A/B/D/E/F/G/H | 最高幸福と最不幸は別 persona でOK                   |
| C             | できれば同一 persona の「底 → 兆し → 爆発」を拾う         |
| Cで無理な場合       | 最高幸福personaと最不幸personaを分け、Phase 6で散布図に戻す |

### 16シーンは50秒に収まるか

```text
Phase 4 最高幸福ランキング 25秒
  0-3秒   タイトル + 定義
  3-19秒  8属性カードを2秒ずつ高速表示
  19-25秒 Top 1〜2だけ少し大きく再表示

Phase 5 最不幸ランキング 25秒  （同じ構成）
```

各カードに載せる情報は3つだけ。

```text
属性名
起きたこと: 確定演出 / 上乗せ / 連敗 / 残金低下
数値: 脳汁 +42 / ストレス 88
```

### 画面レイアウト

```text
┌────────────────────────┐
│ C. 追い上げ型           │
│ 兆し: 特化ゾーン heavy   │
│ 脳汁 +58 / ストレス 91  │
│ 「ここで伸びたら戻せる」 │
└────────────────────────┘
```

### LLM voice few-shot

```text
SYSTEM:
あなたは動画字幕用の短い内面独白を書く。
出力は日本語1行だけ。
20〜34字。
句点なし。
数字を直接言わない。
「また」「やばい」「最高」「終わった」を使いすぎない。
医学・借金・依存・病名・家庭事情など生々しい語は禁止。
分析口調は禁止。
属性名をそのまま言わない。
recent_voices と似た言い回しは禁止。

[USER → ASSISTANT 例 5本]
A 新人 chain_start → 「え、これだけで光るんだ」
C 追い上げ tokka_heavy → 「ここで伸びたら全部戻せる」
E 悠々自適 uwanose_heavy → 「今日は少しツイてるな」
H パチプロ chain_start → 「期待値より上、淡々と続行」
G 息抜き 連敗 → 「少し離れたかっただけなのに」
```

LLM に渡す入力は、属性名、機種、trigger、数値だけ。感情ラベルは渡さない。

### fallback 必須

```python
FALLBACK_VOICES = {
    "A": {
        "best": ["え、これだけで光るんだ", "まだ何も分からないのに来た"],
        "worst": ["何が悪いのか分からない"],
    },
    "C": {
        "best": ["ここで伸びたら全部戻せる", "まだ終わってない、ここから"],
        "worst": ["引くに引けないところまで来た"],
    },
    "H": {
        "best": ["期待値より上、淡々と続行"],
        "worst": ["この展開なら撤退が正解"],
    },
}
```

---

## 6. Q5: 「爆発の兆し」の実装提案

### 結論

α / β / γ の中では、**αを主定義、γを条件フィルタ**にするのが一番よいです。

```text
爆発の兆し = event_impact が高い意味イベント
高ストレス = pre_event_stress が高い状態
```

として分けます。

### 推奨実装

```python
HEAVY_CUE_EVENTS = {
    "kakutei_engi",
    "tokka_heavy",
    "uwanose_heavy",
}

def is_explosion_cue(row):
    trigger = row["trigger_event"]
    event_impact = row["event_impact"]
    machine = row["machine_name"]

    if trigger in HEAVY_CUE_EVENTS:
        return True

    # 入口イベントも、重い機種では「兆し」として扱う
    if trigger == "chain_start" and machine in {"GOD_OKI", "ART_2010"}:
        return event_impact >= 0.52

    return event_impact >= 0.90
```

表示上は、`chain_start` を「爆発の入口」、heavy系を「爆発の兆し」と呼び分け。

### Lv2 測定方法への追加

#### 1. Top5 平均ストレス vs 全 C 平均との差

```text
C型 Top5 の直前ストレス平均: 86
C型 全体平均: 63
C型 兆しイベント平均: 71
```

#### 2. 高ストレス × 兆し の平均 Δ 脳汁

```python
high_stress = pre_event_stress >= quantile(C_rows.pre_event_stress, 0.75)
cue = is_explosion_cue(row)

mean_delta_high_cue = mean(C_rows[high_stress & cue].brain_delta)
mean_delta_low_cue = mean(C_rows[~high_stress & cue].brain_delta)
```

```text
高ストレス × 兆し: 平均 +48
低ストレス × 兆し: 平均 +31
```

#### 3. 条件付き確率

```text
脳汁ピーク確率
高ストレス×兆し: 24%
その他: 7%
```

#### 4. Spearman 相関

飽和があるので Pearson より Spearman が向いています。

### 合否判定（3段階）

```python
if top5_avg >= all_c_avg + 0.12 and mean_delta_high_cue >= mean_delta_low_cue * 1.25:
    result = "支持"
elif top5_avg >= all_c_avg + 0.06 or mean_delta_high_cue >= mean_delta_low_cue * 1.10:
    result = "部分支持"
else:
    result = "未支持"
```

「失敗」と言わない。**支持 / 部分支持 / 今回は支持されず** の3段階。

### 外れた場合のテンプレ

#### パターン1: ストレスより event が強かった

> 仮説は完全には当たりませんでした。
> C型の脳汁ピークは、ストレス最大の瞬間ではなく、**重い兆しが来た瞬間**に集中しました。
> ただしTop5の直前ストレスは平均より高く、ストレスは燃料、イベントは点火役として働いていました。

#### パターン2: 低ストレスでも爆発

> 今回の結果では、ストレスが低いC型にも大きな脳汁ピークが出ました。
> つまり最大要因はストレス単独ではなく、**感受性 × 入口イベント × 取り戻せる予感**でした。
> 仮説は「最もストレスが高い時」から、「高ストレス域で重い兆しが来た時」に修正できます。

#### パターン3: ほぼ支持されなかった

> 今回のモデルでは、C型のピークは高ストレス帯に集中しませんでした。
> 自分の仮説はそのままでは支持されません。
> ただし観察上は、ストレスよりも **イベントの意味** と **感受性** が脳汁の立ち上がりを決めていました。
> これは、自分が「追い詰められていたから興奮した」と感じていた体験の中に、実際には別の要因も混ざっていた可能性を示します。

---

## 7. Q6: 表現の丸さチェック

### 「中毒」はアウトか、セーフか

**内部名としてはセーフ。動画の大見出しとしてはやや強い。**

| 用途           | 表記                         |
| ------------ | -------------------------- |
| コード内部        | `C_ADDICTIVE` or `C_CHASE` |
| 動画の属性名       | **C. 追い上げ**                |
| 小さな補足        | のめり込み傾向                    |
| Phase 6 の仮説文 | 自分はC. 追い上げ型に近いと仮定          |
| PDF本文        | 中毒型という自己仮説、と説明してもOK        |

### 代替語

| 候補    | 評価                         |
| ----- | -------------------------- |
| 追い上げ  | 最推奨。仮説に合う、嫌悪感が少ない          |
| のめり込み | 柔らかいが少し曖昧                  |
| 一発待ち  | パチスロ文脈は強いが、一般視聴者には少し分かりにくい |
| リベンジ  | 分かりやすいが、ややゲームっぽい           |
| 沼     | 軽いが、ハッカソン提出物には少しネットスラング感   |
| 中毒    | 強い。自己仮説パートだけならアリ           |
| 依存    | 避ける。診断・病名っぽく見える            |

**C. 追い上げ** で。Phase 6 でだけ「自分の仮説: 追い上げ型は、ストレスが高い時の爆発の兆しで最大反応するのか？」と出す。

### 8属性紹介の画作り

人物属性に見えすぎると嫌悪感が出ます。**人間アイコンではなく、心理パターンの抽象アイコン**。

| 属性         | アイコン案       | 動き          |
| ---------- | ----------- | ----------- |
| A 新人       | きらめき / ?    | 小さく跳ねる      |
| B 常連       | カレンダー / 定位置 | ゆっくり点滅      |
| C 追い上げ     | 上向き矢印 / 渦   | ストレスバーから急上昇 |
| D アフターファイブ | 時計 / バッグ    | 夕方から点灯      |
| E 悠々自適     | コーヒー / 雲    | ほぼ動かない      |
| F シニア常連    | ベンチ / 長い線   | ゆっくり滞在      |
| G 息抜き      | 葉っぱ / 深呼吸   | 当たりでふっと明るく  |
| H パチプロ     | 電卓 / 定規     | 直線、低振幅      |

色は赤黒を避け、**全属性同じ明度・同じ扱い**。Cだけ危険色にしすぎない。

---

## 8. 見落としてる観点 / 提出 6 日前で踏みそうな罠

### 罠1: 仮説を式に入れてから仮説を検証してしまう

PDFに必ず書く:

> 本作は実データによる因果検証ではなく、仮説を組み込んだ抽象モデル上で、どのようなピークが現れるかを観察するシミュレーションである。

余力があれば、軽い ablation を 1 つ:

```text
通常モデル
stress係数OFFモデル
```

C型の Top5 がどう変わるか。

### 罠2: 最高幸福ランキングと仮説検証ランキングの指標が混ざる

```text
最高幸福 = 脳汁の跳ね上がり + ストレス解放
仮説検証 = ストレス直前値 × Δ脳汁
```

### 罠3: 16シーンが速すぎる

2秒カードで読ませる情報は3つまで。心の声は短く。説明文はPDFへ。

### 罠4: rare event が出ない

```text
統計用: 複数seedで集計
動画用: 代表seedを選ぶ
```

PDFに「動画は代表seed、集計は複数seed平均」と書く。

### 罠5: arousal 100 張り付き

保存する値は3つ:

```python
raw_brain_delta
clipped_brain_delta
brain_after
```

ランキングは `raw_brain_delta`、画面表示は `brain_after`。

### 罠6: 「1000人」がリアル人数に見える

```text
1000人は実際のホール分布ではなく、
8つの心理パターンを同じ人数で比較するための実験設計です
```

### 罠7: 配布コード拡張要件

PDF に必須:

```text
配布コードの「2D空間上で複数エージェントが場所を選ぶ」構造を、
パチスロホール内の台選択・滞在・離脱シミュレーションへ拡張した。
本作では、場所の魅力度だけでなく、台の確率物理、連チャン状態、
中間イベント、個人ごとのストレス反応を追加した。
```

「配布コードを使っていない」ではなく、**空間エージェントシミュレーションを拡張した**と言語化。

### 罠8: Cの自己分析が重くなりすぎる

```text
最後に、自分の仮説を答え合わせします
自分はC. 追い上げ型に近いと仮定
ストレスが高い時ほど、爆発の兆しで脳汁は跳ねたのか？
```

「自分は中毒です」と真正面から出すより、**自分をモデルに当てはめてみた** という距離感。

---

## 最終推奨まとめ

```text
1. 8属性は均等配分でいく
2. 画面表示は「脳汁」「ストレス」だけ
3. Cの動画名は「追い上げ型」、中毒は自己仮説パートだけで使う
4. stress は tanh + 指数飽和 + 慣性で動的化
5. 最高幸福は「脳汁上昇 + ストレス解放」
6. 最不幸は「ストレス高 + 脳汁低 + 負け/ハマり」
7. 爆発の兆しは event_impact ベースで定義
8. Phase 6 は「支持 / 部分支持 / 未支持」の3段階で答え合わせ
9. PDFには「抽象モデルであり、実データの因果検証ではない」と明記
```

一番大事な締めの言葉:

> ストレスは、脳汁を生む原因そのものではなかった。
> でも、重い兆しが来た時に、それを何倍にも増幅する燃料だった。

これなら、仮説が当たっても外れても、動画のラストがちゃんと締まる。
