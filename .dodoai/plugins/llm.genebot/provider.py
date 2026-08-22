"""Declarative Genebot provider entry point for the plugin registry.

The executable adapter is composed by the Core LLM gateway.  Keeping this entry
declarative preserves the public Plugin SDK boundary while the provider extension
point is still reported as unsupported by the current lifecycle registrar.
"""

from __future__ import annotations

PROVIDER_TYPE = "llm"
PROVIDER_ID = "genebot"
PROVIDER_IMPLEMENTATION = (
    "dodo_core.infrastructure.llm.genebot_provider:GenebotProvider"
)

__all__ = ["PROVIDER_ID", "PROVIDER_IMPLEMENTATION", "PROVIDER_TYPE"]
