"""An agent that demonstrates LLM-as-a-judge evaluation for code generation."""

from google.adk.agents import LlmAgent, SequentialAgent
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

root_agent = SequentialAgent(
    name="CodeGenerationAndReviewPipeline",
    sub_agents=[code_generation_agent, code_reviewer_agent],
)


