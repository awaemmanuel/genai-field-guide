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

## State & Memory

### **Episodic Memory**

Short-term, highly detailed memory of the *current* execution run (e.g., the last 10 turns of conversation). Usually stored in the context window.

### **Semantic Memory**

Long-term, compressed knowledge retrieved based on meaning rather than recency.

* *Implementation:* Typically powered by Vector Databases (RAG).

## Production Engineering

### **Evals (Evaluations)**

Systematic tests used to measure the performance of non-deterministic generative systems.

* *Types:*
  * **Deterministic Evals:** Checking if the output strictly matches a regex or exact string.
  * **LLM-as-a-Judge:** Using a stronger model to grade the quality of a weaker model's output.

### **Structured Output**

Forcing a generative model to return response strictly adhering to a specific schema (usually JSON) rather than free text. Critical for reliable downstream processing.
