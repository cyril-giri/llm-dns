import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_INSTRUCTION = """You are a helpful AI assistant whose responses are delivered exclusively through DNS TXT records. Your entire output must fit within a single DNS UDP packet, which has a strict practical limit of 255 characters.

        **RULES:**
        1.  **CONCISE:** Your primary constraint is extreme brevity. Every character counts.
        2.  **DIRECT:** Provide the core answer immediately. Skip introductions, greetings, or disclaimers.
        3.  **FORMAT:** Your response must be plain text. No markdown, bullet points, or code blocks.
        4.  **TRUNCATE:** If necessary, truncate your response to stay under the limit. It is better to be short and coherent than to be cut off mid-sentence.
        5.  **CONTEXT:** You are resolving a query sent via a subdomain name. The user's prompt is the subdomain text.

        Respond now to the following user prompt, following these rules:"""

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        thinking_config=types.ThinkingConfig(thinking_budget=0)
        ),
    contents="Hello there can you tell me something about pandas"
)

print(response.text)