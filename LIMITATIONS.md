# LIMITATIONS.md — intelgraph bilinen sınırları (Faz 14 doğrulanmış)

## NER (extractor.py)
- **Bağlamsal anlam çıkaramaz**: NER sadece regex-based'dir, dilbilimsel/anlamsal analiz yoktur. Örnek: "Sunucu 10.0.0.1" ile "Struts 10.0.4.2" arasındaki fark sadece context keyword'lere dayanır.
- **IPv6 desteği yok**: `IP_RE` sadece IPv4 eşleştirir (`\b(?:\d{1,3}\.){3}\d{1,3}\b`). Gerçek dünyada URLhaus'ta 0 IPv6 örneği bulduk, bu yüzden acil değil.
- **NER DOMAIN FP oranı %53.1**: Faz 9 ölçeğinde 19,794 raw DOMAIN match → 10,144 FILENAME (51%), 8,946 DOMAIN (45%), 704 UNKNOWN (4%). `_classify_domain_match()` bunu TLD + filename ext + URL context ile azaltır ama tamamen sıfırlayamaz.
- **PERSON/ORGANIZATION düşük doğruluk**: Regex pattern başlıklar ("Mr.", "Dr.") ve şirket ekleri ("Inc.", "Corp.") arar — çoğu threat intel metninde bulunmaz.

## EvidenceChain (evidence_chain/confidence.py)
- **Keyword-based çelişki tespiti**: `ContradictionDetector` çelişkiyi proof content'teki "contradicts"/"refutes"/"debunks" kelimelerine bakarak anlar. Doğal dilde "aslında yanlış" gibi ifadeler yakalanmaz.
- **Source trust varsayılanı 50**: `source_trust_map` verilmediğinde her source için 50 kullanır — oysa farklı kaynakların güvenilirliği farklı olmalı.

## EntityMatcher (graph.py)
- **O(n²) ölçek eşiği**: ~100K node eşiğinde O(n²) karşılaştırma takılabilir. Faz 9 ölçeğinde (10K) kabul edilebilir; daha fazlası için hash-based ön filtre gerekir.
- **Eşleştirme sınırları**: Sadece aynı tip (IPAddress↔IPAddress, Domain↔Domain, CveEntity↔CveEntity) eşleştirir; cross-tip eşleştirme yoktur.

## RelationshipExtractor (extractor.py)
- **`min_confidence=0.0` varsayılan (filtre yok)**: Faz 10.3 ölçeğinde 0% FP gözlendi, bu yüzden acil değil; ancak farklı veri setlerinde filtreye ihtiyaç olabilir.
- **Co-occurrence yaklaşımı**: Aynı cümlede veya dokümanda geçen entity'ler için ilişki kurar, gerçek语文 anlamsal ilişkileri anlamaz.
- **Verbs hardcoded**: 28 threat intel fiili hardcoded ("exploits", "uses", "targets", vb.). Yeni fiiller eklemek için kod değişikliği gerekir.

## Graph veritabanı (graph.py)
- **In-memory**: IntelligenceGraph RAM'de tutulur, kalıcı depolama yoktur. Pipeline her çalıştırmada sıfırdan inşa eder.

## Görselleştirme (web/dashboard.html)
- **Chart.js CDN bağımlı**: Dashboard tek HTML dosyası, Chart.js'u CDN'den yükler. Ofline/airgap ortamda çalışmaz.
- **statik**: Dashboard gerçek-zamanlı değil — /dashboard/summary her çağrıldığında yeniden hesaplar, WebSocket/SSE yoktur.

## Pipeline (chain.py)
- **UTE.write() confidence dönmüyor**: `UnifiedTruthEngine.write()` `{"key", "action", "source"}` döner — confidence dahil değildir. `result.truth_entries` üzerinden confidence okumak için `ute.read()` gerekir.
- **VERSION etiketi pipeline'da filtrelenir**: Faz 13 ile _classify_ip_match VERSION'u ayırır, pipeline bu etiketli entity'leri fact'lara eklemez — versiyon numaraları graph'a girmez.
- **chain_manager SQLite**: `resolve_evidence_contradictions` chain_manager path'i her `add_entity` çağrısında SQLite'a yazar — 200+ varlıkta belirgin yavaşlama. In-memory path (`chain_manager=None`) çok daha hızlı.

## Kaynak (Sources)
- **URLhaus JSON API 401**: Sadece CSV'den veri alınabilir.
- **OTX API key gerekli**: Faz 6'da sentetik OTX verisi kullanıldı, gerçek OTX pulse'ları API key olmadan alınamaz.
- **OTX × URLhaus 0 ortak IOC**: Çapraz kaynak eşleşmesi için daha fazla kaynak veya aynı vakaya farklı açılardan bakan kaynaklar gerekir.