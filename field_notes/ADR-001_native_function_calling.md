# ADR-001: Standardizing Native Function Calling for Tool Use

**Status:** Accepted  
**Date:** 2025-11-10  
**Author:** Emmanuel Awa  
**Tags:** [Agentic, Tooling, Reliability]  

## Context

Autonomous agents require reliable mechanisms to interact with external systems (APIs, databases). Early implementations often relied on "prompt engineering" strategies, where the LLM was instructed via system prompt to output a specific JSON structure when it needed to take an action.

In production enterprise environments, this purely prompt-based approach proved brittle. It frequently resulted in:

* **Hallucinated Parameters:** The model inventing arguments that don't exist in the API schema.
* **Malformed JSON:** Outputs that failed standard parsing libraries, requiring fragile regex post-processing.
* **Security Risks:** Vulnerability to prompt injection attacks that could manipulate the tool execution payload.

We needed a standardized pattern for all agents in this architecture to ensure deterministic, secure, and type-safe interactions with external tools.

## Alternatives Considered

### 1. Prompt-Engineered Structured Output (Status Quo)

Relying solely on few-shot prompting to guide the model to output valid JSON.

* *Pros:* Model agnostic; works on any LLM.
* *Cons:* High failure rate at scale; requires extensive post-processing and validation logic.

### 2. Constrained Decoding (Grammar-based)

Forcing the model's output token probabilities to conform to a specific formal grammar (e.g., BNF) during inference.

* *Pros:* Guarantees syntactically correct output.
* *Cons:* High latency overhead; complex to implement and maintain; often not supported by managed Model-as-a-Service endpoints.

### 3. Native GenAI Function Calling APIs (Decision)

Utilizing the first-party **"Tool Use"** or **"Function Calling"** APIs provided by modern foundation models (e.g., Gemini natively trained on standard tool schemas).

* *Pros:* Model is fine-tuned for this task, offering higher reliability; standardized schema definition (OpenAPI/JSON Schema); separates code (logic) from data (prompts).
* *Cons:* Vendor-specific implementation details (locking us slightly into specific provider patterns).

## Decision

We will standardize on **Option 3: Native GenAI Function Calling APIs** for all agentic implementations in this reference architecture.

All tools must be defined using strict JSON Schemas passed via the model's native API (e.g., Gemini `tools` parameter), rather than described loosely in the system prompt.

## Consequences

* **Positive:** drastic reduction in malformed tool calls; enables automatic generation of client libraries from standardized schemas; improved security posture by separating instructions from data.
* **Negative:** marginally higher complexity in initial setup compared to simple prompting; debugging requires inspecting standard API payloads rather than just reading raw text output.
