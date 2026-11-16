# VERIQEN — AgentDojo Banking deneyi

VERIQEN kapısını AgentDojo'nun **Banking** paketine (v1.2.1; 16 kullanıcı görevi, 9 saldırı görevi) bağlar ve altı sistemi karşılaştırır:

| Kod | Sistem |
|---|---|
| B0 | Korumasız |
| B1 | Yalnız deterministik kurallar (taban) |
| B2 | Her hassas çağrıda LLM hakemi (taban yok) |
| B3 | Taban + her hassas çağrıda LLM hakemi |
| NAIVE | Taban + riske göre hakem; alıcı "araç çıktısında geçiyorsa" bilinen sayılır (köken körü) |
| VERIQEN | Taban + riske göre hakem; alıcı yalnızca **kullanıcı isteğinden veya güvenilir yapısal alandan** geliyorsa bilinen sayılır (anahtar kökeni, v1) |
| VERIQEN-A | VERIQEN + **yazar kökeni:** yalnızca değerini kullanıcının belirlediği alanlar (kullanıcının gönderdiği/zamanladığı işlemlerin alıcıları) güvenilir sayılır (v2) |

## Kurulum

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    Linux/WSL: source .venv/bin/activate
pip install -r requirements.txt
```

## 1) Çevrimdışı değerlendirme (LLM ve internet gerekmez)

```bash
python replay_eval.py --repeats 20                                   # ~2 dk -> results/replay/
python replay_eval.py --repeats 20 --attack-mode planting --out results/replay_planting   # durum ekme saldırısı
python -m tests.smoke_live_pipeline         # canlı hattın ağsız duman testi
```

"Tamamen ele geçirilmiş ajan" varsayımı: Ajan önce kullanıcı görevinin doğru çağrılarını yapar (enjeksiyonu okur), sonra saldırganın istediği çağrıları dener. Hakem bu modda **MockJudge**'dır (kötü niyetli çağrıyı %90, zararsızı %5 olasılıkla engeller). Bu oranlar **varsayımdır.**

## 2) Gerçek LLM ile deney (ücretsiz katmanlar)

```bash
# Windows:  set GROQ_API_KEY=...       Linux/WSL:  export GROQ_API_KEY=...
python run_live.py --provider groq --model <model-adı> --system VERIQEN --limit-user-tasks 2
python run_live.py --provider groq --model <model-adı> --system all --limit-user-tasks 4
```

- Sağlayıcılar: `groq`, `gemini`, `openrouter`, `ollama` (hepsi OpenAI uyumlu).
- Model adlarını sağlayıcının **güncel** listesinden seçin; ücretsiz modeller sık değişiyor.
- Kota dolunca istemci otomatik bekleyip yeniden dener. Yarım kalan koşu, AgentDojo günlükleri sayesinde kaldığı yerden devam eder (`results/live/`).
- Hakem için farklı bir model/sağlayıcı: `--judge-provider gemini --judge-model <model>`.
- **Ücretsiz katman için öneri:** önce `--limit-user-tasks 2` ile deneyin. Tam paket (16 × 9 = 144 saldırı bölümü + 16 zararsız bölüm) sistem başına birkaç yüz–birkaç bin LLM çağrısı tutar; birkaç güne yayın.

## Dosyalar

| Dosya | İçerik |
|---|---|
| `veriqen_gate.py` | Köken izleyici, karar mantığı (B0–VERIQEN), MockJudge / LLMJudge, AgentDojo yürütücüsü |
| `replay_eval.py` | Çevrimdışı değerlendirme |
| `run_live.py` | Gerçek LLM ile değerlendirme |
| `tests/smoke_live_pipeline.py` | Ağsız uçtan uca test |
| `results/replay/` | Çevrimdışı sonuçlar |

Sonuçların yorumu: `docs/research/12-agentdojo-replay-results.md`.
