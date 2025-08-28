import os
import socket
from google import genai
from google.genai import types
from dnslib import DNSRecord, QTYPE, RR, TXT
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DNS_PORT = 53
SUBDOMAIN = "llm.cyrilgiri.work."
SYSTEM_INSTRUCTION = """You are a helpful AI assistant whose responses are delivered exclusively through DNS TXT records. Your entire output must fit within a single DNS UDP packet, which has a strict practical limit of 255 characters.

        **RULES:**
        1.  **CONCISE:** Your primary constraint is extreme brevity. Every character counts.
        2.  **DIRECT:** Provide the core answer immediately. Skip introductions, greetings, or disclaimers.
        3.  **FORMAT:** Your response must be plain text. No markdown, bullet points, or code blocks.
        4.  **TRUNCATE:** If necessary, truncate your response to stay under the limit. It is better to be short and coherent than to be cut off mid-sentence.
        5.  **CONTEXT:** You are resolving a query sent via a subdomain name. The user's prompt is the subdomain text.

        Respond now to the following user prompt, following these rules:"""


def generate_response(prompt):
    response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        max_output_tokens=100,
        temperature=0.7,
        thinking_config=types.ThinkingConfig(thinking_budget=0)
        ),
    contents="" + prompt
    )
    return response.text

def handle_dns_query(data, addr, sock):
    request = DNSRecord.parse(data)
    qname = str(request.q.qname)
    qtype = QTYPE[request.q.qtype]
    
    # print(f"Received query for {qname} with type {qtype} from {addr}")
    
    if not qname.endswith(f"{SUBDOMAIN}") or qtype != "TXT":
        print(f"query dropped for {qname} with type {qtype}")
        return
    
    prompt = qname.replace(f".{SUBDOMAIN}", "").replace(".", " ").replace("_", " ").replace("-", " ")
    print(f"Received prompt: {prompt}")
    response = generate_response(prompt)  # Placeholder for actual response generation
    
    reply = request.reply()
    reply.add_answer(RR(qname, QTYPE.TXT, rdata=TXT(response), ttl=300))
    sock.sendto(reply.pack(), addr)
    print(f"Sent TXT response to {addr} for {qname}")
    return

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(("", DNS_PORT))
        print(f"DNS server listening on port {DNS_PORT}")

        try:
            while True:
                data, addr = s.recvfrom(512)  # DNS messages are typically up to 512 bytes
                print(f"Received DNS query from {addr}")
                try:
                    handle_dns_query(data, addr, s)
                except Exception as e:
                    print(f"Error handling DNS query: {e}")
        except KeyboardInterrupt:
                print("\nShutting down DNS server.")
        finally:
                s.close()


if __name__ == "__main__":
    main()