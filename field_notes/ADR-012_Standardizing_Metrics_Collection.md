# ADR-012: Standardizing Metrics Collection for Agent Performance

**Status:** Proposed
**Date:** 2025-11-16
**Author:** Emmanuel Awa
**Tags:** Agentic, Orchestration, MLOps

## Context

**Problem Statement:** While the `LoggingPlugin` provides detailed logs, it does not provide a high-level, aggregated view of agent performance. It is difficult to answer questions like "How many times has this agent been run?" or "What is the average tool call latency?" without manually parsing logs.

**Driving Factors:** The need to track key performance indicators (KPIs) for our agents to understand their usage and identify performance bottlenecks.

**Assumptions:** We will continue to use the `google-adk` library as the primary framework for building agents.

## Alternatives Considered

### 1. No Standardized Metrics

*   *Pros:* No upfront effort.
*   *Cons:* Impossible to track agent performance over time. Difficult to identify and diagnose performance issues.

### 2. Custom Metrics in Each Agent

*   *Pros:* Simple to implement for a single agent.
*   *Cons:* Inconsistent, error-prone, and does not scale. The metrics collected would vary from agent to agent.

### 3. Standardize on a Custom `MetricsPlugin` (Decision)

*   *Pros:* Provides a consistent way to collect and report metrics across all agents. It is extensible and can be adapted to our specific needs.
*   *Cons:* Requires a small amount of custom code to be maintained.

## Decision

We will standardize on the use of a custom `MetricsPlugin` for all agents in this repository. The `MetricsPlugin` will be added to the `InMemoryRunner` for each agent pattern. The plugin will collect a standard set of metrics, including agent run count, tool call count, and model request count.

## Consequences

*   **Positive:**
    *   All agents will have consistent metrics collection.
    *   It will be easy to track agent performance and identify bottlenecks.
    *   The time to develop new agents will be reduced, as developers will not need to implement their own metrics collection.

*   **Negative:**
    *   A small amount of custom code will need to be maintained.

## Related Artifacts

*   [01_agentic_architectures/patterns/orchestration/16_metrics_and_monitoring/](01_agentic_architectures/patterns/orchestration/16_metrics_and_monitoring/)
