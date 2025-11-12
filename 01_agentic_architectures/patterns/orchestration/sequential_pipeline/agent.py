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

"""A sequential pipeline of agents that work together to write a blog post.

This module demonstrates a sequential orchestration pattern, where the output of
one agent is passed as the input to the next. This is useful for deterministic
business processes where the steps are known and must be executed in a specific
order.
"""

from google.adk.agents import Agent, SequentialAgent
from google.adk.models import Gemini
from google.genai import types

retry_options = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1.0,
    http_status_codes=[500, 502, 503, 504],
)

outline_agent = Agent(
    name="outline_agent",
    description="Creates an outline for a blog post.",
    model=Gemini(
      model="gemini-2.5-flash-lite",
      retry_options=retry_options,
    ),
    instruction="""You are a blog post outliner. You will be given a topic and
        you will create an outline for a blog post on that topic.""",
    output_key="outline",
)

writer_agent = Agent(
    name="writer_agent",
    description="Writes a blog post based on an outline.",
    model=Gemini(
      model="gemini-2.5-flash-lite",
      retry_options=retry_options,
    ),
    instruction="""You are a blog post writer. You will be given an outline in the 'outline' state variable and
        you will write a blog post based on that outline.""",
    output_key="draft",
)

editor_agent = Agent(
    name="editor_agent",
    description="Edits a blog post for grammar, spelling, and clarity.",
    model=Gemini(
      model="gemini-2.5-flash-lite",
      retry_options=retry_options,
    ),
    instruction="""You are a blog post editor. You will be given a blog post in the 'draft' state variable and
        you will edit it for grammar, spelling, and clarity.""",
    output_key="final_draft",
)

root_agent = SequentialAgent(
    name="blog_pipeline",
    sub_agents=[outline_agent, writer_agent, editor_agent]
)