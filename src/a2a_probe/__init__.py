"""Probe + I/O monitor for unexpected agent-to-agent interactions in agentic transcripts.

Planned modules:
- activations: extract per-observation residual-stream activations from an open-weight model
- probes: per-layer logistic-regression probes on mean-pooled activations
- cascade: probe -> channel filter -> LLM monitor over flagged windows
"""

__version__ = "0.1.0"
