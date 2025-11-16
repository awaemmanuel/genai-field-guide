# ADR-013: Standardizing on Systematic Evaluation for Agent Quality

**Status:** Proposed
**Date:** 2025-11-16
**Author:** Emmanuel Awa
**Tags:** Agentic, MLOps, Testing

## Context

**Problem Statement:** As our agents become more complex, we need a reliable and scalable way to ensure that new changes do not degrade their performance. Manual testing is time-consuming, error-prone, and does not scale.

**Driving Factors:** The need to proactively detect regressions in agent behavior, and to have a consistent way of measuring agent quality over time.

**Assumptions:** We will continue to use the `google-adk` library as the primary framework for building agents.

## Alternatives Considered

### 1. Manual Testing

*   *Pros:* Simple to get started with for a single agent.
*   *Cons:* Does not scale, is not repeatable, and is prone to human error.

### 2. Ad-hoc Scripting

*   *Pros:* Can be tailored to specific agents and use cases.
*   *Cons:* Leads to a proliferation of custom scripts that are difficult to maintain and do not provide a unified view of agent quality.

### 3. Standardize on `adk eval` for Systematic Evaluation (Decision)

*   *Pros:* Provides a standardized, out-of-the-box solution for systematic agent evaluation. It is easy to use, requires minimal configuration, and is maintained as part of the `google-adk` library.
*   *Cons:* May not be flexible enough for all possible evaluation scenarios.

## Decision

We will standardize on the use of the `adk eval` CLI command for systematic evaluation of all agents in this repository. This includes the creation of `test_config.json` and `.evalset.json` files for each agent pattern.

## Consequences

*   **Positive:**
    *   All agents will have a consistent, automated way of being evaluated.
    *   Regressions in agent performance will be easier to detect.
    *   The overall quality of our agents will improve.

*   **Negative:**
    *   A small amount of boilerplate code and configuration will be added to each agent pattern.

## Related Artifacts

*   [01_agentic_architectures/patterns/orchestration/20_systematic_evaluation/](01_agentic_architectures/patterns/orchestration/20_systematic_evaluation/)
