# gpuaas Helm chart

Packages the repository's existing GPUaaS namespaces, Kueue ResourceFlavors, Cohort, ClusterQueues, LocalQueues,
WorkloadPriorityClasses, and OpenShift AI HardwareProfiles. It does not install Kueue, OpenShift AI, the NVIDIA GPU
Operator, GPU drivers, or nodes.

Key values:

- `namespaces[]`: tenant namespaces and labels;
- `resourceFlavors[]`: Kueue flavors, GPU node labels, and tolerations;
- `clusterQueues[]`: quotas, borrowing, cohort, namespace selector, and preemption;
- `localQueues[]`: namespace-to-ClusterQueue bindings;
- `priorityClasses[]`: inference and training priorities;
- `hardwareProfiles`: OpenShift AI profile namespace, resource ranges, queues, and priorities.

Every value is initialized from the verified source manifests. Confirm CRD versions, actual GPU capacity, labels, quotas,
and namespaces before deployment.
