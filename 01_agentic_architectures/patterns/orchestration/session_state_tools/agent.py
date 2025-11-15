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
Demonstrates using tools to manage a shopping cart in session state.

This pattern shows how an agent can use tools (`add_item_to_cart`, `view_cart`)
to modify a list of items stored in the session state. This is a common
paradigm for managing dynamic, structured data within a conversation, such as
maintaining a shopping cart, a list of tasks, or a configuration object.
"""

import os
from typing import Any, Dict, List

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.sessions import DatabaseSessionService
from google.adk.tools.tool_context import ToolContext
from google.genai import types

# Ensure the GOOGLE_API_KEY environment variable is set.
if "GOOGLE_API_KEY" not in os.environ:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")


def add_item_to_cart(
    tool_context: ToolContext, item: str, quantity: int
) -> Dict[str, Any]:
    """Adds an item to the shopping cart in the session state."""
    if "cart" not in tool_context.state:
        tool_context.state["cart"] = []

    # The state is a mutable list, so we can append to it directly.
    tool_context.state["cart"].append({"item": item, "quantity": quantity})
    return {"status": "success", "item": item, "quantity": quantity}


def view_cart(tool_context: ToolContext) -> Dict[str, Any]:
    """Retrieves the current contents of the shopping cart from the session state."""
    cart_items = tool_context.state.get("cart", [])
    return {"status": "success", "cart": cart_items}


# 1. Initialize the Model with retry configuration
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1.0,
    http_status_codes=[500, 502, 503, 504],
)
model = Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config)

# 2. Initialize the Agent with the shopping cart tools
root_agent = LlmAgent(
    model=model,
    name="shopping_cart_assistant",
    description="An assistant that helps users manage their shopping cart.",
    instruction="You are a shopping cart assistant. Use the `add_item_to_cart` tool to add items to the cart and the `view_cart` tool to show the user what is in their cart. Always confirm with the user after adding an item.",
    tools=[add_item_to_cart, view_cart],
)

# 3. Initialize the persistent Session Service
db_url = "sqlite:///my_shopping_cart.db"
session_service = DatabaseSessionService(db_url=db_url)
