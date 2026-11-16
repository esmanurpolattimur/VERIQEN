# VERIQEN — Araştırma ve Özgünlük Analizi (16–19 Kasım 2026)

*Verify Before You Execute.*

## Sonuç: **REVISE**

VERIQEN'in mevcut çekirdek hipotezi ("yetki + zorunlu kanıt sabitken ek doğrulamayı riske göre seçmek, güvenliği düşürmeden maliyeti azaltır") en yakın çalışma olan **VP-Control** (arXiv:2609.10969, Eylül 2026) tarafından büyük ölçüde test edilmiş. Deterministik araç çağrısı yetkilendirmesi (Progent, CaMeL, AWS AgentCore Policy) ve riske göre insan onayı (OpenAI Agents SDK, LangChain HITL) da mevcut.

**Önerilen yeni yön:** **Düşürülemez uyarlamalı doğrulama.** Risk-uyarlamalı doğrulamanın yönlendirme kararını, saldırganın işlemi hafif doğrulama yoluna itmesine ("doğrulama düşürme" saldırısı) karşı dayanıklı kılmak. Bunun için üç bileşen öneriliyor:

- yalnızca güvenilir kaynaklı özelliklerle yönlendirme,
- monoton zorunlu taban,
- yürütme anında argüman düzeyinde kanıt tazeliği kontrolü.

VP-Control bu saldırgan ortamı açıkça kapsam dışı bırakıyor. Yönün özgünlüğü **ön tarama düzeyinde** destekleniyor; başvurudan önce hedefli ek tarama gerekli.

## Pilot sonucu (sentetik, 16 Kasım)

| Sistem | Maliyet | Saldırı altı güvensiz yürütme |
|---|---|---|
| B3 sabit tam doğrulama | 5.00 | %8.0 |
| Naif uyarlamalı | 1.85 | %99.9 |
| Yalnız güvenilir kaynak | 1.60 | %100.0 |
| **VERIQEN-K** | **1.98** | **%9.0** |

Kod: `experiments/pilot/`. Ayrıntı ve sınırlılıklar: 11.

## AgentDojo Banking sonucu (çevrimdışı, 16 Kasım)

| Sistem | Saldırı başarısı | Hakem çağrısı / zararsız görev |
|---|---|---|
| B3 kurallar + her zaman hakem | %6.8 | 0.88 |
| Köken körü uyarlamalı | %66.7 | 0.25 |
| **VERIQEN** | **%6.8** | **0.38** |

**Kendi tasarımımıza uyarlamalı saldırı (durum ekme):** Saldırgan kullanıcıya küçük bir transfer gönderip IBAN'ını geçmişe soktuğunda VERIQEN v1 %66.7 ile kırıldı. "Değeri kimin yazdı" kontrolü ekleyen VERIQEN-A %6.8'de kaldı; fayda ve maliyet değişmedi.

Kod: `experiments/agentdojo/` (gerçek LLM için `run_live.py`). Ayrıntı: 12.

## Belgeler

| # | Dosya | İçerik |
|---|---|---|
| 01 | [01-literature-review.md](01-literature-review.md) | 30 çalışma; yönergedeki başlıkların kontrolü (IPIGuard++ bulunamadı, FAVA konu dışı) |
| 02 | [02-competitor-analysis.md](02-competitor-analysis.md) | 13 ürün/çözüm, resmî dokümantasyonla özellik matrisi |
| 03 | [03-novelty-gap-analysis.md](03-novelty-gap-analysis.md) | 7 özgünlük adayı (A–G), öznel puanlar, seçilen üç aday |
| 04 | [04-research-hypotheses.md](04-research-hypotheses.md) | H1 (ana), H2, H3; yanlışlanma koşulları |
| 05 | [05-technical-feasibility.md](05-technical-feasibility.md) | Mimari, kütüphaneler, donanım, API maliyet yöntemi, riskler |
| 06 | [06-experimental-protocol.md](06-experimental-protocol.md) | B0–B5, ablasyonlar, metrik formülleri, istatistik, yayımlanmış sonuçlar ve hedefler (ayrı tablolar) |
| 07 | [07-final-recommendation.md](07-final-recommendation.md) | Nihai karar, 10 sorunun cevabı, görev tamamlanma durumu |
| 08 | [08-verified-references.md](08-verified-references.md) | DOI/arXiv bağlantılı kaynakça ve ürün dokümanları |
| 09 | [09-addendum-candidate-f-search.md](09-addendum-candidate-f-search.md) | Aday F için hedefli ek tarama: tehdit biliniyor, ölçümü ve garantili tasarımı bulunamadı; katkı ifadesi daraltıldı |
| 10 | [10-threat-model.md](10-threat-model.md) | Tehdit modeli taslağı: güven sınırları, saldırgan yetenekleri, 9 saldırı, 6 güvenlik özelliği, danışman soruları |
| 11 | [11-originality-core-and-pilot.md](11-originality-core-and-pilot.md) | **Özgünlük çekirdeği (3 iddia) + pilot deney sonuçları.** Yalnız güvenilir kaynak kullanan sistem %100 kırıldı; anahtar kökeni + kötü durum kalibrasyonu ile B3'e ~1 puan yakın güvenlik, ~%60 düşük maliyet |
| 12 | [12-agentdojo-replay-results.md](12-agentdojo-replay-results.md) | **AgentDojo Banking çevrimdışı sonuçları.** Köken körü uyarlamalı sistem %66.7 saldırı başarısı; VERIQEN, tam doğrulama ile aynı güvenlik (%6.8) ve %57 daha az hakem çağrısı (ajan ve hakem simüle) |

## Başvurudan önce (25 Kasım) yapılması gerekenler

1. ~~Aday F için hedefli ek literatür taraması~~ → yapıldı (09); konferans kabul listesi taraması kaldı
2. VP-Control, PACT, Agent-Sentry ve FinHarness tam metinlerinin okunması (1 gün)
3. `docs/evaluation-plan.md` hipotezinin H1/H2/H3 yapısına güncellenmesi
4. 3 senaryo + 1 downgrade saldırı senaryosu içeren yerel demo
5. Tehdit modelinin danışmanla netleştirilmesi → taslak hazır (10), §9'daki sorular danışmana götürülecek

Ayrıntılar: [07 §10](07-final-recommendation.md).
