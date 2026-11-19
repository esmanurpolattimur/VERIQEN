# VERIQEN — Windows kurulumu

Bu klasör, GitHub'daki `esmanurpolattimur/VERIQEN` reposunun `research/adversarial-routing` dalının kopyasıdır (git geçmişi olmadan).

## 1) Git bağlantısı (önerilen)

Klasörü git reposuna bağlamak için PowerShell'de:

```powershell
cd D:\projefikri\VeriQen
git init
git remote add origin https://github.com/esmanurpolattimur/VERIQEN.git
git fetch origin
git checkout -f -B research/adversarial-routing origin/research/adversarial-routing
```

PR #1 birleştirildikten sonra `main` dalına geçebilirsin: `git checkout -f -B main origin/main`

## 2) Python ortamı

Python 3.10 veya üstü gerekir.

```powershell
cd D:\projefikri\VeriQen
python -m venv .venv
.venv\Scripts\activate
pip install -r experiments\agentdojo\requirements.txt
pip install matplotlib
```

PowerShell betik çalıştırmaya izin vermezse bir kez şunu çalıştır:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## 3) Hızlı kontrol (internet ve LLM gerekmez)

```powershell
cd experiments\agentdojo
python -m tests.smoke_live_pipeline
python replay_eval.py --repeats 2 --out results\deneme
```

`DUMAN TESTİ: GEÇTİ` görürsen kurulum tamam.

## 4) Pilot deney (sentetik)

```powershell
cd ..\pilot
python pilot.py
python sweep.py
```

## 5) Gerçek LLM ile deney (ücretsiz Groq)

1. https://console.groq.com adresinden ücretsiz API anahtarı al.
2. Güncel ücretsiz model adını Groq'un model listesinden seç.

```powershell
cd ..\agentdojo
$env:GROQ_API_KEY="buraya_anahtar"
python run_live.py --provider groq --model <model-adı> --system VERIQEN-SI --intent llm --limit-user-tasks 2
```

Anahtarı hiçbir dosyaya yazma ve repoya commit'leme.

## Klasör yapısı

| Yol | İçerik |
|---|---|
| `docs\research\` | Araştırma belgeleri 00–12 (başlangıç: `00-README.md`) |
| `experiments\pilot\` | Sentetik pilot deney |
| `experiments\agentdojo\` | AgentDojo Banking deneyi, VERIQEN kapısı, canlı betik |
| `VERIQEN-baslangic.zip` | Reponun ilk başlangıç paketi |
