import os
from dotenv import load_dotenv
from openai import OpenAI

import json

# Load environment variables from .env file
load_dotenv(dotenv_path="../1_hello_world/.env")

# Get the API key from environment
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)



def start_plan_output(
    user_task: str,
    model: str = "gpt-4o-mini",
    # "gpt-5-mini",
    max_steps: int = 5,
    temperature: float = 0.2
):
    """
    Returns a JSON object with:
      - start: one-line intent
      - plan: list of steps, each with {step, title, reasoning, action}
      - output: {summary, final_answer}
    """
    system_instructions = (
        "You are a senior assistant. Return JSON only.\n"
        "Provide concise, user-facing reasoning for each step (1–2 sentences). "
        "Do NOT include internal chain-of-thought or private notes.\n"
        "Keep steps actionable and minimal."
    )

    # 2) Define a JSON schema to enforce structure and concise reasoning.
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "start_plan_output_schema",
            "schema": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "start": {"type": "string", "minLength": 5, "maxLength": 200},
                    "plan": {
                        "type": "array",
                        "minItems": 1,
                        "maxItems": max_steps,
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "step": {"type": "integer", "minimum": 1},
                                "title": {"type": "string", "minLength": 3, "maxLength": 120},
                                "reasoning": {"type": "string", "minLength": 5, "maxLength": 220},
                                "action": {"type": "string", "minLength": 5, "maxLength": 500}
                            },
                            "required": ["step", "title", "reasoning", "action"]
                        }
                    },
                    "output": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "summary": {"type": "string", "minLength": 5, "maxLength": 600},
                            "final_answer": {"type": "string", "minLength": 0, "maxLength": 1000}
                        },
                        "required": ["summary"]
                    }
                },
                "required": ["start", "plan", "output"]
            }
        }
    }

    # 3) Make the API call.
    res = client.chat.completions.create(
        model=model,
        # temperature=temperature,
        messages=[
            {"role": "system", "content": system_instructions},
            {
                "role": "user",
                "content": (
                    "Task:\n"
                    f"{user_task}\n\n"
                    "Produce a Start → Plan → Output JSON.\n"
                    f"- Steps: <= {max_steps}\n"
                    "- Reasoning per step: 1–2 sentences (concise)\n"
                    "- No internal chain-of-thought; just short justifications."
                )
            }
        ],
        response_format=response_format
    )

    # 4) Parse JSON safely.
    content = res.choices[0].message.content
    try:
        payload = json.loads(content)
    except json.JSONDecodeError:
        # Fallback: wrap it if the model misbehaved
        payload = {"error": "Model did not return valid JSON", "raw": content}

    return payload


if __name__ == "__main__":
    # Example: change the task to whatever you need
    task = "give me step by step plant to solve the equation x^2 - 5x + 6 = 0"
    result = start_plan_output(task)
    print(json.dumps(result, indent=2, ensure_ascii=False))