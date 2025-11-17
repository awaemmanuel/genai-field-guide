"""An e-commerce inventory checker agent that demonstrates metrics and monitoring."""

import logging
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.plugins.base_plugin import BasePlugin
from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.genai import types

# Configure logging
logging.basicConfig(level=logging.INFO)

class MetricsPlugin(BasePlugin):
    """A custom plugin that collects and reports metrics."""

    def __init__(self) -> None:
        """Initialize the plugin with counters."""
        super().__init__(name="metrics_plugin")
        self.agent_run_count: int = 0
        self.tool_call_count: int = 0
        self.model_request_count: int = 0

    async def before_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> None:
        """Count agent runs."""
        self.agent_run_count += 1

    async def before_tool_callback(
        self, *, agent: LlmAgent, callback_context: CallbackContext, tool_name: str
    ) -> None:
        """Count tool calls."""
        self.tool_call_count += 1

    async def before_model_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> None:
        """Count LLM requests."""
        self.model_request_count += 1

    def report_metrics(self):
        """Log the collected metrics."""
        logging.info(f"[Metrics] Agent runs: {self.agent_run_count}")
        logging.info(f"[Metrics] Tool calls: {self.tool_call_count}")
        logging.info(f"[Metrics] Model requests: {self.model_request_count}")


retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

def check_inventory(product_id: str) -> str:
    """Checks the inventory of a product.

    Args:
        product_id: The ID of the product.

    Returns:
        The inventory status of the product.
    """
    if product_id == "A123":
        return "In Stock"
    else:
        return "Out of Stock"


root_agent = LlmAgent(
    name="inventory_checker_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are an inventory checker agent. Your task is to check the inventory of a product.

    You MUST ALWAYS use the 'check_inventory' tool to check the inventory of a product.
    """,
        tools=[check_inventory],
)
    
    
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
