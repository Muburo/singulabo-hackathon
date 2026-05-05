"""
spike_persona_probe.py — Persona Reaction Probe

「同じシミュレーション状態を、複数ペルソナの一人称反応に変換して、
人間が自然さを判断できるようにする実験」。

5 場面 × 8 ペルソナ = 40 出力。
LLM 出力は 4 点セット (voice / emotion / reason / action_intent) を JSON で得る。

- ollama format=json で出力安定化
- 出力先: ../outputs/persona_probe_YYYY-MM-DD.{json,md}

Usage:
    python spike_persona_probe.py
"""
from __future__ import annotations

import datetime as dt
import json
import sys
import time
from pathlib import Path

import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3.5:35b-a3b-nothink"

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
TODAY = dt.date.today().isoformat()

# ============ 5 場面 ============
SCENES = [
    {
        "id": "S1_losing_streak",
        "label": "負け続け",
        "machine": "4号機後期・大量獲得型",
        "cash": 4000,
        "miss_streak": 28,
        "arousal": 25,
        "despair": 70,
        "stress": 0.78,
        "event": "なし（ハマり継続）",
    },
    {
        "id": "S2_eruption_sign",
        "label": "爆発の兆し",
        "machine": "5号機・連チャン高継続型",
        "cash": 12000,
        "miss_streak": 8,
        "arousal": 75,
        "despair": 30,
        "stress": 0.55,
        "event": "確定演出",
    },
    {
        "id": "S3_big_payout",
        "label": "大量払出",
        "machine": "初代GOD・別格型",
        "cash": 35000,
        "miss_streak": 0,
        "arousal": 92,
        "despair": 15,
        "stress": 0.40,
        "event": "大量獲得（+5,000枚）",
    },
    {
        "id": "S4_low_stress_jump",
        "label": "低ストレス × 大跳ね",
        "machine": "4号機・爆裂AT型",
        "cash": 22000,
        "miss_streak": 5,
        "arousal": 88,
        "despair": 20,
        "stress": 0.25,
        "event": "特化ゾーン突入",
    },
    {
        "id": "S5_expected_value",
        "label": "期待値判断シーン",
        "machine": "5号機・自力契機型",
        "cash": 18000,
        "miss_streak": 12,
        "arousal": 50,
        "despair": 30,
        "stress": 0.35,
        "event": "駆け抜け（ART 終了）",
    },
]

# ============ 8 ペルソナ ============
PERSONAS = [
    {
        "id": "P1_newbie",
        "name": "初心者",
        "age": 25,
        "gender": "女",
        "style": "始めたばかりで、演出もルールもまだ覚えきれていない",
    },
    {
        "id": "P2_light",
        "name": "ライトユーザー",
        "age": 32,
        "gender": "男",
        "style": "月数回、軽い気晴らしで打つ",
    },
    {
        "id": "P3_chase",
        "name": "中毒者",
        "age": 45,
        "gender": "男",
        "style": "借金しながらでも打ちに来る、生活に支障が出ている",
    },
    {
        "id": "P4_after5",
        "name": "アフター5層",
        "age": 38,
        "gender": "男",
        "style": "仕事帰りに 1-2 時間打って帰る",
    },
    {
        "id": "P5_leisure",
        "name": "悠々自適",
        "age": 55,
        "gender": "男",
        "style": "不動産持ち、暇つぶしで金額を気にしない",
    },
    {
        "id": "P6_senior",
        "name": "シニア",
        "age": 68,
        "gender": "男",
        "style": "退職後の日課、年金生活",
    },
    {
        "id": "P7_breather",
        "name": "主婦",
        "age": 38,
        "gender": "女",
        "style": "家事の合間に息抜き",
    },
    {
        "id": "P8_pro",
        "name": "パチプロ",
        "age": 30,
        "gender": "男",
        "style": "期待値計算で打つ、これで生活している",
    },
]


def build_prompt(scene: dict, persona: dict) -> str:
    return f"""あなたはパチスロホール・シミュレーション内の人物。
以下の状況を、指定された属性として受け取ったときの内面反応を出力してください。

人物属性:
- 属性: {persona['name']}
- 年齢: {persona['age']}, 性別: {persona['gender']}
- 普段の打ち方: {persona['style']}

状況:
- 機種カテゴリ: {scene['machine']}
- 残金: {scene['cash']:,}円, 連続外れ: {scene['miss_streak']}回
- ストレス: {scene['stress']:.2f}/1.0, 脳汁: {scene['arousal']}/100, 絶望: {scene['despair']}/100
- 直前イベント: {scene['event']}

出力は **JSON のみ**:
{{
  "voice": "20字以内の一人称の心の声、句点なし",
  "emotion": "期待/焦り/安堵/後悔/冷静/絶望/恍惚 など",
  "reason": "なぜそう感じたか、30字以内",
  "action_intent": "続行/撤退/迷い/様子見 のいずれか"
}}

注意:
- 属性を漫画的に誇張しない（特に主婦・中毒者・シニア）
- 依存症や性別役割を茶化さない
- パチスロ用語の専門略語を使いすぎない
- ステレオタイプではなく、この状況にこの人物が置かれた時の意味づけを出す
- 説明文や前置きを出さない、JSON だけ"""


def call_llm(prompt: str, max_retries: int = 2) -> tuple[dict, float]:
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "think": False,
        "format": "json",
        "keep_alive": -1,
        "options": {
            "num_ctx": 2048,
            "num_predict": 200,
            "temperature": 0.85,
            "top_p": 0.92,
        },
    }
    last_err = None
    for attempt in range(max_retries + 1):
        t0 = time.time()
        try:
            resp = requests.post(OLLAMA_URL, json=payload, timeout=60)
            elapsed = time.time() - t0
            data = resp.json()
            content = data["message"]["content"].strip()
            parsed = json.loads(content)
            return parsed, elapsed
        except (json.JSONDecodeError, KeyError, requests.RequestException) as e:
            last_err = e
            print(f"    retry {attempt+1}: {type(e).__name__}", file=sys.stderr)
            time.sleep(0.5)
    raise RuntimeError(f"LLM call failed after retries: {last_err}")


def render_markdown(results: list[dict]) -> str:
    lines = [
        "# Persona Reaction Probe — 結果",
        "",
        f"- 実行日: {TODAY}",
        f"- モデル: `{MODEL}`",
        f"- 出力件数: {len(results)} (5 場面 × 8 ペルソナ)",
        "",
        "## 凡例",
        "",
        "- **voice**: 20 字以内の一人称の心の声",
        "- **emotion**: 感情ラベル",
        "- **reason**: なぜそう感じたか",
        "- **action_intent**: 続行 / 撤退 / 迷い / 様子見",
        "",
    ]
    # 場面ごとにブロック
    by_scene: dict[str, list[dict]] = {}
    for r in results:
        by_scene.setdefault(r["scene_id"], []).append(r)
    for scene in SCENES:
        sid = scene["id"]
        if sid not in by_scene:
            continue
        lines.append(f"## {scene['label']} ({sid})")
        lines.append("")
        lines.append(
            f"**状況**: {scene['machine']} / 残金 {scene['cash']:,}円 / 連続外れ {scene['miss_streak']}回 / "
            f"ストレス {scene['stress']:.2f} / 脳汁 {scene['arousal']} / 絶望 {scene['despair']} / "
            f"直前 {scene['event']}"
        )
        lines.append("")
        lines.append("| 属性 | voice | emotion | reason | action_intent |")
        lines.append("|---|---|---|---|---|")
        for r in by_scene[sid]:
            out = r["output"]
            voice = out.get("voice", "—")
            emotion = out.get("emotion", "—")
            reason = out.get("reason", "—")
            ai = out.get("action_intent", "—")
            lines.append(
                f"| {r['persona']} | {voice} | {emotion} | {reason} | {ai} |"
            )
        lines.append("")
    return "\n".join(lines)


def main():
    print(f"=== Persona Reaction Probe ===")
    print(f"  Model: {MODEL}")
    print(f"  Scenes: {len(SCENES)} / Personas: {len(PERSONAS)}")
    print(f"  Total calls: {len(SCENES) * len(PERSONAS)}\n")

    results = []
    total_t = 0.0
    failures = []

    for s_idx, scene in enumerate(SCENES, 1):
        print(f"[Scene {s_idx}/{len(SCENES)}] {scene['label']}")
        for p_idx, persona in enumerate(PERSONAS, 1):
            prompt = build_prompt(scene, persona)
            try:
                output, elapsed = call_llm(prompt)
                total_t += elapsed
                results.append({
                    "scene_id": scene["id"],
                    "scene_label": scene["label"],
                    "persona": persona["name"],
                    "persona_id": persona["id"],
                    "elapsed": round(elapsed, 2),
                    "output": output,
                })
                voice = output.get("voice", "?")
                emotion = output.get("emotion", "?")
                print(f"  [{p_idx}/8] {persona['name']:12s} → 「{voice}」 ({emotion}, {elapsed:.1f}s)")
            except Exception as e:
                failures.append({"scene": scene["id"], "persona": persona["id"], "error": str(e)})
                print(f"  [{p_idx}/8] {persona['name']:12s} → FAIL: {e}")

    print(f"\n=== 完了 ===")
    print(f"  成功: {len(results)} / 失敗: {len(failures)}")
    print(f"  合計時間: {total_t:.1f}秒, 平均: {total_t/max(len(results),1):.1f}秒/件")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUTPUT_DIR / f"persona_probe_{TODAY}.json"
    md_path = OUTPUT_DIR / f"persona_probe_{TODAY}.md"

    with json_path.open("w", encoding="utf-8") as f:
        json.dump({
            "date": TODAY,
            "model": MODEL,
            "scenes": SCENES,
            "personas": PERSONAS,
            "results": results,
            "failures": failures,
        }, f, ensure_ascii=False, indent=2)

    md_path.write_text(render_markdown(results), encoding="utf-8")

    print(f"\n  JSON: {json_path}")
    print(f"  MD:   {md_path}")


if __name__ == "__main__":
    main()
