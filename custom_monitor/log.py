import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(file_path = None, logger_name="custom_monitor"):
    
    # Log level from env variable (by default INFO)
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

    # Create folder if doesn't exist
    log_dir = os.path.dirname(file_path)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    # Create Main Logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    
    # Stop the duplicates
    logger.propagate = False

    # Convert WARNING in WARN
    logging.addLevelName(logging.WARNING, "WARN")

    if not logger.handlers:
        # Formater with datetime
        formatter = logging.Formatter(
            f"%(asctime)s  %(levelname)s {logger_name}: %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S.000000Z",
        )

        # ============================================================
        # CONSOLE HANDLER
        # ============================================================
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # ============================================================
        # FILE HANDLER
        # ============================================================
        file_handler = RotatingFileHandler(
            file_path,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger