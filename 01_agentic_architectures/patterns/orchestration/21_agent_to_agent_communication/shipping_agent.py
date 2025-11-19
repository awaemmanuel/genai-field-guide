from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

def get_delivery_estimate(product_name: str, destination: str) -> str:
    """Get the delivery estimate for a given product to a specific destination.

    Args:
        product_name: Name of the product.
        destination: The shipping destination (e.g., 'New York', 'California').

    Returns:
        Delivery estimate as a string.
    """
    delivery_data = {
        "iphone 15 pro": {"new york": "3-5 business days", "california": "2-3 business days"},
        "samsung galaxy s24": {"new york": "2-4 business days", "california": "1-2 business days"},
        "macbook pro 14": {"new york": "4-6 business days", "california": "3-4 business days"},
    }

    product_lower = product_name.lower().strip()
    destination_lower = destination.lower().strip()

    if product_lower in delivery_data and destination_lower in delivery_data[product_lower]:
        return f"Delivery estimate for {product_name} to {destination}: {delivery_data[product_lower][destination_lower]}"
    else:
        return f"Delivery estimate not available for {product_name} to {destination}"


def get_tracking_info(order_id: str) -> str:
    """Get tracking information for a given order ID.

    Args:
        order_id: The ID of the order.

    Returns:
        Tracking information as a string.
    """
    tracking_data = {
        "ORD123": "Shipped, estimated delivery Nov 20th",
        "ORD456": "In transit, estimated delivery Nov 22nd",
    }

    order_id_upper = order_id.upper().strip()

    if order_id_upper in tracking_data:
        return f"Tracking for order {order_id}: {tracking_data[order_id_upper]}"
    else:
        return f"Tracking information not found for order {order_id}"

shipping_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="shipping_agent",
    description="Agent that provides delivery estimates and tracking information.",
    instruction="""
    You are a shipping specialist. Your task is to provide delivery estimates and tracking information for orders.
    Use the get_delivery_estimate tool for delivery estimates and get_tracking_info for tracking information.
    """,
    tools=[get_delivery_estimate, get_tracking_info],
)
