"""Runner for the LLM-as-a-judge evaluation for code generation."""

import asyncio
from google.adk.runners import InMemoryRunner
from .agent import root_agent

async def main():
    """Runs the agent."""
    runner = InMemoryRunner(agent=root_agent)
    response = await runner.run_debug("Write a Python function that calculates the factorial of a number.")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
