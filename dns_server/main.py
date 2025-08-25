import socket

DNS_PORT = 53

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(("", DNS_PORT))
        print(f"DNS server listening on port {DNS_PORT}")

        try:
            while True:
                data, addr = s.recvfrom(512)  # DNS messages are typically up to 512 bytes
                print(f"Received DNS query from {addr}")
        except KeyboardInterrupt:
                print("Shutting down DNS server.")
        finally:
                s.close()


if __name__ == "__main__":
    main()