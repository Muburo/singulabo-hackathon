"""
inner_voice_v2.py — 機種 × トリガー × カテゴリで多様化した心の声辞書

階層構造:
  INNER_VOICE_BY_MACHINE[機種][trigger or 状態] -> [セリフ candidates]
  CATEGORY_FLAVOR[カテゴリ] -> { prefix, suffix } のオプション
"""
import random


# ============ 機種 × trigger / 状態 別の心の声 ============
INNER_VOICE_BY_MACHINE = {
    "GOD": {
        "kakutei_engi": [
            "枠連きた、凱旋",
            "神 GOD、ありがとう",
            "天井超え、運命変わった",
            "これは枠 GOD",
            "GG 確定、勝った",
        ],
        "tokka_zone_entry": [
            "神 GOD きた",
            "もう止まらない",
            "GG 入った",
            "ロングフリーズ",
            "脳汁ドバドバ",
        ],
        "uwanose": [
            "200 おかわり",
            "もう一撃 5000 枚",
            "GOD 来てる",
            "上乗せ祭り",
            "止まらない",
        ],
        "chain_start": [
            "GOD きた、頼む伸びろ",
            "ボーナスきた",
            "ようやく当たった",
            "GG 引け",
        ],
        "焦燥": ["もう光れ、GOD", "頼む、一回だけ", "凱旋まで頑張れ俺"],
        "熱狂": ["来る、絶対 GOD", "今日は GG 引く"],
        "絶望": ["GOD、もう無理", "GG 引けない"],
        "解離": ["...", "ふっ、また駆け抜け"],
        "凪": ["まあ、GOD はこんなもん"],
        "倦怠": ["GOD 疲れた"],
        "普通": ["GOD どうかな"],
    },
    "北斗": {
        "kakutei_engi": [
            "無想転生確定",
            "天井超え、続く",
            "ケンシロウ来た",
            "百裂拳",
        ],
        "tokka_zone_entry": [
            "世紀末モード",
            "無想転生入った",
            "百裂モード突入",
            "ケンシロウ覚醒",
        ],
        "uwanose": [
            "ART セット追加",
            "100 上乗せ",
            "もう少し続け",
            "天井まで頑張る",
        ],
        "chain_start": [
            "ART 入った、伸びろ",
            "ボーナス引いた、頼む",
        ],
        "焦燥": ["もう一回 ART 来い", "頼む"],
        "熱狂": ["北斗最高", "今日はイケる"],
        "絶望": ["北斗、終わった"],
        "解離": ["...", "ふっ"],
        "凪": ["まあ、こんなもん"],
        "倦怠": ["疲れた"],
        "普通": ["..."],
    },
    "ART": {
        "kakutei_engi": [
            "確定演出！止まらない",
            "もう、一生終わらない",
            "完走確定",
        ],
        "tokka_zone_entry": [
            "特化ゾーンきた",
            "終わらない、これ終わらない",
            "完走見えた",
            "リセットボタン押したくない",
        ],
        "uwanose": [
            "100 上乗せ、まだ続く",
            "終わらない感",
            "あと 50G、いや 200G",
            "拘束時間延長",
        ],
        "chain_start": [
            "ART 入った",
            "ようやく入口",
            "頼む、続け",
        ],
        "焦燥": ["もう一回上乗せ来てくれ", "終わらせないで"],
        "熱狂": ["これは終わらない", "拘束最高"],
        "絶望": ["駆け抜け、無理だ"],
        "解離": ["...", "ふっ、駆け抜け"],
        "凪": ["まあ、ART はこんなもん"],
        "倦怠": ["長い"],
        "普通": ["..."],
    },
    "沖スロ": {
        "kakutei_engi": [],  # 純A は中間イベント無し
        "tokka_zone_entry": [],
        "uwanose": [],
        "chain_start": [
            "BIG きた、ペカった",
            "ようやく光った",
            "単発で十分",
            "ピカった",
        ],
        "焦燥": ["あと一回、あと一回 BIG", "ペカれ"],
        "熱狂": ["連チャンしてる", "神台"],
        "絶望": ["ハマり、もう無理"],
        "解離": ["...", "ふっ、ハマり"],
        "凪": ["沖スロ、まったり"],
        "倦怠": ["眠い"],
        "普通": ["..."],
    },
}


# ============ カテゴリ別フレーバー（接尾） ============
CATEGORY_FLAVOR_SUFFIX = {
    "依存症末期": ["...神様", "...頼む", "...今日こそ", "...マジで"],
    "中年現役":   ["...嫁にバレる", "...月末やばい", ""],
    "主婦":       ["...子供のお迎え", "...夕飯まだ", "...バレたら"],
    "女子大生":   ["...マジ", "...ウケる", "...ヤバ"],
    "不労所得":   ["...まあ遊びだ", "...悪くない"],
    "年金高齢":   ["...残り少ない", "...孫に内緒"],
    "夜職女性":   ["...あげあげ", "...勝つしか"],
    "退職前男性": ["...退職金まで", "...もう後がない"],
}


# ============ 心の声生成 ============
def classify_state(arousal, despair):
    if arousal >= 75 and despair >= 65: return "焦燥"
    if arousal >= 75: return "熱狂"
    if despair >= 70 and arousal < 45: return "解離"
    if despair >= 65: return "絶望"
    if arousal < 35 and despair < 35: return "凪"
    if arousal < 35: return "倦怠"
    return "普通"


def get_inner_voice_v2(arousal, despair, trigger_event, machine_name, category, voice_rng):
    """機種 × トリガー × カテゴリで多様化した心の声を返す"""
    machine_dict = INNER_VOICE_BY_MACHINE.get(machine_name, INNER_VOICE_BY_MACHINE["GOD"])

    # trigger event 優先
    base = None
    if "kakutei" in trigger_event and machine_dict.get("kakutei_engi"):
        base = voice_rng.choice(machine_dict["kakutei_engi"])
    elif "tokka" in trigger_event and machine_dict.get("tokka_zone_entry"):
        base = voice_rng.choice(machine_dict["tokka_zone_entry"])
    elif "uwanose" in trigger_event and machine_dict.get("uwanose"):
        base = voice_rng.choice(machine_dict["uwanose"])
    elif "chain_start" in trigger_event and machine_dict.get("chain_start"):
        base = voice_rng.choice(machine_dict["chain_start"])
    else:
        # 状態ベース
        state = classify_state(arousal, despair)
        candidates = machine_dict.get(state, machine_dict.get("普通", ["..."]))
        if not candidates:
            candidates = ["..."]
        base = voice_rng.choice(candidates)

    # カテゴリ別の接尾フレーバー（30% で付与、長すぎる時は付けない）
    if voice_rng.random() < 0.30 and len(base) < 12:
        suffix_options = CATEGORY_FLAVOR_SUFFIX.get(category, [""])
        suffix = voice_rng.choice(suffix_options)
        if suffix:
            base = base + suffix

    return base
