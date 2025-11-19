import asyncio
import json
import os
import requests
import subprocess
import time
import uuid

from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from .product_catalog_agent import product_catalog_agent, PRODUCT_CATALOG_PORT
from .inventory_agent import inventory_agent, INVENTORY_PORT
from .shipping_agent import shipping_agent, SHIPPING_PORT
from .customer_support_agent import customer_support_agent

AGENT_CARD_WELL_KNOWN_PATH = "/.well-known/agent-card.json"

async def start_agent_server(agent, port: int, agent_name: str):
    """Starts an agent as a background A2A server."""
    a2a_app = to_a2a(agent, port=port)

    # Save the agent code to a temporary file for uvicorn
    agent_code = f"""import os
from google.adk.agents import LlmAgent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.models.google_llm import Gemini
from google.genai import types

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# --- Agent Specific Code ---
# This part needs to be dynamically generated or imported based on the agent
"""
    if agent_name == "product_catalog_agent":
        from .product_catalog_agent import get_product_info, product_catalog_agent as agent_instance
        agent_code += """def get_product_info(product_name: str) -> str:
    product_catalog = {
        "iphone 15 pro": "iPhone 15 Pro, $999, Low Stock (8 units), 128GB, Titanium finish",
        "samsung galaxy s24": "Samsung Galaxy S24, $799, In Stock (31 units), 256GB, Phantom Black",
        "dell xps 15": 'Dell XPS 15, $1,299, In Stock (45 units), 15.6" display, 16GB RAM, 512GB SSD',
        "macbook pro 14": 'MacBook Pro 14", $1,999, In Stock (22 units), M3 Pro chip, 18GB RAM, 512GB SSD',
        "sony wh-1000xm5": "Sony WH-1000XM5 Headphones, $399, In Stock (67 units), Noise-canceling, 30hr battery",
        "ipad air": 'iPad Air, $599, In Stock (28 units), 10.9" display, 64GB',
        "lg ultrawide 34": 'LG UltraWide 34" Monitor, $499, Out of Stock, Expected: Next week',
    }
    product_lower = product_name.lower().strip()
    if product_lower in product_catalog:
        return f"Product: {product_catalog[product_lower]}"
    else:
        available = ", ".join([p.title() for p in product_catalog.keys()])
        return f"Sorry, I don't have information for {product_name}. Available products: {available}"

agent_instance = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="product_catalog_agent",
    description="External vendor's product catalog agent that provides product information and availability.",
    instruction=\