#!/usr/bin/env python3
"""
LLM DNS Server - Main entry point.
"""
from dns_server.server import start_server
from dns_server.config import DNS_PORT

if __name__ == "__main__":
    start_server(DNS_PORT)