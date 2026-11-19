# 09 — Ek Tarama: Aday F ("Doğrulama Düşürme") için Hedefli Literatür Kontrolü

**Tarih:** 16 Kasım 2026
**Amaç:** "Risk-uyarlamalı doğrulamanın, saldırgan tarafından işlemi hafif kontrol yoluna itecek şekilde manipüle edilmesi" fikrinin daha önce yayımlanıp yayımlanmadığını kontrol etmek.
**Arama ekseni:** adaptive verification downgrade; tiered guardrail escalation evasion; risk score manipulation in agent authorization; selective defense adaptive evasion.

---

## 1. Sonuç (özet)

**Tehdidin kendisi biliniyor, ancak sistematik ölçümü ve buna karşı tasarım garantisi bu taramada bulunamadı.**

| Ne | Durum |
|---|---|
| "Saldırgan güven/risk eşiğini manipüle edebilir" fikri | **Biliniyor.** Tehdit taksonomilerinde ve uygulayıcı yazılarında adı geçiyor. |
| "Risk puanı deterministik kuralın yerine geçmemeli" ilkesi | **Biliniyor.** Mimari derlemede ilke olarak yazılmış. |
| "Risk tahmini modelden değil güvenilir kaynaktan gelmeli" ilkesi | **Biliniyor.** Irreversibility Budget çalışmasında tasarım ilkesi olarak uygulanmış (farklı problem: bütçe tabanlı kabul kontrolü). |
| Araç çağrısı yetkilendirmesinde **uyarlamalı doğrulama seçiminin** düşürme saldırısıyla **deneysel olarak** ölçülmesi | **Bulunamadı.** |
| Bu saldırıya karşı **monoton taban + güvenilir özellik** tasarımının biçimsel önerme ve deneyle sınanması | **Bulunamadı.** |
| Doğrulama/denetim sistemlerinin saldırgan değerlendirmesinin genel olarak eksik olduğu | Güncel bir derleme bunu açıkça bir araştırma boşluğu olarak tanımlıyor. |

**Etki:** Aday F'nin katkısı **"yeni bir fikir"** olarak değil, **"bilinen ama ölçülmemiş bir tehdidin ilk sistematik ölçümü, açık test seti ve garantili tasarım"** olarak konumlandırılmalı. Bu daha dar ama daha savunulabilir bir iddia.

---

## 2. Bulunan ilgili çalışmalar

### 2.1 Toward Safe LLM Agents: A Survey of Specification, Verification, and Enforcement (arXiv:2608.14590)
Derleme, araştırma boşlukları arasında doğrulama sistemlerinin saldırgan dayanıklılığını sayıyor. AgentSpec tarzı monitörlerin prompt injection ile aşıldığının gösterildiğini ve üretim düzeyi guardrail'lerin hâlâ %1.75 saldırı başarısına izin verdiğini hatırlatıyor. Doğrulama ve uygulama (enforcement) sistemlerinin saldırgan değerlendirmesinin literatürde sistematik olarak bulunmadığını belirtiyor.
**VERIQEN için anlamı:** Aday F'nin hedeflediği boşluğun bağımsız bir derlemece de tanımlandığını gösteriyor. Başvuruda motivasyon atfı olarak kullanılabilir.

### 2.2 Authorization Architectures for Tool-Using AI Agents (arXiv:2609.15906)
Yazarlar: Surapani, Kakitapelli, Morampudi, Padi. Tür: derleme ve referans mimari; deney yok.
- Bölüm 5.4: risk puanlamanın pazarlık edilemez kısıtlar için deterministik kontrollerin yerine geçmemesi gerektiğini söylüyor. Bu, **monoton taban** fikrinin ilke düzeyinde zaten ifade edildiğini gösteriyor.
- Saldırganın risk puanını manipüle etmesini veya işlemi düşük denetimli yola yönlendirmesini **ele almıyor.**
- Puanlayıcının özellikleri arasında güvenilmeyen çıktının etkisi gibi "bağlam riski" var, ama özelliklerin yalnızca güvenilir kaynaklardan gelmesi şart koşulmuyor.
- Bölüm 5.2: çalışma zamanının özellikleri güvenilir biçimde sağlayamadığı durumda kararın, denetlediği modelin ürettiği özelliklere dayanabileceği uyarısı var. Ancak bu, saldırgan manipülasyonu olarak değil, öznitelik kalitesi sorunu olarak çerçevelenmiş.

**VERIQEN için anlamı:** Monoton taban ilkesi tek başına katkı olarak sunulmamalı; bu çalışmaya atıfla "ilkeyi biçimselleştirip deneyle sınıyoruz" denmeli.

### 2.3 Security Considerations for Multi-agent Systems — NIST RFI 2026-00206 yanıtı (arXiv:2603.09002)
Yazarlar: Nguyen, Ndebugre, Arremsetty (Crew Scaler). Tür: tehdit taksonomisi ve çerçeve karşılaştırması; 193 tehdit maddesi.
- **RATC_4_1 "Confidence Threshold Manipulation":** prompt injection'ın ajanın güven puanını şişirip, güven düzeyine göre kalibre edilmiş bir kapıdan kötü niyetli işlemi geçirmesi.
- İlgili maddeler: tehlikeli işlemlerin zararsız terimlerle sunulması (risk soyutlama), onay yorgunluğu, otomatik onaylı zaman aşımlarının istismarı, aracı ajan üzerinden yükseltme.
- **Deney yok.** Önerilen savunmalar: güveni geçmiş doğrulukla karşılaştırma, çok faktörlü değerlendirme, zaman aşımında varsayılan ret.

**VERIQEN için anlamı:** Aday F'nin tehdidine çok yakın bir madde **adlandırılmış**. Başvuruda bu çalışma "tehdidi tanımlayan ama ölçmeyen" kaynak olarak anılmalı. Fark: VERIQEN güven puanını değil, doğrulama planı seçimini hedef alan saldırıyı ölçüyor ve tasarım garantisi öneriyor.

### 2.4 The Irreversibility Budget (arXiv:2609.00275) ⚠️ yakın ilke
Yazarlar: Mohammadi, Bindschaedler (MPI-SWS). Agentic OS Workshop 2026.
- Problem farklı: filo düzeyinde, kişi başına geri döndürülemez riskin bütçelenmesi ve bütçe aşılırsa işlemin reddedilmesi (kabul kontrolü).
- **Kritik ortak nokta:** Risk ücretleri modelden değil, efekt tanımlarından ve güvenilir bir fiyatlandırma servisinden geliyor. Tanınmayan efektler en pahalı eşleşen sınıftan ücretlendiriliyor. Bu, VERIQEN'in "güvenilir özellik" ve "belirsizse en sıkı sınıf" ilkelerinin farklı bir problemde uygulanmış hâli.
- Deneylerinde yanlış beyan (misdeclaration) gerçek bir zayıflık: işbirliği yapan transferlerin iade edilebilir olarak yanlış sınıflanması, aşım oranını çalıştırmaların %77'sine çıkarıyor.

**VERIQEN için anlamı:** "Risk tahminini güvenilir kaynaktan al" ilkesi yeni değil. VERIQEN bu çalışmaya atıf yapmalı. Bulgusu (yanlış sınıflandırma = büyük kayıp) ise Aday F'nin motivasyonunu destekliyor. VERIQEN'in farkı: işlem düzeyinde **doğrulama planı seçimi** ve **seçimi hedef alan uyarlamalı saldırıların** ölçülmesi.

### 2.5 Uygulayıcı kaynakları (akademik değil)
Bir güvenlik blog yazısı, ucuz sınıflandırıcıdan sonra belirsiz durumlar için hakem LLM'e giden zincirli yapıların maliyete yardım ettiğini, ama saldırganın ikinci aşamadan kaçmak için birinci aşamayı hedefleyebileceğini not ediyor. Bu, fikrin sektörde sezgisel olarak bilindiğini gösteriyor. Ölçüm veya garanti sunmuyor.

### 2.6 İlgili ama farklı problemler
- **RerouteGuard (arXiv:2601.21380):** Maliyet için sorgu yönlendiren LLM router'ların, sorguya eklenen tetikleyicilerle yönlendirme kararının manipüle edilebildiğini gösteriyor. Bu saldırılar maliyeti artırabiliyor, kaliteyi düşürebiliyor ve güvenlik guardrail'lerini atlatabiliyor. Problem model seçimi; araç çağrısı yetkilendirmesi değil. **Ancak saldırı yöntemleri (beyaz/gri kutu tetikleyici arama) VERIQEN'in saldırı protokolüne doğrudan uyarlanabilir.**
- **Provably Secure Agent Guardrail / ePCA (arXiv:2605.29251):** Ajanın niyetini birinci dereceden mantık kısıtlarına çevirip biçimsel doğrulama yapıyor; LLM politikasının kendisini düşman sayıyor. Değerlendirilen senaryolarda sıfır saldırı başarısı ve sıfır yanlış pozitif raporluyor. Uyarlamalı seçim yok; tam doğrulama yaklaşımı (B3 sınıfı).

---

## 3. Aday F için güncellenmiş katkı ifadesi

**Eski (fazla geniş):** "Uyarlamalı doğrulamanın saldırgana karşı dayanıklı hâlini öneriyoruz."

**Yeni (önerilen):**
> "Risk-uyarlamalı doğrulama yönlendirmesine yönelik 'doğrulama düşürme' tehdidi tehdit taksonomilerinde adlandırılmış (Nguyen vd. 2026) ve 'risk puanı deterministik kontrolün yerine geçmemeli' ilkesi mimari derlemelerde önerilmiştir (Surapani vd. 2026). Ancak bu tehdidin araç çağrısı yetkilendirmesinde **deneysel olarak ölçüldüğü** ve buna karşı **güvenilir-özellik kısıtı ile monoton tabanın** biçimsel önerme ve uyarlamalı saldırılarla **sınandığı** bir çalışmaya rastlanmamıştır. Katkılarımız: (1) tehdit modeli ve Downgrade-ASR metriği; (2) açık kaynak saldırı test seti; (3) güvenilmeyen kanallardan bağımsız yönlendirme ve monoton taban tasarımı ile bunun eşdeğersizlik (non-inferiority) testi."

## 4. 03'teki puana etkisi

Aday F'nin "Literatürden farklılaşma" puanı **20 → 17** olarak düşürüldü. Sebebi: Irreversibility Budget'ta güvenilir kaynaklı risk tahmini ilkesinin, mimari derlemede deterministik taban ilkesinin ve NIST RFI yanıtında tehdidin adlandırılmış olması. Toplam puan **74 → 71.** Aday F yine en yüksek puanlı aday (G: 69).

## 5. Hâlâ açık olanlar

- Bu tarama da web araması düzeyinde. ICML/NeurIPS/USENIX Security/CCS/IEEE S&P 2026 kabul listelerinin başlık bazında taranması önerilir (yarım gün).
- Irreversibility Budget ve 2608.14590 derlemesinin tam metni okunmalı.
- Danışmana gösterilmeden önce 2.3'teki RATC_4_1 maddesinin tam metni okunmalı.
