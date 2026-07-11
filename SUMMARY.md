# SUMMARY.md (Historical)

> **Note:** This summary covers the earliest development phases (1–13). The project has evolved significantly since then. See [README.md](./README.md) for the current feature set.

# SUMMARY.md — intelgraph جلسه ساختاری (Faz 1–13)
Tek oturumdaki ilerlemenin kronolojik özeti. Ayrıntılı sağlık kontrolü için `FINAL_STATUS.md`, bilinen sınırlar için `LIMITATIONS.md`.

## Faz 1–2: Temel kurulum
- 14 temel motor tanımlandб: IntelligenceGraph, UTE/SSOT, UnifiedAlertingCore, SafetyGovernor, ReviewManager, VerificationManager, IncidentControlCenter, GlobalObservabilityDashboard, vb.
- Pipeline mimarisø: DataSourceManager → NER → ContradictionDetector → TruthEngine/SSOT → IntelligenceGraph/ChainManager → ReasoningEngine → UAC → USL → SafetyGovernor → ReviewManager → VerificationManager → ICC → GDD.

## Faz 3: ChainManager entegrasyonu
- `IntelligenceGraph.chain_manager` alanı eklendi (constructor injection, opsiyonel).
- `resolve_evidence_contradictions()` chain_manager varsa `add_evidence_batch()` çağırır (tek detect+compute), yoksa in-memory fallback.
- In-memory path backward-compat korundu.

## Faz 4: ICC + GDD wire
- ICC pipeline'a bağlandı: UnifiedAlertingCore metriklerinden + SafetyGovernor ESCALATE olaylarından otomatik incident üretir.
- Lifecycle düzeltildi: review approval `confirm_alert()` çağırır (confirmed=True, resolved=False). `mark_remediated()` ile resolved=True olur.
- GDD (GlobalObservabilityDashboard) pipeline'a bağlandı.
- 11/11 consistency checks PASS.

## Faz T: Motor tipolojisi analizi
- VM vs RM: tamamlayıcı (sırayla çalışır).
- USL vs SG: farklı seviyeler (USL operasyonel guard, SG policy onayı).
- SSOT → UTE delegate: `set()` → `ute.write()`, `get()` → `ute.read()`. Backward compat.
- Python 3.13 fix: `VerificationStorage._row_to_record` `dict(row)` kullanır (`sqlite3.Row` `.get()` yok).

## Faz 5: URLhaus ilk gerçek veri
- 22,667 CSV girişi indirildi; 50 örnek; 0 crash; 100% IP extraction; 100% domain extraction; 1 alert / 2 incidents.
- EntityMatcher 132→81 node birleştirdi.

## Faz 5.5: NER DOMAIN FP düzeltme
- `intelgraph/core/nlp/_tlds.py`: IANA_TLDS (1,437), FILENAME_EXTS, AMBIGUOUS_EXTS, SAFE_FILENAME_EXTS.
- `_classify_domain_match()`: URL context (`urlparse`) + hostname check + TLD + filename ext.
- Sonuç: 19,794 raw match → 8,946 DOMAIN (45%), 10,144 FILENAME (51%), 704 UNKNOWN (4%).

## Faz 6: OTX ikinci kaynak
- `intelgraph/core/source/otx.py`: `OtxClient` (OTX_API_KEY env).
- 5 pulse, 171 IOC. OTX × URLhaus: 0 ortak IOC.
- NER FP fix OTX verisinde doğrulandı: 92 DOMAIN, 3 FILENAME, 1 UNKNOWN.

## Faz 7: Dashboard backend + frontend
- `intelgraph/api/routers/dashboard.py`: 4 endpoint (`/summary`, `/ner-stats`, `/incidents`, `/sources`).
- `intelgraph/web/dashboard.html`: Chart.js doughnut, metric cards, incident table, pipeline flow.
- DashboardState disk-persist edildi: `/tmp/opencode/phase7/dashboard_state.json`.

## Faz 7.1: CSP fix
- Route-based relaxation: `/web/` ve `/` için script-src + style-src + img-src + connect-src geçitleri; API'da strict `default-src 'self'`.

## Faz 8: graph.graph + api.main direkt doğrulama
- 24/21 checks PASS: Server 1/1, graph.graph 13/12, auth 6/6, rate limit 4/3.
- Rate limiter fix: `_limiter._buckets.clear()` `setup_rate_limiting()`'de — her `create_app()`'ta reset.

## Faz 9: Tam ölçek stress test
- URLhaus 22,365 satır, 55,694 entity, 1.2MB metin, 82.84s NER, 27.8MB peak.
- 3 O(n²) darboğaz: (1) NER `any()` 437M iterasyon [ACİL], (2) EntityMatcher ~100K eşiği [kabul edilebilir], (3) ContradictionDetector 22s [kabul edilebilir].
- NER FP oranı: %53.1 FILENAME vs DOMAIN.

## Faz 9.1: NER optimizasyonu
- `bisect.bisect_right()` ile O(log n) url_spans araması: 82.84s → **0.65s (128× hızlanma)**.
- FP oran değişmedi (%53.1).
- EntityMatcher profillendi: us/entity linear; ~100K node eşiğinde optimizasyon gerekir.

## Faz 10: CISA KEV üçüncü kaynak
- 1,629 KEV kaydı entegre edildi. NER CVE recall %105.2, 0 FP.
- 4 gerçek URLhaus∩KEV çapraz referansı bulundu.
- Pipeline graph builder'da CveEntity eksikti → CVE'ler IPAddress node oluyordu.

## Faz 10.1: CveEntity sınıfı
- `intelgraph/core/entity/cve.py`: `CveEntity(BaseEntity)` — frozen dataclass, 8 CVE alanı.
- EntityType.CVE enum'a eklendi. Pipeline graph builder ve API entities router'a bağlandı.
- 19 CveEntity node başarıyla oluşturuldu. 3 entity tipi beraber çalışıyor.

## Faz 10.2: RelationshipExtractor pipeline entegrasyonu
- 3-pass co-occurrence: verb-based (0.6), same-sentence (0.5), document-level (0.35).
- Pipeline'a NER sonrası, graph edge'lerden önce eklendi.
- 36 edge (12 CVE→IP, 24 CVE→Domain). 0% same-type FP edge.

## Faz 10.3: Büyük ölçek FP ölçümü
- 22,365 URLhaus + 1,629 KEV → 109 relationship (49 verb, 56 sentence, 4 document). **0% FP**.
- `min_confidence` parametresi eklendi (varsayılan 0.0) — filtreye gerek yok.

## Faz 11: Explainable Reasoning
- `intelgraph/core/explanation/builder.py`: `ExplanationBuilder` mevcut 9 veri kaynağını birleştirir (yeni motor değil).
- `/dashboard/incidents/{id}/explain` endpoint. 11 adımlı kanıt zinciri + insan-okunabilir narrative.

## Faz 11.1: 3 eksik veri alanı
- `MetaAlert.entity_id`: ICC ve SafetyGovernor bağlamına eklendi.
- `graph_nodes_summary`: `PipelineResult.to_dict()`'e eklendi — node tip, identifier, confidence, evidence_count.
- `merge_audit`: `IntelligenceGraph.merge_audit` property'si, `PipelineResult.to_dict()`'e dahil.
- ExplanationBuilder her üç alanı da kullanır.

## Faz 12: CISA KEV ransomware → confidence boost
- `_classify_ip_match` ile KEV metninde `Ransomware campaign use: Known` regex tespiti.
- `raw_val` boost: 90→100 (value_data'da). `truth_conf` boost: 0.9→1.0.
- `value_data["known_ransomware_use"]` UTE'ye yazılır, CveEntity'ye aktarılır.
- Evidence `trust_score` ve `reliability_score` 100'e çıkar. Chain confidence 97+ (merged entity avg).
- `graph.py:218` `_evidence_to_items` `ev.reliability_score` kullanır (eski: `ev.trust_score`).
- Sonuç: Known avg=97.5, Unknown avg=76.0 (+21.5 boost). Risk score 1.0, ESCALATE tetiklenir.

## Faz 13: NER versiyon/IP karışıklığı düzeltmesi
- `_classify_ip_match()`: 5 seviyeli sınıflandırma hiyerarşisi.
  1. Octet > 255 → VERSION (kesin)
  2. URL içinde → IP
  3. Version keyword immediately before → VERSION
  4. IP keyword in window → IP
  5. Default → IP (muhafazakar)
- `_VERSION_KEYWORDS`: version, sürüm, release, build, update, patch, before, prior to, up to, through, fixed in, patched in, updated to, affects, impacts, firmware, vb.
- `_VERSION_OPERATORS`: <=, >=, <, >, =
- "v" prefix regex: `\bv\.?\s*$`
- Pipeline VERSION etiketli entity'leri fact'lara eklemez; RelationshipExtractor'a VERMİYORUZ.
- 17/17 hedef vaka PASS. KEV'de 2 FP IP → 2 VERSION (ikisi de doğru). URLhaus'ta 13,637/13,637 IP korundu (%100).

## Faz 14: Final sağlık kontrolü
- pytest: **1448 passed, 0 failed** (90s).
- 3 kaynak pipeline: 0.74s, 58 node (34 Domain, 14 IP, 10 CveEntity), 20 edge, 1 alert, 2 incident, 41 relationship, 510 çelişki, 0 hata.
- CveEntity ransomware boost: Known avg=97.5, Unknown avg=76.0.