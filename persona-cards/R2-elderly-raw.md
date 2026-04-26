# 高齢者と不労所得層のホール内心理反応ライブラリ R2

## 調査の前提と限界

今回は、公開ソースで質を保てた **27カード** のみを採録した。内訳は、A=8、B=10、C=5、D=4 である。特に C は、依頼文どおり公開ソースが薄く、無理な水増しはしていない。D も、50代前半〜60代前半の当事者が自分で内面を語る公開記録が少なく、やや高齢寄りの「退職後発症・退職後再燃」事例が混ざる。数値項目は出典から読める範囲で丸め、内面独白は**設計用に再構成した非引用文**である。

背景としては、高齢者のギャンブルは「交流」が必ずしも中心ではなく、女性では男性より金銭執着が弱い傾向が示唆されている。また、日本の全国調査では 70–74歳でも生涯ギャンブル経験率が 67.9% とされ、高齢層それ自体が希少母集団ではない。さらに、退職とギャンブル行動の関係は日本の科研でも検証対象になっており、海外研究でも 50歳以上就業者では「問題ギャンブル」や「社交目的のギャンブル」がその後の退職と関連した報告がある。citeturn32view0turn35search2turn8search0turn34search11

## 年金生活高齢男性カード

- id: R2-A-001
  category: 年金生活高齢男性
  profile:
    age_range: "70代後半"
    occupation: "年金生活（元会社員）"
    family: "妻と死別、息子は遠方"
    monthly_income_yen: "不明（年金中心）"
    debt_yen: "不明"
    addiction_severity: "中度（居場所固定型）"
    gambling_history: "千葉のマイホへほぼ毎日通っていたが、妻の死去後に転居。帰郷後に再開"
    visit_motive: "顔見知りがいる場所に戻りたい／土地勘と会話のしやすさ"
  trigger:
    event: "会員証の再発行を頼み、5年ぶりに元のホールへ戻る"
    machine_type: "1円パチンコ"
    time_of_day: "昼前後〜夕方"
  inner_monologue_ja: "鹿児島じゃ言葉も空気もよそ者だった。ここなら黙って座っても、自分の席がある"
  emotional_state:
    arousal_0_100: 38
    despair_0_100: 33
    dominant_emotion: "安堵 × 寂しさ"
  action: "以前と同じホールへの来店を再開"
  post_play_state: "勝敗より『戻ってこられた』感覚が残る"
  source:
    type: "ホール業界コラム"
    url_or_ref: "5年ぶりに戻った77〜78歳常連の聞き取り"
    confidence: "中"
    cite: citeturn20view2
  notes: "方言が通じない環境では楽しさが消え、ホールは『遊技』より『所属の確認』になっている"

- id: R2-A-002
  category: 年金生活高齢男性
  profile:
    age_range: "70代前半〜後半"
    occupation: "年金生活"
    family: "不明"
    monthly_income_yen: "不明"
    debt_yen: 0
    addiction_severity: "軽度〜中度（習慣・社交型）"
    gambling_history: "1パチ常連だったが、後にチェスへ関心が移行"
    visit_motive: "顔見知りの安否確認／挨拶／日課"
  trigger:
    event: "いつもの時間にホールへ行き、短く打ちながら常連の顔を見る"
    machine_type: "1円パチンコ"
    time_of_day: "日中"
  inner_monologue_ja: "玉を打ちたいってより、あいつら元気か見に来てるんだよな"
  emotional_state:
    arousal_0_100: 27
    despair_0_100: 18
    dominant_emotion: "習慣的安堵 × 義理"
  action: "遊技時間は短く、会話と挨拶が主になる"
  post_play_state: "『今日は来てたな』という確認で一日が落ち着く"
  source:
    type: "ホール業界コラム"
    url_or_ref: "1パチ常連シニアがチェスへ移行したAさんの発言"
    confidence: "中"
    cite: citeturn19view2
  notes: "本人が『打ちたくて来ていたのではない』と気づくタイプ。依存症層と違い、対象は玉ではなく顔ぶれ"

- id: R2-A-003
  category: 年金生活高齢男性
  profile:
    age_range: "70代後半"
    occupation: "年金生活"
    family: "実子あり"
    monthly_income_yen: "不明（年金の大半を遊技へ）"
    debt_yen: "未発生だが家族は懸念"
    addiction_severity: "中度〜重度"
    gambling_history: "長年継続。加齢後も年金で反復"
    visit_motive: "年金日後の反復習慣／一度始めると止めづらい"
  trigger:
    event: "年金受給後、クレジットや現金へのアクセスを家族が心配する水準で通う"
    machine_type: "不明"
    time_of_day: "不明（日中中心と推定）"
  inner_monologue_ja: "まだ借りてない。今日はこれで終える。そう思っても、手が止まらない"
  emotional_state:
    arousal_0_100: 46
    despair_0_100: 52
    dominant_emotion: "惰性 × 破綻不安"
  action: "年金の多くを打ち込み続ける"
  post_play_state: "家族は借金発生を先回りで警戒"
  source:
    type: "Q&A投稿"
    url_or_ref: "78歳年金暮らしの父がパチンコで散財する家族相談"
    confidence: "中"
    cite: citeturn19view6
  notes: "『今は借金がない』段階でも、家族側は認知低下と決済手段の組み合わせを強いリスクとして見ている"

- id: R2-A-004
  category: 年金生活高齢男性
  profile:
    age_range: "70代前半〜後半"
    occupation: "元高校教師、現在は高齢の依存当事者"
    family: "不明"
    monthly_income_yen: "不明"
    debt_yen: "不明"
    addiction_severity: "重度"
    gambling_history: "パチンコに約2000万円を投じた"
    visit_motive: "強迫的反復／生活の空洞化"
  trigger:
    event: "手元資金があるたびにホールへ向かう反復があったと要約される"
    machine_type: "パチンコ"
    time_of_day: "不明"
  inner_monologue_ja: "もう戻らない金だと分かっても、行かない日をどう過ごせばいいか分からなかった"
  emotional_state:
    arousal_0_100: 54
    despair_0_100: 84
    dominant_emotion: "後悔 × 空虚"
  action: "長期にわたり打ち続ける"
  post_play_state: "治療中で、金と時間を失った感覚が前景化"
  source:
    type: "テレビ番組要約"
    url_or_ref: "高齢依存で2000万円を失った元高校教師のケース"
    confidence: "低〜中"
    cite: citeturn19view5
  notes: "ホール内の細部は薄いが、『老年期の後悔が遅れて押し寄せる』重い参照事例"

- id: R2-A-005
  category: 年金生活高齢男性
  profile:
    age_range: "70代半ば"
    occupation: "年金生活"
    family: "妻あり"
    monthly_income_yen: "不明（夫婦年金生活）"
    debt_yen: 0
    addiction_severity: "軽度（夫婦日課型）"
    gambling_history: "昔からパチンコ好き。現在は低貸で継続"
    visit_motive: "夫婦の共通習慣／会話のネタ／ボケ防止感覚"
  trigger:
    event: "夫婦で50銭パチンコへ行き、月額上限内でほぼ毎日遊ぶ"
    machine_type: "50銭パチンコ"
    time_of_day: "日中"
  inner_monologue_ja: "勝つ負けるより、今日は何の台を打ったか家で話せりゃいい"
  emotional_state:
    arousal_0_100: 23
    despair_0_100: 13
    dominant_emotion: "穏やかな日課"
  action: "低予算で一定時間だけ打つ"
  post_play_state: "夫婦の会話が増え、日課が完成する"
  source:
    type: "ホール業界コラム"
    url_or_ref: "76歳父が妻と50銭パチンコへ通う家族証言"
    confidence: "中"
    cite: citeturn22view2
  notes: "依存症より『老後ルーティン』に近い。勝敗への執着が低い"

- id: R2-A-006
  category: 年金生活高齢男性
  profile:
    age_range: "70代前半"
    occupation: "高齢ギャンブラー"
    family: "不明"
    monthly_income_yen: "年金なし"
    debt_yen: "不明"
    addiction_severity: "重度"
    gambling_history: "50年以上のギャンブル歴"
    visit_motive: "長年の身体化した習慣／やめても空白になる"
  trigger:
    event: "老後破産状態でも打ちに向かう高齢当事者として紹介"
    machine_type: "パチンコを含むギャンブル"
    time_of_day: "不明"
  inner_monologue_ja: "金も貯えもない。でも、今日の時間だけは何かで埋めたい"
  emotional_state:
    arousal_0_100: 59
    despair_0_100: 79
    dominant_emotion: "意地 × 老後破綻感"
  action: "ギャンブル生活をやめきれない"
  post_play_state: "『年金なし、貯金なし』の崖っぷち感が残る"
  source:
    type: "法律メディア記事要約"
    url_or_ref: "71歳・50年超のギャンブル人生を歩んだ男性の紹介"
    confidence: "低〜中"
    cite: citeturn11search10
  notes: "ホール内ディテールは薄いが、A の重症端点として有用"

- id: R2-A-007
  category: 年金生活高齢男性
  profile:
    age_range: "60代後半〜70代前半"
    occupation: "定年後の再就労あり"
    family: "妻と二人暮らし、子は独立"
    monthly_income_yen: "不明（夫婦収入・貯蓄あり）"
    debt_yen: 0
    addiction_severity: "軽度〜中度（解放日型）"
    gambling_history: "もともと好きだったが一度離脱、定年後に再開"
    visit_motive: "仕事のない日だけの楽しみ／一人で過ごす休みの埋め草"
  trigger:
    event: "連休前や休みの日に、1パチ甘デジ海へ行く"
    machine_type: "1円パチンコ・甘デジ海"
    time_of_day: "昼以降"
  inner_monologue_ja: "家計は崩してない。これくらいなら俺の休みの使い方だろ"
  emotional_state:
    arousal_0_100: 34
    despair_0_100: 18
    dominant_emotion: "解放感 × 夫婦摩擦回避"
  action: "週1前後で遊技。時に頻度が増える"
  post_play_state: "本人は娯楽認識、妻は『共有老後』を奪われた感覚"
  source:
    type: "Q&A投稿"
    url_or_ref: "定年後に1パチ甘デジ海を再開した夫への妻の相談"
    confidence: "中"
    cite: citeturn20view5
  notes: "金銭破綻はないが、老後の時間配分をめぐる夫婦摩擦が強い"

- id: R2-A-008
  category: 年金生活高齢男性
  profile:
    age_range: "70代後半〜80代前半"
    occupation: "引退後の高齢男性"
    family: "不明"
    monthly_income_yen: "不明"
    debt_yen: "不明"
    addiction_severity: "中度（開催日追従型）"
    gambling_history: "競輪・競馬・競艇・パチンコを横断する長年のギャンブル習慣"
    visit_motive: "その日『何かを賭ける場』がないことへの耐性の低さ"
  trigger:
    event: "外出先がなくなると、パチンコ営業店の情報を仲間経由で探す"
    machine_type: "パチンコ"
    time_of_day: "日中"
  inner_monologue_ja: "行くところが一個でも開いてりゃ、家でぼんやりしてるよりマシだ"
  emotional_state:
    arousal_0_100: 41
    despair_0_100: 29
    dominant_emotion: "退屈回避 × 反射的外出"
  action: "営業している店を探し、移動距離が伸びても向かう"
  post_play_state: "打てたかどうかより『今日も外へ出られたか』が残る"
  source:
    type: "生活体験投稿"
    url_or_ref: "80歳義父が営業店を探してパチンコへ行こうとする家族談"
    confidence: "中"
    cite: citeturn41search1
  notes: "年齢は依頼レンジを外れるが、『居場所がない日の反射的来店』の参照価値が高い"

## 年金生活高齢女性カード

- id: R2-B-001
  category: 年金生活高齢女性
  profile:
    age_range: "70代"
    occupation: "主婦経験・現在は高齢者"
    family: "孫は成長し、日中の役割が薄い"
    monthly_income_yen: "不明"
    debt_yen: 0
    addiction_severity: "軽度（休憩所併用型）"
    gambling_history: "休憩所利用と時折の遊技"
    visit_motive: "時間余り／休憩所の居心地／少しだけ刺激が欲しい"
  trigger:
    event: "休憩所で血圧を測り、知恵の輪をし、時々1円台へ移る"
    machine_type: "低貸パチンコ"
    time_of_day: "昼前後"
  inner_monologue_ja: "家にいても用事がない。ここならテレビより少しだけ生きてる感じがする"
  emotional_state:
    arousal_0_100: 24
    despair_0_100: 20
    dominant_emotion: "退屈しのぎ × 穏やかな浮上"
  action: "休憩所と遊技台を往復する"
  post_play_state: "一日が空白にならずに済む"
  source:
    type: "テレビ番組要約の業界記事"
    url_or_ref: "孫離れ後に休憩所へ通う70代主婦"
    confidence: "中"
    cite: citeturn20view4
  notes: "『打つこと』単独ではなく、ホール内設備込みの来店動機"

- id: R2-B-002
  category: 年金生活高齢女性
  profile:
    age_range: "60代"
    occupation: "主婦"
    family: "不明"
    monthly_income_yen: "不明"
    debt_yen: 0
    addiction_severity: "中度（感情麻酔型）"
    gambling_history: "近所に内緒で継続"
    visit_motive: "喪失感の一時遮断／後ろめたさを抱えた息抜き"
  trigger:
    event: "世間の目を気にしながら店に入り、負けても打ち続ける"
    machine_type: "1円パチンコと推定"
    time_of_day: "日中"
  inner_monologue_ja: "無駄だし恥ずかしい。でも、家で泣いてるより一瞬だけ忘れられる"
  emotional_state:
    arousal_0_100: 49
    despair_0_100: 46
    dominant_emotion: "後ろめたさ × 一時逃避"
  action: "負けを自覚しつつ店を離れない"
  post_play_state: "虚しさは残るが、喪失感の輪郭だけ薄まる"
  source:
    type: "テレビ番組要約の業界記事"
    url_or_ref: "犬を亡くした後に泣きながら打った60代主婦"
    confidence: "中"
    cite: citeturn20view4
  notes: "金銭欲よりも、感情の鈍麻・空白時間の断片化が中心"

- id: R2-B-003
  category: 年金生活高齢女性
  profile:
    age_range: "70代"
    occupation: "元スナックママ、当時は介護職"
    family: "不明"
    monthly_income_yen: "不明"
    debt_yen: 0
    addiction_severity: "軽度〜中度（美意識伴走型）"
    gambling_history: "仕事後に習慣化"
    visit_motive: "仕事後の切替／自分を整え直す時間"
  trigger:
    event: "仕事を終え、着替えておしゃれしてからホールへ向かう"
    machine_type: "パチンコ"
    time_of_day: "夕方〜夜"
  inner_monologue_ja: "この時間だけは、まだ女でいられる。台も店も綺麗なら、それでいい"
  emotional_state:
    arousal_0_100: 43
    despair_0_100: 21
    dominant_emotion: "自己演出 × 静かな高揚"
  action: "きれいな台を選び、一定時間だけ打つ"
  post_play_state: "勝敗より、身なりと気分の整いが残る"
  source:
    type: "テレビ番組要約の業界記事"
    url_or_ref: "元スナックママの70代女性のインタビュー"
    confidence: "中"
    cite: citeturn20view4
  notes: "高齢女性でも『社交』より『自分の見え方を保つ儀式』として打つ例"

- id: R2-B-004
  category: 年金生活高齢女性
  profile:
    age_range: "70代前後"
    occupation: "年金生活"
    family: "一人暮らし、子や孫の話題あり"
    monthly_income_yen: "年金中心"
    debt_yen: 0
    addiction_severity: "中度（勝ち記憶優位型）"
    gambling_history: "20年以上"
    visit_motive: "生活費補填意識と暇つぶしの混合"
  trigger:
    event: "所用後に立ち寄り、戦績を他人に話したくなる"
    machine_type: "パチンコ"
    time_of_day: "午後"
  inner_monologue_ja: "負けた日のことは忘れるの。勝った日だけ覚えてりゃ、また来られるから"
  emotional_state:
    arousal_0_100: 52
    despair_0_100: 27
    dominant_emotion: "上機嫌 × 記憶の選別"
  action: "勝敗談を語り、再入店する"
  post_play_state: "勝てば饒舌、負けても記憶の重みを薄くする"
  source:
    type: "個人エッセイ"
    url_or_ref: "喫煙所で会った年金暮らしのおばあちゃん"
    confidence: "中"
    cite: citeturn20view0
  notes: "『パチンコはやめときな』と言いながら自分は戻る二重性が重要"

- id: R2-B-005
  category: 年金生活高齢女性
  profile:
    age_range: "70代前後"
    occupation: "不明"
    family: "不明"
    monthly_income_yen: "不明"
    debt_yen: "不明"
    addiction_severity: "中度（感情表出型）"
    gambling_history: "常連化"
    visit_motive: "日課／店員との接触／台への不満の吐き出し"
  trigger:
    event: "近くを通る店員に、勝ち負けの報告や不満をぶつける"
    machine_type: "パチンコ"
    time_of_day: "日中"
  inner_monologue_ja: "今日はダメだ、見てよこれ。誰かに言わないと腹がおさまらない"
  emotional_state:
    arousal_0_100: 57
    despair_0_100: 31
    dominant_emotion: "苛立ち × 依存的接触"
  action: "負けると店員を捕まえて訴える"
  post_play_state: "不機嫌の共有で少し下がるが、根本解消はしない"
  source:
    type: "ホール勤務者エッセイ"
    url_or_ref: "高齢女性『カワサキさん』への店員観察"
    confidence: "中"
    cite: citeturn20view3
  notes: "店員が感情の受け皿になっている。勝敗無関心ではなく、勝敗を人へ渡して処理する型"

- id: R2-B-006
  category: 年金生活高齢女性
  profile:
    age_range: "70代前後"
    occupation: "祖母・無職"
    family: "孫あり"
    monthly_income_yen: "不明"
    debt_yen: 0
    addiction_severity: "中度（午後固定型）"
    gambling_history: "毎日、客足が落ち着く頃に来店"
    visit_motive: "午後の定位置／店員との顔なじみ関係／家の外で機嫌よく過ごす"
  trigger:
    event: "店が少し空く時間帯に来店し、当たると孫を景品カウンターへ呼ぶ"
    machine_type: "パチンコ"
    time_of_day: "午後"
  inner_monologue_ja: "混んでる時間は嫌。少し静かになった頃に来て、当たったらそれで十分"
  emotional_state:
    arousal_0_100: 36
    despair_0_100: 17
    dominant_emotion: "馴染み感 × 軽い期待"
  action: "短〜中時間だけ打ち、当たれば景品選びへつなげる"
  post_play_state: "勝ち負けより、知っている店員に通じる感覚が残る"
  source:
    type: "個人エッセイ"
    url_or_ref: "祖母が毎日パチンコへ行き、店員が景品を案内してくれた記憶"
    confidence: "中"
    cite: citeturn23view0
  notes: "高齢女性の『馴染みの店員』は、台以上にホール定着を強める"

- id: R2-B-007
  category: 年金生活高齢女性
  profile:
    age_range: "80歳超"
    occupation: "高齢女性"
    family: "不明"
    monthly_income_yen: "不明"
    debt_yen: 0
    addiction_severity: "軽度〜中度（高稼働高体力型）"
    gambling_history: "朝一番の常連"
    visit_motive: "朝の定位置／勝負より『今日も来た』感覚"
  trigger:
    event: "朝一番に4パチへ座り、連チャンが続く"
    machine_type: "4円パチンコ"
    time_of_day: "朝〜昼"
  inner_monologue_ja: "まだやれる。でも体は正直だね、ちょっと休ませて"
  emotional_state:
    arousal_0_100: 61
    despair_0_100: 10
    dominant_emotion: "快活 × 身体疲労"
  action: "大当たり中も無理をせず、顔なじみの店長を呼ぶ"
  post_play_state: "勝ちの高揚より、身体が先に限界を知らせる"
  source:
    type: "ホール業界コラム"
    url_or_ref: "80歳超の常連女性が朝一から連チャンした事例"
    confidence: "中"
    cite: citeturn22view0
  notes: "高齢女性の強い常連性。感情より体力限界が行動停止要因になる"

- id: R2-B-008
  category: 年金生活高齢女性
  profile:
    age_range: "高齢女性"
    occupation: "不明"
    family: "不明"
    monthly_income_yen: "不明"
    debt_yen: "不明"
    addiction_severity: "中度（台固定執着型）"
    gambling_history: "毎日同じ台"
    visit_motive: "同じ台・同じリズムで安心したい"
  trigger:
    event: "毎朝、1円の新海物語3Rの同じ台へ座り、40回当たりまで帰らない"
    machine_type: "1円パチンコ・新海物語3R"
    time_of_day: "朝一〜19時頃"
  inner_monologue_ja: "今日はここまで届いてから帰る。途中でやめると一日が気持ち悪い"
  emotional_state:
    arousal_0_100: 42
    despair_0_100: 24
    dominant_emotion: "執拗なルーティン × 小さな緊張"
  action: "食事休憩ほぼなしで同一台を打ち続ける"
  post_play_state: "当たり回数のノルマ達成感が残る"
  source:
    type: "Q&A投稿"
    url_or_ref: "店員が観察した『毎日同じ1円海を打つ高齢女性』"
    confidence: "中"
    cite: citeturn13search1
  notes: "勝敗より『規定回数まで座る』ことが目的化している"

- id: R2-B-009
  category: 年金生活高齢女性
  profile:
    age_range: "70代"
    occupation: "高齢女性"
    family: "震災後に息子夫婦のもとへ身を寄せる"
    monthly_income_yen: "不明"
    debt_yen: 0
    addiction_severity: "軽度〜中度（退避型）"
    gambling_history: "震災後に開始"
    visit_motive: "家に居づらい／人と話さなくてよい場所が欲しい"
  trigger:
    event: "息子夫婦宅に居場所を感じられず、1円パチンコ店へ向かう"
    machine_type: "1円パチンコ"
    time_of_day: "日中"
  inner_monologue_ja: "ここは誰とも深く話さなくていい。ただ座っていれば時間が過ぎる"
  emotional_state:
    arousal_0_100: 29
    despair_0_100: 41
    dominant_emotion: "疎外感 × 静かな避難"
  action: "低貸コーナーで淡々と打つ"
  post_play_state: "家へ戻る前に気持ちのざらつきが少し均される"
  source:
    type: "番組配信サイト要約"
    url_or_ref: "震災後にパチンコを始めた70代女性"
    confidence: "中"
    cite: citeturn44view1
  notes: "『社交』ではなく『非会話でいられる公共空間』としてのホール"

- id: R2-B-010
  category: 年金生活高齢女性
  profile:
    age_range: "70代前後"
    occupation: "高齢女性"
    family: "長年連れ添った夫を亡くした直後"
    monthly_income_yen: "不明"
    debt_yen: 0
    addiction_severity: "軽度（弔い儀式型）"
    gambling_history: "夫婦で長年の共通趣味"
    visit_motive: "悲嘆処理ではなく、夫との約束の履行"
  trigger:
    event: "夫が朝に亡くなったその日の夕方、いつものようにホールへ行く"
    machine_type: "パチンコ"
    time_of_day: "夕方"
  inner_monologue_ja: "今日は行く日じゃない。でも、行くって約束してたから、行かなきゃ"
  emotional_state:
    arousal_0_100: 22
    despair_0_100: 72
    dominant_emotion: "悲嘆 × 儀式的忠実さ"
  action: "短時間でも席に着き、夫婦の約束どおり打つ"
  post_play_state: "遊技そのものより、供養を終えた感覚が残る"
  source:
    type: "ホール業界コラム"
    url_or_ref: "夫の死当日に来店した老夫婦の妻の事例"
    confidence: "中"
    cite: citeturn22view5
  notes: "勝敗や暇つぶしで説明できない『ホール儀礼化』の希少ケース"

## 不労所得層カード

- id: R2-C-001
  category: 不労所得・地主系
  profile:
    age_range: "高齢男性"
    occupation: "地主"
    family: "不明"
    monthly_income_yen: "不明（高資産とされる）"
    debt_yen: 0
    addiction_severity: "軽度（低反応常連型）"
    gambling_history: "ほぼ毎日・長期継続"
    visit_motive: "暇つぶし／定位置習慣"
  trigger:
    event: "毎朝、4パチ海の角台へ座り、夕方まで打つ"
    machine_type: "4円パチンコ・海シリーズ"
    time_of_day: "朝一〜夕方"
  inner_monologue_ja: "今日は出ても出なくてもいい。角だし、海だし、いつも通りでいい"
  emotional_state:
    arousal_0_100: 33
    despair_0_100: 9
    dominant_emotion: "平坦な没入"
  action: "同じ台・同じ時間幅で打ち続ける"
  post_play_state: "金額より『今日も一日座った』感覚が残る"
  source:
    type: "Q&A投稿の回答"
    url_or_ref: "地主のご老人が毎朝同じ海の角台を打つという目撃談"
    confidence: "中"
    cite: citeturn28view0
  notes: "依頼文の想定どおり、C は arousal がかなり低い。勝敗無関心が明瞭"

- id: R2-C-002
  category: 不労所得・地主系
  profile:
    age_range: "高齢女性と中高年女性"
    occupation: "地主の妻と娘"
    family: "母娘"
    monthly_income_yen: "不明（資産余裕ありと目撃者が認識）"
    debt_yen: 0
    addiction_severity: "軽度（来店常態化型）"
    gambling_history: "ほぼ毎日"
    visit_motive: "暇つぶし／店員との会話／外出習慣"
  trigger:
    event: "毎日来店し、店員と長く話し込みながら打つ"
    machine_type: "不明"
    time_of_day: "日中"
  inner_monologue_ja: "家に居ても退屈だし、ここなら誰かいる。お金のことは別に困ってないし"
  emotional_state:
    arousal_0_100: 31
    despair_0_100: 11
    dominant_emotion: "暇つぶし × 社交"
  action: "遊技と雑談をゆっくり反復する"
  post_play_state: "勝敗より会話量と滞在満足が残る"
  source:
    type: "Q&A投稿の回答"
    url_or_ref: "地主の奥さんと娘がほぼ毎日来ていたという元勤務者の証言"
    confidence: "中"
    cite: citeturn30search0
  notes: "金銭プレッシャーの薄さが、滞在を『老人介護的な店員会話』へ変えている"

- id: R2-C-003
  category: 不労所得・社長引退系
  profile:
    age_range: "50代〜60代中心と推定"
    occupation: "零細企業社長・経営者層"
    family: "不明"
    monthly_income_yen: "不明"
    debt_yen: 0
    addiction_severity: "軽度（余裕常連型）"
    gambling_history: "ホールの常連として反復来店"
    visit_motive: "暇つぶし／気軽な会話／上下関係の弱い第三の場"
  trigger:
    event: "ホールで無職の投稿者とも経営や保険の話をする"
    machine_type: "主にスロットと推定"
    time_of_day: "日中"
  inner_monologue_ja: "台そのものより、人と話すほうが面白い日もある。ここは肩書きをちょっと脱げる"
  emotional_state:
    arousal_0_100: 35
    despair_0_100: 8
    dominant_emotion: "余裕 × 社交的観察"
  action: "打ちながら周囲と会話し、遊技はあくまで背景化"
  post_play_state: "損得より『気分転換できたか』が評価軸"
  source:
    type: "個人note"
    url_or_ref: "パチ屋で会った社長・お金持ち常連の観察"
    confidence: "低〜中"
    cite: citeturn25search0turn26view1
  notes: "単一人物ではなく『社長系常連』の凝縮像。Cの資料薄さを補う低圧カード"

- id: R2-C-004
  category: 不労所得・役員系
  profile:
    age_range: "40代後半〜60代"
    occupation: "役員・偉い人・時間に余裕のある常連"
    family: "不明"
    monthly_income_yen: "不明"
    debt_yen: 0
    addiction_severity: "軽度"
    gambling_history: "長期常連"
    visit_motive: "居心地のよいネットワーク維持／勝ち急がない遊技"
  trigger:
    event: "高設定の情報が出ても、他常連に譲ったり声をかけたりする"
    machine_type: "スロット"
    time_of_day: "日中"
  inner_monologue_ja: "慌てなくても時間はある。今日は俺が取らなくても別にいい"
  emotional_state:
    arousal_0_100: 30
    despair_0_100: 7
    dominant_emotion: "余裕 × 関係維持"
  action: "期待値だけで突っ走らず、関係性を優先して立ち回る"
  post_play_state: "勝ち負けより、ホール内の居心地が保たれる"
  source:
    type: "個人note"
    url_or_ref: "お金持ちや役員層とホールで関係ができたという観察"
    confidence: "低〜中"
    cite: citeturn26view2
  notes: "時間制約の弱さが arousal を抑え、対人関係重視の立ち回りに変わる"

- id: R2-C-005
  category: 金銭プレッシャー希薄な趣味層
  profile:
    age_range: "年齢不明"
    occupation: "不明"
    family: "不明"
    monthly_income_yen: "不明"
    debt_yen: 0
    addiction_severity: "軽度（完全趣味勢）"
    gambling_history: "複数のローカルホールへ長年通う"
    visit_motive: "一日を楽しく過ごすこと／店員・常連との馴染み"
  trigger:
    event: "マイホで大きくは勝ちたくない、と自覚しつつ来店"
    machine_type: "パチンコ"
    time_of_day: "日中"
  inner_monologue_ja: "ちょい負けで一日楽しかったなら十分。今日は店の空気が良ければそれで勝ち"
  emotional_state:
    arousal_0_100: 34
    despair_0_100: 12
    dominant_emotion: "穏やかな没入 × 愛着"
  action: "小さな負けを許容し、気持ちよく長く遊ぶ"
  post_play_state: "損益より『今日も楽しかった』が残る"
  source:
    type: "遊技ブログコメント"
    url_or_ref: "完全趣味勢で小さな負けを許容する打ち手の発言"
    confidence: "低〜中"
    cite: citeturn26view3
  notes: "C の比較ベースとして有効。『勝ちたい』より『続けたい』が強い"

## 退職前後男性カード

- id: R2-D-001
  category: 退職前後・早期リタイア男性
  profile:
    age_range: "60代半ば"
    occupation: "完全リタイア"
    family: "妻あり"
    monthly_income_yen: "年金23万円＋妻収入で40万円超"
    debt_yen: 0
    addiction_severity: "中度（退職後導入型）"
    gambling_history: "若い頃は未経験、退職後に同級生に勧められ開始"
    visit_motive: "無趣味ゆえの空白時間処理"
  trigger:
    event: "完全リタイア後、同級生に誘われて1パチを打ち始める"
    machine_type: "1円パチンコ"
    time_of_day: "日中"
  inner_monologue_ja: "家も片付いてるし、今日は何をするでもない。少し打てば時間が埋まる"
  emotional_state:
    arousal_0_100: 44
    despair_0_100: 18
    dominant_emotion: "退屈の浮上 × 初期高揚"
  action: "月3万円前後を使うペースで継続"
  post_play_state: "初の大勝ち後、興奮を妻へ持ち帰り共有したくなる"
  source:
    type: "ホール業界コラム"
    url_or_ref: "完全リタイア後に初めてのパチンコへ入ったAさん"
    confidence: "中"
    cite: citeturn22view4
  notes: "D の典型。『金に困ってないのに始める』退職導入型"

- id: R2-D-002
  category: 退職前後・早期リタイア男性
  profile:
    age_range: "70代後半"
    occupation: "年金生活（元教師）"
    family: "妻あり"
    monthly_income_yen: "不明（年金多めと家族談）"
    debt_yen: "義姉から借金"
    addiction_severity: "中度〜重度"
    gambling_history: "退職後に『一度やってみたい』で開始し、その後毎日化"
    visit_motive: "真面目一筋の反動／初当たりの興奮の再追体験"
  trigger:
    event: "妻と軽い気持ちで初来店し、3000円が7万円になる"
    machine_type: "パチンコ"
    time_of_day: "日中"
  inner_monologue_ja: "もう一回だけ、あの最初の当たりを確かめたい。今日で最後のはずなんだ"
  emotional_state:
    arousal_0_100: 71
    despair_0_100: 36
    dominant_emotion: "初当たり記憶への執着"
  action: "毎日通うようになり、家族に隠れて金を借りる"
  post_play_state: "朝には『また行きたい』が復活する"
  source:
    type: "生活体験投稿"
    url_or_ref: "元教師の78歳父が初当たり後に毎日通うようになった話"
    confidence: "中"
    cite: citeturn38view0
  notes: "D の重要型。退職後の『遅い初体験』は、若年時の依存よりも家族の盲点になりやすい"

- id: R2-D-003
  category: 退職前後・早期リタイア男性
  profile:
    age_range: "70代後半前後"
    occupation: "自営業引退"
    family: "義母・子世帯と同居"
    monthly_income_yen: "年金＋貯金"
    debt_yen: 0
    addiction_severity: "中度"
    gambling_history: "現役時代は我慢、引退後に一気に解放"
    visit_motive: "長年我慢した分の解禁感／外で一日過ごしたい"
  trigger:
    event: "店をたたんだ後、朝から夕飯時まで家にいなくなる"
    machine_type: "パチンコ＋他公営ギャンブル"
    time_of_day: "朝〜夕方"
  inner_monologue_ja: "もう働かなくていいんだ。今まで我慢した分、好きにして何が悪い"
  emotional_state:
    arousal_0_100: 48
    despair_0_100: 29
    dominant_emotion: "解禁感 × 反発"
  action: "毎日の外出先が遊技場中心になっていく"
  post_play_state: "負けた日は落胆が表情に出るが、翌日も外へ出る"
  source:
    type: "生活体験投稿"
    url_or_ref: "75歳超で店をたたんだ義父が、引退後にパチンコと競馬へ通う話"
    confidence: "中"
    cite: citeturn40view0
  notes: "『仕事で抑えていた欲求が退職で一斉に解禁される』タイプ"

- id: R2-D-004
  category: 退職前後・早期リタイア男性
  profile:
    age_range: "60代後半〜70代前半"
    occupation: "定年後の再就労（早朝勤務）"
    family: "妻と二人暮らし"
    monthly_income_yen: "不明"
    debt_yen: 0
    addiction_severity: "軽度〜中度"
    gambling_history: "若い頃好きで、一度やめた後に定年後再開"
    visit_motive: "半日仕事後の自由時間の占有"
  trigger:
    event: "休みの前や連休に、1パチ甘デジ海へ向かう"
    machine_type: "1円パチンコ・甘デジ海"
    time_of_day: "昼〜夕方"
  inner_monologue_ja: "これくらいの楽しみは、長く働いたご褒美だろ"
  emotional_state:
    arousal_0_100: 35
    despair_0_100: 16
    dominant_emotion: "自己正当化された解放"
  action: "週1程度から、やや頻度を増やしていく"
  post_play_state: "本人は娯楽処理、妻は約束違反として蓄積"
  source:
    type: "Q&A投稿"
    url_or_ref: "定年後再就労の夫が1パチ海へ向かう妻の相談"
    confidence: "中"
    cite: citeturn20view5
  notes: "D では金銭より『家族より遊技へ時間を先に配る』ことが摩擦源になる"

## メタ観察

1. **A・B と D の最大差は、「暇を埋める」か「役割喪失の反動を処理する」かにある。** A・B はすでに日中役割が薄く、ホールが時計代わり・居場所代わりになっていた。一方 D は、退職直後の「急に空いた時間」と「長年の我慢の解禁」が引き金になりやすく、初当たりや初体験の強い記憶が再燃源になっている。citeturn20view2turn20view4turn22view4turn38view0turn40view0

2. **B は『お金が欲しい』だけでは動いていない。** 喪失の麻酔、身だしなみの切替、店員との馴染み、家に居づらいという感覚が強く、しかもそれを「堂々とは言えない」後ろめたさと同居させていた。首都圏高齢者調査で、女性は男性より「儲け」への執着が弱い示唆が出ていることとも整合的である。citeturn20view4turn20view0turn23view0turn32view0

3. **C は依頼文の仮説どおり、感情の振れ幅が小さい。** 地主常連や趣味勢では「同じ台・同じ時間・同じ顔ぶれ」が価値で、負けは入場料に近い意味づけへ変わる。高揚はあるが大きくは跳ねず、irritation も短く処理されやすい。LLM パラメータ化するなら、C は arousal を 30–40 台、despair を 5–20 台に置くと差が出やすい。citeturn28view0turn30search0turn25search0turn26view2turn26view3

4. **「依存症」と「習慣化された暇つぶし」の境界は、金額よりも可逆性に出る。** 低貸・月額上限・夫婦会話維持・顔見知り確認で回っている人は、ホール外に代替物ができると頻度が落ちうる。逆に、借金・年金消尽・貯金急減・初当たり再追跡・『今日が最後』反復が出ている人は、すでに習慣ではなく拘束に近い。citeturn19view2turn22view2turn19view6turn38view0turn40view0

5. **高齢者の『社交』は一枚岩ではない。** 常連や店員と挨拶する人もいれば、「人と話さなくていいから来る」人もいる。研究でも、高齢者のギャンブルで他者交流が必ずしも重視されないことが示唆されており、ホールは社交場というより「会話を選べる公共空間」と捉える方が再現性が高い。citeturn44view1turn20view2turn20view4turn32view0

6. **ホール内の微小環境が、感情より先に行動を固定する。** 同じ台、同じ角、客足が落ちた時間、休憩所、顔なじみの店員、身体が疲れてきたときに声をかける相手。高齢層では派手な射幸心より、この「摩擦の少ない動線」が継続理由になっていた。モデル化では、機種よりも「席固定性」「店員会話頻度」「休憩所利用」を別変数にした方が効く。citeturn22view0turn23view0turn20view3turn20view4turn28view0

7. **回復・治療文脈では、高齢・借金なし・重症度低めの人ほど予後が良い関連も報告されている。** これは、A/B/C の一部に見られた「低予算・固定ルーティン・感情振幅の小ささ」が、まだ可逆な段階にある可能性を示す。逆に、年金消尽や貯金流出まで進んだ D/A の重症側は、外から見る以上に切り替えが難しい。citeturn32view3turn32view4

## ソース評価

構造理解に最も強いのは、entity["organization","久里浜医療センター","yokosuka, kanagawa, japan"] 関連の全国調査、厚労科研、地域調査である。これらは「高齢者でも経験母数は十分ある」「交流は必須ではない」「女性は男性ほど金銭執着が強くない可能性がある」といった**設計上の大枠**を支えるのに有効だった。カードの数値パラメータを決める際のベースラインとしては、ここが最も信頼できる。citeturn32view0turn35search2turn32view3turn32view4

現場描写では、entity["organization","NHK","japan broadcaster"] の entity["tv_show","ドキュメント72時間","NHK documentary"] と entity["tv_show","NNNドキュメント","japanese documentary news"] のようなテレビ系素材が強かった。特に、「パチンコは人と話さなくてよい」「犬を亡くした後は泣きながら打った」「休憩所で一日を過ごす」といった短い発話は、プレイ中の心的負荷を再現する上で粒度が高い。citeturn44view1turn20view4turn19view5

家族視点の生活体験投稿と Q&A 投稿は、事実検証力では落ちるが、**ホール外から見た違和感** を採るには非常に有用だった。「2時間するとソワソワする」「休みをパチンコのために取る」「朝から夕飯時まで帰らない」「義姉に金を借りる」といった行動反復は、当事者本人が語らない部分を補ってくれる。設計用モノローグ生成では、危機の徴候と家族側の視認ポイントとして重宝する。citeturn38view0turn40view0turn20view5turn19view6

業界コラムや個人 note は、C と A/B の「店員・常連との関係」「同じ台への固着」「ホールを居場所として使う感覚」を拾うのに役立った一方、演出や美談化のバイアスがある。そのため本稿では、そうした素材は**低〜中 confidence** に留め、金額や病像の断定には使わず、ルーティンや感情の平坦さの補助証拠として使った。citeturn22view0turn22view2turn25search0turn26view2turn26view3

C カテゴリについては、今回の結論をはっきり書く。**公開ソースは薄い。** ただし、「地主の老人が毎朝同じ角台」「地主の妻と娘が毎日来る」「社長・役員層が勝敗より会話や居心地を重視する」という断片は確かに存在した。したがって、LLM シミュレーションでは C を重い劇的感情で埋めるより、**低 arousal・低 despair・高 habit・中程度の hall_attachment** で設計する方が、現状の公開証拠には近い。citeturn28view0turn30search0turn25search0turn26view2turn30search9