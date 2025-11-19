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


