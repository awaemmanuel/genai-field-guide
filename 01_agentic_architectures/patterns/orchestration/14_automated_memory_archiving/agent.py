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
Demonstrates automated memory archiving using callbacks.

This pattern showcases how to use an `after_agent_callback` to automatically
save session data to long-term memory after each agent turn. This ensures
continuous knowledge capture without manual intervention, making it ideal for
applications that require persistent and up-to-date memory.

Use Case: A "Meeting Minutes Generator" agent that automatically archives key
discussion points from a meeting (session) into long-term memory after each
turn, ensuring no important details are lost.
"""

import os

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.genai import types

# Ensure the GOOGLE_API_KEY environment variable is set.
if "GOOGLE_API_KEY" not in os.environ:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")


async def auto_save_to_memory(callback_context):
    """Automatically saves the current session to memory after each agent turn."""
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session
    )


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

# 4. Initialize the Agent with the auto-save callback
root_agent = LlmAgent(
    model=model,
    name="meeting_minutes_generator",
    instruction="You are a meeting minutes generator. You will automatically archive key discussion points from the conversation into long-term memory.",
    after_agent_callback=auto_save_to_memory,  # Saves after each turn!
)
