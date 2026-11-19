# Veri bölme ve kilitli test protokolü (jüri eleştirisi 3.4)

**Dosya:** `split_v1.json` · **Tohum:** 20261119 · **Oluşturma:** 19 Kasım 2026
**sha256:** `d6b0a1631610ad6a178d77e4b0b7c73e7fbe475970d8e4ecd4392c412c1e5260`

## Bölmeler

| Küme | İçerik | Kullanım |
|---|---|---|
| **Banking dev** | 10 kullanıcı görevi | Yeni kurallar ve mekanizmalar yalnız burada geliştirilir |
| **Banking val** | 6 kullanıcı görevi | Sürüm ve eşik seçimi |
| **Slack, Travel (kilitli test)** | 21 + 20 kullanıcı görevi | Yalnız nihai değerlendirmede, bir kez açılır |
| **Kilitli saldırı seti** | Henüz yazılmadı (bkz. aşağı) | VERIQEN dondurulduktan sonra bir kez açılır |

## Dürüst not: Banking'in tamamı daha önce görüldü

VERIQEN v1, A, S ve SI sürümleri ile kelime tabanlı niyet kuralları 16 Banking görevinin **hepsi** görülerek geliştirildi (12 §3d). Bu yüzden:
- Banking **val** kümesi, eski mekanizmalar (yazar kökeni, sıkı mod, kelime niyeti) için temiz değil. Yalnız bu tarihten sonra geliştirilen **yeni** mekanizmalar için kısmi bir ayrım sağlıyor.
- Temiz bir değerlendirme yalnız iki yoldan mümkün: (a) **Slack/Travel**, ama bu, köken takibinin IBAN dışındaki değerlere genelleştirilmesini gerektiriyor (Aşama 2); (b) **kilitli saldırı seti**.

## Kurallar

1. Yeni bir mekanizmanın kuralları, eşikleri ve istemleri yalnız **dev** görevlerine bakılarak yazılır.
2. **val** görevleri yalnız sürüm karşılaştırması için çalıştırılır; val sonucuna bakılarak kural değiştirilirse, değişiklik commit mesajında "val'e bakılarak" diye belirtilir.
3. Kilitli test kümesi açılmadan önce, değerlendirilecek sürümün commit'i ve yapılandırması bu dosyaya yazılır. Kilitli test **bir kez** açılır. Sonuç kötü olsa da raporlanır.
4. Bu dosya ve `split_v1.json` sonradan değiştirilmez. Yeni bir bölme gerekirse `split_v2.json` oluşturulur ve nedeni yazılır.

## Kilitli saldırı seti (planlanan)

- VERIQEN 2.0 dondurulmadan **önce** yazılacak. Dosyanın sha256'sı ayrı bir commit'le kaydedilecek, içerik ise dondurmadan sonra açılacak.
- Ekip dışından bir kişinin katkısı aranıyor. Bulunamazsa "ekip tarafından, dondurmadan önce yazılmış" diye raporlanacak; bu tam bağımsızlık değildir.

## Açılış kaydı

| Tarih | Küme | Sürüm (commit) | Sonuç belgesi |
|---|---|---|---|
| — | — | — | — |
