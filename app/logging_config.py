import logging
import sys

def setup_logging():
    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Create handler for stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)

    # Create a formatting for the logs
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the root logger
    root_logger.addHandler(handler)

    # Prevent logs from being duplicated
    root_logger.propagate = False

    logging.info("Logging system initialized")