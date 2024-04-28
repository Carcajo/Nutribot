from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import openai
from config import settings

openai.api_key = settings.OPENAI_API_KEY

embeddings = OpenAIEmbeddings()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

with open("advice.docx") as f:
    advice_text = f.read()

advice_docs = text_splitter.split_text(advice_text)
advice_vectors = FAISS.from_texts(advice_docs, embeddings)