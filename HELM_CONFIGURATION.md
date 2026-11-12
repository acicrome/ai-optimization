# Helm configuration reference

The defaults reproduce the substantive settings of the verified manifests. Environment-specific changes belong in
separate values files or controlled Git commits; never place credentials in values.

## `charts/all/gpuaas`

- `namespaces[]`: tenant namespace names and labels.
- `resourceFlavors[]`: Kueue ResourceFlavor names, node labels, and tolerations.
- `cohort`: shared Kueue cohort enablement/name.
- `priorityClasses[]`: workload priority names, values, and descriptions.
- `clusterQueues[]`: namespace selectors, preemption, strategy, cohort, CPU/memory/GPU quotas, and borrowing limits.
- `localQueues[]`: LocalQueue namespace and ClusterQueue binding.
- `hardwareProfiles.namespace`: OpenShift AI HardwareProfile namespace.
- `hardwareProfiles.items[]`: profile display names, resource ranges, queue, and priority.

## `charts/all/gpuaas-monitoring`

- `clusterMonitoring`: cluster-wide user-workload monitoring configuration; disable if managed elsewhere.
- `roleBinding`: Prometheus service account and cluster-role binding.
- `serviceMonitor`: Kueue selector, endpoint, interval, scheme, token file, and TLS behavior.
- `dashboard`: dashboard ConfigMap name, namespace, labels, and data key.

## `charts/all/llm-d`

- `defaults.gateway`: MaaS/llm-d Gateway API reference.
- `defaults.hardwareProfileNamespace`: namespace containing OpenShift AI HardwareProfiles.
- `models.<model>.enabled`: independently enable the two source models.
- Per model: namespace, URI, replicas, profile, queue, service account, pull Secrets, vLLM arguments, and resources.

## `charts/all/observability`

- `dashboards`: enablement, target namespace, labels, names, keys, and packaged JSON files.
- `serviceMonitors[]`: independent enablement, namespaces, labels, selectors, namespace selectors, and endpoints.
- `prometheusRule`: enablement, name, namespace, labels, and packaged source rule spec.

## `charts/all/smart-model-router`

- `namespace`: create/name/labels.
- `replicaCount`, `image`, `resources`, `podAnnotations`, and `podLabels`.
- `service` and `route`: HTTP port, hostname, and TLS termination.
- `maas`: URL, TLS verification, and external Secret name/key.
- `models`: simple/complex model identifiers.
- `classifier`: endpoint, model, and timeout.
- `requestTimeoutSeconds` and probe timings.

## Example validation

```bash
helm lint charts/all/gpuaas --strict
helm template gpuaas charts/all/gpuaas --namespace team-inference
scripts/validate-helm.sh
```

To test an environment override without changing defaults:

```bash
helm template llm-d charts/all/llm-d \
  --namespace agent \
  --values /path/to/environment-values.yaml
```
