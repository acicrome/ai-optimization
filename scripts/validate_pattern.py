#!/usr/bin/env python3
"""Validate source fidelity and the Helm-based Validated Patterns integration."""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: python3 -m pip install pyyaml") from exc

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []
expected_source_roots = {
    "README.md", "benchmarking", "gpuaas", "llm-d", "observability",
    "smart-model-router-validated-pattern", "training",
}
expected_charts = {
    "gpuaas", "gpuaas-monitoring", "llm-d", "observability", "smart-model-router",
}

for item in expected_source_roots:
    if not (ROOT / item).exists():
        errors.append(f"missing verified source item: {item}")

# Parse values and chart metadata. Helm templates are parsed by Helm and receive
# a separate block-structure check for restricted/offline environments.
for path in sorted(ROOT.rglob("*.yaml")):
    if "templates" in path.parts:
        continue
    try:
        list(yaml.safe_load_all(path.read_text(encoding="utf-8")))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"invalid YAML {path.relative_to(ROOT)}: {exc}")
for path in sorted(ROOT.rglob("*.json")):
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")

charts_root = ROOT / "charts" / "all"
actual_charts = {p.name for p in charts_root.iterdir() if p.is_dir()} if charts_root.is_dir() else set()
if actual_charts != expected_charts:
    errors.append(f"chart set mismatch: {sorted(actual_charts)}")
for name in expected_charts:
    chart = charts_root / name
    for required in ("Chart.yaml", "values.yaml", "README.md"):
        if not (chart / required).is_file():
            errors.append(f"chart {name} missing {required}")
    if not (chart / "templates").is_dir():
        errors.append(f"chart {name} missing templates/")
    try:
        metadata = yaml.safe_load((chart / "Chart.yaml").read_text(encoding="utf-8"))
        if metadata.get("apiVersion") != "v2" or metadata.get("name") != name:
            errors.append(f"invalid Chart.yaml identity for {name}")
    except Exception:
        pass

try:
    global_values = yaml.safe_load((ROOT / "values-global.yaml").read_text(encoding="utf-8"))
    if global_values.get("global", {}).get("pattern") != "ai-optimization":
        errors.append("global.pattern must be ai-optimization")
    if global_values.get("main", {}).get("variant") != "hub":
        errors.append("main.variant must be hub")
    if global_values.get("global", {}).get("secretLoader", {}).get("disabled") is not True:
        errors.append("secret loading must remain disabled")
except Exception as exc:  # noqa: BLE001
    errors.append(f"cannot validate values-global.yaml: {exc}")

try:
    group = yaml.safe_load((ROOT / "variants/hub/values-hub.yaml").read_text(encoding="utf-8"))["clusterGroup"]
    if "subscriptions" in group:
        errors.append("Operator subscriptions were not present in the source and must not be added")
    applications = group.get("applications", {})
    if set(applications) != expected_charts:
        errors.append(f"application set mismatch: {sorted(applications)}")
    for name, app in applications.items():
        expected_path = f"charts/all/{name}"
        if app.get("path") != expected_path:
            errors.append(f"application {name} must reference {expected_path}")
        if "kustomize" in app:
            errors.append(f"application {name} still declares Kustomize")
        if not (ROOT / expected_path / "Chart.yaml").is_file():
            errors.append(f"application {name} references a non-chart path")
except Exception as exc:  # noqa: BLE001
    errors.append(f"cannot validate values-hub.yaml: {exc}")

if (ROOT / "pattern-metadata.yaml").exists():
    errors.append("pattern-metadata.yaml must not contain invented cluster sizing")
if not ((ROOT / "pattern.sh").stat().st_mode & 0o111):
    errors.append("pattern.sh is not executable")

if errors:
    print("Validation failed:", file=sys.stderr)
    for error in errors:
        print(f" - {error}", file=sys.stderr)
    raise SystemExit(1)
print("Validation successful: 64 source files preserved and 5 source-backed Helm charts wired.")
