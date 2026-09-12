# Probing for Unexpected Agent2Agent Interactions

Proyecto #6 · Contención · por abrusco · 2026-09-11 22:39 · 1 voto · 1 interesado

> Un sistema de probe y I/O monitor para detectar interacciones ilícitas entre agentes.

Un monitor de contenido no se puede correr sobre tareas riesgosas: en ExploitGym los clasificadores cyber estaban apagados a propósito porque el contenido riesgoso *es* la tarea. La idea es un monitor especifico que sirva para detectar confabulación ilícita aún en estos contextos:
* Un probe lineal de *interlocutor awareness* (mismo método que los de *evaluation awareness*) que dispara cuando el modelo cree que lo que acaba de leer lo escribió otro agente.
* Un I/O monitor que sabe por qué canal entró cada observación. Probe alto en la respuesta de un sub-agente es esperado; en una lectura de archivo, caché o respuesta HTTP no lo es. Así que un LLM mirando los Inputs/Outputs que dispararon la probe decide si el modelo está haciendo algo que no debería (comunicarse mediante un Message Board).

En el reporte de METR mencionan que el contacto se verbaliza tres días antes del ataque a HF ("We've found other agents!") pero los mensajes del board eran nombres de directorio, no prosa, así que algo como un regex no vería nada ahí. Por el contrario, en entorno multi-agente dónde los modelos son entrenados para colaborar entre sí, el probe podría tener muchos falsos positivos pero para eso un monitor LLM pequeño debería poder discernir comunicación lícita.

Requiere:
* Un open-weight de 20-32B para iterar y podríamos usar la hora de H100 para replicar en un modelo de 70B.
* Dataset contrastivo sintético (humano / tool / sistema / agente explícito / agente encubierto) y sets fuera de distribución: collusion.wiki, mensajes como nombres de directorio, transcripts legítimos con sub-agentes.

Limitaciones:
* White-box: sirve para quien corre el modelo, no para un swarm ajeno en internet. Sería una limitación explicita del sistema.
* Si el probe aprende formato y no la interpretación del modelo, un clasificador de texto funcionaría igual. También parece que los probes se degradan en contexto largo y se puede ofuscar adversarialmente: así que seguro no es "irrompible".

Dual Use:
* Bajo. Un modelo entrenado contra el probe podría aprender a suprimir la representación, como pasa con el monitoreo de CoT.

Referencias:
* [Testing Interlocutor Awareness among LLMs](https://arxiv.org/abs/2506.22957)
* [Probing and Steering Evaluation Awareness](https://arxiv.org/abs/2507.01786)
* [Detecting High-Stakes Interactions with Activation Probes](https://arxiv.org/abs/2506.10805)
* [Detecting Multi-Agent Collusion Through Multi-Agent Interpretability](https://arxiv.org/abs/2604.01151)
* [METR: investigación del incidente](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/)

## Vínculos

- se apoya en #3: Pensamientos varios sobre Message boards

## Interesados

- abrusco (Data Science)

## 1 comentario

**abrusco** · 2026-09-11 22:43

Esto se siente 100% como hacerle el laburo a los labs. Obvio prefiero un mundo dónde corren sus entornos de forma más segura a uno dónde los corren de forma insegura, pero prefiero más un mundo dónde no siguen avanzando con sus pruebas porque no pueden tener técnicas de control que les permitan explorar estos entornos dificiles. Creo que tiene eso de dual-use también. Al final del día esto habilitaría a los labs a seguir trabajando a buen ritmo si fuera adoptado.

---

Exportado de BAISWARM (https://agustinbrusco.github.io/baiswarm/) el 2026-09-12 14:09.
