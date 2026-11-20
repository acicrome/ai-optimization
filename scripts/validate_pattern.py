#!/usr/bin/env python3
"""Validate the Helm-based Validated Patterns integration."""
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

expected_charts = {
    "gpuaas",
    "gpuaas-monitoring",
    "llm-d",
    "observability",
    "rhoai-config",
    "smart-model-router",
}

expected_subscriptions = {
    "rhods-operator": {
        "namespace": "redhat-ods-operator",
        "source": "redhat-operators",
    },
    "kueue-operator": {
        "namespace": "openshift-kueue-operator",
        "source": "redhat-operators",
    },
}


# Parse repository YAML and JSON files.
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


# Validate Helm chart set and basic chart structure.
charts_root = ROOT / "charts" / "all"

actual_charts = (
    {p.name for p in charts_root.iterdir() if p.is_dir()}
    if charts_root.is_dir()
    else set()
)

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
        metadata = yaml.safe_load(
            (chart / "Chart.yaml").read_text(encoding="utf-8")
        )
        if metadata.get("apiVersion") != "v2" or metadata.get("name") != name:
            errors.append(f"invalid Chart.yaml identity for {name}")
    except Exception:
        pass


# Validate global pattern configuration.
try:
    global_values = yaml.safe_load(
        (ROOT / "values-global.yaml").read_text(encoding="utf-8")
    )

    if global_values.get("global", {}).get("pattern") != "ai-optimization":
        errors.append("global.pattern must be ai-optimization")

    if global_values.get("main", {}).get("variant") != "hub":
        errors.append("main.variant must be hub")

    if (
        global_values.get("global", {})
        .get("secretLoader", {})
        .get("disabled")
        is not True
    ):
        errors.append("secret loading must remain disabled")

except Exception as exc:  # noqa: BLE001
    errors.append(f"cannot validate values-global.yaml: {exc}")


# Validate ClusterGroup wiring.
try:
    group = yaml.safe_load(
        (ROOT / "variants/hub/values-hub.yaml").read_text(encoding="utf-8")
    )["clusterGroup"]

    applications = group.get("applications", {})

    if set(applications) != expected_charts:
        errors.append(f"application set mismatch: {sorted(applications)}")

    for name, app in applications.items():
        expected_path = f"charts/all/{name}"

        if app.get("path") != expected_path:
            errors.append(
                f"application {name} must reference {expected_path}"
            )

        if "kustomize" in app:
            errors.append(f"application {name} still declares Kustomize")

        if not (ROOT / expected_path / "Chart.yaml").is_file():
            errors.append(
                f"application {name} references a non-chart path"
            )

    # Validate required Operator subscriptions.
    subscriptions = group.get("subscriptions", [])

    actual_subscriptions = {
        subscription.get("name"): subscription
        for subscription in subscriptions
        if subscription.get("name")
    }

    for name, expected in expected_subscriptions.items():
        subscription = actual_subscriptions.get(name)

        if subscription is None:
            errors.append(f"required Operator subscription missing: {name}")
            continue

        if subscription.get("namespace") != expected["namespace"]:
            errors.append(
                f"subscription {name} must use namespace "
                f"{expected['namespace']}"
            )

        if subscription.get("source") != expected["source"]:
            errors.append(
                f"subscription {name} must use source "
                f"{expected['source']}"
            )

        if not subscription.get("channel"):
            errors.append(
                f"subscription {name} must define a channel"
            )

    unexpected_subscriptions = (
        set(actual_subscriptions) - set(expected_subscriptions)
    )

    if unexpected_subscriptions:
        errors.append(
            "unexpected Operator subscriptions: "
            f"{sorted(unexpected_subscriptions)}"
        )

except Exception as exc:  # noqa: BLE001
    errors.append(f"cannot validate values-hub.yaml: {exc}")


if (ROOT / "pattern-metadata.yaml").exists():
    errors.append(
        "pattern-metadata.yaml must not contain invented cluster sizing"
    )

if not ((ROOT / "pattern.sh").stat().st_mode & 0o111):
    errors.append("pattern.sh is not executable")


if errors:
    print("Validation failed:", file=sys.stderr)

    for error in errors:
        print(f" - {error}", file=sys.stderr)

    raise SystemExit(1)


print(
    "Validation successful: "
    "6 Helm charts and required Operator subscriptions "
    "wired to the Validated Pattern."
)
