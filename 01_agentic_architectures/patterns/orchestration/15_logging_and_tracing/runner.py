"""Runner for the flight status checker agent."""

import asyncio
from google.adk.runners import InMemoryRunner
from google.adk.plugins.logging_plugin import LoggingPlugin
from .agent import root_agent

async def main():
    """Runs the agent."""
    runner = InMemoryRunner(
        agent=root_agent,
        plugins=[
            LoggingPlugin()
        ],
    )

    response = await runner.run_debug("What is the status of flight UA123?")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
