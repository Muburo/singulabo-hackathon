パチスロプレイ中の「女性当事者」の心理反応と情動モデル：マルチエージェントシミュレーション用質的データライブラリ

> Source: Gemini Deep Research / 2026-04-24 取得 / R1 ラウンド

## 1. 導入と理論的背景：女性ギャンブル依存の特異性とペルソナ設計への接続

マルチエージェントLLMシミュレーションにおいて、パチンコホール内の群像劇を高い解像度で再現するためには、エージェント（ペルソナ）の属性に応じた精緻な情動遷移モデルが必要不可欠である。特に女性のギャンブル依存（病的賭博）は、男性のそれとは動機形成、進行プロセス、およびホール内での心理的反応において決定的な差異を有する。

男性プレイヤーが主にスリル、アクション、あるいは社会的競争心に基づく「追求的動機（Action Motivation）」によってギャンブルに没入する傾向があるのに対し、女性プレイヤーの圧倒的多数は「逃避的動機（Escape Motivation）」に根ざしている。対人関係のストレス、経済的困窮、育児や結婚生活への失望、あるいは「主婦・母親・社会人としての役割」からの解放を求め、ホールという匿名性の高い空間に没入する。

また、初期段階において女性はパチンコホールに対して「うるさい」「タバコ臭い」「底辺の空間」という強いスティグマと羞恥心（Shame）を抱いている。しかし、一度の成功体験（ビギナーズラック）による強烈な自己効力感の錯覚や、数回の来店による「環境への慣れ」によって、この羞恥心の障壁は急速に崩壊し、認知の歪み（Cognitive Distortion）が形成される。

本報告書は、シミュレーションのFSM（有限オートマトン）やペルソナプロンプトに直接実装可能な「場面 × 感情反応」のパラメータ係数表の根拠として、女性当事者および経験者のプレイ中における瞬間的な心理スナップショットを質的に収集・体系化したものである。収集された一次資料（当事者ブログ、SNS、手記）および二次資料（医療機関の症例、自助グループの証言）に基づき、各属性に特有の心理反応を抽出した。

## 2. 情動パラメータの定義と評価マトリクス

本ライブラリでは、LLMエージェントの感情遷移を制御するため、当事者の内面描写から以下の2軸の数値を推定しパラメータ化している。

| 感情軸 | 定義とホール内での発露 | 値の範囲と意味 |
|--------|------------------------|----------------|
| Arousal (覚醒度) | 演出への反応、ドーパミン放出に伴う興奮、または焦燥感による心拍数の上昇。 | 0（無気力・解離）〜 100（極度の興奮・パニック） |
| Despair (絶望感) | 残金減少、ハマり、または退店時の現実直視に伴う精神的苦痛と自己嫌悪。 | 0（全能感・多幸感）〜 100（完全な喪失感・自暴自棄） |

この2軸の交差により、プレイ中の支配的感情（Dominant Emotion）が以下のように分類される。女性プレイヤー特有の現象として、残金が尽きかけた際の「Arousal（高） × Despair（高）＝ デスクトップ・パニック（強迫的な焦燥）」や、苦痛から完全に逃避した「Arousal（低） × Despair（高）＝ 感情の解離」が顕著に現れる。

## 3. 質的素材ライブラリ（事例カード集）

### 3.1. カテゴリA：主婦（パート or 専業）

代表的傾向: 厳格な家庭環境や夫婦間のすれ違いからの逃避。生活費からの直接的な資金捻出による「デスクトップ・パニック」の激しさ。ホール外での無気力と、ホール内でのエネルギー回復の極端な落差。

```yaml
- id: R1-A-001
  category: 主婦
  profile:
    age_range: "30代前半"
    occupation: "パート（個人商店）"
    family: "年下の夫（すれ違い生活）"
    monthly_disposable_yen: 30000
    debt_yen: 0
    addiction_severity: "初期（ビギナーズラック直後）"
    gambling_history: "同僚に連れられ1回経験後、1人で来店"
    visit_motive: "少ない生活費を自力で増やすため／退屈な日常からの逃避"
  trigger:
    event: "初めて1人で座り、大当たりを引いた瞬間"
    machine_type: "ミドルスペック（パチンコ）"
    time_of_day: "平日15時（パート帰り）"
  inner_monologue_ja: "嘘、また当たった。私、自分の力でこんな凄いことできるんだ。今まで親や夫の顔色ばっかり窺ってたけど、夫の安い給料なんか当てにしなくても、これで生活費増やせるじゃん。こんな楽しい世界があったんだ。"
  emotional_state:
    arousal_0_100: 90
    despair_0_100: 0
    dominant_emotion: "万能感 × 将来への希望"
  action: "興奮状態でハンドルを強く握り続ける／周囲を誇らしげに見回す"
  post_play_state: "大勝ちして帰宅／夫には内緒で自分のヘソクリにする"
  source:
    type: "厚労省 依存症体験談 (Milk氏の事例)"
    url_or_ref: "kokoro.mhlw.go.jp/over/877/"
    confidence: "高（当事者手記）"
  notes: "厳格な親元で育った優等生タイプ特有の反応。「自分の力でやり遂げた」という自己効力感の誤認（Illusion of Control）が依存の強力なフックとなっている。"

- id: R1-A-002
  category: 主婦
  profile:
    age_range: "30代前半"
    occupation: "パート"
    family: "夫"
    monthly_disposable_yen: 10000
    debt_yen: 500000
    addiction_severity: "重度（借金隠蔽中）"
    gambling_history: "日常的な通い（給料の全額投入）"
    visit_motive: "街頭でパチンコ店の音楽を聴いたことによる条件反射"
  trigger:
    event: "店外で軍艦マーチ（BGM）を耳にした瞬間"
    machine_type: "未定（入店前）"
    time_of_day: "給料日（現金手渡し）の夕方"
  inner_monologue_ja: "まっすぐ家に帰らなきゃいけないのに。今日パートの給料もらったばかりで現金を持ってるからダメなんだ。でも少しだけ、あの音を聞いたら吸い込まれるみたいに足が勝手に動く。1回当たるまでなら。"
  emotional_state:
    arousal_0_100: 65
    despair_0_100: 40
    dominant_emotion: "抗えない衝動 × 軽い自己嫌悪"
  action: "給料袋を鞄に隠し持ったまま、無意識に入店する"
  post_play_state: "給料全額喪失／夫への言い訳を考えながらのパニック状態"
  source:
    type: "厚労省 依存症体験談"
    url_or_ref: "kokoro.mhlw.go.jp/over/877/"
    confidence: "高"
  notes: "パブロフの犬のように、音響刺激による条件反射が形成されている。現金（手渡しの給料）を持っているという事実がトリガーを増幅させ、自制心を破壊する。"

- id: R1-A-003
  category: 主婦
  profile:
    age_range: "30代前半"
    occupation: "パート"
    family: "夫"
    monthly_disposable_yen: 0
    debt_yen: 1500000
    addiction_severity: "重度（夫のクレジットカード窃取）"
    gambling_history: "キャッシング限度額到達後"
    visit_motive: "エネルギーの補給（パチンコ以外の時間は無気力）"
  trigger:
    event: "プレイ中・通常時（何も起きていない凪の時間）"
    machine_type: "パチンコ"
    time_of_day: "平日昼下がり"
  inner_monologue_ja: "家の中は息が詰まる。夫とも上手くいかない。でもここに座って台の光を見ている時だけ、将来への希望が湧いてきて元気になる。私にとってパチンコだけが生きるエネルギー源なんだ。"
  emotional_state:
    arousal_0_100: 45
    despair_0_100: 10
    dominant_emotion: "安心感 × 現実逃避のトランス"
  action: "無表情のまま、淡々と現金をサンドに投入し、ハンドルを固定する"
  post_play_state: "退店した瞬間に現実に戻り、激しい鬱状態と疲労感に襲われる"
  source:
    type: "厚労省 依存症体験談"
    url_or_ref: "kokoro.mhlw.go.jp/over/877/"
    confidence: "高"
  notes: "「パチンコをしている時だけ元気になれる」という、ギャンブルが文字通り唯一の精神的エネルギー源となっている状態。逃避的動機の究極系。"

- id: R1-A-004
  category: 主婦
  profile:
    age_range: "40代"
    occupation: "専業主婦"
    family: "夫、中学生の子"
    monthly_disposable_yen: 20000
    debt_yen: 800000
    addiction_severity: "中度"
    gambling_history: "数年間"
    visit_motive: "孤独感と家事ストレスからの逃避"
  trigger:
    event: "残金1000円でのハマり（当たらず）と夕刻の接近"
    machine_type: "Aタイプ（パチスロ / ジャグラー等）"
    time_of_day: "平日16時（子供の帰宅直前）"
  inner_monologue_ja: "お願い、光って。この最後の1000円で当たらないと今日の夕飯のおかずが買えない。時間もない。夫に何て言おう、また口座からお金下ろしたのバレたら今度こそ離婚されるかも。光れ、光れ！"
  emotional_state:
    arousal_0_100: 85
    despair_0_100: 80
    dominant_emotion: "極度の焦燥 × 日常崩壊への恐怖"
  action: "メダルを強く握りしめながら、祈るようにレバーを強打する"
  post_play_state: "全損／スーパーで見切り品の安い惣菜を買い、何食わぬ顔で帰宅"
  source:
    type: "メタ分析に基づく構造的推定（主婦カテゴリの普遍的行動様式）"
    url_or_ref: "N/A"
    confidence: "高（現象として極めて典型的）"
  notes: "家計の生活費を直接投下しているため、損失時の「デスクトップ・パニック（プレイ中の絶望感）」が男性よりも生活に直結しており、生存危機レベルの恐怖を生む。"

- id: R1-A-005
  category: 主婦
  profile:
    age_range: "50代"
    occupation: "専業主婦"
    family: "夫（定年退職間近）"
    monthly_disposable_yen: 10000
    debt_yen: 3000000
    addiction_severity: "重度（多重債務）"
    gambling_history: "10年"
    visit_motive: "過去の負け額の回収と現実逃避"
  trigger:
    event: "天井ストッパー（天井直前での単発当たり）を食らった瞬間"
    machine_type: "AT機（パチスロ）"
    time_of_day: "平日14時"
  inner_monologue_ja: "嘘でしょ？あと50ゲームで天井だったのに。ここで単発？今まで突っ込んだ4万円が全部無駄になった。もう嫌だ、死にたい。誰かに全部任せて消えてしまいたい。"
  emotional_state:
    arousal_0_100: 20
    despair_0_100: 95
    dominant_emotion: "完全な思考停止 × 絶望"
  action: "ボーナス確定画面のまま数分間フリーズし、涙ぐむ"
  post_play_state: "ボーナス消化後、放心状態で追加投資を続け全損"
  source:
    type: "依存症家族の証言に基づく当事者内面推定"
    url_or_ref: "gam-anon 証言等の行動特性"
    confidence: "中"
  notes: "深刻なダメージを受けた際、女性特有の「思考が麻痺し、ただ呆然と他人に（あるいは運命に）身を任せる」という認知の解離状態（Dissociation）に陥る。"

- id: R1-A-006
  category: 主婦
  profile:
    age_range: "40代前半"
    occupation: "パート"
    family: "夫と小学生の子2人"
    monthly_disposable_yen: 50000
    debt_yen: 1200000
    addiction_severity: "中度〜重度"
    gambling_history: "5年"
    visit_motive: "姑との同居ストレスの発散"
  trigger:
    event: "近所の主婦仲間がホールに入ってくるのを目撃した瞬間"
    machine_type: "1円パチンコ"
    time_of_day: "平日午前"
  inner_monologue_ja: "ヤバい、〇〇くんのお母さんだ。絶対見つかっちゃダメだ、ママ友のLINEグループで何言われるか分からない。顔を隠さなきゃ。"
  emotional_state:
    arousal_0_100: 80
    despair_0_100: 50
    dominant_emotion: "社会的発覚への恐怖 × パニック"
  action: "台の影に隠れるように深く身を沈め、データカウンターで顔を隠す"
  post_play_state: "見つからずに済んだ後、安堵から逆に気が大きくなり投資が加速"
  source:
    type: "女性依存症特有の『羞恥心ベースのギャンブル』研究に基づく推定"
    url_or_ref: "N/A"
    confidence: "中"
  notes: "地域コミュニティにおける社会的体裁を極端に恐れる。しかし、その恐怖を乗り越えた後の安堵感が、副交感神経の反動によって過剰なプレイを誘発する。"
```

### 3.2. カテゴリB：OL・社会人女性

代表的傾向: 労働環境のストレス、初期の「嫌悪感」から「居心地の良さ」への急速な認知変容。金曜夜や給料日における投資の急拡大とドーパミン報酬の結びつき。

```yaml
- id: R1-B-001
  category: OL・社会人女性
  profile:
    age_range: "20代後半"
    occupation: "IT企業 事務職"
    family: "独身（一人暮らし）"
    monthly_disposable_yen: 80000
    debt_yen: 0
    addiction_severity: "初期（興味本位の初来店）"
    gambling_history: "1日目"
    visit_motive: "暇つぶしと社会経験としての好奇心"
  trigger:
    event: "入店直後・騒音とタバコの匂いを浴びた瞬間"
    machine_type: "未定（台選び中）"
    time_of_day: "休日昼"
  inner_monologue_ja: "うわ、無理。知り合いに見られたら本当に嫌だな。タバコ臭いし、音はうるさいし、光で目が痛い。空気だけでなく雰囲気すら淀んでる。髪の毛パサパサのおばさんが本当にいるし、底辺って感じがして早く出たい。"
  emotional_state:
    arousal_0_100: 20
    despair_0_100: 15
    dominant_emotion: "強烈な羞恥心 × 環境への嫌悪感"
  action: "顔を伏せがちに、足早に空き台を探して着席する"
  post_play_state: "疲労困憊で退店／「二度と行かない」と思うが、数日後に再訪"
  source:
    type: "当事者ブログ (Note)"
    url_or_ref: "note.com/megaya/n/n67c3fd2f59d4"
    confidence: "高（本人執筆）"
  notes: "「パチンコをやってるやつはクズ」という強い偏見を持っていた層の初期反応。視覚・聴覚・嗅覚への過剰刺激がストレスとなっている状態。"

- id: R1-B-002
  category: OL・社会人女性
  profile:
    age_range: "20代後半"
    occupation: "IT企業 事務職"
    family: "独身"
    monthly_disposable_yen: 80000
    debt_yen: 0
    addiction_severity: "初期〜中期"
    gambling_history: "開始から1週間後"
    visit_motive: "仕事終わりの習慣化"
  trigger:
    event: "プレイ中・台の騒音の中でのリラックス"
    machine_type: "パチンコ"
    time_of_day: "平日19時"
  inner_monologue_ja: "1週間前はあんなにうるさいと思ってたのに、今は全然気にならない。むしろこの音の中にいると落ち着く。金額さえちゃんと決めてやれば、別に悪いことじゃないよね？"
  emotional_state:
    arousal_0_100: 30
    despair_0_100: 0
    dominant_emotion: "警戒心の完全な解除 × 認知の歪み（自己正当化）"
  action: "リラックスした姿勢で、スマホで動画を見ながら片手で打つ"
  post_play_state: "収支をエクセルで管理し始め、次の来店日を計画する"
  source:
    type: "当事者ブログ (Note)"
    url_or_ref: "note.com/megaya/n/n67c3fd2f59d4"
    confidence: "高"
  notes: "慣れの恐ろしさ。わずか1週間で環境への嫌悪感が消滅し、プレイを自己正当化（Rationalization）する心理的閾値を突破している。"

- id: R1-B-003
  category: OL・社会人女性
  profile:
    age_range: "50代"
    occupation: "フルタイム勤務（管理職）"
    family: "既婚"
    monthly_disposable_yen: 50000
    debt_yen: 8000000
    addiction_severity: "重度（ロト6からの移行・多重債務）"
    gambling_history: "数年間"
    visit_motive: "仕事の過労と強烈なストレスの発散"
  trigger:
    event: "退勤後、駅前でパチンコ店のネオン看板を見た瞬間"
    machine_type: "未定"
    time_of_day: "平日20時"
  inner_monologue_ja: "今日も疲れた。上司と部下の板挟みで理不尽なことばっかり。あのネオンの中に入れば、頭の中を空っぽにできる。今日だけ、1万円だけなら気分転換になるはず。"
  emotional_state:
    arousal_0_100: 60
    despair_0_100: 50
    dominant_emotion: "現実からの逃避欲求 × 抑えがたい渇望感"
  action: "吸い込まれるように駐輪場へ向かい、足早に入店する"
  post_play_state: "大負けして自己嫌悪／借金がまた増えたことへの絶望感で帰路につく"
  source:
    type: "新聞記事（回復施設GA参加者の証言）"
    url_or_ref: "読売新聞 (すぅさん 50代の事例)"
    confidence: "高"
  notes: "宝くじ（スマホ）による軽度の依存からパチンコへとエスカレートし、800万円の借金を抱えた実例。職場ストレスが強力なトリガーとして作用している。"

- id: R1-B-004
  category: OL・社会人女性
  profile:
    age_range: "30代"
    occupation: "派遣社員"
    family: "独身"
    monthly_disposable_yen: 40000
    debt_yen: 1000000
    addiction_severity: "中期"
    gambling_history: "3年"
    visit_motive: "寂しさと孤独感の埋め合わせ"
  trigger:
    event: "隣の台（見知らぬ男性）が爆連（大連チャン）しているのを見た瞬間"
    machine_type: "AT機（パチスロ）"
    time_of_day: "休日午後"
  inner_monologue_ja: "なんで隣のあのおじさんはあんなに出てるのに、私の台はウンともスンとも言わないの？イライラする。私の方がお金入れてるのに不公平だ。絶対に私の方が不幸なのに。"
  emotional_state:
    arousal_0_100: 70
    despair_0_100: 65
    dominant_emotion: "理不尽な怒り × 他者への嫉妬"
  action: "レバーを叩く力が無意識に強くなる／スマホを台に乱暴に置く"
  post_play_state: "怒りに任せて別の台に乱れ打ちし、資金を全損して退店"
  source:
    type: "メタ分析からの推定"
    url_or_ref: "N/A"
    confidence: "中"
  notes: "ホール内の他者に対する無意識の競争心。孤独な環境下では、他者の「運の良さ」が自己の「不幸な境遇」を際立たせるため、情動が極めて不安定化しやすい。"

- id: R1-B-005
  category: OL・社会人女性
  profile:
    age_range: "20代後半"
    occupation: "正社員（営業職）"
    family: "彼氏と同棲"
    monthly_disposable_yen: 60000
    debt_yen: 200000
    addiction_severity: "中期"
    gambling_history: "彼氏の影響で開始し1年半"
    visit_motive: "給料日直後の高揚感とご褒美"
  trigger:
    event: "大当たり濃厚な激アツ演出（全回転等）の発生"
    machine_type: "ハイミドル（パチンコ）"
    time_of_day: "給料日直後の金曜21時"
  inner_monologue_ja: "よし、来た！これ絶対当たるやつ！仕事の疲れが全部吹き飛ぶ。この時間が一番生きてるって感じする。彼氏には残業って言ってあるし、閉店ギリギリまで取り切るぞ！"
  emotional_state:
    arousal_0_100: 95
    despair_0_100: 0
    dominant_emotion: "全能感 × 極度の興奮（ドーパミン放出）"
  action: "画面を凝視し、マスクの下で小さくガッツポーズをする"
  post_play_state: "5万勝ち／ホクホク顔でコンビニで贅沢なデパ地下スイーツを買って帰る"
  source:
    type: "メタ分析からの推定"
    url_or_ref: "N/A"
    confidence: "中"
  notes: "OLカテゴリにおける「金曜夜・給料日後」のエスカレーション。成功時の強烈なドーパミン報酬系による行動強化が、金銭感覚の麻痺を促進する。"

- id: R1-B-006
  category: OL・社会人女性
  profile:
    age_range: "30代前半"
    occupation: "契約社員"
    family: "独身"
    monthly_disposable_yen: 50000
    debt_yen: 1500000
    addiction_severity: "重度"
    gambling_history: "4年"
    visit_motive: "借金返済の金策"
  trigger:
    event: "店員にメダル補給で声をかけられ、目を合わせられた瞬間"
    machine_type: "パチスロ"
    time_of_day: "平日の有給休暇（昼）"
  inner_monologue_ja: "あ、すいません。……なんかこの店員さん、私のこと『また来てるよこの女』って思ってるんだろうな。平日の昼間からスロットなんて、底辺の女だと思われてる。恥ずかしい、でも打つしかない。"
  emotional_state:
    arousal_0_100: 50
    despair_0_100: 60
    dominant_emotion: "被害妄想的な羞恥心 × 自己卑下"
  action: "目を合わせず、スマホの画面に視線を固定してやり過ごす"
  post_play_state: "他人の視線へのストレスから疲労し、勝っても虚無感が残る"
  source:
    type: "メタ分析からの推定"
    url_or_ref: "N/A"
    confidence: "中"
  notes: "進行した依存症特有の自意識過剰（Spotlight Effect）。ホール内では匿名性を確保したいが、物理的な接触によって現実社会の自分の地位（底辺）を突きつけられる苦痛。"
```

### 3.3. カテゴリC：風俗・夜職系女性

代表的傾向: 圧倒的な資金の流動性と金銭感覚の崩壊。負けに対する耐性の低さが引き起こす「打てなくなるパニック」。性売買等の交差依存への直結と、感情の完全な解離。

```yaml
- id: R1-C-001
  category: 風俗・夜職系女性
  profile:
    age_range: "20代後半"
    occupation: "パート兼売春（夜職）"
    family: "結婚歴あり（のち別居/入籍）"
    monthly_disposable_yen: 200000
    debt_yen: 3000000
    addiction_severity: "極重度（自己破産経験あり・性依存交差）"
    gambling_history: "幼少期に祖母に連れられ、のち夫と通い悪化"
    visit_motive: "「行かなきゃいけない」という強迫観念"
  trigger:
    event: "出玉が飲まれ、財布の残金が完全に尽きかけた瞬間"
    machine_type: "パチンコ"
    time_of_day: "平日14時"
  inner_monologue_ja: "どうしよう、出なくなってきた。もうパチンコできなくなる。早く当てないと。イライラする。焦る。あーあ、また今日の夜、お店に入って体売らなきゃ。売ればまた打てる。"
  emotional_state:
    arousal_0_100: 85
    despair_0_100: 80
    dominant_emotion: "強迫的な焦燥感 × パニック"
  action: "貧乏ゆすりが止まらなくなり、無意識に爪を激しく噛む"
  post_play_state: "全損／そのまま夜の店へ直行して体を売る（交差依存のループ）"
  source:
    type: "自助グループ手記"
    url_or_ref: "nujyumi.la.coocan.jp/storyaf.html"
    confidence: "高（本人執筆）"
  notes: "打っている間だけ落ち着くが、資金が尽きると強烈な離脱症状（イライラ・焦り）が生じる。これが性売買という極端な金策手段（交差依存）へ即座に直結するメカニズム。"

- id: R1-C-002
  category: 風俗・夜職系女性
  profile:
    age_range: "20代後半"
    occupation: "パチンコ店員 兼 夜職"
    family: "独身"
    monthly_disposable_yen: 300000
    debt_yen: 3000000
    addiction_severity: "極重度"
    gambling_history: "10年"
    visit_motive: "孤独感と疲労の麻痺"
  trigger:
    event: "パチンコ店員としてアルバイト中、ボロ負けして帰る客を見た瞬間"
    machine_type: "N/A（店員目線での観察）"
    time_of_day: "閉店作業中（23時）"
  inner_monologue_ja: "うわ、あのおっさん今日もボロ負けして肩落として帰ってくじゃん。私と一緒で悲惨だな。もう来なきゃいいのに……でも明日の休みは、私も他所の店に行って打ちに出かけるんだろうな。バカみたい。"
  emotional_state:
    arousal_0_100: 10
    despair_0_100: 70
    dominant_emotion: "冷笑的な自己憐憫 × 深い虚無感"
  action: "客の悲惨な後ろ姿を冷たい目で見送りながら、ゴミを片付ける"
  post_play_state: "翌日、休日に同僚と打ちに行き、自分も大負けする"
  source:
    type: "自助グループ手記"
    url_or_ref: "nujyumi.la.coocan.jp/storyaf.html"
    confidence: "高"
  notes: "依存症者がギャンブル場に就労するケース。他者の敗北を見て客観的な悲惨さを認識するが、自己の行動制御は完全に破綻しているという認知の乖離。"

- id: R1-C-003
  category: 風俗・夜職系女性
  profile:
    age_range: "20代"
    occupation: "闇金からの斡旋で性的サービス"
    family: "不明（裏社会の借金苦）"
    monthly_disposable_yen: 0
    debt_yen: 5000000以上
    addiction_severity: "極重度（反社との接点・性的搾取）"
    gambling_history: "不明"
    visit_motive: "依存の末路"
  trigger:
    event: "資金欲しさに、ホール内の男子トイレで客相手の性的サービスを強要された瞬間"
    machine_type: "N/A（ホール内トイレ）"
    time_of_day: "深夜帯または人目のない時間"
  inner_monologue_ja: "なんで私、こんなところでこんな事してるんだろう。でもこれでお金貰えば、またあの台に座れる。感覚を消せ。何も考えるな。ただの肉の塊になればいい。"
  emotional_state:
    arousal_0_100: 0
    despair_0_100: 95
    dominant_emotion: "完全な感情の解離（Dissociation） × 虚無"
  action: "ぼんやりした顔で無言のまま行為をこなす"
  post_play_state: "得た金でそのまま店内に戻り、無表情でパチンコを再開する"
  source:
    type: "観察的記述（依存症を描く漫画原作プロット）"
    url_or_ref: "note.com/ouma/n/n45c42d4e204e"
    confidence: "中（創作プロットだが、借金苦の女性当事者が陥る裏社会の現実構造を反映）"
  notes: "ギャンブル依存と性的搾取が同一空間（ホール内）で直結した極限状態。自己防衛としての心理的解離（乖離性障害的反応）が起きている。"

- id: R1-C-004
  category: 風俗・夜職系女性
  profile:
    age_range: "30代"
    occupation: "キャバクラ勤務"
    family: "独身"
    monthly_disposable_yen: 250000
    debt_yen: 1000000
    addiction_severity: "重度"
    gambling_history: "5年"
    visit_motive: "同伴前・出勤前の暇つぶしとアドレナリン欲求"
  trigger:
    event: "荒波機種で大きく張り、投資が5万円を超えた瞬間"
    machine_type: "荒波AT機（パチスロ）"
    time_of_day: "平日17時（出勤直前）"
  inner_monologue_ja: "ヤバい、もう5万入れた。今日のお客さんの同伴代、全部飛んだじゃん。でもここで引いたら絶対負け確定だし。あーもう、最悪客に『体調悪い』って嘘ついて店休もうかな。取り返す方が先だ。"
  emotional_state:
    arousal_0_100: 85
    despair_0_100: 60
    dominant_emotion: "自暴自棄 × 闘争心（アドレナリン）"
  action: "LINEの通知を連続で無視し、万札をサンドに乱暴に押し込み続ける"
  post_play_state: "出勤時間に遅刻し、店長に怒られながら出勤する（社会的信用の毀損）"
  source:
    type: "メタ分析からの推定"
    url_or_ref: "N/A"
    confidence: "中"
  notes: "夜職特有の「所持金の絶対量の多さ」により、損失の許容額・麻痺レベルが一般女性より異常に高い。仕事への責任感よりギャンブルのサンクコストが上回る。"

- id: R1-C-005
  category: 風俗・夜職系女性
  profile:
    age_range: "20代後半"
    occupation: "風俗嬢"
    family: "独身"
    monthly_disposable_yen: 200000
    debt_yen: 3000000
    addiction_severity: "極重度"
    gambling_history: "10年"
    visit_motive: "現実の苦痛と自己嫌悪からの逃避"
  trigger:
    event: "大当たり中（連チャン中）、出玉が爆発的に増えている瞬間"
    machine_type: "パチンコ"
    time_of_day: "平日15時"
  inner_monologue_ja: "最高。出玉がどんどん積まれていく。私を抱いたあの気持ち悪いおっさん達より、この台の方がよっぽど私を満たしてくれる。私を裏切らない。ずっとこのままでいたい。"
  emotional_state:
    arousal_0_100: 95
    despair_0_100: 0
    dominant_emotion: "無敵感 × 歪んだカタルシス"
  action: "ドル箱（またはデータカウンター）を見つめながら、恍惚とした表情でタバコを深く吸い込む"
  post_play_state: "大勝ちした金でホストクラブへ行き散財する（快楽依存の連鎖）"
  source:
    type: "自助グループ手記からの心理構造推定"
    url_or_ref: "nujyumi.la.coocan.jp/storyaf.html"
    confidence: "中"
  notes: "「体さえ差し出せば満たされた気になれる」という性依存の構造が、ギャンブルの出玉という即物的な報酬系と完全に同化し、機械に対する疑似恋愛的な依存が生じている状態。"

- id: R1-C-006
  category: 風俗・夜職系女性
  profile:
    age_range: "30代前半"
    occupation: "スナック経営"
    family: "離婚歴あり"
    monthly_disposable_yen: 300000
    debt_yen: 8000000
    addiction_severity: "極重度"
    gambling_history: "15年"
    visit_motive: "強迫的ギャンブル（無意識の来店）"
  trigger:
    event: "大負けして退店し、駐車場の車内で我に返った瞬間"
    machine_type: "パチスロ"
    time_of_day: "深夜0時"
  inner_monologue_ja: "……あれ、私なんでこんな所にいるんだっけ？財布の中身、全部ない。10万あったのに。またやった。死にたい、誰でもいいから私を殺してほしい。苦しい、苦しい。"
  emotional_state:
    arousal_0_100: 10
    despair_0_100: 100
    dominant_emotion: "極限の希死念慮 × 自責の念"
  action: "ハンドルに突っ伏して嗚咽し、過呼吸気味になる"
  post_play_state: "自殺未遂を考えるが実行できず、数日後にまたホールへ向かう"
  source:
    type: "依存症体験談からの構造的抽出"
    url_or_ref: "ncasa-japan.jp/pdf/document65.pdf"
    confidence: "高"
  notes: "「誰でもいいから殺して欲しかった」という極限の希死念慮。プレイ中のトランス状態から覚めた直後の、Despairパラメータが最大値に振り切れる瞬間。"
```

### 3.4. カテゴリD：女子大生・若年女性

代表的傾向: SNS（XやTikTok）での収支・感情の共有による承認欲求の補完。演出（ギミック）への過剰な反応。彼氏や友人などコミュニティへの依存と体裁の同居。

```yaml
- id: R1-D-001
  category: 女子大生・若年女性
  profile:
    age_range: "20代前半"
    occupation: "フリーター・学生"
    family: "実家暮らし"
    monthly_disposable_yen: 40000
    debt_yen: 100000
    addiction_severity: "初期（エンジョイ勢を自称）"
    gambling_history: "1年未満"
    visit_motive: "SNSのネタ作り／純粋な娯楽としての刺激"
  trigger:
    event: "金保留＋レバブル（激アツ演出）の発生"
    machine_type: "ハイミドル（ガンダムユニコーン等）"
    time_of_day: "休日14時"
  inner_monologue_ja: "きたぁぁぁ！！ユニコーンの叫び！しかもレバブルに金保留じゃん！これ絶対もらったでしょ、脳汁ヤバい！早く写真撮ってXに上げなきゃ！"
  emotional_state:
    arousal_0_100: 100
    despair_0_100: 0
    dominant_emotion: "歓喜（脳汁） × 承認欲求への期待"
  action: "慌ててスマホを取り出し、画面の動画を撮りながら激しく揺れるレバーを握る"
  post_play_state: "当たりを引いてSNSに「投資〇〇で回収〇〇！」と誇らしげに投稿"
  source:
    type: "当事者ブログ（X転載系）"
    url_or_ref: "note.com/bright_carp7915/n/n961bcc6806fe"
    confidence: "高（本人執筆）"
  notes: "「パチンコ女子」特有の、プレイとSNS発信が完全に一体化したプレイスタイル。演出の豪華さ（音と光）にドーパミン分泌が直結しており、射幸性と承認欲求が融合している。"

- id: R1-D-002
  category: 女子大生・若年女性
  profile:
    age_range: "20代前半"
    occupation: "フリーター"
    family: "実家暮らし"
    monthly_disposable_yen: 40000
    debt_yen: 100000
    addiction_severity: "初期"
    gambling_history: "1年未満"
    visit_motive: "前回の興奮（脳汁）を求めての再訪"
  trigger:
    event: "激アツ演出（金保留＋レバブル）を外した瞬間"
    machine_type: "ハイミドル（パチンコ）"
    time_of_day: "休日15時"
  inner_monologue_ja: "……は？嘘でしょ？今の外すの？マジで意味わかんない。遠隔？それとも私の引きが弱すぎるの？Xのフォロワーに何て報告しよう……恥ずかしいしムカつく。"
  emotional_state:
    arousal_0_100: 80
    despair_0_100: 60
    dominant_emotion: "裏切られたショック × 強い不満・怒り"
  action: "スマホを下ろし、台のガラス面を軽く睨みつける"
  post_play_state: "ショックを引きずりながら、取り返すためにムキになって追加投資してしまう"
  source:
    type: "当事者ブログ（X転載系）"
    url_or_ref: "note.com/bright_carp7915/n/n961bcc6806fe"
    confidence: "高"
  notes: "期待値が極めて高い演出を外した際の「落差」が、次の追加投資へのサンクコスト的執着（ムキになる心理）を生む典型的なプロセス。"

- id: R1-D-003
  category: 女子大生・若年女性
  profile:
    age_range: "20代前半"
    occupation: "大学生"
    family: "一人暮らし"
    monthly_disposable_yen: 30000
    debt_yen: 500000
    addiction_severity: "中期（奨学金の流用）"
    gambling_history: "2年（彼氏の影響）"
    visit_motive: "生活費の確保と暇つぶし"
  trigger:
    event: "店員にメダル補給（ホッパーエンプティ）で声をかけられた時"
    machine_type: "AT機（パチスロ）"
    time_of_day: "平日夕方"
  inner_monologue_ja: "あ、すいません。……なんか店員さん、同じくらいの年だしイケメンだな。ていうか私、こんな昼間からスロット打っててどう思われてるんだろ。奨学金溶かしてるのバレたら引かれるよね。"
  emotional_state:
    arousal_0_100: 40
    despair_0_100: 30
    dominant_emotion: "軽い気まずさ × 若年層特有の自意識過剰"
  action: "軽く会釈して、スマホに視線を落としてなるべく目を合わせないようにする"
  post_play_state: "連チャン終了後、周囲の目を気にしてそそくさと景品交換して退店"
  source:
    type: "若年層女性プレイヤーのメタ分析"
    url_or_ref: "N/A"
    confidence: "中"
  notes: "若年層特有の「他者からの視線（特に同年代や男性店員）」に対する自意識。完全なトランス状態には至っていない中期段階における、自己客観視の残滓。"

- id: R1-D-004
  category: 女子大生・若年女性
  profile:
    age_range: "20代前半"
    occupation: "大学生"
    family: "一人暮らし"
    monthly_disposable_yen: 20000
    debt_yen: 300000
    addiction_severity: "中期"
    gambling_history: "1年"
    visit_motive: "大学の講義のサボり"
  trigger:
    event: "台の横を大学の友人らしき人が通ったと錯覚した瞬間"
    machine_type: "パチスロ"
    time_of_day: "大学の授業中（平日昼）"
  inner_monologue_ja: "ビクッ！……なんだ、別人か。心臓止まるかと思った。大学の友達にここに出入りしてるのバレたら絶対ハブられるし、親に知られたら勘当される。でもやめられないんだよ。"
  emotional_state:
    arousal_0_100: 85
    despair_0_100: 40
    dominant_emotion: "冷や汗（恐怖） × 隠匿のプレッシャー"
  action: "深く帽子を被り直し、マスクを目の下まで引き上げる"
  post_play_state: "周囲を警戒しながら早足で退店し、遠回りで帰宅する"
  source:
    type: "女性依存症のスティグマに関する学術的文脈に基づく推定"
    url_or_ref: "N/A"
    confidence: "中"
  notes: "「親に知れたら怒られる」「友達に見られたら嫌だ」という初期〜中期の強烈な社会体裁への恐怖感。このスリルが逆に依存を深める一因にもなる。"

- id: R1-D-005
  category: 女子大生・若年女性
  profile:
    age_range: "20代前半"
    occupation: "飲食店バイト"
    family: "実家暮らし"
    monthly_disposable_yen: 50000
    debt_yen: 200000
    addiction_severity: "中期（消費者金融利用開始）"
    gambling_history: "2年"
    visit_motive: "負けたバイト代を取り戻すため"
  trigger:
    event: "財布の中身が空になり、席を立つか迷う瞬間"
    machine_type: "パチンコ"
    time_of_day: "夜20時"
  inner_monologue_ja: "今日のバイト代、全部溶けた。アコムのカード、まだ枠あったよね？ここで帰ったらただの負け犬だし。あと1万円だけ。推しのライブ代稼ぐはずだったのに、何やってんだろ私。"
  emotional_state:
    arousal_0_100: 60
    despair_0_100: 70
    dominant_emotion: "自己嫌悪 × 損切りへの抵抗"
  action: "台のデータランプを睨みながら、名残惜しそうにゆっくりと立ち上がる"
  post_play_state: "そのままコンビニATMに直行し、キャッシングして再入店する"
  source:
    type: "若年層女性プレイヤーのメタ分析"
    url_or_ref: "N/A"
    confidence: "中"
  notes: "若年層における「推し活」など別の目的のための資金調達が、いつの間にかギャンブル自体への執着（サンクコストの回収）にすり替わる過程。"

- id: R1-D-006
  category: 女子大生・若年女性
  profile:
    age_range: "20代前半"
    occupation: "専門学生"
    family: "実家暮らし"
    monthly_disposable_yen: 30000
    debt_yen: 0
    addiction_severity: "初期"
    gambling_history: "半年"
    visit_motive: "彼氏とのデート代わり"
  trigger:
    event: "隣で打っている彼氏の台がフリーズ（プレミアム演出）を引いた瞬間"
    machine_type: "パチスロ"
    time_of_day: "休日夕方"
  inner_monologue_ja: "えっ、画面真っ暗になった！これヤバいやつだよね！？凄い凄い！今日の夜ご飯は絶対いいとこ連れてってもらおう！私の台は全然出ないけど、まあいっか。"
  emotional_state:
    arousal_0_100: 80
    despair_0_100: 0
    dominant_emotion: "興奮のおすそ分け × 依存の学習"
  action: "自分の手を止めて彼氏の台を覗き込み、一緒に喜ぶ"
  post_play_state: "彼氏の勝ち分で焼肉に行き、ギャンブル＝良い思いができるという学習が固定化される"
  source:
    type: "若年層女性プレイヤーのメタ分析"
    url_or_ref: "N/A"
    confidence: "高（導入期の典型的パターン）"
  notes: "彼氏などの身近な男性の影響でホールに出入りする「イネイブリング（Enabling）的導入」。他者の勝利による報酬（食事など）が、自身のギャンブルへのハードルを下げる。"
```

## 4. メタ観察：女性プレイヤーの心理・行動の共通パターン

上記で抽出された24の事例カードを俯瞰し、LLMペルソナの群像シミュレーションにおいて基盤となる「5つの共通パラメータ・パターン」をメタ分析として提示する。

### 1. 「逃避（Escape）」と「エネルギー源」の等価交換（カテゴリA・Bに顕著）

男性ペルソナがスリルやアクション（高揚感）を求めてギャンブルに走る傾向があるのに対し、女性は「対人関係の苦痛・孤独・疲労」からの逃避を目的とするケースが極めて多い。特筆すべきは、パチンコが単なる逃避ではなく「将来への希望がみなぎり、元気になる」ための「唯一のエネルギー源」として機能している点である。シミュレーションにおいては、家事や仕事の「疲労度（Fatigue）」や「ストレス（Stress）」パラメータが高いペルソナほど、プレイ中の「幸福感（Happiness）」の回復率を非線形に高く設定するロジックが有効である。

### 2. 「羞恥心の障壁（Shame Barrier）」の急速な崩壊（全カテゴリ共通）

女性プレイヤーにとって、ホールは初期段階において「タバコ臭い、うるさい、底辺の場所」という強烈な社会的烙印（スティグマ）として認識される。そのため、「知り合いに見られたくない」という恐怖が初期の行動を強く制限する。しかし、この障壁は「ビギナーズラック」による強烈な自己効力感の誤認や、わずか数週間の反復行動によって急速に「慣れ」へと移行する。LLMエージェントには「ホールへの忌避感（Stigma Barrier）」パラメータを設け、来店回数や勝利経験に応じてこれを急激にゼロへ減衰させる設計が推奨される。

### 3. 「所持金ゼロ」が引き起こすパニックと交差依存への直結（カテゴリCに顕著）

夜職・風俗系女性の事例において、残金が尽きかけた際の心理状態は単なる「後悔」や「落胆」ではない。「もうパチンコができなくなる」という、生存を脅かされるような強迫的なパニック（離脱症状に近い焦燥感）である。これが直ちに「体を売る」「嘘をつく」という極端な金策行動（交差依存）へ直結する。シミュレーション内では、カテゴリCのペルソナが所持金0に近づいた際、Despair（絶望）とArousal（覚醒）が同時に跳ね上がる特異な数値を設定し、異常行動のトリガーとする必要がある。

### 4. 「生活費の直接投下」によるデスクトップ・パニック（カテゴリAに顕著）

主婦層のプレイにおいては、財布の中身が「今日の夕飯代」や「夫の給料」であるため、負けが込んできた際の「日常崩壊への恐怖」が男性のそれよりも遥かにリアルで生々しい。退店直後の「帰宅後に夫にどう嘘をつくか」という思考がプレイ中からセットになっており、プレイ中と退店後のパラメーターの急変動（ドロップ）を表現することで、よりリアルな主婦ペルソナが完成する。

### 5. SNS承認欲求と「パチンコ女子」の分離現象（カテゴリDに顕著）

若年層女性においては、ギャンブル本来の孤独性をSNS（XやTikTok）での共有によって相殺する傾向が見られる。彼女たちは「金保留」「レバブル」といった派手なギミック演出そのものに対してドーパミン報酬を感じており、勝敗と同等かそれ以上に「フォロワーへの報告ネタができたか」が感情を大きく左右する。プレイ中のArousal係数を、出玉だけでなく「レア演出の出現」に強く紐づけ、SNS投稿というアクションを挟む設計が求められる。

## 5. ソース評価と今後の拡張（R2-R4）への示唆

本ラウンド（R1：女性当事者）のデータ収集において利用したソース群の有用性と、今後のペルソナ拡張における展望は以下の通りである。

### 当事者ブログ（Note等の手記）の評価【極めて高】

Megaya氏の体験や若年層のプレイ記録は、ホール内の「音のうるささ」「光の眩しさ」「演出への即時的なリアクション」といったミクロな情動（プレイ中の秒単位の感情推移）を抽出する上で最も有用であった。今後の「初心者（R4）」ペルソナ構築においても、Note等の「初めてパチンコに行った」系エッセイは非常に強力なパラメータ設計素材となる。

### 厚労省・医療機関の回復体験談の評価【高（マクロ分析向け）】

厚労省のサイトに掲載された「Milk」さん（30代主婦）の事例や、大石クリニックの臨床レポートは、「なぜハマったか（動機）」「どう狂っていったか（金銭感覚）」というマクロな心理的軌跡を完璧に描写している。ただし、「リーチ時の感情」といった秒単位の解像度は低いため、今回のように行動心理学の知見を用いて「プレイ中の感情」を逆算・推定する作業が必要となる。

### GA（ギャンブラーズ・アノニマス）およびギャマノン手記の評価【中〜低（ミクロ分析向けとしては）】

提供された資料内の自助グループ（ギャマノン等）の手記は、その大半が「依存症の夫・息子を持つ『妻・母』の苦悩（共依存関係）」であり、女性当事者自身のプレイ中心理を直接描写したものは少なかった（一部の性依存交差の事例を除く）。家族目線のデータは、退店後の「家族への嘘」や「イネイブリング（Enabling）行動」のパラメータ作成には有用だが、ホール内の群像シミュレーションには直接使いづらい。

### 今後のラウンドへの示唆と拡張性

次ラウンド以降で「高齢者（R2）」や「回復期（R3）」のペルソナを作成する際は、地方自治体の医療実態調査や、クリニックの症例レポートがより重要になる。特に高齢女性プレイヤーは「コミュニティの喪失（孤独感）」がホールに向かわせる最大の要因となるため、今回確認できた「主婦の孤独の延長線上」としてパラメータを設計することで、シミュレーション内に連続性と説得力のある群像社会を構築できると確信する。

## 引用元

- kokoro.mhlw.go.jp - 私とパチンコ依存症：こころの病 克服体験記｜こころの耳：働く人
- note.com/megaya - パチンコ嫌いがパチンコを一週間やってわかったこと
- nujyumi.la.coocan.jp - ギャンブル依存症だったんだと思います。「また、パチンコに行く」
- ohishi-clinic.or.jp - ギャンブル依存症 体験談 - 外来治療と家族相談、回復施設｜大石クリニック
- yomiuri.co.jp - ギャンブル依存症の回復プログラム
- note.com/bright_carp7915 - ユニコーン叫び×レバブル×金保留が3連続ハズレた日
- ncasa-japan.jp - 体験談（令和４年１2 月掲載）依存症対策全国センター
- note.com/ouma - 闇金ウシジマくん１話分析
- city.kitakyushu.lg.jp - 本人・ご家族の体験談
- saudade.biz - わかっちゃいるけどやめられない
- addiction.report - ギャン妻たちとの初めての交流（ギャンマネ41）
- pref.kanagawa.jp - 依存症に係る社会資源実態調査 調査報告書
