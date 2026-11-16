# 11 — Özgünlük Çekirdeği ve Pilot Deney

**Tarih:** 16 Kasım 2026
**Kod:** `experiments/pilot/` (`pilot.py`, `sweep.py`) · **Sonuçlar:** `experiments/pilot/results/`
**Durum:** Sentetik veriyle **pilot** çalışma. Ön kayıt yapılmadı. Sayılar varsayımsal modelden geliyor; **niteliksel örüntü** önemlidir, mutlak değerler değil.

---

## 1. Neden bu belge var

Jüri değerlendirmesindeki iki ana eleştiriye yanıt vermek için hazırlandı:

1. **"Güvenilir bilgi kullanıyorsan saldırının başarısız olması tanım gereği değil mi?"** (totoloji eleştirisi)
2. **"Tek bir ölçüm yok."**

Bu belge, VERIQEN'in özgünlüğünü üç somut iddiaya indiriyor ve bunlardan ikisini pilot deneyle sınıyor.

---

## 2. Özgünlük çekirdeği: üç iddia

### İddia 1 — "Güvenilir kaynak" yetmez; **anahtar kökeni** de gerekir

Literatürdeki ilke şudur: risk bilgisini modelden değil güvenilir kaynaktan al (bkz. 09: Irreversibility Budget; mimari derlemeler). Bu ilke **eksiktir.** Bir özellik güvenilir bir veritabanından okunsa bile, **hangi kaydın okunacağını belirleyen anahtar** (müşteri kimliği, sipariş kimliği, referans kayıt) ajanın önerisinden geliyorsa saldırgan, güvenilir kaynaktan **yanlış kaydı** okutabilir.

**Tanım (öneri):** Bir özellik ancak hem (a) değeri güvenilir kaynaktan geliyorsa, hem de (b) anahtarı oturum kimliğinden geliyorsa ya da yürütülecek argümana bağlanmışsa (P4) **güvenilir** sayılır. Bu iki koşulu sağlayan özelliklere **TK-özellik** (güvenilir kaynak + güvenilir anahtar) diyoruz.

**Neden önemli:** Bu ayrım totoloji eleştirisini çürütüyor. "Yalnızca güvenilir kaynak kullan" diyen ve sezgisel olarak güvenli görünen bir tasarım, pilotta **tamamen kırılıyor** (bkz. §4).

**Literatürle ilişkisi (dürüst konumlandırma):** D5, klasik **confused deputy** / IDOR örüntüsünün bir örneğidir. Ajan bağlamında confused deputy iyi bilinir; örneğin *Capability Gates Are Not Authorization: Confused-Deputy Failures in LLM Agent* (arXiv:2606.28679), *A Framework for Formalizing LLM Agent Security* (arXiv:2603.19469) ve *Authorization Architectures for Tool-Using AI Agents* (arXiv:2609.15906, §4.4). Bu çalışmalar, saldırganın **yürütülen işlemin argümanlarını** seçtirdiği durumu ve buna karşı çağrı başına yetkilendirmeyi ele alıyor.

VERIQEN'deki fark şu: D5'te **yürütülen işlem meşrudur**; saldırgan kendi siparişini iade ettirir ve çağrı başına yetki kontrolü geçer. Saldırganın seçtirdiği anahtar yalnızca **risk tahmininde / doğrulama yönlendirmesinde** kullanılır. Yani bu, yetkilendirme katmanında değil, **yönlendirme katmanında oluşan bir confused deputy'dir.** Çağrı başına yetkilendirme bunu yakalamaz. Katkımız bu örüntünün yeni bir yerde ortaya çıktığını göstermek ve TK-özellik tanımıyla kapatmaktır; örüntünün kendisini keşfettiğimizi iddia etmiyoruz. *(Bu konumlandırmanın, yönlendirme düzeyinde confused deputy'yi inceleyen bir çalışma olup olmadığına dair ek taramayla doğrulanması gerekiyor.)*

**Güncelleme (12 §3b):** AgentDojo'da yapılan durum ekme saldırısı, tanıma üçüncü bir koşul eklenmesi gerektiğini gösterdi. (c) **Yazar kökeni:** değeri güvenilir veritabanında dursa bile, o değeri **kimin belirlediği** önemli. Gelen bir transferin gönderen alanını saldırgan belirleyebilir. Güncel tanım: **TK-özellik = güvenilir kaynak + güvenilir anahtar + güvenilir yazar.**

### İddia 2 — Değişmezlik, kalibrasyonun saldırı altına **taşınmasını** sağlar

Yönlendirme kararı yalnızca TK-özelliklere bağlıysa, saldırgan yönlendirmeyi değiştiremez. O zaman saldırganın yapabileceği en kötü şey, yönlendirmeden bağımsız olarak manipüle edebildiği doğrulayıcıları etkisiz bırakmaktır (örnekte: sahte "hasarlı ürün" beyanıyla kargo kontrolünü boşa düşürmek). Bu en kötü durum **temiz kalibrasyon verisi üzerinde simüle edilebilir.**

**Sonuç:** Saldırı altındaki fazla risk, saldırıyı hiç görmeden **önceden tahmin edilebilir ve bir δ hedefine ayarlanabilir.** Manipüle edilebilir özellik kullanan bir yönlendirici için bu mümkün değildir: kalibrasyon ne kadar iyi yapılırsa yapılsın saldırı altında anlamsızlaşır.

Bu iddia, "saldırı başarısız oldu" demek yerine **"saldırı altındaki riski ölçmeden önce bildik ve ayarladık"** diyor. Totoloji değil, **kalibrasyon garantisi.**

### İddia 3 — Doğrulama düşürme tehdidinin ölçümü ve açık test seti

Bu tehdit taksonomilerde adlandırılmış ama ölçülmemiş (bkz. 09). Katkı: Downgrade-ASR metriği ve tekrarlanabilir saldırı seti (D1 beyan, D2 dedektör atlatma, D5 anahtar kaydırma).

---

## 3. Pilot düzeneği (özet)

| Öğe | Değer |
|---|---|
| Dünya | 5.000 müşteri, %6 dolandırıcı; iade istekleri. Dolandırıcılar yeni hesap ve sık iade eğiliminde. Ayrıca %3 fırsatçı sahte "teslim edilmedi" iddiası. |
| Doğrulayıcılar | Kargo kontrolü (maliyet 1): yalan "teslim edilmedi" iddiasını %95 yakalar. Dolandırıcılık kontrolü (maliyet 4): dolandırıcıyı %92 yakalar. Yanlış pozitif oranı sırasıyla %0.5 ve %1. |
| Zorunlu kurallar | 300 TL üstü → insan incelemesi (%85 yakalama); 1000 TL üstü → BLOCK. |
| Planlar | P0: ek doğrulama yok · P1: kargo · P2: kargo + dolandırıcılık (= B3) |
| Yönlendiriciler | Lojistik risk modeli + iki eşik. Eşikler kalibrasyon kümesinde "UAER ≤ B3 + δ" kısıtı altında maliyet minimize edilerek seçiliyor. **Tüm uyarlamalı sistemlere aynı prosedür uygulanıyor.** |
| Özellik setleri | **Naif:** tutar + ajan anahtarıyla okunan kayıt (kıdem, iade sayısı) + ajan beyanı (VIP, sebep) + enjeksiyon dedektör skoru. **T:** yalnız güvenilir kaynak, ajan anahtarıyla. **TK:** yalnız güvenilir kaynak, oturum anahtarıyla. |
| Saldırgan | **Beyaz kutu:** modeli ve eşikleri bilir. Her dolandırıcı isteği için D1/D2/D5 kombinasyonları ve 30 "sadık müşteri" kimliği arasından başarı olasılığını en yükseltecek seçeneği seçer. İstekler 300 TL altında tutulur (insan incelemesinden kaçmak için). |
| Ölçek | 5 tohum × (6.000 eğitim + 6.000 kalibrasyon + 10.000 test + 3.000 saldırı) |
| Metrikler | 06'daki tanımlar. UAER, vaka başına **beklenen** yürütülme olasılığının ortalaması. GA'lar vaka düzeyinde bootstrap ile hesaplandı (5 tohum havuzlanmış). |

---

## 4. Sonuçlar (gerçek pilot sonuçları — sentetik veri)

### 4.1 Ana tablo (5 tohum ortalaması)

| Sistem | Maliyet / karar | Doğal UAER % | **Saldırı altı UAER %** [%95 GA] | Downgrade-ASR % | FBR % | Saldırganın seçtiği |
|---|---|---|---|---|---|---|
| B0 korumasız | 0.00 | 100.0 | 100.0 | 100.0 | 0.00 | — |
| B1 yalnız kurallar | 0.00 | 95.1 | 100.0 | 100.0 | 0.03 | — |
| **B3 sabit tam doğrulama** | **5.00** | 2.8 | **8.0** | 0.0 | 1.52 | D1 |
| B4-naif | 1.85 | 3.7 | **99.9** [99.8, 99.9] | 99.9 | 0.58 | çoğunlukla D1+D2+D5 |
| **B4-T (yalnız güvenilir kaynak)** | 1.60 | 3.4 | **100.0** [100.0, 100.0] | 100.0 | 0.62 | çoğunlukla D1+D5 |
| B4-TK (güvenilir kaynak + anahtar) | 1.60 | 3.4 | 12.0 [11.7, 12.2] | 4.3 | 0.62 | D1 |
| VERIQEN (TK + monoton taban) | 1.60 | 3.4 | 12.2 [11.9, 12.5] | 4.6 | 0.63 | D1 |
| **VERIQEN-K (TK + taban + kötü durum kalibrasyonu, δ = 1 puan)** | **1.98** | 3.7 | **9.0** [8.9, 9.2] | 1.1 | 0.72 | D1 |
| B4-naif + kötü durum kalibrasyonu | 1.89 | 3.6 | 99.8 [99.8, 99.9] | 99.8 | 0.59 | çoğunlukla D1+D2+D5 |

Tüm sistemlerde insan incelemesi oranı (HER) %3.3.

**Eşleştirilmiş fark (saldırı altı UAER, B3'e göre):**
- VERIQEN (doğal kalibrasyon): **+4.2 puan** [3.9, 4.5]
- VERIQEN-K (δ = 1 puan): **+1.05 puan** [0.90, 1.21]

### 4.2 Maliyet–güvenlik eğrisi ve kalibrasyonun taşınması

Grafik: `experiments/pilot/results/pilot_tradeoff.png`

| Hedef δ | VERIQEN-K maliyet | VERIQEN-K saldırı UAER % | Fazla risk: **tahmin** (temiz veri) | Fazla risk: **gerçekleşen** (saldırı) | Naif-K saldırı UAER % | Naif-K fazla risk tahmin → gerçek |
|---|---|---|---|---|---|---|
| 0 | 2.55 | 8.2 | +0.00 | +0.18 | 98.5 | +0.00 → **+90.5** |
| 0.25 puan | 2.39 | 8.4 | +0.19 | +0.42 | 99.3 | +0.19 → +91.3 |
| 0.5 puan | 2.28 | 8.6 | +0.34 | +0.59 | 99.7 | +0.38 → +91.7 |
| 1 puan | 1.98 | 9.0 | +0.71 | +1.05 | 99.8 | +0.83 → +91.8 |
| 2 puan | 1.72 | 10.2 | +1.60 | +2.17 | 100.0 | +1.65 → +92.0 |
| 4 puan | 1.48 | 12.3 | +3.53 | +4.32 | 100.0 | +3.20 → +92.0 |

*(Maliyet: zararsız trafikte karar başına birim. B3 maliyeti 5.00. Fazla risk değerleri yüzde puan.)*

### 4.3 Okuma

1. **Uyarlamalı doğrulama gerçekten kırılabiliyor.** Naif sistem saldırı altında neredeyse her güvensiz işlemi geçiriyor (%99.9). Oysa doğal trafikte B3'e yakın görünüyordu (%3.7 ve %2.8). Yani normal testler bu açığı göstermiyor. → **H1a pilotta desteklendi.**
2. **"Yalnız güvenilir kaynak" kuralı da kırılıyor.** B4-T hiçbir ajan beyanı kullanmamasına rağmen anahtar kaydırma (D5) ile %100 kırıldı. → **İddia 1 pilotta desteklendi.** Totoloji eleştirisine verilecek en güçlü yanıt bu satır.
3. **Anahtar kökeni yetiyor, ama tek başına kalibrasyon garantisi vermiyor.** TK sistemi saldırgan tarafından yönlendirilemedi; D5 ve D2 tercih edilmedi. Ancak doğal trafiğe göre kalibre edildiği için B3'ün 4.2 puan gerisinde kaldı.
4. **Kötü durum kalibrasyonu riski önceden tahmin edilebilir kılıyor.** VERIQEN-K'da temiz veriden tahmin edilen fazla risk, saldırıda gerçekleşenle aynı büyüklükte (ör. δ = 1 puanda +0.71'e karşı +1.05). Aynı kalibrasyon naif sistemde +0.83 tahmin edip +91.8 gerçekleşiyor. → **İddia 2 pilotta niteliksel olarak desteklendi.**
5. **Maliyet kazancı:** δ = 0'da VERIQEN-K, B3 ile neredeyse aynı saldırı altı güvenliği (+0.18 puan) yaklaşık **%49 daha düşük maliyetle** (2.55'e karşı 5.00) sağlıyor.

---

## 5. Dürüst sınırlılıklar (jüriye kendimiz söyleyelim)

| # | Sınırlılık | Etkisi |
|---|---|---|
| 1 | **Sentetik dünya.** Dolandırıcıların güvenilir özelliklerle ayırt edilebilirliği bizim varsayımımız. Gerçek veride bu ayrım zayıfsa VERIQEN-K'nın maliyet kazancı azalır. | Mutlak sayılar genellenemez. |
| 2 | **Tahmin hafifçe iyimser.** Gerçekleşen fazla risk, tahminden tutarlı biçimde 0.2–0.8 puan yüksek. Sebep: kalibrasyon tüm güvensiz istekler üzerinde yapıldı, saldırı kümesi ise yalnızca dolandırıcılardan oluşuyor (dağılım farkı). | Garanti için δ'yı tahminin biraz altına koymak ya da dolandırıcı alt kümesinde kalibre etmek gerekiyor. Biçimsel bir sınır (ör. konformal risk kontrolü) henüz kurulmadı. |
| 3 | **Monoton taban bu pilotta ölçülebilir katkı sağlamadı.** Eşikler yeniden optimize edildiği için taban, sonuçları neredeyse değiştirmedi (VERIQEN ≈ B4-TK). | Tabanın değeri, model hatası veya politika değişikliği durumundaki dayanıklılıkta olabilir; bu ayrıca test edilmeli. Bu sonuç rapordan çıkarılmamalı. |
| 4 | **Saldırgan sınırlı.** Yalnızca D1, D2, D5 ve 30 kurban kimliği. Eşik sondalama (D3), kaynağı yavaşlatma (D4) ve onay sonrası değişiklik (D6) henüz yok. | "Dayanıklı" iddiası yalnızca bu saldırı ailesi içindir. |
| 5 | **LLM yok.** Ajanın davranışı soyut olarak modellendi; saldırgan, ajanın her istediğini beyan edeceğini varsayıyor (en kötü durum). | Gerçek ajanla uçtan uca deney (AgentDojo Banking) hâlâ gerekli. |
| 6 | **UAER beklenen değer olarak hesaplandı.** Rastgele doğrulayıcı sonuçları örneklenmedi; GA'lar yalnızca vaka çeşitliliğini yansıtıyor. | Gerçek deneyde örnekleme ve tekrarla genişletilmeli. |
| 7 | **Tek kişi tasarladı.** Saldırıları savunmayı tasarlayan taraf yazdı. | Ekipte rol ayrımı veya otomatik saldırgan gerekli. |

---

## 6. Jürinin 5 sorusuna güncellenmiş yanıtlar

| Soru | Yanıt |
|---|---|
| Güvenilir bilgi kullanıyorsanız başarı tanım gereği değil mi? | Hayır. "Güvenilir kaynak" kullanan sistem pilotta %100 kırıldı (B4-T). Güvenilirliğin anahtar kökenini de içermesi gerekiyor; katkılarımızdan biri bu ayrımı tanımlamak. |
| Naif sistem kırılmazsa ne kalır? | Pilotta kırıldı (%99.9). Gerçek veride kırılmazsa bu da raporlanabilir bir sonuç; test seti ve kalibrasyon yöntemi yine kullanılabilir kalır. |
| VP-Control olmasaydı yine özgün olur muydunuz? | İddia 1 ve 2, VP-Control'den bağımsızdır. VP-Control saldırganı kapsam dışı bırakıyor; biz tam olarak saldırgan altında kalibrasyonun ne zaman taşındığını gösteriyoruz. |
| Saldırıları siz yazdınız, neden güvenelim? | Beyaz kutu saldırgan (en güçlü varsayım) kullandık ve kodu açıyoruz. Bir sonraki aşamada rol ayrımı ve otomatik saldırgan eklenecek. |
| İki ayda ne garanti ediyorsunuz? | Pilotun gerçek LLM ajanıyla tekrarı, D3–D6 saldırılarının eklenmesi, açık kaynak test seti ve kısa bir rapor. |

## 7. Sonraki adımlar (öncelik sırasıyla)

1. **Dolandırıcı alt kümesinde kalibrasyon + konformal risk kontrolü** ile tahmin–gerçekleşen farkını kapatmak (Sınırlılık #2).
2. **D3 (eşik sondalama / bölme), D4 (kaynak yavaşlatma), D6 (onay sonrası değişiklik)** saldırılarını eklemek.
3. Monoton tabanın değerini **model hatası senaryosunda** test etmek (ör. dağılım kayması) ya da çıkarmak.
4. Aynı deneyi **gerçek LLM ajanıyla** AgentDojo Banking'de küçük ölçekte tekrarlamak.
5. Gerçekçi bir kamu veri setiyle (ör. e-ticaret iade/dolandırıcılık verisi) güvenilir özelliklerin ayırt ediciliğini sınamak.
