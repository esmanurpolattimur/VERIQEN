# VERIQEN pilot deneyi (sentetik)

Risk-uyarlamalı doğrulamanın "doğrulama düşürme" saldırısına karşı davranışını ölçen küçük, GPU ve LLM gerektirmeyen bir simülasyon.

## Çalıştırma

```bash
pip install numpy matplotlib
python pilot.py     # ana tablo  -> results/summary.json   (~20 sn)
python sweep.py     # maliyet–güvenlik eğrisi -> results/sweep_table.json, results/pilot_tradeoff.png (~75 sn)
```

`sweep.py`, `pilot.py`'nin ürettiği `results/summary.json` dosyasını okur; önce `pilot.py` çalıştırılmalıdır.

## Ne ölçülüyor

- **B0/B1/B3:** korumasız / yalnız kurallar / sabit tam doğrulama
- **B4-naif:** ajan beyanı + dedektör skoru + ajan anahtarıyla okunan kayıt
- **B4-T:** yalnız güvenilir kaynak, ama anahtarı ajan belirliyor
- **B4-TK / VERIQEN:** güvenilir kaynak + oturuma bağlı anahtar (+ monoton taban)
- **VERIQEN-K:** ayrıca kötü durum kalibrasyonu (saldırı altı fazla risk ≤ δ)

Saldırgan beyaz kutudur. D1 (beyan), D2 (dedektör atlatma) ve D5 (anahtar kaydırma) kombinasyonları ile 30 kurban kimliği arasından en başarılı seçeneği seçer.

Tüm parametreler `pilot.py` içindeki `CFG` sözlüğündedir ve `results/summary.json` içine yazılır. Sonuçların yorumu ve sınırlılıklar için: `docs/research/11-originality-core-and-pilot.md`.

**Uyarı:** Veriler sentetiktir; mutlak sayılar genellenemez.
