# ADR-002: Adopting Model Context Protocol (MCP) for Tool Interoperability

**Status:** Accepted  
**Date:** 2025-11-10  
**Author:** Emmanuel Awa  
**Tags:** [Agentic, Tooling, Standards, MCP]  

## Context

Our agentic architecture requires connecting foundation models to a growing diverse set of internal data sources (databases, local files, SaaS APIs).

While ADR-001 standardized *how* we invoke tools (via Native Function Calling), it does not solve the *standardization* of how these data sources are exposed to the agents. This leads to:

* **High Fragmentation:** Every new tool requires writing bespoke glue code to wrap it into a function schema.
* **Vendor Lock-in:** Tool definitions often become tightly coupled to specific provider SDKs.
* **Maintenance Burden:** Updating an underlying API requires hunting down every agent codebase that hardcoded that tool's definition.

We need a unified protocol that decouples *data serving* from *agent consumption*.

## Alternatives Considered

### 1. Bespoke Native Function Definitions (Status Quo)

Manually writing JSON schemas/Python Pydantic models for every new tool and hardcoding them into agent orchestration loops.

* *Pros:* Lowest initial barrier to entry for a single, simple agent.
* *Cons:* Does not scale across teams; high duplication of effort; tight coupling between agent and tool.

### 2. Adopting Model Context Protocol (MCP) (Decision)

Implementing established MCP servers for our data domains, allowing any MCP-compliant agent client to discover and consume these resources automatically.

* *Pros:* Decouples data owners (building MCP servers) from agent builders (consuming MCP clients); standardized way to handle authentication and resource discovery; future-proofs against changing model providers.
* *Cons:* Higher initial complexity to set up the first MCP servers compared to writing a raw Python function.

## Decision

We will adopt the **Model Context Protocol (MCP)** as the standard interoperability layer for all production agents in this architecture.

Agents should not directly import hardcoded tool libraries where possible; instead, they should connect to recognized MCP servers to discover available capabilities at runtime.

## Consequences

* **Positive:** Accelerates new agent development as they can instantly tap into existing MCP servers (e.g., a standardized "Enterprise Knowledge" MCP server); promotes reuse across the organization.
* **Negative:** Requires upskilling engineering teams on the MCP specification; necessitates running/maintaining standard MCP servers as infrastructure.
