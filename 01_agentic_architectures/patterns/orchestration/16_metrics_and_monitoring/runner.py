"""Runner for the inventory checker agent."""

import asyncio
from google.adk.runners import InMemoryRunner
from .agent import root_agent, MetricsPlugin

async def main():
    """Runs the agent."""
    metrics_plugin = MetricsPlugin()
    runner = InMemoryRunner(
        agent=root_agent,
        plugins=[
            metrics_plugin
        ],
    )

    response = await runner.run_debug("Is product A123 in stock?")
    print(response)

    metrics_plugin.report_metrics()

if __name__ == "__main__":
    asyncio.run(main())