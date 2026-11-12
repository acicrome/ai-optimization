{{- define "gpuaas.labels" -}}
app.kubernetes.io/name: gpuaas
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/part-of: ai-optimization
{{- end }}
