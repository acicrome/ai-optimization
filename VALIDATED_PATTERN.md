# Helm-based Red Hat Validated Patterns integration

This repository layer targets `https://github.com/acicrome/ai-optimization.git`, branch `validated-pattern`. It converts
only the five deployable source components into parameterized Helm charts while preserving the verified source baseline.

## Source fidelity

`SOURCE_BASELINE.sha256` contains the SHA-256 checksum of every one of the 64 files from the verified source commit
`ea72908c3da8ec18d9f86907b42f23155c1ebd70`. Run `make source-check` to prove that the original files have not changed.
The original Kustomize files remain as historical/source artifacts, but the Validated Patterns bill of materials no
longer references them.

## Helm applications

| Application | Helm chart | Source represented |
|---|---|---|
| `gpuaas` | `charts/all/gpuaas` | Namespaces, Kueue flavors/queues/cohort/priorities, and OpenShift AI HardwareProfiles |
| `gpuaas-monitoring` | `charts/all/gpuaas-monitoring` | Cluster monitoring configuration, RBAC, Kueue ServiceMonitor, and dashboard |
| `llm-d` | `charts/all/llm-d` | GPT-OSS-20B and Qwen3-32B `LLMInferenceService` resources |
| `observability` | `charts/all/observability` | Six dashboards, three ServiceMonitors, and NVIDIA GPU Operator alert rules |
| `smart-model-router` | `charts/all/smart-model-router` | Router code/UI, settings, Deployment, Service, Namespace, and Route |

`training/` and `benchmarking/` remain baseline artifacts. They do not contain Kubernetes deployment resources and are
not represented as Argo CD applications.

## Platform boundary

No Operator subscriptions are declared. The pattern assumes the platform capabilities documented by the original
repository are already installed and compatible: OpenShift AI, Kueue APIs, llm-d/KServe API, GPU support, Prometheus
Operator CRDs, OpenShift monitoring, and any required gateway/model-storage facilities.

The Smart Model Router API key remains an out-of-band Secret. No populated Secret is rendered by a chart.

## Validation

```bash
make validate-static   # checksum, YAML/JSON, chart structure, and VP wiring
make helm-validate     # strict helm lint plus helm template for every chart
make validate          # all checks
```

Rendered manifests are written to `dist/rendered/`. CI runs the same commands with Helm 3.16.4 on pushes and pull
requests to `validated-pattern` and `main`.

## Installation

After reviewing the chart values and satisfying the prerequisites:

```bash
export TARGET_ORIGIN=https://github.com/acicrome/ai-optimization.git
export TARGET_BRANCH=validated-pattern
./pattern.sh make install
```

Before Smart Model Router reconciliation, create its required Secret outside Git:

```bash
oc create secret generic smart-router-maas-credentials \
  --namespace smart-model-router \
  --from-literal=MAAS_API_KEY='<api-key>'
```

## Important source-derived checks

- Review the cluster-wide update rendered by `gpuaas-monitoring.clusterMonitoring`.
- Match Kueue quotas, GPU labels, queue namespaces, and HardwareProfiles to real capacity.
- Confirm the Qwen queue is available to the `agent` namespace or change the chart values.
- Provide the GPT-OSS image-pull Secret and referenced `gpu` HardwareProfile, or customize those values.
- Replace Smart Model Router placeholder endpoints and model identifiers.
- Disable observability objects whose target workloads, namespaces, or metrics services do not exist.

Catalog `pattern-metadata.yaml` remains intentionally absent because the source repository does not provide a tested
control-plane/worker sizing baseline suitable for publication metadata.
