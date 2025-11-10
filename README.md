# Generative AI Engineering: The Field Guide

> **A compendium of architectural patterns, design decisions, and reference implementations for applied GenAI engineering.**

## Mission

This repository distills insights gained from years of architecting large-scale enterprise systems into a living knowledge base. It bridges the gap between theoretical GenAI concepts and the pragmatic realities of enterprise engineering.

The artifacts housed here are curated not just to show *how* something works, but *why* specific architectural decisions are made in production environments.

## Current Focus: Agentic Systems

The repository is currently focused on **Autonomous Agent Architectures**, synthesizing learnings from advanced intensives (including the Google 5-Day Agent workshop) into reusable engineering patterns.

| Module | Focus Area | Key Patterns & Technologies |
| :--- | :--- | :--- |
| **01** | **Foundations & Orchestration** | Reasoning loops (ReAct), Multi-Agent orchestration. |
| **02** | **Tooling & Interoperability** | Idiomatic Function Calling, Model Context Protocol (MCP). |
| **03** | **State Management** | Episodic vs. Semantic memory, long-running thread persistence. |
| **04** | **Production Engineering** | Evaluation frameworks (Evals), observability, and tracing. |

---

## Repository Structure

This "Field Guide" is organized by architectural domain rather than by specific courses or tutorials.

```text
/
├── 01_agentic_architectures/  # <-- ACTIVE: Current focus area
│   ├── patterns/              # Reusable core patterns (e.g., A2A orchestration)
│   ├── reference_impls/       # End-to-end POCs and Capstone projects
│   └── workshops/             # Raw materials from specific intensives (e.g., Google 5-Day)
├── 02_rag_and_retrieval/      # (Planned) Advanced RAG patterns
├── field_notes/               # Architectural Decision Records (ADRs) & deep dives
└── mentorship_resources/      # General guides and career artifacts for mentees
```


## How to Use This Repository

Start by reviewing the **`field_notes/`** for foundational architectural concepts and decision records before diving into the code in **`reference_impls/`**.


## Philosophy

* **Opinionated by Experience:** The code here reflects specific choices suited for high-scale, production-grade environments, particularly on Google Cloud.
* **Patterns over Frameworks:** Emphasis is placed on understanding the underlying architectural pattern rather than just the framework implementing it.


## Stay Updated

New field notes, architectural patterns, and workshop modules are added frequently.

* **⭐ Star** this repository to show support and improve its visibility.
* **👁️ Watch** this repository to get notified of major content updates.
* [**Follow me on LinkedIn**](https://www.linkedin.com/in/emmanuelawa/) for broader discussions on GenAI engineering.

## About the Author

**Emmanuel Awa** is a Staff GenAI Architect at Google, specializing in large-scale enterprise adoption of intelligent, autonomous systems.
