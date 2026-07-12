#!/usr/bin/env python3
"""
40 Yüzeysel Motoru E-IOS Ürün Değerine Göre Kategorize Et

E-IOS = Autonomous Threat Intelligence & Data Fusion Platform
(SIEM + Threat Intel + Knowledge Graph + SOAR)
"""

from __future__ import annotations

# fmt: off
# (motor, kategori, tek_cumle)
ROWS = [
    # ════════════════════════════════════════════════════════════════
    # 🔴 ÇEKİRDEK — V1'de olmazsa ürün SATILAMAZ
    # ════════════════════════════════════════════════════════════════
    ("DataSourceManager",                 "🔴 ÇEKİRDEK",
     "Threat feed'ler (MISP, OpenCTI, VT) olmadan threat intel platformu = boş kutu; DataSourceManager INPUT."),

    ("NEREngine",                          "🔴 ÇEKİRDEK",
     "Threat report/email'den IP, domain, hash çıkaramazsan analist her şeyi manuel girmek zorunda; NER olmazsa ürün satılmaz."),

    ("ContradictionDetector",             "🔴 ÇEKİRDEK",
     "'IP 10.0.0.1 zararlı' vs 'IP 10.0.0.1 zararsız' — hangisi doğru? Çelişki tespiti OLMADAN güven skoru anlamsız."),

    ("ChainManager",                      "🔴 ÇEKİRDEK",
     "Bir observable'ın kanıt zinciri (hangi kaynak, ne dedi, ne zaman) olmadan confidence/reliability hesabı yapılamaz; SOC denetimi için zorunlu."),

    ("VerificationManager",               "🔴 ÇEKİRDEK",
     "Analist 'Bu IP zararlı mı?' diye sorar, sistem 'verification pending' derse çöker; verdict mekanizması CORE."),

    ("ReviewManager",                     "🔴 ÇEKİRDEK",
     "SOAR'ın otomatik aksiyon alması için human-in-the-loop gerekir; review yoksa enterprise satılamaz ('otomatik silah' korkusu)."),

    ("ReasoningEngine",                   "🔴 ÇEKİRDEK",
     "'Bu IP ile TA444 arasında bağlantı var mı?' sorusuna multi-hop DFS ile cevap verir; graph'ın anlamı budur."),

    ("SafetyGovernor",                    "🔴 ÇEKİRDEK",
     "SOAR'ın 'block IP' aksiyonunu risk skoruna göre engeller/kısıtlar; güvenlik analisti 'yanlışlıkla google'ı blocklamayın' der."),

    ("UnifiedSafetyLayer",                "🔴 ÇEKİRDEK",
     "Kill switch + safe degradation + runaway loop detection; SOAR'da 'acil durdurma butonu' her müşterinin ilk sorduğu şey."),

    ("UnifiedAlertingCore",               "🔴 ÇEKİRDEK",
     "Tespit edilen tehditleri alerte çevirmezsen SIEM satılmaz; alert = OUTPUT."),

    ("IncidentControlCenter",             "🔴 ÇEKİRDEK",
     "Alertleri yönetmek (filtrele, kategorize et, eskalasyon) için bir merkez gerekir; aksi halde alert yağmurunda kaybolursun."),

    ("GlobalObservabilityDashboard",      "🔴 ÇEKİRDEK",
     "'Dashboard' en temel UI beklentisidir; dashboard'suz ürün proof-of-concept seviyesinde kalır."),

    ("SingleSourceOfTruth",               "🔴 ÇEKİRDEK",
     "Aynı IP hakkında 5 farklı kaynaktan gelen bilgiyi tek bir doğruluk değerinde birleştirmezsen analist hangisine güveneceğini bilemez."),

    ("UnifiedTruthEngine",                "🔴 ÇEKİRDEK",
     "Confidence-weighted truth write/read — SSOT ile birlikte çalışır; threat intel'in 'source of truth' konsepti satışın kendisidir."),

    # ════════════════════════════════════════════════════════════════
    # 🟡 İLERİDE — V1'de olmasa olur, V2/V3'te gelir
    # ════════════════════════════════════════════════════════════════
    ("GlobalGovernanceEngine",            "🟡 İLERİDE",
     "Cross-layer health + conflict resolution — enterprise compliance için V2'de gerekli olur ama core threat intel için DEĞİL."),

    ("UnifiedPolicyControlPlane",         "🟡 İLERİDE",
     "Policy evaluation (role hierarchy, risk-based override) — multi-tenant enterprise V2 özelliği. V1'de basit RBAC yeter."),

    ("PolicyEvolutionEngine",             "🟡 İLERİDE",
     "Policy'leri başarısızlık pattern'lerinden otomatik iyileştirir — V3 yapay zeka catering özelliği. V1'de manuel policy yeter."),

    ("GlobalHealthIndex",                 "🟡 İLERİDE",
     "Tek bir health score — executive dashboard için güzel ama ops internal metriği. V1'de Prometheus metrics yeter."),

    ("UnifiedTelemetryCore",              "🟡 İLERİDE",
     "İç telemetri (reasoning quality, drift) — sistem monitorizasyonu için. V1'de ops ekibi kendi tool'larını kullanır."),

    ("SystemDiagnostics",                 "🟡 İLERİDE",
     "Pipeline sağlığı, drift, bottleneck analizi — SRE/DevOps aracı. V1 MVP için gerekli değil."),

    ("SafetyMetaControlLayer",            "🟡 İLERİDE",
     "Cross-layer kill switch (birden çok sistemi aynı anda durdurur) — büyük ölçekli dağıtık SOAR için V2."),

    ("SelfImprovementController",         "🟡 İLERİDE",
     "Optimizasyon önerileri + kaynak tahsisi — 'self-healing' AI özelliği, V3+ satış argümanı."),

    ("IdentityConsistencyLayer",          "🟡 İLERİDE",
     "Multi-agent identity + role conflict detection — agent orchestrasyonu V2'de gerekli, V1'de tek user modeli yeter."),

    ("RealWorldAlignmentLayer",           "🟡 İLERİDE",
     "Sistem çıktısını gerçek dünya ile karşılaştır — 'halüsinasyon tespiti' gibi niş bir AI güvenlik özelliği. V3."),

    ("ClosedLoopIntelligenceSystem",      "🟡 İLERİDE",
     "Observe → Orient → Decide → Act döngüsü — SOAR maturity model'de Level 4. V1'de basit playbook çalıştırma yeter."),

    ("SimulationEngine",                  "🟡 İLERİDE",
     "'What-if' simülasyonu (örn. bu IP'yi blocklarsak ne olur?) — güzel ama V2 analiz özelliği. V1'de gerçek aksiyon al."),

    ("TaskManager",                       "🟡 İLERİDE",
     "Async task queue — long-running collection/SOAR için gerekli ama mevcut API zaten sync çalışıyor; V1'de timeout'la idare eder."),

    ("VersionedSystemState",              "🟡 İLERİDE",
     "SHA-256 chain + state restore — compliance/audit için enterprise V2. V1'de snapshot yedekleme yeter."),

    ("BackupManager",                     "🟡 İLERİDE",
     "SQLite/PostgreSQL backup — ops gerekli ama ürün özelliği değil. Dokümantasyon + script ile V1'de çözülür."),

    ("EconomicGovernor",                  "🟡 İLERİDE",
     "NLP/API çağrı başına cost tracking + ROI — SaaS monetizasyonu için V2+. V1'de bu kadar ince hesap gerekmez."),

    ("ArchitectureEvolutionEngine",       "🟡 İLERİDE",
     "Module lifecycle + cycle detection (kendi _dependency_graph ile). Internal tool, customer'ın göreceği bir şey değil."),

    # ════════════════════════════════════════════════════════════════
    # ⚫ GEREKSİZ/ÇAKIŞAN — Zaten var veya hiçbir senaryoda değer üretmez
    # ════════════════════════════════════════════════════════════════
    ("MetaReasoningEngine",               "⚫ GEREKSİZ/ÇAKIŞAN",
     "'Akıl yürütme hakkında akıl yürütme' — SOC analisti 'bu IP'nin C2 olma olasılığı nedir?' diye sorar, 'meta-hipotez' değil. V1'de sıfır değer."),

    ("UnifiedCognitiveCore",              "⚫ GEREKSİZ/ÇAKIŞAN",
     "ReasoningEngine (cognitive/) ile AYNI işi yapar: multi-hop DFS + contradiction + hypothesis. İkisi de request body'den graph dict alır. Biri yetmez mi? Zaten ikisi de mock."),

    ("UnifiedExecutionRuntime",           "⚫ GEREKSİZ/ÇAKIŞAN",
     "Step-based goal execution — TaskManager (orchestrator/) ile çakışır. SOAR playbook execution ayrı bir modül olmalı, bu kadar generic olmamalı."),

    ("ConsolidationEngine",               "⚫ GEREKSİZ/ÇAKIŞAN",
     "importlib ile duplicate engine tarar — engine'leri onarıp gerçek veri akışına bağladıktan sonra bu engine'in varlık sebebi kalmaz."),

    ("SimplificationEngine",              "⚫ GEREKSİZ/ÇAKIŞAN",
     "No-duplicate enforcement + complexity index. ConsolidationEngine'in yan ürünü. Customer value = 0."),

    ("SelfStabilizingMetaControl",        "⚫ GEREKSİZ/ÇAKIŞAN",
     "Approval gate + regression validation — SafetyGovernor + UnifiedSafetyLayer + PolicyEvolutionEngine zaten kapsıyor. Ek bir katman şişkinlik."),

    ("DependencyValidator",               "⚫ GEREKSİZ/ÇAKIŞAN",
     "Module dependency'lerinde circular/self-dependency kontrolü — internal dev tool. Bir SOC analisti bunu göremez bile."),

    ("CollectionManager",                 "⚫ GEREKSİZ/ÇAKIŞAN",
     "Veri toplama yönetimi — DataSourceManager zaten aynı işi yapıyor (kaynak ekleme, polling, scheduling)."),
]
# fmt: on

print("=" * 140)
print("40 YÜZEYSEL MOTOR — E-IOS ÜRÜN DEĞERİNE GÖRE KATEGORİZASYON")
print("=" * 140)
print(f"{'Motor/Sınıf':38s} {'Kategori':22s} {'Gerekçe':78s}")
print("-" * 140)
for motor, kat, gerekce in ROWS:
    # Trim long gerekce
    g = gerekce if len(gerekce) <= 78 else gerekce[:75] + "..."
    print(f"{motor:38s} {kat:22s} {g:78s}")

print("-" * 140)

# ─── İSTATİSTİK ──────────────────────────────────────────────────
cekirdek = sum(1 for _, k, _ in ROWS if k.startswith("🔴"))
ileride = sum(1 for _, k, _ in ROWS if k.startswith("🟡"))
gereksiz = sum(1 for _, k, _ in ROWS if k.startswith("⚫"))

print()
print("=" * 72)
print("ÖZET")
print("=" * 72)
print(f"  🔴 ÇEKİRDEK (V1'de şart):     {cekirdek} motor")
print(f"  🟡 İLERİDE (V2+ için):         {ileride} motor")
print(f"  ⚫ GEREKSİZ/ÇAKIŞAN:            {gereksiz} motor")

print(f"""
🔴 ÇEKİRDEK MOTORLAR ({cekirdek} adet):
""")
for motor, kat, g in ROWS:
    if "ÇEKİRDEK" in kat:
        print(f"   {motor:38s} — {g[:80]}")

print(f"""
⚫ GEREKSİZ/ÇAKIŞAN ({gereksiz} adet):
""")
for motor, kat, g in ROWS:
    if "GEREKSİZ" in kat:
        print(f"   {motor:38s} — {g[:80]}")

print(f"""
═══════════════════════════════════════════════════════════════════
BİR SONRAKİ ADIM İÇİN 🔴 ÇEKİRDEK LİSTESİ ({cekirdek} motor):
═══════════════════════════════════════════════════════════════════
""")
for motor, kat, _ in ROWS:
    if "ÇEKİRDEK" in kat:
        print(f"  • {motor}")
