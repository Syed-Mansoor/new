import os
import sys
import logging
from datetime import datetime

# Define the log format
logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s]"

# Define the log directory
log_dir = 'logs'

# Generate a timestamp for the log file name
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Create the log file path with the timestamp
log_filepath = os.path.join(log_dir, f'Diamond_{timestamp}.log')

# Create the log directory if it doesn't exist
os.makedirs(log_dir, exist_ok=True)

# Configure the logging settings
logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        logging.FileHandler(log_filepath),   # Log to file
        logging.StreamHandler(sys.stdout)    # Log to console
    ]
)

# Create a logger instance
logger = logging.getLogger('Diamond')
