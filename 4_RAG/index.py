# Example indexing (run once when creating the collection)
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from langchain_openai import OpenAIEmbeddings

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables from .env file
load_dotenv(dotenv_path="../1_hello_world/.env")

# Get the API key from environment
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

loader = PyPDFLoader(r"C:\Users\balak\Downloads\nodeJsBook.pdf")
docs = loader.load()  # each Document should have metadata like {"source": "...", "page": N}

# If not present, add what you need:
for d in docs:
    d.metadata["page_number"] = d.metadata.get("page", d.metadata.get("pageIndex", None))
    d.metadata["source"] = d.metadata.get("source", "path/to/book.pdf")

splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
chunks = splitter.split_documents(docs)

client = QdrantClient(url="http://localhost:6333")
store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=OpenAIEmbeddings(model="text-embedding-3-large", dimensions=512),
    collection_name="nodejs_book_1",
    url="http://localhost:6333",
    prefer_grpc=True,
)