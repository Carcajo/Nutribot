import dotenv
from openai import AsyncOpenAI
import json
import openai

from config import SETTINGS

client = openai.AsyncOpenAI(api_key=SETTINGS.OPENAI_API_KEY)


async def check_goal(goal: str) -> bool:
    messages = [{"role": "user", "content": f"Is this goal for weightloss valid?\n{goal}"}]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "is_goal_valid",
                "description": "Check if user goal is valid",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "is_ok": {
                            "type": "boolean",
                            "description": "True if goal is valid, for ex lose weight, False otherwise",
                        },
                    },
                    "required": ["is_ok"],
                },
            },
        }
    ]
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=messages,
        tools=tools,
        tool_choice="required",  # auto is default, but we'll be explicit
    )
    response_message = response.choices[0].message
    is_ok = None
    if response_message.tool_calls:
        available_functions = {
                "is_goal_valid": lambda x: x,
        }

        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            assert function_name == "is_goal_valid"
            is_ok = json.loads(tool_call.function.arguments)["is_ok"]
    assert is_ok is not None
    return is_ok
