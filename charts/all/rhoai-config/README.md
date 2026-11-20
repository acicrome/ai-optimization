# rhoai-config

This Helm chart configures the Red Hat OpenShift AI components required by the AI Optimization Validated Pattern.

It manages:

- DSCInitialization
- DataScienceCluster
- Models as a Service enablement
- OpenShift AI dashboard
- training components
- workbenches

Kueue remains unmanaged by the DataScienceCluster because the Red Hat build of Kueue Operator is installed separately through the Validated Patterns framework.

The chart does not manage GPU drivers, GPU hardware, model artifacts, credentials, or environment-specific secrets.
