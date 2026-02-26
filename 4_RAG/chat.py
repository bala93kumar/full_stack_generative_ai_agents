import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

# 1) Load environment and configure OpenAI
load_dotenv(dotenv_path="../1_hello_world/.env")
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is missing. Check your ../1_hello_world/.env")

client = OpenAI(api_key=api_key)  # or: client = OpenAI() if your env is set

# 2) Embeddings config (ensure your Qdrant collection was created with same embedding dims)
embeddings = OpenAIEmbeddings(model="text-embedding-3-large", dimensions=512)

# 3) Connect to existing Qdrant collection
vecto_db = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    url="http://localhost:6333",
    prefer_grpc=True,          # requires Qdrant started with gRPC; set False if unsure
    collection_name="nodejs_book_1"
)

# 4) Take user query
user = input("Enter your query: ")

# 5) Similarity search
search_result = vecto_db.similarity_search(user, k=3)

# Optional: Quick debug to see metadata keys you actually have
for i, doc in enumerate(search_result, 1):
    print(f"[DEBUG] Hit {i} metadata keys:", list(doc.metadata.keys()))

# 6) Build context safely, with fallbacks for missing keys
def fmt_doc(doc):
    md = doc.metadata or {}
    page = md.get("page_number") or md.get("page") or md.get("pageIndex") or "N/A"
    src = md.get("source") or md.get("file_path") or md.get("path") or "N/A"
    # Trim content a bit to avoid huge prompts (optional)
    content = doc.page_content.strip()
    return (
        f"Page Number: {page}\n"
        f"File Location: {src}\n"
        f"Page Content:\n{content}"
    )

context = "\n\n---\n\n".join(fmt_doc(doc) for doc in search_result)

SYSTEM_PROMPT = (
    "You are a helpful assistant for answering questions about NodeJS.\n"
    "Use ONLY the provided context to answer the question.\n"
    "If the answer isn't in the context, say you don't know and point the user to the page to read more.\n\n"
    f"Context:\n{context}\n"
)

# 7) Chat completion
responses = client.chat.completions.create(
    model="gpt-5-mini",
    max_completion_tokens=1024,
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user}
    ]
)

print(f"\nResponse:\n{responses.choices[0].message.content}")