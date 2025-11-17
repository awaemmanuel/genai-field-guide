"""An agent that demonstrates LLM-as-a-judge evaluation for code generation."""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# Code Generation Agent
code_generation_agent = LlmAgent(
    name="code_generation_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are a code generation agent. Your task is to write a Python function based on the user's prompt.""",
)

# LLM-as-a-Judge Agent
code_reviewer_agent = LlmAgent(
    name="code_reviewer_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are a code reviewer agent. Your task is to evaluate a Python function based on the following criteria:
    - Correctness
    - Readability
    - Efficiency

    Provide a score from 1 to 10 for each criterion and an overall score.
    """,
)


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

