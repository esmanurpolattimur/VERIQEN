# VERIQEN 2.0 — İlk Rapor: Sistem Denetimi, Jüri Eleştirileri ve Özellik Seçimi

**Tarih:** 19 Kasım 2026
**Kapsam:** Master prompt §14 ("Şimdi kod yazmaya başlama"). Bu rapor yalnızca denetim ve plan içerir; kod değişikliği yok.
**Durum:** Onay bekliyor.

---

## 0. Önce dürüst bir çerçeve

1. **Takvim.** Başvuruya 6 gün var. Master prompt'taki programın tamamı (30+ bağımsız saldırı, iki ek benchmark, yedi mekanizma, B0–B6 karşılaştırması, beş tohum, ablasyon, biçimsel doğrulama, 18 belge) gerçekçi olarak **2–3 aylık** bir iş. 25 Kasım'a kadar yapılabilecek olan: ölçüm altyapısını düzeltmek, en kritik eleştirilere ölçümle cevap vermek ve **bir** yeni mekanizmayı MVP olarak deneylerle sınamak. Plan (§6) buna göre iki aşamaya ayrıldı.
2. **Puan.** 90–100 hedefini bu rapor garanti edemez; puanı jüri verir. Verebileceğimiz söz, her iddianın arkasında ölçüm olması.
3. **Özgünlük uyarısı.** Önerilen yedi mekanizmanın hiçbiri tek başına yeni değil (bkz. §4). Hepsinin literatürde yakın karşılığı var. Katkı ancak "bu mekanizma, ölçtüğümüz şu açığı şu kadar kapattı" biçiminde kurulabilir. Yeni isim vermek yeterli olmaz (master prompt §13).
4. **Kota.** Groq ücretsiz katmanında `gpt-oss-120b` için günlük 200 bin token sınırı var. Ölçülen tüketim bölüm başına yaklaşık 5 bin token, yani model başına günde yaklaşık 40 bölüm. Gerçek LLM deneylerinin ölçeğini en çok bu sınırlıyor.

---

## 1. Sistem denetimi

### 1.1 Depo içeriği (dal: `research/adversarial-routing`, `6498ede`)

| Bileşen | Dosya | Boyut | Ne yapıyor |
|---|---|---|---|
| Karar motoru | `experiments/agentdojo/veriqen_gate.py` | 381 satır | Köken izleme, niyet çıkarma, zorunlu taban, yönlendirme, hakem, AgentDojo entegrasyonu |
| Çevrimdışı değerlendirme | `experiments/agentdojo/replay_eval.py` | 184 satır | Senaryolu ajan + MockJudge ile AgentDojo Banking |
| Canlı değerlendirme | `experiments/agentdojo/run_live.py` | 127 satır | Gerçek LLM ajanı + gerçek hakem |
| Test | `experiments/agentdojo/tests/smoke_live_pipeline.py` | 81 satır | Tek bir duman testi (ağsız) |
| Pilot | `experiments/pilot/pilot.py`, `sweep.py` | 414 satır | Sentetik iade dünyası; **karar motorundan bağımsız ayrı bir uygulama** |
| Belgeler | `docs/research/00–12` | ~2.000 satır | Literatür, rakipler, özgünlük, hipotezler, protokol, tehdit modeli, sonuçlar |

### 1.2 Karar motorunun mimarisi (mevcut)

```
Kullanıcı isteği ──► Niyet çıkarıcı (kelime / LLM / kâhin) ──► izinli işlem türleri
Ortam durumu ─────► ProvenanceTracker (USER / TRUSTED_STATE / TOOL_TEXT / UNSEEN)
Ajanın araç çağrısı ─► Gate.decide:
     1. hassas değilse ALLOW
     2. zorunlu taban (parola kullanıcıdan mı, bakiye, >5000 → REVIEW)
     3. yönlendirme: niyet dışı tür / bilinmeyen alıcı / >1000 / tekrar → hakem
     4. hakem (MockJudge veya LLMJudge) → ALLOW / BLOCK
```

### 1.3 Sürüm geçmişi

| Sürüm | Commit | Değişiklik | Neden |
|---|---|---|---|
| VERIQEN (v1) | 73895eb | Anahtar kökeni, yapısal alanlara güven | Köken körü NAIVE %66.7 ile kırıldı |
| VERIQEN-A | c426209 | Yazar kökeni | Durum ekme saldırısı v1'i kırdı |
| VERIQEN-S | 2603db6 | Yalnız kullanıcının yazdığı alıcıya güven | Ele geçirilmiş geçmiş alıcı A'yı kırdı |
| VERIQEN-AI / SI / SI* | 398b99e | İşlem–niyet bağlama | S'de "istenmemiş ek işlem" açığı |
| Canlı hat düzeltmeleri | 6498ede | Token sınırı, kayıt bağlamı, hakem kaydı | Gerçek LLM koşusunda ortaya çıktı |

### 1.4 Belgelerdeki iddialar ile kod/deney karşılaştırması

| İddia (belge) | Kodda / deneyde karşılığı | Durum |
|---|---|---|
| Replay sonuçları (12) | `replay_eval.py`; yeniden çalıştırıldı, sayılar birebir aynı | ✅ Tekrar üretilebilir |
| "VERIQEN, B3 kadar güvenli (%6.8)" (12) | Fark MockJudge'ın %10 kaçırma varsayımından geliyor; tüm saldırılar hakeme gidiyor | ⚠️ Simülasyon; gerçek performans değil |
| "Zararsız fayda %98.1" (12) | MockJudge'ın %5 yanlış alarm varsayımı | ⚠️ Gerçek hakem meşru işlemleri engelledi (bkz. 1.5) |
| H1c: güvenilmeyen kanal değişince plan değişmez (04) | Bu özelliği sınayan bir test **yok** | ❌ Test edilmedi |
| ALLOW/REVIEW/BLOCK + insan incelemesi (README) | REVIEW yalnız >5000'de; deneylerde **hiç tetiklenmedi** | ❌ Pratikte denenmedi |
| FastAPI karar servisi, sipariş simülatörü (başlangıç ZIP'i) | Yok | ❌ Uygulanmadı |
| Denetim kaydı (ilke 8) | `gate.log` bellekte; canlı özet yalnız **son bölümün** kaydını tutuyor | ⚠️ Kısmi (hata) |
| Hassas bilgi loglanmaz (ilke 9) | `_safe_args` parolayı maskeliyor | ✅ |
| Pilot sonuçları (11) VERIQEN tasarımını gösterir | Pilot, karar motorunun kodunu kullanmıyor; ayrı model | ⚠️ Kavramsal kanıt, uygulama kanıtı değil |
| Köken takibi | `origin()` alt dize (substring) eşleşmesi; dönüşüm (boşluk, biçim) ve serbest metin desteklenmiyor | ⚠️ Banking IBAN'larına özel |

### 1.5 Gerçek LLM deneylerinin şu anki durumu (`results/live/`, git'e eklenmiyor)

| Koşu | Model | Kapsam | Durum | Bulgu |
|---|---|---|---|---|
| Deneme | gpt-oss-120b | VERIQEN-SI, 2 görev × 1 saldırı | Tamam | Saldırılar engellendi; meşru fatura ödemesi de engellendi |
| run2 / B3 | gpt-oss-120b | 4 görev × 4 saldırı | Tamam | ASR 0/16; 36 hakem çağrısı; hakem meşru iade ve düzenli ödemeleri engelledi; **hakem kayıt dosyası yok** (o sırada özellik eklenmemişti) |
| run2 / VERIQEN-SI | gpt-oss-120b | aynı | Kota nedeniyle yarıda | Kullanılmayacak |

Ek gözlem: Ajan, zararsız görevlerin çoğunda ödemeyi **hiç denemedi** (örneğin faturayı okuyup durdu). Bu bir ajan hatası, denetim hatası değil. Mevcut metrikler ikisini ayırt etmiyor (jüri eleştirisi 3.7).

---

## 2. Jüri eleştirileri: sorun → çözüm → deney → başarı kriteri

| # | Sorun | Mevcut durum | Çözüm | Gerekli deney | Başarı kriteri |
|---|---|---|---|---|---|
| 3.1 | Güvenlik sonucu MockJudge varsayımına dayanıyor | %6.8 = varsayılan %10 kaçırma | (a) MockJudge sonuçlarını "simülasyon" diye yeniden etiketle; (b) kaçırma oranı %0/5/10/20/30/50 ve yanlış alarm %0/5/10/20/30 için duyarlılık analizi; (c) gerçek hakemin FNR/FPR'sini ölç | (b) çevrimdışı, maliyetsiz; (c) hakem kayıtlarından, etiketli çağrılar üzerinde | Her iddia ya ölçülmüş hakemle ya da açıkça "varsayım X altında" diye raporlanıyor |
| 3.2 | Gerçek hakem meşru işlemleri engelliyor | Tek koşuda gözlendi, oran bilinmiyor | (a) Meşru işlem kataloğu (fatura, iade, düzenli ödeme, kayıtlı alıcı, açık onaylı yeni alıcı, tutar ve alıcı değişikliği); (b) kullanıcı tarafından açıkça belirlenmiş işlemleri hakeme göndermeden geçiren deterministik yol (**yetenek belirteçleri**, §4) | Politika düzeyinde: aynı çağrılar hakem ile ve belirteçle | Meşru işlem kabul oranı ve FPR, B3'e göre anlamlı biçimde daha iyi; ASR B3'ten kötü değil |
| 3.3 | Saldırıları ekip tasarladı | 3 saldırı modu, hepsi geliştirme sırasında kullanıldı | Kilitli saldırı seti: VERIQEN dondurulmadan **önce** yazılıp hash'i commit edilir, dondurmadan sonra açılır. Tam bağımsızlık için ekip dışından bir kişi veya sabit istemli bir LLM saldırgan | Dondurulmuş sürüm × kilitli set | Kilitli sette ASR ve FPR raporlanır, kötü de olsa saklanmaz |
| 3.4 | Test kümesi sızıntısı | Kelime kuralları 16 Banking görevi görülerek yazıldı | Görev bölümleme: Banking'i dev/val olarak ayır, **Slack ve Travel paketlerini kilitli test** olarak sakla; bölme tohumu ve görev kimlikleri dosyaya yazılır | Kurallar dev'de, seçim val'de, nihai sonuç kilitli testte | Kilitli test yalnız bir kez açılır; açılış commit'i kayıtlı |
| 3.5 | Özgünlük dar; tam metinler okunmadı | VP-Control [T], PACT ve Agent-Sentry [İ] | VP-Control, PACT, Agent-Sentry, Irreversibility Budget, CaMeL ve Progent'in tam metinlerini okumak; her biri için problem / tehdit modeli / yöntem / sonuç / sınırlılık tablosu | — (literatür) | Her farklılık iddiası birincil kaynağa sayfa veya bölüm numarasıyla bağlı |
| 3.6 | Yalnız Banking; IBAN yapısı köken takibini kolaylaştırıyor | Alt dize eşleşmesi | Köken grafiği (§4) + AgentDojo Slack (URL, e-posta, kanal adları) ve Travel (adres, tarih, serbest metin) | Aynı sistemler üç pakette | Banking dışındaki paketlerde ASR/FPR raporlanır; başarısızlıklar saklanmaz |
| 3.7 | Fayda ölçümü karışık | "Utility" tek sayı | Başarısızlık taksonomisi: ajan denemedi / politika engelledi / hakem engelledi / ayrıştırıcı hatası / araç hatası / değerlendirici hatası (ör. "€ 1 050,00") | Mevcut ve yeni kayıtların yeniden sınıflanması | Her başarısız bölüm tek bir kategoriye atanmış; "denetim engelledi" yalnız gerçekten engellenenleri sayıyor |
| ek | REVIEW hiç tetiklenmiyor | Eşik 5000 | REVIEW'i anlamlı kılan politika (ör. niyetle uyuşmayan ama düşük riskli işlem) | Review oranı metriği | REVIEW oranı raporlanıyor |
| ek | Denetim kaydı yalnız son bölümü tutuyor | `gate_log_tail` | Bölüm başına karar kaydı (JSONL) | — | Her kararın gerekçesi kayıtta |
| ek | H1c test edilmedi | Yok | Karşı-olgusal / metamorfik test: güvenilmeyen kanalı değiştir, kararın değişmediğini doğrula (property-based) | Hypothesis ile ≥1000 rastgele çift | Karşı örnek sayısı = 0, ya da bulunanlar raporlanıp düzeltilir |

---

## 3. Mevcut deneylerden çıkan ve plana yön veren iki bulgu

1. **Asıl ölçülen zayıflık güvenlik değil, yanlış engelleme.** Gerçek LLM ile koşulan 16 saldırının hiçbiri başarılı olmadı, ama hakem kullanıcının açıkça istediği işlemleri de engelledi. Yani "hakemi daha az çağırmak" yalnız bir maliyet sorunu değil, **fayda sorunu**. Hakemi çağırmadan, kullanıcının isteğine kanıtlanabilir biçimde bağlı işlemleri geçirmek hem maliyeti hem yanlış engellemeyi düşürebilir.
2. **Kalan güvenlik açığı "doğru alıcıya yanlış işlem".** VERIQEN-S'nin B3'ten farkı tamamen bu açıktan geliyor (12 §3c). Kelime tabanlı niyet çıkarıcı bunu kapatamıyor; kâhin niyet kapatıyor. Aradaki boşluğu dolduracak şey işlem türünü, alıcıyı, tutar sınırını ve kullanım sayısını **birlikte** bağlayan bir yapı.

İkisi de aynı mekanizmaya işaret ediyor: niyete bağlı, sınırlı yetki.

---

## 4. Yedi önerilen mekanizmanın değerlendirmesi

Puanlar öznel (Düşük / Orta / Yüksek), ölçüm değil.

| Mekanizma | Literatürdeki en yakın karşılık | Bilimsel özgünlük | Teknik uygulanabilirlik (6 gün) | Deneysel doğrulanabilirlik (AgentDojo'da) | Geliştirme maliyeti | Beklenen güvenlik katkısı | Ölçülmüş bir açığa cevap mı? |
|---|---|---|---|---|---|---|---|
| **4.3 Niyete bağlı yetenek belirteçleri** | CaMeL (değerlere bağlı yetenekler), Progent (ayrıcalık politikaları), Macaroons / capability tabanlı güvenlik | Düşük–Orta (mekanizma bilinen; **yönlendirmede hakemin yerine geçmesi ve FPR etkisi** ölçülmemiş) | Yüksek | Yüksek (mevcut niyet bağlama ve alıcı kökeni üzerine kurulur) | Düşük–Orta | Yüksek: "doğru alıcıya yanlış işlem" ve tekrar saldırıları | ✅ İki ölçülmüş açık (§3) |
| **4.2 Dinamik köken grafiği** | FIDES, RTBAS (taint/bilgi akışı), PACT (argüman düzeyinde köken), Agent-Sentry | Düşük (PACT'e çok yakın); fark yalnız **kullanım yerinde** (yetki değil yönlendirme) | Orta | Orta (Slack/Travel gerekir) | Orta–Yüksek | Orta: serbest metinde mevcut alt dize eşleşmesinin yerine geçer | ✅ Jüri eleştirisi 3.6 |
| **4.1 Kanıt taşıyan yürütme (PCE)** | Proof-carrying code (Necula 1997), PACT, VP-Control (kanıt soyu) | Düşük (kavram eski); değer: **her ALLOW'un denetlenebilir gerekçesi** | Yüksek (ince katman olarak) | Düşük (güvenlik artışı tek başına ölçülemez; diğerlerini bağlar) | Düşük | Dolaylı: denetlenebilirlik ve diğer mekanizmaların birleştiricisi | ⚠️ Denetim kaydı eksikliğine |
| **4.6 Sürekli bütünlük koruması (TOCTOU)** | VP-Control (kontrol sonrası yarış, idempotency), işlem veritabanları | Düşük | Yüksek | **Düşük:** AgentDojo'da karar ile yürütme arasında değişim fırsatı yok; REVIEW akışı da yok | Düşük | Gerçek üründe yüksek, deneyde gösterilemez | ❌ Ölçülmüş açık yok |
| **4.7 Uyarlamalı kanıt bütçesi** | VP-Control (portföy), mevcut VERIQEN yönlendirmesi | Düşük (mevcut çekirdeğin yeniden adlandırılması olur) | — (zaten var) | Yüksek | — | Mevcut | Zaten var; yeni mekanizma değil |
| **4.4 Zamansal saldırı tespiti** | Klasik dolandırıcılık tespiti, kümülatif limitler | Düşük | Orta | **Düşük:** AgentDojo bölümleri tek oturumluk; çok oturumlu veri yok | Orta | Düşük (bu benchmark'ta) | ❌ |
| **4.5 Karşı-olgusal güvenlik motoru** | Karşı-olgusal açıklamalar, metamorfik test | Düşük (bir mekanizma olarak) | Yüksek | Yüksek (**test yöntemi** olarak) | Düşük | Doğrudan değil; ama H1c'yi sınamanın en iyi yolu | ✅ H1c test edilmedi |

---

## 5. Seçilen üç özellik ve önerilen sıradan farkı

Önerilen sıra: PCE → yetenek belirteçleri → bütünlük koruması. **Değiştirilmiş öneri:**

### 1) Niyete bağlı yetenek belirteçleri (ana katkı adayı)
- **Neden ilk:** Ölçülmüş iki açığa (§3) aynı anda cevap veriyor: yanlış engelleme ve "doğru alıcıya yanlış işlem". Mevcut kodun (niyet bağlama, yazar kökeni) doğal devamı. AgentDojo'da ölçülebilir.
- **Ne yapacak:** Kullanıcının isteğinden çıkarılan her izin, alanları (işlem türü, alıcı, azami tutar, kullanım sayısı, süre) olan bir belirtece dönüşür. Belirtece tam uyan çağrı **hakem çağrılmadan** geçer; uymayan çağrı hakeme gider. Belirteç yalnız kullanıcının isteğinden üretilir, araç çıktılarından asla.
- **Hipotez:** B3 ve VERIQEN-SI'ye göre FPR'yi ve hakem çağrısını düşürürken ASR'yi artırmaz.
- **Dürüst sınır:** Yetenek kavramı yeni değil (CaMeL, Progent). Katkı, bunun **yönlendirmede** hakemin yerine geçtiğinde güvenlik–fayda dengesine etkisinin ölçülmesi olacak. "Kriptografik" imza (HMAC) yalnız belirteç bir güven sınırını aşıyorsa anlamlı; tek süreçli deneyde güvenlik katkısı yok, ürün mimarisi için eklenecek ve öyle raporlanacak.
- **Saldırılar:** belirteç tekrar kullanımı (replay), tutar aşımı, alıcı değiştirme, tür değiştirme, belirteç üretimini kullanıcı istemine enjeksiyonla etkileme.
- **Kilit risk:** Belirteçleri LLM çıkarıyorsa, LLM'in hatası belirteç hatasına dönüşür. Ölçülecek: LLM niyet çıkarıcının belirteç doğruluğu.

### 2) Karşı-olgusal / metamorfik doğrulama (test yöntemi olarak, 4.5'in dar hâli)
- **Neden:** Projenin ana güvenlik önermesi H1c hiç test edilmedi. Karşı-olgusal motor bunu ucuza ve maliyetsiz (çevrimdışı) sınar: aynı çağrıda yalnız güvenilmeyen kanalları değiştir, kararın değişmediğini doğrula. Ayrıca jüri sorusu 4'e ("bağımsız test") kısmi bir cevap: insan tasarımına bağlı olmayan, otomatik üretilmiş binlerce karşı örnek denemesi.
- **Ne yapacak:** Hypothesis ile özellik tabanlı testler: (P1) güvenilmeyen kanal değişimi kararı değiştirmez, (P2) belirteç dışı çağrı hakemsiz ALLOW alamaz, (P3) tek kullanımlık belirteç ikinci kez geçmez, (P4) süresi dolmuş belirteç geçmez.
- **Dürüst sınır:** Bu biçimsel ispat değil; "N rastgele örnekte karşı örnek bulunamadı" demek. Öyle raporlanacak.

### 3) İnce kanıt taşıyan yürütme kaydı (PCE + bütünlük, birleşik)
- **Neden:** Master prompt §5'in "her ALLOW'un kanıtı, her BLOCK'un politika dayanağı" şartını karşılıyor. Mevcut denetim kaydı hatasını da kapatıyor. Bütünlük koruması (onaylanan parametrelerin hash'i, nonce, süre) aynı kayda birkaç satırla eklenebiliyor; ayrı bir mekanizma olarak ele almaya gerek yok.
- **Dürüst sınır:** AgentDojo'da TOCTOU fırsatı olmadığı için bütünlük kısmı benchmark'ta ölçülemez; yalnız birim ve özellik testleriyle doğrulanacak. Güvenlik katkısı iddia edilmeyecek, denetlenebilirlik katkısı olarak sunulacak.

### Ertelenenler (25 Kasım sonrası)
- **Dinamik köken grafiği:** Dış geçerlilik için en önemli ikinci adım, ama PACT'e çok yakın ve Slack/Travel entegrasyonu gerektiriyor. Aşama 2'nin ilk işi.
- **Zamansal tespit:** Bu benchmark'ta veri yok.
- **Uyarlamalı kanıt bütçesi:** Zaten mevcut çekirdek; yeniden adlandırılmayacak.
- **Ayrı bütünlük koruması:** 3 numaralı maddeye dahil edildi.

---

## 6. Plan

### Aşama 1 — 25 Kasım'a kadar (6 gün)

| Gün | İş | Çıktı | LLM kotası |
|---|---|---|---|
| 1 (20 Kas) | Ölçüm altyapısı: bölüm başına karar kaydı, başarısızlık taksonomisi, MockJudge duyarlılık analizi (çevrimdışı), görev bölümleme dosyası (Banking dev/val, Slack/Travel kilitli) | `SYSTEM_AUDIT.md`, duyarlılık tablosu | Yok |
| 1 | Kotaya göre: VERIQEN-SI canlı koşusu (run3) | Gerçek hakemle B3 vs VERIQEN-SI | 120b |
| 2 | Yetenek belirteçleri MVP + birim testleri + özellik tabanlı testler (P1–P4) | Yeni modül, test raporu | Yok |
| 3 | Kilitli saldırı seti: yaz, hash'ini commit et, dokunma | `RED_TEAM_PROTOCOL.md` | Yok |
| 3–4 | Canlı koşular: VERIQEN-SI + belirteç (VERIQEN-T) | FPR / ASR / hakem çağrısı | 120b + ikinci sağlayıcı |
| 5 | Kilitli setin açılması (bir kez); sonuçların raporlanması | `BENCHMARK_RESULTS.md` | Kalan kota |
| 6 | `JURY_CRITICISM_RESPONSE.md`, `LIMITATIONS.md`, `JURY_DEFENSE.md`; 07'nin güncellenmesi | Başvuru metni için kanıt seti | Yok |

**Kota planı:** Tek model ve tek sağlayıcıyla günde yaklaşık 40 bölüm. Kapsamı iki katına çıkarmak için ikinci bir ücretsiz sağlayıcı (Gemini, kart istemiyor) önerilir. Ancak aynı karşılaştırmadaki tüm sistemler **aynı modelle** koşulmalı.

### Plan güncellemesi — 19 Kasım akşamı (ara jüri değerlendirmesinden sonra)

**Ne değişti ve neden:** Yetenek belirteçleri (VERIQEN-T) replay'de "doğru alıcıya istenmemiş ek işlem" açığını kapattı. Ama yalnız kullanıcı isteğinde **yazılı** IBAN'lara yetki verdiği için, gerçek hakemin en çok yanlış engellediği durumu (fatura gibi alıcının bir **belgeden** geldiği meşru ödemeler) değiştirmiyor. Bu durumlar için ayrı bir tasarım kararı gerekiyor. Ayrıca kilitli saldırı seti, VERIQEN-T dondurulmadan önce yazılmalı; aksi hâlde bağımsızlık iddiası zayıflar.

| Sıra | İş | Not |
|---|---|---|
| 1 (19 Kas) | **Kilitli saldırı seti v1:** yaz, içeriği git dışında sakla, sha256'sını commit et; yalnız korumasız sistemde (B0) çalışabilirlik kontrolü yap | Yazar, VERIQEN'in geliştiricisi; tam bağımsız değil, öyle raporlanacak |
| 2 (19–20 Kas) | `analyze_live.py`: meşru çağrıların yanlış engellenme oranını **alıcının kaynağına göre** ayır (kullanıcı isteği / belge-araç çıktısı / kullanıcının geçmişi) | Canlı koşudan önce hazır olmalı |
| 3 (20 Kas) | **VERIQEN-TR:** T + kaynağı belge olan alıcılarda hakem yerine REVIEW (kullanıcıya "Faturadaki IBAN UK12…, onaylıyor musunuz?" sorusu) | **Tasarım tercihi, katkı değil.** Ticari ürünlerdeki onay akışına benzer. REVIEW'in hiç tetiklenmemesi eleştirisine de cevap. Değerlendirmede REVIEW ayrı raporlanır, "başarı" sayılmaz |
| 4 (kota dolunca) | Canlı koşu: B3, VERIQEN-SI, VERIQEN-T, VERIQEN-TR aynı modelde, karar ve hakem kaydıyla | Kota: 120b için günde ~40 bölüm |
| 5 (dondurma) | VERIQEN-T/TR commit'i protokole yazılır → kilitli set **bir kez** açılır | Sonuç kötü olsa da raporlanır |
| 6 (24–25 Kas) | Jüri cevabı, sınırlılıklar, savunma belgeleri | |

### Aşama 2 — 25 Kasım sonrası (2–3 ay)
Köken grafiği ve Slack/Travel entegrasyonu → ekip dışı red-team (30+ saldırı, 8 kategori) → B4 (VP-Control yeniden uygulaması) → 5 tohumlu tam karşılaştırma ve ablasyon → beklenen fayda ve Pareto analizi → tam metin literatür incelemesi → FastAPI ürün katmanı ve REVIEW akışı (TOCTOU ancak burada ölçülebilir) → kalan belgeler.

### Belge eşlemesi (tekrar yazmamak için)
Master prompt'taki 18 belgeden bazılarının karşılığı zaten var: `RELATED_WORK` ≈ 01+08, `THREAT_MODEL` ≈ 10, `EXPERIMENT_PROTOCOL` ≈ 06, `NOVELTY_ANALYSIS` ≈ 03+09+11. Bunlar yeniden yazılmayacak, güncellenecek. Yeni belgeler `docs/v2/` altına konacak.

---

## 7. Onay gereken kararlar

1. **Kapsam:** 25 Kasım için Aşama 1, geri kalanı sonrası. Kabul mü?
2. **Sıra:** Belirteçler → metamorfik testler → kanıt kaydı (önerilen sıradan farklı). Kabul mü?
3. **Dal:** Yeni geliştirme `veriqen-2` dalında; `research/adversarial-routing` ve PR #1 olduğu gibi kalır. Melih'e haber verilmeli, çünkü PR onun.
4. **İkinci sağlayıcı:** Gemini ücretsiz anahtarı alınsın mı?
5. **Bağımsız saldırgan:** Ekip dışından birinin (ör. bir arkadaş) kilitli saldırı setine katkı vermesi mümkün mü? Değilse "ekip tarafından, dondurmadan önce yazılmış" diye dürüstçe raporlanacak.
