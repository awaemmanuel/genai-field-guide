# ADR-015: Standardizing on ReAct Cognitive Architecture

**Status:** Accepted  
**Date:** 2025-11-19  
**Author:** Emmanuel Awa  
**Tags:** Agentic, Design Patterns, Cognitive Architecture  

## Context

**Problem Statement:** An agent's effectiveness is largely determined by its underlying reasoning process, or "cognitive architecture." While many patterns in this repository implicitly use a ReAct-like cycle, this has not been formalized. This lack of an explicit standard can lead to inconsistent agent designs, making them difficult to understand, debug, and maintain. New developers are left to infer the intended reasoning pattern.

**Driving Factors:** The need for a consistent, predictable, and effective reasoning framework for our agents. We want to provide clear guidance on how to build agents that can reliably solve problems by interacting with their environment through tools.

**Assumptions:** Agents are built using Large Language Models that have strong instruction-following and reasoning capabilities.

## Alternatives Considered

### 1. Chain-of-Thought (CoT)

The model generates a series of intermediate reasoning steps before producing a final answer. It is a pure reasoning pattern and does not involve external actions.

* **Pros:** Simple to prompt for and effective for complex reasoning tasks that do not require external information.
* **Cons:** Not suitable for tasks that require interacting with the world (e.g., looking up real-time data, executing code). The agent cannot correct its course based on external feedback.

### 2. Tree-of-Thoughts (ToT)

The model explores multiple reasoning paths (thoughts) simultaneously. It self-evaluates the progress made in each path and decides which one to pursue.

* **Pros:** More robust for complex problems that benefit from exploration and backtracking.
* **Cons:** Significantly more complex to implement and orchestrate. It requires a more sophisticated runner and can lead to higher latency and token consumption.

### 3. ReAct (Reason+Act) (Decision)

The model interleaves **Reasoning** (forming a thought about what to do next) and **Acting** (using a tool to interact with the environment). After each action, the agent observes the result and uses that observation to inform its next thought.

* **Pros:**
  * **Effective for Tool Use:** It is a natural fit for tasks that require dynamic interaction with an external environment.
  * **Debuggable:** The explicit thought-action-observation cycle is easy to trace, making it clear why an agent made a particular decision.
  * **Balance of Power and Simplicity:** It is more powerful than CoT for interactive tasks but less complex to implement than ToT.
* **Cons:** For problems that do not require tool use, the overhead of the ReAct loop can be unnecessary.

## Decision

We will standardize on the **ReAct (Reason+Act)** cognitive architecture as the default pattern for all agents in this repository that need to use tools to accomplish their goals.

This means that agents should be designed to follow a loop:

1. **Thought:** The agent reasons about the current state and decides on the next action.
2. **Action:** The agent selects and executes a tool.
3. **Observation:** The agent receives the output from the tool.
4. The agent uses the observation to inform its next thought, repeating the cycle until the task is complete.

## Consequences

* **Positive:**
  * **Consistency:** All tool-using agents will follow a consistent and predictable reasoning pattern.
  * **Clarity:** The code and prompts for our agents will be easier to understand and maintain.
  * **Guidance:** New developers will have a clear and effective mental model for building agents.

* **Negative:**
  * For very simple, single-shot tasks, the ReAct loop may introduce unnecessary overhead. In such rare cases, a simpler architecture may be justified, but this should be explicitly documented.

## Related Artifacts

* **Code Pattern:** `01_agentic_architectures/patterns/orchestration/01_basic_react_agent/`
