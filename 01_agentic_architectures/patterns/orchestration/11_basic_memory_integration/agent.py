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
Demonstrates basic memory integration with manual session data ingestion.

This pattern showcases how to initialize a `MemoryService` and manually transfer
session data into long-term memory using `add_session_to_memory()`. This is the
foundational step for enabling agents to recall information across multiple
conversations.

Use Case: A "Customer Preference Tracker" agent that manually stores user
preferences (e.g., dietary restrictions, favorite brands) from a conversation
into long-term memory.
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

# 1. Initialize the Model with standard retry configuration
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1.0,
    http_status_codes=[500, 502, 503, 504],
)
model = Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config)

# 2. Initialize the Memory Service
# For this basic demonstration, we use InMemoryMemoryService.
# For production, VertexAiMemoryBankService would be used.
memory_service = InMemoryMemoryService()

# 3. Initialize the Session Service
session_service = InMemorySessionService()

# 4. Initialize the Agent
root_agent = LlmAgent(
    model=model,
    name="customer_preference_tracker",
    instruction="You are a customer preference tracker. Your goal is to understand and store user preferences.",
)
