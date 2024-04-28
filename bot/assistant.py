from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from config import settings
import openai

openai.api_key = settings.OPENAI_API_KEY

embeddings = OpenAIEmbeddings()
advice_vectors = FAISS.load_local("advice_vectors", embeddings)

llm = OpenAI(temperature=0)
qa = ConversationalRetrievalChain.from_llm(llm, advice_vectors.as_retriever())


async def get_answer(query, user_id):
    metadata = {"user_id": user_id}
    result = await qa.run(query, metadata=metadata)
    return result


async def save_target(user, target):
    texts = [f"Моя цель: {target}"]
    metadatas = [{"user_id": user.id, "target": target}]
    await advice_vectors.add_texts(texts, metadatas)
