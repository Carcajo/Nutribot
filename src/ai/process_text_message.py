from typing import Optional
from dataclasses import dataclass
from openai import AsyncAssistantEventHandler
import dotenv
from openai import AsyncOpenAI
import json

from openai.types.beta.threads import TextContentBlock
from .check_goal import check_goal

client = AsyncOpenAI(api_key=dotenv.get_key(".env", key_to_get="OPENAI_API_KEY"))
ASSISTANT_ID = "asst_hoqPgqhBg8YFBsozHNZu8DhO"


class EventHandler(AsyncAssistantEventHandler):
    def __init__(self):
        super().__init__()
        self.response = ""
        self.goal = None

    async def on_message_done(self, message) -> None:
        assert isinstance(message.content[0], TextContentBlock)
        message_content = message.content[0].text
        self.response = message_content.value 

    async def on_event(self, event):
        if event.event == 'thread.run.requires_action':
            data = event.data
            assert data.required_action is not None

            tool_outputs = []
            for tool in data.required_action.submit_tool_outputs.tool_calls:
                self.goal = json.loads(tool.function.arguments)["goal"]

                if tool.function.name == "save_target":
                    tool_outputs.append({"tool_call_id": tool.id, "output": "Ok"})
                await self.submit_tool_outputs(tool_outputs)

    async def submit_tool_outputs(self, tool_outputs):
        assert self.current_run is not None

        event_handler = EventHandler()
        async with client.beta.threads.runs.submit_tool_outputs_stream(
                thread_id=self.current_run.thread_id,
                run_id=self.current_run.id,
                tool_outputs=tool_outputs,
                event_handler=event_handler
                ) as stream:
            await stream.until_done()
        self.response = event_handler.response
        self.goal = self.goal or event_handler.goal

    async def on_tool_call_created(self, tool_call):
        pass
        # print("==============================")
        # print(f"\nassistant > {tool_call.type}\n", flush=True)
        # print(tool_call)


@dataclass
class ProcessResponse:
    response: str
    goal: Optional[str]
    openai_thread_id: str


async def process_text_message(openai_thread_id: Optional[str], message: str, goal: Optional[str]) -> ProcessResponse:
    if openai_thread_id is None:
        thread = await client.beta.threads.create(
                messages=[{
                    "role": "user",
                    "content": message,
                    }]
                )
    else:
        thread = await client.beta.threads.retrieve(openai_thread_id)
        await client.beta.threads.messages.create(
                thread_id=openai_thread_id,
                role="user",
                content=message)

    event_handler = EventHandler()
    async with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID,
            instructions="Look for information only in the advice.docx file. Do not mention advice.docx file.",
            event_handler=event_handler,
    ) as stream:
        await stream.until_done()

    if event_handler.goal is not None and await check_goal(event_handler.goal):
        goal = event_handler.goal

    return ProcessResponse(event_handler.response or "😊", event_handler.goal or goal, thread.id)
