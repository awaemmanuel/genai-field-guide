# Copyright 2025 Google LLC
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

"""A parallel execution of agents that work together to research a topic.

This module demonstrates a parallel orchestration pattern, where multiple agents
run concurrently to perform a task. This is useful for reducing latency by
running independent tasks in parallel.
"""

from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.models import Gemini
from google.genai import types

retry_options = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1.0,
    http_status_codes=[500, 502, 503, 504],
)

researcher_agent_1 = Agent(
    name="researcher_agent_1",
    description="Researches a topic and provides a summary of findings.",
    model=Gemini(
      model="gemini-2.5-flash-lite",
      retry_options=retry_options,
    ),
    instruction="""You are a researcher. You will be given a topic and you
        will research it and provide a summary of your findings.""",
)

researcher_agent_2 = Agent(
    name="researcher_agent_2",
    model=Gemini(
      model="gemini-2.5-flash-lite",
      retry_options=retry_options,
    ),
    instruction="""You are a researcher. You will be given a topic and you
        will research it and provide a summary of your findings.""",
)

aggregator_agent = Agent(
    name="aggregator_agent",
    description="Aggregates a list of research summaries into a single summary.",
    model=Gemini(
      model="gemini-2.5-flash-lite",
      retry_options=retry_options,
    ),
    instruction="""You are an aggregator. You will be given a list of research
        summaries and you will aggregate them into a single summary.""",
)

parallel_research_team = ParallelAgent(
    name="parallel_research_team",
    sub_agents=[researcher_agent_1, researcher_agent_2],
)

root_agent = SequentialAgent(
    name="research_system",
    sub_agents=[parallel_research_team, aggregator_agent],
)