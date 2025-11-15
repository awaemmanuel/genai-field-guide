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
Demonstrates context compaction for a financial news analyst agent.

This pattern shows how `EventsCompactionConfig` can be used for an agent that
analyzes financial news over a long conversation. As the conversation grows,
the agent automatically summarizes the history, allowing it to maintain context
about market trends and user interests without exceeding the context window.
"""

import os

from google.adk.agents import LlmAgent
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.models.google_llm import Gemini
from google.adk.sessions import DatabaseSessionService
from google.genai import types

# Ensure the GOOGLE_API_KEY environment variable is set.
if "GOOGLE_API_KEY" not in os.environ:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")

# 1. Initialize the Model with retry configuration
retry_config = types.HttpRetryOptions(attempts=3)
model = Gemini(model="gemini-pro", retry_options=retry_config)

# 2. Initialize the Agent
compaction_agent = LlmAgent(
    model=model,
    name="financial_news_analyst",
    description="A financial analyst that can discuss market trends and news over a long conversation.",
    instruction="You are a financial news analyst. You can discuss market trends, analyze articles, and maintain a long-running conversation about the user's financial interests.",
)

# 3. Define the Application with Context Compaction
root_app = App(
    name="financial_analyst_app",
    root_agent=compaction_agent,
    events_compaction_config=EventsCompactionConfig(
        compaction_interval=5,  # Trigger compaction every 5 turns
        overlap_size=2,  # Keep the last 2 turns for context
    ),
)

# 4. Initialize the persistent Session Service
db_url = "sqlite:///my_financial_analyst.db"
session_service = DatabaseSessionService(db_url=db_url)
