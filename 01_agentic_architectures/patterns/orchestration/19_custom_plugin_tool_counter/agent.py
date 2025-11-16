"""A recipe finder agent that demonstrates a custom plugin for counting tool calls."""

import logging
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.plugins.base_plugin import BasePlugin
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.google_search_tool import google_search
from google.genai import types

# Configure logging
logging.basicConfig(level=logging.INFO)

class ToolCountPlugin(BasePlugin):
    """A custom plugin that counts tool calls."""

    def __init__(self) -> None:
        """Initialize the plugin with a counter."""
        super().__init__(name="tool_count_plugin")
        self.tool_call_count: int = 0

    async def before_tool_callback(
        self, *, agent: LlmAgent, callback_context: CallbackContext, tool_name: str
    ) -> None:
        """Count tool calls."""
        self.tool_call_count += 1

    def report_tool_calls(self):
        """Log the total number of tool calls."""
        logging.info(f"[Metrics] Total tool calls: {self.tool_call_count}")


retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)


root_agent = LlmAgent(
    name="recipe_finder_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are a recipe finder agent. Your task is to find recipes on a given topic.

    You MUST ALWAYS use the 'google_search' tool to find recipes.
    """,
    tools=[google_search],
)
