# ADR-016: Standardizing on Pytest for Testing

**Status:** Proposed  
**Date:** 2025-11-19  
**Author:** Emmanuel Awa  
**Tags:** Testing, MLOps, Quality  

## Context

**Problem Statement:** Without a formal standard for testing, practices can become inconsistent, making it difficult to ensure the quality, reliability, and maintainability of our growing collection of agentic patterns. Specifically, there is a need to ensure that the deterministic components of our agents are rigorously tested.

**Driving Factors:** The need for a consistent, reliable, and scalable testing strategy is paramount for a repository that serves as a guide for production-grade systems. We need to ensure that all patterns are well-tested and that new changes do not introduce regressions.

**Assumptions:** We are developing Python-based agents and patterns.

## Alternatives Considered

### 1. No Formal Testing Standard

Relying on individual developers to write tests as they see fit.

* **Pros:** No upfront effort to define a standard.
* **Cons:** Leads to inconsistent test quality and coverage. It makes it difficult to enforce testing as a requirement and complicates the maintenance of the patterns.

### 2. Using Python's built-in `unittest` framework

Using the `unittest` module from the Python standard library.

* **Pros:** It is part of the standard library, so it does not introduce any external dependencies.
* **Cons:** It requires more boilerplate code compared to other frameworks. Its fixture system is less flexible, and its syntax is more verbose.

### 3. Standardizing on `pytest` (Decision)

A mature, feature-rich, and widely adopted testing framework for Python.

* **Pros:**
  * **Simple Syntax:** `pytest` uses plain assert statements, making tests more readable and concise.
  * **Powerful Fixtures:** It has a powerful and flexible fixture system that simplifies the setup and teardown of test resources.
  * **Large Ecosystem:** It has a rich ecosystem of plugins that can extend its functionality (e.g., `pytest-mock`, `pytest-asyncio`).
  * **Auto-discovery:** It has a powerful test discovery mechanism.
* **Cons:** It introduces an external dependency to the project.

## Decision

We will standardize on **`pytest`** for all unit and integration testing in this repository. All new architectural patterns must include a `tests` directory with basic `pytest` coverage.

This includes:

* **Unit tests** for deterministic components such as parsers, validators, and helper functions.
* **Integration tests** with mocked examples for the agent loop and tool interactions.

## Consequences

* **Positive:**
  * **Improved Quality:** Enforces a high standard of quality and reliability for all patterns.
  * **Consistency:** Provides a consistent and predictable testing strategy across the repository.
  * **Maintainability:** Well-tested code is easier to maintain and refactor with confidence.
  * **Developer Experience:** `pytest`'s features will improve the developer experience when writing tests.

* **Negative:**
  * **New Dependency:** A new development dependency on `pytest` and its plugins will be added to the project.
  * **Learning Curve:** Developers who are not familiar with `pytest` will need to learn its conventions.

## Related Artifacts

This ADR will serve as the foundation for adding `tests` directories and `pytest` configurations to all existing and future patterns.
