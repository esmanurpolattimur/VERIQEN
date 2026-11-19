# 03 — Özgünlük ve Araştırma Boşluğu Analizi

**Tarih:** 16 Kasım 2026 (yönergedeki 18 Kasım görevi)
**Girdi:** 01 (literatür, 30 çalışma) ve 02 (13 rakip)

> **Puanlama uyarısı:** Bu belgedeki tüm puanlar **öznel uzman değerlendirmesidir.** Bilimsel bir ölçüm değildir. Gerekçeler ayrıca yazıldı; başka bir değerlendirici farklı puan verebilir.

---

## 1. Mevcut VERIQEN önerisinin durumu

Repodaki `docs/evaluation-plan.md` hipotezi şöyle:

> "Yetki ve zorunlu kanıt denetimini sabit tutup ek doğrulamayı işlem riskine göre seçmek, her vakada aynı ek kontrolleri çalıştıran bir politikaya kıyasla güvensiz işlemlerin yürütülme oranını artırmadan doğrulama yükünü azaltabilir."

**Bulgu:** Bu hipotez, **VP-Control** (arXiv:2609.10969, Eylül 2026) tarafından büyük ölçüde test edilmiş durumda:

| VERIQEN unsuru | VP-Control karşılığı |
|---|---|
| Riske göre ek doğrulama seçimi | Gözlemlenebilir üst veriye (kanıt yaşı, kaynak sağlığı, guard varlığı, etki alanı, geri alınabilirlik) göre 37 plan arasından seçim yapan portföy denetleyicisi |
| Sabit ek doğrulamaya karşı maliyet tasarrufu | Eşit bütçeli karşılaştırmalar: bağımsız kaynakla aynı bütçede güvensiz yürütme %16.5 → %5.7 |
| Kanıt güvenilirliği / bağımsızlık | Kanıt soyu (lineage); aynı kaynaktan beslenen doğrulayıcıların birlikte yanılması |
| Yürütme anında kanıt tazeliği | Kontrol sonrası yarış durumu ve atomik transactional guard |
| Yinelenen istek | İdempotent istek kimliği |
| İnsan incelemesi | İnsana erteleme (deferral) |

**Sonuç:** VERIQEN mevcut hâliyle bu hipotezi yeni bir katkı olarak sunarsa, hakem büyük olasılıkla "VP-Control'ün yeniden adlandırılmış hâli" ya da "farklı alanda tekrarı (replication)" değerlendirmesi yapar. Bu durum, VERIQEN'in **değersiz olduğu** anlamına gelmez; **özgünlük iddiasının yer değiştirmesi gerektiği** anlamına gelir.

VP-Control'ün kendi belirttiği sınırlar VERIQEN için açık alan bırakıyor:

- Saldırgan yazarlar, **sahte köken (forged provenance)** ve uzun ufuklu ajanlar değerlendirilmemiş.
- Görülmemiş arıza ailelerinde kalibrasyon bozuluyor (%5 hedefe karşı %26'ya kadar).
- Tek domain (altyapı işlemleri); FinQA'da ana etki tekrarlanmamış.

---

## 2. Aday değerlendirmeleri

Her aday için yönergedeki 10 soru yanıtlandı. Ardından 100 üzerinden öznel puan verildi.

### Aday A — Kanıt güvenilirliğine göre uyarlamalı doğrulama

1. **Problem:** Her işlemde aynı pahalı doğrulamayı çalıştırmak hem gecikme hem maliyet üretiyor.
2. **En yakın yöntem:** VP-Control (portföy denetleyicisi), FinHarness (risk window), Agent-Sentry (ucuzdan pahalıya katmanlar), CausalArmor (seçici temizleme).
3. **Neden yetersiz:** Yetersiz değil. VP-Control kanıt yaşı ve kaynak sağlığına göre seçimi zaten yapıyor. Tek eksik: saldırgan ortam ve farklı domain.
4. **Yeni mekanizma:** Ayrı bir mekanizma önerilmiyor; yalnızca iade/ödeme alanına uygulanıyor.
5. **Yalnızca birleştirme mi?** Evet.
6. **Yeni karar algoritması veya optimizasyon problemi?** Hayır (VP-Control'ün amaç fonksiyonu ile aynı biçim).
7. **Hipotez:** Bkz. 04, H3 (tekrar/replikasyon hipotezi olarak).
8. **Baseline:** B3 (sabit tam doğrulama), VP-Control tarzı portföy.
9. **GPU'suz geliştirilebilir mi?** Evet.
10. **Ürünleşebilir mi?** Evet, ama rakiplerden farkı zayıf.

| Kriter | Puan | Gerekçe |
|---|---|---|
| Literatürden farklılaşma (30) | 7 | VP-Control ve FinHarness doğrudan örtüşüyor. |
| Deneysel doğrulanabilirlik (20) | 16 | Sentetik simülatör + τ-bench retail ile ölçülebilir. |
| Teknik uygulanabilirlik (20) | 18 | Kural motoru + birkaç doğrulayıcı; CPU yeterli. |
| Gerçek kullanıcıya fayda (20) | 13 | Maliyet azalır, ancak kullanıcı için asıl değer güvenlik. |
| Ürünleşme (10) | 6 | Rakip ürünlere kolayca eklenebilecek bir özellik. |
| **Toplam** | **60** | |

### Aday B — Güvenlik riski ve doğrulama maliyetini birlikte optimize eden karar mekanizması

1. **Problem:** Güvenlik ve maliyet arasındaki dengeyi açık bir hedef fonksiyonla kurmak.
2. **En yakın yöntem:** VP-Control (maliyet − kapsama + risk fiyatı × güvensiz oran), CTD (bütçe garantili delegasyon), LTT.
3. **Neden yetersiz:** VP-Control'ün kalibrasyonu yaklaşık; arıza ailesi değişince garanti bozuluyor. CTD tool-call yetkilendirmesi değil.
4. **Yeni mekanizma:** Kısıtlı optimizasyon: min E[maliyet], kısıt P(güvensiz ALLOW) ≤ α. Eşik konformal risk kontrolü ile ayarlanıyor.
5. **Yalnızca birleştirme mi?** Büyük ölçüde evet (CRC + VP-Control fikri).
6. **Yeni optimizasyon problemi?** Biçim yeni değil; uygulama alanı yeni.
7. **Hipotez:** "CRC ile kalibre edilmiş eşik, hedef α'yı test dağılımında tutar ve VP-Control tipi lookup tablosundan daha az erteleme üretir."
8. **Baseline:** VP-Control tarzı portföy, sabit eşik, LTT.
9. **GPU'suz?** Evet.
10. **Ürün?** Orta.

| Kriter | Puan | Gerekçe |
|---|---|---|
| Farklılaşma (30) | 8 | Aynı problem formu VP-Control'de var; istatistik araçları hazır. |
| Doğrulanabilirlik (20) | 16 | Kalibrasyon/test ayrımı ile net ölçülür. |
| Uygulanabilirlik (20) | 15 | İstatistiksel kalibrasyon dikkat ister; küçük örneklemde α ≤ %1 çözülemez (VP-Control de çözememiş). |
| Fayda (20) | 13 | Operasyon ekipleri için değerli ama dolaylı. |
| Ürünleşme (10) | 6 | |
| **Toplam** | **58** | |

### Aday C — Çoklu ajanlarda kanıt kökeni ve bağımlılık takibi

1. **Problem:** Bir ajanın çıktısı diğerine "kanıt" olarak geçtiğinde güven zinciri kopuyor (Prompt Infection).
2. **En yakın yöntem:** ARM (köken grafiği + reddedilen eylemler), AuthGraph (köken ve yetki grafiği), Agent-Sentry (tek ajan köken grafiği), FIDES/RTBAS (etiket yayılımı), Prompt Infection'daki LLM Tagging.
3. **Neden yetersiz:** Çoğu tek ajanlı; çoklu ajanlarda dış kanıt kaynağına kadar uzanan uçtan uca köken zinciri bu taramada bulunamadı. Ancak 2026'da bu alanda yayın yoğunluğu hızla artıyor.
4. **Yeni mekanizma:** Ajanlar arası mesajlara imzalı kanıt referansları; bir ajanın beyanı ancak güvenilir kaynağa uzanan bir zincir varsa kanıt sayılıyor.
5. **Yalnızca birleştirme mi?** Kısmen (IFC + imzalı kanıt).
6. **Yeni algoritma?** Orta (güven yayılımı kuralları).
7. **Hipotez:** "Uçtan uca köken zinciri, ajan beyanını kanıt sayan sisteme göre çoklu ajanlı enjeksiyonda UAER'ı düşürür."
8. **Baseline:** Etiketsiz çoklu ajan, LLM Tagging, tek ajan IFC.
9. **GPU'suz?** Evet, ama çoklu ajan deneyleri API maliyetini katlar.
10. **Ürün?** Gelecekte güçlü; bugün pazar erken.

| Kriter | Puan | Gerekçe |
|---|---|---|
| Farklılaşma (30) | 14 | Boşluk var ama hızla kapanıyor (ARM, AuthGraph 2026). |
| Doğrulanabilirlik (20) | 10 | Standart çoklu ajan güvenlik benchmark'ı zayıf; kendi benchmark'ını kurmak gerekir. |
| Uygulanabilirlik (20) | 10 | 2 kişilik ekip için kapsam büyük. |
| Fayda (20) | 12 | |
| Ürünleşme (10) | 6 | |
| **Toplam** | **52** | Yönergeye uygun olarak "gelecek aşama" kalmalı. |

### Aday D — İşlem riskine göre insan onayına yönlendirme

1. **Problem:** Her işlemde onay istemek onay yorgunluğu yaratıyor; hiç istememek tehlikeli.
2. **En yakın yöntem:** OpenAI Agents SDK (`needs_approval` fonksiyonu), LangChain HITL (`when` yüklemi), AgentSpec (`user_inspection`), RTBAS, CaMeL, TBAC (risk + belirsizlik → insan), KnowNo.
3. **Neden yetersiz:** Ürünlerde **özellik** olarak hazır; akademide RTBAS ve KnowNo var.
4. **Yeni mekanizma:** Yok (eşik kuralı).
5. **Yalnızca birleştirme mi?** Evet.
6. **Yeni algoritma?** Hayır.
7. **Hipotez:** Yalnızca mühendislik doğrulaması olarak test edilebilir.
8. **Baseline:** Her zaman onay, hiç onay yok, sabit tutar eşiği.
9. **GPU'suz?** Evet.
10. **Ürün?** Evet, ama farklılaşmıyor.

| Kriter | Puan | Gerekçe |
|---|---|---|
| Farklılaşma (30) | 3 | Ticari SDK'larda hazır. |
| Doğrulanabilirlik (20) | 14 | İnsan simülasyonu gerekir; gerçek insanla ölçmek zor. |
| Uygulanabilirlik (20) | 19 | Çok kolay. |
| Fayda (20) | 15 | Kullanıcı için somut. |
| Ürünleşme (10) | 7 | |
| **Toplam** | **58** | Bilimsel katkı olarak sunulmamalı; ürün özelliği olarak kalmalı. |

### Aday E — Güvenlik kontrollerinin belirsizlik ve bütçe kısıtına göre seçilmesi

1. **Problem:** Doğrulayıcı çağrı bütçesi sınırlıyken hangi işlemlerin pahalı doğrulamaya gideceği.
2. **En yakın yöntem:** CTD (risk ve bütçe garantili kademeli yapı), KnowNo, Conformal Risk Control, VP-Control (Wilson + fixed-sequence), TBAC (öz-belirsizlik eşiği).
3. **Neden yetersiz:** CTD içerik izliyor, araç çağrısını yetkilendirmiyor. TBAC deneysiz. VP-Control'ün garantisi yaklaşık. **Hepsi i.i.d./değiş tokuş edilebilirlik varsayıyor**; saldırgan bu varsayımı bozar.
4. **Yeni mekanizma:** Araç çağrısı yetkilendirmesi için bütçe garantili delegasyon.
5. **Yalnızca birleştirme mi?** Büyük ölçüde (CTD'nin alan aktarımı).
6. **Yeni optimizasyon?** Alan aktarımı.
7. **Hipotez:** "Bütçe α_B altında, DV tabanlı seçim belirsizlik top-k'dan daha düşük UAER verir."
8. **Baseline:** Belirsizlik top-k, rastgele seçim (eşit bütçe), VP-Control.
9. **GPU'suz?** Gizil prob gerektirmeyen sürümü evet. CTD'nin gizil prob sürümü küçük modelle CPU'da mümkün ama yavaş.
10. **Ürün?** Orta.

| Kriter | Puan | Gerekçe |
|---|---|---|
| Farklılaşma (30) | 10 | Yöntem hazır; alan aktarımı. |
| Doğrulanabilirlik (20) | 15 | |
| Uygulanabilirlik (20) | 14 | Kalibrasyon için çok sayıda etiketli vaka gerekir. |
| Fayda (20) | 12 | |
| Ürünleşme (10) | 6 | |
| **Toplam** | **57** | |

### Aday F (yeni) — Manipülasyona dayanıklı risk-uyarlamalı doğrulama ("downgrade-resistant adaptive verification")

1. **Problem:** Uyarlamalı doğrulama sistemleri, ucuz yola mı pahalı yola mı gidileceğine **özelliklere (features)** bakarak karar veriyor. Bu özelliklerin bir kısmı ajanın beyanından ya da güvenilmeyen içerikten etkilenebiliyorsa, saldırganın hedefi işlemi engelletmek değil, **işlemin hafif doğrulama yoluna yönlendirilmesini** sağlamak olur. Buna "doğrulama düşürme saldırısı" (verification downgrade) denebilir. Uyarlamalılık, maliyet kazandırırken yeni bir saldırı yüzeyi açar.
2. **En yakın yöntem:** VP-Control (saldırganı kapsam dışı bırakıyor), CausalArmor (uyarlamalı saldırganlara karşı tek başına önerilmiyor), Agent-Sentry (ilk katman "Allow" derse LLM hakemine gidilmiyor), TBAC (risk puanını LLM hesaplıyor ve yazarlar bunun manipüle edilebileceğini kabul ediyor). Diğer alanlarda kademeli LLM'lerin saldırı altında kırılganlığı (2605.17288) ve yönlendirici saldırıları (RerouteGuard) gösterilmiş.
3. **Neden yetersiz:** Bu taramada, **araç çağrısı yetkilendirmesinde** risk-uyarlamalı doğrulama yönlendiricisini hedef alan bir tehdit modeli ve bu modele karşı garanti veren bir tasarım bulunamadı.
4. **Yeni mekanizma (öneri):**
   - **(i) Güvenilir özellik kısıtı:** Yönlendirici yalnızca güvenilir kaynaklardan hesaplanan özellikleri kullanır: sunucu tarafı kimlik, sistemden okunan tutar, politika sürümü, kaynak sağlığı, geri alınabilirlik. Ajanın beyan ettiği değerler ve güvenilmeyen içerikten türeyen sinyaller yönlendirmeye girmez.
   - **(ii) Monoton güvenlik tabanı:** Yönlendiricinin seçtiği plan, işlem sınıfının zorunlu tabanından **asla daha zayıf olamaz.** Uyarlamalılık yalnızca tabanın **üstüne** ek doğrulama ekleyebilir.
   - **(iii) Kararlılık kontrolü:** Aynı işlem için, güvenilmeyen girdi parçaları değiştirildiğinde yönlendirme kararı değişiyorsa, bu durum bir yükseltme sinyali sayılır.
   - **(iv) Uyarlamalı saldırgan protokolü:** Yönlendiriciyi açıkça hedef alan saldırılar (özellik manipülasyonu, eşik sondalama, kaynak sağlığını bozarak "degraded → ucuz yol" tetikleme, DoS ile zaman aşımı) üretilir ve ölçülür.
5. **Yalnızca birleştirme mi?** Hayır. Katkı yeni bir **tehdit modeli + ölçüt (downgrade ASR) + tasarım kısıtı + garanti** dörtlüsü. Bileşenler (taint, politika tabanı) bilinen yapılar, ancak uyarlamalı doğrulama yönlendirmesine uygulanması ve ölçülmesi yeni görünüyor.
6. **Yeni karar algoritması / optimizasyon?** Evet: kısıtlı politika sınıfı. Yönlendirme fonksiyonu, güvenilir özellik alt uzayında ve monoton taban kısıtı altında maliyeti minimize ediyor. Biçimsel bir önerme kurulabilir: "Saldırgan yalnızca güvenilmeyen kanalları kontrol ediyorsa, yönlendirme kararı saldırgandan bağımsızdır; dolayısıyla UAER, taban politikanın UAER'ından büyük olamaz." Bu önerme ispatlanabilir ve deneyle sınanabilir.
7. **Hipotez:** Bkz. 04, H1.
8. **Baseline:** B3 (sabit tam doğrulama), naif uyarlamalı (ajan beyanı ve içerik sinyali dahil özelliklerle), VP-Control tarzı portföy, B2 (LLM hakemi).
9. **GPU'suz?** Evet. Yönlendirici kural/istatistik tabanlı; saldırı üretimi API LLM ile yapılır.
10. **Ürün?** Evet. "Uyarlamalı ama düşürülemez doğrulama" güvenlik ekipleri için anlaşılır bir değer önerisi.

| Kriter | Puan | Gerekçe |
|---|---|---|
| Farklılaşma (30) | 17 | VP-Control'ün açıkça bıraktığı boşluk. Ek taramada (09) tehdidin taksonomide adlandırıldığı ve güvenilir kaynaklı risk / deterministik taban ilkelerinin başka çalışmalarda geçtiği görüldü; 20'den 17'ye düşürüldü. Deneysel ölçüm ve garanti hâlâ bulunamadı. |
| Doğrulanabilirlik (20) | 16 | Downgrade ASR, UAER ve maliyet net tanımlanabiliyor; sentetik + AgentDojo Banking. |
| Uygulanabilirlik (20) | 16 | Uyarlamalı saldırı üretimi emek ister; API maliyeti sınırlı. |
| Fayda (20) | 15 | Uyarlamalı guardrail kullanan herkes için ilgili bir tehdit. |
| Ürünleşme (10) | 7 | |
| **Toplam** | **71** | (ek tarama sonrası; önceki 74) |

### Aday G (yeni) — Argüman düzeyinde kanıt bağlama + yürütme anı tazelik (TOCTOU) denetimi

1. **Problem:** Karar anında doğru olan kanıt, yürütme anında eskimiş olabilir (sipariş durumu değişmiş, iade zaten yapılmış). Ayrıca kanıt **işlemin tamamına** değil, **yetki taşıyan argümana** (tutar, alıcı, sipariş kimliği) bağlanmalı.
2. **En yakın yöntem:** PACT (argüman rolü + köken sözleşmesi), VP-Control (atomik guard, kontrol sonrası yarış), Claws in Plain Sight (onayın çağrı özetine bağlanması), Progent (argüman düzeyinde politika).
3. **Neden yetersiz:** PACT kökeni izliyor ama dış kaynak tazeliğini ve yürütme anında yeniden doğrulamayı ele almıyor. VP-Control yarış durumunu ele alıyor ama argüman rollerini ve saldırgan kökeni değil. Birleşimi VERIQEN mimarisinde (`docs/architecture.md`, "Yürütme sınırı") zaten taslak hâlinde var.
4. **Yeni mekanizma:** Her yetki taşıyan argüman için `(değer, kaynak, kaynak_sürümü, zaman damgası)` kanıt kaydı tutulur. Yürütücü, yazma işlemiyle aynı işlem (transaction) içinde kaynak sürümünü tekrar kontrol eder. İnsan onayı bu kayıtların özetine (hash) bağlanır; parametre değişirse onay geçersiz olur.
5. **Yalnızca birleştirme mi?** Büyük ölçüde evet (PACT + VP-Control atomik guard + onay bağlama).
6. **Yeni algoritma?** Hayır; sistem tasarımı.
7. **Hipotez:** Bkz. 04, H2.
8. **Baseline:** B3 (yalnızca karar anında kontrol), PACT tarzı yalnız köken kontrolü.
9. **GPU'suz?** Evet; LLM bile gerekmez.
10. **Ürün?** Evet; ödeme/iade gibi alanlarda çok somut.

| Kriter | Puan | Gerekçe |
|---|---|---|
| Farklılaşma (30) | 11 | Parçaları literatürde var. |
| Doğrulanabilirlik (20) | 16 | Deterministik senaryolarla kesin ölçülür. |
| Uygulanabilirlik (20) | 18 | FastAPI + SQLite ile kolay. |
| Fayda (20) | 16 | Gerçek finansal hataları önler. |
| Ürünleşme (10) | 8 | |
| **Toplam** | **69** | |

---

## 3. Puan özeti (öznel)

| Aday | Farklılaşma (30) | Doğrulanabilirlik (20) | Uygulanabilirlik (20) | Fayda (20) | Ürünleşme (10) | **Toplam** |
|---|---|---|---|---|---|---|
| **F — Manipülasyona dayanıklı uyarlamalı doğrulama** | 17 | 16 | 16 | 15 | 7 | **71** |
| **G — Argüman düzeyinde kanıt + yürütme anı tazelik** | 11 | 16 | 18 | 16 | 8 | **69** |
| **A — Kanıt güvenilirliğine göre uyarlamalı doğrulama** | 7 | 16 | 18 | 13 | 6 | **60** |
| B — Risk–maliyet ortak optimizasyonu | 8 | 16 | 15 | 13 | 6 | 58 |
| D — Riske göre insan onayı | 3 | 14 | 19 | 15 | 7 | 58 |
| E — Belirsizlik/bütçe kısıtlı seçim | 10 | 15 | 14 | 12 | 6 | 57 |
| C — Çoklu ajan kanıt kökeni | 14 | 10 | 10 | 12 | 6 | 52 |

## 4. Seçilen üç aday

1. **F (ana katkı adayı):** Tek başına literatürden ayrışma potansiyeli en yüksek aday.
2. **G (zorunlu taban):** F'nin "monoton taban" bileşeninin somut hâli. Bilimsel katkıdan çok sistemin güvenilirlik temeli.
3. **A (kontrol/tekrar deneyi):** VERIQEN'in orijinal fikri. VP-Control sonucunun farklı bir alanda (iade/ödeme) **tekrarı** olarak dürüstçe sunulmalı. F'nin "uyarlamalılık maliyet kazandırıyor" önkoşulunu da doğrular.

> B ve E, F'nin içinde **kalibrasyon yöntemi** olarak kullanılabilir (ör. eşiklerin konformal risk kontrolüyle ayarlanması), ancak ayrı katkı olarak sunulmamalı.

## 5. Aşırı genelleme kontrolü

| Risk | Önlem |
|---|---|
| "Literatürde yok" demek | Belgelerde "bu ön taramada bulunamadı" ifadesi kullanıldı. Başvurudan önce hedefli bir ek tarama zorunlu (bkz. 07). |
| F'nin yeniden adlandırma olması | F'nin bileşenleri (taint, politika tabanı) bilinen yapılar. Katkı, **uyarlamalı doğrulama yönlendirmesine özgü tehdit modeli ve ölçüt.** Bu ayrım her metinde açık yazılmalı. |
| VP-Control'ü görmezden gelmek | Her başvuru metninde VP-Control en yakın çalışma olarak açıkça anılmalı ve farkla birlikte konumlandırılmalı. |
