# Validation report

## Completed in the build environment

- Verified all 64 original source files against `SOURCE_BASELINE.sha256`.
- Parsed all non-template YAML and JSON files.
- Verified five `apiVersion: v2` charts with matching names, values, templates, and documentation.
- Verified the five Validated Patterns applications reference `charts/all/<name>` and contain no Kustomize mode.
- Verified no Operator subscriptions were introduced.
- Verified packaged dashboard, Python, and HTML assets match the original source bytes.
- Checked Helm template delimiter/block balance and all named-template references.
- Checked Bash and Python syntax and the training notebook JSON.
- Scanned the package for excluded autoscaler resource names; none were found.

## Helm-native validation

The repository includes `scripts/validate-helm.sh`, which runs for every chart:

```bash
helm lint <chart> --strict
helm template <release> <chart> --include-crds
```

`make validate` invokes this script after source/static validation. The GitHub Actions workflow installs Helm 3.16.4 and
runs `make validate` on pushes and pull requests to `validated-pattern` and `main`, uploading all rendered manifests.

The sandbox used to assemble this package had no Helm binary and no outbound DNS access, so the Helm-native stage could
not be executed locally. It is deliberately mandatory rather than silently skipped: run `make validate` before merging
the package into the branch, or use the included CI workflow.
