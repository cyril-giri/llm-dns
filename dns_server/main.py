import socket
from dnslib import DNSRecord, QTYPE, RR, TXT

DNS_PORT = 53
SUBDOMAIN = "llm.cyrilgiri.work"

def handle_dns_query(data, addr, sock):
    request = DNSRecord.parse(data)
    qname = str(request.q.qname)
    qtype = QTYPE[request.q.qtype]
    
    print(f"Received query for {qname} with type {qtype} from {addr}")
    
    if qname.endswith(f"{SUBDOMAIN}.") and qtype == "TXT":
        reply = request.reply()
        reply.add_answer(RR(qname, QTYPE.TXT, rdata=TXT("Hello heheh!"), ttl=1))
        sock.sendto(reply.pack(), addr)
        print(f"Sent TXT response to {addr} for {qname}")
    else:
        print(f"query dropped for {qname} with type {qtype}")
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