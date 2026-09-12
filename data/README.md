# Datos

Un archivo JSONL por dataset, un registro por observación. Esquema propuesto (ajustar entre todos):

| campo | tipo | descripción |
|---|---|---|
| `text` | str | La observación tal como la ve el modelo. Es la ventana sobre la que se calcula el probe. |
| `source_channel` | str | Origen de la observación en el transcript: `user`, `tool_output`, `system`, `subagent`, `file_read`, `http_response`, ... |
| `label` | int | 1 si la observación la escribió otro agente o está dirigida al modelo como agente, 0 si no. Por construcción en el set sintético. |
| `split` | str | `train`, `val`, `test`, o el nombre del set fuera de distribución: `collusion_wiki`, `metr_dirnames`, `subagent_legit`, `moltbook`. |
| `origin` | str | De dónde salió el registro: `synthetic`, `collusion_wiki`, `metr_report`, `inspect_transcript`, `claude_code`, `moltbook`, ... |

Campos opcionales: `source_class` (str, la clase fina del set sintético: `human_user`, `tool_output`, `system`, `agent_explicit`, `agent_covert`), `context` (str, transcript previo a la observación si se usa), `belief_label` (int, respuesta del modelo a "¿quién escribió esto?", para separar formato de interpretación), `meta` (dict).

Los JSONL van en git salvo que pesen. Las activaciones van en `activations/` (ignorado por git), en `.npy` o `.safetensors`.

Toda cita al registro del incidente lleva fuente. Si es METR, número de línea de [`context/metr-report-2026-08.txt`](../context/metr-report-2026-08.txt).
