# Architectural Glossary

> **Definitions of key terms as they are applied within this reference architecture.**

## Core Architectural Concepts

### **ADR (Architectural Decision Record)**

A standardized document that captures a significant architectural decision, including the context, alternatives considered, and consequences.

* *Usage:* We use ADRs in `field_notes/` to document *why* we chose specific patterns (e.g., ADR-002 on adopting MCP).

### **Agent**

An autonomous software entity capable of perceiving its environment (via context), making decisions (via reasoning loops), and taking actions (via tools) to achieve a specific goal.

* *See also: ReAct, Orchestration*

### **Cognitive Architecture**

The specific "brain" pattern used by an agent to reason. Defines how it breaks down problems.

* *Examples in this repo:* ReAct (Reason+Act), Chain-of-Thought (CoT), Tree-of-Thoughts (ToT).

### **Model Context Protocol (MCP)**

An open standard that enables standardized, secure, and discoverable connections between AI agents and external data sources or tools.

* *Usage:* Our preferred method for decoupling tool definitions from agent logic (see ADR-002).

### **Orchestration**

The mechanism for coordinating multiple agents or complex multi-step workflows.

* *Types:*
  * **Controller-based:** A central "boss" agent delegates tasks.
  * **Choreography (A2A):** Agents communicate directly with each other without a central bottleneck.

### **Tool (Function)**

A deterministic unit of capability exposed to an agent, typically an API wrapper defined by a rigorous JSON schema.

* *Key distinction:* Tools must be *deterministic* (same input = same output) to be reliable, unlike the LLM itself.

### **Agent as a Tool**

A design pattern where a specialist agent is wrapped as a tool and used by a primary agent to perform a specific task. This is a form of delegation and promotes modularity and reusability.

* *See also: Orchestration*

### **Long-Running Operation (LRO)**

An operation within an agent's workflow that may not return immediately, often requiring a pause for external input (e.g., human approval) or the completion of a background task. LROs are typically handled by resumable agents that can maintain state across these pauses.

* *See also: Resumable Agents*

## State & Memory

### **Episodic Memory**

Short-term, highly detailed memory of the *current* execution run (e.g., the last 10 turns of conversation). Usually stored in the context window.

### **Semantic Memory**

Long-term, compressed knowledge retrieved based on meaning rather than recency.

* *Implementation:* Typically powered by Vector Databases (RAG).

### **MemoryService**
A service that provides long-term knowledge storage for agents, persisting information across multiple conversations and application restarts. It can support various storage backends (e.g., in-memory, vector databases, cloud services).

### **load_memory**
A reactive tool that an agent can use to explicitly search and retrieve relevant information from its `MemoryService` when it determines that past knowledge is needed to answer a query or complete a task.

### **preload_memory**
A proactive tool that automatically loads relevant information from the `MemoryService` into the agent's context before each turn. This ensures that the agent always has access to pertinent long-term knowledge, but can be less efficient than `load_memory` if not always needed.

### **Memory Consolidation**
The process of intelligently extracting and summarizing key facts from raw conversation events before storing them in long-term memory. This reduces storage size, improves retrieval efficiency, and helps the agent focus on salient information.

### **Callback**
A function registered with an agent or runner that is automatically executed at specific points in the agent's lifecycle (e.g., before/after an agent turn, before/after a tool call). Callbacks are used to inject custom logic, such as logging, monitoring, or automated memory storage.

## Session Management

### **Session**

A container for a single, continuous conversation between a user and an agent. It encapsulates the chronological history of all events and the current state.

### **Event**

An individual interaction within a session. Events are the building blocks of a conversation and can include user inputs, agent responses, tool calls, and tool outputs.

### **Session State**

A key-value store representing the agent's short-term "scratchpad" memory for a specific session. It holds dynamic information that needs to be accessed and modified by tools or agents during the conversation.

### **SessionService**

The storage layer responsible for the persistence of session data. Different implementations determine where the data lives (e.g., in-memory vs. a database).

* *See also: `InMemorySessionService`, `DatabaseSessionService`*

### **Runner**

The orchestration layer that manages the flow of information and the execution of the agentic loop for a given session. It is responsible for invoking the agent, handling events, and maintaining the session history.

### **Context Compaction**

An automated process of summarizing the event history within a long-running session. This helps manage the size of the context sent to the LLM, reducing latency and cost while preserving relevant information.

## Production Engineering

### **Evals (Evaluations)**

Systematic tests used to measure the performance of non-deterministic generative systems.

* *Types:*
  * **Deterministic Evals:** Checking if the output strictly matches a regex or exact string.
  * **LLM-as-a-Judge:** Using a stronger model to grade the quality of a weaker model's output.

### **Structured Output**

Forcing a generative model to return response strictly adhering to a specific schema (usually JSON) rather than free text. Critical for reliable downstream processing.
