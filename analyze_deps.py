#!/usr/bin/env python3
"""
AIOS Bağımlılık Haritası v2 — hassas fan-in
Sadece EXACT modül eşleşmesi ile fan-in hesaplar.
"""

from __future__ import annotations

import ast
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path("/home/berkay/intelgraph")
SOURCE_DIR = PROJECT_ROOT / "intelgraph"


def get_all_py_files(root: Path) -> list[Path]:
    return [p for p in root.rglob("*.py") if "__pycache__" not in str(p)]


def extract_module_name(filepath: Path, root: Path) -> str:
    rel = filepath.relative_to(root.parent)
    parts = list(rel.parts)
    parts[-1] = parts[-1].replace(".py", "")
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def get_imports_from_file(filepath: Path) -> set[str]:
    imports: set[str] = set()
    try:
        tree = ast.parse(filepath.read_text(encoding="utf-8"))
    except SyntaxError:
        return imports
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("intelgraph"):
                    imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.startswith("intelgraph"):
                imports.add(node.module)
    return imports


py_files = get_all_py_files(SOURCE_DIR)
all_modules: dict[str, Path] = {}
for f in py_files:
    all_modules[extract_module_name(f, SOURCE_DIR)] = f

# mod -> list of imported project modules (exact names that exist in all_modules)
deps: dict[str, set[str]] = {}
for f in py_files:
    mod = extract_module_name(f, SOURCE_DIR)
    raw_imports = get_imports_from_file(f)
    deps[mod] = {i for i in raw_imports if i in all_modules}

# =====================================================================
# FAN-IN: exact module match only
# =====================================================================
fan_in_exact: dict[str, int] = defaultdict(int)
for source_mod, imported_set in deps.items():
    for imported_mod in imported_set:
        fan_in_exact[imported_mod] += 1

sorted_fi = sorted(fan_in_exact.items(), key=lambda x: -x[1])

print("=" * 72)
print("SADECE EXACT MODÜL EŞLEŞMESİ İLE FAN-IN (TOP 20)")
print("(kaç farklı dosya bu modülü DOĞRUDAN import ediyor)")
print("=" * 72)

print(f"\n{'#':>3} {'Modül Adı':55s} {'Fan-in':>7} {'Dosya':40s}")
print("-" * 107)
for rank, (mod, count) in enumerate(sorted_fi[:20], 1):
    f = all_modules.get(mod, Path(""))
    fname = str(f.relative_to(PROJECT_ROOT)) if f else ""
    print(f"{rank:3d} {mod:55s} {count:7d} {fname:40s}")

# =====================================================================
# DÖNGÜ TARAMASI
# =====================================================================
print("\n" + "=" * 72)
print("PROJE ÇAPINDA DÖNGÜSEL BAĞIMLILIK TARAMASI")
print("=" * 72)


def find_cycles(dep_graph: dict[str, set[str]]) -> list[list[str]]:
    visited: set[str] = set()
    in_stack: set[str] = set()
    path: list[str] = []
    cycles: list[list[str]] = []

    def _dfs(node: str) -> None:
        visited.add(node)
        in_stack.add(node)
        path.append(node)
        for neighbor in dep_graph.get(node, []):
            if neighbor not in visited:
                _dfs(neighbor)
            elif neighbor in in_stack:
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                if cycle not in cycles:
                    cycles.append(cycle)
        path.pop()
        in_stack.discard(node)

    for node in dep_graph:
        if node not in visited:
            _dfs(node)
    return cycles


cycles = find_cycles(deps)
if cycles:
    print(f"\n⚠️  {len(cycles)} adet döngü BULUNDU:")
    for i, c in enumerate(cycles, 1):
        print(f"  #{i}: {' → '.join(c)}")
        for m in c:
            f = all_modules.get(m)
            if f:
                print(f"      {f.relative_to(PROJECT_ROOT)}")
else:
    print("\n✅ Döngü bulunamadı — tüm bağımlılıklar DAG.")

# =====================================================================
# KRİTİK MODÜLLER — fan-in >= 5, leaf modüller (__init__ değil)
# =====================================================================
print("\n" + "=" * 72)
print("EN KRİTİK LEAF MODÜLLER (fan-in >= 3, __init__.py DEĞİL)")
print("=" * 72)

leaf_files = {mod for mod in all_modules if not mod.endswith(("__init__",)) or mod.count(".") >= 3}

print(f"\n{'#':>3} {'Modül Adı':55s} {'Fan-in':>7} {'Test Durumu':25s}")
print("-" * 92)
for rank, (mod, count) in enumerate(sorted_fi, 1):
    if count < 3 or mod.endswith(("__init__",)):
        continue
    # Test detection
    mod_name = mod.split(".")[-1]
    # Look for test file patterns
    test_found = False
    for parent in [PROJECT_ROOT / "tests", PROJECT_ROOT / "tests" / "core"]:
        candidates = [
            parent / f"test_{mod_name}.py",
            parent / f"test_{mod_name.replace('_', '')}.py",
        ]
        for p in parent.rglob("*.py"):
            if f"test_{mod_name}" in p.name:
                test_found = True
                break
        if test_found:
            break

    status = "✅ Test var" if test_found else "⚠️  Test YOK"

    # Check if previously verified
    verified = mod in [
        "intelgraph.core.metaintel.architecture",
    ]
    if verified:
        status = "✅ Doğrulandı"

    print(f"{rank:3d} {mod:55s} {count:7d} {status:25s}")

print("\n" + "=" * 72)
print("ÖNERİLEN DOĞRULAMA SIRASI")
print("(en yüksek fan-in → testsiz modüller öncelikli)")
print("=" * 72)

print(f"\n{'#':>3} {'Modül Adı':55s} {'Fan-in':>7} {'Öncelik':30s}")
print("-" * 97)
for rank, (mod, count) in enumerate(sorted_fi, 1):
    if count < 3 or mod.endswith(("__init__",)):
        continue
    has_test = any(
        f"test_{mod.split('.')[-1]}" in p.name for p in (PROJECT_ROOT / "tests").rglob("*.py")
    )
    if has_test:
        prio = "🔵 Düşük (test var)"
    else:
        prio = "🔴 YÜKSEK (testsiz!)"
    print(f"{rank:3d} {mod:55s} {count:7d} {prio:30s}")
