# AI Optimization — Validated Pattern

This repository contains the Helm charts, Kubernetes/OpenShift resources, and configuration files for the **AI Optimization Validated Pattern**, covering GPU as a Service (GPUaaS), AI workload management, Models as a Service (MaaS), intelligent model routing, distributed inference, and observability.

## Prerequisites

The following infrastructure is assumed to be available before deploying the pattern:

- **Red Hat OpenShift Container Platform (OCP)**.
- GPU-capable worker nodes with the required GPU drivers and device enablement.
- Access to the required Red Hat Operator catalogs and container registries.
- Cluster administrator access.
- Required subscriptions and entitlements.
- LLM model artifacts and environment-specific credentials.

The pattern manages the required **Red Hat OpenShift AI** and **Red Hat build of Kueue** Operators through the Validated Patterns framework.

The Operator channels defined in `variants/hub/values-hub.yaml` are default values and can be adapted to the target environment after verifying compatibility.

## Repository Structure

| Directory | Description |
|---|---|
| `variants/hub/values-hub.yaml` | ClusterGroup configuration defining managed namespaces, required Operator subscriptions, and Argo CD applications. |
| `charts/all/rhoai-config/` | Red Hat OpenShift AI configuration, including `DSCInitialization`, `DataScienceCluster`, and Models as a Service enablement. |
| `charts/all/gpuaas/` | GPUaaS and Kueue configuration, including ResourceFlavors, Cohort, ClusterQueues, LocalQueues, HardwareProfiles, quotas, and priority classes. |
| `charts/all/gpuaas-monitoring/` | Kueue monitoring resources, including ServiceMonitor, RBAC, and Grafana dashboard configuration. |
| `charts/all/llm-d/` | Parameterized `LLMInferenceService` resources for distributed model serving. |
| `charts/all/smart-model-router/` | Smart Model Router application, configuration, Deployment, Service, and Route. |
| `charts/all/observability/` | Observability resources, including ServiceMonitors, PrometheusRules, and Grafana dashboards. |
| `training/` | Distributed fine-tuning example using OpenShift AI, Kubeflow Trainer, and Kueue. |
| `benchmarking/` | Documentation for inference benchmarking and model evaluation. |
| `docs/` | Validated Pattern documentation and related images. |

## Configurations to Be Versioned

Project-specific configurations and custom resources must be maintained in this repository, including:

- **Validated Patterns configuration:** namespaces, Operator subscriptions, and Argo CD applications defined in `variants/hub/values-hub.yaml`.
- **OpenShift AI:** `DSCInitialization`, `DataScienceCluster`, and Models as a Service enablement.
- **GPUaaS and Kueue:** queues, ResourceFlavors, Cohort, HardwareProfiles, priority classes, quotas, and borrowing configuration.
- **Model serving:** llm-d and parameterized `LLMInferenceService` configuration.
- **MaaS and model management:** configuration and integrations required by the solution.
- **Smart Model Router:** application configuration, Deployment, Service, Route, and model endpoints.
- **Observability:** Grafana dashboards, monitoring rules, ServiceMonitors, and related configuration resources.

The Red Hat OpenShift AI and Red Hat build of Kueue Operators are declared as subscriptions in `variants/hub/values-hub.yaml`.

The `rhoai-config` application configures the OpenShift AI components required by the pattern. Models as a Service is enabled through the OpenShift AI `DataScienceCluster`.

Kueue remains unmanaged by the OpenShift AI `DataScienceCluster` because the Red Hat build of Kueue Operator is installed separately through the pattern.

Environment-specific settings should be managed through values files or controlled Git changes rather than hardcoded into Helm templates.

## Environment-specific Configuration

The repository provides default values based on the validated reference configuration. These values are not fixed infrastructure or software-version requirements.

Depending on the target environment, review and adapt:

- OpenShift AI and Kueue Operator channels.
- GPU node labels and tolerations.
- GPU type and HardwareProfile values.
- GPU quotas and borrowing limits.
- Team namespaces and queues.
- Model URIs and identifiers.
- Number of GPUs per model replica.
- vLLM and llm-d parameters.
- MaaS endpoint configuration.
- Smart Model Router model endpoints.
- Monitoring configuration.

The default HardwareProfile uses the generic accelerator configuration:

```yaml
displayName: NVIDIA GPU
identifier: nvidia.com/gpu


