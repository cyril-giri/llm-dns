import os
from dotenv import load_dotenv
load_dotenv()

# env loading
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash-lite")

# dns server config
DNS_PORT = 53
SUBDOMAIN = "llm.cyrilgiri.work."

# system instruction for the LLM
SYSTEM_INSTRUCTION = """You are a helpful AI assistant whose responses are delivered exclusively through DNS TXT records. Your entire output must fit within a single DNS UDP packet, which has a strict practical limit of 255 characters.

        **RULES:**
        1.  **CONCISE:** Your primary constraint is extreme brevity. Every character counts.
        2.  **DIRECT:** Provide the core answer immediately. Skip introductions, greetings, or disclaimers.
        3.  **FORMAT:** Your response must be plain text. No markdown, bullet points, or code blocks.
        4.  **TRUNCATE:** If necessary, truncate your response to stay under the limit. It is better to be short and coherent than to be cut off mid-sentence.
        5.  **CONTEXT:** You are resolving a query sent via a subdomain name. The user's prompt is the subdomain text.

        Respond now to the following user prompt, following these rules:"""