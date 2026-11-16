# 07 — Nihai Öneri

## Karar: **REVISE**

**Gerekçe (tek paragraf):** VERIQEN'in mevcut çekirdek hipotezi, yani yetki ve zorunlu kanıt sabitken ek doğrulamayı riske göre seçerek güvenliği düşürmeden maliyeti azaltmak, **VP-Control** (arXiv:2609.10969, Eylül 2026) tarafından kanıt soyu, geri alınabilirlik, idempotency ve kontrol sonrası yarış dahil olmak üzere büyük ölçüde test edilmiş durumda. Deterministik araç çağrısı yetkilendirmesi akademide (Progent, CaMeL, PACT) ve üründe (AWS AgentCore Policy) çözülmüş; riske göre insan onayı ise ticari SDK'larda (OpenAI Agents SDK, LangChain HITL) hazır bir özellik. Bu nedenle mevcut hâliyle özgünlük savunulamaz (NO-GO'ya yakın). Buna karşılık VP-Control'ün **açıkça kapsam dışı bıraktığı saldırgan ortam**, VERIQEN'in mevcut mimarisiyle uyumlu ve GPU gerektirmeyen bir yön sunuyor: **uyarlamalı doğrulamanın yönlendirme kararını saldırgana karşı dayanıklı kılmak.** Teknik zemin sağlam, mimari büyük ölçüde korunabilir; değişmesi gereken **özgünlük iddiası ve hipotez**. Bu yüzden karar **REVISE**.

---

## Önerilen tek ana araştırma yönü

### "Düşürülemez uyarlamalı doğrulama" (Aday F + G tabanı)

**Bir cümlelik iddia:**
Otonom ajanların araç çağrılarında risk-uyarlamalı doğrulama, yönlendirme kararı yalnızca güvenilir kaynaklardan hesaplanan özelliklerle verildiğinde ve sabit bir zorunlu tabanın altına inemediğinde, uyarlamalı "doğrulama düşürme" saldırılarına karşı sabit tam doğrulama kadar güvenli kalırken doğrulama maliyetini anlamlı ölçüde azaltabilir. Bu bir **hipotezdir**; henüz sınanmadı.

**Neden bu yön seçildi:**

1. En yakın çalışmanın (VP-Control) açıkça bıraktığı boşluğa denk geliyor: saldırgan yazarlar ve sahte köken.
2. Diğer alanlarda (kademeli LLM'ler, LLM yönlendiricileri) yönlendirmenin saldırı yüzeyi olduğu gösterilmiş. Araç çağrısı yetkilendirmesindeki uyarlamalı doğrulama için bu tehdit modeli ve ölçütü bu taramada bulunamadı.
3. Mevcut VERIQEN mimarisini (Gateway, karar motoru, yürütücü, simülatör) çöpe atmıyor; üzerine bir **tehdit modeli, ölçüt ve tasarım kısıtı** ekliyor.
4. GPU'suz yürütülebilir; karar yolu LLM içermiyor.
5. Ürün mesajı net: "Uyarlamalı ama düşürülemez."

**Hangi rakiplere karşı test edilecek:**

| Tür | Rakip | Nasıl |
|---|---|---|
| Akademik | VP-Control tarzı portföy (B5) | Makaledeki tasarımın yeniden uygulanması; aynı senaryolar + downgrade saldırıları |
| Akademik | Progent / Cedar tarzı sabit politika (B1) | Deterministik kural tabanı |
| Akademik | LLM hakemi (B2) — MELON/Task Shield sınıfı yaklaşımların temsilcisi | Aynı kanıtla LLM kararı |
| Ticari (yaklaşık) | AWS AgentCore Policy davranışı | B1 içinde Cedar ile modellenir (AWS hizmeti çalıştırılmadan) |
| Ticari (yaklaşık) | OpenAI Agents SDK `needs_approval` | B1 + parametre eşiğine göre REVIEW |
| İç | B3 (sabit tam doğrulama), B4-naif | H1a, H1b |

**Hangi koşullarda başarısız sayılacak:** 06 §8'deki dört koşul. Kısaca: B4, saldırı altında B3'ten 1 puandan fazla kötü UAER verirse, maliyet tasarrufu anlamlı değilse ya da biçimsel önerme (H1c) tasarım düzeyinde ihlal edilirse.

---

## 9. bölümdeki sorulara açık cevaplar

**1. VERIQEN mevcut haliyle yeterince özgün mü?**
**Hayır.** Çekirdek hipotez VP-Control ile büyük ölçüde örtüşüyor. Yetki katmanı Progent/CaMeL/AgentCore Policy ile, insan onayı yönlendirmesi OpenAI/LangChain SDK'ları ile örtüşüyor.

**2. Değilse hangi teknik mekanizması değiştirilmeli?**
"Riske göre ek doğrulama seçimi" mekanizması **katkı olmaktan çıkıp araştırma nesnesine** dönüşmeli. Değişiklikler:
- (a) Yönlendiricinin girdileri tip düzeyinde `TrustedFeature` ile sınırlandırılmalı.
- (b) Her işlem sınıfı için monoton zorunlu taban tanımlanmalı.
- (c) Güvenilmeyen kanal değişimine karşı kararlılık kontrolü eklenmeli.
- (d) Değerlendirmeye **uyarlamalı downgrade saldırgan protokolü** eklenmeli.

Ayrıca hipotez metni (`docs/evaluation-plan.md`) H1 olarak yeniden yazılmalı ve orijinal hipotez H3 (tekrar) olarak korunmalı.

**3. En yakın üç akademik rakip:**
1. **VP-Control** — Engineering Reliable Commit Gates for Agentic AI (arXiv:2609.10969)
2. **Progent** — Programmable Privilege Control for LLM Agents (arXiv:2504.11703)
3. **Agent-Sentry** — Bounding LLM Agents via Execution Provenance (arXiv:2603.22868)

Yakın takipçiler: CausalArmor (ICML 2026), PACT (arXiv:2605.11039), CaMeL.

**4. En yakın üç ticari rakip:**
1. **AWS Bedrock AgentCore Policy** (Cedar ile araç çağrısı öncesi deterministik yetkilendirme)
2. **Invariant Guardrails / Snyk** (araç çağrısı yakalama + iz üzerinde veri akışı kuralları)
3. **OpenAI Agents SDK** (tool guardrails + çağrı başına koşullu `needs_approval`)

**5. Önerilen yöntem hangi metrikte avantaj sağlayabilir?**
Beklenen (hedef): **Downgrade-ASR** ve saldırı altındaki **UAER**'da naif uyarlamalı sistemlere ve muhtemelen VP-Control tarzı portföye karşı. Zararsız trafikte **doğrulama maliyetinde** sabit tam doğrulamaya (B3) karşı. B3'e karşı güvenlikte **üstünlük değil, eşdeğerlik** hedefleniyor; bu iddia buna göre kurulmalı.

**6. Hangi koşullarda başarısız olabilir?**
- Güvenilir özellikler riski ayırt etmeye yetmezse, uyarlamalılığın maliyet kazancı kaybolur (H1b-2 reddi).
- Naif uyarlamalı sistem de saldırıya dayanıklı çıkabilir; bu durumda tehdit pratikte önemsizdir (H1a reddi).
- "Güvenilir" sayılan bir özellik dolaylı olarak saldırgan etkisinde olabilir (ör. ajanın seçtiği sipariş kimliği). Bu, garantiyi bozar.
- Kaynak sistemde sürüm/tazelik alanı yoksa G tabanı kurulamaz.
- Saldırılar zayıf tasarlanırsa sonuç yanlış güvence verir.

**7. Gerçek hayatta kimler kullanabilir?**
Müşteri hizmetleri ajanıyla iade/iptal yapan e-ticaret ve abonelik şirketleri; ödeme ve muhasebe kaydı yapan fintech ajanları; altyapı işlemi yapan (yeniden başlatma, IAM değişikliği) DevOps ajanları; uyarlamalı guardrail ürünü geliştiren güvenlik firmaları (tehdit modeli ve test aracı olarak).

**8. İki GPU'suz bilgisayarla geliştirilebilir mi?**
**Evet.** Karar motoru LLM içermiyor. LLM ihtiyacı (ajan, B2 hakemi, saldırgan) API ile karşılanır. Dondurulmuş yörünge yöntemiyle API maliyeti kontrol edilebilir. Windows'ta WSL2 önerilir (bkz. 05).

**9. 25 Kasım'daki proje fikri başvurusu için bilimsel temel yeterince güçlü mü?**
**Revizyonla evet, mevcut hâliyle hayır.** Başvuru metni (a) VP-Control'ü en yakın çalışma olarak açıkça anar, (b) katkıyı "uyarlamalı doğrulamanın saldırgana karşı dayanıklılığı" olarak konumlandırır ve (c) sonuçları **hipotez** olarak sunarsa, bir proje *fikri* başvurusu için savunulabilir bir temel oluşur. Henüz deney sonucu yok; başvuruda sonuç iddiası olmamalı.

**10. Başvurudan önce mutlaka giderilmesi gereken eksikler:**

| # | Eksik | Neden kritik | Tahmini süre |
|---|---|---|---|
| 1 | Aday F için **hedefli ek literatür taraması** ("adaptive guardrail evasion", "verification downgrade", "routing attack" + "agent tool authorization"; ICML/NeurIPS/USENIX/CCS 2026 bildiri listeleri) | Özgünlük iddiasının tek dayanağı; 2026'da alan çok hızlı ilerliyor | 1 gün |
| 2 | VP-Control, PACT, Agent-Sentry ve FinHarness'in **tam metinlerinin** okunması (yöntem, deney ve sınırlılık bölümleri) | PACT ve Agent-Sentry sayıları ikincil kaynaktan geldi; FinHarness hiç ayrıntılı okunmadı | 1 gün |
| 3 | Repodaki `evaluation-plan.md` hipotezinin H1/H2/H3 yapısına göre güncellenmesi | Başvuru metni ile repo tutarlı olmalı | 2 saat |
| 4 | Asgari demo: 3 senaryo (ALLOW/REVIEW/BLOCK) + 1 downgrade saldırı senaryosunun yerelde uçtan uca çalışması | "Fikir"in uygulanabilir olduğunu göstermek | 2–3 gün |
| 5 | Danışmanla F'nin tehdit modelinin (saldırganın neyi kontrol ettiği) yazılı olarak netleştirilmesi | Hakem ilk olarak bunu sorar | 1 görüşme |

---

## Görev tamamlanma durumu

### Tamamlanan
- Yönergedeki 5 başlığın bibliyografik kontrolü (IPIGuard++ bulunamadı; FAVA farklı konuda).
- 30 akademik çalışmanın taranması ve VERIQEN ile ilişkilendirilmesi (24'ü ayrıntılı tabloda).
- 13 ticari/açık kaynak çözümün resmî dokümantasyondan incelenmesi ve karşılaştırma matrisi.
- 7 özgünlük adayının (A–G) 10 soru ve öznel puanla değerlendirilmesi; en güçlü üç adayın seçilmesi.
- Üç aday için yanlışlanabilir hipotezler, fizibilite, deney protokolü, metrik tanımları ve istatistik planı.
- Gerçek sonuçlar ile hedeflerin ayrı tablolarda sunulması.
- Nihai karar (REVISE) ve 10 sorunun yanıtları.

### Kısmen tamamlanan
- **Sayısal sonuç doğrulaması:** AgentDojo, MELON, IPIGuard, VP-Control ve LlamaFirewall tablo düzeyinde; CaMeL, Progent, AgentSpec ve CausalArmor metin/kısmi tablo düzeyinde doğrulandı. PACT, Agent-Sentry ve ToolEmu'nun bir kısmı ikincil kaynaktan; ASB, FIDES, KnowNo ve Prompt Infection için sayısal değer çıkarılamadı.
- **Rakip özellikleri:** Belgelerde bulunamayan özellikler "doğrulanamadı" olarak bırakıldı. Ürünler bizim tarafımızdan çalıştırılmadı.
- **Özgünlük boşluğu (Aday F):** Ön tarama düzeyinde; "literatürde yok" kesinliğinde değil.

### Tamamlanamayan
- ~~GitHub'a yazma~~ → Dosyalar `research/adversarial-routing` dalına yüklendi (PR #1).
- CausalArmor'ın AgentDojo sonuç tablosu (Tablo 3) erişilen metinde yer almadığı için okunamadı.
- Ödeme dışındaki alanlarda (DevOps, sağlık erişim kontrolü) kullanıcı ihtiyacı doğrulaması (görüşme/anket) yapılmadı.
