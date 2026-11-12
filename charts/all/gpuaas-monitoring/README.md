# gpuaas-monitoring Helm chart

Packages the monitoring resources under the original `gpuaas/monitoring/` directory. Values parameterize the
cluster-monitoring ConfigMap, RBAC subject, ServiceMonitor endpoint/selector, and dashboard namespace/labels.

`clusterMonitoring.enabled=true` updates `openshift-monitoring/cluster-monitoring-config` and therefore has cluster-wide
impact. Review existing ConfigMap ownership before installation. The source ServiceMonitor defaults to
`tls.insecureSkipVerify=true`; configure trusted certificate verification where possible.
