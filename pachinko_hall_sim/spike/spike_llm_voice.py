"""
spike_llm_voice.py — 本物の LLM（qwen3:4b）で心の声を生成する spike

複数の persona × 機種 × trigger イベントを LLM に投げて、
自然な日本語の心の声が返ってくることを確認する。
ollama サーバー必須（http://localhost:11434）。
"""
import json
import time

import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3:4b-instruct-2507-q4_K_M"


def generate_inner_voice(persona_ctx, voice_history=None):
    """LLM で心の声を生成"""
    voice_history = voice_history or []
    avoid_str = ""
    if voice_history:
        avoid_str = f"\n\n直前に既に言ったセリフ: {' / '.join(voice_history[-3:])}\n→ これらと違う表現で書いてください。"

    prompt = f"""あなたは「{persona_ctx['category']}」のパチスロプレイヤー（{persona_ctx['age']}歳、{persona_ctx['gender']}）。

現在の状況:
- 機種: {persona_ctx['machine']}
- 残金: {persona_ctx['cash']}円
- 連続外れ: {persona_ctx['miss_streak']}回
- 脳汁度（興奮）: {persona_ctx['arousal']:.0f}/100
- 絶望度: {persona_ctx['despair']:.0f}/100
- 追い詰められ度（借金・仕事ストレス等）: {persona_ctx['stress_load']:.2f}/1.0

直前のイベント: {persona_ctx['trigger_event']}{avoid_str}

今、心の中でつぶやいている一言を **20字以内、一人称、句点なし** で書いてください。
人名・地名・固有名詞は禁止。直前のイベントへの自然な反応を意識して。
**心の声のテキストだけ**を出力してください。前置き・説明・引用符なし。"""

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "think": False,
        "keep_alive": -1,
        "options": {
            "num_ctx": 2048,
            "num_predict": 60,
            "temperature": 0.7,
        },
    }

    t0 = time.time()
    response = requests.post(OLLAMA_URL, json=payload, timeout=30)
    elapsed = time.time() - t0
    data = response.json()
    voice = data["message"]["content"].strip()
    # 「」など余計な記号を除去
    voice = voice.strip("「」\"'`")
    return voice, elapsed


# ============ テストケース ============
TEST_CASES = [
    {
        "name": "1. 依存症末期、GOD でボーナス当選",
        "ctx": {
            "category": "依存症末期", "age": 45, "gender": "男性",
            "machine": "GOD（爆裂AT）", "cash": 8000,
            "miss_streak": 0, "arousal": 92, "despair": 30,
            "stress_load": 0.85, "trigger_event": "ボーナス当選"
        }
    },
    {
        "name": "2. 主婦、ART で上乗せ +200G",
        "ctx": {
            "category": "主婦", "age": 38, "gender": "女性",
            "machine": "ART（拘束系）", "cash": 6000,
            "miss_streak": 0, "arousal": 88, "despair": 45,
            "stress_load": 0.40, "trigger_event": "上乗せ +200G"
        }
    },
    {
        "name": "3. 不労所得、北斗で確定演出",
        "ctx": {
            "category": "不労所得・地主", "age": 55, "gender": "男性",
            "machine": "北斗（4.5号機）", "cash": 95000,
            "miss_streak": 0, "arousal": 78, "despair": 20,
            "stress_load": 0.10, "trigger_event": "確定演出"
        }
    },
    {
        "name": "4. 女子大生、沖スロでハマり中",
        "ctx": {
            "category": "女子大生", "age": 21, "gender": "女性",
            "machine": "沖スロ", "cash": 2500,
            "miss_streak": 18, "arousal": 78, "despair": 75,
            "stress_load": 0.30, "trigger_event": "なし（ハマり継続）"
        }
    },
    {
        "name": "5. 中年現役、GOD で残金 0 寸前",
        "ctx": {
            "category": "中年現役男性", "age": 40, "gender": "男性",
            "machine": "GOD（爆裂AT）", "cash": 1000,
            "miss_streak": 22, "arousal": 65, "despair": 88,
            "stress_load": 0.70, "trigger_event": "なし（最終局面）"
        }
    },
    {
        "name": "6. 夜職女性、ART で特化ゾーン突入",
        "ctx": {
            "category": "夜職・風俗系女性", "age": 28, "gender": "女性",
            "machine": "ART（拘束系）", "cash": 35000,
            "miss_streak": 0, "arousal": 95, "despair": 25,
            "stress_load": 0.60, "trigger_event": "特化ゾーン突入"
        }
    },
]


def main():
    print(f"=== ollama 接続確認 ===")
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=5)
        print(f"  ✅ サーバー応答 OK")
        models = [m["name"] for m in r.json().get("models", [])]
        print(f"  利用可能モデル: {len(models)} 個")
        if MODEL in models:
            print(f"  ✅ {MODEL} 利用可能")
        else:
            print(f"  ❌ {MODEL} が見つからない")
            return
    except Exception as e:
        print(f"  ❌ サーバー接続失敗: {e}")
        return

    print(f"\n=== qwen3:4b で心の声を生成 ===\n")
    history = []
    total_time = 0
    for i, tc in enumerate(TEST_CASES, 1):
        print(f"--- {tc['name']} ---")
        ctx = tc["ctx"]
        print(f"  状況: {ctx['category']}, {ctx['machine']}, 残{ctx['cash']:,}円, "
              f"脳汁{ctx['arousal']:.0f}, 絶望{ctx['despair']:.0f}, "
              f"ストレス{ctx['stress_load']:.2f}")
        print(f"  trigger: {ctx['trigger_event']}")
        try:
            voice, elapsed = generate_inner_voice(ctx, voice_history=history)
            history.append(voice)
            total_time += elapsed
            print(f"  💭 「{voice}」  ({elapsed:.1f}秒)")
        except Exception as e:
            print(f"  ❌ エラー: {e}")
        print()

    print(f"=== 完了 ===")
    print(f"  合計: {total_time:.1f}秒, 平均: {total_time/len(TEST_CASES):.1f}秒/call")
    print(f"\n  本番想定 (30 persona × 100 step / 5 step ごと = 600 call):")
    print(f"    予想時間: {total_time/len(TEST_CASES) * 600 / 60:.1f}分")


if __name__ == "__main__":
    main()
