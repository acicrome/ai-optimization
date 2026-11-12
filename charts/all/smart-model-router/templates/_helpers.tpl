{{- define "smart-model-router.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "smart-model-router.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- include "smart-model-router.name" . -}}
{{- end -}}
{{- end }}

{{- define "smart-model-router.labels" -}}
app: {{ include "smart-model-router.fullname" . }}
app.kubernetes.io/name: {{ include "smart-model-router.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/part-of: ai-optimization
{{- end }}
