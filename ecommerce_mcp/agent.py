import os
import json
import requests
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

MCP_URL = "http://127.0.0.1:8000/api/mcp/"


def call_mcp(tool_name, arguments):
    payload = {"tool": tool_name, "arguments": arguments}

    response = requests.post(MCP_URL, json=payload)
    return response.json()


while True:
    user_input = input("You: ")

    prompt = f"""
You are an e-commerce AI assistant.

If a tool is needed, respond ONLY valid JSON:

{{
  "tool": "search_products",
  "arguments": {{
      "q": "Laptop"
  }}
}}

Available tools:
search_products
check_stock
track_order
place_order
cancel_order

User request: {user_input}
"""

    response = client.models.generate_content(
        model="gemini-flash-latest", contents=prompt
    )

    text = response.text.strip()

    try:
        data = json.loads(text)

        result = call_mcp(data["tool"], data["arguments"])

        final = client.models.generate_content(
            model="gemini-flash-latest",
            contents=f"""
User request: {user_input}

Tool result:
{result}

Write a helpful natural language response.
""",
        )

        print("Bot:", final.text)

    except:
        print("Bot:", text)
