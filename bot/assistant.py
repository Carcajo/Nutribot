from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
from vector_store import advice_vectors
import openai
from config import settings

openai.api_key = settings.OPENAI_API_KEY

llm = OpenAI(temperature=0)
qa = ConversationalRetrievalChain.from_llm(llm, advice_vectors.as_retriever())


async def get_answer(query):
    result = await qa.run(query)
    return result