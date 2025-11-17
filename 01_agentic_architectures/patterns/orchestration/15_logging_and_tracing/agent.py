"""A flight status checker agent that demonstrates logging and tracing."""

import logging
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types

# Configure logging
logging.basicConfig(level=logging.INFO)

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

def get_flight_status(flight_number: str) -> str:
    """Gets the status of a given flight.

    Args:
        flight_number: The flight number to check.

    Returns:
        The status of the flight.
    """
    logging.info(f"Checking status of flight: {flight_number}")
    if flight_number == "UA123":
        return "On Time"
    elif flight_number == "DL456":
        return "Delayed"
    else:
        return "Flight not found"


root_agent = LlmAgent(
    name="flight_status_checker_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""Your task is to check the status of a flight.

    You MUST ALWAYS use the 'get_flight_status' tool to check the flight status.
    """,
    tools=[get_flight_status],
)


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
