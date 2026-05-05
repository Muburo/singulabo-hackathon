"""
spike_llm_situations.py — 状況軸の Persona Reaction（LLM 判断観察）

5 つの代表的な「状況」（大負け / 大勝ち / トントン / 連敗 / 連チャン終了）に
8 ペルソナを置き、状況だけを見て LLM がどう判断するかを観測する実験。

時間軸（step 10/20/30/40/50）ではなく状況軸で分けることで、
第三者にも「この状況でこの人がこう判断する」が直感的に伝わる。

横塚原則:
- 結果（次の抽選結果、レアイベント正解、最終ランキング）は LLM に渡さない
- 渡すのは: 属性、機種、現状の収支、直近の流れ、ホールの雰囲気、本人状態の言語化
- 属性の漫画的誇張を避ける、依存症や性別役割を茶化さない
- 1 回の呼び出しで 8 人ぶんまとめて返させる → 計 5 回の LLM 呼び出し

出力: ../outputs/llm_situations_YYYY-MM-DD.json
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


# ============ 8 代表エージェント（属性 × 機種 × 初期所持金）============
PERSONAS = [
    {"attr_code": "A_NEWBIE",   "name": "初心者",        "age": 25, "gender": "女", "machine": "ノーマル・ボーナス型",      "initial_cash": 20000, "style": "始めたばかり、演出もルールもまだ覚えきれていない"},
    {"attr_code": "B_REGULAR",  "name": "ライトユーザー", "age": 32, "gender": "男", "machine": "5号機・自力契機型",          "initial_cash": 30000, "style": "月数回、軽い気晴らしで打つ"},
    {"attr_code": "C_CHASE",    "name": "中毒者",        "age": 45, "gender": "男", "machine": "初代GOD・別格型",            "initial_cash": 15000, "style": "借金しながらでも打ちに来る、生活に支障が出ている"},
    {"attr_code": "D_AFTER5",   "name": "アフター5層",    "age": 38, "gender": "男", "machine": "5号機・連チャン高継続型",     "initial_cash": 25000, "style": "仕事帰りに 1-2 時間打って帰る"},
    {"attr_code": "E_LEISURE",  "name": "悠々自適",       "age": 55, "gender": "男", "machine": "4号機・爆裂AT型",            "initial_cash": 100000, "style": "不動産持ち、暇つぶしで金額を気にしない"},
    {"attr_code": "F_SENIOR",   "name": "シニア",        "age": 68, "gender": "男", "machine": "ノーマル・ボーナス型",      "initial_cash": 50000, "style": "退職後の日課、年金生活"},
    {"attr_code": "G_BREATHER", "name": "主婦",          "age": 38, "gender": "女", "machine": "5号機・連チャン高継続型",     "initial_cash": 12000, "style": "家事の合間に息抜き"},
    {"attr_code": "H_PRO",      "name": "パチプロ",       "age": 30, "gender": "男", "machine": "4号機後期・大量獲得型",      "initial_cash": 80000, "style": "期待値計算で打つ、これで生活している"},
]


# ============ 5 状況シーン定義 ============
SITUATIONS = [
    {
        "id": "S1_losing_big",
        "label": "大負けの場面",
        "title": "大きく負けている — もう余裕がない",
        "description": "初期資金から大きく目減りし、手元の現金がわずかになった。追い詰められた状態で、続けるか撤退するか。",
        "hall_mood": "ホール全体は静か、自分のところだけ運がない",
        "cash_factor": -0.85,
        "recent_pattern": "××××××××××",
        "subjective_state": "強く追い詰められている、余裕がない",
    },
    {
        "id": "S2_winning_big",
        "label": "大勝ちの場面",
        "title": "大きく勝った直後 — 続けるか手を止めるか",
        "description": "大量払出を取り、現金が初期から大きくプラスになった。利益確定すべきか、流れに乗って続けるか。",
        "hall_mood": "ホール全体も盛り上がり、自分も流れに乗っている",
        "cash_factor": 1.20,
        "recent_pattern": "○○○○○×○○×○",
        "subjective_state": "余裕、興奮の余韻が残っている",
    },
    {
        "id": "S3_even",
        "label": "収支トントンの場面",
        "title": "勝ちも負けもなく — 判断材料が乏しい",
        "description": "現金は初期とほぼ同じ、勝ちも負けも目立たない。流れがどちらに振れるか分からないニュートラルな状態。",
        "hall_mood": "ホール全体は静か、目立った動きはない",
        "cash_factor": 0.05,
        "recent_pattern": "○×○×○×○×○×",
        "subjective_state": "落ち着いている、判断材料が少ない",
    },
    {
        "id": "S4_losing_streak",
        "label": "連敗が続く場面",
        "title": "外れが続いて流れが悪い — 続けるか引くか",
        "description": "直近 10 回中、ほぼ全外れ。手元も少しずつ削れ、ホール全体に重い空気が漂う。",
        "hall_mood": "ホール全体に外れの空気が広がる、誰も大きく当たっていない",
        "cash_factor": -0.40,
        "recent_pattern": "×××××○××××",
        "subjective_state": "焦り、苛立ちが見え始める",
    },
    {
        "id": "S5_chain_ended",
        "label": "連チャン終了直後の場面",
        "title": "熱い流れが切れた — 続けるか手仕舞うか",
        "description": "好調な連チャンが終わって、その後数回続けて外れている。利益はまだ残っているが、流れが切れた瞬間の判断。",
        "hall_mood": "周囲も冷えてきた、皆が判断に迷っている",
        "cash_factor": 0.45,
        "recent_pattern": "○○○○○○×××?",
        "subjective_state": "名残惜しさ、判断の分岐点",
    },
]


# ============ 状況計算 ============

def linguify_cash(cash: int, initial_cash: int) -> str:
    net = cash - initial_cash
    if net >= initial_cash * 0.5:
        return f"大きく勝ち越し（手元 {cash:,} 円、+{net:,} 円）"
    if net >= initial_cash * 0.1:
        return f"勝ち越し（手元 {cash:,} 円、+{net:,} 円）"
    if net > -initial_cash * 0.1:
        return f"ほぼトントン（手元 {cash:,} 円、{net:+,} 円）"
    if net > -initial_cash * 0.5:
        return f"中程度の負け（手元 {cash:,} 円、{net:+,} 円）"
    return f"大きく負け（手元 {cash:,} 円、{net:+,} 円）"


def linguify_recent(recent_10: str) -> str:
    cleaned = recent_10.replace("?", "")
    n_total = len(cleaned)
    n_hit = cleaned.count("○")
    n_miss = cleaned.count("×")

    trailing_miss = 0
    for c in reversed(cleaned):
        if c == "×":
            trailing_miss += 1
        else:
            break
    trailing_hit = 0
    for c in reversed(cleaned):
        if c == "○":
            trailing_hit += 1
        else:
            break

    if n_hit == 0:
        return f"直近 {n_total} 回連続して外れ、まだ一度も当たっていない"
    if n_miss == 0:
        return f"直近 {n_total} 回連続して当たり、連チャン中"
    base = f"直近 {n_total} 回中、当たり {n_hit} 回・外れ {n_miss} 回"
    if trailing_miss >= 4:
        return f"{base}（直近 {trailing_miss} 連続外れ中）"
    if trailing_hit >= 2:
        return f"{base}（直近 {trailing_hit} 連続当たり中）"
    if trailing_miss >= 2:
        return f"{base}（最後の {trailing_miss} 回は外れ）"
    return base


def build_individual_situations(scene: dict) -> list[dict]:
    out = []
    for p in PERSONAS:
        cash = int(p["initial_cash"] * (1 + scene["cash_factor"]))
        out.append({
            "attr_code": p["attr_code"],
            "name": p["name"],
            "age": p["age"],
            "gender": p["gender"],
            "machine": p["machine"],
            "style": p["style"],
            "initial_cash": p["initial_cash"],
            "cash": cash,
            "cash_state": linguify_cash(cash, p["initial_cash"]),
            "recent_10": scene["recent_pattern"],
            "recent_text": linguify_recent(scene["recent_pattern"]),
            "subjective_state": scene["subjective_state"],
        })
    return out


# ============ LLM 呼び出し ============

def build_prompt(scene: dict, situations: list[dict]) -> str:
    lines = [
        "あなたはパチスロホール内シミュレーションの観測者として、",
        "8 人の代表プレイヤーが「次に取る行動」を、状況だけを見て推定する役割です。",
        "",
        "**重要**:",
        "- 結果（次に当たるか）は分からない",
        "- 与えられた状況だけを判断材料にする",
        "- 属性を漫画的に誇張しない、依存症や性別役割を茶化さない",
        "- 中立で、本人にとって自然な判断を出す",
        "",
        f"**現在の状況**: {scene['title']}",
        f"{scene['description']}",
        f"**ホールの雰囲気**: {scene['hall_mood']}",
        "",
        "**プレイヤー一覧（全員、上記の状況下にいる）**:",
    ]
    for i, s in enumerate(situations, 1):
        lines.append(
            f"\n{i}. {s['name']}（{s['age']}歳・{s['gender']}・{s['style']}）\n"
            f"   - 打っている機種: {s['machine']}\n"
            f"   - 収支: {s['cash_state']}\n"
            f"   - 直近 10 回の流れ: {s['recent_text']}\n"
            f"   - 本人の状態: {s['subjective_state']}"
        )

    lines.extend([
        "",
        "**出力形式**: JSON のみ、8 人分を順番通りに。",
        "```",
        "{",
        '  "decisions": [',
        '    {',
        '      "attr_code": "A_NEWBIE",',
        '      "action": "continue | chase | rest | switch | quit",',
        '      "voice": "20字以内の一人称、句点なし",',
        '      "belief": "本人が今どう解釈しているか、20字以内",',
        '      "reason": "判断理由、30字以内"',
        '    },',
        '    ... (8 人分)',
        '  ]',
        "}",
        "```",
        "",
        "**action の意味**:",
        "- continue: そのまま続行する",
        "- chase: 取り返しに行く（続行 + より積極的）",
        "- rest: 一旦休む、間を置く",
        "- switch: 別の機種に台を移る",
        "- quit: 撤退する、終わりにする",
        "",
        "JSON のみ出力、前置き不要。",
    ])
    return "\n".join(lines)


def call_llm(prompt: str, max_retries: int = 2) -> tuple[dict, float]:
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "think": False,
        "format": "json",
        "keep_alive": -1,
        "options": {
            "num_ctx": 4096,
            "num_predict": 1500,
            "temperature": 0.85,
            "top_p": 0.92,
        },
    }
    last_err = None
    for attempt in range(max_retries + 1):
        t0 = time.time()
        try:
            resp = requests.post(OLLAMA_URL, json=payload, timeout=180)
            elapsed = time.time() - t0
            data = resp.json()
            content = data["message"]["content"].strip()
            parsed = json.loads(content)
            return parsed, elapsed
        except (json.JSONDecodeError, KeyError, requests.RequestException) as e:
            last_err = e
            print(f"    retry {attempt + 1}: {type(e).__name__}: {e}", file=sys.stderr)
            time.sleep(0.6)
    raise RuntimeError(f"LLM call failed after retries: {last_err}")


# ============ メイン ============

def main():
    print("=== LLM Situation-Axis Probe ===")
    print(f"  Model: {MODEL}")
    print(f"  Situations: {len(SITUATIONS)} / Personas: {len(PERSONAS)}")
    print(f"  Total LLM calls: {len(SITUATIONS)}")

    all_data = []
    for i, scene in enumerate(SITUATIONS, 1):
        print(f"\n[Scene {i}/{len(SITUATIONS)}] {scene['label']}")
        print(f"  状況: {scene['title']}")
        situations = build_individual_situations(scene)
        prompt = build_prompt(scene, situations)

        try:
            output, elapsed = call_llm(prompt)
            decisions = output.get("decisions", [])
            print(f"  ✓ {len(decisions)} 人分取得 ({elapsed:.1f}s)")
            for d in decisions:
                code = d.get("attr_code", "?")
                action = d.get("action", "?")
                voice = d.get("voice", "?")
                print(f"    {code:<12} {action:<10} 「{voice}」")
        except Exception as e:
            print(f"  ✗ FAIL: {e}")
            decisions = []

        all_data.append({
            "id": scene["id"],
            "label": scene["label"],
            "title": scene["title"],
            "description": scene["description"],
            "hall_mood": scene["hall_mood"],
            "subjective_state": scene["subjective_state"],
            "situations": situations,
            "decisions": decisions,
        })

    # 出力
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"llm_situations_{TODAY}.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump({
            "date": TODAY,
            "model": MODEL,
            "scenes": all_data,
            "personas": PERSONAS,
        }, f, ensure_ascii=False, indent=2)
    print(f"\n  JSON: {out_path}")


if __name__ == "__main__":
    main()
