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

"""A human-in-the-loop pattern for long-running operations requiring approval."""

from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.adk.tools import FunctionTool, ToolContext
from google.adk.apps import App, ResumabilityConfig
from google.genai import types
import re

retry_options = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1.0,
    http_status_codes=[500, 502, 503, 504],
)

def post_to_social_media(
    content: str, tool_context: ToolContext
) -> dict:
    """Posts content to a social media platform. Requires approval for posts with images or links.

    Args:
        content: The text content to be posted.

    Returns:
        Dictionary with the post status.
    """
    has_image_or_link = bool(re.search(r'https?://\S+|[image]', content))

    # SCENARIO 1: Simple text post, auto-approve
    if not has_image_or_link:
        return {
            "status": "posted",
            "post_id": "123456789",
            "content": content,
            "message": "Content posted automatically.",
        }

    # SCENARIO 2: First call for a post with image/link, request approval
    if not tool_context.tool_confirmation:
        tool_context.request_confirmation(
            hint=f"⚠️ This post contains an image or link. Do you want to approve it?\n\nContent: {content}",
            payload={"content": content},
        )
        return {
            "status": "pending",
            "message": "This post requires approval because it contains an image or a link.",
        }

    # SCENARIO 3: Resuming after approval
    if tool_context.tool_confirmation.confirmed:
        return {
            "status": "posted",
            "post_id": "987654321",
            "content": content,
            "message": "Content posted after approval.",
        }
    else:
        return {
            "status": "rejected",
            "message": "The post was rejected.",
        }

social_media_agent = LlmAgent(
    name="SocialMediaAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_options),
    instruction="""You are a social media assistant.

  When users ask you to post content:
   1. Use the `post_to_social_media` tool with the content they provide.
   2. If the post status is 'pending', inform the user that approval is required.
   3. After receiving the final result, provide a clear summary including:
      - The status of the post (posted/rejected).
      - The post ID (if available).
      - The content that was posted.
   4. Keep your responses concise and informative.
  """,
    tools=[FunctionTool(func=post_to_social_media)],
)

root_agent = App(
    name="SocialMediaManager",
    root_agent=social_media_agent,
    resumability_config=ResumabilityConfig(is_resumable=True),
)