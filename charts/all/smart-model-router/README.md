# smart-model-router Helm chart

Packages the existing Python/HTML router application with its Namespace, settings/code ConfigMaps, Deployment, Service,
and OpenShift Route. The source files are embedded from `files/` at render time.

Values parameterize image, replicas, namespace, service/Route, MaaS URL and TLS verification, model identifiers,
classifier endpoint/model/timeouts, probes, pod metadata, resources, and the external Secret reference.

The chart deliberately does not create `smart-router-maas-credentials`. Create that Secret out-of-band in the configured
namespace. Replace the placeholder MaaS and classifier URLs and retain TLS verification wherever possible.
