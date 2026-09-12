# Probing for Unexpected Agent2Agent Interactions

Probe lineal sobre activaciones más monitor de I/O para detectar interacciones inesperadas entre agentes en transcripts agénticos.

Proyecto del equipo de BAISH (Buenos Aires AI Safety Hub) para el [AI Incident Response Sprint](https://apartresearch.com/sprints/ai-incident-response-sprint-2026-09-11-to-2026-09-13) de Apart Research y CeSIA (11 al 13 de septiembre de 2026), track abierto, sobre el incidente OpenAI / Hugging Face de julio de 2026. Nació como el proyecto #6 del foro BAISWARM; el post original está en [`context/`](context/).

## La idea

1. **Probe de interlocutor.** Probe lineal sobre el residual stream de un modelo open-weight que dispara cuando el modelo cree que lo que acaba de leer lo escribió otro agente, o está dirigido a él como agente. Mismo método que los probes de evaluation awareness.
2. **Canal.** Cada observación del transcript tiene un origen conocido: sub-agente, herramienta, usuario, archivo, HTTP. Probe alto en un canal donde se esperan agentes no es nada. Probe alto en un canal inesperado es la señal.
3. **Monitor de I/O.** Un LLM que mira solo las ventanas marcadas y decide si el modelo está tratando ese contenido como instrucción o coordinándose con otro agente.

El argumento es "barato y ortogonal al contenido de la tarea", nunca "irrompible". El contexto completo (registro del incidente, plan de evaluación, cómputo, límites a declarar, bibliografía) está en [`CLAUDE.md`](CLAUDE.md).

## Estructura

```
context/      fuentes: post de BAISWARM, texto del informe de METR (citable por línea)
data/         datasets en JSONL, un registro por observación (esquema en data/README.md)
src/          paquete `a2a_probe`: extracción de activaciones, probes, cascada
eval/         scripts de evaluación y figuras
results/      pesos de probes, métricas y figuras finales (chico, va en git)
report/        informe en LaTeX sobre el template de Apart
activations/  activaciones en .npy / .safetensors (ignorado por git)
```

## Setup

### Python

Requiere [uv](https://docs.astral.sh/uv/). Elegí el extra según la máquina:

```bash
uv sync --extra cpu     # laptop sin GPU
uv sync --extra cuda    # NVIDIA (la H100 alquilada); torch de PyPI
uv sync --extra rocm    # AMD Strix Halo; torch del índice ROCm de PyTorch
```

Para verificar la GPU (en ROCm también responde por `cuda`):

```bash
uv run python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
```

Nada de claves de API en el repo: van en `.env`, que está ignorado.

### LaTeX

Requiere TeX Live con `pdflatex` (y `latexmk` para el modo watch).

```bash
make -C report          # compila report/apart-template.pdf
make -C report watch    # recompila al guardar
make -C report clean
```

El template es un port a LaTeX de la plantilla oficial de Apart. Tiene un switch `\guidancetrue` / `\guidancefalse` en el preámbulo que muestra u oculta todo el texto de guía: apagarlo antes de entregar.

Formato de entrega: PDF de hasta 8 páginas sin contar referencias y apéndices, con el artefacto en este repo o en un apéndice. El apéndice de limitaciones y dual use es obligatorio. Video de 3 a 5 minutos opcional. Entrega el domingo 2026-09-13 a las 23:59 AoE.

## Convenciones

- Código e identificadores en inglés. Documentación e informe en español salvo que el equipo decida entregar en inglés (el informe seguramente sí).
- Toda cita al registro del incidente lleva fuente y, si es METR, número de línea de `context/metr-report-2026-08.txt`.
- Activaciones y pesos de modelos fuera de git. Pesos de probes, que son chicos, en `results/`.
