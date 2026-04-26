# パチスロプレイ中の心理反応ライブラリ R3

## 調査範囲と採用基準

本セットは、公開アクセス可能な一次・準一次資料だけを使い、**ホール内・プレイ中・退店直後**に寄せて再構成した質的カード群である。`inner_monologue_ja` は原文の長い引用ではなく、各ソースの叙述から**ホール内の瞬間反応に限定して要約**した。今回は、公開資料の質を優先したため **24 cards** にとどめた。A と C は本人記述が比較的厚く、B は本人手記が薄いため観察者記述を混ぜ、D は病名をカテゴリで丸めて用いた。

高信頼の核は、entity["organization","NCASA-Japan","japan addiction support"] の当事者手記と、entity["organization","厚生労働省","japan health ministry"]の「こころの耳」体験記である。日本の臨床サンプルでは、病的賭博患者の **4〜5割に感情障害やアルコール依存などの合併**があり、**95%が負債を持ち、3割超が法的債務整理**に至っていた。さらに **3/4 がパチンコ主体**だった。併存精神疾患があると問題が重くなりやすいこと、ギャンブル関連の**視覚・聴覚キュー**が強い反応を起こすことも、国内の医療・研究資料で繰り返し示されている。したがって本セットの `arousal / despair / interruptibility / mood_lability / impulse_control / dissociation_tendency` は、本人叙述に加えてこれらの臨床知見と整合するように推定した。 citeturn24view0turn26view0turn33view0turn38search0turn10search11turn8search11turn38search8

## 依存症末期カード

- id: R3-A-001
  category: 依存症末期
  profile:
    age_range: "50代"
    occupation: "公務員"
    family: "親・長男と断絶寸前"
    debt_yen: 15000000
    addiction_severity: "末期（7社借入、任意整理後も継続）"
    gambling_history: "34年、年300日超、仕事後も閉店まで"
    visit_motive: "返済不能の焦りを麻痺させる／取り返し"
    psychiatric_comorbidity: "強い抑うつ的消耗"
  trigger: {event: "借入先が尽きても閉店まで打ち切ろうとする局面", machine_type: "パチスロ", time_of_day: "仕事終わり〜閉店"}
  inner_monologue_ja: "今日やめても返済は消えない。なら、当たるまで座っていたほうがまだマシだ。"
  emotional_state: {arousal_0_100: 84, despair_0_100: 97, dominant_emotion: "切迫 × 麻痺"}
  action: "借金不能が見えても翌日の軍資金を探す"
  post_play_state: "親への資金依頼、家族断裂の進行"
  source: {type: "公的当事者手記", url_or_ref: "NCASA document81 No.1", confidence: "高"}
  notes: "interruptibility 0.02 / dissociation_tendency 0.78。『死にたい』が感情表出であると同時に資金調達言語にもなっており、despair が高くても停止行動に結びついていない。"。 citeturn26view0

- id: R3-A-002
  category: 依存症末期
  profile:
    age_range: "40代"
    occupation: "会社員"
    family: "不詳"
    debt_yen: 6000000
    addiction_severity: "末期手前〜末期"
    gambling_history: "学生期開始、平日毎日閉店まで・土日も開店から閉店まで"
    visit_motive: "仕事ストレス遮断／自己破壊的な続行"
    psychiatric_comorbidity: "うつ病"
  trigger: {event: "平日夜、負債と抑うつを抱えたまま閉店まで回し続ける瞬間", machine_type: "パチンコ・パチスロ", time_of_day: "平日夜"}
  inner_monologue_ja: "帰っても眠れない。ここで座っている間だけ、地獄に名前が付かない。"
  emotional_state: {arousal_0_100: 88, despair_0_100: 95, dominant_emotion: "希死念慮を伴う切迫"}
  action: "自死・犯罪を考えながらも席を立てない"
  post_play_state: "借金と抑うつが翌日にそのまま持ち越される"
  source: {type: "公的当事者手記", url_or_ref: "NCASA document65 No.4", confidence: "高"}
  notes: "interruptibility 0.03 / dissociation_tendency 0.74。A群で最も典型的な『despair 90+ でも arousal が落ちない』型。"。 citeturn24view0

- id: R3-A-003
  category: 依存症末期
  profile:
    age_range: "40代"
    occupation: "会社員"
    family: "妻子あり"
    debt_yen: 10800000
    addiction_severity: "末期（15社借入、3回破綻）"
    gambling_history: "20代からパチスロ、長期反復"
    visit_motive: "督促と自己嫌悪を一時停止する／取り返し"
    psychiatric_comorbidity: "不詳"
  trigger: {event: "督促と返済不能が頭に浮かんでも追い銭を続ける局面", machine_type: "パチスロ", time_of_day: "不詳"}
  inner_monologue_ja: "ここでやめたら借金だけが本物になる。もう少しだけ伸びろ。"
  emotional_state: {arousal_0_100: 82, despair_0_100: 96, dominant_emotion: "破綻認識 × 続行強迫"}
  action: "多重債務化してもプレイ反復"
  post_play_state: "家族危機、返済不能、破綻の反復"
  source: {type: "自己記述系漫画・周辺紹介", url_or_ref: "借金1080万・40代サラリーマン妻子あり", confidence: "中"}
  notes: "interruptibility 0.05 / dissociation_tendency 0.76。ホール内モノローグの再構成幅はやや大きいが、極端債務の上限値サンプルとして有用。"。 citeturn15search1turn15search6

- id: R3-A-004
  category: 依存症末期
  profile:
    age_range: "20代後半"
    occupation: "不安定就労"
    family: "単身、住居不安定"
    debt_yen: 6000000
    addiction_severity: "末期（支払予算を軍資金化）"
    gambling_history: "若年期から反復"
    visit_motive: "支払い穴埋めの一発化"
    psychiatric_comorbidity: "不詳"
  trigger: {event: "家賃とガス代の支払予算を、そのままスロットの軍資金に回す決断", machine_type: "スロット", time_of_day: "支払期限直前"}
  inner_monologue_ja: "払って終わるくらいなら、賭けたほうがまだ逆転の目がある。"
  emotional_state: {arousal_0_100: 79, despair_0_100: 92, dominant_emotion: "追い詰められた賭け"}
  action: "生活維持費の一部だけ払い、残りを勝負金に変える"
  post_play_state: "負ければ即タイミー・即地獄という自己追い込み"
  source: {type: "当事者ブログ", url_or_ref: "元ホームレススロッターの備忘録", confidence: "中"}
  notes: "interruptibility 0.08 / dissociation_tendency 0.70。A群のなかでも『現実の支払い』を『プレイ燃料』へ変換する危険な反転例。"。 citeturn50view2

- id: R3-A-005
  category: 依存症末期
  profile:
    age_range: "30代後半〜40代前半"
    occupation: "会社員"
    family: "独身期の記述"
    debt_yen: null
    addiction_severity: "末期手前（生活費破壊→借入）"
    gambling_history: "給料と生活費を恒常的に流用"
    visit_motive: "生活費を増やすはずが、借入後も再プレイ衝動へ転化"
    psychiatric_comorbidity: "不詳"
  trigger: {event: "無人契約機で現金を受け取った直後、『生活費補填』ではなく『まだ打てる』へ傾く瞬間", machine_type: "パチンコ", time_of_day: "資金枯渇後"}
  inner_monologue_ja: "これで戻せる。いや、もしかしたら、ここから増やせる。"
  emotional_state: {arousal_0_100: 76, despair_0_100: 90, dominant_emotion: "安堵と背徳の同時到来"}
  action: "借入金を生活再建より再プレイ可能性として知覚する"
  post_play_state: "借入→再借入の雪だるま化"
  source: {type: "当事者 note", url_or_ref: "生活費に手をつけた日", confidence: "中"}
  notes: "interruptibility 0.10 / dissociation_tendency 0.68。A群で必要な『残金0→借入決断』カードとして有効。ホール内そのものではないが、R3定義上の重要遷移点。"。 citeturn50view0

## 不労所得補強カード

B 群は、本人手記が公開範囲でかなり薄かったため、**店員観察・常連観察・本人の低覚醒自記**を混ぜた。よって `confidence` は A/C より一段低い。

- id: R3-B-001
  category: "不労所得・富裕層補強"
  profile:
    age_range: "40代後半〜60代"
    occupation: "会社経営者・役員"
    family: "不詳"
    monthly_income_yen: null
    addiction_severity: "低〜中（観察ベース）"
    gambling_history: "ホール常連"
    visit_motive: "暇つぶし・会話・遊技そのもの"
    psychiatric_comorbidity: "不詳"
  trigger: {event: "負けが込んでも『遊べたらいい』で終える局面", machine_type: "パチスロ", time_of_day: "不詳"}
  inner_monologue_ja: "勝てんでも、遊べたらええしな。"
  emotional_state: {arousal_0_100: 16, despair_0_100: 8, dominant_emotion: "低刺激の余裕"}
  action: "勝敗より会話や滞在経験を優先する"
  post_play_state: "大きな自己嫌悪を残さず離席"
  source: {type: "常連観察＋会話", url_or_ref: "社長・お金持ち常連との会話記録", confidence: "中"}
  notes: "arousal_range [8,22] / despair_range [0,12] / interruptibility 0.94。B群の基準カード。"。 citeturn28view0

- id: R3-B-002
  category: "不労所得・富裕層補強"
  profile:
    age_range: "40代後半〜70代"
    occupation: "自営業の社長・株主"
    family: "不詳"
    monthly_income_yen: null
    addiction_severity: "低〜中（観察ベース）"
    gambling_history: "20年級の常連"
    visit_motive: "店との長期関係を楽しむ／押し引き"
    psychiatric_comorbidity: "不詳"
  trigger: {event: "『今日は甘くない』と見切って深追いしない局面", machine_type: "パチスロ・4円パチンコ", time_of_day: "平日中心"}
  inner_monologue_ja: "今日はここまででええ。無理に取りにいかんでも、また来ればいい。"
  emotional_state: {arousal_0_100: 22, despair_0_100: 10, dominant_emotion: "淡々とした観察"}
  action: "店の利益日・還元日を見ながら無理打ちを避ける"
  post_play_state: "継続来店前提で軽く引く"
  source: {type: "観察 note", url_or_ref: "地域富裕層常連の特徴", confidence: "中"}
  notes: "interruptibility 0.88 / time_cost_efficiency 0.74。A群の『止まれなさ』と真逆で、資金圧ではなく長期関係と暇の埋め方が主軸。"。 citeturn30view0

- id: R3-B-003
  category: "不労所得・富裕層補強"
  profile:
    age_range: "50代〜70代"
    occupation: "自営業・店経営者の常連"
    family: "不詳"
    monthly_income_yen: null
    addiction_severity: "低（観察ベース）"
    gambling_history: "店員と顔なじみの長期常連"
    visit_motive: "遊技＋接客関係の維持"
    psychiatric_comorbidity: "不詳"
  trigger: {event: "勝敗よりも、店員とのやり取りや差し入れで滞在感が満たされる場面", machine_type: "パチンコ・スロット不問", time_of_day: "日中"}
  inner_monologue_ja: "今日はコーヒー渡して、少し遊んで、頃合いで帰ればいい。"
  emotional_state: {arousal_0_100: 18, despair_0_100: 6, dominant_emotion: "社交的な低反応"}
  action: "店員に差し入れし、常連関係を確認しながら遊ぶ"
  post_play_state: "負けても関係性コストが主で、感情コストは小さい"
  source: {type: "店員観察ブログ", url_or_ref: "仲良くなると得する常連客", confidence: "中"}
  notes: "interruptibility 0.90 / stigma_barrier 0.12。『VIP感の確認』がプレイ自体より価値を持つB群カード。"。 citeturn28view1

- id: R3-B-004
  category: "不労所得・富裕層補強"
  profile:
    age_range: "40歳前後"
    occupation: "地主家系の息子"
    family: "地主家系"
    monthly_income_yen: null
    addiction_severity: "不詳"
    gambling_history: "毎日級の常連と観察される"
    visit_motive: "時間消費・習慣"
    psychiatric_comorbidity: "不詳"
  trigger: {event: "大当たり・ヘソ落ち・損失局面でも表情が動かない瞬間", machine_type: "ガロ系パチンコ", time_of_day: "日常的"}
  inner_monologue_ja: "数万なら揺れない。続けるか、移るか、その程度だ。"
  emotional_state: {arousal_0_100: 12, despair_0_100: 5, dominant_emotion: "無反応に近い平滑"}
  action: "眉ひとつ動かさず座り続ける"
  post_play_state: "金銭損失が感情波形に変換されにくい"
  source: {type: "掲示板観察ログ", url_or_ref: "大地主の息子らしい常連の描写", confidence: "低〜中"}
  notes: "arousal_range [5,18] / interruptibility 0.97。B群の極端な低反応サンプルとして有用。"。 citeturn28view2

- id: R3-B-005
  category: "不労所得・富裕層補強"
  profile:
    age_range: "40代"
    occupation: "FIRE後の個人投資家・元事業主"
    family: "独身"
    monthly_income_yen: null
    addiction_severity: "低"
    gambling_history: "20年以上前に一時ハマった経験あり"
    visit_motive: "企業理解・見学"
    psychiatric_comorbidity: "既往の不調記述あり"
  trigger: {event: "台の前まで行っても『理解不能』『カモになる』と判断し、そのまま帰る瞬間", machine_type: "entity[\"company\",\"SANKYO\",\"jp gaming company\"]機種（ヴァルヴレイヴ2）", time_of_day: "日中"}
  inner_monologue_ja: "打てなくはない。でも、知らないまま座るほどの理由がない。今日は見るだけでいい。"
  emotional_state: {arousal_0_100: 20, despair_0_100: 10, dominant_emotion: "分析的な距離感"}
  action: "ホールに入るが、打たずに撤収する"
  post_play_state: "後悔よりも検討材料の持ち帰り"
  source: {type: "FIRE当事者 note", url_or_ref: "株主としてホール見学のみ", confidence: "中"}
  notes: "interruptibility 0.99 / time_cost_efficiency 0.91。B群の『いつでも帰れる』をもっとも素直に表すカード。"。 citeturn31view0

## 中年現役男性カード

- id: R3-C-001
  category: "中年現役男性"
  profile:
    age_range: "40代"
    occupation: "サラリーマン"
    family: "妻子あり"
    debt_yen: 3000000
    addiction_severity: "中〜高"
    gambling_history: "仕事帰りの定着化、ギャンブル二刀流"
    visit_motive: "帰宅前の緩衝帯／疲労遮断"
    psychiatric_comorbidity: "不詳"
  trigger: {event: "仕事帰りにホールへ寄り、台を打ちながら別ギャンブルも回してしまう局面", machine_type: "パチンコ", time_of_day: "仕事終わり"}
  inner_monologue_ja: "家に帰る前に、頭をいったん空にしたい。ここなら時間も埋まるし、まだ勝負もできる。"
  emotional_state: {arousal_0_100: 70, despair_0_100: 62, dominant_emotion: "疲労麻酔 × 逃避"}
  action: "パチンコを打ちながら競輪まで並行する"
  post_play_state: "半年で負債300万、家族時間の空洞化"
  source: {type: "当事者ブログ", url_or_ref: "40代サラリーマン・妻子あり・負債300万", confidence: "中"}
  notes: "interruptibility 0.25 / payday_sensitivity 0.43。C群に多い『帰宅前にワンクッション置く』型。"。 citeturn14search10turn20view0

- id: R3-C-002
  category: "中年現役男性"
  profile:
    age_range: "40代"
    occupation: "サラリーマン"
    family: "不詳"
    debt_yen: null
    addiction_severity: "高"
    gambling_history: "長期、依存からの離脱過程"
    visit_motive: "仕事・生活ストレスの爆発先"
    psychiatric_comorbidity: "うつ誘発的な消耗の自己言及あり"
  trigger: {event: "319分の1をやっと引いたのに50%確変を何度も外し、総投資12万円に達した瞬間", machine_type: "パチンコ", time_of_day: "不詳"}
  inner_monologue_ja: "ここでやめたら12万がただ消えるだけだ。次こそ入る、次こそ。"
  emotional_state: {arousal_0_100: 86, despair_0_100: 74, dominant_emotion: "怒り × 追い込み"}
  action: "遠隔・顔認証といった認知へ寄り、さらに感情を煽る"
  post_play_state: "疲弊と業界憎悪だけが残る"
  source: {type: "当事者ブログ", url_or_ref: "中年サラリーマン・依存脱出ブログ", confidence: "中"}
  notes: "interruptibility 0.12 / sensory_gating_factor 0.86。C群では arousal が高く、怒りで離席がむしろ遅れるタイプ。"。 citeturn22view0

- id: R3-C-003
  category: "中年現役男性"
  profile:
    age_range: "50代"
    occupation: "会社員"
    family: "妻・子あり"
    debt_yen: null
    addiction_severity: "高"
    gambling_history: "学生期開始、結婚後も隠匿・再燃"
    visit_motive: "職場の誘いからの再燃／取り返し"
    psychiatric_comorbidity: "不詳"
  trigger: {event: "『もう二度とやらない』後、職場でパチンコに誘われ再入店する瞬間", machine_type: "パチンコ", time_of_day: "仕事絡み"}
  inner_monologue_ja: "一回だけなら戻らない。前みたいにはならない。"
  emotional_state: {arousal_0_100: 72, despair_0_100: 68, dominant_emotion: "自己正当化 × 予兆不安"}
  action: "再入店を軽く扱い、そのまま再債務化"
  post_play_state: "妻子への再告白、離婚手続きへ"
  source: {type: "公的当事者手記", url_or_ref: "NCASA document81 No.3", confidence: "高"}
  notes: "payday_sensitivity 0.54 / interruptibility 0.20。C群に典型的な『仕事ネットワーク起点の再燃』カード。"。 citeturn27view0

- id: R3-C-004
  category: "中年現役男性"
  profile:
    age_range: "40歳"
    occupation: "会社員"
    family: "2児の父"
    debt_yen: null
    addiction_severity: "低〜中"
    gambling_history: "隙間時間稼働で年間プラス志向"
    visit_motive: "副収入補強／期待値取得"
    psychiatric_comorbidity: "不詳"
  trigger: {event: "送迎や本業の隙間に、期待値だけ拾って帰る判断", machine_type: "パチンコ・パチスロ", time_of_day: "隙間時間"}
  inner_monologue_ja: "今日は取れる台だけ。子どもの迎えまでに終わる分しか触らない。"
  emotional_state: {arousal_0_100: 44, despair_0_100: 18, dominant_emotion: "実務的な集中"}
  action: "時間制約を先に決め、台選びを絞る"
  post_play_state: "副収入化の感覚で帰宅"
  source: {type: "当事者プロフィール note", url_or_ref: "40歳会社員・2児の父・年間+300万", confidence: "中"}
  notes: "time_cost_efficiency 0.86 / interruptibility 0.72。C群の比較ベースラインとして有用。"。 citeturn14search5

- id: R3-C-005
  category: "中年現役男性"
  profile:
    age_range: "40代"
    occupation: "年収250〜300万台のサラリーマン"
    family: "妻子あり"
    debt_yen: null
    addiction_severity: "中"
    gambling_history: "家計補助ではなく小遣い・玩具代狙い"
    visit_motive: "小遣い稼ぎ／自分の居場所"
    psychiatric_comorbidity: "不詳"
  trigger: {event: "低賃金への補償として、限られた日時でスロットに向かう瞬間", machine_type: "スロット", time_of_day: "空き時間"}
  inner_monologue_ja: "これで子どもの玩具と自分の小遣いを少しだけ作れればいい。"
  emotional_state: {arousal_0_100: 55, despair_0_100: 45, dominant_emotion: "不足感 × 期待"}
  action: "家計の主戦力ではないが、心理的には補填役として座る"
  post_play_state: "勝敗が家の空気より自尊心に響く"
  source: {type: "当事者プロフィール blog", url_or_ref: "安月給子持ちスロッター", confidence: "中"}
  notes: "payday_sensitivity 0.62 / stigma_barrier 0.39。C群の『中産ではないが現役・既婚・父』サンプル。"。 citeturn14search7

- id: R3-C-006
  category: "中年現役男性"
  profile:
    age_range: "40代"
    occupation: "サラリーマン"
    family: "不詳"
    debt_yen: null
    addiction_severity: "中"
    gambling_history: "夕方からの短時間稼働"
    visit_motive: "仕事帰りのストレス発散"
    psychiatric_comorbidity: "不詳"
  trigger: {event: "仕事終わり30分だけのつもりが、1〜2万円を飛ばしてしまう夕方", machine_type: "パチンコ・パチスロ", time_of_day: "18時以降"}
  inner_monologue_ja: "30分だけなら大丈夫。今日は当たりだけ見て帰る。"
  emotional_state: {arousal_0_100: 64, despair_0_100: 52, dominant_emotion: "自己説得 × 焦り"}
  action: "短時間だからこそ押し引きが雑になり、ずるずる延びる"
  post_play_state: "短時間のはずが『何も残らない負け』として残る"
  source: {type: "当事者系 note", url_or_ref: "夕方から打つサラリーマン像", confidence: "中"}
  notes: "time_cost_efficiency 0.34 / interruptibility 0.38。C群の『短時間だから安全』という自己欺瞞カード。"。 citeturn14search9

- id: R3-C-007
  category: "中年現役男性"
  profile:
    age_range: "40代前後"
    occupation: "残業のある会社員"
    family: "不詳"
    debt_yen: null
    addiction_severity: "中"
    gambling_history: "仕事終わりの反復"
    visit_motive: "認知疲労の麻酔／『3000円だけ』"
    psychiatric_comorbidity: "不詳"
  trigger: {event: "残業終わり、ネオンを見て『3000円だけ』と入店する瞬間", machine_type: "パチスロ", time_of_day: "残業後"}
  inner_monologue_ja: "頭が死んでる日こそ、ペカらせて帰れば整う。"
  emotional_state: {arousal_0_100: 60, despair_0_100: 49, dominant_emotion: "疲労性の衝動"}
  action: "判断力が落ちたままゾーン狙いがダラ打ちに変わる"
  post_play_state: "場合によってはATMまで走る"
  source: {type: "啓発寄り note の自傷的シナリオ描写", url_or_ref: "仕事帰りのパチンコは募金", confidence: "低〜中"}
  notes: "interruptibility 0.34 / payday_sensitivity 0.58。一次資料としては弱いが、『会社帰り疲労→押し引き崩壊』の描写はC群の挙動仮説と一致。"。 citeturn13search4

- id: R3-C-008
  category: "中年現役男性"
  profile:
    age_range: "51歳"
    occupation: "サラリーマン"
    family: "独身"
    debt_yen: null
    addiction_severity: "高（累計損失2000万超）"
    gambling_history: "17年、4号機〜5号機、退職金・失業保険も投入"
    visit_motive: "仕事帰りの高揚／習慣化した報酬"
    psychiatric_comorbidity: "不詳"
  trigger: {event: "夜勤明けで朝一から15時まで打ち、そのまま仮眠して再出勤する局面", machine_type: "パチスロ", time_of_day: "朝一〜午後"}
  inner_monologue_ja: "寝る前に一勝ちだけ。今の疲れならむしろ何も考えず打てる。"
  emotional_state: {arousal_0_100: 71, despair_0_100: 57, dominant_emotion: "消耗した高揚"}
  action: "勤務サイクルそのものをホール中心に組み替える"
  post_play_state: "退職金・失業保険・日雇いへと生活が後退"
  source: {type: "当事者 note", url_or_ref: "51歳サラリーマン・元依存症記", confidence: "中"}
  notes: "interruptibility 0.28 / payday_sensitivity 0.51。C群のなかでも『労働シフトとプレイ時間が一体化』した強い例。"。 citeturn23view0

## 精神疾患併発カード

D 群は、**診断名をカテゴリレベルに丸めた上で、状態変化をパラメータ化する**ことを目的に使うのが妥当である。診断の厳密性より、R3 では **プレイ中の mood_lability / impulse_control / dissociation / sensory reactivity** を拾うことを優先した。

- id: R3-D-001
  category: "精神疾患併発"
  profile:
    age_range: "20代後半〜30代前半"
    occupation: "過重労働の会社員"
    family: "彼女との関係喪失"
    debt_yen: null
    addiction_severity: "高"
    gambling_history: "仕事の合間・早帰り日に単独通い"
    visit_motive: "注意資源の固定／仕事忘却"
    psychiatric_comorbidity: "ADHD"
  trigger: {event: "玉の流れを見ているときだけ頭が静かになり、記憶も曖昧になるプレイ", machine_type: "パチンコ", time_of_day: "仕事の合間・休日夕方"}
  inner_monologue_ja: "玉だけ見ていればいい。この時間だけ、頭の中が散らからない。"
  emotional_state: {arousal_0_100: 73, despair_0_100: 67, dominant_emotion: "鎮静を求める没入"}
  action: "生活費以外をほぼ投入、行けない日は競馬・競輪へスライド"
  post_play_state: "記憶の抜け、遅刻、仕事崩壊"
  source: {type: "当事者 note", url_or_ref: "ADHD診断後の振り返り", confidence: "中"}
  notes: "mood_lability 0.71 / impulse_control 0.24 / sensory_gating_factor 0.52。『刺激追求』だけでなく『刺激でしか静まらない注意系』として実装価値が高い。"。 citeturn36view0

- id: R3-D-002
  category: "精神疾患併発"
  profile:
    age_range: "40代半ば"
    occupation: "就労継続中"
    family: "妹・母に金銭管理を依頼"
    debt_yen: 370000
    addiction_severity: "中〜高"
    gambling_history: "43歳頃から時間さえあれば通う"
    visit_motive: "落ち着かなさの解消／躁偏位時の行動化"
    psychiatric_comorbidity: "双極性障害"
  trigger: {event: "開店時間の10時になるまで落ち着かず、一万円札を見るだけで身体が前のめりになる朝", machine_type: "パチンコ", time_of_day: "開店前〜開店直後"}
  inner_monologue_ja: "10時になれば行ける。打てば落ち着く。今のそわそわを止めたい。"
  emotional_state: {arousal_0_100: 78, despair_0_100: 70, dominant_emotion: "焦燥 × 衝動"}
  action: "生活費を流用し、足りないと借入へ直結"
  post_play_state: "妹へ打ち明け、現金管理を全面移管"
  source: {type: "当事者ブログ", url_or_ref: "双極性障害とパチンコ依存症", confidence: "中"}
  notes: "mood_lability 0.89 / impulse_control 0.22。D群のなかでも『開始前ソワソワ』が強く、プレイ開始が鎮静化行動になっている。"。 citeturn46view1

- id: R3-D-003
  category: "精神疾患併発"
  profile:
    age_range: "20代"
    occupation: "建築現場労働者"
    family: "家族・友人・仕事仲間へ嘘が常態化"
    debt_yen: null
    addiction_severity: "高"
    gambling_history: "給料が財布に着地する前にホールへ直行"
    visit_motive: "躁っぽい加速と強い機械刺激"
    psychiatric_comorbidity: "双極性障害（本人は関連を示唆）"
  trigger: {event: "給料日、現金を持った瞬間にそのままパチ屋へ直行する", machine_type: "パチンコ・パチスロ", time_of_day: "給料日"}
  inner_monologue_ja: "今すぐ行ける。今日の一発で全部ひっくり返る。"
  emotional_state: {arousal_0_100: 81, despair_0_100: 58, dominant_emotion: "全能感混じりの衝動"}
  action: "壁を蹴るほどの感情爆発、しかし翌日にはまた座る"
  post_play_state: "家賃遅延、ライフライン停止、生活秩序の崩壊"
  source: {type: "当事者ブログ", url_or_ref: "双極性障害とギャンブル依存症", confidence: "中"}
  notes: "mood_lability 0.78 / impulse_control 0.30。C群の給料日高揚より、D群ではブレーキ系がさらに弱い。"。 citeturn46view0

- id: R3-D-004
  category: "精神疾患併発"
  profile:
    age_range: "20代後半〜30代"
    occupation: "会社員〜退職期"
    family: "妻子あり"
    debt_yen: 12000000
    addiction_severity: "高"
    gambling_history: "うつ期に『打ちたいものを打つ』へ変質"
    visit_motive: "誰からも否定されない空間への逃避"
    psychiatric_comorbidity: "PTSD + うつ"
  trigger: {event: "不安になるとパチ屋へ逃げ込み、最大音量でもうずくまりながら打ち続ける局面", machine_type: "パチスロ", time_of_day: "不安増大時"}
  inner_monologue_ja: "ここなら誰も干渉しない。痛くても、うるさくても、ここから出るよりはマシだ。"
  emotional_state: {arousal_0_100: 69, despair_0_100: 89, dominant_emotion: "解離的逃避 × 自己否定"}
  action: "現金が尽きるまで換金ギャップを自分から払い続け、足りなければキャッシング"
  post_play_state: "1日20万負けでも感情が動かず、あとから自己嫌悪だけが来る"
  source: {type: "当事者 note", url_or_ref: "PTSD持ち・うつ・借金1200万の記録", confidence: "中"}
  notes: "mood_lability 0.76 / impulse_control 0.21 / dissociation_tendency 0.80 / sensory_gating_factor 0.25。D群で最も実装価値が高い『苦痛刺激が停止信号にならない』例。"。 citeturn47view0

- id: R3-D-005
  category: "精神疾患併発"
  profile:
    age_range: "30代"
    occupation: "就労中"
    family: "不詳"
    debt_yen: null
    addiction_severity: "中〜高"
    gambling_history: "借金をして打つ時期あり"
    visit_motive: "惰性で座り続ける／終日プレイ後の頭の霧"
    psychiatric_comorbidity: "うつ病"
  trigger: {event: "ほぼ1日打ったあと、負けすぎて放心し、頭がぼーっとしたまま台の怖さを反芻する夜", machine_type: "スマスロ", time_of_day: "終日稼働後の夜"}
  inner_monologue_ja: "もうやめたほうがいい。でも明日になればまた、座れば何か変わる気がする。"
  emotional_state: {arousal_0_100: 46, despair_0_100: 72, dominant_emotion: "鈍麻 × 反芻"}
  action: "大負けしたのに『切り替える』と書いて離脱を先送りする"
  post_play_state: "放心、誤字だらけ、頭の霞み"
  source: {type: "当事者ブログ", url_or_ref: "30代うつ病パチンカスの日記", confidence: "中"}
  notes: "mood_lability 0.55 / impulse_control 0.32 / dissociation_tendency 0.58。D群の抑うつ相は arousal が低めでも interruptibility が高くならない。"。 citeturn35view1turn48search0

- id: R3-D-006
  category: "精神疾患併発"
  profile:
    age_range: "30代前半"
    occupation: "元会社員・現在フリーランス"
    family: "母から金銭支援あり"
    debt_yen: null
    addiction_severity: "中〜高"
    gambling_history: "2回目の大当たり確変を境に単独通いが定着"
    visit_motive: "快感の再演／精神的不調による生活中心化"
    psychiatric_comorbidity: "精神疾患（詳細非開示）"
  trigger: {event: "2回目の確変快感を再現しようとして一人でホールへ向かう瞬間", machine_type: "パチンコ", time_of_day: "不詳"}
  inner_monologue_ja: "もう一回あの感覚が来れば、今日は何とかなる。"
  emotional_state: {arousal_0_100: 64, despair_0_100: 61, dominant_emotion: "快感追跡 × 生活比重の逆転"}
  action: "手を出してはいけない金に手を出し、収入が切れても母に借りて通う"
  post_play_state: "会社退職、家計の重心がパチンコへ移る"
  source: {type: "当事者 note", url_or_ref: "精神疾患×ギャンブル依存", confidence: "中"}
  notes: "mood_lability 0.67 / impulse_control 0.40。病名が明示されないため診断的な使い方は不可だが、『精神的不調→ホールが生活中心』の遷移例としては有効。"。 citeturn35view2

## メタ観察

### 末期群は高絶望でも高覚醒のまま止まらない

A 群で最も目立ったのは、**despair が 90 台でも arousal が落ち切らない**ことだった。A-001 は借金1500万円・年300日超の通いでも閉店まで打ち切る形を崩さず、A-002 はうつ病と自死・犯罪思考を抱えながら平日毎日閉店まで打っていた。日本の臨床サンプルでも、負債保有が 95%、法的債務整理が 3割超で、罹病期間と負債額が相関した。R3 の極端値としては、**interruptibility = 0 に最も近い群**である。 citeturn26view0turn24view0turn38search0

### 富裕層群は低反応と高中断性の対極にある

B 群は、A 群とほぼ対称に、**低 arousal・低 despair・高 interruptibility**で並んだ。B-001 の「勝てんくても遊べたらええしな」、B-004 の「数万が動いても眉ひとつ動かない」、B-005 の「見て帰る」だけでも、金銭圧の薄いプレイヤーは**離席判断そのものが容易**であることが見える。非障害疑い群では、金額・時間の制限を設定・遵守する頻度が高いという調査とも整合的で、B 群は baseline 比較群として有益だ。 citeturn28view0turn28view2turn31view0turn38search1

### 中年現役男性は快楽追跡より帰宅前バッファとしてホールを使う

C 群の中心動機は、単純な「勝ちたい」よりも、**仕事終わりの麻酔・帰宅前の緩衝・不足分の補填感覚**だった。C-001 は家に帰る前の時間埋めとしてホールへ寄り、C-006 と C-007 は「30分だけ」「3000円だけ」の自己説得で入店し、C-008 は夜勤明けから朝一へ流れ込んで勤務サイクルとプレイ時間が一体化していた。R1 原票がこのスレッドでは参照できないため女性群との厳密比較は保留だが、C 群の手触りは**対人感情の前景化より、労働疲労の無音化**に近い。 `payday_sensitivity` は C-005〜C-007 で特に高く置ける。 citeturn14search10turn20view0turn14search9turn13search4turn23view0

### 併発疾患は trait ではなく state modifier として使うのが安全

D 群の実装上もっとも重要なのは、精神疾患併発を**固定人格ではなく状態修飾子**として扱うことだ。D-001 の ADHD では、機械刺激が「興奮」だけでなく**注意の固定化と静まり**をもたらし、`impulse_control` を大きく下げる。D-002 と D-003 の双極性障害では、給料日・開店時刻・現金視認がそのまま行動化に接続し、`mood_lability` が高い。D-004 の PTSD + うつでは、ホールは「誰にも否定されない空間」として機能する一方、最大音量は明確な苦痛刺激にもなる。それでも停止しないので、`sensory_gating_factor` は低く、`dissociation_tendency` は高く置くのが妥当だ。なお診断学上は、**主に躁状態で現れるギャンブル問題は別扱い**になるため、D 群は診断ラベルではなく挙動係数として使うのが安全である。 citeturn36view0turn46view1turn46view0turn47view0turn38search8turn10search11

### 視覚音響は依存を深めるが、PTSD では苦痛刺激にも反転しうる

パチンコ・パチスロでは、機械や台を**見たり聞いたりするだけで**欲求が強まるキュー反応が知られている。さらに、あと一歩で当たるように見える場面や音・光の演出は報酬系を活性化させやすい。D-001 の「玉が流れる姿で落ち着く」、D-004 の「音量最大でうずくまりながらも打つ」、B-005 の「久々に入ったら音と光がしんどい」は、同じ刺激が**鎮静・興奮・苦痛**のいずれにもなりうることを示している。シミュレーションでは `sensory_gating_factor` を単なる「刺激に強い弱い」ではなく、**快刺激/苦痛刺激の両義性を持つ変数**にすると表現力が上がる。 citeturn8search11turn43search1turn36view0turn47view0turn32search6

### 極限値の根拠として強いカード

`despair 95+ / interruptibility ≈ 0` の根拠としては **A-001** と **A-002** が最も強い。`arousal 15 前後 / interruptibility 0.9+` の基準には **B-004** と **B-005** が向く。`mood_lability` の上限寄りには **D-002**、`impulse_control` の下限寄りには **D-001**、`dissociation_tendency` と `sensory pain yet continuation` の同居には **D-004** が強い。C 群の典型的な `payday_sensitivity` は **C-005〜C-007** に置くと、R3 が目指す両極の補完としてバランスがよい。 citeturn26view0turn24view0turn28view2turn31view0turn46view1turn36view0turn47view0turn14search7turn14search9turn13search4

## ソース評価と限界

もっとも堅いのは、**本人記述が明示された公的回収資料**である。今回だと NCASA の手記群と、厚労省系の体験記が核になった。これらは疫学的厳密さよりも支援文脈の語りに寄っているが、R3 の目的が「設計用の質的素材ライブラリ」である以上、**瞬間の感情・言い訳・続行ロジック**を拾うには非常に相性がよい。加えて、臨床論文と国の研究班資料は、カードごとの数値推定が暴走しないためのガードレールとして有効だった。 citeturn24view0turn26view0turn33view0turn38search0turn38search9

中位の信頼度は、本人が長文で記した note / Ameba / Hatena の自記録群である。これらは年齢・職業・家族構造・負債額が一部ぼかされる一方、**「玉の流れを見ると落ち着く」「給料が財布に着地する前に直行」「夜勤明けに朝一から打つ」**のような、学術論文では取りこぼされやすいホール内微表情が濃い。R3 のカード化にはこの層が不可欠だった。 citeturn36view0turn46view0turn47view0turn23view0turn20view0

最も慎重に扱うべきは、B 群で使った店員観察・掲示板ログ・観察 note である。これは**分布推定には使えない**が、富裕層の本人手記が少ない現状では、`低反応 / 高 interruptibility / 店舗関係性重視` という B 群の設計仮説を置く補助線にはなる。とくに B-004 のような「地主の息子で眉ひとつ動かない」型は、事実性よりも**極端な対極サンプル**として使うのが適切である。補助的に、entity["organization","国立病院機構久里浜医療センター","kanagawa, japan"] や entity["organization","大石クリニック","yokohama, kanagawa, japan"] の公開説明、発達障害とギャンブルの相談実例資料も参照したが、これらは**背景理解の補助**であり、今回の card 本体はなるべく本人のホール内叙述に寄せている。 citeturn28view0turn28view1turn28view2turn30view0turn8search11turn8search4turn42view2turn42view3