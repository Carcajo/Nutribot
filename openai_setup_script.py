import openai
from openai import OpenAI
import dotenv
from openai import AssistantEventHandler

client = OpenAI(api_key=dotenv.get_key(".env", key_to_get="OPENAI_API_KEY"))
#kek = openai.beta.vector_stores.list()
#print(kek)

#for ass in kek:
    #if ass.name == "Food advice":
        #print(openai.beta.vector_stores.delete(ass.id))
        #openai.beta.assistants.files.delete(ass.id)
        #openai.beta.assistants.delete(ass.id)
    #print(ass.name)

vector_store = client.beta.vector_stores.create(name="Food advice")
file_paths = ["advice.docx"]
file_streams = [open(path, "rb") for path in file_paths]

assistant = client.beta.assistants.create(
    name="sWeightloss assistant",
    instructions="Answer the nutrition questions using the file_search tool using only the Nutritionist Bot's advice from the advice.docx file, quoting only word for word. Limit yourself to 3 points. Don't mention the advice.docx file. If the question is not related to food, weight loss, weight gain or weight maintenance, then answer it with, 'Sorry, only ask questions on the topic of nutrition'",
    model="gpt-4-turbo",
    tools=[
       {"type": "file_search"},
       {"type": "function",
        "function": {
            "name": "save_target",
            "description": "Save the user's target",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The ID of the user",
                    },
                    "target": {
                        "type": "string",
                        "description": "The target to save",
                    },
                },
                "required": ["user_id", "target"],
            },
        },
        },
    ],
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)

print("Created assistant with ID: ", assistant.id)
