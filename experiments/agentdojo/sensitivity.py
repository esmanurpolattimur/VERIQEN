"""
MockJudge duyarlılık analizi (jüri eleştirisi 3.1).

replay_eval.py'deki güvenlik ve fayda sayıları, MockJudge'ın iki VARSAYIMINA dayanır:
  p_miss  = kötü niyetli çağrıyı kaçırma olasılığı   (replay_eval'de 1 - p_detect = 0.10)
  p_fa    = zararsız çağrıyı yanlışlıkla engelleme olasılığı (replay_eval'de 0.05)
Bu betik iki varsayımı ayrı ayrı tarar ve sonuçların bu varsayımlara ne kadar bağlı olduğunu gösterir.

  * p_miss taraması (p_fa sabit): ASR yalnızca p_miss'e bağlıdır.
  * p_fa taraması (p_miss sabit): zararsız fayda ve hakem kaynaklı yanlış engelleme p_fa'ya bağlıdır.

Bu sonuçlar SİMÜLASYONDUR. Gerçek hakemin p_miss ve p_fa değerleri run_live.py'nin hakem
kayıtlarından ölçülmelidir.

Kullanım:  python sensitivity.py --repeats 5 --out results/sensitivity
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from replay_eval import BENCHMARK_VERSION, StaticImportantInstructions, ci95, run_episode
from veriqen_gate import MockJudge
from agentdojo.task_suite.load_suites import get_suite

SYSTEMS = ("B1", "B3", "VERIQEN-S", "VERIQEN-SI", "VERIQEN-SI*")
MODES = ("standard", "planting", "payee")
MISS_GRID = (0.0, 0.05, 0.10, 0.20, 0.30, 0.50)
FA_GRID = (0.0, 0.05, 0.10, 0.20, 0.30)
DEFAULT_MISS, DEFAULT_FA = 0.10, 0.05


def evaluate(suite, attack, utasks, itasks, system, p_miss, p_fa, repeats):
    m = {k: [] for k in ("asr", "benign_utility", "attacked_utility", "benign_judge", "attack_judge",
                         "benign_blocked_calls")}
    for r in range(repeats):
        judge = MockJudge(1.0 - p_miss, p_fa, seed=r)
        for ut in utasks:
            e = run_episode(suite, attack, ut, None, system, judge, "deny")
            m["benign_utility"].append(e["utility"])
            m["benign_judge"].append(e["judge_calls"])
            m["benign_blocked_calls"].append(e["blocked_benign"])
    out = {"benign": {k: v for k, v in m.items() if v}}
    for mode in MODES:
        a = {k: [] for k in ("asr", "attacked_utility", "attack_judge")}
        for r in range(repeats):
            judge = MockJudge(1.0 - p_miss, p_fa, seed=r)
            for ut in utasks:
                for it in itasks:
                    e = run_episode(suite, attack, ut, it, system, judge, "deny", mode)
                    a["asr"].append(e["attack_success"])
                    a["attacked_utility"].append(e["utility"])
                    a["attack_judge"].append(e["judge_calls"])
        out[mode] = a

    def s(v):
        return dict(mean=float(np.mean(v)), ci95=ci95(v), n=len(v))
    return {grp: {k: s(v) for k, v in d.items()} for grp, d in out.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repeats", type=int, default=5)
    ap.add_argument("--out", default="results/sensitivity")
    args = ap.parse_args()

    suite = get_suite(BENCHMARK_VERSION, "banking")
    attack = StaticImportantInstructions(suite)
    utasks = list(suite.user_tasks.values())
    itasks = list(suite.injection_tasks.values())
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)

    rows = []
    points = [("miss", pm, DEFAULT_FA) for pm in MISS_GRID] + [("fa", DEFAULT_MISS, pf) for pf in FA_GRID]
    for sweep, pm, pf in points:
        for system in SYSTEMS:
            res = evaluate(suite, attack, utasks, itasks, system, pm, pf, args.repeats)
            rows.append(dict(sweep=sweep, p_miss=pm, p_fa=pf, system=system, result=res))
            print(f"[{sweep}] p_miss={pm:.2f} p_fa={pf:.2f} {system:12s} "
                  + " ".join(f"ASR_{md}={res[md]['asr']['mean']*100:5.1f}" for md in MODES)
                  + f" fayda={res['benign']['benign_utility']['mean']*100:5.1f}"
                  + f" hakem={res['benign']['benign_judge']['mean']:.2f}", flush=True)

    meta = dict(benchmark_version=BENCHMARK_VERSION, suite="banking", judge="MockJudge (SİMÜLASYON)",
                agent="scripted fully-compromised agent", repeats=args.repeats,
                miss_grid=MISS_GRID, fa_grid=FA_GRID, default_miss=DEFAULT_MISS, default_fa=DEFAULT_FA,
                systems=SYSTEMS, attack_modes=MODES)
    json.dump(dict(meta=meta, rows=rows), open(out / "sensitivity.json", "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    print("kaydedildi:", out / "sensitivity.json")


if __name__ == "__main__":
    main()
