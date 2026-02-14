import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Make a simple API call
message = client.chat.completions.create(
    model="gpt-5-mini",
    max_completion_tokens=1024,
    messages=[
        {"role": "system", "content": "you are an maths assistant any only answer questions related to maths"},
        {"role": "user", "content": "how are you?"}
        
    ]
)

# Print the response
print(message.choices[0].message.content)