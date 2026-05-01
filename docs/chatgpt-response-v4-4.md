# ChatGPT Pro 回答 v4.4 → v4.5（機種仕様詳細レビュー、2026-05-02）

> 投げたプロンプト: `docs/相談プロンプト-v4-4.md`
> 添付: CLAUDE.md / spike_v43.py / chatgpt-response-v4-3.md / R1-R3-aggregation.md

---

## 1. 方向性総評

v4.5 は **採用でいい**です。今回の追加は「機種を増やしたい」ではなく、実機経験から出てきた **興奮の質とストレスの質を分ける校正**なので、v4.4 の観察型構造をむしろ強くします。

ただし、実装上の整理はこうした方が安全です。

> **物理連チャン**、**体感連チャン**、**期待の意味づけ**を分離する。

特に PURE_A はここが重要です。純 A は物理的には `chain_mode: none` のままでよいです。でも「ジャグ連」「謎の 10 連」みたいな体感は、`continue_prob` ではなく **streak_bonus** で表現する方がきれいです。`continue_prob > 0` にしてしまうと、純 A が別の機械になってしまいます。

今回の v4.5 で入れるべき優先順位:

| 優先 | 概念 | 理由 |
|----|------|------|
| 1 | `big_gain_log` | GOD / 爆裂 AT の桁違い感を出す必須項 |
| 2 | `streak_bonus` | ジャグ連・北斗 10 連・沖ドキ 20 連の体感を表現 |
| 3 | `chain_anxiety` 機種別化 | CHAIN_OKI の「楽しいのにしんどい」を出す |
| 4 | 期待裏切り + scrap stress | 2 つを別実装せず、同じ disappointment 系にまとめる |
| 5 | 未練打ち | C 追い上げ型の観察として動画に立つ |

6 日残しなら、**Q5 期待裏切り**と **Q6 激レア scrap** は別概念として説明しつつ、実装は `disappointment_stress` 1 本に統合するのが現実的です。

---

## 2. Q1: 6 機種の物理仕様 YAML 推奨

```yaml
machines:
  - code: PURE_A
    display_name: "5号機 Aタイプ"
    representatives: ["ジャグラー", "ハナハナ"]
    chain_mode: "none"
    p_initial_hit: 0.215
    continue_prob: 0.00
    payout_mean: 4700
    payout_std: 2200
    payout_cap: 18000
    stake: 1000
    bonus_excitement_multiplier: 0.85
    chain_start_impact: 0.18
    continuation_excitement_multiplier: 0.00
    streak_gap_steps: 2
    streak_onset: 4
    streak_bonus_multiplier: 1.35
    chain_anxiety_profile: "none_or_low"
    event_probs: {}
    event_impacts: {}

  - code: MIDDLE_45
    display_name: "4.5号機ミドル"
    representatives: ["北斗の拳", "吉宗", "銭形"]
    chain_mode: "chain"
    p_initial_hit: 0.055
    continue_prob: 0.60
    payout_mean: 8200
    payout_std: 7000
    payout_cap: 80000
    stake: 1000
    bonus_excitement_multiplier: 1.35
    chain_start_impact: 0.45
    continuation_excitement_multiplier: 0.85
    streak_gap_steps: 1
    streak_onset: 5
    streak_bonus_multiplier: 1.15
    chain_anxiety_profile: "milestone_pressure"
    event_probs:
      uwanose_light: 0.030
      uwanose_heavy: 0.0040
      tokka_light: 0.012
      tokka_heavy: 0.0015
      kakutei_engi: 0.0008
    event_impacts:
      uwanose_light: 0.40
      uwanose_heavy: 1.05
      tokka_light: 0.70
      tokka_heavy: 1.25
      kakutei_engi: 1.40

  - code: BAKURETSU_AT
    display_name: "4号機 爆裂AT"
    representatives: ["アラジン", "獣王", "サラリーマン金太郎"]
    chain_mode: "chain"
    p_initial_hit: 0.018
    continue_prob: 0.72
    payout_mean: 16500
    payout_std: 27000
    payout_cap: 200000
    stake: 1000
    bonus_excitement_multiplier: 2.25
    chain_start_impact: 0.82
    continuation_excitement_multiplier: 0.80
    streak_gap_steps: 1
    streak_onset: 4
    streak_bonus_multiplier: 0.85
    chain_anxiety_profile: "entry_rare_betrayal_high"
    event_probs:
      uwanose_light: 0.025
      uwanose_heavy: 0.0060
      tokka_light: 0.010
      tokka_heavy: 0.0030
      kakutei_engi: 0.0015
    event_impacts:
      uwanose_light: 0.55
      uwanose_heavy: 1.25
      tokka_light: 0.80
      tokka_heavy: 1.55
      kakutei_engi: 1.75

  - code: ART_2010
    display_name: "2010年代 爆裂ART"
    representatives: ["凱旋", "ハーデス", "秘宝伝", "神々の系譜"]
    chain_mode: "chain"
    p_initial_hit: 0.030
    continue_prob: 0.83
    payout_mean: 6700
    payout_std: 6500
    payout_cap: 100000
    stake: 1000
    bonus_excitement_multiplier: 1.70
    chain_start_impact: 0.55
    continuation_excitement_multiplier: 0.75
    streak_gap_steps: 1
    streak_onset: 7
    streak_bonus_multiplier: 0.75
    chain_anxiety_profile: "accident_entrance"
    event_probs:
      uwanose_light: 0.055
      uwanose_heavy: 0.0060
      tokka_light: 0.035
      tokka_heavy: 0.0040
      kakutei_engi: 0.0010
    event_impacts:
      uwanose_light: 0.45
      uwanose_heavy: 1.10
      tokka_light: 0.75
      tokka_heavy: 1.35
      kakutei_engi: 1.55

  - code: CHAIN_OKI
    display_name: "中毒性連チャン型"
    representatives: ["沖ドキ！", "ヴァルヴレイヴ"]
    chain_mode: "chain"
    p_initial_hit: 0.035
    continue_prob: 0.82
    payout_mean: 6200
    payout_std: 7500
    payout_cap: 120000
    stake: 1000
    bonus_excitement_multiplier: 1.65
    chain_start_impact: 0.65
    continuation_excitement_multiplier: 0.95
    streak_gap_steps: 1
    streak_onset: 5
    streak_bonus_multiplier: 1.25
    chain_anxiety_profile: "no_guarantee_high"
    # uwanose_light=継続示唆 / uwanose_heavy=継続確定 / tokka_light=天国 / tokka_heavy=超連
    event_probs:
      uwanose_light: 0.060
      uwanose_heavy: 0.018
      tokka_light: 0.010
      tokka_heavy: 0.0030
      kakutei_engi: 0.0010
    event_impacts:
      uwanose_light: 0.55
      uwanose_heavy: 0.95
      tokka_light: 1.15
      tokka_heavy: 1.45
      kakutei_engi: 1.60

  - code: GOD_2000
    display_name: "2000年 ミリオンゴッド系"
    representatives: ["ミリオンゴッド"]
    chain_mode: "chain"
    p_initial_hit: 0.006
    continue_prob: 0.52
    payout_mean: 80000
    payout_std: 90000
    payout_cap: 220000
    stake: 1000
    bonus_excitement_multiplier: 4.40
    chain_start_impact: 0.95
    continuation_excitement_multiplier: 0.70
    streak_gap_steps: 1
    streak_onset: 3
    streak_bonus_multiplier: 0.45
    chain_anxiety_profile: "god_afterglow"
    event_probs:
      uwanose_light: 0.010
      uwanose_heavy: 0.0040
      tokka_light: 0.005
      tokka_heavy: 0.0020
      kakutei_engi: 0.0015
    event_impacts:
      uwanose_light: 0.50
      uwanose_heavy: 1.35
      tokka_light: 0.90
      tokka_heavy: 1.75
      kakutei_engi: 2.10
```

| 機種 | hit_rate | target_return | 質感 |
|------|---------|--------------|------|
| PURE_A | 0.215 | 1.01 | コツコツ + streak で脳汁 |
| MIDDLE_45 | 0.121 | 0.99 | 当たりやすいが 10 連は遠い |
| BAKURETSU_AT | 0.060 | 1.00 | 入らない、入ると重い |
| ART_2010 | 0.150 | 1.00 | 入るが伸びるには事故が必要 |
| CHAIN_OKI | 0.163 | 1.01 | 継続多いが保証なし不安 |
| GOD_2000 | 0.012 | 0.99 | 基本吸い込み、来たら別格 |

---

## 3. Q2: 興奮量計算式の最終案

```python
from math import log10, tanh

def compute_brain_delta(persona, mt, event, state):
    payout = event.payout
    pre_stress = state.pre_event_stress
    event_impact = mt.event_impacts.get(event.trigger_event, 0.0)

    # 1. 当たり身体反応
    if event.chain_just_started:
        hit_body = 22.0 * mt.bonus_excitement_multiplier
    elif event.hit:
        hit_body = 12.0 * mt.continuation_excitement_multiplier
    else:
        hit_body = 0.0

    # 2. 通常の取得感（早めに飽和）
    gain_signal = tanh(max(0, payout - mt.stake) / 7000.0)
    gain_body = 8.0 * gain_signal

    # 3. 大量取得項（v4.5 重要追加）
    big_gain_log = max(0.0, log10(max(payout, 5000) / 5000.0))
    big_gain_arousal = 10.0 * big_gain_log * mt.bonus_excitement_multiplier

    # 4. 意味づけ爆発
    dopamine_burst = 35.0 * event_impact * (0.5 + 1.5 * pre_stress) * persona.dopamine_sensitivity

    # 5. 異常連チャン
    streak = compute_streak_bonus(state.streak_count, mt)

    raw_delta = hit_body + gain_body + big_gain_arousal + dopamine_burst + streak
    raw_delta -= 0.05 * (state.brain_arousal - persona.base_arousal)
    return raw_delta
```

`bonus_excitement_multiplier` 推奨:

| 機種 | 推奨 | 理由 |
|------|-----|------|
| PURE_A | 0.85 | 光る喜びはあるが控えめ |
| MIDDLE_45 | 1.35 | キーン・REG/BIG 分岐 |
| BAKURETSU_AT | 2.25 | AT 入った瞬間が強烈 |
| ART_2010 | 1.70 | 入口より事故契機が主役 |
| CHAIN_OKI | 1.65 | 継続中の毎回反応が強い |
| **GOD_2000** | **4.40** | 3.80 だと普通、5.00 だと統計破壊 |

GOD 100,000 円なら `log10(20)=1.30` で `10 × 1.30 × 4.40 = +57` が大量取得項だけで乗る。raw 180-250 が普通に出る。

---

## 4. Q3: streak_bonus 式と機種別カーブ

PURE_A は `chain_mode: none` のまま、近接当たりだけ streak に入れる:

```python
def update_streak(state, mt, event):
    if not event.hit:
        state.steps_since_last_hit += 1
        if mt.chain_mode == "none" and state.steps_since_last_hit > mt.streak_gap_steps:
            state.streak_count = 0
        return

    if mt.chain_mode == "none":
        if state.steps_since_last_hit <= mt.streak_gap_steps:
            state.streak_count += 1
        else:
            state.streak_count = 1
    else:
        state.streak_count = state.chain_step_count

    state.steps_since_last_hit = 0


def compute_streak_bonus(N, mt):
    if N < mt.streak_onset:
        return 0.0
    x = N - mt.streak_onset
    step_up = 18.0 * sigmoid((x - 0.5) / 1.2)
    tail = 4.0 * x
    return mt.streak_bonus_multiplier * (step_up + tail)
```

体感例:

| 機種 | N | streak_bonus | 体感 |
|------|---|------------|------|
| PURE_A | 5 | +20 | 「あれ、また光った」 |
| PURE_A | 10 | +55 | 「ジャグ連おかしい」 |
| MIDDLE_45 | 10 | +40 | 「北斗 10 連見えた」 |
| CHAIN_OKI | 20 | +90 | 「20 連、どこまで行く？」 |

### streak と anxiety の同時立ち上がり

```python
def compute_streak_anxiety(N, mt):
    if N <= 0:
        return 0.0
    if mt.code == "MIDDLE_45":
        # 北斗 10連プレッシャー（10連で下がる）
        return 0.65 * sigmoid((N-5)/1.2) * (1.0 - sigmoid((N-10)/1.0))
    if mt.code == "CHAIN_OKI":
        # 保証なし、長いほど不安
        return 0.85 * sigmoid((N-4)/2.0)
    if mt.code == "PURE_A":
        return 0.25 * sigmoid((N-6)/2.0)
    if mt.code == "ART_2010":
        return 0.35 * sigmoid((N-8)/2.5)
    if mt.code == "BAKURETSU_AT":
        return 0.30 * sigmoid((N-5)/2.0)
    if mt.code == "GOD_2000":
        return 0.20 * sigmoid((N-3)/1.5)
    return 0.0
```

CHAIN_OKI の証言「ドキドキ感はずっとある。これはストレスかも」が初めてモデル化される。

---

## 5. Q4: chain_anxiety 機種別カーブ

```python
def compute_chain_anxiety(persona, mt, state):
    if not state.chain_active:
        return 0.0

    chain_len = state.chain_step_count
    chain_stock = state.chain_stock
    guarantee_signal = min(1.0, chain_stock / 2.0)

    low_stock = sigmoid((2.0 - chain_stock) / 1.5)
    no_guarantee_dread = (1.0 - guarantee_signal) * sigmoid((chain_len - mt.anxiety_onset) / mt.anxiety_scale)
    torikirezu = state.time_pressure_signal * persona.torikirezu_sensitivity * sigmoid((state.expected_chain_tail - state.remaining_steps) / 8.0)

    milestone_pressure = 0.0
    if mt.code == "MIDDLE_45":
        milestone_pressure = sigmoid((chain_len-5)/1.2) * (1.0 - sigmoid((chain_len-10)/1.0))

    return clip(
        mt.anxiety_base
        + mt.low_stock_w * low_stock
        + mt.no_guarantee_w * no_guarantee_dread
        + mt.milestone_w * milestone_pressure
        + mt.time_w * torikirezu,
        0.0, 1.0
    )
```

機種別係数:

| 機種 | base | low_stock | no_guarantee | milestone | time | stress 重み |
|------|-----:|---------:|-------------:|----------:|-----:|-----------:|
| PURE_A | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| MIDDLE_45 | 0.08 | 0.25 | 0.20 | **0.55** | 0.20 | 0.10 |
| BAKURETSU_AT | 0.06 | 0.20 | 0.25 | 0.00 | 0.15 | 0.08 |
| ART_2010 | 0.08 | 0.25 | 0.25 | 0.00 | 0.35 | 0.10 |
| **CHAIN_OKI** | **0.14** | **0.35** | **0.60** | 0.00 | 0.20 | **0.16** |
| GOD_2000 | 0.04 | 0.15 | 0.15 | 0.00 | 0.10 | 0.06 |

stress_target に追加:

```python
stress_target += mt.chain_anxiety_stress_weight * chain_anxiety
```

---

## 6. Q5/Q6: disappointment_stress（期待裏切り + 激レア scrap 統合）

### betrayal (chain 終了時)

```python
def expected_satisfying_chain_len(mt, state):
    base = {"PURE_A":1, "MIDDLE_45":5, "BAKURETSU_AT":5, "ART_2010":6, "CHAIN_OKI":7, "GOD_2000":3}[mt.code]
    if state.last_heavy_event_impact >= 1.2: base += 3
    if state.last_heavy_event_impact >= 1.6: base += 5
    if mt.code == "MIDDLE_45" and state.premium_start: base = max(base, 10)
    return base

def compute_betrayal_stress(mt, state, pre_stress):
    if not state.chain_just_ended:
        return 0.0
    expected_len = expected_satisfying_chain_len(mt, state)
    actual_len = max(1, state.last_chain_len)
    gap = max(0.0, expected_len - actual_len) / expected_len
    expectation_heat = clip(0.35 + 0.35 * state.last_chain_start_impact + 0.30 * state.last_heavy_event_impact, 0.0, 1.0)
    return mt.betrayal_kappa * (gap ** 1.25) * (0.6 + 0.4 * pre_stress) * expectation_heat
```

| 機種 | betrayal_kappa |
|------|----------------|
| PURE_A | 0.00 |
| MIDDLE_45 | 0.14 |
| **BAKURETSU_AT** | **0.22** |
| ART_2010 | 0.18 |
| CHAIN_OKI | 0.12 |
| GOD_2000 | 0.20 |

CHAIN_OKI を最大にしないのがコツ。CHAIN_OKI は継続中の不安が主役。

### scrap (heavy event 後の評価)

```python
HEAVY_EVENTS = {"uwanose_heavy", "tokka_heavy", "kakutei_engi"}

def start_pending_event_eval(mt, event, state):
    if event.trigger_event not in HEAVY_EVENTS:
        return
    impact = mt.event_impacts[event.trigger_event]
    expected_payout = mt.payout_mean * (1.0 + 2.5 * impact)
    state.pending_event_eval = {
        "event": event.trigger_event,
        "start_step": state.step,
        "window": mt.scrap_eval_window,
        "expected_payout": expected_payout,
        "realized_payout": 0,
        "impact": impact,
    }

def update_pending_event_eval(mt, event, state, pre_stress):
    pe = state.pending_event_eval
    if pe is None:
        return 0.0
    pe["realized_payout"] += max(0, event.payout)
    elapsed = state.step - pe["start_step"]
    if elapsed < pe["window"] and not state.chain_just_ended:
        return 0.0

    threshold = pe["expected_payout"] * mt.scrap_eta
    if pe["realized_payout"] >= threshold:
        state.pending_event_eval = None
        return 0.0

    shortage = 1.0 - pe["realized_payout"] / max(1.0, threshold)
    rarity_weight = 0.75 + 0.25 * min(1.0, pe["impact"])
    scrap = mt.scrap_kappa * (shortage ** 1.15) * rarity_weight * (0.7 + 0.3 * pre_stress)
    state.pending_event_eval = None
    return scrap
```

| 機種 | window | scrap_eta | scrap_kappa |
|------|-------:|----------:|------------:|
| PURE_A | - | - | 0.00 |
| MIDDLE_45 | 4 | 0.35 | 0.18 |
| BAKURETSU_AT | 5 | 0.35 | 0.22 |
| **ART_2010** | **8** | 0.35 | **0.25** |
| CHAIN_OKI | 5 | 0.30 | 0.16 |
| GOD_2000 | 4 | 0.30 | **0.28** |

ART_2010 の「事故の入口を引いたのに数十ゲームで終わる」が scrap stress の主役。

---

## 7. Q7: 未練打ち δ の policy override

```python
def compute_miren_signal(persona, state):
    cash_ratio = state.cash / max(1, state.initial_cash)
    net_loss_ratio = max(0, state.initial_cash - state.cash) / max(1, state.initial_cash)

    stress_part = sigmoid((state.pre_event_stress - persona.miren_stress_threshold) / 0.06)
    cash_part = sigmoid((persona.miren_cash_ratio_threshold - cash_ratio) / 0.04)
    loss_part = sigmoid((net_loss_ratio - persona.miren_loss_ratio_threshold) / 0.12)
    chain_block = 0.0 if state.chain_active else 1.0

    return stress_part * cash_part * loss_part * chain_block


def choose_machine_with_miren(persona, state, normal_machine_probs, rng):
    miren = compute_miren_signal(persona, state)
    p_pure_a_override = clip(persona.miren_strength * miren, 0.0, persona.miren_max_pure_a_prob)
    if rng.random() < p_pure_a_override:
        return "PURE_A", "miren_uchi"
    return sample_from(normal_machine_probs), "normal"
```

属性別:

| 属性 | stress 閾値 | cash 比率 | loss 比率 | strength | max PURE_A |
|------|-----------:|---------:|---------:|---------:|-----------:|
| A 新人 | 0.82 | 0.12 | 0.55 | 0.25 | 0.35 |
| B 常連 | 0.86 | 0.12 | 0.55 | 0.35 | 0.45 |
| **C 追い上げ** | **0.82** | **0.15** | **0.45** | **0.85** | **0.70** |
| D アフター5 | 0.88 | 0.10 | 0.55 | 0.20 | 0.30 |
| E 悠々自適 | 0.95 | 0.05 | 0.80 | 0.05 | 0.10 |
| F シニア | 0.88 | 0.12 | 0.55 | 0.25 | 0.35 |
| G 息抜き | 0.84 | 0.12 | 0.50 | 0.30 | 0.40 |
| H パチプロ | 0.92 | 0.08 | 0.70 | 0.05 | 0.10 |

動画字幕:
> 残りわずか。C 追い上げ型は、最後に PURE_A へ流れやすい。

「敗者」「依存」みたいな語は出さない。

---

## 8. Q8: chain_start_impact / event_impacts 校正表

| 機種 | chain_start | uwanose_light | uwanose_heavy | tokka_light | tokka_heavy | kakutei_engi |
|------|------------:|-------------:|-------------:|-----------:|-----------:|------------:|
| PURE_A | 0.18 | - | - | - | - | - |
| MIDDLE_45 | 0.45 | 0.40 | 1.05 | 0.70 | 1.25 | 1.40 |
| BAKURETSU_AT | **0.82** | 0.55 | 1.25 | 0.80 | 1.55 | 1.75 |
| ART_2010 | 0.55 | 0.45 | 1.10 | 0.75 | 1.35 | 1.55 |
| CHAIN_OKI | 0.65 | 0.55 | 0.95 | 1.15 | 1.45 | 1.60 |
| GOD_2000 | **0.95** | 0.50 | 1.35 | 0.90 | 1.75 | **2.10** |

---

## 9. Q9: 桁違い興奮の表現

> **raw と clipped の 2 値保存で十分。表示は `100+` 表記。**

ログには 4 つ残す:
```python
raw_brain_delta       # 例: +214
brain_after_raw       # 例: 236
brain_after_clipped   # 100
brain_overcap         # max(0, brain_after_raw - 100)
```

ランキングは `raw_brain_delta`、画面メーターは `brain_after_clipped`。

表示例:
```text
脳汁 100+
raw Δ脳汁 +214
```

### 神演出後の short-term boost（GOD afterglow）

物理確率を上げない、認知と行動だけ。

```python
def trigger_afterglow(mt, event, state):
    god_like = (mt.code == "GOD_2000") and (
        event.trigger_event == "kakutei_engi"
        or event.payout >= 100000
        or event.event_impact >= 1.8
    )
    if god_like:
        state.afterglow_remaining = 5
        state.afterglow_strength = 1.0

def compute_afterglow_effect(state):
    if state.afterglow_remaining <= 0:
        return 0.0
    age = 5 - state.afterglow_remaining
    effect = state.afterglow_strength * exp(-age / 2.5)
    state.afterglow_remaining -= 1
    return effect

# 使い方
afterglow = compute_afterglow_effect(state)
effective_bonus_multiplier = mt.bonus_excitement_multiplier * (1.0 + 0.35 * afterglow)
urge_to_continue += 0.25 * afterglow
stress_target += 0.04 * afterglow * miss_signal
```

---

## 10. Q10: 全体妥当性

### C 追い上げ仮説の言い方を変える

元: 「C 追い上げ型が最も興奮を感じるのは、最もストレスを感じている時に爆発の兆しがあった時」

v4.5: 「C 追い上げ型では、ストレスが高いほど、爆発の兆し・異常連チャン・大逆転可能性への脳汁反応が増幅される」

「最もストレスを感じている時」と言い切ると、scrap stress や chain_anxiety を入れたせいでストレス最大値が「気持ちいい瞬間」ではなく「終わった直後」に来る可能性がある。

Phase 6 検証指標は v4.4 のまま:
- 高ストレス × 兆し の平均 Δ脳汁
- 低ストレス × 兆し の平均 Δ脳汁
- C Top5 の pre_event_stress

### 削るなら実装の枝分かれ

| 概念 | 残す/削る |
|------|---------|
| big_gain_log | 残す |
| streak_bonus | 残す |
| chain_anxiety | 残す |
| 未練打ち | 残す |
| 期待裏切り | 残すが簡易 |
| 激レア scrap | 残すが簡易（disappointment_stress に統合） |
| GOD afterglow | 余力なら |

実装名 5 本: `streak_bonus / chain_anxiety / disappointment_stress / miren_uchi_policy / afterglow`

### 最重要 3 機種

**GOD_2000 / CHAIN_OKI / PURE_A** が推し（v4.5 の 5 概念が最も見える）。

| 方針 | 最重要 3 |
|-----|---------|
| C 仮説と動画映え重視 | **GOD_2000 / CHAIN_OKI / PURE_A** |
| 全盛期世代の共感重視 | GOD_2000 / MIDDLE_45 / PURE_A |
| 事故待ち構造の説明重視 | GOD_2000 / ART_2010 / CHAIN_OKI |

---

## 11. 罠 10 個

| # | 罠 | 対策 |
|---|---|------|
| 1 | event_probs 母集団ズレ | event 名は固定、表示ラベルだけ機種別 |
| 2 | PURE_A を chain に流す | `chain_mode: none` 維持、`streak_count` で表現 |
| 3 | GOD が Top5 独占 | raw Top5 + stratified highlight 併用 |
| 4 | rare event 出ない | 統計は複数 seed、動画は代表 seed |
| 5 | stress 最大点と joy 最大点ズレる | Phase 6 は pre_event_stress を見る、post_stress 最大ではない |
| 6 | 自己成就 | PDF 明記 + ablation |
| 7 | 低A高D 消える | 内部に反応鈍化 / stress_floor 残す |
| 8 | CHAIN_OKI がただの ART に | chain_anxiety_stress_weight=0.16 で差別化 |
| 9 | 未練打ちが重い表現に | 「敗者」「依存」NG、「最後の一勝負」OK |
| 10 | calibration 後回し | 各機種 100,000 step 空回しで return_index 確認 |

---

## 12. 最終推奨まとめ

```text
1. PURE_A は chain なし、streak_bonus あり
2. GOD_2000 は bonus_excitement_multiplier 4.40、chain_start_impact 0.95
3. payout 大量取得は log10(payout / 5000) で追加
4. raw 脳汁は 200 超え許容、表示は 100+
5. CHAIN_OKI は chain_anxiety を最強にする
6. MIDDLE_45 は 10連 milestone pressure
7. BAKURETSU_AT は entry rare + betrayal high
8. ART_2010 は scrap stress high
9. 未練打ちは C 追い上げ型の policy override
10. Q5/Q6 は disappointment_stress として実装統合
```

動画ラスト:
> 脳汁を生むのは、当たりそのものだけではなかった。
> 負け、未練、続く不安、そして「ここから戻せる」という予感。
> その全部が重なった時、C 追い上げ型の反応は跳ね上がった。
