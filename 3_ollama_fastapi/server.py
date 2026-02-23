from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../1_hello_world/.env")

app = FastAPI()

# Load OpenAI API key from .env
api_key = os.getenv("OPENAI_API_KEY")
#use below line to connect to ollama
client = OpenAI(api_key=api_key)

# Local Ollama client - connects to Ollama running in Docker container
local_ollama_client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")




# Request model for user message
class Message(BaseModel):
    user_message: str

# Simple GET route
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# GET route with parameter
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# POST route
@app.post("/items/")
def create_item(name: str, price: float):
    return {"name": name, "price": price}

# OpenAI endpoint - responds to user messages
@app.post("/chat/")
def chat_with_openai(message: Message):
    """
    Send a message to OpenAI and get a response.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": message.user_message}
            ],
            max_tokens=500
        )
        
        return {
            "user_message": message.user_message,
            "ai_response": response.choices[0].message.content
        }
    except Exception as e:
        return {"error": str(e)}


# Local Ollama endpoint - responds to user messages using local Ollama in Docker
@app.post("/chat_with_local_ollama/")
def chat_with_local_ollama(message: Message):
    """
    Send a message to local Ollama model running in Docker container and get a response.
    """
    try:
        response = local_ollama_client.chat.completions.create(
            model="mistral",
            messages=[
                {"role": "user", "content": message.user_message}
            ],
            max_tokens=500
        )
        
        return {
            "user_message": message.user_message,
            "ai_response": response.choices[0].message.content,
            "model": "mistral (local Ollama)"
        }
    except Exception as e:
        return {"error": str(e)}
        

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
