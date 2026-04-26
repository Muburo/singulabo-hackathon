パチスロプレイ中の心理反応収集およびメタ観察レポート：極端値・補完収集ラウンド（R3）

> Source: Gemini Deep Research / 2026-04-25 取得 / R3 ラウンド

## 1. 事例カード集（質的素材ライブラリ）

本セクションでは、収集された質的データに基づき、シミュレーションモデル用の感情パラメータを含むペルソナカードを提示する。各カードは「ホール内・プレイ中の心理反応」に厳密に焦点を当てて構築されている。

### カテゴリA：依存症末期（多重債務・自己破産寸前）

```yaml
- id: R3-A-001
  category: 依存症末期
  profile:
    age_range: "30代"
    occupation: "無職（元営業職）"
    family: "単身（家族から絶縁状態）"
    debt_yen: 30000000
    addiction_severity: "末期（窃盗・万引き常習、親の退職金全損）"
    gambling_history: "15年以上"
    visit_motive: "飢えと寒さからの現実逃避／生存本能の完全な麻痺"
    psychiatric_comorbidity: "重度の抑うつ・解離性障害"
  trigger:
    event: "生活保護費（あるいは盗品売却金）の最後の一枚をサンドに入れた瞬間"
    machine_type: "1円パチンコ"
    time_of_day: "平日午前"
  inner_monologue_ja: "今思うと本当に狂っていた。今日食べるものもないのに、本屋で盗んだ本を売ってパチンコを打っている。もうどうにもならない。自分が崩壊していく。"
  emotional_state:
    arousal_0_100: 90
    despair_0_100: 100
    dominant_emotion: "完全な絶望 × 強迫的狂気"
  action: "無表情のまま、ただ惰性で右打ちを続ける。玉が減るのを見つめる。"
  post_play_state: "一文無しになり、スーパーで食料を万引きして帰る。"
  source:
    type: "依存症対策センター当事者手記"
    url_or_ref: "ncasa-japan.jp"
    confidence: "高"
  notes: "Interruptibility = 0。Dissociation tendency = 1.0。生存のための資金すら投じる極限状態であり、Despairが100に達していてもArousalが落ちない。"

- id: R3-A-002
  category: 依存症末期
  profile:
    age_range: "50代"
    occupation: "元会社員（失職）"
    family: "離婚（妻・娘と離別）"
    debt_yen: 100000000
    addiction_severity: "極限（総損失1億円超、富士の樹海を彷徨う）"
    gambling_history: "36年間"
    visit_motive: "過去の栄光の追体験／死の直前の麻酔"
    psychiatric_comorbidity: "希死念慮"
  trigger:
    event: "借金返済の目処が完全に絶たれ、天井付近で単発を引いた瞬間"
    machine_type: "AT機（パチスロ）"
    time_of_day: "休日夜"
  inner_monologue_ja: "こんなクズ人間は生きていてもしょうがない。死んだほうが世のためだ。でも、あともう1回だけ。これで出なかったら樹海に行こう。"
  emotional_state:
    arousal_0_100: 95
    despair_0_100: 95
    dominant_emotion: "希死念慮 × 焦燥感"
  action: "手元の小銭をかき集め、震える手で最後のメダルを投入する。"
  post_play_state: "退店後、車で富士の樹海へ向かい2日間彷徨う。"
  source:
    type: "依存症対策センター当事者手記"
    url_or_ref: "ncasa-japan.jp"
    confidence: "高"
  notes: "Interruptibility = 0。ギャンブルによる損失額が1億円を突破しており、資金枯渇と同時に物理的な死を意識している。Sensory_gating_factor = 0.1（外部の音が聞こえない）。"

- id: R3-A-003
  category: 依存症末期
  profile:
    age_range: "40代"
    occupation: "元会社員"
    family: "親と同居（絶縁寸前）"
    debt_yen: 7000000
    addiction_severity: "末期（自己破産免責直後）"
    gambling_history: "20年"
    visit_motive: "借金免責の解放感からの油断"
    psychiatric_comorbidity: "なし"
  trigger:
    event: "自己破産の免責が下りた当日の給料日、駅に着いた瞬間"
    machine_type: "パチスロ"
    time_of_day: "平日夕方"
  inner_monologue_ja: "自己破産の手続きが終わった。やっと気が楽になった。そういえば今日給料日だ。借金もないし、ちょっとなら打ってもいいだろう。"
  emotional_state:
    arousal_0_100: 85
    despair_0_100: 80
    dominant_emotion: "無意識の自動操縦 × 安堵の歪み"
  action: "気がつくと銀行で生活費を下ろし、パチンコ屋の席に座ってレバーを叩いている。"
  post_play_state: "免責直後にも関わらず再び借金生活に転落。"
  source:
    type: "依存症対策センター当事者手記"
    url_or_ref: "ncasa-japan.jp"
    confidence: "高"
  notes: "Interruptibility = 0.1。自己破産という究極のペナルティを経ても行動を制御できない。Despairは底を打った直後にArousalの誘惑に負けるメカニズム。"

- id: R3-A-004
  category: 依存症末期
  profile:
    age_range: "30代"
    occupation: "会社員"
    family: "妻・子（家庭内別居中）"
    debt_yen: 8000000
    addiction_severity: "末期（消費者金融カード8枚）"
    gambling_history: "10年"
    visit_motive: "負けを取り返すという強迫観念"
    psychiatric_comorbidity: "強迫性障害の傾向"
  trigger:
    event: "財布の現金が底をつき、ATMへ向かうか迷う瞬間"
    machine_type: "パチスロ"
    time_of_day: "休日午後"
  inner_monologue_ja: "これ以上つぎ込んだら生活費どうするんだ。でも、パチンコの負けはパチンコで勝って返すしかないんだ。取り返さなきゃ終われない。"
  emotional_state:
    arousal_0_100: 100
    despair_0_100: 90
    dominant_emotion: "極度の強迫観念 × 悪魔の声への服従"
  action: "心の底からの警告を無視し、店舗内のATMで新たなカードからキャッシングを引き出す。"
  post_play_state: "現金全損。駐車場で車の中で何時間も動けず、虚無感に苛まれる。"
  source:
    type: "依存症対策センター当事者手記"
    url_or_ref: "ncasa-japan.jp"
    confidence: "高"
  notes: "Interruptibility = 0。負け分をギャンブルで取り返すという認知の歪みが固定化されている。Arousalが100のまま暴走する。"

- id: R3-A-005
  category: 依存症末期
  profile:
    age_range: "30代"
    occupation: "会社員（横領発覚寸前）"
    family: "独身"
    debt_yen: 5000000
    addiction_severity: "末期（ヤミ金・会社資金横領）"
    gambling_history: "12年"
    visit_motive: "横領金補填のための一発逆転"
    psychiatric_comorbidity: "パニック発作"
  trigger:
    event: "ヤミ金からの着信がスマホ画面に表示された瞬間"
    machine_type: "パチスロ（ハイエナ狙い）"
    time_of_day: "平日昼間"
  inner_monologue_ja: "電話に出られない。会社のお金にも手をつけてしまった。ここでフリーズを引かないと警察に行かれる。頼む、頼む、頼む。"
  emotional_state:
    arousal_0_100: 100
    despair_0_100: 100
    dominant_emotion: "極限の恐怖 × 祈り"
  action: "画面の着信を無視し、震える手でMAXBETボタンを連打する。周囲の音は一切聞こえない。"
  post_play_state: "敗北。ヤミ金に拉致され、5時間の監禁を受ける。"
  source:
    type: "依存症対策センター当事者手記"
    url_or_ref: "ncasa-japan.jp"
    confidence: "高"
  notes: "Arousal 100 × Despair 100の極限値。Stigma_barrier = 1.0（社会的信用の完全喪失の恐怖）。"

- id: R3-A-006
  category: 依存症末期
  profile:
    age_range: "50代"
    occupation: "公務員（高位・安定収入）"
    family: "妻・子"
    debt_yen: 15000000
    addiction_severity: "末期（カード枠を貯金と勘違いする金銭麻痺）"
    gambling_history: "34年"
    visit_motive: "特権意識の裏返し／無限の資金があるという錯覚"
    psychiatric_comorbidity: "なし"
  trigger:
    event: "投資が10万円を超え、追加でクレジットカードでキャッシングする瞬間"
    machine_type: "パチスロ"
    time_of_day: "休日昼"
  inner_monologue_ja: "自分は公務員で収入は安定している。カードの限度額は自分の貯金みたいなものだ。いくらでも借りられるし、いくらでも打てる。"
  emotional_state:
    arousal_0_100: 80
    despair_0_100: 10
    dominant_emotion: "全能感 × 認知の歪み"
  action: "焦る様子もなく、ATMで限度額いっぱいまで引き出し、当然のように台に戻る。"
  post_play_state: "長期的には借金1500万に至るが、プレイ中はその恐怖を感じていない。"
  source:
    type: "依存症対策センター当事者手記"
    url_or_ref: "ncasa-japan.jp"
    confidence: "高"
  notes: "安定収入がもたらす致命的な認知の歪み。プレイ中のDespairが極端に低く、事後的に一気に100へ跳ね上がる遅延型モデル。"

- id: R3-A-007
  category: 依存症末期
  profile:
    age_range: "20代"
    occupation: "フリーター"
    family: "実家暮らし（家庭内窃盗常習）"
    debt_yen: 3500000
    addiction_severity: "末期（サラ金＋友人からの借金）"
    gambling_history: "5年"
    visit_motive: "才能があるという妄想の証明"
    psychiatric_comorbidity: "なし"
  trigger:
    event: "友人の財布から盗んだ金で大当たりを引いた瞬間"
    machine_type: "パチスロ"
    time_of_day: "平日夜"
  inner_monologue_ja: "よし、当たった。これで盗んだ分をこっそり返せる。自分にはギャンブルの才能があるんだ。いつか大勝して全部なんとかなる。"
  emotional_state:
    arousal_0_100: 95
    despair_0_100: 40
    dominant_emotion: "歪んだ安堵感 × 誇大妄想"
  action: "罪悪感を完全に忘れ、ドヤ顔でメダルを箱に詰める。"
  post_play_state: "結局全額使い果たし、友人に窃盗がバレて地獄を見る。"
  source:
    type: "大石クリニック症例報告"
    url_or_ref: "ohishi-clinic.or.jp"
    confidence: "高"
  notes: "Dissociation tendency = 0.8。他者の金を盗んでいるという犯罪の事実がプレイ中のArousalによって完全に麻痺している。"

- id: R3-A-008
  category: 依存症末期
  profile:
    age_range: "40代"
    occupation: "無職（元会社員）"
    family: "妻と同居（離婚協議中）"
    debt_yen: 12000000
    addiction_severity: "末期（親の退職金全損）"
    gambling_history: "20年"
    visit_motive: "何も考えたくないための作業"
    psychiatric_comorbidity: "重度の抑うつ"
  trigger:
    event: "財布の中の最後の1000円札を見つめている瞬間"
    machine_type: "パチンコ"
    time_of_day: "休日夕方"
  inner_monologue_ja: "これを入れれば本当に何もなくなる。でも、もうどうでもいい。家に帰って妻の顔を見るくらいなら、ここで液晶を見つめていたい。"
  emotional_state:
    arousal_0_100: 20
    despair_0_100: 100
    dominant_emotion: "無気力 × 虚無感"
  action: "ゆっくりと1000円札を入れ、玉が打ち出されるのをただ眺める。"
  post_play_state: "車に戻り、数時間シートを倒して天井を見つめる。"
  source:
    type: "依存症対策センター当事者手記"
    url_or_ref: "ncasa-japan.jp"
    confidence: "高"
  notes: "Interruptibility = 0。Arousalが低いままDespairが100に張り付く「アパシー持続型」。 Sensory_gating_factor = 0.1。"

- id: R3-A-009
  category: 依存症末期
  profile:
    age_range: "30代"
    occupation: "元営業職"
    family: "独身"
    debt_yen: 5000000
    addiction_severity: "極限（公園・コインランドリー寝泊まり）"
    gambling_history: "15年"
    visit_motive: "ゴミ箱を漁る現実からの完全な逃避"
    psychiatric_comorbidity: "解離性障害"
  trigger:
    event: "実家に一時帰宅し、家の中のお金を探し出してホールへ来た瞬間"
    machine_type: "AT機"
    time_of_day: "平日午後"
  inner_monologue_ja: "ダメだ。もう、ギャンブルを止められない。親の金だ。でもレバーを叩いている間だけは、自分がホームレス同然だということを忘れられる。"
  emotional_state:
    arousal_0_100: 70
    despair_0_100: 95
    dominant_emotion: "自己嫌悪 × トランス状態"
  action: "涙目になりながらも、高速でリールを止め続ける。"
  post_play_state: "再び失踪し、コインランドリーへ戻る。"
  source:
    type: "依存症対策センター当事者手記"
    url_or_ref: "ncasa-japan.jp"
    confidence: "高"
  notes: "Dissociation_tendency = 1.0。生存機能が完全に崩壊しており、衣食住よりもプレイへのArousalが優先される。"

- id: R3-A-010
  category: 依存症末期
  profile:
    age_range: "50代"
    occupation: "専業主婦"
    family: "夫・子供（育児放棄状態）"
    debt_yen: 8000000
    addiction_severity: "末期（ヤミ金借入・消費者金融多数）"
    gambling_history: "30年"
    visit_motive: "家庭内の居場所のなさからの逃避"
    psychiatric_comorbidity: "パニック障害"
  trigger:
    event: "夫の帰宅時間が迫っているのに確変が止まらない瞬間"
    machine_type: "パチンコ"
    time_of_day: "平日夕方"
  inner_monologue_ja: "子供のご飯を作らなきゃ。夫が帰ってくる。でも確変が終わらない。捨てて帰れない。バレたら殺されるかもしれないのに。"
  emotional_state:
    arousal_0_100: 100
    despair_0_100: 80
    dominant_emotion: "パニック × 射幸心の呪縛"
  action: "冷や汗をかき、時計を何度も見ながら、震える手でハンドルを固定する。"
  post_play_state: "取り繕うための嘘を考えながら急いで帰宅し、パニック発作を起こす。"
  source:
    type: "依存症対策センター当事者手記"
    url_or_ref: "ncasa-japan.jp"
    confidence: "高"
  notes: "Interruptibility = 0。Stigma_barrier（夫への恐怖）が極大化しているが、サンクコストとArousalがそれを上回る現象。"

- id: R3-A-011
  category: 依存症末期
  profile:
    age_range: "20代"
    occupation: "大学生（留年・中退寸前）"
    family: "実家暮らし"
    debt_yen: 3000000
    addiction_severity: "末期（学生ローン・友人からの多重借金）"
    gambling_history: "3年"
    visit_motive: "奨学金を取り戻すための絶望的投資"
    psychiatric_comorbidity: "なし"
  trigger:
    event: "母親に管理されていたキャッシュカードを盗み出し、全額引き出して負けた瞬間"
    machine_type: "パチスロ"
    time_of_day: "平日夜"
  inner_monologue_ja: "奨学金を全部溶かした。もう大学にも行けない。親にも合わせる顔がない。死ぬしかない。誰でもいいから殺してほしい。"
  emotional_state:
    arousal_0_100: 10
    despair_0_100: 100
    dominant_emotion: "完全な絶望 × 希死念慮"
  action: "台の前でうなだれ、動けなくなる。店員に声をかけられるまでフリーズする。"
  post_play_state: "失踪し、友人宅やネットカフェを転々とする。"
  source:
    type: "依存症対策センター当事者手記"
    url_or_ref: "ncasa-japan.jp"
    confidence: "高"
  notes: "Despair_rangeが100に到達し、Arousalが完全に消失する「燃え尽き型」。"

- id: R3-A-012
  category: 依存症末期
  profile:
    age_range: "30代"
    occupation: "元営業職"
    family: "単身"
    debt_yen: 15000000
    addiction_severity: "末期（総損失3000万超）"
    gambling_history: "15年"
    visit_motive: "「ちょっとだけなら」という悪魔の囁き"
    psychiatric_comorbidity: "なし"
  trigger:
    event: "親に借金を肩代わりしてもらい完済した翌週、再びホールに入った瞬間"
    machine_type: "パチスロ"
    time_of_day: "休日昼"
  inner_monologue_ja: "借金はゼロになった。だからちょっとぐらいならやっても大丈夫だろう。最初の1回だけ。すぐ帰るから。"
  emotional_state:
    arousal_0_100: 70
    despair_0_100: 10
    dominant_emotion: "自己欺瞞 × 軽い高揚感"
  action: "安心しきった顔でサンドに万札を入れ、リラックスして打ち始める。"
  post_play_state: "2週間で再び300万円の借金を作り、完全な自己嫌悪に陥る。"
  source:
    type: "依存症対策センター当事者手記"
    url_or_ref: "ncasa-japan.jp"
    confidence: "高"
  notes: "Interruptibility = 0.5 (初期) -> 0 (プレイ中)。リセット直後のDespairの低さが、結果的に最大の悲劇を生むメカニズム。"
```

### カテゴリB：不労所得・地主層の補強（金銭プレッシャー希薄層）

```yaml
- id: R3-B-001
  category: 不労所得・地主層
  profile:
    age_range: "60代"
    occupation: "元経営者（引退）"
    family: "妻と同居（子独立済）"
    monthly_income_yen: 2000000
    addiction_severity: "習慣的（毎日来店するが生活破綻なし）"
    gambling_history: "40年"
    visit_motive: "暇つぶし／VIP待遇による承認欲求"
    psychiatric_comorbidity: "なし"
  trigger:
    event: "10万円を投資しても全く見せ場がなく、常連の店員に声をかけられた瞬間"
    machine_type: "Aタイプ（パチスロ）"
    time_of_day: "平日午後"
  inner_monologue_ja: "（店員に対して）今日は全然ダメだね。まあいいや、また明日来るよ。夕飯の時間だからそろそろ帰るか。"
  emotional_state:
    arousal_0_100: 20
    despair_0_100: 10
    dominant_emotion: "退屈 × 軽い落胆"
  action: "残りのメダルをさっさと流し、店員と談笑しながら余裕の表情で席を立つ。"
  post_play_state: "高級車で帰宅し、何事もなかったかのように夕食をとる。"
  source:
    type: "観察・類推（メタ推論）"
    url_or_ref: "メタ推論"
    confidence: "中"
  notes: "Interruptibility = 1.0（いつでも中断可）。Arousal_rangeが極めて低い。投資額に対する痛みが麻痺しているベースライン群。"

- id: R3-B-002
  category: 不労所得・地主層
  profile:
    age_range: "50代"
    occupation: "不動産大家"
    family: "独身"
    monthly_income_yen: 1500000
    addiction_severity: "中等度（金額的ダメージはないが時間は浪費）"
    gambling_history: "20年"
    visit_motive: "刺激の希求／日常の空白を埋めるため"
    psychiatric_comorbidity: "軽度の抑うつ（退屈起因）"
  trigger:
    event: "プレミア演出が発生し、周囲の客が振り返った瞬間"
    machine_type: "AT機"
    time_of_day: "平日午前"
  inner_monologue_ja: "お、引いたか。これで夕方までは時間が潰せるな。（スマホで株価や不動産市況を見ながら片手で消化）"
  emotional_state:
    arousal_0_100: 40
    despair_0_100: 0
    dominant_emotion: "平坦な満足感"
  action: "表情を変えず、スマホを操作しながら片手で淡々とレバーを叩き続ける。"
  post_play_state: "適当なところでヤメて、勝った金で高級寿司を食べて帰る。"
  source:
    type: "観察・類推（メタ推論）"
    url_or_ref: "メタ推論"
    confidence: "中"
  notes: "Sensory_gating_factor = 0.8。外部からの刺激に対しても感情が動かない。作業的プレイ。"

- id: R3-B-003
  category: 不労所得・地主層
  profile:
    age_range: "70代"
    occupation: "資産家（遺産相続）"
    family: "妻と死別"
    monthly_income_yen: 3000000
    addiction_severity: "習慣的（毎日のルーティン）"
    gambling_history: "30年"
    visit_motive: "孤独感の緩和／ホールの音と光の安心感"
    psychiatric_comorbidity: "なし"
  trigger:
    event: "隣の若者が大負けして台パンして帰っていった瞬間"
    machine_type: "海物語（パチンコ）"
    time_of_day: "平日昼間"
  inner_monologue_ja: "若いのは金がなくて余裕がないな。パチンコなんてのは出る時もあれば出ない時もある。ただ座って時間が過ぎればそれでいいんだ。"
  emotional_state:
    arousal_0_100: 10
    despair_0_100: 0
    dominant_emotion: "無関心 × 達観"
  action: "隣をチラリと見ただけで、再び自分の台の液晶に視線を戻し、コーヒーをすする。"
  post_play_state: "夕方のニュースの時間に合わせて静かに退店する。"
  source:
    type: "観察・類推（メタ推論）"
    url_or_ref: "メタ推論"
    confidence: "中"
  notes: "Interruptibility = 1.0。他者のDespairに対して完全に無関心。ホールを「安全なノイズ空間」として利用している。"

- id: R3-B-004
  category: 不労所得・地主層
  profile:
    age_range: "40代"
    occupation: "デイトレーダー"
    family: "独身"
    monthly_income_yen: 5000000
    addiction_severity: "中等度（金額感覚の完全な麻痺）"
    gambling_history: "10年"
    visit_motive: "相場が閉まっている時間の刺激"
    psychiatric_comorbidity: "なし"
  trigger:
    event: "5万円投資して天井に到達し、ショボ連で終わった瞬間"
    machine_type: "スマスロ"
    time_of_day: "平日午後（15時以降）"
  inner_monologue_ja: "相場で動く金に比べたら5万なんて誤差みたいなもんだな。まあ、今日はヒキが弱かった。次行くか。"
  emotional_state:
    arousal_0_100: 30
    despair_0_100: 5
    dominant_emotion: "微かな退屈 × 割り切り"
  action: "一切の未練もなくICカードを抜き、即座に立ち上がる。"
  post_play_state: "タクシーで繁華街へ向かい、飲みに行く。"
  source:
    type: "観察・類推（メタ推論）"
    url_or_ref: "メタ推論"
    confidence: "中"
  notes: "投資額に対するDespairの発火閾値が異常に高い。Arousalもギャンブル自体では跳ね上がらない。"

- id: R3-B-005
  category: 不労所得・地主層
  profile:
    age_range: "60代"
    occupation: "地主"
    family: "妻・同居の息子"
    monthly_income_yen: 1200000
    addiction_severity: "軽度（完全な趣味）"
    gambling_history: "45年"
    visit_motive: "家にいても小言を言われるため"
    psychiatric_comorbidity: "なし"
  trigger:
    event: "大当り中に妻から「お米買ってきて」とLINEが来た瞬間"
    machine_type: "Aタイプ（ジャグラー）"
    time_of_day: "休日夕方"
  inner_monologue_ja: "お、連チャン中だが仕方ない。ペカってるけど、隣の兄ちゃんにこの台譲って帰るか。お米買わないと怒られるしな。"
  emotional_state:
    arousal_0_100: 40
    despair_0_100: 0
    dominant_emotion: "余裕 × 家族優先"
  action: "隣の客に「これ打つ？」と声をかけ、残りのメダルを持って交換所へ向かう。"
  post_play_state: "スーパーでお米を買い、機嫌良く帰宅する。"
  source:
    type: "観察・類推（メタ推論）"
    url_or_ref: "メタ推論"
    confidence: "中"
  notes: "Interruptibility = 1.0の極致。確変・連チャン中であっても、些細な外部要因で未練なくプレイを中断できる特異なベースライン。"

- id: R3-B-006
  category: 不労所得・地主層
  profile:
    age_range: "50代"
    occupation: "会社経営者"
    family: "妻"
    monthly_income_yen: 4000000
    addiction_severity: "中等度"
    gambling_history: "20年"
    visit_motive: "経営の重圧からの解放（何も考えない時間）"
    psychiatric_comorbidity: "軽度の慢性疲労"
  trigger:
    event: "店長がわざわざ挨拶に来て、コーヒーを差し入れた瞬間"
    machine_type: "パチスロ"
    time_of_day: "平日夜"
  inner_monologue_ja: "店長も大変だな。まあ、俺がここで月に何十万も落としてるからな。誰からも決断を迫られないこの空間が一番落ち着く。"
  emotional_state:
    arousal_0_100: 20
    despair_0_100: 0
    dominant_emotion: "優越感 × リラックス"
  action: "軽く会釈してコーヒーを受け取り、ゆったりとした動作でレバーを叩く。"
  post_play_state: "適当な時間で切り上げ、運転手付きの車で帰る。"
  source:
    type: "観察・類推（メタ推論）"
    url_or_ref: "メタ推論"
    confidence: "中"
  notes: "ホールを「接待される安全地帯」として消費している。Despairが発生する余地がない。"

- id: R3-B-007
  category: 不労所得・地主層
  profile:
    age_range: "60代"
    occupation: "自由業（作家・ライター）"
    family: "独身"
    monthly_income_yen: 1000000
    addiction_severity: "軽度"
    gambling_history: "30年"
    visit_motive: "インプットの遮断と単純作業"
    psychiatric_comorbidity: "なし"
  trigger:
    event: "激熱演出が外れて、周囲がざわついた瞬間"
    machine_type: "パチンコ"
    time_of_day: "平日午後"
  inner_monologue_ja: "いまの演出バランスはおかしいな。まあ、ネタにはなるか。しかし今日は回らないな、店を変えるか。"
  emotional_state:
    arousal_0_100: 30
    despair_0_100: 10
    dominant_emotion: "分析的思考 × 呆れ"
  action: "怒ることもなく、冷静に玉の挙動を数分観察した後、席を立つ。"
  post_play_state: "別の店舗へ移動するか、カフェで仕事のメモをまとめる。"
  source:
    type: "観察・類推（メタ推論）"
    url_or_ref: "メタ推論"
    confidence: "中"
  notes: "ギャンブルをメタ認知的に捉えており、没入（Dissociation）が発生しない。"

- id: R3-B-008
  category: 不労所得・地主層
  profile:
    age_range: "70代"
    occupation: "資産家（元地主）"
    family: "妻と同居"
    monthly_income_yen: 1500000
    addiction_severity: "習慣的（毎朝並ぶ）"
    gambling_history: "50年"
    visit_motive: "常連仲間とのコミュニケーション"
    psychiatric_comorbidity: "なし"
  trigger:
    event: "朝イチ、いつもの席が別の客に取られていた瞬間"
    machine_type: "海物語（パチンコ）"
    time_of_day: "朝イチ"
  inner_monologue_ja: "おや、あそこは今日は若いのが座ってるな。仕方ない、隣の台にするか。出玉なんて時の運だ。"
  emotional_state:
    arousal_0_100: 15
    despair_0_100: 5
    dominant_emotion: "穏やかな受容"
  action: "執着することなく、すぐ隣の台に座り、常連仲間と笑顔で挨拶を交わす。"
  post_play_state: "勝敗に関わらず、昼過ぎには常連仲間と昼食へ行く。"
  source:
    type: "観察・類推（メタ推論）"
    url_or_ref: "メタ推論"
    confidence: "中"
  notes: "縄張り意識はあるが、それによるストレス（Despair）の発生が極めて低い。"

- id: R3-B-009
  category: 不労所得・地主層
  profile:
    age_range: "50代"
    occupation: "不労所得（マンション経営）"
    family: "独身"
    monthly_income_yen: 2500000
    addiction_severity: "中等度"
    gambling_history: "25年"
    visit_motive: "純粋なギャンブルの波を楽しむ"
    psychiatric_comorbidity: "なし"
  trigger:
    event: "1日で20万円負けた直後、閉店のアナウンスを聞いた瞬間"
    machine_type: "スマスロ"
    time_of_day: "夜22:45"
  inner_monologue_ja: "おお、もうこんな時間か。今日はやられたな。まあ、明日またリベンジすればいい。家賃収入が入るし痛くはない。"
  emotional_state:
    arousal_0_100: 40
    despair_0_100: 10
    dominant_emotion: "ゲームとしての敗北感 × 経済的余裕"
  action: "伸びをして、店員に愛想よく手を挙げて退店する。"
  post_play_state: "負けたこと自体をエンターテインメントとして消費している。"
  source:
    type: "観察・類推（メタ推論）"
    url_or_ref: "メタ推論"
    confidence: "中"
  notes: "20万円という大敗であっても、Monthly_incomeが緩衝材となりDespairが発火しない。"

- id: R3-B-010
  category: 不労所得・地主層
  profile:
    age_range: "40代"
    occupation: "投資家"
    family: "既婚"
    monthly_income_yen: 6000000
    addiction_severity: "軽度"
    gambling_history: "5年"
    visit_motive: "確率と期待値の遊び"
    psychiatric_comorbidity: "なし"
  trigger:
    event: "期待値の高い台（ハイエナ台）を見つけた瞬間"
    machine_type: "AT機"
    time_of_day: "平日夕方"
  inner_monologue_ja: "これは期待値3000円くらいあるな。打っておくか。結果はどうあれ試行回数を稼ぐだけだ。"
  emotional_state:
    arousal_0_100: 30
    despair_0_100: 0
    dominant_emotion: "機械的な作業意識"
  action: "淡々と千円札を投入し、スマホで期待値計算ツールを見ながら無表情で打つ。"
  post_play_state: "期待値通りに出なくても全く気にせず帰る。"
  source:
    type: "観察・類推（メタ推論）"
    url_or_ref: "メタ推論"
    confidence: "中"
  notes: "ギャンブルを完全に「投資・作業」としてメタ化しており、感情の波（Arousal/Despair）が意図的に切り離されている。"

- id: R3-B-011
  category: 不労所得・地主層
  profile:
    age_range: "60代"
    occupation: "資産家夫人"
    family: "夫と同居"
    monthly_income_yen: 1000000
    addiction_severity: "習慣的"
    gambling_history: "15年"
    visit_motive: "買い物のついで、派手な演出を見たい"
    psychiatric_comorbidity: "なし"
  trigger:
    event: "大当りしてドル箱が積み上がった瞬間"
    machine_type: "パチンコ"
    time_of_day: "休日昼"
  inner_monologue_ja: "あら、出たわ。でも箱を積まれると足元が狭くて嫌ね。店員さん、早く流してくれないかしら。"
  emotional_state:
    arousal_0_100: 20
    despair_0_100: 0
    dominant_emotion: "物理的な煩わしさ"
  action: "出玉の喜びよりも、パーソナルシステム（各台計数機）でないことへの不満を顔に出し、店員を呼ぶ。"
  post_play_state: "景品を日用品に換えて、デパートへ買い物に向かう。"
  source:
    type: "観察・類推（メタ推論）"
    url_or_ref: "メタ推論"
    confidence: "中"
  notes: "出玉によるArousalの上昇がなく、むしろ物理的な快適性を重視する極端な例。"

- id: R3-B-012
  category: 不労所得・地主層
  profile:
    age_range: "50代"
    occupation: "元プロスポーツ選手"
    family: "離婚"
    monthly_income_yen: 1500000
    addiction_severity: "中等度"
    gambling_history: "10年"
    visit_motive: "過去のヒリヒリした勝負の代替"
    psychiatric_comorbidity: "なし"
  trigger:
    event: "設定6（最高設定）を確信した瞬間"
    machine_type: "パチスロ"
    time_of_day: "平日昼間"
  inner_monologue_ja: "間違いなく上（高設定）だ。でも、昔の試合みたいなヒリつく感覚はないな。金は増えるが、なんか物足りない。"
  emotional_state:
    arousal_0_100: 50
    despair_0_100: 0
    dominant_emotion: "勝利への確信 × 慢性的な渇望感"
  action: "ブン回す（高速で打つ）ことはせず、あくびをしながら適当なペースで打ち続ける。"
  post_play_state: "5000枚出しても「こんなもんか」と冷めた表情で退店する。"
  source:
    type: "観察・類推（メタ推論）"
    url_or_ref: "メタ推論"
    confidence: "中"
  notes: "勝利が確定していてもArousalが上がりきらない。ギャンブルの刺激が過去の体験（競技）の代替になり得ていない。"
```

### カテゴリC：中年現役男性（サラリーマン・自営・公務員）

```yaml
- id: R3-C-001
  category: 中年現役男性
  profile:
    age_range: "40代"
    occupation: "サラリーマン（管理職）"
    family: "妻と小学生の子2人"
    debt_yen: 1500000
    addiction_severity: "中等度（小遣いの範疇を超えキャッシング常態化）"
    gambling_history: "15年"
    visit_motive: "仕事のストレス発散／家庭に帰りたくない"
    psychiatric_comorbidity: "慢性的な疲労・ストレス"
  trigger:
    event: "仕事帰りの21時、妻から「何時に帰る？」とLINEが来た瞬間"
    machine_type: "Aタイプ（ジャグラー等）"
    time_of_day: "平日夜21:30"
  inner_monologue_ja: "『仕事が立て込んでて遅くなる』と。帰っても小言を言われるだけだ。ボーナス引くまで帰れない。"
  emotional_state:
    arousal_0_100: 60
    despair_0_100: 50
    dominant_emotion: "煩わしさ × 逃避"
  action: "LINEの通知をスワイプして消し、メダルを追加投資する。"
  post_play_state: "閉店まで打ち切り、罪悪感を抱えながら深夜に帰宅。"
  source:
    type: "依存症対策センター当事者手記"
    url_or_ref: "ncasa-japan.jp"
    confidence: "高"
  notes: "Interruptibility = 0.3。Stigma_barrierが高く、家族への嘘が常態化している。Time_cost_efficiencyを意識しつつも止められない。"

- id: R3-C-002
  category: 中年現役男性
  profile:
    age_range: "50代"
    occupation: "自営業"
    family: "妻（夫婦関係冷え切り）"
    debt_yen: 3000000
    addiction_severity: "重度（仕事資金の流用）"
    gambling_history: "25年"
    visit_motive: "「借金があるからギャンブルをやらないといけない」という倒錯"
    psychiatric_comorbidity: "なし"
  trigger:
    event: "大負けして帰り際、妻からの問い詰めを思い出した瞬間"
    machine_type: "AT機"
    time_of_day: "休日夕方"
  inner_monologue_ja: "違うよ、借金があるからギャンブルをやらないといけないんだよ！普通に働いてたって返せる額じゃないんだから。"
  emotional_state:
    arousal_0_100: 70
    despair_0_100: 60
    dominant_emotion: "正当化 × 苛立ち"
  action: "負けた怒りを正当化し、タバコを強く吸い込みながらイライラと退店する。"
  post_play_state: "帰宅後、妻に問い詰められ逆ギレする。"
  source:
    type: "依存症対策センター当事者手記（家族手記）"
    url_or_ref: "ncasa-japan.jp"
    confidence: "高"
  notes: "認知の歪みの典型例。Despairを抑え込むために『投資の正当性』を脳内で構築している。"

- id: R3-C-003
  category: 中年現役男性
  profile:
    age_range: "40代"
    occupation: "営業職"
    family: "妻・子"
    debt_yen: 0
    addiction_severity: "軽〜中等度（小遣いの範囲だが時間は浪費）"
    gambling_history: "20年"
    visit_motive: "給料日のルーティン／ささやかな贅沢"
    psychiatric_comorbidity: "なし"
  trigger:
    event: "給料日当日、財布に10万円入っている状態でのプレイ開始時"
    machine_type: "パチスロ"
    time_of_day: "給料日（25日）夜"
  inner_monologue_ja: "今日は給料日だ。財布には余裕がある。5万までは突っ込めるぞ。ここで出せば今月は小遣いが倍になる。"
  emotional_state:
    arousal_0_100: 80
    despair_0_100: 10
    dominant_emotion: "期待感 × 万能感"
  action: "普段は座らない荒い波の機種に座り、強気で投資を開始する。"
  post_play_state: "5万円負けて激しい後悔に襲われる。"
  source:
    type: "観察・類推（給料日の行動パターン）"
    url_or_ref: "メタ推論"
    confidence: "中"
  notes: "Payday_sensitivity = 1.0。資金的余裕が一時的にArousalを引き上げ、リスク許容度を狂わせる。"

- id: R3-C-004
  category: 中年現役男性
  profile:
    age_range: "30代後半"
    occupation: "会社員（夜勤あり）"
    family: "結婚目前の彼女"
    debt_yen: 2000000
    addiction_severity: "重度（クレジットカードのキャッシング依存）"
    gambling_history: "10年"
    visit_motive: "過去の10万円勝ちの幻影を追う"
    psychiatric_comorbidity: "虚無感・焦燥感"
  trigger:
    event: "天井ストッパーで単発終了し、手持ちが尽きた瞬間"
    machine_type: "パチスロ"
    time_of_day: "平日夜"
  inner_monologue_ja: "またやってしまった。結婚資金に手をつけてしまった。彼女にバレたら終わりだ。でも取り返すしかない。"
  emotional_state:
    arousal_0_100: 85
    despair_0_100: 85
    dominant_emotion: "焦燥感 × 自己嫌悪"
  action: "頭を抱え、台のデータランプを睨みつけながら次の借り入れを計算する。"
  post_play_state: "自転車操業が加速し、数ヶ月後に破綻する。"
  source:
    type: "依存症対策センター当事者手記"
    url_or_ref: "ncasa-japan.jp"
    confidence: "高"
  notes: "Stigma_barrierが極端に高い（結婚破棄の恐怖）。ArousalとDespairが拮抗している状態。"

- id: R3-C-005
  category: 中年現役男性
  profile:
    age_range: "40代"
    occupation: "公務員"
    family: "妻・子2人"
    debt_yen: 1000000
    addiction_severity: "中等度"
    gambling_history: "18年"
    visit_motive: "職場の人間関係のストレス"
    psychiatric_comorbidity: "なし"
  trigger:
    event: "同じ職場の同僚らしき人物がホールに入ってきたのを見た瞬間"
    machine_type: "パチンコ"
    time_of_day: "平日夕方"
  inner_monologue_ja: "やばい、〇〇課長じゃないか？こんなところで会ったら何を言われるか分からない。顔を隠さなきゃ。"
  emotional_state:
    arousal_0_100: 90
    despair_0_100: 40
    dominant_emotion: "焦燥感 × 隠蔽衝動"
  action: "慌ててマスクを深く被り、下を向いて打ち出しを止める。気配が消えるまで動かない。"
  post_play_state: "見つからずに済んだが、集中が切れ、早々に退店する。"
  source:
    type: "観察・類推（Stigmaの顕在化）"
    url_or_ref: "メタ推論"
    confidence: "高"
  notes: "Stigma_barrier = 1.0。社会的地位の喪失リスクがプレイのInterruptibilityを強制的に1.0に引き上げる。"

- id: R3-C-006
  category: 中年現役男性
  profile:
    age_range: "50代"
    occupation: "会社員（窓際族）"
    family: "妻"
    debt_yen: 500000
    addiction_severity: "中等度"
    gambling_history: "20年"
    visit_motive: "有休消化の暇つぶし、家庭内の居場所のなさ"
    psychiatric_comorbidity: "なし"
  trigger:
    event: "平日昼間、ふと周囲が専業（プロ）と老人ばかりだと気づいた瞬間"
    machine_type: "パチスロ（Aタイプ）"
    time_of_day: "平日昼間"
  inner_monologue_ja: "周りを見るとジジババか、スロプロみたいな若いやつばっかりだな。俺、平日の真っ昼間にスーツ着て何やってるんだろうな。"
  emotional_state:
    arousal_0_100: 30
    despair_0_100: 60
    dominant_emotion: "虚無感 × 自己嫌悪"
  action: "ため息をつき、スマホで会社のメールを無意味にチェックする。"
  post_play_state: "定時まで時間を潰し、仕事帰りを装って帰宅する。"
  source:
    type: "観察・類推"
    url_or_ref: "メタ推論"
    confidence: "中"
  notes: "中年特有の「社会からの疎外感」がDespairを緩やかに上昇させる。"

- id: R3-C-007
  category: 中年現役男性
  profile:
    age_range: "40代"
    occupation: "運送業"
    family: "独身"
    debt_yen: 4000000
    addiction_severity: "重度"
    gambling_history: "20年"
    visit_motive: "ギャンブルで一発当てて仕事を辞めたい"
    psychiatric_comorbidity: "なし"
  trigger:
    event: "投資5万でようやくATに入ったが、上乗せなしで駆け抜けた瞬間"
    machine_type: "AT機"
    time_of_day: "休日夜"
  inner_monologue_ja: "ふざけんなよ！遠隔だろこれ。せっかくの休みがこれで終わりかよ。明日からまたあのクソみたいな仕事かよ！"
  emotional_state:
    arousal_0_100: 100
    despair_0_100: 80
    dominant_emotion: "激怒 × 被害妄想"
  action: "台のボタンを強く叩き（台パン）、舌打ちをしながらメダルを叩きつけるように下皿に落とす。"
  post_play_state: "怒りが収まらず、帰りにコンビニで酒を大量に買ってやけ酒。"
  source:
    type: "観察・類推"
    url_or_ref: "メタ推論"
    confidence: "中"
  notes: "労働の苦痛（Time_cost_efficiencyの低さ）への代償が満たされなかったことによる怒りの爆発。"

- id: R3-C-008
  category: 中年現役男性
  profile:
    age_range: "40代"
    occupation: "ITエンジニア"
    family: "妻・子（小遣い制）"
    debt_yen: 0
    addiction_severity: "軽度"
    gambling_history: "15年"
    visit_motive: "小遣い稼ぎ、趣味"
    psychiatric_comorbidity: "なし"
  trigger:
    event: "1万円の投資で3万円の回収が確定し、キリが良い時間になった瞬間"
    machine_type: "パチスロ"
    time_of_day: "平日夜20:00"
  inner_monologue_ja: "よし、プラス2万だ。これ以上追うと確率が収束して飲まれる。ここでヤメて、帰りにちょっといいビールでも買って帰ろう。"
  emotional_state:
    arousal_0_100: 60
    despair_0_100: 0
    dominant_emotion: "達成感 × 冷静な計算"
  action: "即座にICカードを抜き、周囲の台を少しだけ確認して交換所へ向かう。"
  post_play_state: "小遣いが増えた喜びで、家族にも優しく接する。"
  source:
    type: "観察・類推"
    url_or_ref: "メタ推論"
    confidence: "高"
  notes: "Interruptibility = 1.0。中等度以下のサラリーマンの理想的な成功体験モデル。"

- id: R3-C-009
  category: 中年現役男性
  profile:
    age_range: "50代"
    occupation: "工場勤務"
    family: "妻・大学生の子"
    debt_yen: 2000000
    addiction_severity: "重度"
    gambling_history: "30年"
    visit_motive: "子供の学費のプレッシャーからの逃避"
    psychiatric_comorbidity: "なし"
  trigger:
    event: "財布の残金がなくなり、キャッシュカードで銀行アプリの残高を見た瞬間"
    machine_type: "パチンコ"
    time_of_day: "休日昼"
  inner_monologue_ja: "今月は子供の学費の引き落としがあるのに。どうしよう、足りない。でも、もう一万円だけ打てば確変に入る気がする。給料日までなんとか誤魔化せるか。"
  emotional_state:
    arousal_0_100: 80
    despair_0_100: 70
    dominant_emotion: "焦り × ギャンブル的思考"
  action: "アプリを閉じ、ため息をつきながらコンビニATMへ向かう。"
  post_play_state: "学費に手をつけてしまい、妻に嘘をつき続けることになる。"
  source:
    type: "依存症対策センター当事者手記"
    url_or_ref: "ncasa-japan.jp"
    confidence: "高"
  notes: "家族のイベント（学費等）に対する罪悪感がDespairを高めるが、認知の歪みにより「勝って返す」というArousalへ変換される。"

- id: R3-C-010
  category: 中年現役男性
  profile:
    age_range: "40代"
    occupation: "自営業"
    family: "妻・子"
    debt_yen: 5000000
    addiction_severity: "末期一歩手前"
    gambling_history: "20年"
    visit_motive: "仕事の資金繰りの現実逃避"
    psychiatric_comorbidity: "なし"
  trigger:
    event: "取引先からの電話が鳴ったが、大当たりが始まった瞬間"
    machine_type: "AT機"
    time_of_day: "平日午後"
  inner_monologue_ja: "取引先からの電話だ。出ないと仕事が飛ぶ。でもいま上乗せ特化ゾーン中だ。手を止めたくない。あとで折り返せばいい。"
  emotional_state:
    arousal_0_100: 95
    despair_0_100: 40
    dominant_emotion: "興奮 × 優先順位の崩壊"
  action: "着信音を消し、スマホを裏返してレバーを叩き続ける。"
  post_play_state: "大勝したが、取引先からの信用を失い、長期的には負債が増える。"
  source:
    type: "依存症対策センター当事者手記"
    url_or_ref: "ncasa-japan.jp"
    confidence: "高"
  notes: "Interruptibility = 0。Arousalが社会的責任（Stigma_barrier）を突破した瞬間。"

- id: R3-C-011
  category: 中年現役男性
  profile:
    age_range: "30代後半"
    occupation: "サラリーマン"
    family: "妻（妊娠中）"
    debt_yen: 1000000
    addiction_severity: "中等度"
    gambling_history: "10年"
    visit_motive: "もうすぐ自由がなくなることへの焦り"
    psychiatric_comorbidity: "マタニティブルー（夫側）"
  trigger:
    event: "妻から「体調が悪いから早く帰ってきて」と連絡が来た瞬間"
    machine_type: "パチスロ"
    time_of_day: "平日夜"
  inner_monologue_ja: "帰らなきゃいけないのは分かってる。でも、子供が生まれたらもうパチンコなんて一生できないんだ。今出てるこのメダルを取り切るまでは。"
  emotional_state:
    arousal_0_100: 70
    despair_0_100: 60
    dominant_emotion: "葛藤 × 未練"
  action: "「今向かってる」と嘘のLINEを返し、高速で消化を続ける。"
  post_play_state: "帰宅後、妻に冷たくされ自己嫌悪に陥る。"
  source:
    type: "観察・類推"
    url_or_ref: "メタ推論"
    confidence: "中"
  notes: "ライフステージの変化に対する焦りが、逆にギャンブルへの執着を強める現象。"

- id: R3-C-012
  category: 中年現役男性
  profile:
    age_range: "50代"
    occupation: "管理職"
    family: "妻・子独立"
    debt_yen: 0
    addiction_severity: "軽度"
    gambling_history: "30年"
    visit_motive: "仕事帰りの習慣"
    psychiatric_comorbidity: "なし"
  trigger:
    event: "隣の若い客が、台の知識をひけらかしながら大声で話しているのを聞いた瞬間"
    machine_type: "パチスロ"
    time_of_day: "平日夜"
  inner_monologue_ja: "うるさい若造だな。こっちは仕事で疲れて静かに打ちたいんだ。スマホで調べた知識だけで勝てるなら苦労しないよ。"
  emotional_state:
    arousal_0_100: 30
    despair_0_100: 10
    dominant_emotion: "苛立ち × 世代的優越感"
  action: "舌打ちをして、イヤホンのノイズキャンセリングを強める。"
  post_play_state: "ストレスが溜まり、早めに切り上げる。"
  source:
    type: "観察・類推"
    url_or_ref: "メタ推論"
    confidence: "中"
  notes: "Sensory_gating_factorが他者のノイズによって破られ、不快感がプレイ続行の意欲（Arousal）を下げる。"

- id: R3-C-013
  category: 中年現役男性
  profile:
    age_range: "40代"
    occupation: "会社員"
    family: "既婚"
    debt_yen: 300000
    addiction_severity: "中等度"
    gambling_history: "20年"
    visit_motive: "過去の成功体験の追体験"
    psychiatric_comorbidity: "なし"
  trigger:
    event: "昔のパチスロ4号機時代によく似た演出が出現した瞬間"
    machine_type: "スマスロ"
    time_of_day: "休日午後"
  inner_monologue_ja: "おお、この演出！懐かしいな。あの頃は毎日のように勝ってたな。よし、今日はあの時みたいに万枚出してやる。"
  emotional_state:
    arousal_0_100: 85
    despair_0_100: 0
    dominant_emotion: "ノスタルジー × 興奮"
  action: "顔をほころばせ、リールを止める手に力が入る。"
  post_play_state: "結局出玉は伸びず、昔とは違うという現実に直面する。"
  source:
    type: "観察・類推"
    url_or_ref: "メタ推論"
    confidence: "中"
  notes: "ノスタルジーが強力なArousalのトリガーとして機能する中年特有のモデル。"

- id: R3-C-014
  category: 中年現役男性
  profile:
    age_range: "40代"
    occupation: "自営業"
    family: "独身"
    debt_yen: 2000000
    addiction_severity: "重度"
    gambling_history: "15年"
    visit_motive: "借金返済のプレッシャー"
    psychiatric_comorbidity: "なし"
  trigger:
    event: "天井到達直前で、最も恩恵の少ないボーナスに当選してしまった瞬間"
    machine_type: "パチスロ"
    time_of_day: "平日夜"
  inner_monologue_ja: "うわ、まじかよ。ここでレギュラーかよ。天井まであと少しだったのに。これじゃ今日使った3万円がパーだ。"
  emotional_state:
    arousal_0_100: 90
    despair_0_100: 80
    dominant_emotion: "激しい落胆 × 怒り"
  action: "天を仰ぎ、下皿のメダルを乱暴に箱に移す。貧乏ゆすりが止まらない。"
  post_play_state: "取り返すために別の台に移動し、さらに傷口を広げる。"
  source:
    type: "観察・類推"
    url_or_ref: "メタ推論"
    confidence: "高"
  notes: "サンクコスト効果が最も強く働く瞬間。Despairの急上昇が、撤退（Interruptibility）ではなく更なるArousal（怒りによる続行）を引き起こす。"
```

### カテゴリD：精神疾患併発（プレイ中の感情変調・衝動性）

```yaml
- id: R3-D-001
  category: 精神疾患併発
  profile:
    age_range: "30代"
    occupation: "休職中（元営業職）"
    family: "親と同居"
    debt_yen: 500000
    addiction_severity: "中等度（現実逃避型依存）"
    gambling_history: "2年"
    visit_motive: "家に居たくない／社会からの逃避"
    psychiatric_comorbidity: "うつ病（抑うつ状態）"
  trigger:
    event: "パチンコの激しい光と音の中で、ふと我に返る瞬間"
    machine_type: "パチンコ"
    time_of_day: "平日昼間"
  inner_monologue_ja: "仕事も行けず、こんな平日昼間に何をしているんだろう。でも、ここにいる間だけは嫌なことを全部忘れられる。何も考えたくない。"
  emotional_state:
    arousal_0_100: 30
    despair_0_100: 80
    dominant_emotion: "無気力 × 感覚の麻痺"
  action: "虚ろな目で盤面の光を見つめ、ハンドルを握り続ける。"
  post_play_state: "退店時、現実に戻った瞬間に強烈な自己嫌悪と抑うつに襲われる。"
  source:
    type: "依存症対策センター当事者手記"
    url_or_ref: "ncasa-japan.jp"
    confidence: "高"
  notes: "Mood_lability = 低いが、ベースラインのDespairが高い。Sensory_gating_factor = 0.2（パチンコ台の刺激だけが心地よい麻酔となっている）。"

- id: R3-D-002
  category: 精神疾患併発
  profile:
    age_range: "40代"
    occupation: "自営業"
    family: "妻・子"
    debt_yen: 4000000
    addiction_severity: "重度"
    gambling_history: "15年"
    visit_motive: "全能感と散財衝動"
    psychiatric_comorbidity: "双極性障害（躁状態）"
  trigger:
    event: "大当りが連続し、出玉が急速に増え始めた瞬間"
    machine_type: "パチスロ（AT機）"
    time_of_day: "休日午後"
  inner_monologue_ja: "俺は天才だ！この台の波が完全に読める。店中のメダルを全部出してやる。誰も俺を止められない！"
  emotional_state:
    arousal_0_100: 100
    despair_0_100: 0
    dominant_emotion: "過剰な全能感 × 異常な高揚"
  action: "周囲の客に見せつけるように、乱暴かつ高速でレバーを叩き、ボタンを強打する。店員に横柄な態度をとる。"
  post_play_state: "勝った金で後先考えず高額な買い物（散財）をする。"
  source:
    type: "クリニック症例・ブログ類推"
    url_or_ref: "ohishi-clinic.or.jp"
    confidence: "高"
  notes: "Mood_lability = 1.0。躁状態における異常なArousalの跳ね上がりと、Impulse_control = 0（衝動の完全な解放）。"

- id: R3-D-003
  category: 精神疾患併発
  profile:
    age_range: "20代"
    occupation: "フリーター"
    family: "一人暮らし"
    debt_yen: 1000000
    addiction_severity: "中等度"
    gambling_history: "5年"
    visit_motive: "衝動制御の困難／刺激への渇望"
    psychiatric_comorbidity: "ADHD（注意欠如・多動症）"
  trigger:
    event: "天井まで残り200ゲームのところで、突然手持ちの現金が尽きた瞬間"
    machine_type: "パチスロ"
    time_of_day: "平日夜"
  inner_monologue_ja: "ああああ！もう待てない！あと少しなのに！金、金、金！早く金をおろさないと誰かに取られる！"
  emotional_state:
    arousal_0_100: 95
    despair_0_100: 30
    dominant_emotion: "極度の焦燥感 × 衝動性"
  action: "台にスマホやタバコを乱雑に投げ置き、ATMへ全速力で走る。周囲の迷惑は目に入らない。"
  post_play_state: "落ち着いた後、自分がなぜあそこまで焦っていたのか理解できず自己嫌悪に陥る。"
  source:
    type: "当事者ブログ"
    url_or_ref: "個人ブログ類推"
    confidence: "中"
  notes: "Impulse_control = 0.1。一時的に芽生えた欲望を全く制御できず、直情的な行動に出る特性。"

- id: R3-D-004
  category: 精神疾患併発
  profile:
    age_range: "50代"
    occupation: "主婦（パート）"
    family: "夫・子（育児放棄傾向）"
    debt_yen: 3000000
    addiction_severity: "重度（離婚危機）"
    gambling_history: "10年"
    visit_motive: "過去のトラウマと現在の苦痛からの逃避"
    psychiatric_comorbidity: "パニック発作・解離傾向"
  trigger:
    event: "激しい演出が外れ、借金総額が頭をよぎった瞬間"
    machine_type: "パチンコ"
    time_of_day: "平日夕方"
  inner_monologue_ja: "また外れた。どうしよう、夫が帰ってくる前に夕飯を作らなきゃ。心臓がバクバクする。息が苦しい。でも席から立てない。体が動かない。"
  emotional_state:
    arousal_0_100: 90
    despair_0_100: 90
    dominant_emotion: "パニック × 身体的硬直"
  action: "冷や汗をかきながら、震える手でお札をサンドに押し込み続ける。視線は定まらない。"
  post_play_state: "心と行動がバラバラになり、自分が自分でないような解離感覚を抱えたまま駐車場へ向かう。"
  source:
    type: "依存症対策センター当事者手記"
    url_or_ref: "ncasa-japan.jp"
    confidence: "高"
  notes: "Dissociation_tendency = 0.9。心（やめたい・帰らなきゃ）と行動（打ち続ける）が完全に乖離している状態。"

- id: R3-D-005
  category: 精神疾患併発
  profile:
    age_range: "30代"
    occupation: "無職"
    family: "実家暮らし"
    debt_yen: 1500000
    addiction_severity: "中等度"
    gambling_history: "8年"
    visit_motive: "躁状態と鬱状態の波の合間の刺激"
    psychiatric_comorbidity: "双極性障害（鬱状態への移行期）"
  trigger:
    event: "昨日までの万能感が嘘のように消え、投資が止まらない瞬間"
    machine_type: "パチスロ"
    time_of_day: "平日午後"
  inner_monologue_ja: "昨日はあんなに勝てる気がしたのに。今日は全然ダメだ。体が重い。でも昨日出たあの光と音が忘れられない。またあの感覚を味わいたい。"
  emotional_state:
    arousal_0_100: 40
    despair_0_100: 70
    dominant_emotion: "気分の急転直下 × 執着"
  action: "ため息をつきながら、機械的にメダルを入れ続ける。"
  post_play_state: "完全な抑うつ状態に陥り、数日間寝込む。"
  source:
    type: "観察・類推"
    url_or_ref: "メタ推論"
    confidence: "中"
  notes: "Mood_labilityによるArousalの急激な低下。しかし依存行動自体は止まらない。"

- id: R3-D-006
  category: 精神疾患併発
  profile:
    age_range: "20代"
    occupation: "派遣社員"
    family: "独身"
    debt_yen: 500000
    addiction_severity: "中等度"
    gambling_history: "3年"
    visit_motive: "衝動性と過集中の対象"
    psychiatric_comorbidity: "ADHD（過集中傾向）"
  trigger:
    event: "朝イチから打ち始め、気づけば夕方になっていた瞬間"
    machine_type: "パチスロ"
    time_of_day: "休日夕方"
  inner_monologue_ja: "えっ、もう17時？朝から水も飲んでない。トイレにも行ってない。でもこのモードが終わるまでは立てない。"
  emotional_state:
    arousal_0_100: 90
    despair_0_100: 10
    dominant_emotion: "過集中 × 時間感覚の喪失"
  action: "猛烈なスピードでリールを回し続け、周囲の出来事に一切反応しない。"
  post_play_state: "退店後、急激な疲労感と空腹に襲われる。"
  source:
    type: "当事者ブログ・類推"
    url_or_ref: "個人ブログ類推"
    confidence: "中"
  notes: "ADHD特有のハイパーフォーカス（過集中）。Interruptibility = 0。生理的欲求すらブロックされる。"

- id: R3-D-007
  category: 精神疾患併発
  profile:
    age_range: "40代"
    occupation: "無職（障害年金受給）"
    family: "単身"
    debt_yen: 0
    addiction_severity: "軽度（少額だが毎日の日課）"
    gambling_history: "10年"
    visit_motive: "トラウマからの自己防衛"
    psychiatric_comorbidity: "PTSD"
  trigger:
    event: "ホール内の大音量とフラッシュに包まれている瞬間"
    machine_type: "1円パチンコ"
    time_of_day: "平日昼間"
  inner_monologue_ja: "この音がいい。爆音で耳を塞いでくれる。光が視界を埋め尽くしてくれる。過去の嫌な記憶が入り込む隙間がない。"
  emotional_state:
    arousal_0_100: 20
    despair_0_100: 40
    dominant_emotion: "安心感 × 感覚遮断"
  action: "耳栓もつけず、目を細めながら盤面の強烈なフラッシュを浴び続ける。"
  post_play_state: "閉店まで少額で粘り、静かなアパートに帰るのを嫌がる。"
  source:
    type: "観察・類推"
    url_or_ref: "メタ推論"
    confidence: "中"
  notes: "Sensory_gating_factor = 0。外部刺激が苦痛ではなく「防音壁」として機能している。"

- id: R3-D-008
  category: 精神疾患併発
  profile:
    age_range: "30代"
    occupation: "フリーランス"
    family: "独身"
    debt_yen: 2000000
    addiction_severity: "重度"
    gambling_history: "7年"
    visit_motive: "衝動性と怒りのコントロール不全"
    psychiatric_comorbidity: "ADHD・二次的な怒り"
  trigger:
    event: "隣の客が自分の台を覗き込んできた瞬間"
    machine_type: "パチスロ"
    time_of_day: "休日午後"
  inner_monologue_ja: "なんだこいつ、ジロジロ見やがって！俺がハマってるのを笑ってるのか！？ふざけんな！"
  emotional_state:
    arousal_0_100: 100
    despair_0_100: 20
    dominant_emotion: "激しい怒り × 衝動性"
  action: "隣の客をものすごい剣幕で睨みつけ、台を強く叩いて威嚇する。"
  post_play_state: "店員に注意され、トラブルになり退店させられる。"
  source:
    type: "当事者ブログ・類推"
    url_or_ref: "個人ブログ類推"
    confidence: "中"
  notes: "Impulse_control = 0。些細な外部刺激に対する過剰防衛と衝動的行動。"

- id: R3-D-009
  category: 精神疾患併発
  profile:
    age_range: "50代"
    occupation: "休職中"
    family: "妻と別居中"
    debt_yen: 6000000
    addiction_severity: "末期"
    gambling_history: "20年"
    visit_motive: "死を望むための口実作り"
    psychiatric_comorbidity: "重度のうつ病・希死念慮"
  trigger:
    event: "大負けが確定し、残金がゼロになった瞬間"
    machine_type: "パチンコ"
    time_of_day: "平日夜"
  inner_monologue_ja: "これで全部なくなった。もう言い訳できない。これでやっと、死ぬ理由ができた。"
  emotional_state:
    arousal_0_100: 10
    despair_0_100: 100
    dominant_emotion: "不気味な安堵感 × 希死念慮"
  action: "暴れることもなく、静かに深く息を吐き、ゆっくりと立ち上がる。"
  post_play_state: "帰路、線路や高いビルを探しながら歩く。"
  source:
    type: "依存症対策センター当事者手記"
    url_or_ref: "ncasa-japan.jp"
    confidence: "高"
  notes: "Despairが100に達した瞬間に、Arousalがゼロになり「死への安心感」に反転する特異なフェーズ。"

- id: R3-D-010
  category: 精神疾患併発
  profile:
    age_range: "20代"
    occupation: "水商売"
    family: "独身"
    debt_yen: 1500000
    addiction_severity: "中等度"
    gambling_history: "4年"
    visit_motive: "気分の波のコントロール不全"
    psychiatric_comorbidity: "双極性障害（混合状態）"
  trigger:
    event: "大当たりが確定し、派手なファンファーレが鳴った瞬間"
    machine_type: "パチスロ"
    time_of_day: "深夜"
  inner_monologue_ja: "やった、当たった！…でも、これで借金が返せるわけじゃない。なんで私こんなことしてるんだろう。悲しい。でも嬉しい。"
  emotional_state:
    arousal_0_100: 90
    despair_0_100: 80
    dominant_emotion: "歓喜と号泣の混在"
  action: "大当たりを消化しながら、ポロポロと涙を流して泣きながら打つ。"
  post_play_state: "勝ったのにも関わらず、ひどく落ち込んだ状態で帰宅する。"
  source:
    type: "観察・臨床的推論"
    url_or_ref: "メタ推論"
    confidence: "中"
  notes: "Mood_lability = 1.0。ArousalとDespairが同時に高ぶる「混合状態」の典型的なプレイスタイル。"
```

## 2. メタ観察とシミュレーション用パラメータの考察

### 2.1. カテゴリA（末期）とカテゴリB（不労所得）の対極的メカニズム

**カテゴリA（末期）の特異性：解離とArousalの高止まり**

末期ギャンブラーの心理において最も顕著な現象は、**「Despair（絶望）が100に達しても、Arousal（覚醒・興奮）が低下しない、あるいはさらに上昇する」**という点。通常であれば絶望感が極まれば行動は停止（アパシー状態）するはずだが、依存症末期においては「打つこと自体が絶望からの唯一の麻酔」として機能する。

**パラメータ設計への適用**: despair_0_100 >= 90 かつ arousal_0_100 >= 90 の交差点において、dissociation_tendency（解離傾向）の係数を指数関数的に上昇させるモデルを推奨する。財布が完全に空になる（interruptibility = 0）まで、いかなる外部介入（家族からのLINE、店員の声かけ、隣客の騒音）も完全に無視（Sensory Gating）して行動を継続する。

**カテゴリB（不労所得）の特異性：感情の低ボラティリティ**

金銭的プレッシャーが希薄なカテゴリBは、arousal_rangeおよびdespair_rangeの振幅が極めて狭い。

**パラメータ設計への適用**: monthly_income_yen が一定の閾値を超えるペルソナに対しては、演出の成否や残金の減少に対する arousal と despair の反応係数を大幅に減衰させるダンプ関数（減衰器）を実装する必要がある。少しでも煩わしいことがあれば、いつでも容易に退店判断を下せる（interruptibility = 1.0）。

### 2.2. カテゴリC（中年現役男性）における認知の歪みと社会的ストレス

女性層（R1）が「孤独感」から逃避するのに対し、中年男性層は「社会的責任（仕事・家庭）」から逃避する傾向が強い。

**Payday Sensitivity（給料日感度）の極大化**: 給料日（25日など）の直後は、財布の中の現金額が多いため、一時的な全能感と期待感が醸成される。資金的余裕がある時のみ、普段は打たない荒い波の機種（ハイリスク機）に座る傾向が強まる。

**認知の歪みによるDespairの隠蔽と正当化**: 妻からの追求や仕事の重圧など、外部からのストレス（stigma_barrier）に対して、彼らは「借金があるからパチンコで取り返さなければならない」という論理的倒錯を用いて自己正当化を図る。

**パラメータ設計への適用**: 外部からのストレス入力（家族からの連絡等）があった際、Despairを直接上昇させるのではなく、防衛機制としてArousalと「怒り・苛立ち（Irritation）」のパラメータを瞬間的に高め、帰宅を遅らせてプレイを続行させるアルゴリズムが、中年男性層のリアリティを生む。

### 2.3. カテゴリD（精神疾患併発）が与えるパラメータの変調

**Mood Lability（気分の易変性）と双極性障害**: 躁状態にあるペルソナは、mood_lability が極大化し、わずかなプラスのフィードバック（小当たりなど）で Arousal が100まで振り切れる。

**Impulse Control（衝動制御）の喪失とADHD**: ADHD傾向のあるペルソナは、impulse_control パラメータが恒常的に低い。フラストレーションが高まる場面において「待つ」「冷静に判断する」ことができず、即座にATMへ走るなどの突発的行動（Actionの即時発火）や、飲食・排泄を忘れるほどの過集中（Hyper-focus）を引き起こす。

**うつ病・PTSDとSensory Gating（感覚の遮断）**: うつ状態やPTSDを抱えるペルソナは、強烈な光や音（パチンコ台の刺激）を浴びることで、現実の孤独感やトラウマのフラッシュバックから防衛する。sensory_gating_factor を極端に低く（またはマスキング効果を高く）設定し、外部環境を遮断し、目の前の台のノイズだけを「安全な防音壁」として受け入れるトンネルビジョン状態を再現する。

## 3. ソース評価と今後のデータ適用に向けた提言

### 3.1. ソースの信頼性とバイアスの評価

**依存症対策センター当事者手記・クリニック症例報告**: 本レポートの主軸として活用した当事者手記や大石クリニックの症例報告は、回復施設や自助グループに繋がった「底つき（最悪の事態）」を経験した当事者自身の言葉。記述の生々しさ、感情の解像度、絶望の深さ（借金1500万、万引き、ヤミ金、希死念慮）については極めて高い信頼性を持つ。

**バイアスへの留意**: これらの手記は「回復後の視点」から過去の狂気を振り返って書かれているため、「今思えば狂っていた」「悪魔の声」といった自己分析的なバイアスが含まれている。シミュレーションにおける「プレイ中のリアルタイムな独白」へ変換する際は、この「後知恵の反省」を取り除き、当時の視野狭窄と狂気に満ちた現在進行形の思考（Raw Monologue）として抽出・再構成する処理を行った。

**SNS・ブログ・メタ観察からの類推**: カテゴリB（不労所得層）やカテゴリC（中年男性の日常的プレイ）については、重度の依存症患者のような劇的な破綻を伴わないため、公的機関のレポートには上がりにくい。そのため本レポートでは、収集された断片的な事実をベースに、シミュレーション用ペルソナとして合理的な行動パターンをメタ推論によって構築した。

### 3.2. シミュレーションモデルへの実装に向けた提言

**「Interruptibility（中断可能性）」の動的・非線形な変化**: エージェントが席を立つかどうかの判定関数には、単なる所持金や時間だけでなく、「感情状態と疾患特性によるロックイン効果」を組み込むべき。カテゴリAやDの一部では、所持金が尽きても席を立たず、借金をしてでも続行するという行動ツリーを最優先で発火させる必要がある。

**感情・パラメータの可視化による異常性の表現（動画・ログへの出力）**: カテゴリによって「ArousalとDespairの相関」が根本的に異なることを、システムログや可視化UIで表現することが、本モデルの最大の価値となる。例えば、カテゴリC（サラリーマン）は給料の増減に比例して感情が正常に上下動するが、カテゴリA（末期）は常にパラメータがレッドゾーン（Arousal 90+, Despair 90+）に張り付いたまま動かない。**この「パラメータの張り付きと麻痺」こそが、依存症末期の異常性を動画上で表現する最も強力な証左となる**。

## 引用元

- ncasa-japan.jp - 体験談（令和５年３月掲載）依存症対策全国センター
- ncasa-japan.jp - 体験談（令和４年10月掲載）
- ncasa-japan.jp - 体験談（令和５年４月掲載）
- ohishi-clinic.or.jp - ギャンブル依存症 体験談 大石クリニック
- ohishi-clinic.or.jp - ギャンブル依存症の症状 大石クリニック
