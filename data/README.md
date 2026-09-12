# Data

One JSONL file per dataset, one record per observation. Proposed schema (to be agreed by the team):

| field | type | description |
|---|---|---|
| `text` | str | The observation as the model sees it. This is the window the probe is computed over. |
| `source_channel` | str | Where the observation came from in the transcript: `user`, `tool_output`, `system`, `subagent`, `file_read`, `http_response`, ... |
| `label` | int | 1 if the observation was written by another agent or is addressed to the model as an agent, 0 otherwise. By construction in the synthetic set. |
| `split` | str | `train`, `val`, `test`, or the name of the out-of-distribution set: `collusion_wiki`, `metr_dirnames`, `subagent_legit`, `moltbook`. |
| `origin` | str | Where the record came from: `synthetic`, `collusion_wiki`, `metr_report`, `inspect_transcript`, `claude_code`, `moltbook`, ... |

Optional fields: `source_class` (str, the fine-grained class in the synthetic set: `human_user`, `tool_output`, `system`, `agent_explicit`, `agent_covert`), `context` (str, the transcript preceding the observation, if used), `belief_label` (int, the model's answer to "who wrote this?", to separate format from interpretation), `meta` (dict).

JSONL files are tracked in git unless they get large. Activations go in `activations/` (git-ignored) as `.npy` or `.safetensors`.

Every citation of the incident record carries its source. For METR, the line number in [`context/metr-report-2026-08.txt`](../context/metr-report-2026-08.txt).
