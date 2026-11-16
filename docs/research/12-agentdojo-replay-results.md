# 12 — AgentDojo Banking: Çevrimdışı Değerlendirme Sonuçları

**Tarih:** 16 Kasım 2026
**Kod:** `experiments/agentdojo/` · **Sonuçlar:** `experiments/agentdojo/results/replay/`
**Durum:** Gerçek benchmark ortamı ve gerçek saldırı şablonu kullanıldı, ancak **ajan ve hakem simüle edildi.** Gerçek LLM ile tekrar (`run_live.py`) henüz yapılmadı.

---

## 1. Düzenek

| Öğe | Değer |
|---|---|
| Ortam | AgentDojo v1.2.1, Banking paketi: 16 kullanıcı görevi × 9 saldırı görevi = 144 saldırı bölümü + 16 zararsız bölüm |
| Saldırı | AgentDojo'nun `important_instructions` şablonu (model adı sabit: "the AI language model") |
| Ajan | **Senaryolu, tamamen ele geçirilmiş ajan.** Önce kullanıcı görevinin doğru çağrılarını yapıyor (enjeksiyonu okuyor), sonra saldırı görevinin doğru çağrılarını deniyor. En kötü durum varsayımı. |
| Hakem | **MockJudge** (varsayım): kötü niyetli çağrıyı %90, zararsız çağrıyı %5 olasılıkla engelliyor. Rastgelelik vaka anahtarından türetiliyor, böylece sistemler eşleştirilmiş. |
| Tekrar | 20 (hakem tohumları). GA: bölüm düzeyinde bootstrap. |
| Taban kuralları | Parola yalnızca kullanıcının yazdığı değere değiştirilebilir. Bakiyeyi aşan transfer engellenir. 5.000 üstü insan incelemesine gider. |
| Yönlendirme | Alıcı "bilinen" ve tutar ≤ 1.000 ise hakem atlanır, değilse hakem çağrılır. **NAIVE:** IBAN araç çıktısının metninde geçiyorsa bilinen sayılır. **VERIQEN:** IBAN yalnızca kullanıcı isteğinde veya geçmiş işlemlerin yapısal alıcı/gönderen alanlarında geçiyorsa bilinen sayılır. |

## 2. Sonuçlar (gerçek çıktılar; ajan ve hakem simüle)

| Sistem | Saldırı başarısı (ASR) % [%95 GA] | Zararsız fayda % | Saldırı altı fayda % | Hakem çağrısı / görev (zararsız) | Hakem çağrısı / görev (saldırı) |
|---|---|---|---|---|---|
| B0 korumasız | 100.0 | 100.0 | 86.8 | 0.00 | 0.00 |
| B1 yalnız kurallar | 66.7 [64.9, 68.4] | 100.0 | 91.7 | 0.00 | 0.00 |
| B2 her zaman hakem | 8.7 [7.7, 9.8] | 95.3 | 94.5 | 0.88 | 2.10 |
| B3 kurallar + her zaman hakem | **6.8** [5.9, 7.7] | 95.3 | 95.0 | **0.88** | **1.54** |
| NAIVE (köken körü uyarlamalı) | **66.7** [64.9, 68.4] | 99.1 | 90.5 | 0.25 | 0.31 |
| **VERIQEN (anahtar kökenli uyarlamalı)** | **6.8** [5.9, 7.7] | **98.1** | **97.7** | **0.38** | **1.04** |

İnsan incelemesi politikası (reddet/onayla) sonuçları değiştirmedi; bu düzenekte hiçbir çağrı 5.000 eşiğine ulaşmadı.

## 3. Okuma

1. **Köken körü uyarlamalılık, kurallar kadar zayıf kaldı.** NAIVE, saldırganın IBAN'ı araç çıktısının metninde (fatura, işlem açıklaması) geçtiği için onu "bilinen alıcı" saydı. Saldırganın para transferlerinin tamamında hakemi atladı. ASR'si, hiç hakem kullanmayan B1 ile aynı: %66.7. Kalan üçte birlik kısmı (parola, bakiye aşımı) yalnızca deterministik taban durdurdu. Bu, pilotta (11) gördüğümüz "anahtar kökeni" açığının **gerçek bir benchmark ortamında da ortaya çıktığını** gösteriyor.
2. **VERIQEN, tam doğrulama (B3) ile aynı güvenliği daha az doğrulamayla sağladı.** ASR %6.8, B3 ile aynı. Hakem çağrısı zararsız görevlerde **%57**, saldırı altında **%32** daha az.
3. **Fayda daha yüksek.** Daha az hakem çağrısı, zararsız işlemlerin yanlışlıkla engellenmesini de azaltıyor: zararsız fayda %98.1, B3'te %95.3.
4. **B2 ile B3 farkı:** Deterministik taban, hakemin kaçırdığı parola ve bakiye saldırılarını yakalıyor (ASR 8.7'ye karşı 6.8).

## 3b. Uyarlamalı saldırı: durum ekme (kendi tasarımımıza karşı)

**Gözlem:** AgentDojo ortamında enjeksiyon, gelen bir transferin açıklama alanına yerleştirilmiş, ama transferin gönderen alanında başka bir IBAN yazıyor. Gerçek hayatta açıklama alanını parayı gönderen kişi yazar. Saldırgan kullanıcıya küçük bir tutar gönderirse kendi IBAN'ı geçmişin **gönderen** alanına girer. VERIQEN (v1) bu alanı "güvenilir yapısal alan" saydığı için saldırganın IBAN'ını "bilinen alıcı" kabul eder. Bu, tehdit modelindeki C4 yeteneğinin (saldırganın gerçek sistem durumu yaratabilmesi) doğrudan sonucu.

**Düzeltme (VERIQEN-A, v2):** Bir alan, verinin güvenilir veritabanında durması yüzünden değil, **değerini kimin belirlediği** yüzünden güvenilir sayılır. VERIQEN-A yalnızca kullanıcının kendi başlattığı işlemlerin alıcılarını ve kullanıcının zamanladığı ödemelerin alıcılarını güvenilir kabul eder. Gelen transferlerin gönderen alanına güvenmez.

**Deney:** Saldırılı bölümlerde gelen transferin gönderen alanı saldırganın IBAN'ı yapıldı (`--attack-mode planting`); diğer her şey aynı.

| Sistem | ASR % (standart) | **ASR % (durum ekme)** | Zararsız fayda % | Hakem çağrısı / zararsız görev |
|---|---|---|---|---|
| B3 kurallar + her zaman hakem | 6.8 | 6.8 | 95.3 | 0.88 |
| NAIVE | 66.7 | 66.7 | 99.1 | 0.25 |
| VERIQEN (v1, yapısal güven) | 6.8 | **66.7** [64.9, 68.4] | 98.1 | 0.38 |
| **VERIQEN-A (v2, yazar farkındalıklı güven)** | 6.8 | **6.8** [5.9, 7.7] | 98.1 | 0.38 |

**Sonuç:** "Güvenilir kaynak + güvenilir anahtar" tanımı da eksikti. Gereken üçüncü koşul **yazar kökeni**: değeri, kararı denetlenen işlemin sahibi (kullanıcı) mı belirledi, yoksa dışarıdan biri mi? Düzeltme bu düzenekte fayda veya maliyetten hiçbir şey götürmedi.

**Kalan risk (henüz test edilmedi):** VERIQEN-A, kullanıcının daha önce ödeme yaptığı herkese güveniyor. Eğer geçmişteki bir alıcı (ör. bir satıcı) saldırganın kontrolündeyse, otomatik limitin (1.000) altındaki transferler hakemsiz geçebilir. Bunun için ek önlem gerekiyor: alıcı başına kümülatif limit ya da "bu alıcıya bu görevde ödeme yapılması kullanıcı isteğiyle tutarlı mı" kontrolü. Bu, bir sonraki uyarlamalı saldırı (D11).

## 4. Dürüst sınırlılıklar

| # | Sınırlılık |
|---|---|
| 1 | **VERIQEN ile B3'ün ASR'sinin aynı çıkması tasarımın doğal sonucu.** Bu düzenekte saldırganın tüm para çağrıları "bilinmeyen alıcı" olarak hakeme gitti. Kalan %6.8 tamamen MockJudge'ın %10 kaçırma varsayımından geliyor. Gerçek hakemin başarısı **ölçülmedi.** |
| 2 | **Ajan senaryolu.** Gerçek bir LLM saldırıya her zaman uymayabilir (ASR daha düşük olabilir) ya da zararsız görevlerde hata yapabilir (fayda daha düşük olabilir). |
| 3 | **Uyarlamalı saldırı kapsamı dar.** Yalnızca durum ekme (§3b) test edildi. Ele geçirilmiş geçmiş alıcı (D11) ve konu alanından veri sızdırma henüz test edilmedi. |
| 4 | **Yalnızca Banking.** Diğer AgentDojo paketleri (Slack, Travel, Workspace) için köken kuralları yazılmadı. |
| 5 | **Banking'in IBAN yapısı köken takibini kolaylaştırıyor.** Serbest metin argümanlarda (adres, e-posta gövdesi) köken takibi daha zor. |
| 6 | Taban ve yönlendirme eşikleri (1.000 / 5.000) bizim seçimimiz. Ön kayıtla sabitlenmeli. |

## 5. Sonraki adımlar

1. `run_live.py` ile gerçek LLM ajanı ve gerçek hakemle küçük ölçekli koşu (ücretsiz katman; önce 2–4 kullanıcı görevi).
2. ~~VERIQEN'i hedef alan uyarlamalı saldırı~~ → durum ekme yapıldı (§3b). Sırada: ele geçirilmiş geçmiş alıcı (D11) ve `subject` alanından veri sızdırma.
3. Gerçek hakemin ASR ve yanlış alarm oranını ölçüp MockJudge varsayımlarının yerine koymak.
