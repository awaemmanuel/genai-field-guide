"""Runner for the agent deployment pattern."""

import os
from .agent import KnowledgeBaseTool, CustomerServiceAgent, deploy_agent_to_vertex_ai

# Example Usage
customer_support_tool = KnowledgeBaseTool()
my_customer_agent = CustomerServiceAgent(
    name="SupportBot",
    description="An AI agent to assist customers with common queries.",
    tools=[customer_support_tool]
)

# Simulate deployment
# Replace with your actual GCP project ID and location
gcp_project_id = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
gcp_location = os.getenv("GCP_LOCATION", "us-central1")

if gcp_project_id == "your-gcp-project-id":
    print("WARNING: GCP_PROJECT_ID environment variable not set. Using placeholder.")
if gcp_location == "us-central1":
    print("WARNING: GCP_LOCATION environment variable not set. Using default 'us-central1'.")

deployment_result = deploy_agent_to_vertex_ai(my_customer_agent, gcp_project_id, gcp_location)
print("\nDeployment Result:")
print(deployment_result)

# Simulate agent interaction post-deployment
print("\nSimulating agent interaction:")
response = my_customer_agent.process_message("What is your return policy?")
print(response)

