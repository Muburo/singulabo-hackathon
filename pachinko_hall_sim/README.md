# pachinko_hall_sim

Singulabo Hackathon 提出用のパチンコホール物理実験シミュレーター。

仕様の SSoT は親ディレクトリの [CLAUDE.md](../CLAUDE.md) を参照。

## 概要

- **目的**: 「どういう属性の人が、どういう感情を持つか」を観測する物理実験
- **物理**: rule-based（抽選確率モデル + 感情更新ルール）
- **LLM**: 5 step ごとに行動決定 + 自己申告のみ間引き使用（qwen3:4b）
- **感情 2 系統**: rule-based canonical state + LLM 自己申告の併記

## 実行方法

### 環境構築

プロジェクトパスにコロン `:` が含まれるため、venv は `/tmp` に置く:

```bash
/usr/bin/python3 -m venv /tmp/sing_venv
/tmp/sing_venv/bin/python -m pip install \
  --trusted-host pypi.org --trusted-host files.pythonhosted.org \
  -r requirements.txt
```

### MVP run（Day1 以降）

```bash
/tmp/sing_venv/bin/python -m src.run_simulation \
  --config configs/run_mvp.yaml \
  --seed 42 \
  --no-llm
```

LLM 有効化は Day4 以降:

```bash
/tmp/sing_venv/bin/python -m src.run_simulation \
  --config configs/run_mvp.yaml \
  --seed 42
```

## ディレクトリ

| パス | 内容 |
|------|------|
| `data/persona_cards.jsonl` | 10人 sampling 済みペルソナ（Day0 で生成） |
| `configs/machines.yaml` | 3機種パラメータ（AT / Hokuto / ART） |
| `configs/run_mvp.yaml` | 案A（10 persona × 30 step）設定 |
| `src/models.py` | dataclass（PersonaCard/State, MachineType/State） |
| `src/machine.py` | 抽選物理 |
| `src/emotion.py` | 感情更新ルール |
| `src/policy_rule.py` | rule-based 行動 |
| `src/policy_llm.py` | LLM 行動 + self-report |
| `src/llm_client.py` | Ollama wrapper |
| `src/simulator.py` | メインループ |
| `src/logger.py` | JSONL ロガー |
| `src/visualize.py` | matplotlib 可視化 |
| `src/run_simulation.py` | CLI エントリポイント |
| `outputs/<run_id>/` | log + plot + animation |

## 実装スコープ

| 案 | persona | step | 機種 | LLM | 段階 |
|----|---------|------|------|-----|------|
| A (MVP) | 10 | 30 | 3×2=6 | 5 step ごと | Day1-5 |
| B (本命) | 30 | 50 | 3×4=12 | 5 step + event | Day6-8 |
| C (フル) | 100 | 100 | 30 | 10 step ごと | 余力時 |

詳細は [CLAUDE.md](../CLAUDE.md) を参照。
