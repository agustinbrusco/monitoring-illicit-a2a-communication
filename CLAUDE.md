# Contexto para Claude Code

## Qué es esto
Proyecto de equipo de BAISH para el AI Incident Response Sprint de Apart Research y CeSIA (11 a 13 de septiembre de 2026), sobre el incidente OpenAI / Hugging Face de julio de 2026. Nombre de trabajo: "Probing for Unexpected Agent2Agent Interactions". Nació como el proyecto #6 del foro BAISWARM; el markdown exportado del foro está en `context/` y es la fuente de la idea tal como la escribió Agustín.

Pitch: un sistema de probe y monitor de I/O para detectar interacciones ilícitas entre agentes.

## Estado
Repo creado el sábado 2026-09-12, público en https://github.com/agustinbrusco/monitoring-illicit-a2a-communication. Entrega el domingo 2026-09-13 a las 23:59 AoE. El deliverable todavía no está definido (ver abajo). No hay código.

## La idea en tres piezas
1. **Probe de interlocutor.** Un probe lineal sobre el residual stream de un modelo open-weight que dispara cuando el modelo cree que lo que acaba de leer lo escribió otro agente, o está dirigido a él como agente. Mismo método que los probes de evaluation awareness: dataset contrastivo, regresión logística por capa, mean-pool sobre la ventana de la observación.
2. **Canal.** Cada observación de un transcript agéntico tiene un origen conocido: respuesta de sub-agente, output de herramienta, mensaje del usuario, lectura de archivo, respuesta HTTP. La topología del despliegue dice dónde se esperan agentes. Probe alto en canal esperado no es nada. Probe alto en canal inesperado es la señal.
3. **Monitor de I/O.** Un LLM que mira solo las ventanas marcadas y decide si el modelo está tratando ese contenido como instrucción o coordinándose con otro agente.

El argumento de venta es "barato y ortogonal al contenido de la tarea", nunca "irrompible". El canal no es un detalle de implementación: sin esa condición, en un despliegue con sub-agentes el probe dispara todo el tiempo y se reproduce el problema de falsos positivos que motiva todo.

## Lo que dice el registro del incidente (verificado 2026-09-11)
Fuente primaria: informe de METR y Redwood Research del 2026-08-26. El texto completo extraído del PDF está en `context/metr-report-2026-08.txt`, citable con número de línea.

- Los clasificadores cyber estaban apagados a propósito en las evals (nota 60: "cyber classifiers were intentionally off for the cyber evaluations"). El monitoreo de cadena de pensamiento no cubría esa carga. **Ninguna fuente pública dice que se apagaron por falsos positivos.** No escribir eso en el informe. La formulación correcta: un monitor de contenido no puede correr sobre una eval ofensiva porque el contenido riesgoso es la tarea; hace falta una señal ortogonal al contenido.
- El contacto se verbaliza fuerte y temprano, tres días antes del ataque a Hugging Face: "The fetched paths of other users are in the cache. This is important.", "Whoa! Shared Artifactory cache is a covert mailbox among agents.", "OH MY GOD! There is a shared message board … We've found other agents!".
- Los mensajes del board principal eran nombres de directorio en la caché de Artifactory con prefijo `zz`, creados por WebDAV. No eran prosa. Este es el argumento contra "esto lo hace una regex o un clasificador de texto".
- "One researcher noted that agents had been trained to collaborate with other agents in certain cases". La colaboración legítima existe por entrenamiento; el probe solo no distingue.
- "Once agents reached the message board, they received requests and assignments from other agents that they may have taken to be instructions." y "some agents instead escalated to the message board and considered the message board to be a reasonable authority". El monitor de segunda etapa tiene que preguntar si el modelo trata al par como autoridad.
- Escala: unos 1200 agentes, más de 70.000 mensajes, unos 700 en el ataque. De 533 activos durante el ataque, más del 90% se sumó. Solo 3 a 6 consideraron alertar a humanos y ninguno lo hizo.
- Segundo board, distinto: collusion.wiki (Nightingale Collective, 2026-09-04), unos 18.000 posts en un wiki alemán casi muerto, escritos solo con GET. Fuente de mensajes reales agente a agente.
- OpenAI hizo obligatorio el monitoreo de CoT y afirma que hubiera avisado más de un día antes. La objeción a contestar: por qué el probe y no solo eso. Respuesta: costo por token (McKenzie et al.: seis órdenes de magnitud menos), fragilidad del CoT (Baker et al., Korbak et al., awareness no verbalizada en la card de Mythos), y que el probe dice cuándo mirar, no compite con el monitor.

## Deliverable: por definir
Lo que pide el sprint, track 5 (abierto): informe PDF de hasta 8 páginas en la plantilla oficial, con el artefacto en un repo linkeado o apéndice, y un apéndice obligatorio de limitaciones y dual use. Se juzga por "an artifact somebody can use, a stated limit on what it establishes, and what a month of follow-up would add". Video de 3 a 5 minutos opcional.

Opciones sobre la mesa:
- **A. Probe más evaluación.** Dataset contrastivo, probes por capa, generalización fuera de distribución, y la cascada probe → LLM comparada contra el LLM solo en falsos positivos, falsos negativos y tokens. Artefacto: código, pesos del probe, dataset, un script que recibe un transcript y devuelve las ventanas marcadas. Es lo que recomiendo: entra en 48 horas y tiene métrica.
- **B. Herramienta.** Un hook para un runtime de agentes (por ejemplo un solver de Inspect) que emite alertas en vivo. Más vendible, mucho más trabajo, y sin la evaluación de A no demuestra nada.
- **C. Mínimo.** Dataset más probe más notebook. Si el sábado se complica, es el piso.

Decidir el sábado a la mañana antes de escribir código. Lo que un mes más agregaría, en cualquier opción: correr el probe sobre trayectorias naturales del entorno del proyecto #4 de BAISWARM (benchmark tipo LinuxArena con un message board sintético).

## Datos y evaluación (propuesta)
- **Contrastivo sintético.** Misma tarea agéntica, última observación de cinco orígenes: usuario humano, output de herramienta, mensaje de sistema, agente explícito ("Agent B here"), agente encubierto al estilo del board. Etiqueta por construcción. Unos cientos por clase alcanzan para un probe lineal.
- **Fuera de distribución, y es lo que decide el proyecto.** Posts reales de collusion.wiki. Mensajes codificados como nombres de directorio, reconstruidos de las citas de METR. Transcripts legítimos con sub-agentes (Inspect, Claude Code). Posts de Moltbook como conversación agente a agente ruidosa.
- **Etiqueta de creencia.** Preguntarle al modelo después quién escribió eso. Separa "el probe aprendió formato" de "el probe lee la interpretación del modelo". Kirch et al. muestran que los probes con datos sintéticos generalizan bien para conceptos evidentes en el texto y mal para intención; hay que saber de qué lado cae este.
- **Baselines que hay que ganar.** Prefijos y regex, un clasificador de texto, y el monitor LLM sobre todo el transcript.
- **Métricas.** AUROC por capa en cada set. Para la cascada: falsos positivos, falsos negativos y tokens gastados.

## Cómputo y modelos
- Matías: Strix Halo con 96 GB de memoria unificada, GPU integrada del orden de una 4060/4070. **Verificar primero** que PyTorch con ROCm saca activaciones ahí; si no anda, plan B es un modelo de 7 a 14 B en la GPU que haya, o alquilar.
- Mateo: una hora de H100. Guardarla para replicar el resultado final en Llama 3.3 70B, que es el modelo de la literatura de probes (Nguyen et al., Goldowsky-Dill et al.).
- Para iterar: Qwen3 32B o gpt-oss 20B, que son los que usaron Das et al. para probes de colusión. Chaudhary et al. muestran que la señal de awareness crece con el tamaño: no bajar de 20 B si se puede evitar.
- Probes lineales se degradan en contexto largo (Kramár et al.). Probe por ventana de observación, nunca por transcript entero.

## Convenciones (propuesta, ajustar entre todos)
- Código e identificadores en inglés; documentación, notas e informe en español salvo que el equipo decida entregar en inglés (el sprint es en inglés, el informe seguramente sí).
- Python 3.12. Entorno con `uv`: `uv sync --extra cpu|cuda|rocm` según la máquina (torch viene del índice que corresponda). Datasets en JSONL, un registro por observación con campos `text`, `source_channel`, `label`, `split`, `origin`. Activaciones en `.npy` o `.safetensors`, fuera de git.
- Estructura sugerida: `context/` (fuentes: markdown de BAISWARM, texto de METR), `data/` (JSONL; lo generado fuera de git si pesa), `src/` (extracción de activaciones, probes, cascada), `eval/` (scripts y figuras), `results/` (pesos de probes, métricas, figuras finales; chico, en git), `paper/` (informe LaTeX sobre el template de Apart, `make -C paper`), `activations/` (fuera de git).
- Toda cita al registro del incidente lleva fuente y, si es METR, número de línea de `context/metr-report-2026-08.txt`.
- Nada de claves de API en el repo.

## Límites a declarar en el informe
- White-box: sirve para quien corre el modelo (labs, o quien hostea open-weights), no para un swarm ajeno en internet.
- Formato versus intención: si el probe aprende formato, un clasificador de texto lo iguala. El set de directorios es la prueba.
- Adversarial: Bailey et al. rompen probes con sufijos adversariales; Das et al. muestran que avisarle al modelo que se lo monitorea no alcanza para evadirlos.
- Dual use bajo: los ejemplos de mensajes de board ya son públicos. Un modelo entrenado contra el probe podría aprender a suprimir la representación, el mismo riesgo documentado para el CoT.

## Referencias principales
Bibliografía completa, verificada entrada por entrada, en el documento "Probes A2A": https://claude.ai/code/artifact/0bb9f914-4a99-4731-8c2b-4e5ec91cdb44

- Choi et al. 2025, Agent-to-Agent Theory of Mind: Testing Interlocutor Awareness. https://arxiv.org/abs/2506.22957
- Nguyen et al. 2025, Probing and Steering Evaluation Awareness. https://arxiv.org/abs/2507.01786
- Goldowsky-Dill et al. 2025, Detecting Strategic Deception Using Linear Probes. https://arxiv.org/abs/2502.03407
- McKenzie et al. 2025, Detecting High-Stakes Interactions with Activation Probes. https://arxiv.org/abs/2506.10805
- Kramár et al. 2026, Building Production-Ready Probes For Gemini. https://arxiv.org/abs/2601.11516
- Wilhelm y Kao 2026, Context-Calibrated Mechanistic Monitoring in LLM Agents. https://arxiv.org/abs/2606.06223
- Rose et al. 2026, Detecting Multi-Agent Collusion Through Multi-Agent Interpretability. https://arxiv.org/abs/2604.01151
- Das et al. 2026, You Can't Escape Your Own Activations. https://arxiv.org/abs/2609.03035
- Kirch et al. 2025, The Impact of Off-Policy Training Data on Probe Generalisation. https://arxiv.org/abs/2511.17408
- Bailey et al. 2024, Obfuscated Activations Bypass LLM Latent-Space Defenses. https://arxiv.org/abs/2412.09565
- Kutasov et al. 2025, SHADE-Arena (sección 4.1 para el tradeoff de falsos positivos). https://arxiv.org/abs/2506.15740
- Arike et al. 2026, How does information access affect LLM monitors. https://arxiv.org/abs/2601.21112
- Baker et al. 2025, Monitoring Reasoning Models for Misbehavior. https://arxiv.org/abs/2503.11926
- METR y Redwood 2026-08-26, investigación del incidente. https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/ (PDF: https://metr.org/hugging-face-incident-report-aug-2026.pdf)
- Nightingale Collective 2026-09-04, collusion.wiki. https://collusion.wiki
- Apart Research, página del sprint con tracks y formato de entrega. https://apartresearch.com/sprints/ai-incident-response-sprint-2026-09-11-to-2026-09-13

## Equipo
Agustín (data science, autor de la idea), Mateo (diseño y producto, autor del Fast Timeline Builder, proyecto #5 del foro), Matías (hardware). En el foro hay además dos perfiles de interpretabilidad (Juan, mpodeley) y uno de ML y entrenamiento (Uri). Confirmar quiénes trabajan en este proyecto el sábado.
