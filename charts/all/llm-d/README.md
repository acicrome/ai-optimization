# llm-d Helm chart

Packages only the two `LLMInferenceService` objects already versioned in `llm-d/examples/`.

Each entry under `models` controls enablement, namespace, model name/URI, replicas, HardwareProfile, Kueue queue label,
service account, image-pull Secrets, vLLM arguments, and resource requests/limits. `defaults.gateway` and
`defaults.hardwareProfileNamespace` configure the shared dependencies.

The chart does not create the `agent` namespace, gateway, model storage, service accounts, image-pull Secrets, llm-d API,
or GPU capacity. The source defaults intentionally retain those external references; customize them before deployment.
The Qwen queue label should be checked against the namespace of the deployed Kueue LocalQueue.
