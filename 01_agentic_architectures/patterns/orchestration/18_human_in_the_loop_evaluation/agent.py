"""An agent that demonstrates human-in-the-loop evaluation for financial transaction categorization."""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

def get_transaction_details(transaction_id: str) -> str:
    """Gets the details of a financial transaction.

    Args:
        transaction_id: The ID of the transaction.

    Returns:
        The details of the transaction.
    """
    if transaction_id == "T123":
        return "Merchant: Starbucks, Amount: 5.50"
    else:
        return "Transaction not found."


root_agent = LlmAgent(
    name="transaction_categorizer_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are a financial transaction categorizer. Your task is to suggest a category for a transaction.

    You MUST ALWAYS use the 'get_transaction_details' tool to get the transaction details.
    """,
    tools=[get_transaction_details],
)


"""Runner for the human-in-the-loop evaluation for financial transaction categorization."""

import asyncio
from google.adk.runners import InMemoryRunner
from .agent import root_agent

async def main():
    """Runs the agent and gets human feedback."""
    runner = InMemoryRunner(agent=root_agent)

    # 1. Get category suggestion from the agent
    prompt = "What is the category for transaction T123?"
    suggestion_response = await runner.run_debug(prompt)
    suggestion = suggestion_response["text"]
    print(f"Agent's Suggestion:\n{suggestion}")

    # 2. Get human feedback
    print("\nPlease provide your feedback on the suggestion.")
    feedback = input("Is the suggestion correct? (yes/no): ")

    if feedback.lower() == "yes":
        print("Thank you for your feedback. The category is confirmed.")
    else:
        correction = input("Please provide the correct category: ")
        print(f"Thank you for your feedback. The category has been corrected to: {correction}")

if __name__ == "__main__":
    asyncio.run(main())

