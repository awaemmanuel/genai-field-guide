"""Runner for the recipe finder agent."""

import asyncio
from google.adk.runners import InMemoryRunner
from .agent import root_agent, ToolCountPlugin

async def main():
    """Runs the agent."""
    tool_count_plugin = ToolCountPlugin()
    runner = InMemoryRunner(
        agent=root_agent,
        plugins=[
            tool_count_plugin
        ],
    )

    response = await runner.run_debug("Find a recipe for chocolate chip cookies")
    print(response)

    tool_count_plugin.report_tool_calls()

if __name__ == "__main__":
    asyncio.run(main())
