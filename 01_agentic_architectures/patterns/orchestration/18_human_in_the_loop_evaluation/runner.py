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

