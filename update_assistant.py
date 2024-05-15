import openai
from openai import OpenAI
import dotenv
from openai import AssistantEventHandler

client = OpenAI(api_key=dotenv.get_key(".env", key_to_get="OPENAI_API_KEY"))

assistant_id = "asst_hoqPgqhBg8YFBsozHNZu8DhO"
assistant = client.beta.assistants.retrieve(assistant_id)
print(assistant.tools)
print(assistant)
client.beta.assistants.update(assistant_id, 
    instructions = "Add 3 exclamation marks in the end of every message.",
    tools=[
       {"type": "file_search"},
       {"type": "function",
        "function": {
            "name": "save_target",
            "description": "Save the user's target in nutrition",
        "parameters": {
          "type": "object",
          "properties": {
            "goal": {
              "type": "string",
              "description": "User goal, eg: 'lose weight'"
            },
          },
          "required": ["goal"]
        },
        }
       }])
