#!/usr/bin/env python3
"""Validate source fidelity and the Validated Patterns integration."""
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

expected_top_level_source = {
    "README.md",
    "benchmarking",
    "gpuaas",
    "llm-d",
    "observability",
    "smart-model-router-validated-pattern",
    "training",
}
required_framework = {
    "values-global.yaml",
    "variants/hub/values-hub.yaml",
    "pattern.sh",
    "Makefile",
    "Makefile-common",
    "ansible.cfg",
    "SOURCE_BASELINE.sha256",
    "VALIDATED_PATTERN.md",
    "llm-d/kustomization.yaml",
    "gpuaas/monitoring/kustomization.yaml",
}
expected_apps = {
    "gpuaas": "gpuaas",
    "gpuaas-monitoring": "gpuaas/monitoring",
    "llm-d": "llm-d",
    "observability": "observability",
    "smart-model-router": "smart-model-router-validated-pattern/manifests",
}

for item in expected_top_level_source:
    if not (ROOT / item).exists():
        errors.append(f"missing verified source item: {item}")
for item in required_framework:
    if not (ROOT / item).is_file():
        errors.append(f"missing framework file: {item}")

# Parse all YAML except values-example.yaml, which is a plain application values
# document but still valid YAML. Kustomization files are included in the same pass.
for path in sorted(ROOT.rglob("*.yaml")):
    try:
        list(yaml.safe_load_all(path.read_text(encoding="utf-8")))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"invalid YAML {path.relative_to(ROOT)}: {exc}")

for path in sorted(ROOT.rglob("*.json")):
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")

try:
    global_values = yaml.safe_load((ROOT / "values-global.yaml").read_text(encoding="utf-8"))
    if global_values.get("global", {}).get("pattern") != "ai-optimization":
        errors.append("values-global.yaml: global.pattern must be ai-optimization")
    if global_values.get("main", {}).get("variant") != "hub":
        errors.append("values-global.yaml: main.variant must be hub")
    if global_values.get("global", {}).get("secretLoader", {}).get("disabled") is not True:
        errors.append("values-global.yaml: secret loader must remain disabled")
except Exception as exc:  # noqa: BLE001
    errors.append(f"cannot validate values-global.yaml: {exc}")

try:
    hub = yaml.safe_load((ROOT / "variants/hub/values-hub.yaml").read_text(encoding="utf-8"))
    group = hub.get("clusterGroup", {})
    if "subscriptions" in group:
        errors.append("the clusterGroup must not introduce Operator subscriptions")
    actual_apps = group.get("applications", {})
    if set(actual_apps) != set(expected_apps):
        errors.append(f"application set differs from source mapping: {sorted(actual_apps)}")
    for name, relative in expected_apps.items():
        app = actual_apps.get(name, {})
        if app.get("path") != relative:
            errors.append(f"application {name} must reference {relative}")
        if app.get("kustomize") is not True:
            errors.append(f"application {name} must be marked as Kustomize")
        if not (ROOT / relative / "kustomization.yaml").is_file():
            errors.append(f"application {name} has no Kustomization at {relative}")
except Exception as exc:  # noqa: BLE001
    errors.append(f"cannot validate values-hub.yaml: {exc}")

# Verify local Kustomize resource and generator references without requiring a
# cluster or network access.
for kustomization in sorted(ROOT.rglob("kustomization.yaml")):
    try:
        data = yaml.safe_load(kustomization.read_text(encoding="utf-8")) or {}
    except Exception:
        continue
    base = kustomization.parent
    for value in data.get("resources", []) or []:
        target = base / str(value)
        if not target.exists():
            errors.append(f"{kustomization.relative_to(ROOT)} references missing resource {value}")
        elif target.is_dir() and not (target / "kustomization.yaml").is_file():
            errors.append(f"{kustomization.relative_to(ROOT)} references directory without kustomization: {value}")
    for generator in data.get("configMapGenerator", []) or []:
        for key in ("files", "envs"):
            for value in generator.get(key, []) or []:
                source = str(value).split("=", 1)[-1]
                if not (base / source).is_file():
                    errors.append(f"{kustomization.relative_to(ROOT)} references missing generator input {source}")

if (ROOT / "pattern-metadata.yaml").exists():
    errors.append("pattern-metadata.yaml must not contain invented cluster sizing")
if (ROOT / "charts").exists():
    errors.append("no new Helm charts are expected; source applications are Kustomize-based")
if not ((ROOT / "pattern.sh").stat().st_mode & 0o111):
    errors.append("pattern.sh is not executable")

if errors:
    print("Validation failed:", file=sys.stderr)
    for error in errors:
        print(f" - {error}", file=sys.stderr)
    raise SystemExit(1)

print("Validation successful: 64 source files preserved and 5 source-backed Kustomize applications wired.")
