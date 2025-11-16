"""Runner for the LLM-as-a-judge evaluation for code generation."""

import asyncio
from google.adk.runners import InMemoryRunner
from .agent import code_generation_agent, code_reviewer_agent

async def main():
    """Runs the agents."""
    code_generator_runner = InMemoryRunner(agent=code_generation_agent)
    code_reviewer_runner = InMemoryRunner(agent=code_reviewer_agent)

    # 1. Generate code
    prompt = "Write a Python function that calculates the factorial of a number."
    code_response = await code_generator_runner.run_debug(prompt)
    code = code_response["text"]
    print(f"Generated Code:\n{code}")

    # 2. Judge the code
    evaluation_prompt = f"Please evaluate the following Python function:\n\n{code}"
    evaluation_response = await code_reviewer_runner.run_debug(evaluation_prompt)
    evaluation = evaluation_response["text"]
    print(f"\nCode Review:\n{evaluation}")

if __name__ == "__main__":
    asyncio.run(main())

