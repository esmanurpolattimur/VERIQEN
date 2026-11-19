# 01 — Literatür Taraması

**Proje:** VERIQEN — Otonom Yapay Zekâ Ajanları için Kanıt Temelli ve Risk Uyarlamalı İşlem Denetim Sistemi
**Tarama tarihi:** 16 Kasım 2026
**Kapsam:** 30 çalışma (24'ü ayrıntılı tablo, 6'sı ek tarama listesi)

---

## 0. Okuma notları ve doğrulama düzeyi

Her çalışmanın yanında doğrulama düzeyi belirtilmiştir:

| Etiket | Anlamı |
|---|---|
| **[T]** | Sayısal sonuçlar makalenin deney tablosundan (arXiv HTML sürümü) okundu. |
| **[M]** | Sayılar makale metninden (giriş/sonuç/özet bölümü) alındı; tablo ayrıca açılamadı. |
| **[Ö]** | Yalnızca özet (abstract) veya yayın sayfası düzeyinde doğrulandı. |
| **[İ]** | İkincil kaynak (özet sitesi) üzerinden; birincil kaynakla tekrar kontrol edilmeli. |

**Önemli uyarılar:**

- Farklı benchmark'lardaki yüzdeler doğrudan karşılaştırılamaz. AgentDojo içinde bile model, saldırı türü ve AgentDojo sürümü (v1, v1.1, v1.2) farklı olduğunda sayılar kıyaslanamaz.
- Bu tarama tek kişilik bir masa başı çalışmasıdır. "Bulunamadı" ifadesi "yok" anlamına gelmez.
- Bazı makalelerde tablo ile metin arasında tutarsızlık var; bunlar ilgili satırda belirtildi.

---

## 1. Yönergede adı geçen başlıkların bibliyografik kontrolü

| Yönergedeki ad | Durum | Açıklama |
|---|---|---|
| AgentDojo | ✅ Doğrulandı | Debenedetti vd., NeurIPS 2024 Datasets & Benchmarks, arXiv:2406.13352 |
| τ-bench | ✅ Doğrulandı | Yao vd., arXiv:2406.12045 (Sierra) |
| CaMeL | ✅ Doğrulandı | "Defeating Prompt Injections by Design", arXiv:2503.18813 (Google DeepMind / ETH) |
| FAVA | ⚠️ Var ama **konu farklı** | FAVA, "Fine-grained Hallucination Detection and Editing for Language Models" (Mishra vd., arXiv:2401.06855) çalışmasındaki modeldir. Ajan güvenliği veya yetkilendirme çalışması **değildir**; LLM çıktısındaki olgusal halüsinasyonları tespit edip düzeltir. VERIQEN ile ilişkisi yalnızca "kanıta göre doğrulama" düzeyinde dolaylıdır. |
| IPIGuard++ | ❌ **Bulunamadı** | "IPIGuard++" adıyla yayımlanmış bir çalışma bulunamadı. Bulunan en yakın çalışma **IPIGuard** (An vd., EMNLP 2025, arXiv:2508.15310). IPIGuard makalesinin metninde de "IPIGuard++" geçmiyor. Bu ad muhtemelen bir yapay zekâ özetinden ya da hatalı bir atıftan gelmiştir; kaynakçada kullanılmamalıdır. |

---

## 2. Ayrıntılı çalışma tabloları

Tablolar dört kümede toplandı:

- **K1:** Benchmark ve saldırılar
- **K2:** Sistem düzeyinde savunmalar (yetki ve bilgi akışı)
- **K3:** Algılama ve hizalama tabanlı savunmalar
- **K4:** Seçici/uyarlamalı doğrulama, belirsizlik ve insan onayı (VERIQEN'in özgünlük iddiasına en yakın küme)

### K1 — Benchmark ve saldırılar

#### 1. AgentDojo [T]
| Alan | İçerik |
|---|---|
| Başlık | AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents |
| Yazarlar | Edoardo Debenedetti, Jie Zhang, Mislav Balunović, Luca Beurer-Kellner, Marc Fischer, Florian Tramèr |
| Yıl / Kaynak | 2024 / NeurIPS 2024 Datasets and Benchmarks Track |
| DOI / URL | https://doi.org/10.48550/arXiv.2406.13352 |
| Problem | Güvenilmeyen veri üzerinde araç çalıştıran ajanların prompt injection'a karşı dayanıklılığını ölçmek. |
| Yöntem | Genişletilebilir ortam; kullanıcı görevleri, enjeksiyon görevleri, saldırı ve savunma bileşenleri. |
| Veri kümesi | 4 paket (Workspace, Slack, Travel, Banking), 74 araç, 97 kullanıcı görevi, 27 enjeksiyon görevi, 629 güvenlik vakası (Tablo 1). |
| Karşılaştırmalar | 10 LLM; tool filter, PI dedektörü, data delimiting, prompt sandwiching savunmaları. |
| Metrikler | Benign utility, utility under attack, targeted ASR. |
| Sayısal sonuçlar | Tablo 3 (%95 GA ile): GPT-4o benign utility 69.00, saldırı altında utility 50.08, targeted ASR 47.69. Claude 3.5 Sonnet: 78.22 / 51.19 / 33.86. GPT-4o'da tool filter ASR'yi 7.5'e düşürüyor. |
| Sınırlılıklar | Yazarlara göre saldırı ve savunmalar "görece basit". Tool filter, gerekli araçlar saldırıyı da mümkün kılıyorsa çalışmıyor (vakaların %17'si). Çok görevli oturumlar ve çok modlu ajanlar kapsam dışı. |
| VERIQEN ilişkisi | Fiilî standart değerlendirme ortamı. **Banking paketi (send_money)** VERIQEN'in para hareketi senaryosuna en yakın hazır test zemini. |
| Not | Tablo 1 başlığında 70 araç yazıyor, sütun toplamı 74. Girişteki "%66'dan az" ifadesi Tablo 3 ile çelişiyor (v3 güncellemesi). |

#### 2. τ-bench [Ö]
| Alan | İçerik |
|---|---|
| Başlık | τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains |
| Yazarlar | Shunyu Yao, Noah Shinn, Pedram Razavi, Karthik Narasimhan |
| Yıl / Kaynak | 2024 / arXiv preprint (Sierra) |
| DOI / URL | https://doi.org/10.48550/arXiv.2406.12045 |
| Problem | Ajanların insan kullanıcıyla etkileşirken alana özgü politika kurallarına uyumunu ölçmek. |
| Yöntem | LLM ile simüle edilmiş kullanıcı + alan API'leri + politika dokümanı. Değerlendirme, konuşma sonundaki veritabanı durumunu hedef durumla karşılaştırıyor. pass^k metriği. |
| Veri kümesi | Retail ve airline alanları. |
| Karşılaştırmalar | Function-calling ajanlar (gpt-4o dahil). |
| Metrikler | Başarı oranı, pass^k. |
| Sayısal sonuçlar | Özete göre gpt-4o görevlerin <%50'sinde başarılı, retail'de pass^8 <%25. |
| Sınırlılıklar | Simüle kullanıcı gürültüsü; saldırgan senaryo yok. |
| VERIQEN ilişkisi | Retail alanındaki **iade/iptal politikaları** VERIQEN'in iade senaryosuyla birebir örtüşüyor. "Politikaya aykırı işlem yürütüldü mü" ölçümü için güçlü bir kaynak. Güvenlik (saldırı) boyutu eksik. |

#### 3. InjecAgent [Ö]
| Alan | İçerik |
|---|---|
| Başlık | InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents |
| Yazarlar | Qiusi Zhan, Zhixiang Liang, Zifan Ying, Daniel Kang |
| Yıl / Kaynak | 2024 / Findings of ACL 2024, s. 10471–10506 |
| DOI / URL | https://aclanthology.org/2024.findings-acl.624 |
| Problem | Araç kullanan ajanların dolaylı prompt injection'a açıklığını ölçmek. |
| Yöntem | Tek adımlı enjeksiyon test vakaları; doğrudan zarar ve veri sızdırma niyetleri. |
| Veri kümesi | 1.054 vaka, 17 kullanıcı aracı, 62 saldırgan aracı. |
| Karşılaştırmalar | 30 LLM ajanı. |
| Metrikler | ASR. |
| Sayısal sonuçlar | ReAct-prompted GPT-4 %24 ASR. "Hacking prompt" ile güçlendirilmiş ayarda ASR neredeyse iki katına çıkıyor. |
| Sınırlılıklar | Tek adımlı ve statik vakalar; çok adımlı durum değişimi yok. |
| VERIQEN ilişkisi | Ek, ucuz bir saldırı test seti. |

#### 4. Agent Security Bench (ASB) [Ö]
| Alan | İçerik |
|---|---|
| Başlık | Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents |
| Yazarlar | Hanrong Zhang, Jingyuan Huang, Kai Mei, Yifei Yao, Zhenting Wang, Chenlu Zhan, Hongwei Wang, Yongfeng Zhang |
| Yıl / Kaynak | 2025 / ICLR 2025 |
| DOI / URL | https://doi.org/10.48550/arXiv.2410.02644 |
| Problem | Ajan saldırı ve savunmalarını kapsamlı ve biçimsel olarak karşılaştırmak. |
| Yöntem | 10 senaryo, 10 ajan, 400+ araç, 27 saldırı/savunma yöntemi, 7 metrik, 13 LLM omurgası. |
| Veri kümesi | ASB (DPI, OPI, bellek zehirleme, Plan-of-Thought arka kapı). |
| Karşılaştırmalar | 11 savunma. |
| Metrikler | ASR, refuse rate, utility vb. |
| Sayısal sonuçlar | Özet düzeyinde sayısal değer alınmadı; tablolar doğrulanmadı. |
| Sınırlılıklar | Savunmaların çoğu prompt düzeyinde; yetkilendirme katmanı yok. |
| VERIQEN ilişkisi | Progent bu benchmark'ı kullanıyor. VERIQEN için ikincil test seti olabilir. |

#### 5. Adaptive Attacks Break Defenses Against IPI Attacks on LLM Agents [Ö]
| Alan | İçerik |
|---|---|
| Yazarlar | Qiusi Zhan, Richard Fang, Henil Shalin Panchal, Daniel Kang |
| Yıl / Kaynak | 2025 / Findings of NAACL 2025, s. 7101–7117 |
| DOI / URL | https://doi.org/10.18653/v1/2025.findings-naacl.395 |
| Problem | IPI savunmalarının uyarlamalı (savunmayı bilen) saldırılara karşı dayanıklılığı. |
| Yöntem | 8 savunmaya karşı GCG/AutoDAN tabanlı uyarlamalı saldırılar. |
| Sayısal sonuçlar | 8 savunmanın tamamı aşılıyor; ASR sürekli olarak %50'nin üzerinde. |
| VERIQEN ilişkisi | **Zorunlu değerlendirme ilkesi:** VERIQEN'in LLM'e dayanan her bileşeni (B2 hakemi, risk sınıflandırıcı) uyarlamalı saldırıyla test edilmeli. |

#### 6. The Attacker Moves Second [Ö]
| Alan | İçerik |
|---|---|
| Başlık | The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections |
| Yazarlar | Milad Nasr, Nicholas Carlini, Chawin Sitawarin, Sander V. Schulhoff, Jamie Hayes, Michael Ilie, Juliette Pluto, Shuang Song, Harsh Chaudhari, Ilia Shumailov, Abhradeep Thakurta, Kai Yuanqing Xiao, Andreas Terzis, Florian Tramèr |
| Yıl / Kaynak | 2025 (arXiv) / USENIX Security 2026 |
| DOI / URL | https://doi.org/10.48550/arXiv.2510.09023 |
| Problem | Savunmaların statik saldırılarla değerlendirilmesinin yanıltıcılığı. |
| Yöntem | Gradyan, RL, rastgele arama ve insan red-teaming ile uyarlamalı saldırılar. |
| Sayısal sonuçlar | 12 savunma aşılıyor; çoğunda ASR >%90. Savunmaların çoğu orijinal makalelerinde ~%0 ASR raporlamıştı. |
| VERIQEN ilişkisi | VERIQEN'in "algılama" bileşenleri üzerine hiçbir güvenlik iddiası tek başına kurulmamalı. Deterministik taban (yetki + zorunlu kanıt) bu nedenle kritik. |

#### 7. Prompt Infection [Ö]
| Alan | İçerik |
|---|---|
| Başlık | Prompt Infection: LLM-to-LLM Prompt Injection within Multi-Agent Systems |
| Yazarlar | Donghyun Lee, Mo Tiwari |
| Yıl / Kaynak | 2024 / arXiv preprint |
| DOI / URL | https://doi.org/10.48550/arXiv.2410.07283 |
| Problem | Çoklu ajan sistemlerinde enjeksiyonun ajandan ajana kendini kopyalayarak yayılması. |
| Yöntem | Kendini kopyalayan enjeksiyon; savunma olarak "LLM Tagging". |
| Sayısal sonuçlar | Bu taramada sayısal değer doğrulanmadı. |
| VERIQEN ilişkisi | Aday C (çoklu ajan kanıt kökeni) için tehdit motivasyonu. |

### K2 — Sistem düzeyinde savunmalar (yetki, bilgi akışı, politika)

#### 8. CaMeL [M]
| Alan | İçerik |
|---|---|
| Başlık | Defeating Prompt Injections by Design |
| Yazarlar | Edoardo Debenedetti, Ilia Shumailov, Tianqi Fan, Jamie Hayes, Nicholas Carlini, Daniel Fabian, Christoph Kern, Chongyang Shi, Andreas Terzis, Florian Tramèr |
| Yıl / Kaynak | 2025 / arXiv preprint (v2: Haziran 2025) |
| DOI / URL | https://doi.org/10.48550/arXiv.2503.18813 |
| Problem | Prompt injection'ı modelin davranışına güvenmeden, tasarım yoluyla engellemek. |
| Yöntem | Güvenilir sorgudan kontrol ve veri akışını çıkaran P-LLM + Q-LLM, özel Python yorumlayıcısı, değerlere bağlı yetenekler (capabilities) ve güvenlik politikaları. |
| Veri kümesi | AgentDojo. |
| Karşılaştırmalar | Tool filter, spotlighting, prompt sandwiching, PI detector. |
| Metrikler | Utility, saldırı sayısı, token ek yükü. |
| Sayısal sonuçlar | Görevlerin %77'si kanıtlanabilir güvenlikle çözülüyor (savunmasız sistem %84). Claude 3.5 Sonnet'te 949 saldırıdan 0'ı başarılı (tool filter 8). Medyan görevde girdi token'ı 2.82×, çıktı token'ı 2.73×. |
| Sınırlılıklar | Politikaları kullanıcı yazmalı ve sürdürmeli. Sık onay istemleri onay yorgunluğu yaratıyor. Yan kanallar (exception başına ~1 bit). Yalnızca metin üreten saldırılar kapsam dışı. |
| VERIQEN ilişkisi | Güçlü akademik rakip. VERIQEN'in "LLM çıktısı tek başına yetki veremez" ilkesi CaMeL'de yapısal olarak zaten var. **Fark:** CaMeL kanıtın dış sistemden doğrulanmasını ve riske göre doğrulama seçimini hedeflemiyor. |

#### 9. Progent [M]
| Alan | İçerik |
|---|---|
| Başlık | Progent: Programmable Privilege Control for LLM Agents |
| Yazarlar | Tianneng Shi, Jingxuan He, Zhun Wang, Hongwei Li, Linyu Wu, Wenbo Guo, Dawn Song |
| Yıl / Kaynak | 2025 / arXiv preprint (v2: Ağustos 2025) |
| DOI / URL | https://doi.org/10.48550/arXiv.2504.11703 |
| Problem | Aşırı yetkili araç erişimi. |
| Yöntem | Araç çağrısı düzeyinde ayrıntılı ayrıcalık politikaları için DSL, geri dönüş (fallback) eylemleri, dinamik politika güncelleme, LLM ile politika üretimi (Progent-LLM). |
| Veri kümesi | AgentDojo, ASB, AgentPoison (EHRAgent). |
| Karşılaştırmalar | repeat_user_prompt, spotlighting, tool_filter, transformers_pi_detector, DataSentinel, Llama Prompt Guard 2. |
| Metrikler | ASR, utility, çalışma süresi. |
| Sayısal sonuçlar | AgentDojo (gpt-4o): ASR %39.9 → %0. ASB: %70.3 → %0. Progent-LLM, AgentDojo: ASR %39.9 → %1.0, utility %76.3 (savunmasız %79.4). Politika denetimi ek süresi 0.0008 s (görev başına toplam ~6.09 s). |
| Sınırlılıklar | Görev için gereken en düşük ayrıcalığın içinde kalan saldırılar (ör. tercih manipülasyonu) engellenmiyor. Metin çıktısını hedefleyen saldırılar kapsam dışı. Doğruluk politika yazarına bağlı. |
| VERIQEN ilişkisi | **En yakın üç akademik rakipten biri.** VERIQEN'in "sabit yetki kontrolü" bileşeni Progent'in deterministik politika denetimiyle örtüşüyor. VERIQEN'in farkı ancak **kanıt** ve **risk** boyutunda kurulabilir. |

#### 10. FIDES (Securing AI Agents with Information-Flow Control) [Ö]
| Alan | İçerik |
|---|---|
| Yazarlar | Manuel Costa, Boris Köpf, Aashish Kolluri, Andrew Paverd, Mark Russinovich, Ahmed Salem, Shruti Tople, Lukas Wutschitz, Santiago Zanella-Béguelin (Microsoft) |
| Yıl / Kaynak | 2025 / arXiv preprint (v2: Eylül 2025) |
| DOI / URL | https://doi.org/10.48550/arXiv.2505.23643 |
| Problem | Ajan planlayıcılarında güvenlik garantisi sağlamak. |
| Yöntem | Gizlilik ve bütünlük etiketleri, deterministik politika uygulama, bilgiyi seçici gizleme primitifleri. |
| Veri kümesi | AgentDojo. |
| Sayısal sonuçlar | Bu taramada tablo değeri doğrulanmadı. |
| VERIQEN ilişkisi | Kanıt kökeni ve "ajanın beyanı kanıt sayılmaz" ilkesine (ilke 4) teorik temel sağlıyor. |

#### 11. RTBAS [M]
| Alan | İçerik |
|---|---|
| Başlık | RTBAS: Defending LLM Agents Against Prompt Injection and Privacy Leakage |
| Yazarlar | Peter Yong Zhong, Siyuan Chen, Ruiqi Wang, McKenna McCall, Ben L. Titzer, Heather Miller, Phillip B. Gibbons |
| Yıl / Kaynak | 2025 / arXiv preprint |
| DOI / URL | https://doi.org/10.48550/arXiv.2502.08966 |
| Problem | Her araç çağrısında kullanıcı onayı istemenin yarattığı yük. |
| Yöntem | Seçici etiket yayılımlı bilgi akışı kontrolü. LM-judge ve dikkat (attention) tabanlı iki bağımlılık tarayıcısı. Kullanıcı onayı yalnızca bütünlük ve gizlilik sağlanamadığında isteniyor. |
| Veri kümesi | AgentDojo + yazarların gizlilik sızıntısı benchmark'ı. |
| Sayısal sonuçlar | Sonuç bölümüne göre AgentDojo'da politika ihlali yaratan tüm istismarlar durduruluyor; görev başarısındaki düşüş %2'nin altında. |
| VERIQEN ilişkisi | **Aday D'nin (riske göre insan onayı) doğrudan öncülü.** "İnsan onayını yalnızca gerektiğinde iste" fikri yeni değil. |

#### 12. AgentSpec [M]
| Alan | İçerik |
|---|---|
| Başlık | AgentSpec: Customizable Runtime Enforcement for Safe and Reliable LLM Agents |
| Yazarlar | Haoyu Wang, Christopher M. Poskitt, Jun Sun |
| Yıl / Kaynak | 2026 / ICSE '26 (48th IEEE/ACM ICSE) |
| DOI / URL | https://doi.org/10.48550/arXiv.2503.18666 |
| Problem | Ajanlara özelleştirilebilir çalışma zamanı kısıtları uygulamak. |
| Yöntem | Tetikleyici + yüklem + uygulama eylemi (stop, user_inspection, invoke_action, llm_self_examine) içeren DSL. |
| Veri kümesi | RedCode-Exec (kod), SafeAgentBench (bedenlenmiş ajan), FixDrive (otonom sürüş). |
| Sayısal sonuçlar | Kodda >%90 güvensiz yürütme önleme (özet). Ancak Tablo 3 toplamlarından hesaplanan engelleme ~%65; bu fark makalede açıklanmıyor. SafeAgentBench'te güvensiz görev başarısı %0, güvenli görev başarısı %58.62 → %54.26. LLM ile üretilen kurallarda bedenlenmiş ajan için kesinlik %95.56, duyarlılık %70.96. Ek yük milisaniye düzeyinde. |
| Sınırlılıklar | Yüklemler kaynak kod düzeyinde; veri akışı analizi yok. |
| VERIQEN ilişkisi | ALLOW/REVIEW/BLOCK karar yapısının (stop / user_inspection) yakın karşılığı. |

#### 13. Conseca (Contextual Agent Security) [Ö]
| Alan | İçerik |
|---|---|
| Başlık | Contextual Agent Security: A Policy for Every Purpose (ilk sürüm: "Context is Key for Agent Security") |
| Yazarlar | Lillian Tsai, Eugene Bagdasarian |
| Yıl / Kaynak | 2025 / HotOS '25 |
| DOI / URL | https://doi.org/10.1145/3713082.3730378 |
| Problem | Statik politikaların bağlamla ölçeklenememesi. |
| Yöntem | Göreve özgü, tam zamanında (just-in-time), insan tarafından doğrulanabilir politika üretimi. |
| Sayısal sonuçlar | Pozisyon makalesi; sayısal sonuç doğrulanmadı. |
| VERIQEN ilişkisi | VERIQEN'in politikayı sabit tutup ek doğrulamayı uyarlama yaklaşımına bir alternatif. |

#### 14. PACT (Argument-Level Provenance) [İ]
| Alan | İçerik |
|---|---|
| Başlık | The Granularity Mismatch in Agent Security: Argument-Level Provenance Solves Enforcement and Isolates the LLM Reasoning Bottleneck |
| Yazarlar | Linfeng Fan, Ziwei Li, Yuan Tian, Yichen Wang, Rongsheng Li, Xiong Wang |
| Yıl / Kaynak | 2026 (11 Mayıs) / arXiv:2605.11039 |
| URL | https://arxiv.org/abs/2605.11039 |
| Problem | Güvenin araç çağrısının bütünü yerine argüman düzeyinde ele alınması gereği. |
| Yöntem | Her argümana anlamsal rol (target, command, credential, content, selector, control), TRUSTED > USER > TOOL > EXTERNAL köken sıralaması, role özgü güven sözleşmesi. |
| Veri kümesi | 17 tanısal senaryo, AgentDojo v1 (5 model), InjecAgent, Agent-SafetyBench. |
| Karşılaştırmalar | Vanilla, FIDES, CaMeL. |
| Sayısal sonuçlar | Kehanet (oracle) kökenli tanısal sette PACT %100 utility ve %100 güvenlik (CaMeL: %33.3 / %100). AgentDojo'da en güçlü modellerde %38.1–46.4 utility; aynı güvenlik düzeyinde CaMeL'den 8–16 puan yüksek. InjecAgent'te 1.598 saldırı çağrısının tamamı engelleniyor. P99 gecikme <272 µs. |
| Sınırlılıklar | Sözleşme sentezi ve köken çıkarımındaki hatalar baskın arıza kaynağı. İzinli içerik alanları üzerinden yapılan saldırılar kapsam dışı. |
| VERIQEN ilişkisi | **Aday G'nin (argüman düzeyinde kanıt bağlama) en yakın öncülü.** Sayılar ikincil kaynaktan; birincil PDF'ten doğrulanmalı. |

#### 15. Design Patterns for Securing LLM Agents against Prompt Injections [Ö]
| Alan | İçerik |
|---|---|
| Yazarlar | Luca Beurer-Kellner, Beat Buesser, Ana-Maria Creţu, Edoardo Debenedetti, Daniel Dobos, Daniel Fabian, Marc Fischer, David Froelicher, Kathrin Grosse, Daniel Naeff, Ezinwanne Ozoani, Andrew Paverd, Florian Tramèr, Václav Volhejn |
| Yıl / Kaynak | 2025 / arXiv preprint |
| DOI / URL | https://doi.org/10.48550/arXiv.2506.08837 |
| Yöntem | Ajanın yapabileceklerini kısıtlayan altı mimari tasarım deseni ve vaka çalışmaları. |
| Sayısal sonuçlar | Yok (tasarım ve vaka analizi). |
| VERIQEN ilişkisi | VERIQEN mimarisini bu desenlerden birine konumlandırmak, hakem incelemesinde beklenen bir adım. |

### K3 — Algılama ve hizalama tabanlı savunmalar

#### 16. MELON [T]
| Alan | İçerik |
|---|---|
| Başlık | MELON: Provable Defense Against Indirect Prompt Injection Attacks in AI Agents |
| Yazarlar | Kaijie Zhu, Xianjun Yang, Jindong Wang, Wenbo Guo, William Yang Wang |
| Yıl / Kaynak | 2025 / ICML 2025 |
| DOI / URL | https://doi.org/10.48550/arXiv.2502.05174 |
| Problem | Eğitim gerektirmeyen, faydayı koruyan IPI tespiti. |
| Yöntem | Kullanıcı istemi maskelenerek yeniden yürütme. İki yürütmedeki araç çağrıları benzerse saldırı sayılıyor (θ = 0.8). |
| Veri kümesi | AgentDojo. |
| Sayısal sonuçlar | Tablo 1, GPT-4o (BU / UA / ASR): No Defense 80.41 / 69.08 / 16.06; Tool Filter 65.98 / 65.54 / 2.34; MELON 68.04 / 58.78 / 0.24; MELON-Aug 76.29 / 68.72 / 0.32. GPT-4o'da yanlış pozitif oranı: MELON %9.28, DeBERTa dedektörü %61.86. API maliyeti ≈2×. |
| Sınırlılıklar | Yalnızca araç çağrılarını izliyor; metin yanıtı üzerinden gelen saldırılar kaçıyor (kaçan vakaların %72.73'ü). Beyaz kutu saldırı değerlendirilmedi. |
| VERIQEN ilişkisi | B2 (LLM-as-a-judge) ve "her zaman açık pahalı kontrol" karşılaştırmaları için referans maliyet ve doğruluk noktası. |

#### 17. IPIGuard [T]
| Alan | İçerik |
|---|---|
| Başlık | IPIGuard: A Novel Tool Dependency Graph-Based Defense Against Indirect Prompt Injection in LLM Agents |
| Yazarlar | Hengyu An, Jinghuai Zhang, Tianyu Du, Chunyi Zhou, Qingming Li, Tao Lin, Shouling Ji |
| Yıl / Kaynak | 2025 / EMNLP 2025 (Main) |
| URL | https://aclanthology.org/2025.emnlp-main.53 |
| Problem | Dış verinin yeni araç çağrısı tetiklemesi. |
| Yöntem | Planlama aşamasında Araç Bağımlılık Grafiği (TDG); planda olmayan araç çağrılarını kısıtlama. |
| Sayısal sonuçlar | Tablo 1 (GPT-4o-mini, ortalama), ASR / UA: No Defense 13.16 / 54.30; Tool Filter 2.06 / 53.36; IPIGuard 0.69 / 58.77. Tablo 2 ek yük: girdi token'ı 14.605 (savunmasız 6.165), süre 13.88 s (7.13 s). |
| Sınırlılıklar | Güçlü planlama yeteneği gerektiriyor. Yalnızca araç kullanımına karışan saldırıları hedefliyor. |
| Not | Benign utility metinde %67.01, Tablo 3'te %69.07; makalede tutarsız. |

#### 18. Task Shield [Ö]
| Alan | İçerik |
|---|---|
| Başlık | The Task Shield: Enforcing Task Alignment to Defend Against Indirect Prompt Injection in LLM Agents |
| Yazarlar | Feiran Jia, Tong Wu, Xin Qin, Anna Squicciarini |
| Yıl / Kaynak | 2025 / ACL 2025 (Long), s. 29680–29697 |
| DOI / URL | https://doi.org/10.18653/v1/2025.acl-long.1435 |
| Yöntem | Her talimatın kullanıcı hedefine katkı sağlayıp sağlamadığını LLM ile denetleme. |
| Sayısal sonuçlar | AgentDojo, GPT-4o: ASR %2.07, utility %69.79 (özet). |
| Sınırlılıklar | Yazarlara göre LLM'e bağımlı olduğu için uyarlamalı saldırılara açık; tek benchmark ve tek model. |
| VERIQEN ilişkisi | "İşlem kullanıcı talimatıyla tutarlı mı" (VERIQEN sorusu 3) için doğrudan rakip yöntem. |

#### 19. LlamaFirewall [M]
| Alan | İçerik |
|---|---|
| Başlık | LlamaFirewall: An open source guardrail system for building secure AI agents |
| Yazarlar | Sahana Chennabasappa, Cyrus Nikolaidis, Daniel Song, David Molnar, Stephanie Ding, Shengye Wan, Spencer Whitman vd. (Meta) |
| Yıl / Kaynak | 2025 / arXiv preprint |
| DOI / URL | https://doi.org/10.48550/arXiv.2505.03574 |
| Yöntem | PromptGuard 2 (DeBERTa sınıflandırıcı), AlignmentCheck (LLM ile düşünce zinciri denetimi), CodeShield (statik analiz). |
| Sayısal sonuçlar | AgentDojo: ASR %17.63 / utility %47.73 (temel); yalnız PromptGuard 2 86M: 7.53 / 47.01; yalnız AlignmentCheck: 2.89 / 43.09; birlikte: 1.75 / 42.68. PromptGuard 2 86M: %1 FPR'de %97.5 recall, A100'de 92.4 ms. |
| Sınırlılıklar | AlignmentCheck büyük model gerektiriyor ve kendisi de enjeksiyona açık. Yüksek gecikme. Güvensiz araç kullanımı henüz kapsamda değil. |
| VERIQEN ilişkisi | Hem akademik hem ticari (açık kaynak) rakip; rakip analizine de alındı. |

#### 20. GuardAgent [Ö]
| Alan | İçerik |
|---|---|
| Başlık | GuardAgent: Safeguard LLM Agents via Knowledge-Enabled Reasoning |
| Yazarlar | Zhen Xiang, Linzhi Zheng, Yanjie Li, Junyuan Hong, Qinbin Li, Han Xie, Jiawei Zhang, Zidi Xiong, Chulin Xie, Carl Yang, Dawn Song, Bo Li |
| Yıl / Kaynak | 2025 / ICML 2025 (PMLR 267) |
| URL | https://proceedings.mlr.press/v267/xiang25a.html |
| Yöntem | Koruma isteklerini görev planına, planı yürütülebilir koruma koduna çeviren LLM ajanı. |
| Veri kümesi | EICU-AC (sağlık erişim kontrolü), Mind2Web-SC. |
| Sayısal sonuçlar | v1 özetinde iki benchmark için %98.7 ve %90.0 raporlanmış (tablo doğrulanmadı). |
| VERIQEN ilişkisi | **EICU-AC rol tabanlı erişim kontrolü** VERIQEN'in yetki boyutu için hazır bir test kümesi. |

#### 21. ShieldAgent [M]
| Alan | İçerik |
|---|---|
| Başlık | ShieldAgent: Shielding Agents via Verifiable Safety Policy Reasoning |
| Yazarlar | Zhaorun Chen, Mintong Kang, Bo Li |
| Yıl / Kaynak | 2025 / ICML 2025 (PMLR 267, s. 8313–8344) |
| DOI / URL | https://doi.org/10.48550/arXiv.2503.22738 |
| Yöntem | Politika dokümanlarından doğrulanabilir kurallar çıkarıp olasılıksal kural devreleri kuruyor; model denetimi ile birleştiriyor. |
| Veri kümesi | ShieldAgent-Bench (6 web ortamı, 7 risk kategorisinde ~3K örnek). |
| Sayısal sonuçlar | Yanlış pozitif oranı %4.8, ihlal edilen kuralları yakalama oranı %90.1. Kapalı API sorguları %64.7, çıkarım süresi %58.2 azalıyor. |
| VERIQEN ilişkisi | "Doğrulama maliyetini azaltma" iddiasında güçlü bir önceki çalışma. **Fark:** ShieldAgent dış kanıt kaynağı doğrulamıyor ve riske göre strateji seçmiyor. |

### K4 — Seçici/uyarlamalı doğrulama, belirsizlik ve insan onayı (en kritik küme)

#### 22. VP-Control — Cost-Aware Verification Portfolios [T] ⚠️ EN YAKIN RAKİP
| Alan | İçerik |
|---|---|
| Başlık | Engineering Reliable Commit Gates for Agentic AI: Cost-Aware Verification Portfolios under Common-Mode Data Failures |
| Yazarlar | Zihao Zheng, Baichuan Li, Junyi Yao, Jiayu Long |
| Yıl / Kaynak | 2026 (Eylül) / arXiv:2609.10969 [cs.SE], hakemli yayın yeri belirtilmemiş |
| URL | https://arxiv.org/abs/2609.10969 |
| Problem | Durum değiştiren işlemlerden önce çalışan "commit gate" tasarımı. Doğrulayıcılar aynı veri kaynağını paylaştığında birlikte yanılıyor; kanıt, kontrol ile yazma arasında eskiyebiliyor. |
| Yöntem | Kanıt soyu (evidence lineage), 37 doğrulama planı, gözlemlenebilir üst veriye (kanıt yaşı, kaynak sağlığı, guard varlığı, etki alanı, geri alınabilirlik) bakarak plan seçen portföy denetleyicisi. Amaç: maliyet − ağırlıklı güvenli kapsama + risk fiyatı × güvensiz oran. Wilson sınırı ile yaklaşık kalibrasyon, transactional guard, insana erteleme, idempotency. |
| Veri kümesi | 48 şablon, 2.880 senaryo; 5.760 dondurulmuş öneri (yerel Qwen3.5-9B ve Gemma4-8B aktörler; Qwen3-4B ve Phi-4-mini doğrulayıcılar). Ayrıca FinQA alt kümesi ve canlı SQLite servisi (216 bölüm). |
| Karşılaştırmalar | Her zaman yürüt, aynı kaynakla kontrol, çoğunluk oyu, modeller arası oy, bağımsız kaynak, exact guard, guard + kaynak, TTL ve güven eşikleri, eşit maliyette rastgele mekanizma, LTT. |
| Metrikler | Güvensiz yürütme oranı, güvenli otomatik kapsama, erteleme oranı, birim maliyet, yanlış onay. |
| Sayısal sonuçlar | Test seti (güvensiz % / kapsama % / erteleme %): her zaman yürüt 44.2 / 55.7 / 0; modeller arası oy (aynı kaynak) 27.8 / 40.6 / 0; bağımsız kaynak 16.5 / 45.6 / 0; %5 hedefli portföy 1.9 [1.0, 2.8] / 38.2 / 31.4 (maliyet 4.96; guard + bağımsız kaynak 0.8 / 31.4 / 56.2, maliyet 8.82). Bağımsız kaynakla aynı bütçede güvensiz yürütme %16.5 → %5.7. Ön kayıtlı üç karşılaştırma Holm düzeltmesi sonrası anlamlı (p = 0.0006). |
| Sınırlılıklar | Maliyetler modellenmiş birimler. Kalibrasyon yaklaşık. Görülmemiş arıza ailelerinde %5 hedefi aşılıyor (%26'ya kadar). **Saldırgan yazarlar, sahte köken (forged provenance) ve uzun ufuklu ajanlar değerlendirilmemiş.** Tek bir loopback servisi; FinQA'da ana etki tekrarlanmadı. |
| VERIQEN ilişkisi | VERIQEN'in mevcut çekirdek hipotezi ("yetki ve zorunlu kanıt sabitken ek doğrulamayı riske göre seçmek, güvenliği düşürmeden maliyeti azaltır") büyük ölçüde **bu çalışmada zaten test edilmiş**. Kanıt yaşı, kaynak bağımsızlığı, geri alınabilirlik, idempotency ve kontrol sonrası yarış durumu (race) dahil. VERIQEN'in açık kalan alanı bu çalışmanın açıkça dışarıda bıraktığı **saldırgan (adversarial) ortam**. |

#### 23. CausalArmor [M]
| Alan | İçerik |
|---|---|
| Başlık | CausalArmor: Efficient Indirect Prompt Injection Guardrails via Causal Attribution |
| Yazarlar | Minbeom Kim, Mihir Parmar, Phillip Wallis, Lesly Miculicich, Kyomin Jung, Krishnamurthy Dj Dvijotham, Long T. Le, Tomas Pfister |
| Yıl / Kaynak | 2026 / ICML 2026 (arXiv:2602.07918) |
| DOI / URL | https://doi.org/10.48550/arXiv.2602.07918 |
| Problem | "Aşırı savunma ikilemi": her zaman açık pahalı temizleme, zararsız durumlarda faydayı ve gecikmeyi bozuyor. |
| Yöntem | Ayrıcalıklı karar noktalarında leave-one-out atıf; güvenilmeyen bir parça kullanıcı isteğine baskın geldiğinde **yalnızca o zaman** hedefli temizleme. |
| Veri kümesi | AgentDojo, DoomArena. |
| Sayısal sonuçlar | Tablo 1 (DoomArena, Gemini-3-Pro), BU / BL / ASR: No Defense 73.57 / 1.00 / 88.87; PiGuard 55.13 / 1.16 / 5.57; CausalArmor 70.96 / 1.38 / 3.65. AgentDojo tablosu (Tablo 3) bu taramada açılamadı. |
| Sınırlılıklar | Etkinlik temizleyiciye bağlı. Yoğun saldırı altında ek yük her zaman açık savunmaya yaklaşıyor. Uyarlamalı saldırganlara karşı tek başına çözüm olarak önerilmiyor. |
| VERIQEN ilişkisi | "Seçici doğrulama" fikrinin IPI alanındaki güncel ve güçlü örneği. Aday A ve E'nin farklılaşma alanını daraltıyor. |

#### 24. Agent-Sentry [İ]
| Alan | İçerik |
|---|---|
| Başlık | Agent-Sentry: Bounding LLM Agents via Execution Provenance |
| Yazarlar | Rohan Sequeira, Stavros Damianakis, Umar Iqbal, Konstantinos Psounis |
| Yıl / Kaynak | 2026 / arXiv:2603.22868 (v2: Mayıs 2026) |
| URL | https://arxiv.org/abs/2603.22868 |
| Yöntem | Her yürütme için köken grafiği. Üç katman: yapısal sınıflandırıcı (XGBoost), köken bilgili izin listesi, LLM hakemi. LLM hakemi yalnızca önceki katmanlar karar veremediğinde çağrılıyor. |
| Veri kümesi | AgentDojo, AgentDyn, Agent-Sentry Bench. |
| Sayısal sonuçlar | Özete göre başarılı enjeksiyonların %94.3'ü engelleniyor, zararsız yürütmelerin %95.1'ine izin veriliyor. LLM hakemi kararların ~%3'ünde devreye giriyor. Ortalama 0.073 s. |
| VERIQEN ilişkisi | "Ucuzdan pahalıya kademeli doğrulama + köken" mimarisinin uygulanmış hâli. **En yakın üç akademik rakipten biri.** Sayılar ikincil kaynaktan. |

#### 25. Uncertainty-Aware, Risk-Adaptive Access Control (LLM-Judged TBAC) [M]
| Alan | İçerik |
|---|---|
| Yazarlar | Charles Fleming, Ashish Kundu, Ramana Kompella (Cisco) |
| Yıl / Kaynak | 2025 / arXiv:2510.11414 |
| Yöntem | LLM hakemi göreve özel politika sentezliyor; araç risk puanlarından bileşik risk (R_comp) ve öz-belirsizlik (v) hesaplıyor; eşik aşılırsa insana yükseltiyor. |
| Sayısal sonuçlar | **Deneysel değerlendirme yok**; yalnızca varsayımsal örnek değerler. |
| VERIQEN ilişkisi | "Risk + belirsizlik → insan onayı" fikri (Aday D/E) **2025'te önerilmiş**, ancak deneysel olarak sınanmamış. Kendi sınırlılıklarında, riski LLM'in hesaplamasının manipülasyona açık olduğunu kabul ediyor. Bu durum Aday F'yi destekliyor. |

#### 26. Calibrate-Then-Delegate (CTD) [M]
| Alan | İçerik |
|---|---|
| Yazarlar | Edoardo Pona, Milad Kazemi, Mehran Hosseini, Yali Du, David Watson, Osvaldo Simeone, Nicola Paoletti |
| Yıl / Kaynak | 2026 / arXiv:2604.14251 (yayın yeri metinde belirtilmemiş) |
| Yöntem | Ucuz gizil prob ile pahalı uzman LLM arasında, "devretme değeri" tahmini ve Learn-then-Test kalibrasyonuyla, risk ve bütçe garantili kademeli yapı. |
| Veri kümesi | Anthropic HH, MTSamples, MTS-Dialog, ToolACE. |
| Sayısal sonuçlar | Bütçe kontrolünde (α_B = 0.35, güçlü uzman) belirsizlik top-k'ya göre +4.0 AUROC, +2.8 doğruluk. Performans kontrolünde ihlal oranı %5.6 (ampirik seçicide %43.6). |
| VERIQEN ilişkisi | Bütçe kısıtlı doğrulama seçiminin istatistiksel çerçevesi (Aday E). Ancak araç çağrısı yetkilendirmesini **ele almıyor**; yalnızca içerik izleme yapıyor. |

#### 27. KnowNo — Robots That Ask For Help [Ö]
| Alan | İçerik |
|---|---|
| Yazarlar | Allen Z. Ren, Anushri Dixit, Alexandra Bodrova, Sumeet Singh, Stephen Tu, Noah Brown, Peng Xu, Leila Takayama, Fei Xia, Jake Varley, Zhenjia Xu, Dorsa Sadigh, Andy Zeng, Anirudha Majumdar |
| Yıl / Kaynak | 2023 / CoRL 2023, PMLR 229:661–682 |
| URL | https://proceedings.mlr.press/v229/ren23a.html |
| Yöntem | Konformal tahmin ile LLM planlayıcının belirsizliğini hizalama; tahmin kümesi tek elemanlı değilse insandan yardım isteme. Görev başarısı için istatistiksel garanti. |
| VERIQEN ilişkisi | "Belirsizse insana sor" kararının garantili biçimi. REVIEW eşiğinin kalibrasyonu için yöntemsel temel. |

#### 28. Conformal Risk Control [Ö]
| Alan | İçerik |
|---|---|
| Yazarlar | Anastasios N. Angelopoulos, Stephen Bates, Adam Fisch, Lihua Lei, Tal Schuster |
| Yıl / Kaynak | 2024 / ICLR 2024 (Spotlight) |
| URL | https://proceedings.iclr.cc/paper_files/paper/2024/hash/f3549ef9b5ff520a7e41ff3cc306ab2b-Abstract-Conference.html |
| Yöntem | Konformal tahmini, herhangi bir monoton kaybın beklenen değerini kontrol edecek şekilde genelleştiriyor; O(1/n) sıkılık. |
| VERIQEN ilişkisi | "Yanlış ALLOW oranı ≤ α" türünden eşik kalibrasyonu için doğrudan kullanılabilir araç. Değiş tokuş edilebilirlik (exchangeability) varsayımı saldırgan ortamda bozulur; bu da Aday F'nin konusu. |

#### 29. ToolEmu [Ö/İ]
| Alan | İçerik |
|---|---|
| Başlık | Identifying the Risks of LM Agents with an LM-Emulated Sandbox |
| Yazarlar | Yangjun Ruan, Honghua Dong, Andrew Wang, Silviu Pitis, Yongchao Zhou, Jimmy Ba, Yann Dubois, Chris J. Maddison, Tatsunori Hashimoto |
| Yıl / Kaynak | 2024 / ICLR 2024 (Spotlight) |
| DOI / URL | https://doi.org/10.48550/arXiv.2309.15817 |
| Yöntem | Araç yürütmesini LLM ile taklit eden sanal ortam + LLM tabanlı güvenlik değerlendiricisi. |
| Sayısal sonuçlar | İnsan değerlendirmesinde ToolEmu'nun tespit ettiği hataların %68.8'i geçerli bulunmuş (özet). İkincil kaynağa göre 36 yüksek riskli araç, 144 test vakası; en güvenli ajan bile ~%24 oranında riskli eylem yapıyor. |
| VERIQEN ilişkisi | Pahalı ama GPU gerektirmeyen bir "yürütme öncesi sonuç simülasyonu" doğrulayıcısı olarak VERIQEN portföyüne aday bileşen. |

#### 30. FAVA [Ö] — yönergede adı geçtiği için eklendi
| Alan | İçerik |
|---|---|
| Başlık | Fine-grained Hallucination Detection and Editing for Language Models |
| Yazarlar | Abhika Mishra, Akari Asai, Vidhisha Balachandran, Yizhong Wang, Graham Neubig, Yulia Tsvetkov, Hannaneh Hajishirzi |
| Yıl / Kaynak | 2024 / arXiv:2401.06855 (v4: Ağustos 2024) |
| Yöntem | Geri getirme destekli LM ile ince taneli halüsinasyon tespiti ve düzeltme; FAVABENCH (~1.000 insan yargısı). |
| Sayısal sonuçlar | Özete göre önerilen düzeltmeler FActScore'u %5–10 iyileştiriyor. |
| VERIQEN ilişkisi | Doğrudan ilgili değil. Ajanın ürettiği metinsel gerekçe ile kaynak kanıt arasındaki tutarlılığı ölçen opsiyonel bir doğrulayıcı olarak kullanılabilir. **Ajan güvenliği literatürü olarak sunulmamalı.** |

---

## 3. Ek tarama listesi (ayrıntılı doğrulanmadı)

Aşağıdaki 2026 çalışmaları VERIQEN'in alanına çok yakın görünüyor. Başvurudan önce en azından özet ve deney bölümleri okunmalı.

| Çalışma | arXiv | Neden önemli |
|---|---|---|
| FinHarness: An Inline Lifecycle Safety Harness for Finance LLM Agents | 2605.27333 | Her araç adımı için riske göre doğrulama derinliği belirleyen "risk window", adım başına en fazla bir LLM çağrısı. Aday A'ya doğrudan rakip. |
| Aligning Provenance with Authorization: A Dual-Graph Defense (AuthGraph) | 2605.26497 | Köken grafiği ile kullanıcı niyetinden türetilen yetki grafiğini karşılaştırıyor. |
| Causality Laundering: Denial-Feedback Leakage (ARM) | 2604.04035 | **Reddedilen işlemlerin kendisinin bilgi sızdırabileceğini** gösteriyor. VERIQEN'in BLOCK gerekçesi mesajları için önemli bir tehdit. |
| The Claws in Plain Sight: Unauthorized Context Disclosure through Tool Calls | 2608.20658 | Yürütme öncesi köken bilgili izleme; onay çağrının SHA-256 özetine bağlanıyor. VERIQEN'in onay bütünlüğü ilkesine (ilke 7) çok yakın. |
| When Efficiency Backfires: Cascading LLMs Trigger Cascade Failure under Adversarial Attack | 2605.17288 | Kademeli (cascade) sistemlerin saldırı altında en güçlü bileşenlerinden daha kırılgan olabileceğini gösteriyor. Aday F'nin motivasyonu. |
| From Shield to Target: Denial-of-Service Attacks on LLM-Based Agent Guardrails | 2606.14517 | Zaman aşımında "geçir" varsayılanının finansal işlemi incelemesiz geçirdiğini gösteriyor. VERIQEN ilke 6 (güvenli varsayılan) için kanıt. |

---

## 4. Literatürden çıkan sentez

1. **Deterministik yetki denetimi çözülmüş bir alt problem.** Progent, CaMeL, FIDES, AgentSpec ve PACT, araç çağrısı düzeyinde politika uygulamayı ve %0'a yakın ASR'yi gösterdi. VERIQEN'in yetki katmanı bilimsel katkı olarak sunulamaz; mühendislik bileşenidir.
2. **"Seçici/uyarlamalı doğrulama" artık kalabalık bir alan.** VP-Control (Eylül 2026), CausalArmor (ICML 2026), Agent-Sentry, FinHarness ve RTBAS, "her zaman pahalı kontrol yerine gerektiğinde kontrol" fikrini farklı biçimlerde uyguluyor. VP-Control, VERIQEN'in mevcut hipotezini neredeyse birebir test ediyor.
3. **Algılama tabanlı savunmalar uyarlamalı saldırıya dayanmıyor** (Zhan vd. 2025; Nasr vd. 2025). Bu bulgu VERIQEN'in tasarımında LLM'i yalnızca **öneri** katmanında tutma kararını güçlendiriyor.
4. **Açık boşluk:** Uyarlamalı doğrulama sistemleri, **yönlendirme kararının kendisi bir saldırı yüzeyidir** varsayımıyla değerlendirilmemiş. VP-Control saldırgan yazarları ve sahte kökeni açıkça kapsam dışı bırakıyor; TBAC çalışması LLM'in risk puanını manipüle edilebilir sayıyor ama çözmüyor. Kademeli LLM sistemlerinde (2605.17288) ve LLM yönlendiricilerinde (RerouteGuard, 2601.21380) yönlendirme saldırıları gösterilmiş, ancak **araç çağrısı yetkilendirmesindeki risk-uyarlamalı doğrulama** için bu analiz bulunamadı. *(Bu bir ön tarama bulgusudur; "literatürde yok" kesinliğinde değildir.)*

---

## 5. Kalite kontrol (bu aşama)

| Kontrol | Sonuç |
|---|---|
| Kaynaklar gerçekten mevcut mu? | 30/30 çalışmanın varlığı doğrulandı. IPIGuard++ bulunamadı; FAVA farklı konuda. |
| Başlık/yazar/yıl/DOI | arXiv ve ACL Anthology kayıtlarından alındı. Yayın yeri belirsiz olanlar "preprint" olarak işaretlendi. |
| Başarı oranları doğru veri kümesine mi ait? | Her sayı veri kümesi ve modeliyle birlikte verildi. Tutarsızlıklar (AgentDojo Tablo 1, IPIGuard BU, AgentSpec %90) not edildi. |
| İkincil kaynaklı sayılar | PACT, Agent-Sentry, ToolEmu (kısmen) **[İ]** olarak işaretlendi; birincil PDF ile tekrar kontrol edilmeli. |
| Eksik kalanlar | ASB, FIDES, KnowNo, Prompt Infection ve CausalArmor'ın AgentDojo tablosu için sayısal sonuçlar çıkarılamadı. |
