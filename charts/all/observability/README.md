# observability Helm chart

Packages the six JSON dashboards, three ServiceMonitors, and NVIDIA GPU Operator PrometheusRule already present in the
repository. It does not install Grafana, Prometheus, the Prometheus Operator, OpenShift monitoring, or the NVIDIA GPU
Operator.

Configuration:

- `dashboards.namespace`, `labels`, and `items` control generated dashboard ConfigMaps;
- `serviceMonitors[]` controls each namespace, labels, selector, namespace selector, endpoint, and enablement;
- `prometheusRule` controls enablement, namespace, labels, name, and the source rule file.

Verify target namespaces, metrics service labels/ports, metric names, dashboard datasource configuration, and monitoring
permissions before sync. Disable resources whose backing workload or Operator is absent.
