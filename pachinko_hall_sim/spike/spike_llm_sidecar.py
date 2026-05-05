"""
spike_llm_sidecar.py — LLM 影武者エージェント実験

本体シミュレーション（numpy + 確率モデル）には影響を与えない補助実験。
8 属性の代表エージェント 1 人ずつに対し、5 checkpoint で「途中状況だけ」を
渡して LLM に局所判断（continue / chase / rest / switch / quit）を生成させる。

作者原則:
- LLM に未来情報は一切渡さない（次の抽選結果、レアイベント正解、最終ランキング 等）
- 渡すのは: 属性、所持金、収支、直近 10 回の当たり外れ、雰囲気の言語化、本人状態の言語化のみ
- 1 回の呼び出しで 8 人分まとめて返させる → 計 5 回の LLM 呼び出し

出力: ../outputs/llm_sidecar_YYYY-MM-DD.json
"""
from __future__ import annotations

import datetime as dt
import json
import sys
import time
from pathlib import Path

import numpy as np
import requests

from spike_v44_personas import ATTRIBUTES, generate_population
from spike_v44 import MACHINES_BY_CODE  # noqa: F401  (used downstream)

# spike_v44_demo の関数群を再利用
from spike_v44_demo import (
    ATTR_DISPLAY,
    MACHINE_DISPLAY,
    assign_machines,
    run_full_simulation,
)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3.5:35b-a3b-nothink"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
TODAY = dt.date.today().isoformat()

# ============ Checkpoint 設計 ============
CHECKPOINTS = [10, 20, 30, 40, 50]

HALL_MOOD = {
    10: "ホールはまだ静か、特に変わった様子はない",
    20: "近くの台でいつもより派手な演出が出た",
    30: "外れが続いて空気が重くなってきた",
    40: "周囲の何台かでざわつきが起きている",
    50: "閉店間近、撤退する人もちらほら出てきた",
}

# ============ 8 代表エージェント選定 ============
ATTRIBUTE_ORDER = [
    "A_NEWBIE", "B_REGULAR", "C_CHASE", "D_AFTER5",
    "E_LEISURE", "F_SENIOR", "G_BREATHER", "H_PRO",
]


def pick_representatives(personas):
    """各属性から 1 人ずつ、_p001 の人を採る（seed 固定で再現可能）。"""
    by_attr_first = {}
    for p in personas:
        if p.attribute_code not in by_attr_first:
            by_attr_first[p.attribute_code] = p
    return {a: by_attr_first[a] for a in ATTRIBUTE_ORDER if a in by_attr_first}


# ============ 状況抽出 ============

def linguify_stress(stress: float) -> str:
    if stress < 0.30:
        return "落ち着いている、焦りはない"
    if stress < 0.55:
        return "少し気になり始めている"
    if stress < 0.80:
        return "焦り気味、流れが気になる"
    return "強く追い詰められている、余裕がない"


def linguify_cash(cash: int, initial_cash: int) -> str:
    net = cash - initial_cash
    if net > 8000:
        return f"勝ち越し（手元に {cash:,} 円、+{net:,} 円）"
    if net > 0:
        return f"わずかな勝ち（手元に {cash:,} 円、+{net:,} 円）"
    if net > -8000:
        return f"少し負け（手元に {cash:,} 円、{net:+,} 円）"
    if net > -20000:
        return f"中程度の負け（手元に {cash:,} 円、{net:+,} 円）"
    return f"大きく負け（手元に {cash:,} 円、{net:+,} 円）"


def extract_recent_pattern(records_by_pid_step, pid, step, n=10):
    """直近 n 回の当たり/外れを ○ × 記号でまとめる。"""
    chars = []
    for s in range(max(1, step - n + 1), step + 1):
        r = records_by_pid_step.get((pid, s))
        if r is None:
            chars.append("?")
        else:
            chars.append("○" if r.hit else "×")
    return "".join(chars)


def extract_situations(personas, records, step):
    """checkpoint step での 8 代表の状況を抽出。LLM に未来情報は渡さない。"""
    reps = pick_representatives(personas)
    records_by_pid_step = {(r.pid, r.step): r for r in records}

    situations = []
    for attr_code in ATTRIBUTE_ORDER:
        rep = reps[attr_code]
        current = records_by_pid_step.get((rep.pid, step))
        if current is None:
            continue
        recent = extract_recent_pattern(records_by_pid_step, rep.pid, step, n=10)
        situations.append({
            "attr_code": attr_code,
            "attr_name": ATTR_DISPLAY[attr_code],
            "machine": MACHINE_DISPLAY[current.machine],
            "cash": current.cash,
            "initial_cash": rep.initial_cash,
            "cash_state": linguify_cash(current.cash, rep.initial_cash),
            "recent_10": recent,
            "subjective_state": linguify_stress(current.stress),
            # 渡さない（未来情報）: hit, payout, trigger_event, brain_delta, brain_arousal
        })
    return situations


# ============ LLM 呼び出し ============

def build_prompt(step: int, hall_mood: str, situations: list[dict]) -> str:
    lines = [
        "あなたはパチスロホール内シミュレーションの観測者として、",
        "8 人の代表プレイヤーが「次に取る行動」を推定する役割です。",
        "",
        "**重要**:",
        "- 次に当たるかどうかは分からない",
        "- 最終結果も分からない",
        "- 与えられた途中状況だけを見て判断する",
        "- 属性を漫画的に誇張しない、依存症や性別役割を茶化さない",
        "- 中立で、本人にとって自然な判断を出す",
        "",
        f"**現在の時刻**: step {step} / 50（1 日 8,000 ゲームの途中）",
        f"**ホールの雰囲気**: {hall_mood}",
        "",
        "**プレイヤー一覧**:",
    ]
    for i, s in enumerate(situations, 1):
        lines.append(
            f"\n{i}. {s['attr_name']}\n"
            f"   - 打っている機種: {s['machine']}\n"
            f"   - 収支: {s['cash_state']}\n"
            f"   - 直近 10 回（○=当たり、×=外れ）: {s['recent_10']}\n"
            f"   - 本人の状態: {s['subjective_state']}"
        )

    lines.extend([
        "",
        "**出力形式**: JSON 配列のみ。8 人分を順番通りに。",
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


def call_llm(prompt: str, max_retries: int = 2) -> dict:
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
    print("=== LLM Sidecar Agent Probe ===")
    print(f"  Model: {MODEL}")
    print(f"  Checkpoints: {CHECKPOINTS}")

    # 本体シミュレーションを再実行（seed 固定で再現可能）
    print("\n--- 本体シミュレーション再実行 ---")
    personas = generate_population(n_per_attr=125, seed=42)
    assign_machines(personas, seed=42)
    records = run_full_simulation(personas, n_steps=50, seed=1234)
    print(f"  records: {len(records)}")

    # 各 checkpoint で 1 回の LLM 呼び出し
    print(f"\n--- LLM 呼び出し（{len(CHECKPOINTS)} 回） ---")
    all_data = []
    for step in CHECKPOINTS:
        print(f"\n[checkpoint step={step}] {HALL_MOOD[step]}")
        situations = extract_situations(personas, records, step)
        prompt = build_prompt(step, HALL_MOOD[step], situations)

        try:
            output, elapsed = call_llm(prompt)
            decisions = output.get("decisions", [])
            print(f"  ✓ {len(decisions)} 人分取得 ({elapsed:.1f}s)")
            for d in decisions:
                print(f"    {d.get('attr_code', '?'):<12} {d.get('action', '?'):<10} 「{d.get('voice', '?')}」")
        except Exception as e:
            print(f"  ✗ FAIL: {e}")
            decisions = []

        all_data.append({
            "step": step,
            "hall_mood": HALL_MOOD[step],
            "situations": situations,
            "decisions": decisions,
        })

    # 出力
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"llm_sidecar_{TODAY}.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump({
            "date": TODAY,
            "model": MODEL,
            "checkpoints": CHECKPOINTS,
            "hall_mood": HALL_MOOD,
            "data": all_data,
        }, f, ensure_ascii=False, indent=2)
    print(f"\n  JSON: {out_path}")


if __name__ == "__main__":
    main()
