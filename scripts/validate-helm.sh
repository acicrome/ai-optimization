#!/usr/bin/env bash
set -euo pipefail

command -v helm >/dev/null 2>&1 || {
  echo "ERROR: helm is required for lint and template validation." >&2
  exit 1
}

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
rendered="${root}/dist/rendered"
rm -rf "$rendered"
mkdir -p "$rendered"

for chart in "$root"/charts/all/*; do
  name="$(basename "$chart")"
  echo "==> helm lint ${name}"
  helm lint "$chart" --strict
  echo "==> helm template ${name}"
  helm template "$name" "$chart" \
    --namespace "$name" \
    --include-crds \
    > "$rendered/${name}.yaml"
done

echo "Helm validation completed. Rendered manifests: $rendered"
