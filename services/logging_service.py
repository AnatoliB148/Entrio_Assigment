import logging

# Configure logging with a timestamp
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def info(message):
    logging.info(message)

def error(message):
    logging.error(message)