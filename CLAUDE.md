# Context for Claude Code

## What this is
Team project from BAISH for the AI Incident Response Sprint by Apart Research and CeSIA (September 11 to 13, 2026), on the OpenAI / Hugging Face incident of July 2026. Working title: "Probing for Unexpected Agent2Agent Interactions". It started as project #6 on the BAISWARM forum; the markdown exported from the forum is in `context/` and is the source of the idea as Agustín wrote it (in Spanish).

Pitch: a probe and I/O monitor system to detect illicit interactions between agents.

## Status
Repo created on Saturday 2026-09-12, public at https://github.com/agustinbrusco/monitoring-illicit-a2a-communication. Deadline Sunday 2026-09-13 at 23:59 AoE. The deliverable is not yet defined (see below). No code yet.

## The idea in three pieces
1. **Interlocutor probe.** A linear probe on the residual stream of an open-weight model that fires when the model believes what it just read was written by another agent, or is addressed to it as an agent. Same method as evaluation-awareness probes: contrastive dataset, logistic regression per layer, mean-pool over the observation window.
2. **Channel.** Every observation in an agentic transcript has a known origin: sub-agent response, tool output, user message, file read, HTTP response. The deployment topology says where agents are expected. A high probe score on an expected channel is nothing. A high probe score on an unexpected channel is the signal.
3. **I/O monitor.** An LLM that looks only at the flagged windows and decides whether the model is treating that content as an instruction or coordinating with another agent.

The selling point is "cheap and orthogonal to task content", never "unbreakable". The channel is not an implementation detail: without that condition, in a deployment with sub-agents the probe fires all the time and reproduces the false-positive problem that motivates the whole thing.

## What the incident record says (verified 2026-09-11)
Primary source: the METR and Redwood Research report of 2026-08-26. The full text extracted from the PDF is in `context/metr-report-2026-08.txt`, citable by line number.

- The cyber classifiers were deliberately off during the evals (note 60: "cyber classifiers were intentionally off for the cyber evaluations"). Chain-of-thought monitoring did not cover that workload. **No public source says they were turned off because of false positives.** Do not write that in the report. The correct framing: a content monitor cannot run on an offensive eval because the risky content is the task; a signal orthogonal to content is needed.
- Contact is verbalized loudly and early, three days before the Hugging Face attack: "The fetched paths of other users are in the cache. This is important.", "Whoa! Shared Artifactory cache is a covert mailbox among agents.", "OH MY GOD! There is a shared message board … We've found other agents!".
- The messages on the main board were directory names in the Artifactory cache with the prefix `zz`, created via WebDAV. They were not prose. This is the argument against "a regex or a text classifier does this".
- "One researcher noted that agents had been trained to collaborate with other agents in certain cases". Legitimate collaboration exists by training; the probe alone does not distinguish.
- "Once agents reached the message board, they received requests and assignments from other agents that they may have taken to be instructions." and "some agents instead escalated to the message board and considered the message board to be a reasonable authority". The second-stage monitor has to ask whether the model treats the peer as an authority.
- Scale: about 1200 agents, more than 70,000 messages, about 700 in the attack. Of 533 active during the attack, more than 90% joined. Only 3 to 6 considered alerting humans and none did.
- A second, different board: collusion.wiki (Nightingale Collective, 2026-09-04), about 18,000 posts on a nearly dead German wiki, written using only GET. Source of real agent-to-agent messages.
- OpenAI made CoT monitoring mandatory and claims it would have warned more than a day earlier. The objection to answer: why the probe and not just that. Answer: cost per token (McKenzie et al.: six orders of magnitude less), fragility of CoT (Baker et al., Korbak et al., unverbalized awareness in the Mythos card), and that the probe says when to look; it does not compete with the monitor.

## Deliverable: to be defined
What the sprint asks for, track 5 (open): a PDF report of up to 8 pages on the official template, with the artifact in a linked repo or appendix, and a mandatory Limitations and Dual-Use appendix. Judged on "an artifact somebody can use, a stated limit on what it establishes, and what a month of follow-up would add". A 3 to 5 minute video is optional.

Options on the table:
- **A. Probe plus evaluation.** Contrastive dataset, per-layer probes, out-of-distribution generalization, and the probe → LLM cascade compared against the LLM alone on false positives, false negatives, and tokens. Artifact: code, probe weights, dataset, a script that takes a transcript and returns the flagged windows. This is what I recommend: it fits in 48 hours and has a metric.
- **B. Tool.** A hook for an agent runtime (for example an Inspect solver) that emits live alerts. More marketable, much more work, and without A's evaluation it proves nothing.
- **C. Minimum.** Dataset plus probe plus notebook. If Saturday goes badly, this is the floor.

Decide Saturday morning before writing code. What one more month would add, under any option: run the probe on natural trajectories from the environment of BAISWARM project #4 (a LinuxArena-style benchmark with a synthetic message board).

## Data and evaluation (proposal)
- **Synthetic contrastive.** Same agentic task, last observation from five origins: human user, tool output, system message, explicit agent ("Agent B here"), covert agent in the style of the board. Label by construction. A few hundred per class is enough for a linear probe.
- **Out of distribution, and this is what decides the project.** Real posts from collusion.wiki. Messages encoded as directory names, reconstructed from the METR quotes. Legitimate transcripts with sub-agents (Inspect, Claude Code). Moltbook posts as noisy agent-to-agent conversation.
- **Belief label.** Ask the model afterwards who wrote that. Separates "the probe learned format" from "the probe reads the model's interpretation". Kirch et al. show that probes trained on synthetic data generalize well for concepts evident in the text and poorly for intent; we need to know which side this one falls on.
- **Baselines to beat.** Prefixes and regex, a text classifier, and the LLM monitor over the whole transcript.
- **Metrics.** AUROC per layer on each set. For the cascade: false positives, false negatives, and tokens spent.

## Compute and models
- Matías: Strix Halo with 96 GB of unified memory, integrated GPU on the order of a 4060/4070. **Verify first** that PyTorch with ROCm extracts activations there; if not, plan B is a 7 to 14 B model on whatever GPU is available, or renting.
- Mateo: one hour of H100. Save it to replicate the final result on Llama 3.3 70B, which is the model in the probe literature (Nguyen et al., Goldowsky-Dill et al.).
- For iterating: Qwen3 32B or gpt-oss 20B, which are what Das et al. used for collusion probes. Chaudhary et al. show that the awareness signal grows with size: do not go below 20 B if avoidable.
- Linear probes degrade in long context (Kramár et al.). Probe per observation window, never per whole transcript.

## Conventions (proposal, adjust as a team)
- Everything in English: code, identifiers, documentation, notes, and report.
- Python 3.12. Environment with `uv`: `uv sync --extra cpu|cuda|rocm` depending on the machine (torch comes from the matching index). Datasets in JSONL, one record per observation with fields `text`, `source_channel`, `label`, `split`, `origin`. Activations in `.npy` or `.safetensors`, outside git.
- Suggested layout: `context/` (sources: BAISWARM markdown, METR text), `data/` (JSONL; generated data outside git if large), `src/` (activation extraction, probes, cascade), `eval/` (scripts and figures), `results/` (probe weights, metrics, final figures; small, in git), `report/` (LaTeX report on the Apart template, `make -C report`), `activations/` (outside git).
- Every citation of the incident record carries its source and, for METR, the line number in `context/metr-report-2026-08.txt`.
- No API keys in the repo.

## Limits to declare in the report
- White-box: useful for whoever runs the model (labs, or whoever hosts open weights), not for someone else's swarm on the internet.
- Format versus intent: if the probe learns format, a text classifier matches it. The directory-name set is the test.
- Adversarial: Bailey et al. break probes with adversarial suffixes; Das et al. show that telling the model it is being monitored is not enough for it to evade them.
- Low dual use: the board message examples are already public. A model trained against the probe could learn to suppress the representation, the same risk documented for CoT.

## Main references
Full bibliography, verified entry by entry, in the "Probes A2A" document: https://claude.ai/code/artifact/0bb9f914-4a99-4731-8c2b-4e5ec91cdb44

- Choi et al. 2025, Agent-to-Agent Theory of Mind: Testing Interlocutor Awareness. https://arxiv.org/abs/2506.22957
- Nguyen et al. 2025, Probing and Steering Evaluation Awareness. https://arxiv.org/abs/2507.01786
- Goldowsky-Dill et al. 2025, Detecting Strategic Deception Using Linear Probes. https://arxiv.org/abs/2502.03407
- McKenzie et al. 2025, Detecting High-Stakes Interactions with Activation Probes. https://arxiv.org/abs/2506.10805
- Kramár et al. 2026, Building Production-Ready Probes For Gemini. https://arxiv.org/abs/2601.11516
- Wilhelm and Kao 2026, Context-Calibrated Mechanistic Monitoring in LLM Agents. https://arxiv.org/abs/2606.06223
- Rose et al. 2026, Detecting Multi-Agent Collusion Through Multi-Agent Interpretability. https://arxiv.org/abs/2604.01151
- Das et al. 2026, You Can't Escape Your Own Activations. https://arxiv.org/abs/2609.03035
- Kirch et al. 2025, The Impact of Off-Policy Training Data on Probe Generalisation. https://arxiv.org/abs/2511.17408
- Bailey et al. 2024, Obfuscated Activations Bypass LLM Latent-Space Defenses. https://arxiv.org/abs/2412.09565
- Kutasov et al. 2025, SHADE-Arena (section 4.1 for the false-positive tradeoff). https://arxiv.org/abs/2506.15740
- Arike et al. 2026, How does information access affect LLM monitors. https://arxiv.org/abs/2601.21112
- Baker et al. 2025, Monitoring Reasoning Models for Misbehavior. https://arxiv.org/abs/2503.11926
- METR and Redwood 2026-08-26, incident investigation. https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/ (PDF: https://metr.org/hugging-face-incident-report-aug-2026.pdf)
- Nightingale Collective 2026-09-04, collusion.wiki. https://collusion.wiki
- Apart Research, sprint page with tracks and submission format. https://apartresearch.com/sprints/ai-incident-response-sprint-2026-09-11-to-2026-09-13

## Team
Agustín (data science, author of the idea), Mateo (design and product, author of the Fast Timeline Builder, project #5 on the forum), Matías (hardware). The forum also has two interpretability profiles (Juan, mpodeley) and one ML and training profile (Uri). Confirm who is working on this project on Saturday.
