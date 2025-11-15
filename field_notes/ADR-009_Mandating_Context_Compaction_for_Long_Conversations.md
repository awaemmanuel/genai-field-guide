# ADR-009: Mandating Context Compaction for Long-Running Conversations

**Status:** Proposed
**Date:** 2025-11-14
**Author:** Emmanuel Awa
**Tags:** [Agentic, Context Management, Scalability]

## Context

Large Language Models have a finite context window. As a conversation with an agent grows, the number of tokens in the conversation history increases. If unmanaged, this will eventually exceed the model's context limit, leading to errors or, more subtly, the loss of early context, causing the agent to "forget" what was discussed at the beginning of the conversation.

The `google-adk` provides an `EventsCompactionConfig` that can be applied to an `App`. This feature automatically triggers a summarization process in the background when the conversation reaches a certain length, effectively "compacting" the history into a more concise form. This allows the agent to maintain the salient points of the conversation while staying within the context window.

To build robust, scalable agents that can handle long-running tasks, we need a standardized approach to prevent context window overflow.

## Decision

We will mandate the use of `EventsCompactionConfig` for any agent that is designed for a long-running or extended conversation, which we define as any interaction that is reasonably expected to exceed **10 turns**.

This means that such agents must be wrapped in an `App` and configured with an appropriate `EventsCompactionConfig`. The `compaction_interval` and `overlap_size` should be tuned based on the specific use case, but a sensible default (e.g., interval of 5, overlap of 2) should be used as a starting point.

## Consequences

*   **Positive:**
    *   Our agent patterns will be more robust and less likely to fail due to context window limitations.
    *   It forces us to think about the conversational length and context management early in the design process.
    *   It provides a clear, standardized solution to a common problem in agent development.

*   **Negative:**
    *   It introduces a small amount of additional complexity in the agent setup, as the agent must be wrapped in an `App`.
    *   It will incur a minor increase in LLM usage due to the background summarization calls. This is a necessary trade-off for building scalable and resilient agents.
