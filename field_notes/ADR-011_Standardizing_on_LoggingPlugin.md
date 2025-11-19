# ADR-011: Standardizing on LoggingPlugin for Agent Observability

**Status:** Accepted  
**Date:** 2025-11-16  
**Author:** Emmanuel Awa  
**Tags:** Agentic, Orchestration, MLOps

## Context

**Problem Statement:** As the number of agents and patterns in the repository grows, there is no consistent, repository-wide standard for logging agent activities. This makes debugging, monitoring, and evaluating agent performance difficult and time-consuming.

**Driving Factors:** The need for a unified approach to observability that can scale with the project. The desire to have a single, well-understood way to get visibility into agent behavior, both in development and in production-like environments.

**Assumptions:** We will continue to use the `google-adk` library as the primary framework for building agents.

## Alternatives Considered

### 1. Manual Logging in Each Agent

* *Pros:* Simple to implement for a single agent.
* *Cons:* Inconsistent, error-prone, and does not scale. Each developer would need to remember to add logging statements, and the format and content of the logs would vary.

### 2. Custom Logging Plugin

* *Pros:* Allows for complete control over what is logged and how it is formatted.
* *Cons:* Requires significant effort to develop and maintain. It would also introduce another piece of custom code to the project.

### 3. Standardize on the built-in `LoggingPlugin` (Decision)

* *Pros:* Provides a comprehensive, out-of-the-box solution for agent observability. It is easy to use and requires minimal configuration. It is also maintained as part of the `google-adk` library.
* *Cons:* Less flexibility compared to a custom plugin.

## Decision

We will standardize on the use of the `LoggingPlugin` for all agents in this repository. The `LoggingPlugin` will be added to the `InMemoryRunner` for each agent pattern.

## Consequences

* **Positive:**
  * All agents will have consistent, detailed logging.
  * Debugging and monitoring will be significantly easier.
  * The time to develop new agents will be reduced, as developers will not need to implement their own logging.

* **Negative:**
  * A small amount of boilerplate code will be added to each runner file.

## Related Artifacts

* [01_agentic_architectures/patterns/orchestration/15_logging_and_tracing/](01_agentic_architectures/patterns/orchestration/15_logging_and_tracing/)
