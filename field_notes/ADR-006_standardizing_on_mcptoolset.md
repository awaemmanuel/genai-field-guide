# ADR-006: Standardizing on `McpToolset` for MCP Integration

**Status:** Accepted  
**Date:** 2025-11-12  
**Author:** Emmanuel Awa  
**Tags:** [Agentic, Tooling, MCP, ADK]  

## Context

While ADR-002 established our decision to adopt the Model Context Protocol (MCP) for tool interoperability, it did not specify the precise method for integrating MCP servers with our ADK-based agents. A consistent approach is needed.

## Decision

We will standardize on using the `McpToolset` class from the Agent Development Kit (ADK) to connect to and consume tools from external MCP servers.

## Alternatives Considered

### 1. Manual HTTP clients

Building our own clients to interact with MCP servers.

* *Pros:* No dependency on a specific library.
* *Cons:* High-effort, error-prone, and would not leverage the benefits of the ADK framework.

### 2. Other MCP client libraries

Using non-ADK MCP client libraries, which would require writing custom integration code.

* *Pros:* Potentially more feature-rich than the ADK's built-in toolset.
* *Cons:* Requires writing custom integration code; might not be compatible with the ADK's event model.

## Consequences

* **Positive:** This provides a standardized, ADK-native way to integrate MCP tools, simplifying agent development by abstracting away the complexities of the MCP protocol.
* **Negative:** This approach tightly couples our MCP integration strategy to the ADK's `McpToolset`. Any limitations or bugs in `McpToolset` will directly impact our agents.
