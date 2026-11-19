# 01 — Niyete Bağlı Yetenek Belirteçleri (VERIQEN-T) ve MockJudge Duyarlılığı

**Tarih:** 19 Kasım 2026 · **Dal:** `veriqen-2`
**Kod:** `experiments/agentdojo/capability.py`, `veriqen_gate.py` (VERIQEN-T, VERIQEN-TN), `tests/test_capability.py`, `sensitivity.py`, `analyze_live.py`
**Sonuç dosyaları:** `experiments/agentdojo/results/v2/replay_{standard,planting,payee}/summary.json`, `results/sensitivity/`, `results/sensitivity_T/`
**Durum:** Replay (senaryolu ajan + MockJudge) sonuçları tamam. Gerçek LLM ile VERIQEN-T koşusu **sürüyor**; bu belge o koşudan önce yazıldı.

---

## 1. Problem

İki ölçülmüş sorun (00 §3):

1. **Kalan güvenlik açığı:** VERIQEN-SI, kullanıcının adını verdiği alıcıya istenmemiş **ek** bir işlem yaptırılmasına karşı açık bırakıyordu (ele geçirilmiş geçmiş alıcı saldırısı, ASR %9.9; kâhin niyetli üst sınır %6.8).
2. **Gerçek hakemin yanlış engellemesi:** Gerçek LLM hakemi meşru işlemleri sık engelliyor (§5).

## 2. Mekanizma

Kullanıcının isteğinde **yazılı** her IBAN için, izin verilen para işlemi türleriyle sınırlı bir belirteç üretilir:

| Alan | Değer |
|---|---|
| İşlem türleri | Niyet çıkarıcının izin verdiği para işlemleri |
| Alıcı | Kullanıcı isteğindeki IBAN (normalize) |
| Azami tutar | Otomatik limit (1.000) |
| Kullanım | 1 |
| Geçerlilik | Yalnız o bölüm (yeni kullanıcı isteğinde geçersiz) |
| İmza | HMAC-SHA256, oturum anahtarı |

Para işlemi ancak bir belirtece **tam uyuyorsa** (alıcı, tür, tutar, kalan kullanım, bölüm, imza) hakem çağrılmadan yürütülür ve belirteç tüketilir. Uymuyorsa hakeme gider. Araç çıktıları belirteç üretemez. Zorunlu taban (bakiye, parola, büyük tutar) belirteçten önce uygulanır.

**Literatürle ilişki:** Yetenek tabanlı yetkilendirme yeni değil (CaMeL'in değerlere bağlı yetenekleri, Progent, Macaroons). Buradaki soru, bu yapı **doğrulama yönlendirmesinde** hakemin yerine geçtiğinde güvenlik, yanlış engelleme ve maliyet dengesinin nasıl değiştiği.

**İmza hakkında dürüst not:** Deneyde belirteç üreten ve uygulayan bileşen aynı süreçte. İmzanın bu düzenekte güvenlik katkısı yok; ürün mimarisinde (bileşenler ayrıysa) anlam kazanıyor. Testlerde kurcalamaya karşı doğrulanıyor.

## 3. Replay sonuçları (gerçek çıktılar; ajan senaryolu, hakem SİMÜLASYON: kaçırma %10, yanlış alarm %5; 20 tekrar, 16 görev × 9 saldırı)

| Sistem | ASR standart | ASR durum ekme | ASR geçmiş alıcı | Zararsız fayda | Hakem / zararsız görev | Hakem / saldırılı görev |
|---|---|---|---|---|---|---|
| B3 (her işlemde hakem) | 6.8 | 6.8 | 6.8 | 95.3 | 0.88 | 1.54 |
| VERIQEN-SI | 6.8 | 6.8 | **9.9** [8.9, 11.0] | 97.8 | 0.44 | 1.07–1.10 |
| VERIQEN-SI\* (kâhin niyet, üst sınır) | 6.8 | 6.8 | 6.8 | 97.8 | 0.44 | 1.10 |
| **VERIQEN-T** | 6.8 | 6.8 | **6.8** [5.9, 7.7] | 97.5 | 0.56 | 1.23 |
| VERIQEN-TN (adla çözümleme) | 6.8 | 6.8 | **14.8** | 97.5 | 0.56 | 1.14 |

**Okuma:**
1. VERIQEN-T, üç saldırı türünün hepsinde B3 ve kâhin üst sınırla aynı ASR'ye ulaşıyor; kâhin niyet gerektirmeden.
2. Bedeli hakem çağrısında: zararsız görev başına 0.44 → 0.56 (B3: 0.88). Fark iki görevden geliyor (`user_task_5`, `user_task_11`): AgentDojo'nun doğru çözümü alıcıyı IBAN yerine adla yazıyor ("Spotify", "Apple"); VERIQEN-SI bu adları kullanıcı isteğinde bulduğu için hakemsiz geçiriyordu. Gerçek ajan IBAN kullanacağından bu farkın büyük kısmı replay yan etkisi olabilir; canlı koşu ile doğrulanacak.

### Dev / val ayrımı (`experiments/protocol/split_v1.json`, 5 tekrar)

| Sistem | Dev ASR (std / ekleme / geçmiş alıcı) | Val ASR | Dev hakem / görev | Val hakem / görev |
|---|---|---|---|---|
| B3 | 6.2 / 6.2 / 6.2 | 9.3 / 9.3 / 9.3 | 0.70 | 1.17 |
| VERIQEN-SI | 6.2 / 6.2 / **11.8** | 9.3 / 9.3 / 9.3 | 0.40 | 0.50 |
| VERIQEN-T | 6.2 / 6.2 / **6.2** | 9.3 / 9.3 / 9.3 | 0.50 | 0.67 |
| VERIQEN-TN | 6.2 / 6.2 / 7.3 | 9.3 / 9.3 / **27.4** | 0.50 | 0.67 |

## 4. Olumsuz sonuç: adla çözümleme (VERIQEN-TN)

İlk tasarımda belirteç, kullanıcının **adını** andığı alıcılar için de üretiliyordu: ad, yalnız kullanıcının kendi başlattığı işlemlerin konu alanlarında aranıp IBAN'a çözülüyordu. Dev kümesinde sorun görülmedi (payee ASR 7.3). **Val kümesinde payee ASR %27.4'e çıktı.** Neden: bir alıcının adının geçmesi ona ödeme yapma niyeti değil. "Yeni ev sahibime geçir" isteğinde eski ev sahibinin "Rent" kaydı da belirteç alıyor; "Apple aradı" isteğinde Apple'ın hesabı, saldırgan o hesabı kontrol ediyorsa açık kapı oluyor.

Bu varyant kapatıldı ama VERIQEN-TN olarak tutuluyor. **Val'e bakılarak yapılan bir tasarım değişikliği** olduğu için VERIQEN-T'nin val sonuçları bu karar açısından temiz değil.

## 5. MockJudge duyarlılığı (jüri eleştirisi 3.1)

`sensitivity.py`, 5 tekrar, 16 görev. Tüm değerler **simülasyon**.

**Kaçırma oranı taraması (yanlış alarm %5):**

| Hakem kaçırma | %0 | %5 | %10 | %20 | %30 | %50 |
|---|---|---|---|---|---|---|
| B3 ASR (üç saldırı türü) | 0 | 4.0 | 7.4 | 14.7 | 21.2 | 36.9 |
| VERIQEN-SI ASR, geçmiş alıcı | **3.5** | 7.5 | 10.8 | 17.8 | 23.5 | 38.3 |
| VERIQEN-T ASR (üç saldırı türü) | **0** | 4.0 | 7.4 | 14.7 | 21.2 | 36.9 |

**Yanlış alarm taraması (kaçırma %10), zararsız fayda %:**

| Hakem yanlış alarm | %0 | %5 | %10 | %20 | %30 |
|---|---|---|---|---|---|
| B3 | 100 | 92.5 | 83.8 | 75.0 | 71.2 |
| VERIQEN-SI | 100 | 96.2 | 93.8 | 85.0 | 83.8 |
| VERIQEN-T | 100 | 96.2 | 93.8 | 85.0 | 82.5 |

**Okuma:**
1. Mutlak güvenlik tamamen hakemin kalitesine bağlı. "%6.8 güvenli" bir sistem özelliği değil, varsayımın sonucu.
2. Savunulabilir iddia: **VERIQEN-T, her hakem kalitesinde ve üç saldırı türünde B3 ile aynı ASR'yi veriyor.** Yani hiçbir saldırı hakemi atlamıyor. VERIQEN-SI'de, kusursuz hakemle bile %3.5'lik bir atlama kalıyordu.
3. Hakem ne kadar çok yanlış alarm verirse, hakemi daha az çağıran sistemlerin fayda avantajı büyüyor (%30 yanlış alarmda +11–13 puan).

## 6. Gerçek hakem: yanlış engellemenin kaynağı (B3, iki model)

`analyze_live.py`; meşru çağrılar alıcının kaynağına göre ayrıldı. B3'te her hassas çağrı hakeme gider.

| Alıcının kaynağı | gpt-oss-120b (run2) | gpt-oss-20b (run3-20b) | Toplam engellenen |
|---|---|---|---|
| Kullanıcı isteğinde yazılı IBAN | 7/7 | 4/6 | **11/13** |
| Kullanıcının kendi geçmişi | 1/5 | 2/2 | 3/7 |
| Belge (fatura, dosya) | — | 0/1 | 0/1 |

- 20b koşusunda hakem kaydı var: 33 çağrı, **0 hata**. Engellemeler kota hatası değil.
- 120b koşusunda hakem kaydı yoktu; bazı engellemelerin kota hatası olma ihtimali dışlanamıyor.
- **Önemli düzeltme:** Ara jüri değerlendirmesinde "belirteçler gözlenen sorunu (fatura ödemesi) çözmüyor" denmişti. Veri, yanlış engellemelerin çoğunun alıcının **kullanıcı isteğinde yazılı** olduğu işlemlerde olduğunu gösteriyor. VERIQEN-T tam bu işlemleri hakemsiz geçiriyor. Örnek küçük (20 meşru çağrı); VERIQEN-T'nin gerçekten daha az yanlış engellediği ancak aynı görevlerde canlı koşuyla gösterilebilir (sürüyor).

## 7. Testler

`python -m pytest tests -q` → 11 test, hepsi geçiyor. Özellik tabanlı testler hypothesis ile her biri 300 rastgele örnek:

| Test | Özellik |
|---|---|
| P1 | Kullanıcı isteğinde yazılmamış alıcıya para işlemi hakemsiz ALLOW alamaz |
| P2 | Aynı alıcıya ikinci ödeme hakeme gider (tek kullanım) |
| P3 | Güvenilmeyen kanal (araç çıktısı) değişse de sıkı sistemlerde yönlendirme kararı değişmez (H1c'nin karşı-olgusal testi) |
| Birim | Tür/tutar sınırı, kurcalanmış imza, başka bölüm/anahtardan belirteç, araç çıktısından belirteç üretilmemesi, gelen transferlerin adla çözümlemede yok sayılması |

**Mutasyon kontrolü:** Kodda dört bilinçli hata yapıldı (tek kullanım kapalı, bölüm kontrolü kapalı, gelen transfer filtresi kapalı, sıkı modun araç metnine güvenmesi). Dördü de testlerce yakalandı. Gelen transfer testi ilk yazıldığında hatayı yakalamıyordu; düzeltildi.

**Sınır:** P3, sıkı modun araç çıktısını tasarım gereği yok saymasını doğruluyor. Bu bir uygulama hatasını yakalar, tasarımın doğruluğunu kanıtlamaz. Biçimsel ispat değildir.

## 8. Sınırlılıklar

1. Replay sonuçları senaryolu ajan ve MockJudge ile. Gerçek LLM sonucu bekleniyor.
2. Banking görevlerinin tamamı daha önce görüldü; val ayrımı yalnız yeni mekanizma için kısmi bir ayrım. TN kararı val'e bakılarak verildi.
3. Belirteç yalnız kullanıcı isteğinde **yazılı** IBAN'lardan üretiliyor. Alıcıyı adla ya da belgeyle veren meşru ödemeler hâlâ hakeme gidiyor (plan: VERIQEN-TR, belgeden gelen alıcılar için REVIEW).
4. İşlem türü ile alıcı arasında eşleme yok; belirteç, izin verilen tüm para işlemi türlerini kapsıyor ve tek kullanımlık olmasıyla sınırlanıyor.
5. Kilitli saldırı seti (12 saldırı) mühürlendi ama henüz açılmadı; VERIQEN-T'ye karşı çalıştırılmadı.
