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

"""A basic ReAct agent that can use a search tool.

This module demonstrates the fundamental Reason+Act (ReAct) loop, a core pattern
in agentic architectures. The agent is given a prompt and a tool, and it
iteratively reasons about which tool to use, acts by calling the tool, and
observes the output until it can answer the user's question.
"""

from google.adk.agents import Agent
from google.adk.models import Gemini
from google.adk.tools import google_search
from google.genai import types

retry_options = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1.0,
    http_status_codes=[500, 502, 503, 504],
)

root_agent = Agent(
    name="basic_react_agent",
    model=Gemini(
      model="gemini-2.5-flash-lite",
      retry_options=retry_options,
    ),
    tools=[google_search],
    description="A simple react agent that can answer questions using a search tool",
    instruction="""You are a helpful assistant that can search for information.
        When you need to search for something, use the search tool.
        When you have the answer, respond to the user with the answer."""
)