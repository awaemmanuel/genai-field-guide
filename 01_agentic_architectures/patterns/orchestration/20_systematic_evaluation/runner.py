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
