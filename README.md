# AI Optimization Demo — Artifacts

This repository contains the Kubernetes/OpenShift manifests and configuration files for the **AI Optimization demo**, covering GPUaaS, AI workload management, model routing, and observability.

## Prerequisites

The following platform components are assumed to be already installed and operational:

- **OpenShift Container Platform (OCP)**.
- Required GPU infrastructure and platform components, where applicable.

The pattern manages the required **Red Hat OpenShift AI (RHOAI)** and **Red Hat build of Kueue** Operators through the Validated Patterns framework.

Operator channels are defined in `variants/hub/values-hub.yaml` and can be adapted according to the target environment and supported OpenShift version.

This repository focuses on project-specific resources and custom configurations, including the OpenShift AI configuration required by the solution.

## Repository Structure

| Directory | Description |
|---|---|
| `charts/all/rhoai-config/` | OpenShift AI configuration, including `DSCInitialization`, `DataScienceCluster`, and Models as a Service enablement. |
| `charts/all/gpuaas/` | GPUaaS manifests and Kueue configuration, including ResourceFlavors, queues, hardware profiles, and priority classes. |
| `charts/all/smart-model-router/` | Smart Model Router deployment manifests and configuration. |
| `charts/all/observability/` | Observability resources, including ServiceMonitors, PrometheusRules, and Grafana dashboard ConfigMaps. |
| `variants/hub/values-hub.yaml` | Validated Patterns configuration for namespaces, Operator subscriptions, and applications. |

## Configurations to Be Versioned

Project-specific configurations and custom resources must be maintained in this repository, including:

- **OpenShift AI:** configuration required by the pattern, including `DSCInitialization`, `DataScienceCluster`, and Models as a Service enablement.
- **GPUaaS and Kueue:** queues, ResourceFlavors, hardware profiles, priority classes, and related resources.
- **MaaS and model management:** custom manifests and configuration required by the solution, including integrations and policies where applicable.
- **Smart Model Router:** application configuration, Deployment, Service, and Route.
- **Observability:** Grafana dashboards, monitoring rules, and related configuration resources.
- **Validated Patterns integration:** namespaces, Operator subscriptions, and applications declared in `variants/hub/values-hub.yaml`.

Environment-specific values should be adapted through configuration rather than hardcoded in the Helm templates.

## Security

- Do not commit passwords, access tokens, private keys, MaaS API keys, or other secrets in plaintext.
- Manage credentials through Kubernetes/OpenShift Secrets or dedicated secret-management solutions.
- Avoid hardcoding environment-specific hostnames, addresses, and parameters when these can be managed through environment-specific configuration.

## Validation and Deployment

Validate the Helm charts and the Validated Patterns configuration before deployment and verify that the required infrastructure components are available in the target environment.

The pattern is deployed through the Validated Patterns framework. Required namespaces and Operator subscriptions are declared in `variants/hub/values-hub.yaml`, while the project-specific resources are managed through the Helm charts under `charts/all/`.

Once the pattern is installed, Argo CD manages and reconciles the desired state defined in the configured Git branch.
