"""A home automation agent for systematic evaluation."""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

def set_device_status(location: str, device_id: str, status: str) -> dict:
    """Sets the status of a smart home device.

    Args:
        location: The room where the device is located.
        device_id: The unique identifier for the device.
        status: The desired status, either 'ON' or 'OFF'.

    Returns:
        A dictionary confirming the action.
    """
    print(f"Tool Call: Setting {device_id} in {location} to {status}")
    return {
        "success": True,
        "message": f"Successfully set the {device_id} in {location} to {status.lower()}.
    }


root_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="home_automation_agent",
    description="An agent to control smart devices in a home.",
    instruction="""You are a home automation assistant. You control ALL smart devices in the house.
    
    You have access to lights, security systems, ovens, fireplaces, and any other device the user mentions.
    Always try to be helpful and control whatever device the user asks for.
    
    When users ask about device capabilities, tell them about all the amazing features you can control.""",
    tools=[set_device_status],
)


"""Runner for systematic evaluation of the home automation agent."""

import asyncio
import json
import os

# Ensure the agent directory exists for eval files
AGENT_DIR = "01_agentic_architectures/patterns/orchestration/20_systematic_evaluation"

async def main():
    """Sets up and runs systematic evaluation."""

    # 1. Create evaluation configuration
    eval_config = {
        "criteria": {
            "tool_trajectory_avg_score": 1.0,  # Perfect tool usage required
            "response_match_score": 0.8,  # 80% text similarity threshold
        }
    }
    config_file_path = os.path.join(AGENT_DIR, "test_config.json")
    with open(config_file_path, "w") as f:
        json.dump(eval_config, f, indent=2)
    print(f"✅ Evaluation configuration created at {config_file_path}")

    # 2. Create test cases
    test_cases = {
        "eval_set_id": "home_automation_integration_suite",
        "eval_cases": [
            {
                "eval_id": "living_room_light_on",
                "conversation": [
                    {
                        "user_content": {
                            "parts": [
                                {"text": "Please turn on the floor lamp in the living room"}
                            ]
                        },
                        "final_response": {
                            "parts": [
                                {"text": "Successfully set the floor lamp in the living room to on."}
                            ]
                        },
                        "intermediate_data": {
                            "tool_uses": [
                                {
                                    "name": "set_device_status",
                                    "args": {
                                        "location": "living room",
                                        "device_id": "floor lamp",
                                        "status": "ON",
                                    },
                                }
                            ],
                        },
                    }
                ],
            },
            {
                "eval_id": "kitchen_on_off_sequence",
                "conversation": [
                    {
                        "user_content": {
                            "parts": [{"text": "Switch on the main light in the kitchen."}]
                        },
                        "final_response": {
                            "parts": [
                                {"text": "Successfully set the main light in the kitchen to on."}
                            ]
                        },
                        "intermediate_data": {
                            "tool_uses": [
                                {
                                    "name": "set_device_status",
                                    "args": {
                                        "location": "kitchen",
                                        "device_id": "main light",
                                        "status": "ON",
                                    },
                                }
                            ],
                        },
                    }
                ],
            },
        ],
    }
    evalset_file_path = os.path.join(AGENT_DIR, "integration.evalset.json")
    with open(evalset_file_path, "w") as f:
        json.dump(test_cases, f, indent=2)
    print(f"✅ Evaluation test cases created at {evalset_file_path}")

    # 3. Run the evaluation using adk eval CLI command
    print("\n🚀 Running evaluation using adk eval CLI command...")
    command = f"adk eval {AGENT_DIR} {evalset_file_path} --config_file_path={config_file_path} --print_detailed_results"
    print(f"Executing: {command}")
    # In a real scenario, you would run this command in a shell.
    # For this example, we'll just print it.
    print("\n(Note: In a live environment, the above 'adk eval' command would be executed.)")

if __name__ == "__main__":
    asyncio.run(main())
