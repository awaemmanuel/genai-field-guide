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

"""A delegation pattern where a primary agent uses a specialist agent as a tool."""

from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool
from google.adk.models import Gemini
from google.genai import types

retry_options = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1.0,
    http_status_codes=[500, 502, 503, 504],
)

def create_jira_ticket(title: str, description: str, priority: str) -> dict:
    """Creates a Jira ticket with the given title, description, and priority.

    This is a mock tool that simulates creating a Jira ticket.

    Args:
        title: The title of the Jira ticket.
        description: The description of the Jira ticket.
        priority: The priority of the Jira ticket (e.g., "High", "Medium", "Low").

    Returns:
        A dictionary with the status and the ticket ID.
        Success: {"status": "success", "ticket_id": "PROJ-1234"}
        Error: {"status": "error", "error_message": "Failed to create Jira ticket"}
    """
    print(f"--- Creating Jira Ticket ---")
    print(f"Title: {title}")
    print(f"Description: {description}")
    print(f"Priority: {priority}")
    # In a real implementation, this would make an API call to Jira.
    # For this example, we'll just return a mock ticket ID.
    mock_ticket_id = "PROJ-1234"
    print(f"--- Mock Jira Ticket Created: {mock_ticket_id} ---")
    return {"status": "success", "ticket_id": mock_ticket_id}

jira_agent = LlmAgent(
    name="JiraAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_options),
    instruction="""You are a Jira specialist agent. Your sole purpose is to create Jira tickets using the `create_jira_ticket` tool.
You will be given the title, description, and priority for the ticket.
You must call the `create_jira_ticket` tool with the provided information.
Do not add any conversational text or explanations.
    """,
    tools=[create_jira_ticket],
)

root_agent = LlmAgent(
    name="CustomerSupportAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_options),
    instruction="""You are a customer support agent. Your goal is to help users by creating a Jira ticket for their issues.

1.  First, understand the user's issue.
2.  Gather the necessary information to create a Jira ticket: a title for the ticket, a detailed description of the issue, and the priority level (High, Medium, or Low).
3.  Once you have all the information, use the `JiraAgent` tool to create the ticket.
4.  Finally, confirm to the user that the ticket has been created and provide them with the ticket ID.
    """,
    tools=[
        AgentTool(agent=jira_agent),
    ],
)