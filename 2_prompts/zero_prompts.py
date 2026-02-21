import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv(dotenv_path="../1_hello_world/.env")

# Get the API key from environment
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = "you should only answer coding related questions do not answer any thing else. your name is alexa. If user ask something else just say sorry"

# Make a simple API call
message = client.chat.completions.create(
    model="gpt-5-mini",
    max_completion_tokens=1024,
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "how are you?"}
        
    ]
)

# Print the response
print(message.choices[0].message.content)