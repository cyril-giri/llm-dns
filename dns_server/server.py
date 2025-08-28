import socket
from dnslib import DNSRecord, QTYPE, RR, TXT
from .config import SUBDOMAIN , DNS_PORT
from .llm_handler import generate_response

def extract_prompt(qname: str) -> str:
    """
    Extract and clean the prompt from a DNS query name.
    
    Args:
        qname: The full DNS query name
        
    Returns:
        str: Cleaned prompt text
    """
    # Remove the subdomain and clean the prompt
    base_prompt = qname.replace(f".{SUBDOMAIN}", "")
    clean_prompt = base_prompt.replace(".", " ").replace("_", " ").replace("-", " ")
    return clean_prompt

def handle_dns_query(data: bytes, addr: tuple, sock: socket.socket) -> None:
    """
    Handle an incoming DNS query.
    
    Args:
        data: Raw DNS query data
        addr: Client address tuple (ip, port)
        sock: UDP socket for sending response
    """
    try:
        request = DNSRecord.parse(data)
        qname = str(request.q.qname)
        qtype = QTYPE[request.q.qtype]
        
        # Validate query type and target domain
        if not qname.endswith(SUBDOMAIN) or qtype != "TXT":
            print(f"Dropped query: {qname} ({qtype})")
            return
        
        # Extract and process prompt
        prompt = extract_prompt(qname)
        print(f"Processing prompt: {prompt}")
        
        # Generate response
        response = generate_response(prompt)
        
        # Build and send DNS response
        reply = request.reply()
        reply.add_answer(RR(qname, QTYPE.TXT, rdata=TXT(response), ttl=300))
        sock.sendto(reply.pack(), addr)
        
        print(f"Sent response to {addr[0]}:{addr[1]}")
        
    except Exception as e:
        print(f"Error handling query from {addr}: {e}")

def start_server(port: int = DNS_PORT) -> None:
    """
    Start the DNS server.
    
    Args:
        port: UDP port to listen on
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(("", port))
        print(f"DNS server listening on port {port}")
        
        try:
            while True:
                data, addr = sock.recvfrom(512)
                print(f"Received query from {addr[0]}:{addr[1]}")
                handle_dns_query(data, addr, sock)
                
        except KeyboardInterrupt:
            print("\nShutting down server gracefully")
        except Exception as e:
            print(f"Server error: {e}")