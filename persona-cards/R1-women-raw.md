# 女性当事者のパチスロ心理反応ライブラリ

## 調査の前提

今回は、**公開された女性当事者の一人称記述**だけを優先し、ホール内での「座る前」「打っている最中」「残金が減った瞬間」「帰るか追うかの判断」「退店直後」に寄せて再構成しました。  
目標の 50–60 件には届いていませんが、**本人性別が比較的明確で、しかも内面の言葉が取れるもの**に絞ると、薄い要約を量産するより **32 カード**に留めたほうが設計素材として有用だと判断しました。数値パラメータは公開記述からの推定で、明確に読み取れない部分は幅をもたせています。  
なお、**同一当事者の長い手記から複数場面を切り出したカード**が含まれます。これは「人物サンプル数」を増やす目的ではなく、**場面別の反応係数**を取るためです。

## 主婦

```yaml
- id: R1-A-001
  category: 主婦
  profile:
    age_range: "30代前半"
    occupation: "パート寄りの就労・既婚"
    family: "夫と子どもあり"
    addiction_severity: "中度"
    gambling_history: "友人に連れられた初回大当たり後、結婚後に1人打ちへ移行"
    visit_motive: "生活の息苦しさを一時的に忘れたい"
  trigger:
    event: "財布の現金が尽き、生活費の封筒に手を伸ばす"
    machine_type: "パチンコ"
    time_of_day: "日中"
  inner_monologue_ja: "これ当たれば戻せる。今日だけ借りるだけ、家に帰る頃には帳尻合う"
  emotional_state:
    arousal_0_100: 72
    despair_0_100: 46
    dominant_emotion: "焦り × 自己正当化"
  action: "生活費を追加入金して続行"
  post_play_state: "帰宅後は何もなかったように振る舞う"
  source:
    type: "公的メンタルヘルス体験記"
    url_or_ref: "公開当事者手記・既婚女性の回復回想"
    confidence: "高"
  notes: "『使ってはいけない金』の境界が崩れる場面として再構成"

- id: R1-A-002
  category: 主婦
  profile:
    age_range: "30代前半"
    occupation: "パート寄りの就労・既婚"
    family: "夫と子どもあり"
    debt_yen: "不明"
    addiction_severity: "中度〜重度"
    gambling_history: "継続打ちが習慣化"
    visit_motive: "家計の穴埋めと気分転換が混線"
  trigger:
    event: "給料日直後、封筒の現金がある状態でホール前を通る"
    machine_type: "パチンコ"
    time_of_day: "昼"
  inner_monologue_ja: "今日だけ増やしてから帰れば、今月は少し楽になる。減らすためじゃなく増やすため"
  emotional_state:
    arousal_0_100: 78
    despair_0_100: 41
    dominant_emotion: "期待 × 打算"
  action: "『少しだけ』のつもりで入店し、上限を崩す"
  post_play_state: "支払い予定を頭の中で組み替え続ける"
  source:
    type: "公的メンタルヘルス体験記"
    url_or_ref: "公開当事者手記・既婚女性の回復回想"
    confidence: "高"
  notes: "家計補填の論理が軍資金化する瞬間"
```

上の 2 カードは、同一当事者の公開回想から「家計内流用」と「給料日直後の自己正当化」を分けて切り出したものです。citeturn5view1turn5view3

```yaml
- id: R1-A-003
  category: 主婦
  profile:
    age_range: "30代前半"
    occupation: "専業主婦"
    family: "夫と小学生の子1人"
    debt_yen: 5700000
    addiction_severity: "重度"
    gambling_history: "初打ちの大勝ち後、平日にほぼ毎日通う"
    visit_motive: "大当たりの快感の再演"
  trigger:
    event: "開店前に並び、昼食を抜いて席を立てなくなる"
    machine_type: "パチンコ"
    time_of_day: "平日10時〜夕方"
  inner_monologue_ja: "今やめたらこの台を捨てるだけ。ご飯食べてる場合じゃない、当たりを逃したくない"
  emotional_state:
    arousal_0_100: 83
    despair_0_100: 38
    dominant_emotion: "没入 × 固執"
  action: "食事を後回しにして打ち続ける"
  post_play_state: "帰宅時間までに感情を平坦化して母親役に戻る"
  source:
    type: "女性向けメディアの本人取材"
    url_or_ref: "主婦当事者の取材記事"
    confidence: "中"
  notes: "家事・昼食を切ってでも離席回避を優先する"

- id: R1-A-004
  category: 主婦
  profile:
    age_range: "30代前半"
    occupation: "専業主婦"
    family: "夫と子どもあり"
    debt_yen: 5700000
    addiction_severity: "重度"
    gambling_history: "共有貯金にまで流用が進行"
    visit_motive: "負けの穴埋め"
  trigger:
    event: "共有貯金の残高が減っているのに、さらに軍資金が足りなくなる"
    machine_type: "パチンコ"
    time_of_day: "午後"
  inner_monologue_ja: "ここで取り返せなかったら本当に終わる。最悪、別の手で作ればいい"
  emotional_state:
    arousal_0_100: 86
    despair_0_100: 67
    dominant_emotion: "切迫感 × 逃避"
  action: "負けを止めず、資金調達の発想が風俗・親頼みまで拡張"
  post_play_state: "夫に知られていない前提で次の資金繰りを考える"
  source:
    type: "女性向けメディアの本人取材"
    url_or_ref: "主婦当事者の取材記事"
    confidence: "中"
  notes: "『風俗か……』という発想がホール内で現実的選択肢になる"
```

この 2 カードは、同一取材記事から「昼の没入」と「資金枯渇時の切迫」を分けて再構成しました。citeturn7view2turn26search4

```yaml
- id: R1-A-005
  category: 主婦
  profile:
    age_range: "50代前半"
    occupation: "既婚・育児期を経験"
    family: "夫と子ども"
    debt_yen: "不明"
    addiction_severity: "重度"
    gambling_history: "20歳からの長期化、結婚後も継続"
    visit_motive: "混乱感と役割疲労からの逃避"
  trigger:
    event: "子どもを放置気味にしながらでも台前に戻ってしまう"
    machine_type: "パチンコ"
    time_of_day: "日中〜夕方"
  inner_monologue_ja: "今日だけ回してから帰る。家のことはあとで合わせれば何とかなる"
  emotional_state:
    arousal_0_100: 74
    despair_0_100: 63
    dominant_emotion: "麻痺 × 焦燥"
  action: "育児より遊技継続を優先"
  post_play_state: "帳尻合わせのように夫の帰宅時だけ平静を演じる"
  source:
    type: "支援団体掲載の当事者手記PDF"
    url_or_ref: "50代女性当事者・長期回復手記"
    confidence: "高"
  notes: "本人が後年『育児放棄の状況』と回想した部分を場面化"

- id: R1-A-006
  category: 主婦
  profile:
    age_range: "40代前半"
    occupation: "回復支援職に就く元当事者"
    family: "既婚"
    addiction_severity: "重度化歴あり"
    gambling_history: "結婚後に1人打ちが加速し、3年で遊びの域を超える"
    visit_motive: "不安から逃げるため"
  trigger:
    event: "大負けした夜、帰宅してからも『もう一回』が頭から離れない"
    machine_type: "パチンコ"
    time_of_day: "夜"
  inner_monologue_ja: "このままじゃダメって分かってるのに、明日もう一回行けば少し戻る気がする"
  emotional_state:
    arousal_0_100: 68
    despair_0_100: 72
    dominant_emotion: "羞恥 × 渇望"
  action: "ネットで助けを探しながらも、頭の中では再戦を反芻"
  post_play_state: "大負けの夜が初めてのSOSにつながる"
  source:
    type: "公開プロフィール手記"
    url_or_ref: "元当事者女性カウンセラーの自己紹介文"
    confidence: "高"
  notes: "『ずたぼろに負けた夜』をホール直後の反応として切り出した"
```

前者は長期の当事者手記、後者は元当事者支援者の自己紹介文です。主婦カテゴリでも、**育児放置型**と**夜間の自己嫌悪型**が分かれました。citeturn36view0turn16view0

```yaml
- id: R1-A-007
  category: 主婦
  profile:
    age_range: "30代前半"
    occupation: "パート＋歩合仕事"
    family: "夫と子どもあり"
    debt_yen: 820000
    addiction_severity: "中度"
    gambling_history: "元彼由来で長期化、断パチ反復"
    visit_motive: "お金の不安とPMS・ストレスの増幅"
  trigger:
    event: "車検や生活費を考えた直後に『1万円入れてやる』衝動が出る"
    machine_type: "パチンコ"
    time_of_day: "日中"
  inner_monologue_ja: "どうせ今も苦しいなら、一回勝てば少し息つける。入れるなら一万、そこで止める"
  emotional_state:
    arousal_0_100: 70
    despair_0_100: 60
    dominant_emotion: "切迫感 × 衝動"
  action: "断パチ中でも再投資の空想を繰り返す"
  post_play_state: "『今日で何日目』と数えながら再発を警戒"
  source:
    type: "個人ブログ"
    url_or_ref: "依存症アラサー既婚女性ブログ"
    confidence: "中"
  notes: "PMS・家計不安・再発衝動が結びついている"

- id: R1-A-008
  category: 主婦
  profile:
    age_range: "30代後半〜40代前半"
    occupation: "パート主婦"
    family: "夫あり"
    addiction_severity: "中度〜重度"
    gambling_history: "禁パチ反復、短期再発を繰り返す"
    visit_motive: "前日の負けをその日のうちに薄めたい"
  trigger:
    event: "前日の負けを取り返すため昼から再入店"
    machine_type: "パチンコ"
    time_of_day: "昼〜夕方"
  inner_monologue_ja: "勝てるなんて思ってない。でも昨日の分を少しでも薄めたい"
  emotional_state:
    arousal_0_100: 66
    despair_0_100: 69
    dominant_emotion: "イライラ × 自罰"
  action: "昼から夕方まで打ち、負けた勢いで惣菜や甘い物を大量買い"
  post_play_state: "母の病院にも行かず、自己嫌悪が増幅"
  source:
    type: "個人ブログ"
    url_or_ref: "既婚女性の禁パチ反復ブログ"
    confidence: "中"
  notes: "損失の直後に食行動へスライドする反応が強い"
```

この 2 カードは、**生活不安での再発空想**と**取り返し打ち→やけ買い**の対照として置きました。citeturn19view1turn21view5turn32search3

## OL・社会人女性

```yaml
- id: R1-B-001
  category: "OL・社会人女性"
  profile:
    age_range: "30代前半"
    occupation: "実家暮らしの会社員"
    family: "親と同居"
    addiction_severity: "中度"
    gambling_history: "職場で好きな人の話題に合わせたくて開始"
    visit_motive: "会話に入るための軽い参加"
  trigger:
    event: "初打ちで1000円を入れる瞬間と、直後の1万円勝ち"
    machine_type: "パチンコ"
    time_of_day: "仕事後"
  inner_monologue_ja: "千円入れるの怖い。でも当たったら話せる、分かる側に入れる"
  emotional_state:
    arousal_0_100: 77
    despair_0_100: 18
    dominant_emotion: "緊張 × 高揚"
  action: "大当たり後に一気に警戒感が薄れる"
  post_play_state: "『自分にもできる』感覚が残る"
  source:
    type: "支援団体掲載の当事者手記PDF"
    url_or_ref: "30代女性当事者手記"
    confidence: "高"
  notes: "導入は承認欲求と恋愛文脈"

- id: R1-B-002
  category: "OL・社会人女性"
  profile:
    age_range: "30代前半"
    occupation: "実家暮らしの会社員"
    family: "親と同居"
    debt_yen: 2000000
    addiction_severity: "重度"
    gambling_history: "開始1か月以内に1人打ち常態化"
    visit_motive: "負けの取り返しと借金返済の錯覚"
  trigger:
    event: "親に渡す生活費とボーナス、資格取得費まで軍資金化"
    machine_type: "パチンコ"
    time_of_day: "仕事後〜休日"
  inner_monologue_ja: "資格のお金はまた作ればいい。今ここで勝てば何も崩れない"
  emotional_state:
    arousal_0_100: 79
    despair_0_100: 58
    dominant_emotion: "切迫感 × 麻痺"
  action: "生活費流用→初めての消費者金融→継続"
  post_play_state: "借金への絶望より『月々数千円なら回る』と考える"
  source:
    type: "支援団体掲載の当事者手記PDF"
    url_or_ref: "30代女性当事者手記"
    confidence: "高"
  notes: "社会人女性の『用途の転用』が鮮明"
```

同一手記ですが、**導入の軽さ**と**生活費・資格費の軍資金化**で心理の質がかなり違います。citeturn35view0

```yaml
- id: R1-B-003
  category: "OL・社会人女性"
  profile:
    age_range: "30代前半"
    occupation: "会社員"
    family: "実家暮らし"
    debt_yen: 2000000
    addiction_severity: "重度"
    gambling_history: "借金後も継続"
    visit_motive: "返済資金をギャンブルで作る発想"
  trigger:
    event: "譲ってもらった大事な楽器やカメラを現金化し、その足でホールへ直行"
    machine_type: "パチンコ"
    time_of_day: "昼〜夕方"
  inner_monologue_ja: "これは元手。今日勝てば売らなくて済んだことになる"
  emotional_state:
    arousal_0_100: 74
    despair_0_100: 71
    dominant_emotion: "罪悪感 × 追い込み"
  action: "質入れ・売却金を全投入"
  post_play_state: "負けるたびに『もうやめよう』と思うが数日で戻る"
  source:
    type: "支援団体掲載の当事者手記PDF"
    url_or_ref: "30代女性当事者手記"
    confidence: "高"
  notes: "物品の換金がそのままホール導線になる"

- id: R1-B-004
  category: "OL・社会人女性"
  profile:
    age_range: "30代前半"
    occupation: "会社員"
    family: "実家暮らし"
    debt_yen: 2000000
    addiction_severity: "重度"
    gambling_history: "毎日行かないと気が済まない段階"
    visit_motive: "不眠・不安の一時停止"
  trigger:
    event: "借金で眠れず不安定なのに、帰宅前にホールへ向かってしまう"
    machine_type: "パチンコ"
    time_of_day: "仕事後"
  inner_monologue_ja: "行きたくない。でも行かないと頭の中が静かにならない"
  emotional_state:
    arousal_0_100: 64
    despair_0_100: 81
    dominant_emotion: "不安 × 強迫"
  action: "打ちたくないと思いながら連日入店"
  post_play_state: "不眠と不安が改善せず、さらに孤立"
  source:
    type: "支援団体掲載の当事者手記PDF"
    url_or_ref: "30代女性当事者手記"
    confidence: "高"
  notes: "快楽追求より『静めるために打つ』局面"
```

この 2 カードは、**物を金に換える段階**と**楽しさが消えた強迫段階**です。設計上は同じ「社会人女性」でも重みを分けたほうが良いです。citeturn35view0

```yaml
- id: R1-B-005
  category: "OL・社会人女性"
  profile:
    age_range: "30代後半"
    occupation: "就労女性"
    family: "家族・恋人との関係あり"
    debt_yen: "不明"
    addiction_severity: "重度"
    gambling_history: "数年で制御不能"
    visit_motive: "好きだが、やめなければ壊れるという葛藤"
  trigger:
    event: "家族や彼氏から借り、仕事をさぼり、約束も飛ばし、上限も守れない"
    machine_type: "パチンコ"
    time_of_day: "仕事時間帯を含む"
  inner_monologue_ja: "次で止める。今日は本当に止める。でも今やめたら全部むだになる"
  emotional_state:
    arousal_0_100: 71
    despair_0_100: 76
    dominant_emotion: "執着 × 自責"
  action: "上限を何度も更新し、行動予定をギャンブル優先に再編"
  post_play_state: "信用を失う恐怖より、次の再戦欲求が勝つ"
  source:
    type: "支援団体掲載の当事者手記PDF"
    url_or_ref: "30代女性当事者手記"
    confidence: "高"
  notes: "『時間の上限』まで壊れる"

- id: R1-B-006
  category: "OL・社会人女性"
  profile:
    age_range: "30代後半"
    occupation: "就労女性"
    family: "家族・恋人との関係あり"
    debt_yen: "不明"
    addiction_severity: "重度"
    gambling_history: "自助グループ前の末期"
    visit_motive: "虚しさと孤独感の遮断"
  trigger:
    event: "使ってはいけないお金を使い果たし、『死にたい』と『次を打ちたい』が同時に出る"
    machine_type: "パチンコ"
    time_of_day: "負け後"
  inner_monologue_ja: "もう終わりにしたい。でも終わる前に、もう一回だけ当たりを引きたい"
  emotional_state:
    arousal_0_100: 62
    despair_0_100: 89
    dominant_emotion: "虚無 × 渇望"
  action: "自己嫌悪のまま再戦欲求を抑えきれない"
  post_play_state: "自助グループに辿り着き、初めて『病気』の言葉に泣く"
  source:
    type: "支援団体掲載の当事者手記PDF"
    url_or_ref: "30代女性当事者手記"
    confidence: "高"
  notes: "快楽より『地獄の反復』としてのギャンブル"
```

この 2 カードでは、**スケジュール破壊**と**自死念慮に近い自責＋再戦欲求**が共存します。citeturn36view1turn9search2

```yaml
- id: R1-B-007
  category: "OL・社会人女性"
  profile:
    age_range: "40代前半"
    occupation: "独身会社員"
    family: "一人暮らし寄り"
    addiction_severity: "中度"
    gambling_history: "20代で彼氏に連れられて開始"
    visit_motive: "嫌なことを忘れる・涼みに行くという自己弁護"
  trigger:
    event: "給料日直後に『即パチンコ屋』のルートが自然化する"
    machine_type: "パチンコ"
    time_of_day: "給料日・仕事後"
  inner_monologue_ja: "今日だけはいいでしょ。勝ったら明日もいけるし、嫌なことも忘れられる"
  emotional_state:
    arousal_0_100: 73
    despair_0_100: 44
    dominant_emotion: "高揚 × 言い訳"
  action: "給料出たら直行、勝てば翌日の稼働予定まで立てる"
  post_play_state: "後日トータルで負けていたと冷える"
  source:
    type: "個人ブログ"
    url_or_ref: "40代独身女性ブログ"
    confidence: "中"
  notes: "『嫌なことを忘れる』が強い"

- id: R1-B-008
  category: "OL・社会人女性"
  profile:
    age_range: "30代後半〜40代前半"
    occupation: "独身会社員"
    family: "単身"
    debt_yen: 7730000
    addiction_severity: "重度"
    gambling_history: "ギャンブル依存と買い物依存が併発"
    visit_motive: "勝って終わらせたい、負けをただの負け日にしたくない"
  trigger:
    event: "『今日はダメな日』と分かっても帰れず、紙幣をサンドに入れ続ける"
    machine_type: "パチンコ"
    time_of_day: "朝イチ〜夕方"
  inner_monologue_ja: "もうダメなのは分かってる。でもここで帰ったら今日が丸ごと無駄になる"
  emotional_state:
    arousal_0_100: 69
    despair_0_100: 84
    dominant_emotion: "麻痺 × 追い詰め"
  action: "止められず追加入金、店を出てから別の散財に流れる"
  post_play_state: "頭も財布も空っぽになり、買い物で負け感を上塗りする"
  source:
    type: "個人ブログ"
    url_or_ref: "借金773万円の独身会社員ブログ"
    confidence: "高"
  notes: "『機械の体』表現は行動自動化の描写として極めて有用"
```

この 2 カードは、**給料日直行型**と**停止不能型**の対照です。前者はまだ快楽が残り、後者はすでに快楽より麻痺が前面です。citeturn31view2turn19view0turn21view0

## 風俗・夜職系女性

```yaml
- id: R1-C-001
  category: "風俗・夜職系女性"
  profile:
    age_range: "30代前半"
    occupation: "パートを転々"
    family: "同棲相手あり"
    debt_yen: 700000
    addiction_severity: "重度"
    gambling_history: "彼と週末打ち→1人の平日打ちへ"
    visit_motive: "彼より長く打てる『1人打ち』の自由さ"
  trigger:
    event: "仕事帰り、彼がいない日は閉店近くまで打てると感じる"
    machine_type: "パチンコ→スロット併用"
    time_of_day: "夕方〜閉店"
  inner_monologue_ja: "帰ろうって言われない一人のほうが楽。今日は好きなだけ回せる"
  emotional_state:
    arousal_0_100: 76
    despair_0_100: 37
    dominant_emotion: "解放感 × 執着"
  action: "平日夜の単独稼働が習慣化"
  post_play_state: "生活リズムがホール中心に組み替わる"
  source:
    type: "公開当事者手記"
    url_or_ref: "女性当事者の長文回想"
    confidence: "高"
  notes: "『同行者に止められない自由』が促進因子"

- id: R1-C-002
  category: "風俗・夜職系女性"
  profile:
    age_range: "30代前半"
    occupation: "パートを転々"
    family: "同棲相手あり"
    debt_yen: 700000
    addiction_severity: "重度"
    gambling_history: "給料消失後、駅前消費者金融へ"
    visit_motive: "今打つための現金を作る"
  trigger:
    event: "給料がなくなっても打ちたくて、駅近の消費者金融で1万5000円を借りる"
    machine_type: "パチンコ・スロット"
    time_of_day: "平日夕方"
  inner_monologue_ja: "少額ならすぐ返せる。今日の軍資金さえあればひっくり返せる"
  emotional_state:
    arousal_0_100: 81
    despair_0_100: 52
    dominant_emotion: "切迫感 × 多幸予測"
  action: "借入→即ホール"
  post_play_state: "『なければ借りればいい』思考が固定化"
  source:
    type: "公開当事者手記"
    url_or_ref: "女性当事者の長文回想"
    confidence: "高"
  notes: "夜職化以前の資金調達パターン"
```

上の 2 カードは、**同行者からの切り離し**と**借入の即時軍資金化**を示します。夜職・性産業へ移る前段として重要です。citeturn30search4turn25view0

```yaml
- id: R1-C-003
  category: "風俗・夜職系女性"
  profile:
    age_range: "30代前半"
    occupation: "パート＋売春"
    family: "彼あり"
    debt_yen: 700000
    addiction_severity: "重度"
    gambling_history: "借金隠しのため性売買に移行"
    visit_motive: "負け分を現金で即補充したい"
  trigger:
    event: "パートの合間に客を取り、その金をそのまま軍資金にする"
    machine_type: "パチンコ・スロット"
    time_of_day: "昼〜夕方"
  inner_monologue_ja: "これでまた打てる。今日分さえ作れれば、まだごまかせる"
  emotional_state:
    arousal_0_100: 74
    despair_0_100: 79
    dominant_emotion: "切実さ × 解離"
  action: "『会社』『残業』と嘘をついて客に会い、その後ホールへ"
  post_play_state: "終わった後は虚しいが、軍資金が手に入ると再びホールへ向く"
  source:
    type: "公開当事者手記"
    url_or_ref: "女性当事者の長文回想"
    confidence: "高"
  notes: "性行為そのものより『次の稼働資金』が目的化"

- id: R1-C-004
  category: "風俗・夜職系女性"
  profile:
    age_range: "20代後半"
    occupation: "派遣就労→街娼"
    family: "家族と断絶"
    addiction_severity: "重度"
    gambling_history: "海物語に没入、給料が1日で消える"
    visit_motive: "音・演出・魚群への執着"
  trigger:
    event: "月給が1日で消え、店内を泣きながら歩いているところに声をかけられる"
    machine_type: "パチンコ"
    time_of_day: "日中"
  inner_monologue_ja: "魚群が外れた。もう終わり。でもこのまま帰るのはもっと無理"
  emotional_state:
    arousal_0_100: 88
    despair_0_100: 85
    dominant_emotion: "パニック × 飢餓感"
  action: "ホテル同行で現金を得て、その成功体験が固定"
  post_play_state: "『体で現金を作れる』回路ができる"
  source:
    type: "取材インタビュー"
    url_or_ref: "街娼経験女性の回想取材"
    confidence: "中"
  notes: "ホール内での涙→即現金化という極端な切り替わり"
```

ここでは、**資金補填としての売春**と**ホール内で売春導線が開く瞬間**を分けています。citeturn25view0turn27view0

```yaml
- id: R1-C-005
  category: "風俗・夜職系女性"
  profile:
    age_range: "20代後半"
    occupation: "街娼"
    family: "家族と絶縁"
    addiction_severity: "重度"
    gambling_history: "負けた日はその場で性売買する習慣化"
    visit_motive: "負けを即日で埋めたい"
  trigger:
    event: "負けた後、景品交換所まわりをうろついて声待ちする"
    machine_type: "パチンコ"
    time_of_day: "夕方〜夜"
  inner_monologue_ja: "このまま帰るなら負けのまま。誰か拾ってくれれば、もう一回回せる"
  emotional_state:
    arousal_0_100: 73
    despair_0_100: 82
    dominant_emotion: "飢餓感 × 諦め"
  action: "負け後にその場で客待ち"
  post_play_state: "朝から晩までパチンコ中心の一日に固定"
  source:
    type: "取材インタビュー"
    url_or_ref: "街娼経験女性の回想取材"
    confidence: "中"
  notes: "交換所周辺が『再戦資金の採取地点』になる"

- id: R1-C-006
  category: "風俗・夜職系女性"
  profile:
    age_range: "20代後半〜30代前半"
    occupation: "元キャバ嬢"
    family: "単身"
    addiction_severity: "中度"
    gambling_history: "日払い習慣と昼時間でスロット化"
    visit_motive: "ストレス発散と現金消費"
  trigger:
    event: "仕事終わりに仮眠して、昼頃から近所のホールへ向かう"
    machine_type: "スロット"
    time_of_day: "昼"
  inner_monologue_ja: "今日も入ったし、少しくらい打ってもまた夜に稼げる"
  emotional_state:
    arousal_0_100: 71
    despair_0_100: 33
    dominant_emotion: "緩み × 習慣化"
  action: "日払い現金をそのままスロットへ投入"
  post_play_state: "『今日稼いだから』の論理で貯蓄ゼロが続く"
  source:
    type: "夜職経験者のnote"
    url_or_ref: "元キャバ嬢の生活回想"
    confidence: "中"
  notes: "夜職とスロットの時間相性が明瞭"
```

この 2 カードは、**ホール外周での客待ち**と**夜職ルーティン内の昼スロ**という、Cカテゴリの両極です。citeturn27view0turn44view0

```yaml
- id: R1-C-007
  category: "風俗・夜職系女性"
  profile:
    age_range: "20代後半〜30代前半"
    occupation: "元キャバ嬢"
    family: "単身"
    addiction_severity: "中度"
    gambling_history: "日払い・美容費・遊び・ギャンブルの負のループ"
    visit_motive: "暇さと現金保有で財布の紐が切れる"
  trigger:
    event: "日払いがある前提で出費水準が上がり、暇な日にまたホールへ向かう"
    machine_type: "パチンコ・スロット"
    time_of_day: "昼〜夕方"
  inner_monologue_ja: "今日使っても明日入るし。暇だし、少し回して帰ろう"
  emotional_state:
    arousal_0_100: 63
    despair_0_100: 29
    dominant_emotion: "弛緩 × 慢心"
  action: "日払い前提で小さな浪費を重ね、結果的にギャンブル支出も増える"
  post_play_state: "月末に何も残らない"
  source:
    type: "夜職経験者のnote"
    url_or_ref: "元キャバ嬢の生活回想"
    confidence: "中"
  notes: "重度依存症というより構造的誘発"

- id: R1-C-008
  category: "風俗・夜職系女性"
  profile:
    age_range: "30代前半"
    occupation: "昼職＋人妻デリヘル嬢"
    family: "既婚"
    debt_yen: 5000000
    addiction_severity: "重度"
    gambling_history: "パチンコとソシャゲの複合依存"
    visit_motive: "『今日こそ勝てる』の反復"
  trigger:
    event: "給料日前、ATMで泣きながら借りるのに、台前ではまだ『勝てる』と思う"
    machine_type: "パチンコ"
    time_of_day: "給料日前後"
  inner_monologue_ja: "もうこれ以上は無理。でも今日当たれば全部つながる。ここで引ければまだ死なない"
  emotional_state:
    arousal_0_100: 82
    despair_0_100: 87
    dominant_emotion: "追い込み × 妄信"
  action: "借入継続、最高で1日20万円規模まで溶かす"
  post_play_state: "家族に嘘を重ねながら返済と再発を往復"
  source:
    type: "個人note"
    url_or_ref: "借金500万円超の当事者マガジン"
    confidence: "中"
  notes: "Cカテゴリでは最も高額損失帯"
```

この 2 カードは、**構造的にお金が消える夜職**と**夜職を含む複合依存の末期**を分けています。citeturn44view0turn45search5turn45search0

## 女子大生・若年女性

```yaml
- id: R1-D-001
  category: "女子大生・若年女性"
  profile:
    age_range: "20歳"
    occupation: "勤労学生"
    family: "実家外の住み込み就労"
    addiction_severity: "初期→中度"
    gambling_history: "休日にふらっと入店して開始"
    visit_motive: "学校と仕事の重圧からの解放感"
  trigger:
    event: "音・光・演出に包まれ、初めて当たりを引く"
    machine_type: "パチンコ"
    time_of_day: "休日昼"
  inner_monologue_ja: "これ、すごい。学校も仕事もない時間が全部ここにある"
  emotional_state:
    arousal_0_100: 84
    despair_0_100: 12
    dominant_emotion: "解放感 × 興奮"
  action: "休日をホールで過ごす習慣ができる"
  post_play_state: "『休み＝ホール』の連想が固定"
  source:
    type: "支援団体掲載の当事者手記PDF"
    url_or_ref: "50代女性の20歳当時の回想"
    confidence: "高"
  notes: "若年導入の感覚入力が非常に鮮明"

- id: R1-D-002
  category: "女子大生・若年女性"
  profile:
    age_range: "20代前半"
    occupation: "勤労学生"
    family: "田舎の母とつながり"
    debt_yen: "不明"
    addiction_severity: "中度〜重度"
    gambling_history: "カード作成、家電売却、親への虚偽送金依頼"
    visit_motive: "負けを負けで終わらせたくない"
  trigger:
    event: "返済不能になり、母に嘘をついて振込を頼んだ直後でも台前に戻る"
    machine_type: "パチンコ"
    time_of_day: "休日"
  inner_monologue_ja: "今度こそ返して終わる。負けた分は負けた場所で返すしかない"
  emotional_state:
    arousal_0_100: 76
    despair_0_100: 70
    dominant_emotion: "執着 × 罪悪感"
  action: "家電売却・親への虚偽依頼後も続行"
  post_play_state: "謝罪と再発のループ"
  source:
    type: "支援団体掲載の当事者手記PDF"
    url_or_ref: "50代女性の20歳当時の回想"
    confidence: "高"
  notes: "若年層でも『負けはそこで返す』認知が早い"
```

この 2 カードは、同一当事者の若年期から切っています。**導入の感覚報酬**と**借金後の返済幻想**が並んで取れる稀少例です。citeturn36view0turn12search1

```yaml
- id: R1-D-003
  category: "女子大生・若年女性"
  profile:
    age_range: "20歳前後"
    occupation: "大学生"
    family: "母もパチンコ経験あり"
    addiction_severity: "初期"
    gambling_history: "初彼の影響でホールに入る"
    visit_motive: "彼と同じ景色を見たい、少し大人になりたい"
  trigger:
    event: "彼が打つのを隣で見ているうち、自分も座りたくなる"
    machine_type: "パチスロ見学→パチンコ着席"
    time_of_day: "デート時"
  inner_monologue_ja: "隣で見てるだけでも楽しい。私もやれたら、もっと近づける気がする"
  emotional_state:
    arousal_0_100: 68
    despair_0_100: 10
    dominant_emotion: "憧れ × 好奇心"
  action: "彼同行の見学から自分の遊技へ移る"
  post_play_state: "『彼の趣味』が『自分の入口』に変わる"
  source:
    type: "個人note"
    url_or_ref: "若年女性の回想エッセイ"
    confidence: "中"
  notes: "恋愛導線の典型"

- id: R1-D-004
  category: "女子大生・若年女性"
  profile:
    age_range: "20歳前後"
    occupation: "大学生"
    family: "母との同行経験あり"
    addiction_severity: "初期→中度"
    gambling_history: "1パチから4パチへ移行"
    visit_motive: "演出の面白さから『お金を増やしたい』へ変化"
  trigger:
    event: "アニメ演出目当てで座った台から、気づけば4パチが基本になる"
    machine_type: "パチンコ"
    time_of_day: "昼"
  inner_monologue_ja: "当たったらいいな、じゃなくて、今日はちゃんと増やしたい"
  emotional_state:
    arousal_0_100: 73
    despair_0_100: 24
    dominant_emotion: "好奇心 × 金銭期待"
  action: "低貸しから通常レートへ上げる"
  post_play_state: "遊び感覚が徐々に薄れる"
  source:
    type: "個人note"
    url_or_ref: "若年女性の回想エッセイ"
    confidence: "中"
  notes: "初心者がレートを上げる時の認知転換"
```

この 2 カードは、**恋愛誘導**と**レート上昇**の流れが明快です。若年女性カテゴリでは非常に使いやすい素材です。citeturn31view1

```yaml
- id: R1-D-005
  category: "女子大生・若年女性"
  profile:
    age_range: "19歳"
    occupation: "大学生"
    family: "彼氏あり"
    addiction_severity: "軽度"
    gambling_history: "彼氏の影響で月1〜2回"
    visit_motive: "彼との共通体験"
  trigger:
    event: "彼氏と一緒にホールへ向かう前、『女の子でパチンコは変』と言われた直後"
    machine_type: "パチンコ"
    time_of_day: "休日"
  inner_monologue_ja: "そんなに変かな。でも彼と行くの楽しいし、別に悪いことしてる感じもしない"
  emotional_state:
    arousal_0_100: 55
    despair_0_100: 14
    dominant_emotion: "違和感 × 好奇心"
  action: "周囲のまなざしに引っかかりつつも継続"
  post_play_state: "『自分はまだ大丈夫』という線引きを持つ"
  source:
    type: "公開相談投稿"
    url_or_ref: "大学生女性の相談文"
    confidence: "中"
  notes: "依存手前の正当化を取るためのカード"

- id: R1-D-006
  category: "女子大生・若年女性"
  profile:
    age_range: "20代前半"
    occupation: "女子大生"
    family: "単身または実家圏"
    debt_yen: 170000
    addiction_severity: "中度"
    gambling_history: "暇つぶし→ストレス発散→借入"
    visit_motive: "負けとストレスの両方を消したい"
  trigger:
    event: "『また取り返せばいい』を繰り返し、アコム残高17万円を背負った後の再来店欲求"
    machine_type: "パチンコ"
    time_of_day: "不定"
  inner_monologue_ja: "やめたい。でも楽しい。返済してる間にまた行きたくなるのが一番こわい"
  emotional_state:
    arousal_0_100: 67
    despair_0_100: 73
    dominant_emotion: "依存自覚 × 恐怖"
  action: "返済計画を考えつつ、再発可能性を強く意識"
  post_play_state: "『酒もタバコもやらないのにギャンブルだけ』という自己認識が残る"
  source:
    type: "公開相談投稿"
    url_or_ref: "女子大生の相談文"
    confidence: "中"
  notes: "若年女性の『楽しいのに怖い』両価性"
```

この 2 カードは、**まだ軽い段階の違和感**と**すでに借入に入った段階の恐怖**で使い分けできます。citeturn23search1turn23search3

```yaml
- id: R1-D-007
  category: "女子大生・若年女性"
  profile:
    age_range: "20代前半"
    occupation: "実家暮らしのアルバイト女性"
    family: "親と同居"
    debt_yen: 1500000
    addiction_severity: "重度"
    gambling_history: "元彼に教わり、一度やめても数か月後に再燃"
    visit_motive: "久々の負けを『取り返し戦』に変える"
  trigger:
    event: "少し負けたことに火がつき、仕事と言って毎日ホールに行く"
    machine_type: "パチンコ"
    time_of_day: "昼"
  inner_monologue_ja: "ここで取り返さないと前よりもっと終わる。今日は仕事じゃなくて回収の日"
  emotional_state:
    arousal_0_100: 84
    despair_0_100: 78
    dominant_emotion: "切迫感 × 妄執"
  action: "仕事を辞めてまで通い、3〜4か月で借金急増"
  post_play_state: "後半は楽しくなく、ただ回収目的になる"
  source:
    type: "公開相談投稿"
    url_or_ref: "24歳女性の債務相談文"
    confidence: "中"
  notes: "『少し負けた』が再発トリガー"

- id: R1-D-008
  category: "女子大生・若年女性"
  profile:
    age_range: "20代前半"
    occupation: "無職化した若年女性"
    family: "親と同居"
    debt_yen: 1500000
    addiction_severity: "重度"
    gambling_history: "借入不能になるまで継続"
    visit_motive: "現実逃避ではなく、もはや資金調達の最後の幻想"
  trigger:
    event: "借入不能になり、性売買や自殺まで考えるのに『借りられたらまだ行っていた』と自覚"
    machine_type: "パチンコ"
    time_of_day: "負け後・返済日前"
  inner_monologue_ja: "もう無理。でも借りられるなら、たぶんまた行く。そこが一番こわい"
  emotional_state:
    arousal_0_100: 52
    despair_0_100: 94
    dominant_emotion: "絶望 × 自己嫌悪"
  action: "誰にも言えず債務相談へ流れる"
  post_play_state: "親への告白恐怖が最大化"
  source:
    type: "公開相談投稿"
    url_or_ref: "24歳女性の債務相談文"
    confidence: "中"
  notes: "若年女性カテゴリの末期カード"
```

この 2 カードは、**再燃の火種**と**借入不能後の絶望**のセットです。若年カテゴリの終盤係数に使えます。citeturn25view2

## メタ観察

- **主婦カテゴリでは「家計の見えにくいお金」が軍資金化しやすい**です。生活費の封筒、共有貯金、保険、児童関係の金、車検・支払い予定金など、名目のあるお金が「いったん借りるだけ」と処理されやすい。しかもプレイ最中は罪悪感よりも「今日だけ戻せばいい」が優勢でした。citeturn5view1turn7view2turn36view0turn19view1turn32search3

- **OL・社会人女性では「仕事帰りの一人打ち」が強い導線**でした。最初の入口が恋愛や同僚会話でも、数週間〜数か月で一人打ちへ移行し、給料日直行、残業・約束キャンセル、上限書き換えが起きやすい。快楽期よりも、後半は「静かにするために打つ」記述が増えます。citeturn35view0turn36view1turn31view2turn19view0

- **風俗・夜職系女性は「日払い現金」と「昼の空き時間」と「ストレス抜き」の三点セット**が極めて強いです。夜勤明け→仮眠→昼スロ、負け→その場で現金調達、というように、ホールが一日の中継地点ではなくルーティンの核に入り込みます。citeturn44view0turn27view0turn25view0turn45search5

- **若年女性カテゴリでは、導入に「彼氏」「母」「身近な大人」の影響が目立ちます。** しかも入口は「恋愛」「見学」「暇つぶし」「アニメ演出」で軽く、最初から借金目的で始まるわけではない。それが低貸し→通常レート、月1〜2回→一人打ちへと滑っていく。citeturn31view1turn36view0turn23search1turn25view2

- **全カテゴリに共通して「負けをその場で終わらせない思考」が非常に強い**です。残金が減るほど撤退ではなく再戦に傾き、「今日をただの負け日にしない」が強くなる。数理的判断ではなく、**その日の物語を敗北で閉じたくない心理**として出ています。citeturn29view0turn36view1turn19view0turn25view2

- **羞恥と孤立は、ホール外の長期問題ではなく、プレイ直後の反応としてすでに強く出る**ことが多いです。打ちながらは麻痺していても、退店直後に「夫・親・彼氏に言えない」「また嘘をつく」「でも明日も行く」が同時に立ち上がる。この二重性は女性当事者素材としてかなり重要です。citeturn7view2turn16view0turn36view1turn45search5

- **食行動や買い物へのスライド**も目立ちました。大負け後に惣菜や甘い物を大量買いする、負けを“ただの損失日”にしないために服やアクセを買う、など、ホール直後の感情調整が別依存へ流れる場面が複数見られます。シミュレーションでは「退店後の補償的消費」を別変数で持たせる価値があります。citeturn19view0turn32search3

## ソース評価

今回の 32 カードの内訳は、**公開個人ブログ・note・Ameba 13 件、支援団体・公的体験記 11 件、公開相談投稿 4 件、取材記事 4 件**でした。  
最も密度が高かったのは、公的・支援団体系では entity["organization","厚生労働省","japan ministry"] の体験記と、entity["organization","依存症対策全国センター","support center japan"] 掲載の当事者手記 PDF 群でした。ここは**「きっかけ→深まり→借金→隠蔽→限界」**が通しで読めるため、ペルソナの時系列パラメータ化に向いています。citeturn5view3turn35view0turn36view0turn36view1

個人ブログや note は、**内面独白の口語強度**で最も優れていました。特に「紙幣が紙切れになる」「機械の体になる」「1万円入れてやる」「今日使っても明日入る」といった、**係数化しやすい短い言い回し**が取れます。一方で、人物属性は曖昧なことも多く、**カード化時に推定が混ざる**ため confidence は一段落とすのが妥当です。citeturn19view0turn19view1turn32search3turn44view0turn45search5

取材記事は、危機場面の描写には有用でしたが、**連日連夜の微細な心理推移**は一次手記より薄いです。今回だと、主婦の 570 万円損失事例や、いわゆる「パチンコ売春」の導線把握には役立ちましたが、パラメータ設計の主軸はやはり一次手記に置くべきです。citeturn7view2turn27view0

R2 以降でも有効そうなのは、**長文の回復手記 PDF、長期運営の個人ブログ、公開相談投稿**です。特に回復手記は末期症状だけでなく、最初期の「面白かった」「軽かった」「まだ大丈夫だと思っていた」が取れるため、高齢者・回復期・初心者のラウンドにも横展開しやすいです。終盤の切り返し導線としては、entity["organization","Gamblers Anonymous","self-help fellowship"] などの自助グループ言及が繰り返し現れました。citeturn36view0turn36view1turn16view0

このラウンドの弱点は明確で、**Cカテゴリの純粋な“一次の夜職当事者×ホール内マイクロ心理”はまだ薄い**こと、そして**若年女性は相談投稿由来が多く、本人属性の検証性がやや低い**ことです。R1 の次の補強先は、夜職経験者の長文 note・Ameba と、若年女性の連続投稿型ブログだと思います。