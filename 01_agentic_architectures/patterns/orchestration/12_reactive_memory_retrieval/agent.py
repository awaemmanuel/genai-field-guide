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

"""
Demonstrates reactive knowledge retrieval using the `load_memory` tool.

This pattern showcases how an agent can explicitly decide when to search its
long-term memory for relevant information. The `load_memory` tool is provided
to the agent, and the agent's instruction guides it to use this tool only when
it needs to recall past context to answer a query.

Use Case: A "Technical Support Agent" that uses `load_memory` to reactively
search a knowledge base (memory) only when it needs to answer a specific
technical question that requires past context.
"""

import os

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.tools import load_memory
from google.genai import types

# Ensure the GOOGLE_API_KEY environment variable is set.
if "GOOGLE_API_KEY" not in os.environ:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")

# 1. Initialize the Model with standard retry configuration
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1.0,
    http_status_codes=[500, 502, 503, 504],
)
model = Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config)

# 2. Initialize the Memory Service
memory_service = InMemoryMemoryService()

# 3. Initialize the Session Service
session_service = InMemorySessionService()

# 4. Initialize the Agent with the load_memory tool
root_agent = LlmAgent(
    model=model,
    name="technical_support_agent",
    instruction="You are a technical support agent. Use the `load_memory` tool if you need to recall past information to answer a technical question. If you don't find relevant information, state that you don't know.",
    tools=[
        load_memory  # Agent now has access to Memory and can search it whenever it decides to!
    ],
)
