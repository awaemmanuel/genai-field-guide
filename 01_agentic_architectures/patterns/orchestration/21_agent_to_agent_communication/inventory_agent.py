from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

def get_stock_level(product_name: str) -> str:
    """Get the stock level and restocking schedule for a given product.

    Args:
        product_name: Name of the product.

    Returns:
        Stock level and restocking schedule as a string.
    """
    stock_data = {
        "iphone 15 pro": "Low Stock (8 units), Next restock: 2 days",
        "samsung galaxy s24": "In Stock (31 units)",
        "dell xps 15": "In Stock (45 units)",
        "macbook pro 14": "In Stock (22 units)",
        "sony wh-1000xm5": "In Stock (67 units)",
        "ipad air": "In Stock (28 units)",
        "lg ultrawide 34": "Out of Stock, Expected: Next week",
    }

    product_lower = product_name.lower().strip()

    if product_lower in stock_data:
        return f"Stock for {product_name}: {stock_data[product_lower]}"
    else:
        return f"Stock information not available for {product_name}"

inventory_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="inventory_agent",
    description="Agent that provides stock levels and restocking schedules.",
    instruction="""
    You are an inventory specialist. Your task is to provide stock levels and restocking schedules for products.
    Always use the get_stock_level tool to fetch inventory data.
    """,
    tools=[get_stock_level],
)
