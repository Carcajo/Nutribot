from openai import OpenAI
import dotenv
from openai import AssistantEventHandler

from bot_responses import *

client = OpenAI(api_key=dotenv.get_key(".env", key_to_get="OPENAI_API_KEY"))


def save_target(user_id: int, target) -> bool:
    try:
        if not validate_target(target):
            return False
        print(f"Цель '{target}' для пользователя {user_id}")
        return True
    except Exception as e:
        print(f"Ошибка: {e}")
        return False
    finally:
        print("penis")


def validate_target(target: str) -> bool:
    try:
        if len(target) > 100:
            return False
        response = client.completions.create(
            model="gpt-4-turbo",
            prompt= f"Проверь, подходит ли следующая целевая информация: {target}",
            max_tokens=1,
            n=1,
            stop=None,
            temperature=0.5,
        )
        if response.choices[0].text.strip().lower() == "yes":
            return True
        else:
            return False
    except Exception as e:
        print(f"Ошибка валидации {e}")
        return False

vector_store = client.beta.vector_stores.create(name="Food advice")
file_paths = ["advice.docx"]
file_streams = [open(path, "rb") for path in file_paths]

assistant = client.beta.assistants.create(
    name="TODO TEST REMOVEME Weightloss assistant",
    instructions="Answer the weight loss questions using the file_search tool using only the Nutritionist Bot's advice from the advice.docx file, quoting only word for word. Limit yourself to 3 points.If the question is not related to food, weight loss, weight gain or weight maintenance, then answer it with, Sorry, only ask questions on the topic of nutrition. Answer in Russian.",
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


file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=file_streams
)

message_file = client.files.create(
  file=open("advice.docx", "rb"), purpose="assistants"
)
thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": "Как набрать вес?",
            "attachments": [
                {"file_id": message_file.id, "tools": [{"type": "file_search"}]}
            ],
        }
    ],
)

print(thread.tool_resources.file_search)
print(thread.id)


class EventHandler(AssistantEventHandler):
    def on_message_done(self, message) -> None:
        message_content = message.content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(
                annotation.text, f"[{index}]"
            )
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        print(message_content.value)
        print("\n".join(citations))


    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)


with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Please address the user as Jane Doe. Look for information only in the advice.docx file",
        event_handler=EventHandler(),
) as stream:
    stream.until_done()
