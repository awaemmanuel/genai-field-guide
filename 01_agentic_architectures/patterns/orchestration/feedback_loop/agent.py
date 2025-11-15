# Copyright 2025 Emmanuel Awa
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A feedback loop between a worker and a critic agent.

This module demonstrates a feedback loop pattern, where a critic agent provides
feedback to a worker agent, which then refines its work. This is useful for
iteratively improving the quality of an agent's output.
"""

from google.adk.agents import Agent, LoopAgent, SequentialAgent
from google.adk.models import Gemini
from google.adk.tools import FunctionTool
from google.genai import types

retry_options = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1.0,
    http_status_codes=[500, 502, 503, 504],
)

def exit_loop():
    """Call this function ONLY when the critique is 'APPROVED', indicating the story is finished and no more changes are needed."""
    return {"status": "approved", "message": "Story approved. Exiting refinement loop."}


initial_writer_agent = Agent(
    name="InitialWriterAgent",
    description="Writes the first draft of a short story.",
    model=Gemini(
      model="gemini-2.5-flash-lite",
      retry_options=retry_options,
    ),
    instruction="""You are a writer. You will be given a topic and you will
        write a short story on that topic.""",
    output_key="current_story",
)

critic_agent = Agent(
    name="CriticAgent",
    description="Provides feedback on a short story.",
    model=Gemini(
      model="gemini-2.5-flash-lite",
      retry_options=retry_options,
    ),
    instruction="""You are a critic. You will be given a short story and you
        will provide feedback on it. If the story is good enough, you will
        say 'APPROVED'. Otherwise, you will provide feedback on how to improve
        it.""",
    output_key="critique",
)

refiner_agent = Agent(
    name="RefinerAgent",
    description="Refines a short story based on critique.",
    model=Gemini(
      model="gemini-2.5-flash-lite",
      retry_options=retry_options,
    ),
    instruction="""You are a story refiner. You have a story draft and critique.
    
    Story Draft: {current_story}
    Critique: {critique}
    
    Your task is to analyze the critique.
    - IF the critique is EXACTLY "APPROVED", you MUST call the `exit_loop` function and nothing else.
    - OTHERWISE, rewrite the story draft to fully incorporate the feedback from the critique.""",
    output_key="current_story",
    tools=[
        FunctionTool(exit_loop)
    ],
)

story_refinement_loop = LoopAgent(
    name="StoryRefinementLoop",
    sub_agents=[critic_agent, refiner_agent],
    max_iterations=2,
)

root_agent = SequentialAgent(
    name="StoryPipeline",
    sub_agents=[initial_writer_agent, story_refinement_loop],
)
