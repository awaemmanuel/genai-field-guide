# ADR-010: Standardizing Session State Key Conventions

**Status:** Proposed
**Date:** 2025-11-14
**Author:** Emmanuel Awa
**Tags:** [Agentic, State Management, Convention]

## Context

The session state (`tool_context.state`) provides a key-value store for an agent to maintain dynamic information throughout a conversation. As we build more complex agents with multiple tools, the session state can become cluttered and difficult to manage. Without a clear naming convention, we risk key collisions (where two different tools try to use the same key for different purposes) and make it difficult to debug the agent's state.

The `day-3a-agent-sessions.ipynb` notebook introduced a convention of using prefixes (e.g., `user:`) to organize the session state. We need to formalize this convention to ensure consistency across all our architectural patterns.

## Decision

We will adopt a standardized convention for all keys stored in the session state, using a `{scope}:{key_name}` format. The following scopes are defined:

*   **`user:`**: For user-specific information that is not tied to a specific application, such as a user's name, preferences, or location.
    *   *Example:* `user:name`, `user:theme_preference`

*   **`app:`**: For application-specific information that is relevant to the current task or workflow.
    *   *Example:* `app:shopping_cart`, `app:current_project_id`

*   **`temp:`**: For temporary or transient information that is only needed for a short period within a single turn or a few turns.
    *   *Example:* `temp:requires_clarification`

All tools and agents that interact with the session state *must* use this convention.

## Consequences

*   **Positive:**
    *   The session state will be more organized, readable, and easier to debug.
    *   It significantly reduces the risk of key collisions between different tools or agents.
    *   It provides a clear mental model for understanding the scope and lifecycle of the data stored in the session state.

*   **Negative:**
    *   It adds a minor amount of verbosity to the keys. This is a small price to pay for the significant improvement in clarity and maintainability.
