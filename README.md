# Probing for Unexpected Agent2Agent Interactions

A linear probe on model activations plus an I/O monitor to detect unexpected agent-to-agent interactions in agentic transcripts.

Project by the BAISH (Buenos Aires AI Safety Hub) team for the [AI Incident Response Sprint](https://apartresearch.com/sprints/ai-incident-response-sprint-2026-09-11-to-2026-09-13) by Apart Research and CeSIA (September 11 to 13, 2026), open track, on the OpenAI / Hugging Face incident of July 2026. It started as project #6 on the BAISWARM forum; the original post (in Spanish) is in [`context/`](context/).

## The idea

1. **Interlocutor probe.** A linear probe on the residual stream of an open-weight model that fires when the model believes what it just read was written by another agent, or is addressed to it as an agent. Same method as evaluation-awareness probes.
2. **Channel.** Every observation in a transcript has a known origin: sub-agent, tool, user, file, HTTP. A high probe score on a channel where agents are expected means nothing. A high probe score on an unexpected channel is the signal.
3. **I/O monitor.** An LLM that looks only at the flagged windows and decides whether the model is treating that content as an instruction or coordinating with another agent.

The pitch is "cheap and orthogonal to task content", never "unbreakable". Full context (incident record, evaluation plan, compute, limits to declare, bibliography) is in [`CLAUDE.md`](CLAUDE.md).

## Layout

```
context/      sources: BAISWARM post, text of the METR report (citable by line number)
data/         JSONL datasets, one record per observation (schema in data/README.md)
src/          `a2a_probe` package: activation extraction, probes, cascade
eval/         evaluation scripts and figures
results/      probe weights, metrics, final figures (small, tracked in git)
report/       LaTeX report on the Apart template
activations/  activations as .npy / .safetensors (git-ignored)
```

## Setup

### Python

Requires [uv](https://docs.astral.sh/uv/). Pick the extra that matches your machine:

```bash
uv sync --extra cpu     # laptop without a GPU
uv sync --extra cuda    # NVIDIA (the rented H100); torch from PyPI
uv sync --extra rocm    # AMD Strix Halo; torch from PyTorch's ROCm index
```

To check the GPU (on ROCm it also reports through `cuda`):

```bash
uv run python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
```

No API keys in the repo: they go in `.env`, which is git-ignored.

### LaTeX

Requires TeX Live with `pdflatex` (and `latexmk` for watch mode).

```bash
make -C report          # builds report/apart-template.pdf
make -C report watch    # rebuilds on save
make -C report clean
```

The template is a LaTeX port of Apart's official template. It has a `\guidancetrue` / `\guidancefalse` switch in the preamble that shows or hides all guidance text: turn it off before submitting.

Submission format: PDF of up to 8 pages excluding references and appendices, with the artifact in this repo or in an appendix. A Limitations and Dual-Use Considerations appendix is mandatory. A 3 to 5 minute video is optional. Deadline: Sunday 2026-09-13 at 23:59 AoE.

## Conventions

- Everything in English: code, identifiers, documentation, report.
- Every citation of the incident record carries its source and, for METR, the line number in `context/metr-report-2026-08.txt`.
- Activations and model weights stay out of git. Probe weights, which are small, go in `results/`.
