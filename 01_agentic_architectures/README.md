# Agentic Architectures

This directory contains a collection of reusable patterns and reference implementations for building autonomous agent architectures.

## Orchestration Patterns

The `patterns/orchestration` directory contains several common patterns for coordinating the work of multiple agents:

* **BasicReactAgent**: A simple agent that demonstrates the ReAct (Reason+Act) pattern. This is the fundamental building block for more complex agentic systems.

* **SequentialPipeline**: A pipeline of agents that execute in a predefined sequence. This is useful for deterministic workflows where the steps are known and must be executed in a specific order.

* **ParallelExecution**: A set of agents that execute concurrently to reduce latency. This is useful for tasks that can be broken down into independent sub-tasks.

* **FeedbackLoop**: A pattern where agents work in a loop for iterative refinement and improvement. This is useful for tasks that require multiple iterations to achieve a high-quality result, such as writing and editing a document.

*   **Delegation**: A primary agent that delegates specific tasks to a specialist agent. This pattern promotes modularity and reusability, allowing you to build complex systems by composing smaller, specialized agents.



*   **Human-in-the-Loop**: A pattern for long-running operations that require human approval before completion. This is essential for building safe and reliable agents that perform critical tasks.



*   **MCP FileSystem**: An agent that uses the Model Context Protocol (MCP) to interact with a local file system, demonstrating how to connect agents to external services in a standardized way.
