# 02 — Ticari ve Açık Kaynak Rakip Analizi

**Tarama tarihi:** 16 Kasım 2026
**Yöntem:** Her ürünün yetenekleri mümkün olduğunca **resmî dokümantasyondan** doğrulandı. Resmî kaynak bulunamayan iddialar "ikincil" olarak işaretlendi.
**İncelenen ürün/çözüm sayısı:** 13

## Etiketler

| Etiket | Anlamı |
|---|---|
| **Var** | Resmî dokümantasyonda açıkça tanımlı. |
| **Kısmi** | Benzer bir yetenek var ama VERIQEN'in tanımından dar; ya da geliştiricinin özel kodla kurması gerekiyor. |
| **Yok** | Ürünün tanımı gereği kapsam dışı (ör. yalnızca gözlemlenebilirlik aracı). |
| **Doğrulanamadı** | Belgelerde bulunamadı. Bu, özelliğin olmadığını **kanıtlamaz.** |

---

## 1. Ürün profilleri

### 1.1 Amazon Bedrock AgentCore — Policy (AWS) ⚠️ en yakın ticari rakip
- **Ne yapıyor:** AgentCore Gateway üzerinden geçen **tüm ajan araç çağrılarını yakalıyor** ve her isteği politika motorundaki politikalara göre değerlendiriyor. Bu değerlendirme araç erişiminden önce yapılıyor. Değerlendirme ajanın kodunun dışında, sınırda gerçekleşiyor; bu yüzden ajan nasıl yazılmış olursa olsun tutarlı ve deterministik uygulanıyor.
- **Politika dili:** Cedar (ayrıca Dogwood). Politikalar OAuth taleplerinden gelen kimlik (principal), araç çağrısı (action) ve Gateway (resource) üzerinden yazılıyor. Araç girdilerine koşul konabiliyor; resmî örneklerde `context.input.passengers == 2` gibi parametre kontrolleri var.
- **Ek:** Doğal dilden Cedar politikası üretme. `LOG_ONLY` modu kararı uygulamadan izleme kaydına yazıyor.
- **Güçlü yanı:** Ajandan bağımsız, deterministik uygulama noktası; kurumsal kimlik entegrasyonu.
- **Sınırlılık (doğrulanabildiği kadarıyla):** Politika, aracın girdi parametrelerini ve kimliği değerlendiriyor. Kararı vermeden önce **dış sistemden kanıt çekip doğrulama** veya **riske göre doğrulama seçimi** belgelerde bulunamadı.
- **Kaynak:** docs.aws.amazon.com/bedrock-agentcore (Policy, Core concepts, Common patterns, GatewayPolicyEngineConfiguration)

### 1.2 NVIDIA NeMo Guardrails (açık kaynak, Apache 2.0)
- **Ne yapıyor:** Beş tür "rail" sunuyor: input, retrieval, dialog, execution ve output. **Execution rails** araç/fonksiyon çağrılarını, argümanlarını ve sonuçlarını doğrulayıp kontrol ediyor. Güncel sürümde (0.23.0) tool-call ve tool-result doğrulaması `IORails` motorunda da var.
- **Güçlü yanı:** Olgun, yaygın; Colang ile esnek akış tanımı; üçüncü taraf sağlayıcı entegrasyonları.
- **Sınırlılık:** Kimlik tabanlı yetkilendirme, dış kanıt kaynağı doğrulaması veya riske göre doğrulama seçimi hazır bir özellik olarak bulunamadı; özel action koduyla yazılabilir.
- **Kaynak:** docs.nvidia.com/nemo/guardrails

### 1.3 Meta LlamaFirewall (açık kaynak)
- **Ne yapıyor:** PromptGuard 2 (jailbreak/enjeksiyon sınıflandırıcısı), AlignmentCheck (LLM ile düşünce zinciri ve hedef uyumu denetimi), CodeShield (güvensiz kod analizi).
- **Raporlanan sonuç (AgentDojo):** ASR %17.63'ten %1.75'e iniyor, utility %47.73'ten %42.68'e düşüyor (ayrıntı: 01).
- **Sınırlılık (makaleye göre):** AlignmentCheck büyük model gerektiriyor ve kendisi de enjeksiyona açık. Güvensiz araç kullanımı henüz kapsamda değil.
- **Kaynak:** arXiv:2505.03574

### 1.4 Lakera Guard (Check Point AI Agent Security)
- **Ne yapıyor:** `/v2/guard` API'si mesajları prompt saldırısı, veri sızıntısı, içerik ihlali ve politika dışı ajan davranışı açısından tarıyor. Resmî dokümana göre kapsamda **araç çağrıları ve araç yanıtları** dahil tüm ajan iş akışı var.
- **Kurumsal durum:** Resmî dokümantasyon ürünü artık "Check Point AI Agent Security" çatısı altında sunuyor. Bir ikincil kaynak şirketin Cisco tarafından satın alındığını yazıyor; bu bilgi resmî dokümanla çelişiyor ve **doğrulanmadı.** Resmî doküman esas alındı.
- **Güçlü yanı:** Düşük gecikmeli, yönetilen API; Gandalf oyunundan gelen büyük saldırı verisi.
- **Sınırlılık:** Bir **tarama/algılama** API'si. Kararı uygulama vermeli. Yetki ve kanıt doğrulama tanımlı değil.
- **Kaynak:** docs.lakera.ai

### 1.5 Invariant Guardrails (Invariant Labs → Snyk)
- **Ne yapıyor:** LLM ve MCP proxy'si olarak araç çağrılarını yakalayıp kurallara göre engelliyor. Python benzeri kural dili ile belirli araçlar, belirli parametre değerleri ve **veri akışı kuralları** yazılabiliyor. Örneğin bir araç çıktısından sonra gelen araç çağrısını yakalayıp güvenilmeyen bir kaynağın e-posta göndermesini engellemek mümkün.
- **Kurumsal durum:** Snyk, Invariant Labs'ı Haziran 2025'te satın aldı (Snyk Labs duyurusu).
- **Güçlü yanı:** Ajan izi (trace) üzerinde akış duyarlı kurallar; kod değişikliği gerektirmeyen ağ geçidi.
- **Sınırlılık:** Kurallar izdeki veriye bakıyor. Dış sistemden bağımsız kanıt doğrulama ve risk/maliyet uyarlaması belgelerde bulunamadı.
- **Kaynak:** explorer.invariantlabs.ai/docs, invariantlabs-ai.github.io/docs

### 1.6 Open Policy Agent (OPA, CNCF)
- **Ne yapıyor:** Genel amaçlı politika karar noktası (PDP), Rego dili. Ajan araç yetkilendirmesi için yerel bir ürün değil, ancak **üçüncü taraf ağ geçitleri** (ör. TrueFoundry AI Gateway'in `mcp_tool_pre_invoke_guardrails` kancası, Strata Maverics MCP Proxy) OPA'yı MCP araç çağrısı öncesi denetimde kullanıyor.
- **Güçlü yanı:** Olgun, test edilebilir, sürüm kontrollü "policy-as-code".
- **Sınırlılık:** Kanıtı OPA'ya girdi olarak getirmek, insan onayı ve risk uyarlaması tamamen entegrasyona bağlı.
- **VERIQEN için anlamı:** VERIQEN'in deterministik kural katmanı için **rakipten çok yapı taşı** (Cedar ile birlikte).

### 1.7 Guardrails AI (açık kaynak)
- **Ne yapıyor:** Hub üzerinden kurulan doğrulayıcılarla (validator) LLM çıktılarını denetliyor ve düzeltiyor. Hub'da 65 doğrulayıcı listeleniyor. `ProvenanceLLM` gibi doğrulayıcılar metni kaynaklara karşı kontrol ediyor.
- **Sınırlılık:** Odak çıktı doğrulaması. Araç çağrısı yükü (payload) doğrulanabilir, ancak çalıştırma izni kararını iş akışı vermeli.

### 1.8 Galileo — Protect → Agent Control
- **Durum:** Resmî dokümana göre **Galileo Protect Haziran 2026 itibarıyla kullanımdan kaldırıldı**; yerine **Agent Control** öneriliyor. Agent Control, Mart 2026'da Apache-2.0 lisansıyla açık kaynak olarak yayımlandı.
- **Ne yapıyor (resmî doküman):** Kontroller tetiklendiğinde ajana `deny` (engelle) ya da `observe` (allow/log/warn) eylemlerinden birini yaptırıyor. Merkezî politika yönetimi sunuyor.
- **Sınırlılık:** Kanıt doğrulama ve risk/maliyet uyarlaması belgelerde bulunamadı. "Steer" eylemi ikincil kaynakta geçiyor.

### 1.9 OpenAI Agents SDK — Guardrails + Human-in-the-loop
- **Ne yapıyor:** Input, output ve tool guardrail'leri var. `needs_approval=True` ya da **çağrı başına karar veren bir asenkron fonksiyon** tanımlanabiliyor; fonksiyon çalışma bağlamını, ayrıştırılmış parametreleri ve çağrı kimliğini alıyor. Onay gerektiğinde çalıştırma duruyor ve serileştirilebilir bir `RunState` ile daha sonra devam ediyor.
- **VERIQEN için anlamı:** "Parametreye/riske göre insan onayına yönlendirme" (Aday D) **resmî SDK'da hazır bir özellik.**

### 1.10 LangChain / LangGraph — HumanInTheLoopMiddleware
- **Ne yapıyor:** Araç çağrısı yürütülmeden önce ajanı durdurup insan incelemesine sunuyor (approve, edit, reject, respond). Bir `when` yüklemi ile **çağrının argümanlarına göre koşullu kesinti** yapılabiliyor (langchain ≥1.3.3). Çağrı başına (per_call) kesinti modu da var.
- **VERIQEN için anlamı:** Aday D bu çerçevede de hazır bir özellik.

### 1.11 AgentOps
- **Ne yapıyor:** Gözlemlenebilirlik: oturum tekrarı (session replay), adım adım yürütme grafikleri, LLM maliyet takibi.
- **Engelleme:** Yok (gözlemlenebilirlik aracı). VERIQEN ile **tamamlayıcı**.

### 1.12 Arize Phoenix (açık kaynak)
- **Ne yapıyor:** OpenTelemetry/OpenInference tabanlı izleme, LLM ile değerlendirme, veri kümeleri ve deneyler. Guardrails AI izlerini yakalayan bir entegrasyonu var.
- **Engelleme:** Yok/doğrulanamadı. VERIQEN deney kayıtları için **altyapı adayı**.

### 1.13 LangSmith (LangChain)
- **Ne yapıyor:** İzleme, çevrim dışı ve çevrim içi değerlendirme, panolar, uyarılar, otomasyon kuralları.
- **Engelleme:** Yok (yürütme öncesi engelleme belgelerde yok). Tamamlayıcı.

---

## 2. Karşılaştırma matrisi

| Özellik | AWS AgentCore Policy | NeMo Guardrails | LlamaFirewall | Lakera Guard | Invariant | OPA (+ağ geçidi) | Guardrails AI | Galileo Agent Control | OpenAI Agents SDK | LangChain HITL | AgentOps | Phoenix | LangSmith | **VERIQEN hedefi** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| İşlem öncesi engelleme | Var | Var | Kısmi | Kısmi | Var | Var* | Kısmi | Var | Var | Var | Yok | Yok | Yok | Var |
| Yetki kontrolü | Var | Kısmi | Yok | Doğrulanamadı | Kısmi | Var* | Yok | Kısmi | Kısmi | Yok | Yok | Yok | Yok | Var |
| Kanıt doğrulama (dış kaynaktan) | Doğrulanamadı | Kısmi | Yok | Yok | Kısmi** | Kısmi* | Kısmi*** | Doğrulanamadı | Yok | Yok | Yok | Yok | Yok | Var |
| Risk uyarlaması | Kısmi | Doğrulanamadı | Doğrulanamadı | Kısmi | Doğrulanamadı | Kısmi* | Doğrulanamadı | Doğrulanamadı | Kısmi | Kısmi | Yok | Yok | Yok | Araştırılacak |
| İnsan onayı | Doğrulanamadı | Doğrulanamadı | Doğrulanamadı | Doğrulanamadı | Doğrulanamadı | Yok* | Yok | Doğrulanamadı | Var | Var | Yok | Yok | Yok | Var |
| Karar açıklaması/denetim kaydı | Kısmi | Kısmi | Kısmi | Kısmi | Kısmi | Kısmi | Kısmi | Kısmi | Kısmi | Kısmi | Kısmi (izleme) | Kısmi (izleme) | Kısmi (izleme) | Var |
| Maliyet optimizasyonu | Doğrulanamadı | Kısmi | Kısmi | Doğrulanamadı | Doğrulanamadı | Yok | Yok | Doğrulanamadı | Yok | Yok | Kısmi (yalnız takip) | Yok | Yok | Araştırılacak |
| Çoklu ajan desteği | Doğrulanamadı | Doğrulanamadı | Doğrulanamadı | Doğrulanamadı | Doğrulanamadı | Doğrulanamadı | Doğrulanamadı | Kısmi | Kısmi | Kısmi | Kısmi (izleme) | Kısmi (izleme) | Kısmi (izleme) | Gelecek aşama |

\* OPA'nın kendisi bir politika motoru; bu yetenekler ağ geçidi entegrasyonuna bağlı.
\*\* Invariant'ta iz içi veri akışı kuralları var; bu "köken" denetimidir, dış sistemden kanıt doğrulama değildir.
\*\*\* Guardrails AI'daki `ProvenanceLLM` metni kaynaklara karşı kontrol ediyor; işlem yetkilendirmesi için değil.

**Okuma notu:** "Risk uyarlaması: Kısmi", ürünün parametreye bağlı koşullu kurala veya koşullu onaya izin verdiği anlamına gelir (ör. tutar eşiği). **Riske göre doğrulama stratejisi seçen** bir ürün hiçbir rakipte belgelenmiş olarak bulunamadı.

---

## 3. Rakiplerin güçlü yanları (VERIQEN'in hafife almaması gerekenler)

1. **Dağıtım ve güven:** AWS, NVIDIA, Meta ve Snyk gibi aktörler kurumsal kimlik, uyum ve ölçek altyapısına sahip. Bir öğrenci projesinin bunlarla "ürün özelliği" düzeyinde yarışması gerçekçi değil.
2. **Deterministik politika uygulama hazır:** Cedar (AgentCore) ve Rego (OPA), VERIQEN'in "kesin yetki ihlali BLOCK" kuralını zaten üretim kalitesinde karşılıyor.
3. **Koşullu insan onayı standartlaştı:** OpenAI Agents SDK ve LangChain HITL, parametreye göre onay istemeyi birkaç satır kodla sağlıyor.
4. **Algılama katmanı olgun:** Lakera Guard, PromptGuard 2 ve NeMo, enjeksiyon tespitinde VERIQEN'in sıfırdan geliştireceği bir modelden çok daha güçlü. Bu yüzden VERIQEN bu katmanı **kullanmalı**, yeniden yazmamalı.

## 4. Doğrulanabilir boşluk (dikkatli ifade)

Belgelerde bulunamayanlar:

- Karar vermeden önce **güvenilir dış sistemden kanıt** çekip işlem parametresine bağlayan ve kanıtın tazeliğini yürütme anında yeniden kontrol eden hazır bir özellik.
- **Riske ve kanıt güvenilirliğine göre hangi doğrulamanın çalıştırılacağını seçen** ve bu seçimin saldırgan tarafından manipüle edilemeyeceğini garanti eden bir mekanizma.

Bu boşluklar **ürün düzeyinde** geçerli. Akademik düzeyde birincisini VP-Control ve PACT, ikincisinin "seçim" kısmını VP-Control büyük ölçüde ele alıyor (bkz. 01, 03).

## 5. En yakın üç ticari rakip

| Sıra | Ürün | Neden |
|---|---|---|
| 1 | **AWS Bedrock AgentCore Policy** | Ajan kodu dışında, araç çağrısından önce, kimlik + parametre tabanlı deterministik yetkilendirme. VERIQEN mimarisinin "Gateway + karar motoru" kısmının üretim karşılığı. |
| 2 | **Invariant Guardrails (Snyk)** | Araç çağrısı yakalama + iz üzerinde veri akışı (köken) kuralları. VERIQEN'in "kanıt kökeni" fikrine en yakın ticari özellik. |
| 3 | **OpenAI Agents SDK (needs_approval + tool guardrails)** | Çağrı başına koşullu insan onayı ve devam ettirilebilir durum. VERIQEN'in REVIEW yolunun hazır karşılığı. |

## 6. Kalite kontrol (bu aşama)

| Kontrol | Sonuç |
|---|---|
| Özellikler resmî belgeyle destekleniyor mu? | AgentCore, NeMo, Lakera, Invariant, Galileo, OpenAI SDK, LangChain ve LangSmith için resmî doküman sayfaları kullanıldı. AgentOps için resmî GitHub/doküman özetleri kullanıldı. |
| İkincil kaynak kullanımı | Lakera'nın kurumsal durumu ve Galileo Agent Control'ün "steer" eylemi ikincil kaynakta geçiyor; matriste bunlara dayanılmadı. |
| "Yok" ile "Doğrulanamadı" ayrımı | Yalnızca ürünün tanımı gereği kapsam dışı olduğu durumlarda (gözlemlenebilirlik araçları) "Yok" kullanıldı. |
| Eksik | Fiyatlandırma ve performans (gecikme) değerleri bağımsız testle doğrulanmadı. Ürünlerin hiçbiri bizim tarafımızdan çalıştırılmadı. |
