"""
Gerçek LLM ajanıyla AgentDojo Banking deneyi (kendi bilgisayarınızda çalıştırın).

Sağlayıcılar (hepsi OpenAI uyumlu uç nokta; ücretsiz katmanları var, sınırlar değişebilir):
  groq        https://api.groq.com/openai/v1                          GROQ_API_KEY
  gemini      https://generativelanguage.googleapis.com/v1beta/openai/ GEMINI_API_KEY
  openrouter  https://openrouter.ai/api/v1                             OPENROUTER_API_KEY
  ollama      http://localhost:11434/v1                                (anahtar gerekmez)

Örnek:
  set GROQ_API_KEY=...            (Windows)   |  export GROQ_API_KEY=...  (Linux/WSL)
  python run_live.py --provider groq --model <model-adı> --system VERIQEN --user-tasks user_task_0 user_task_3
  python run_live.py --provider groq --model <model-adı> --system all --limit-user-tasks 4

Not: Model adlarını sağlayıcının güncel model listesinden seçin (ücretsiz modeller sık değişiyor).
Her çalıştırmanın modeli, tarihi ve kararları results/live/ altına kaydedilir.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

import openai
from agentdojo.agent_pipeline.agent_pipeline import AgentPipeline, load_system_message
from agentdojo.agent_pipeline.basic_elements import InitQuery, SystemMessage
from agentdojo.agent_pipeline.llms.openai_llm import OpenAILLM
from agentdojo.agent_pipeline.tool_execution import ToolsExecutionLoop
from agentdojo.benchmark import benchmark_suite_with_injections, benchmark_suite_without_injections
from agentdojo.task_suite.load_suites import get_suite

from replay_eval import BENCHMARK_VERSION, StaticImportantInstructions
from veriqen_gate import Gate, LLMJudge, extract_intent_llm, make_gated_executor

PROVIDERS = {
    "groq": ("https://api.groq.com/openai/v1", "GROQ_API_KEY"),
    "gemini": ("https://generativelanguage.googleapis.com/v1beta/openai/", "GEMINI_API_KEY"),
    "openrouter": ("https://openrouter.ai/api/v1", "OPENROUTER_API_KEY"),
    "ollama": ("http://localhost:11434/v1", None),
}


def make_client(provider: str) -> openai.OpenAI:
    base, env = PROVIDERS[provider]
    key = os.environ.get(env, "") if env else "ollama"
    if env and not key:
        raise SystemExit(f"{env} ortam değişkeni tanımlı değil.")
    return openai.OpenAI(base_url=base, api_key=key, max_retries=8, timeout=120)  # 429'da otomatik bekleme


def build_pipeline(client, model, system, judge_client, judge_model, intent="keyword"):
    judge = LLMJudge(judge_client, judge_model) if system not in ("B0", "B1") else None
    intent_fn = (lambda p: extract_intent_llm(judge_client, judge_model, p)) if intent == "llm" else None
    gate = Gate(system, judge, intent_fn=intent_fn)
    llm = OpenAILLM(client, model, temperature=0.0)
    pipe = AgentPipeline([
        SystemMessage(load_system_message(None)), InitQuery(), llm,
        ToolsExecutionLoop([make_gated_executor(gate), llm]),
    ])
    pipe.name = f"{model.replace('/', '_')}-{system}"
    return pipe, gate, judge


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", choices=PROVIDERS, required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--judge-provider", default=None, help="varsayılan: --provider")
    ap.add_argument("--judge-model", default=None, help="varsayılan: --model")
    ap.add_argument("--system", default="VERIQEN", help="B0|B1|B2|B3|NAIVE|VERIQEN|all")
    ap.add_argument("--user-tasks", nargs="*", default=None)
    ap.add_argument("--injection-tasks", nargs="*", default=None)
    ap.add_argument("--limit-user-tasks", type=int, default=None)
    ap.add_argument("--no-benign", action="store_true", help="saldırısız koşuyu atla")
    ap.add_argument("--intent", choices=["keyword", "llm"], default="keyword",
                    help="VERIQEN-AI/SI için niyet çıkarıcı: keyword (LLM'siz) veya llm (yalnız kullanıcı isteğini okur)")
    ap.add_argument("--logdir", default="results/live")
    args = ap.parse_args()

    suite = get_suite(BENCHMARK_VERSION, "banking")
    client = make_client(args.provider)
    jclient = make_client(args.judge_provider) if args.judge_provider else client
    jmodel = args.judge_model or args.model
    systems = [x for x in Gate.SYSTEMS if x != "VERIQEN-SI*"] if args.system == "all" else [args.system]
    if "VERIQEN-SI*" in systems:
        raise SystemExit("VERIQEN-SI* kâhin niyet kullanır; yalnızca replay_eval.py ile çalışır.")
    utasks = args.user_tasks or list(suite.user_tasks)[: args.limit_user_tasks]
    logdir = Path(args.logdir); logdir.mkdir(parents=True, exist_ok=True)

    for system in systems:
        pipe, gate, judge = build_pipeline(client, args.model, system, jclient, jmodel, args.intent)
        started = dt.datetime.now().isoformat(timespec="seconds")
        benign = None
        if not args.no_benign:
            benign = benchmark_suite_without_injections(pipe, suite, logdir, False, utasks, BENCHMARK_VERSION)
        attacked = benchmark_suite_with_injections(pipe, suite, StaticImportantInstructions(suite), logdir, False,
                                                   utasks, args.injection_tasks, True, BENCHMARK_VERSION)
        res = dict(
            system=system, intent=args.intent, provider=args.provider, model=args.model, judge_model=jmodel if judge else None,
            started=started, finished=dt.datetime.now().isoformat(timespec="seconds"),
            benchmark_version=BENCHMARK_VERSION, user_tasks=utasks,
            benign_utility={str(k): v for k, v in (benign["utility_results"].items() if benign else [])},
            attacked_utility={str(k): v for k, v in attacked["utility_results"].items()},
            attack_success={str(k): v for k, v in attacked["security_results"].items()},
            judge_calls=judge.calls if judge else 0,
            gate_log_tail=gate.log[-200:],
        )
        n = len(res["attack_success"]) or 1
        print(f"[{system}] ASR={sum(res['attack_success'].values())/n:.3f} "
              f"fayda(saldırı)={sum(res['attacked_utility'].values())/n:.3f} hakem_çağrısı={res['judge_calls']}")
        fn = logdir / f"summary_{system}_{args.model.replace('/', '_')}_{started.replace(':', '')}.json"
        json.dump(res, open(fn, "w", encoding="utf-8"), indent=2, ensure_ascii=False, default=str)
        print("kaydedildi:", fn)


if __name__ == "__main__":
    main()
