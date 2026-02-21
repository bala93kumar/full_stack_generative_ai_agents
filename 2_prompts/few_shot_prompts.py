import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv(dotenv_path="../1_hello_world/.env")

# Get the API key from environment
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = """you are helpful assistant 

Rule : 
- Strictly give output in json format


Examples : 
Q: if your are asked any thing other than coding related questions
A : just say I can only answer coding related questions 

Q : can you explain a + b whole square 
A : give a python code to do the same
"""


# Make a simple API call
message = client.chat.completions.create(
    model="gpt-5-mini",
    max_completion_tokens=1024,
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "what is a +  b whole square?"}
        
    ]
)

# Print the response
print(message.choices[0].message.content)