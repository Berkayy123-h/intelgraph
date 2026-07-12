from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import StreamingResponse

from intelgraph.core.graph.export import ExportSettings, GraphExporter
from intelgraph.core.graph.graph import IntelligenceGraph
from intelgraph.core.graph.node import Node

router = APIRouter(prefix="/export", tags=["export"])

_CONTENT_TYPES = {
    "graphml": "application/xml",
    "gexf": "application/xml",
    "json": "application/json",
    "csv": "text/csv",
}


def _build_graph() -> IntelligenceGraph:
    from intelgraph.api.main import _container

    g = IntelligenceGraph()
    for entity in _container.backend.list_entities():
        eid = entity.id
        g.nodes[eid] = Node(entity=entity)
        g.adjacency.setdefault(eid, set())
        g.forward_adjacency.setdefault(eid, set())
        g.reverse_adjacency.setdefault(eid, set())
        g.node_edges.setdefault(eid, set())
    for rel in _container.backend.list_relationships():
        src = rel.source_id
        tgt = rel.target_id
        if src in g.nodes and tgt in g.nodes:
            g.adjacency.setdefault(src, set()).add(tgt)
            g.adjacency.setdefault(tgt, set()).add(src)
            g.forward_adjacency.setdefault(src, set()).add(tgt)
            g.reverse_adjacency.setdefault(tgt, set()).add(src)
            g.node_edges.setdefault(src, set()).add(rel.id)
            g.node_edges.setdefault(tgt, set()).add(rel.id)
            g.edge_node_map[rel.id] = (src, tgt)
            from intelgraph.core.graph.edge import Edge

            g.edges[rel.id] = Edge(relationship=rel)
    return g


@router.get(
    "/graph",
    summary="Export graph in popular formats",
    description="Export the intelligence graph in GraphML, GEXF, JSON, or CSV format. Supports temporal filtering, confidence/threat-score thresholds, and entity type filters. Streaming for large graphs.",
)
def export_graph(
    request: Request,
    format: str = Query("graphml", description="Export format: graphml, gexf, json, csv"),
    since: str | None = Query(
        None, description="Include only data since (ISO datetime or relative like 7d, 30d)"
    ),
    until: str | None = Query(None, description="Include only data until (ISO datetime)"),
    min_confidence: int = Query(0, ge=0, le=100, description="Minimum confidence score"),
    min_threat_score: float = Query(0.0, ge=0.0, le=100.0, description="Minimum threat score"),
    entity_types: list[str] = Query(
        default=[], description="Include only specific entity types (e.g. ip_address, domain, cve)"
    ),
):
    if format not in GraphExporter.SUPPORTED_FORMATS:
        alts = ", ".join(sorted(GraphExporter.SUPPORTED_FORMATS))
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format: {format}. Supported: {alts}.",
        )

    graph = _build_graph()
    if graph.node_count == 0:
        from fastapi.responses import JSONResponse

        return JSONResponse(
            status_code=200,
            content={
                "status": "empty",
                "message": "Graph is empty. Run a pipeline first to generate data.",
            },
        )

    settings = ExportSettings(
        include_entity_types=set(entity_types) if entity_types else None,
        min_confidence=min_confidence,
        min_threat_score=min_threat_score,
        since=since,
        until=until,
        include_metadata=True,
    )

    content_type = _CONTENT_TYPES.get(format, "application/octet-stream")

    exporter = GraphExporter(graph, settings)

    def _stream():
        yield from exporter.export_iter(format)

    return StreamingResponse(
        _stream(),
        media_type=content_type,
        headers={
            "Content-Disposition": f'attachment; filename="intelgraph.{format}"',
            "X-Export-Node-Count": str(len(exporter._get_node_list())),
            "X-Export-Edge-Count": str(len(exporter._get_edge_triples())),
        },
    )
