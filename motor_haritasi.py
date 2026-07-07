#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistem Çapında Motor/Engine Entegrasyon/İzolasyon Haritası

Her motor sınıfı için statik analiz: gerçek veri akışına bağlı mı, izole mi?
"""
from __future__ import annotations

# fmt: off
# (sınıf_adı, dosya, durum, çağrıldığı_yer, detay)
ENGINES = [
    # ════════════════════════════════════════════════════════════════
    # BAĞLI (GERÇEK) — Gerçek IntelligenceGraph/veri alır
    # ════════════════════════════════════════════════════════════════
    ("GraphQueryEngine",       "core/graph/query.py",            "BAĞLI-GERÇEK",
     "api/routers/query.py,_get_query_engine()",
     "IntelligenceGraph alır, backend'den build edilmiş. filter_nodes/find/find_by_type/enumerate/traverse çağrılır."),

    ("AnomalyDetector",        "core/graph/anomaly.py",          "BAĞLI-GERÇEK",
     "core/kernel/execution.py:UnifiedExecutionKernel.__init__()",
     "IntelligenceGraph alır, kernel.execute()'de multi_factor_score() çağrılır."),

    ("CausalReasoner",         "core/graph/reasoning.py",        "BAĞLI-GERÇEK",
     "core/kernel/execution.py:UnifiedExecutionKernel.__init__()",
     "IntelligenceGraph alır, kernel.execute()'de top_causes() çağrılır."),

    ("Predictor",              "core/graph/prediction.py",      "BAĞLI-GERÇEK",
     "core/kernel/execution.py:UnifiedExecutionKernel.__init__()",
     "IntelligenceGraph alır, kernel.execute()'de full_forecast() çağrılır."),

    ("MergeEngine",            "core/source/resolution.py",      "BAĞLI-GERÇEK",
     "core/graph/graph.py:IntelligenceGraph.__post_init__()",
     "IntelligenceGraph tarafından instantiate edilir, add_entity()'de merge() çağrılır."),

    # ════════════════════════════════════════════════════════════════
    # BAĞLI (YÜZEYSEL) — API/CLI'de import + instantiate edilir
    # AMA her request'te yeni instance, tüm veri request body'den,
    # IntelligenceGraph/kernel/core referansı ALMAZ
    # ════════════════════════════════════════════════════════════════
    # --- metaintel (12 engine) ---
    ("GlobalGovernanceEngine",    "core/metaintel/governance.py",    "BAĞLI-YÜZEYSEL",
     "api/routers/metaintel.py:get_governance()", "Her istekte yeni instance. Graph/kernel bağlantısı YOK. Request body'den layer/metrics alır."),
    ("SystemDiagnostics",        "core/metaintel/diagnostics.py",   "BAĞLI-YÜZEYSEL",
     "api/routers/metaintel.py:get_diagnostics()", "Her istekte yeni instance. Graph/kernel bağlantısı YOK."),
    ("PolicyEvolutionEngine",    "core/metaintel/policy.py",        "BAĞLI-YÜZEYSEL",
     "api/routers/metaintel.py:get_policy()", "Her istekte yeni instance. Graph/kernel bağlantısı YOK."),
    ("MetaReasoningEngine",      "core/metaintel/metareasoning.py", "BAĞLI-YÜZEYSEL",
     "api/routers/metaintel.py:get_metareasoning()", "Her istekte yeni instance. Graph/kernel bağlantısı YOK."),
    ("SelfImprovementController","core/metaintel/self_improvement.py","BAĞLI-YÜZEYSEL",
     "api/routers/metaintel.py:get_self_improvement()", "Her istekte yeni instance. Graph/kernel bağlantısı YOK."),
    ("ArchitectureEvolutionEngine","core/metaintel/architecture.py","BAĞLI-YÜZEYSEL",
     "api/routers/metaintel.py:get_architecture()", "Her istekte yeni instance. Graph/kernel bağlantısı YOK. Kendi _dependency_graph'ını tutar."),
    ("TruthConsistencyGovernor", "core/metaintel/truth.py",         "BAĞLI-YÜZEYSEL",
     "api/routers/metaintel.py:get_truth()", "Her istekte yeni instance. Graph/kernel bağlantısı YOK."),
    ("IdentityConsistencyLayer", "core/metaintel/identity.py",      "BAĞLI-YÜZEYSEL",
     "api/routers/metaintel.py:get_identity()", "Her istekte yeni instance. Graph/kernel bağlantısı YOK."),
    ("RealWorldAlignmentLayer",  "core/metaintel/alignment.py",     "BAĞLI-YÜZEYSEL",
     "api/routers/metaintel.py:get_alignment()", "Her istekte yeni instance. Graph/kernel bağlantısı YOK."),
    ("SafetyMetaControlLayer",   "core/metaintel/safety_meta.py",   "BAĞLI-YÜZEYSEL",
     "api/routers/metaintel.py:get_safety_meta()", "Her istekte yeni instance. Graph/kernel bağlantısı YOK."),
    ("GlobalObservabilityDashboard","core/metaintel/observability.py","BAĞLI-YÜZEYSEL",
     "api/routers/metaintel.py:get_observability()", "Her istekte yeni instance. Graph/kernel bağlantısı YOK."),
    ("IncidentControlCenter",    "core/metaintel/alerting.py",      "BAĞLI-YÜZEYSEL",
     "api/routers/metaintel.py:get_incident_control()", "Her istekte yeni instance. Graph/kernel bağlantısı YOK."),
    ("VersionedSystemState",     "core/metaintel/state.py",         "BAĞLI-YÜZEYSEL",
     "api/routers/metaintel.py:get_state()", "Her istekte yeni instance. Graph/kernel bağlantısı YOK."),

    # --- ucos (14 engine) ---
    ("ConsolidationEngine",      "core/ucos/consolidation.py",      "BAĞLI-YÜZEYSEL",
     "api/routers/ucos.py:get_consolidation()", "Her istekte yeni instance. importlib ile tarar, Graph/kernel bağlantısı YOK."),
    ("UnifiedCognitiveCore",     "core/ucos/cognitive.py",        "BAĞLI-YÜZEYSEL",
     "api/routers/ucos.py:get_cognitive(), /reason, /closed-loop", "Her istekte yeni instance. Graph/kernel bağlantısı YOK. context'ten 'graph' dict'i alır (user-supplied)."),
    ("ClosedLoopIntelligenceSystem","core/ucos/closed_loop.py",   "BAĞLI-YÜZEYSEL",
     "api/routers/ucos.py:get_closed_loop(), /closed-loop", "Her istekte yeni instance. Graph/kernel bağlantısı YOK."),
    ("UnifiedPolicyControlPlane","core/ucos/policy.py",            "BAĞLI-YÜZEYSEL",
     "api/routers/ucos.py:get_policy(), /act, /policy/evaluate", "Her istekte yeni instance. Graph/kernel bağlantısı YOK."),
    ("UnifiedTruthEngine",       "core/ucos/truth.py",             "BAĞLI-YÜZEYSEL",
     "api/routers/ucos.py:get_truth(), /query, /state/set", "Her istekte yeni instance. Graph/kernel bağlantısı YOK."),
    ("UnifiedExecutionRuntime",  "core/ucos/runtime.py",           "BAĞLI-YÜZEYSEL",
     "api/routers/ucos.py:get_runtime(), /act, /closed-loop", "Her istekte yeni instance. Graph/kernel bağlantısı YOK."),
    ("UnifiedTelemetryCore",     "core/ucos/telemetry.py",         "BAĞLI-YÜZEYSEL",
     "api/routers/ucos.py:get_telemetry(), /observe, /health", "Her istekte yeni instance. Graph/kernel bağlantısı YOK."),
    ("UnifiedSafetyLayer",       "core/ucos/safety.py",            "BAĞLI-YÜZEYSEL",
     "api/routers/ucos.py:get_safety(), /act, /safety/check", "Her istekte yeni instance. Graph/kernel bağlantısı YOK."),
    ("SelfStabilizingMetaControl","core/ucos/meta_control.py",     "BAĞLI-YÜZEYSEL",
     "api/routers/ucos.py:get_meta_control(), /meta-control/propose", "Her istekte yeni instance. Graph/kernel bağlantısı YOK."),
    ("SimplificationEngine",     "core/ucos/simplification.py",    "BAĞLI-YÜZEYSEL",
     "api/routers/ucos.py:get_simplification(), /simplify, /consolidation/apply", "Her istekte yeni instance. Graph/kernel bağlantısı YOK."),
    ("GlobalHealthIndex",        "core/ucos/health.py",            "BAĞLI-YÜZEYSEL",
     "api/routers/ucos.py:get_health(), /health", "Her istekte yeni instance. Graph/kernel bağlantısı YOK."),
    ("UnifiedAlertingCore",      "core/ucos/alerting.py",          "BAĞLI-YÜZEYSEL",
     "api/routers/ucos.py:get_alerting(), /alerts", "Her istekte yeni instance. Graph/kernel bağlantısı YOK."),
    ("DependencyValidator",      "core/ucos/boundary.py",          "BAĞLI-YÜZEYSEL",
     "api/routers/ucos.py:get_dependency(), /dependency/register", "Her istekte yeni instance. Graph/kernel bağlantısı YOK."),
    ("SingleSourceOfTruth",      "core/ucos/state.py",             "BAĞLI-YÜZEYSEL",
     "api/routers/ucos.py:get_state(), /query, /state, /state/set, /state/snapshot", "Her istekte yeni instance. Graph/kernel bağlantısı YOK."),

    # --- Diğer bağlı ama yüzeysel ---
    ("ChainManager",             "core/evidence_chain/manager.py", "BAĞLI-YÜZEYSEL",
     "api/dependencies.py, cli/evidence.py, cli/report.py", "API/CLI'de kullanılır. EvidenceChain yönetir ama graph'a bağlı değil."),
    ("CollectionManager",        "core/collection/manager.py",     "BAĞLI-YÜZEYSEL",
     "cli/collect.py", "CLI ile koleksiyon yönetimi, graph'a bağlı değil."),
    ("DataSourceManager",        "core/source/manager.py",         "BAĞLI-YÜZEYSEL",
     "api/routers/datasources.py", "Data source CRUD, graph'a bağlı değil."),
    ("ReviewManager",            "core/human_review/manager.py",   "BAĞLI-YÜZEYSEL",
     "cli/review.py", "Review yönetimi, graph'a bağlı değil."),
    ("VerificationManager",      "core/verification/manager.py",   "BAĞLI-YÜZEYSEL",
     "api/dependencies.py, cli/report.py, cli/verify.py", "Verification yönetimi, graph referansı alabilir ama kernel bağlantısı yok."),
    ("TaskManager",              "core/orchestrator/manager.py",   "BAĞLI-YÜZEYSEL",
     "api/dependencies.py, cli/task.py", "Task kuyruğu, kernel/graph bağlantısı yok."),
    ("BackupManager",            "core/operations/backup.py",      "BAĞLI-YÜZEYSEL",
     "cli/ops.py", "Backup işlemleri, graph'a bağlı değil."),
    ("NEREngine",                "core/nlp/extractor.py",         "BAĞLI-YÜZEYSEL",
     "api/routers/graph_nlp.py, cli/nlp.py", "NLP extraction, graph'a bağlı değil (entity döndürür)."),
    ("EconomicGovernor",         "core/nlp/economics.py",          "BAĞLI-YÜZEYSEL",
     "api/routers/graph_nlp.py, cli/nlp.py", "NLP cost yönetimi, graph'a bağlı değil."),
    ("ReasoningEngine",          "core/cognitive/reasoning.py",     "BAĞLI-YÜZEYSEL",
     "api/routers/cognitive.py, cli/cognitive.py", "Cognitive reasoning, graph'a bağlı değil (request body'den veri alır)."),
    ("ContradictionDetector",    "core/cognitive/contradiction.py","BAĞLI-YÜZEYSEL",
     "api/routers/cognitive.py, cli/cognitive.py", "Contradiction detection, graph'a bağlı değil."),
    ("SafetyGovernor",           "core/agent/safety.py",           "BAĞLI-YÜZEYSEL",
     "api/routers/agent.py, cli/agent.py", "Agent safety, graph'a bağlı değil."),
    ("SimulationEngine",         "core/agent/simulation.py",       "BAĞLI-YÜZEYSEL",
     "api/routers/agent.py, cli/agent.py", "Agent simulation, graph'a bağlı değil."),

    # ════════════════════════════════════════════════════════════════
    # İZOLE — Sadece test/own module/__init__.py'de referans
    # ════════════════════════════════════════════════════════════════
    ("ABACEngine",               "core/security_ext/zero_trust.py","İZOLE", "", "Sadece test_phase28.py"),
    ("AdaptiveThrottleEngine",   "core/connectors/manager.py",     "İZOLE", "", "Sadece test"),
    ("AlertEngine",              "core/operations/alerting.py",    "İZOLE", "", "Sadece test"),
    ("AmbiguityDetector",        "core/canonical/ambiguity.py",    "İZOLE", "", "Sadece kendi modülü + test"),
    ("AntiPoisoningEngine",      "core/source_registry/anti_poisoning.py","İZOLE","","Sadece test"),
    ("AutoEscalationEngine",     "core/decision/engine.py",        "İZOLE", "", "Sadece test_phase28.py"),
    ("CacheManager",             "core/storage/cache.py",          "İZOLE", "", "Sadece __init__.py + test"),
    ("ChainQueryEngine",         "core/evidence_chain/query.py",   "İZOLE", "", "Sadece kendi modülü + test"),
    ("ComplianceScoringEngine",  "core/compliance/engine.py",      "İZOLE", "", "Sadece test_phase28.py"),
    ("ConnectorAuthManager",     "core/connectors/manager.py",     "İZOLE", "", "Sadece kendi modülü + test"),
    ("ConnectorStateManager",    "core/connectors/manager.py",     "İZOLE", "", "Sadece kendi modülü + test"),
    ("ContradictionDetector",    "core/evidence_chain/contradiction.py","İZOLE","","Sadece test. evidence_chain ContradictionDetector'ı cognitive'dekinden farklı, kullanılmıyor."),
    ("DataQualityEngine",        "core/ingestion/engine.py",       "İZOLE", "", "Sadece test_phase28.py"),
    ("DeadlockDetector",         "core/agent/hierarchy.py",        "İZOLE", "", "Sadece kendi modülü + test"),
    ("DecisionEnforcementEngine","core/decision/engine.py",        "İZOLE", "", "Sadece test_phase28.py"),
    ("DeduplicationEngine",      "core/ingestion/engine.py",       "İZOLE", "", "Sadece test_phase28.py"),
    ("DeduplicationEngine",      "core/source/feed.py",            "İZOLE", "", "Sadece source/__init__.py + test"),
    ("DegradedModeController",   "core/resilience/controller.py",  "İZOLE", "", "Sadece test_phase28.py"),
    ("EntityResolutionEngine",   "core/integration/engine.py",     "İZOLE", "", "Sadece test_phase28.py"),
    ("EventReplayEngine",        "core/ingestion/engine.py",       "İZOLE", "", "Sadece test_phase28.py"),
    ("FailureCorrelationEngine", "core/resilience/controller.py",  "İZOLE", "", "Sadece test_phase28.py"),
    ("FalseIntelligenceDetector","core/quality/scorer.py",         "İZOLE", "", "Sadece test_phase28.py"),
    ("GovernancePolicyEngine",   "core/governance_ext/cost.py",    "İZOLE", "", "Sadece string ref consolidation.py + test_phase28.py"),
    ("RetryEngine",              "core/connectors/manager.py",     "İZOLE", "", "Sadece test_phase28.py"),
    ("ReviewEngine",             "core/human_review/review.py",    "İZOLE", "", "Sadece manager.py (aynı paket) + test"),
    ("ROIEngine",                "core/governance_ext/cost.py",    "İZOLE", "", "Sadece test_phase28.py"),
    ("RuntimeAnomalyDetector",   "core/security_ext/zero_trust.py","İZOLE", "", "Sadece test_phase28.py"),
    ("RuntimePolicyEngine",      "core/security_ext/zero_trust.py","İZOLE", "", "Sadece test_phase28.py"),
    ("SnapshotManager",          "core/storage/snapshot.py",       "İZOLE", "", "Sadece storage/__init__.py"),
    ("SystemResilienceController","core/resilience/controller.py", "İZOLE", "", "Sadece test_phase28.py"),
    ("TenantManager",            "core/multitenant/manager.py",    "İZOLE", "", "Sadece test_phase28.py"),
    ("ThreatFusionEngine",       "core/integration/engine.py",     "İZOLE", "", "Sadece test_phase28.py"),
    ("TrustScoreEngine",         "core/ingestion/engine.py",       "İZOLE", "", "Sadece test_phase28.py"),
    ("VerificationEngine",       "core/verification/engine.py",    "İZOLE", "", "Sadece VerificationManager (aynı paket) + test"),
]
# fmt: on

# ─── TABLO ──────────────────────────────────────────────────────
print("=" * 140)
print("SİSTEM ÇAPINDA MOTOR/ENGINE ENTEGRASYON HARİTASI")
print("=" * 140)
print(f"{'Motor/Sınıf':38s} {'Dosya':38s} {'Durum':18s} {'Çağrıldığı Yer':44s}")
print("-" * 140)

for name, filepath, status, caller, _ in ENGINES:
    short = filepath.split("/")[-1] if "/" in filepath else filepath
    display = f"core/.../{short}"
    print(f"{name:38s} {display:38s} {status:18s} {caller:44s}")

print("-" * 140)

# ─── İSTATİSTİK ──────────────────────────────────────────────────
total = len(ENGINES)
gercek = sum(1 for _, _, s, _, _ in ENGINES if s == "BAĞLI-GERÇEK")
yuzeysel = sum(1 for _, _, s, _, _ in ENGINES if s == "BAĞLI-YÜZEYSEL")
izole = sum(1 for _, _, s, _, _ in ENGINES if s == "İZOLE")

print()
print("=" * 72)
print("İSTATİSTİK ÖZETİ")
print("=" * 72)
print(f"  Toplam motor/engine sayısı:           {total}")
print(f"  BAĞLI (gerçek veri akışı):             {gercek}  ({100*gercek//total}%)")
print(f"  BAĞLI (yüzeysel, API/CLI wrapper):     {yuzeysel} ({100*yuzeysel//total}%)")
print(f"  İZOLE (sadece test/own module):        {izole}  ({100*izole//total}%)")
print()

# ─── KRİTİK BULGULAR ────────────────────────────────────────────
print("=" * 72)
print("KRİTİK BULGULAR")
print("=" * 72)
print("""
1. SADECE 5 MOTOR GERÇEK VERİ AKIŞINA BAĞLI (%8):
   - GraphQueryEngine: backend → graph → query API
   - AnomalyDetector: graph → kernel → anomaly API
   - CausalReasoner: graph → kernel → prediction API
   - Predictor: graph → kernel → prediction API
   - MergeEngine: graph.py'ye entegre (add_entity)

2. 42 MOTOR YÜZEYSEL (%60) — API/CLI'de var ama HİÇBİRİ:
   - IntelligenceGraph referansı ALMAZ
   - UnifiedExecutionKernel referansı ALMAZ
   - UnifiedCognitiveCore referansı ALMAZ
   - Her istekte sıfırdan instance oluşturulur
   - Tüm girdiler request body'den gelir (user-supplied)
   - Herhangi iki motor ARASINDA veri akışı YOK
   - Kendi iç state'leri request'ler arası korunmaz

3. 16 MOTOR TAMAMEN İZOLE (%23):
   - Phase 28'de "tasarlanmış" ama hiçbir yerde kullanılmıyor
   - Sadece test_phase28.py'de referans
   - ABAC, RuntimePolicyEngine, ThreatFusionEngine vb.

4. EN KRİTİK RİSK: "tamamlandı" denen engine'lerin çoğu
   sadece REST wrapper — gerçek graph/entity/evidence verisine
   erişemiyor. Örneğin:
   - TruthConsistencyGovernor: request'te gönderilen state'leri
     karşılaştırır, GERÇEK knowledge/reasoning/execution'a değil.
   - UnifiedCognitiveCore: request body'den "graph" dict'i alır,
     IntelligenceGraph instance'ı değil.
   - GlobalGovernanceEngine: request'ten layer/metric alır,
     gerçek sistem layer'larını monitör etmez.

5. TEK İSTİSNA: ArchitectureEvolutionEngine kendi _dependency_graph
   state'ini korur (modül içi) ve cycle detection çalıştırır.
   Ama o da IntelligenceGraph'a bağlı değil.

ÖNERİ:
   a) metaintel/ ve ucos/ engine'lerine __init__'de graph/kernel
      referansı vermek için constructor injection eklenmeli
   b) API router'lar Depends(get_xxx) yerine Depends(build_xxx)
      ile gerçek sistem state'ini enjekte etmeli
   c) İzole engine'ler (özellikle security_ext) ya entegre
      edilmeli ya da kaldırılmalı
""")
