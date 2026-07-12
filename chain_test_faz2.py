#!/usr/bin/env python3
"""
Pipeline doğrulaması — AYNI Pazartesi/Salı senaryosu, TEK çağrı.
"""

from __future__ import annotations

from intelgraph.core.pipeline.chain import Pipeline

print("=" * 72)
print("PIPELINE DOĞRULAMASI — FAZ 2")
print("Tek orkestrasyon çağrısıyla Pazartesi/Salı senaryosu")
print("=" * 72)

pipeline = Pipeline()

sources = [
    {
        "id": "log_pazartesi",
        "name": "Pazartesi Log (internal_logs)",
        "text": (
            "192.168.1.5 adresinden şüpheli giriş denemesi tespit edildi. "
            "Güven seviyesi: düşük (30/100). Kaynak: internal_logs."
        ),
        "value": 30,
    },
    {
        "id": "threat_sali",
        "name": "Salı Threat Report (MISP)",
        "text": (
            "192.168.1.5 adresi bilinen bir C2 sunucusu olarak tespit edildi. "
            "APT29 ile ilişkili. Güven seviyesi: yüksek (90/100). "
            "Kaynak: MISP threat intel."
        ),
        "value": 90,
    },
]

thresholds = {
    "c2_detection": {
        "enabled": True,
        "metric_key": "overall_confidence",
        "max": 0.4,
        "severity": "critical",
    },
    "attack_path_found": {
        "enabled": True,
        "metric_key": "attack_path_found",
        "max": 0,
        "severity": "high",
    },
}

result = pipeline.run(
    sources=sources,
    thresholds=thresholds,
    query_ip="192.168.1.5",
    query_target="",
)

print("\n" + "=" * 72)
print("PIPELINE SONUCU")
print("=" * 72)

print(f"\n  Kaynak sayısı:         {len(result.source_texts)}")
print(f"  Çıkarılan entity:      {len(result.extracted_entities)}")
for e in result.extracted_entities:
    print(f"    {e.label:10s} '{e.text}' (conf={e.confidence})")

print(f"\n  Çelişki sayısı:          {len(result.contradictions)}")
for c in result.contradictions:
    print(f"    {c.contradiction_type} ({c.severity}): {c.explanation}")

print("\n  Truth entries:")
for te in result.truth_entries:
    print(f"    {te['key']}: truth={te['truth']['action']}, ssot={te['ssot']}")

print(f"\n  Graph node sayısı:       {len(result.graph.nodes) if result.graph else 0}")
if result.graph:
    for nid, node in result.graph.nodes.items():
        print(f"    {nid}: {node.entity.__class__.__name__}")

print(f"\n  Path sayısı:             {len(result.reasoning_paths)}")
for p in result.reasoning_paths:
    summary = p.to_path_summary()
    print(f"    [{p.total_confidence:.2f}] {summary[:100]}")

print(f"\n  Alert sayısı:            {len(result.alerts)}")
for a in result.alerts:
    print(f"    ┌─ ID:      {a['alert_id']}")
    print(f"    ├─ Kategori: {a['category']}")
    print(f"    ├─ Severity: {a['severity']}")
    print(f"    ├─ Mesaj:    {a['message']}")
    print(f"    ├─ Değer:    {a.get('current_value')} (thresh: {a.get('threshold_value')})")
    if a.get("context"):
        ctx = a["context"]
        if ctx.get("entity_id"):
            print(f"    ├─ Entity:   {ctx['entity_id']}")
        if ctx.get("source_summary"):
            print(f"    ├─ Kaynak:   {ctx['source_summary']}")
        if ctx.get("confidence") is not None:
            print(f"    ├─ Conf:     {ctx['confidence']}")
        if ctx.get("contradiction"):
            print(f"    ├─ Çelişki:  {ctx['contradiction']}")
        if ctx.get("path_summary"):
            print(f"    ├─ Path:     {ctx['path_summary'][:100]}")
        if ctx.get("raw_context"):
            print(f"    └─ Bağlam:   '{ctx['raw_context'][:80]}...'")

print(f"\n  Hata sayısı:             {len(result.errors)}")
for err in result.errors:
    print(f"    ❌ {err}")

print("\n" + "=" * 72)
print("KARŞILAŞTIRMA: Manuel (Faz 1) vs Pipeline (Faz 2)")
print("=" * 72)

print("""
  Adım           | Faz 1 (manuel)           | Faz 2 (pipeline)
  ───────────────┼──────────────────────────┼──────────────────────────
  1→2 DSM→NER   | 15 satır köprü kodu      | Otomatik (Pipeline.run)
  2→3 NER→Detect | elle dict oluşturma       | ExtractedEntity.to_contradiction_dict()
  3→4 Truth→Ent  | elle IPAddress oluşturma  | Otomatik factory
  4→5 Path→Alert | elle metrics dict         | ReasoningPath.to_alert_metrics()
  Alert mesajı   | generic: "X exceeds Y"    | "IP — source — conf — path — contradiction"
  Orkestrasyon   | manuel sıralama           | Tek çağrı: Pipeline.run(sources)

  FAZ 1: 5 köprü × ortalama 12 satır = ~60 satır manuel kod
  FAZ 2: 0 satır manuel kod (tek çağrı)
""")

pipeline.cleanup()
