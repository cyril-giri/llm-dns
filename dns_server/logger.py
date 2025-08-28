import logging

# Configure logging
logging.basicConfig(
    filename="dns_server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_info(message: str) -> None:
    logging.info(message)

def log_error(message: str) -> None:
    logging.error(message)
