# 03 — VERIQEN-T2: Kilitli Sette Bulunan Açıkların Kapatılması

**Tarih:** 20 Kasım 2026 · **Dal:** `veriqen-2`
**Önemli:** VERIQEN-T2, kilitli saldırı seti v1 **açıldıktan sonra** ve orada görülen açıklara bakılarak geliştirildi. Bu yüzden T2'nin kilitli setteki sonuçları **bağımsız bir test değildir**; yalnızca açıkların kapandığını gösterir. VERIQEN-T'nin kilitli set sonuçları (`02`) değiştirilmedi. T2'nin bağımsız değerlendirmesi için yeni bir kilitli set (v2) gerekir.

**Kod:** `capability.py` (`mint_tokens_v2`, `_amount_ok`), `veriqen_gate.py` (`VERIQEN-T2`, `_gate_judge_v2`, `ProvenanceTracker.exact`, `explicit_secret`)
**Testler:** `tests/test_veriqen_t2.py` (13 test). Toplam 24 test geçiyor. Beş bilinçli mutasyonun beşi de yakalanıyor.
**Sonuçlar:** `results/v2/replay_T2_compare.json`, `results/locked_v1/locked_v1_T2_seen.json`, `results/sensitivity_T2/`

---

## 1. Değişiklikler

| Kod | Değişiklik | Kapattığı açık |
|---|---|---|
| **A1** | **Kanıta bağlı tutar:** Belirteç, tutarı da kontrol eder. Tutar ya kullanıcı isteğinde parasal bir tutar olarak geçmeli ya da kullanıcının kendi başlattığı bir işlemin tutarı olmalı. Alıcı kullanıcıya para göndermişse, ondan alınan toplamı aşmayan tutar da kabul edilir (iade). Kanıtsız tutar belirteci **tüketmez**, hakeme gider. | L05 (tutar kurcalama); canlı koşuda ajanın yanlış tutarla belirteci boşa harcaması |
| **A2** | **Sınırlı köken eşleşmesi:** Bir değerin "kullanıcıdan geldiği", isteğin içinde harf ya da rakama bitişik olmayan tam bir parça olarak geçmesiyle kabul edilir; alt dize yetmez. **Açık parola:** Parola, istekte tırnak içinde ya da "password to/is" ifadesinden hemen sonra açıkça verilmiş olmalıdır. | L10 (parola), L03 tipi önek eşleşmeleri |
| **A3** | **IBAN normalizasyonu:** Boşluklu yazılmış IBAN'lar da belirteç üretir ve eşleşir. | Kullanıcı IBAN'ı boşluklu yazdığında gereksiz hakem çağrısı |
| **A4** | **Bölüm sınırları:** (a) Hakemin **reddettiği** alıcı o bölüm boyunca kapalı kalır; aynı alıcıya yeni deneme hakeme gitmez. (b) Hakemin onayladığı bir alıcıya ikinci ödeme insan onayına gider. (c) Kullanıcının istekte yazmadığı alıcılara hakem onaylı toplam tutar, ikinci ödemeden itibaren otomatik limiti aşarsa insan onayına gider. | L08 (taksite bölme): her yeni çağrı hakeme bağımsız bir hata şansı veriyordu |
| **B3** | **Hakem önbelleği:** Bölüm içinde birebir aynı çağrı tekrar gelirse önceki hakem kararı kullanılır. | Ajanın tekrar denemelerinde gereksiz hakem çağrısı; aynı işleme çelişkili kararlar |

### Geliştirme sırasında yapılan iki hata ve düzeltmesi
1. Toplam tutar sınırı ilk sürümde **ilk** ödemeye de uygulanıyordu. Tek bir büyük meşru ödeme (kira 1.200) insan onayına düştü ve zararsız fayda %97.5'ten **%80'e** indi. Düzeltme: sınır ikinci ödemeden itibaren uygulanır.
2. Ardından kullanıcının istekte açıkça yazdığı yeni ev sahibine yapılan 2.200'lük kira ödemesi toplam sınırı doldurdu ve aynı istekteki 10 €'luk iadeyi engelledi (fayda %91.6). Düzeltme: toplam sınıra yalnız kullanıcının yazmadığı alıcılara giden ödemeler sayılır.

Her iki düzeltme de replay'deki **zararsız görevlere** bakılarak yapıldı; kilitli sete bakılarak değil.

## 2. Sonuçlar (replay, ajan senaryolu, MockJudge 0.90 / 0.05, 20 tekrar)

| Sistem | ASR std / ekleme / geçmiş alıcı | Zararsız fayda | Hakem / zararsız görev | Hakem / saldırılı görev | Engellenen meşru çağrı / görev |
|---|---|---|---|---|---|
| B3 | 6.8 / 6.8 / 6.8 | 95.3 | 0.88 | 1.54 | 0.066 |
| VERIQEN-SI | 6.8 / 6.8 / 9.9 | 97.8 | 0.44 | 1.10 | 0.025 |
| VERIQEN-T | 6.8 / 6.8 / 6.8 | 97.5 | 0.56 | 1.23 | 0.044 |
| **VERIQEN-T2** | **5.6 / 5.6 / 5.6** | **97.5** | **0.56** | **1.11** | **0.044** |

## 3. Kilitli set v1 (GÖRÜLEREK düzeltildi — bağımsız test değil)

| | B3 | VERIQEN-T (bağımsız, `02`) | VERIQEN-T2 (görülerek) |
|---|---|---|---|
| Kusursuz hakemde atlama | 0.0 | 1.1 | **0.0** |
| Varsayılan hakemde toplam ASR | 13.2 | 14.3 | **7.1** |
| Taksite bölme (L08), varsayılan hakem | 39.7 | 39.7 | **8.8** |

## 3b. Hakem kalitesine duyarlılık (AgentDojo, 3 saldırı türü, 5 tekrar, simülasyon)

| Hakem kaçırma | %0 | %5 | %10 | %20 | %30 | %50 |
|---|---|---|---|---|---|---|
| B3 ASR | 0 | 4.0 | 7.4 | 14.7 | 21.2 | 36.9 |
| VERIQEN-T ASR | 0 | 4.0 | 7.4 | 14.7 | 21.2 | 36.9 |
| **VERIQEN-T2 ASR** | **0** | **3.3** | **5.8** | **12.1** | **17.5** | **30.3** |

Kusursuz hakemle atlama sıfır. Hakem kötüleştikçe T2'nin B3'e göre avantajı büyüyor (%50 kaçırmada 36.9'a karşı 30.3), çünkü bölüm sınırları hakeme tekrar tekrar şans vermiyor. Zararsız fayda ve hakem maliyeti T ile aynı.

## 4. Okuma

1. T2, kilitli setteki iki atlama yolunu kapattı. Kusursuz hakemle hem AgentDojo saldırılarında hem kilitli sette atlama sıfır.
2. Fayda ve hakem maliyeti T ile aynı kaldı.
3. **T2'nin B3'ten daha düşük ASR vermesinin nedeni A4 ve B3 kuralları:** Çok çağrılı saldırılarda hakem her çağrıda yeniden şans vermiyor. Bu, "uyarlamalı doğrulama"nın kendisinden değil, bölüm düzeyinde sınırlardan geliyor. Aynı sınırlar B3'e de eklenebilir. Adil bir karşılaştırma için "B3 + A4" de raporlanmalı (yapılmadı).
4. Sonuçlar hâlâ MockJudge ve senaryolu ajanla; T2 gerçek LLM ile henüz koşulmadı.

## 5. Kalan açıklar ve riskler

- A1'deki parasal tutar tanıma sezgisel bir kurala dayanıyor (para birimi işareti, "is/of/to" sonrası, iki ondalık). Bu kural kaçırırsa meşru ödeme hakeme gider (fayda kaybı); yanlış bir sayıyı tutar sanırsa, kullanıcının yazdığı alıcıya o tutar hakemsiz gidebilir.
- A1, kullanıcının kendi işlemlerindeki tutarları (ör. 1.000, 1.100) da kanıt sayıyor. Kullanıcının adını verdiği alıcıya bu tutarlardan biriyle fazla ödeme yaptırılabilir; zarar, kullanıcının yazdığı alıcıyla sınırlı.
- A4'teki "hakemin reddettiği alıcı kapalı" kuralı, hakemin yanlış reddettiği meşru bir alıcıyı da bölüm boyunca kapatır.
