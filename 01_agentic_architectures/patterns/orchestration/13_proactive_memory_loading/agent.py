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
Demonstrates proactive knowledge loading using the `preload_memory` tool.

This pattern showcases how an agent can automatically load relevant information
from its long-term memory into its context before every turn. The `preload_memory`
tool ensures that the agent always has access to pertinent past knowledge,
making it suitable for highly personalized or context-dependent interactions.

Use Case: A "Personalized Learning Assistant" that uses `preload_memory` to
proactively load a student's learning history and preferences into the agent's
context before every interaction, ensuring highly personalized guidance.
"""

import os

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.tools import preload_memory
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

# 4. Initialize the Agent with the preload_memory tool
root_agent = LlmAgent(
    model=model,
    name="personalized_learning_assistant",
    instruction="You are a personalized learning assistant. You will proactively use your memory to provide tailored guidance based on the student's learning history and preferences.",
    tools=[
        preload_memory  # Agent now has access to Memory and will preload it before each turn!
    ],
)
