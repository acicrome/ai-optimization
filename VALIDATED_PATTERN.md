# Red Hat Validated Patterns integration

This layer turns the verified repository content into a Validated Patterns GitOps repository without installing or
inventing platform components. The source baseline is commit `ea72908c3da8ec18d9f86907b42f23155c1ebd70` from the
reconstructed backup. `SOURCE_BASELINE.sha256` protects all 64 files tracked by that commit.

## Applications mapped from the source

| Argo CD application | Source path | Existing content |
|---|---|---|
| `gpuaas` | `gpuaas/` | Namespaces, Kueue ResourceFlavors, queues, cohort, priorities and OpenShift AI HardwareProfiles |
| `gpuaas-monitoring` | `gpuaas/monitoring/` | Existing monitoring ConfigMap, RoleBinding, ServiceMonitor and Kueue dashboard JSON |
| `llm-d` | `llm-d/` | The two existing `LLMInferenceService` examples |
| `observability` | `observability/` | Existing dashboards, ServiceMonitors and NVIDIA GPU Operator PrometheusRule |
| `smart-model-router` | `smart-model-router-validated-pattern/manifests/` | Existing router Namespace, ConfigMaps, Deployment, Service and Route |

The only Kustomize files added inside source component directories are entry points for content that had manifests but no
root `kustomization.yaml`: `llm-d/kustomization.yaml` and `gpuaas/monitoring/kustomization.yaml`.

`training/` and `benchmarking/` are preserved but are not Argo CD applications: the verified baseline contains a training
notebook and documentation, not Kubernetes deployable resources.

## Deliberately not installed

The pattern declares no Operator subscriptions. It does not install OpenShift, OpenShift AI, Kueue, llm-d APIs, the
NVIDIA GPU Operator, Prometheus Operator, Grafana, model storage, gateways, service accounts, image-pull credentials, or
MaaS. Those are prerequisites explicitly documented by the original repository.

## Secret boundary

Secret loading is disabled. The original Smart Model Router requires a `smart-router-maas-credentials` Secret to be
created out-of-band in `smart-model-router`; its `secret-example.yaml` remains excluded from the original Kustomization.
Do not commit the MaaS API key.

## Environment review before installation

The original manifests contain concrete example values: namespaces, GPU quantities, HardwareProfile names, queue names,
model URIs, gateway references, service accounts, Route exposure and metrics selectors. Review those existing values
before enabling automatic reconciliation against a cluster.

In particular:

- `gpuaas/monitoring/enableMonitoring.yaml` changes the cluster-wide OpenShift monitoring ConfigMap. It is a separate
  Argo CD application so it can be reviewed and disabled independently in `variants/hub/values-hub.yaml`.
- the Qwen `LLMInferenceService` is in namespace `agent`, while the versioned `team-inference` LocalQueue is in namespace
  `team-inference`; confirm or correct that queue binding for the target Kueue configuration before sync.
- the GPT-OSS example references the `gpu` HardwareProfile and image-pull Secret, while this repository versions only the
  `highpriority` and `lowpriority` HardwareProfiles; provide the referenced prerequisites externally or customize the
  example.
- the Smart Model Router uses placeholder MaaS and classifier endpoints from `router-config.env`; replace them with values
  valid for the target environment without committing credentials.

## Validation

```bash
make validate
```

This verifies original-file checksums, parses YAML and JSON, checks every Kustomization reference, verifies that all
Validated Patterns application paths exist, and confirms that no Operator subscriptions were added. When `kubectl` or
`oc` is available, it also renders all five Kustomize applications.

## Installation

1. Review and customize the original environment-specific manifests.
2. Create the required Smart Model Router Secret out-of-band.
3. Commit and push the pattern files to a branch reachable by OpenShift GitOps.
4. Log in to the target OpenShift cluster.
5. Run:

```bash
export TARGET_BRANCH=<published-branch>
./pattern.sh make install
```

Override `TARGET_ORIGIN` if the cluster must read a fork or a different Git URL.

## Publication metadata

`pattern-metadata.yaml` is intentionally not fabricated. Validated Patterns catalog metadata requires tested cluster
sizing and publication links, but the source repository contains no validated worker/control-plane sizing. Add metadata
only after the integrated pattern has been tested on a documented cluster configuration.
