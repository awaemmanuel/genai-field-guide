import os
from google.adk.agents import LlmAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH
from google.adk.models.google_llm import Gemini
from google.genai import types

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

# Define ports for the A2A agents
PRODUCT_CATALOG_PORT = 8001
INVENTORY_PORT = 8002
SHIPPING_PORT = 8003

# Create RemoteA2aAgent instances for each external agent
remote_product_catalog_agent = RemoteA2aAgent(
    name="product_catalog_agent",
    description="Remote product catalog agent from external vendor that provides product information.",
    agent_card=f"http://localhost:{PRODUCT_CATALOG_PORT}{AGENT_CARD_WELL_KNOWN_PATH}",
)

remote_inventory_agent = RemoteA2aAgent(
    name="inventory_agent",
    description="Remote inventory agent that provides stock levels and restocking schedules.",
    agent_card=f"http://localhost:{INVENTORY_PORT}{AGENT_CARD_WELL_KNOWN_PATH}",
)

remote_shipping_agent = RemoteA2aAgent(
    name="shipping_agent",
    description="Remote shipping agent that provides delivery estimates and tracking information.",
    agent_card=f"http://localhost:{SHIPPING_PORT}{AGENT_CARD_WELL_KNOWN_PATH}",
)

customer_support_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="customer_support_agent",
    description="A customer support assistant that helps customers with product inquiries, stock, and shipping.",
    instruction="""
    You are a friendly and professional customer support agent.
    
    When customers ask about products, stock, or shipping:
    1. Use the product_catalog_agent sub-agent to look up product information.
    2. Use the inventory_agent sub-agent to check stock levels and restocking schedules.
    3. Use the shipping_agent sub-agent to get delivery estimates or tracking information.
    4. Provide clear answers about pricing, availability, specifications, delivery, and tracking.
    5. If a product is out of stock, mention the expected availability.
    6. Be helpful and professional!
    
    Always get information from the relevant sub-agents before answering customer questions.
    """,
    sub_agents=[
        remote_product_catalog_agent,
        remote_inventory_agent,
        remote_shipping_agent,
    ],
)
