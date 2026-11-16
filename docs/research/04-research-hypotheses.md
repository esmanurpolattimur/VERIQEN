# 04 — Araştırma Hipotezleri

Her hipotez **yanlışlanabilir** biçimde yazıldı: hangi sonucun hipotezi çürüteceği önceden belirtildi. Eşik değerler (δ, oranlar) **deneyden önce** ön kayıt (preregistration) belgesinde sabitlenmelidir. Buradaki değerler önerilen başlangıç değerleridir.

Notasyon ve metrik tanımları için bkz. 06.

---

## H1 — Aday F: Manipülasyona dayanıklı uyarlamalı doğrulama (ana hipotez)

**Bağlam:** Uyarlamalı doğrulama, saldırgan yönlendirme kararını etkileyebiliyorsa yeni bir saldırı yüzeyi açar.

**H1a (zafiyet hipotezi):**
Yönlendirme özellikleri ajan beyanı veya güvenilmeyen içerikten etkilenebilen bir **naif uyarlamalı doğrulayıcı (B4-naif)**, uyarlamalı "doğrulama düşürme" saldırıları altında, **sabit tam doğrulamaya (B3)** göre anlamlı ölçüde daha yüksek UAER üretir.

- **Ölçüt:** ΔUAER = UAER(B4-naif) − UAER(B3), aynı saldırı vakaları üzerinde eşleştirilmiş.
- **Destek koşulu:** ΔUAER > 0 ve %95 GA alt sınırı > 0 (McNemar, Holm düzeltmeli p < 0.05).
- **Yanlışlanma:** %95 GA 0'ı içeriyorsa veya ΔUAER ≤ 0 ise H1a reddedilir. Bu durumda "naif uyarlamalılık zaten güvenli" sonucu yayımlanabilir bir negatif sonuçtur, ancak F'nin motivasyonu zayıflar.

**H1b (çözüm hipotezi):**
Güvenilir özellik kısıtı + monoton taban uygulayan **VERIQEN-F (B4)**:

1. Aynı saldırılar altında UAER bakımından B3'e göre **eşdeğersiz değildir (non-inferior)**: UAER(B4) − UAER(B3) için %95 GA üst sınırı < δ = 1 puan.
2. Zararsız trafikte (benign) B3'e göre **doğrulama maliyetini en az %30 azaltır**: maliyet oranı için %95 GA üst sınırı < 0.70.
3. Downgrade-ASR'yi B4-naif'e göre anlamlı ölçüde düşürür.

- **Yanlışlanma:** (1) veya (2)'den biri sağlanmazsa H1b reddedilir. Örneğin güvenlik eşdeğerliği ancak maliyet tasarrufu sıfıra yaklaşınca sağlanıyorsa, "uyarlamalılık güvenli ama kazançsız" sonucu raporlanır.

**H1c (biçimsel önerme, deneyle tutarlılık):**
Saldırgan yalnızca güvenilmeyen kanalları (araç çıktısı, ajan beyanı) kontrol ediyorsa, B4'ün plan seçimi bu kanallardaki değişikliklerden etkilenmez. Test: aynı işlem için yalnızca güvenilmeyen kanallar değiştirilmiş N çift vakada **plan değişim oranı = 0** olmalıdır. Tek bir karşı örnek (> 0), uygulamada önermeyi ihlal eden bir hata olduğunu gösterir.

---

## H2 — Aday G: Argüman düzeyinde kanıt bağlama + yürütme anı tazelik

**H2:**
Yetki taşıyan argümanları kaynak sürümüne bağlayan ve yürütme anında aynı transaction içinde yeniden doğrulayan sistem (**B4-G**), yalnızca karar anında doğrulayan sisteme (**B3-karar-anı**) göre **durum değişimi senaryolarında** UAER'ı anlamlı ölçüde düşürür. Bu senaryolar şunlardır: sipariş sürümü değişimi, onay sonrası parametre değişimi, yinelenen istek, kontrol–yazma arası yarış.

Aynı zamanda zararsız vakalarda FBR artışı ≤ 2 puan ve P95 karar gecikmesi artışı ≤ 50 ms olmalıdır.

- **Destek koşulu:** ΔUAER < 0 (%95 GA üst sınırı < 0), ΔFBR GA üst sınırı ≤ 2 puan, ΔP95 ≤ 50 ms.
- **Yanlışlanma:** Durum değişimi senaryolarında UAER farkı anlamlı değilse ya da FBR veya gecikme maliyeti eşiği aşıyorsa H2 reddedilir.
- **Not:** Bu hipotezin başarısız olma olasılığı düşüktür, çünkü büyük ölçüde mühendislik doğrulamasıdır. Bu nedenle bilimsel katkı olarak değil, **sistem doğruluğu** olarak raporlanmalıdır.

---

## H3 — Aday A: Kanıt güvenilirliğine göre uyarlamalı doğrulama (tekrar hipotezi)

**H3 (replikasyon):**
Saldırısız, yalnızca operasyonel arıza içeren rejimlerde (eskimiş kanıt, kaynak kesintisi, çelişkili kanıt), kanıt güvenilirliği ve işlem riskine göre doğrulama seçen sistem (**B4-A**), sabit tam doğrulamaya (**B3**) göre:

- UAER bakımından eşdeğersiz değildir (δ = 1 puan), ve
- eşit maliyette daha yüksek güvenli otomatik kapsama sağlar **veya** eşit kapsamada daha düşük maliyetle çalışır.

Bu, VP-Control'ün (arXiv:2609.10969) altyapı işlemleri alanındaki bulgusunun **iade/ödeme alanında tekrarıdır.**

- **Yanlışlanma:** Eşdeğersizlik sağlanmazsa veya maliyet/kapsama kazancı %95 GA'da 0'ı içeriyorsa, VP-Control bulgusu bu alana **genellenemiyor** demektir. Bu da raporlanabilir bir sonuçtur.

---

---

## H1d — Anahtar kökeni (İddia 1, bkz. 11)

Değerleri güvenilir kaynaktan gelen ama **okunacak kaydın anahtarı ajan önerisinden alınan** özelliklerle çalışan yönlendirici (**B4-T**), anahtar kaydırma (D5) saldırısı altında, anahtarı oturuma bağlı yönlendiriciye (**B4-TK**) göre anlamlı ölçüde daha yüksek UAER üretir.

- **Yanlışlanma:** UAER(B4-T) − UAER(B4-TK) farkının %95 GA'sı 0'ı içerirse reddedilir.
- **Pilot durumu (sentetik):** desteklendi; %100.0'a karşı %12.0 (bkz. 11 §4.1).

## H1e — Kalibrasyonun saldırı altına taşınması (İddia 2, bkz. 11)

Yönlendirmesi yalnızca TK-özelliklere bağlı bir sistemde, temiz kalibrasyon verisi üzerinde **kötü durum dönüşümüyle** tahmin edilen fazla risk (B3'e göre), uyarlamalı saldırı altında gerçekleşen fazla riski |fark| ≤ ε içinde öngörür. Manipüle edilebilir özellik kullanan bir sistemde bu öngörü başarısız olur.

- **Ölçüt:** Her δ hedefi için |gerçekleşen − tahmin| (VERIQEN-K) ile aynı değerin naif sistemdeki karşılığı.
- **Yanlışlanma:** VERIQEN-K için fark ε'dan büyükse (öneri: ε = 1 puan) veya naif sistemle VERIQEN-K arasında anlamlı fark yoksa reddedilir.
- **Pilot durumu (sentetik):** niteliksel olarak desteklendi. VERIQEN-K'da fark 0.2–0.8 puan, ancak tutarlı biçimde iyimser (tahmin düşük kalıyor). Naif sistemde fark yaklaşık 90 puan.

> **Not:** H1d ve H1e, 11 numaralı belgedeki pilot sonrası projenin **ana özgünlük iddiaları** oldu. H1b (B3'e karşı eşdeğersizlik) bunların sonucu olarak korunuyor.

## Hipotezler arası bağımlılık

```
H3 (uyarlamalılık maliyet kazandırıyor mu?)
   └─ Evet ise → H1a (bu kazanç saldırı altında güvenliği bozuyor mu?)
                   └─ Evet ise → H1b (güvenilir özellik + monoton taban bozulmayı önlüyor mu?)
H2, H1b'nin "monoton taban" bileşeninin somut doğrulamasıdır; bağımsız da test edilir.
```

H3 reddedilirse (uyarlamalılık hiç kazanç getirmiyorsa) H1'in pratik önemi azalır, ancak H1a yine test edilebilir.

## Kesin üstünlük iddiası için gereken kanıt

"VERIQEN, X'ten üstündür" denebilmesi için **hepsi** sağlanmalıdır:

1. Hipotez, metrik, δ ve analiz planı **deneyden önce** ön kayıt edilmiş olmalı (ör. OSF veya repoda tarihli commit).
2. Geliştirme ve eşik ayarlama vakaları test vakalarından **şablon düzeyinde** ayrılmış olmalı.
3. Etki en az **2 farklı veri kaynağında** (sentetik simülatör + AgentDojo Banking veya τ-bench retail) ve en az **2 farklı ajan LLM'i** ile tekrarlanmış olmalı.
4. Uyarlamalı saldırı protokolü (savunmayı bilen saldırgan) uygulanmış olmalı. Yalnızca statik saldırı kümesiyle elde edilen sonuç "üstünlük" olarak sunulmamalı (Nasr vd. 2025).
5. Holm düzeltmesi sonrası anlamlılık ve δ dışında kalan güven aralığı birlikte sağlanmalı.
6. Sonuçlar bağımsız bir çalıştırmada (farklı tohum, farklı makine) yeniden üretilmiş olmalı.
