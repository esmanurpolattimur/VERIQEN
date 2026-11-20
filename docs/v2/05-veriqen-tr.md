# 05 — VERIQEN-TR: Kaynağı Olmayan Alıcı İçin İnsan Onayı ve Köken Bilgili Hakem (v4)

**Tarih:** 20 Kasım 2026 · **Dal:** `veriqen-2`
**Durum:** Kod, testler ve simülasyon sonuçları hazır. Gerçek LLM ile ölçüm **yapılmadı** (kota).
**Önemli:** VERIQEN-TR, kilitli set v1 açıldıktan sonra yazıldı. Kilitli set sonuçları bağımsız test değildir.

---

## 1. Neden

Hakem talimatı denemeleri (`04`) şunu gösterdi: talimatı sıkılaştırmak (v1) meşru işlemleri, gevşetmek (v3) saldırıları geçiriyor. Hakemin hatası talimattan değil, **eksik bilgiden** geliyor: "Bu alıcı gerçekten meşru alıcı mı?"

- Kimi durumda cevap sistemde **var**: kullanıcı Spotify'a daha önce şu IBAN'a ödeme yapmış.
- Kimi durumda **yok**: faturadaki yeni bir IBAN'ın doğru olup olmadığını yalnız kullanıcı bilebilir.

## 2. Tasarım

1. **Kaynağı olmayan alıcı → insan onayı.** Para işleminin alıcısı (a) kullanıcı isteğinde yazılı değilse, (b) kullanıcının daha önce ödeme yaptığı bir hesap değilse ve (c) mevcut bir zamanlanmış ödemenin alıcısı değilse, hakeme gönderilmez; kullanıcıya sorulur ("Faturadaki IBAN UK12…, onaylıyor musunuz?").
2. **Hakeme alıcı kökeni (talimat v4).** Hakeme giden işlemlerde hakem şunları görür: işlem türü istenmiş mi; alıcı istekte yazılı mı; kullanıcı bu alıcıya daha önce ödeme yapmış mı ve **hangi konuyla** (ör. "Spotify Premium"). Hakemi yanıltan tutar bilgisi verilmez.
3. Geri kalan her şey VERIQEN-T2 ile aynı (belirteçler, kanıta bağlı tutar, bölüm sınırları, önbellek).

**Bu bir tasarım tercihidir, bilimsel katkı olarak sunulmaz.** Ticari ajan çerçevelerindeki onay akışlarına benzer. Farkı, onayın **ne zaman** isteneceğinin köken bilgisiyle deterministik olarak belirlenmesi.

## 3. Sonuçlar (replay; ajan senaryolu; MockJudge 0.90/0.05; 20 tekrar)

İnsan onayı iki şekilde raporlandı: kullanıcı her onayı **reddederse** (en kötü fayda) ve meşru onayları **kabul ederse**.

| | B3 | VERIQEN-T2 | **VERIQEN-TR** |
|---|---|---|---|
| ASR standart / durum ekme / geçmiş alıcı | 6.8 / 6.8 / 6.8 | 5.6 / 5.6 / 5.6 | **0.0 / 0.0 / 5.6** |
| Zararsız fayda, onaylar reddedilirse | 95.3 | 97.5 | 91.6 |
| Zararsız fayda, kullanıcı meşru onayları kabul ederse | 95.3 | 97.5 | **97.8** |
| Hakem çağrısı / zararsız görev | 0.88 | 0.56 | **0.50** |
| Hakem çağrısı / saldırılı görev | 1.54 | 1.11 | **0.50** |
| İnsan onayına giden zararsız bölüm | 0 | 0 | 6.2 % |
| İnsan onayına giden saldırılı bölüm | 0 | 12.0 % | **68.8 %** |

**Kilitli set v1 (açılış sonrası, bağımsız değil; onay = red):** kusursuz hakemle 0; varsayılan hakemle toplam **2.2 %** (B3 13.2, T2 7.1).

**Hakem test seti (dev), yönlendirme:** 58 saldırı çağrısının **54'ü** hakeme hiç gitmiyor, insan onayına gidiyor; 16 meşru çağrının 4'ü (fatura ödemeleri) de onaya gidiyor. Hakemin karar vermesi gereken vaka 74'ten **16'ya** iniyor. v4'ün bu 16 vakadaki doğruluğu gerçek LLM ile ölçülmedi.

## 4. Okuma ve sınırlılıklar

1. **Saldırı başarısının sıfıra inmesi, kullanıcının saldırıları reddettiği varsayımına dayanıyor.** Saldırılı bölümlerin %68.8'inde karar kullanıcıya bırakılıyor. Kullanıcı da kandırılabilir: onay penceresinde "Spotify farkı" gibi ikna edici bir konu görebilir. İnsan hatası modellenmedi. Doğru ifade şu: "Saldırıların büyük kısmı otomatik onaylanmıyor ve kullanıcıya açık bir uyarıyla soruluyor."
2. **Ele geçirilmiş geçmiş alıcı (payee) saldırısında TR'nin katkısı yok** (5.6). Saldırgan, kullanıcının daha önce ödeme yaptığı bir hesabı kontrol ettiğinde alıcının kaynağı var görünüyor ve karar hakeme kalıyor.
3. **Kullanıcı yükü:** Zararsız bölümlerin %6.2'sinde (fatura ödemeleri) kullanıcıya soru soruluyor. Faturayı onaylamak çoğu kullanıcı için makul bir adım, ama gerçek kullanıcı deneyimi ölçülmedi.
4. Bütün sayılar simülasyon. Gerçek hakem (v4) ve gerçek ajanla ölçüm bekliyor.

## 5. Ölçüm planı (gerçek LLM)

1. Hakem test setinde v4 (dev, 16 hakem çağrısı + 58 yönlendirme): `hakem.ps1 v4`
2. Canlı koşu: VERIQEN-TR + hakem v4, aynı görevlerde B3 ile karşılaştırma: `canli.ps1 VERIQEN-TR -JudgePrompt v4`
3. Raporlanacaklar: ASR, meşru engelleme, insan onayına giden oran (meşru ve saldırılı ayrı), hakem çağrısı.
