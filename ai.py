from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="env.vars")
api_key = os.environ.get('API_KEY')
if not api_key:
    raise ValueError("API_KEY not found in environment variables. Make sure ai/env.vars exists and does not use quotes around the value.")

os.environ['GROQ_API_KEY'] = api_key
client = Groq(api_key=api_key)
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain of fast language models in 1 word",
        }
    ],
    model="llama-3.3-70b-versatile",
    stream=False,
)

print(chat_completion.choices[0].message.content)