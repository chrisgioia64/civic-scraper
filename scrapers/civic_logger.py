import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("civic_scraper")


def add_logger(logger : logging.Logger, filename_suffix : str, level : int):
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    logs_folder = "logs"
    log_filename = f"{logs_folder}/{current_time}_{filename_suffix}.log"

    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    

add_logger(logger, "error", logging.ERROR)
add_logger(logger, "info", logging.INFO)
add_logger(logger, "debug", logging.DEBUG)
