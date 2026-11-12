#!/usr/bin/env bash
set -euo pipefail

is_available() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "$1 is required but is not installed. Aborting." >&2
    exit 1
  }
}

PATTERN_UTILITY_CONTAINER="${PATTERN_UTILITY_CONTAINER:-quay.io/validatedpatterns/utility-container}"
is_available podman

if [[ -n "${KUBECONFIG:-}" && "${KUBECONFIG}" != "$HOME"* ]]; then
  echo "KUBECONFIG must be below HOME so it can be mounted into the utility container." >&2
  exit 1
fi

pki_args=()
if [[ -d /etc/pki/tls ]]; then
  pki_args=(-v /etc/pki:/etc/pki:ro)
elif [[ -d /etc/ssl ]]; then
  pki_args=(-v /etc/ssl:/etc/ssl:ro)
fi

podman run -it --rm --pull=newer \
  --security-opt label=disable \
  -e ANSIBLE_STDOUT_CALLBACK \
  -e DISABLE_VALIDATE_ORIGIN \
  -e EXTRA_HELM_OPTS \
  -e EXTRA_PLAYBOOK_OPTS \
  -e K8S_AUTH_HOST \
  -e K8S_AUTH_PASSWORD \
  -e K8S_AUTH_SSL_CA_CERT \
  -e K8S_AUTH_TOKEN \
  -e K8S_AUTH_USERNAME \
  -e K8S_AUTH_VERIFY_SSL \
  -e KUBECONFIG \
  -e PATTERN_DISCONNECTED_HOME \
  -e PATTERN_INSTALL_CHART \
  -e TARGET_BRANCH \
  -e TARGET_ORIGIN \
  "${pki_args[@]}" \
  -v "$(pwd -P):$(pwd -P)" \
  -v "${HOME}:${HOME}" \
  -v "${HOME}:/pattern-home" \
  -w "$(pwd -P)" \
  "$PATTERN_UTILITY_CONTAINER" \
  "$@"
