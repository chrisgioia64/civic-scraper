from abc import ABC, abstractmethod
import time
from scrapers.utils import write_to_csv, download_files, get_timestamp
from scrapers.antioch_scraper import AntiochScraper
from scrapers.walnut_creek_scraper import WalnutCreekScraper
from scrapers.brentwood_scraper import BrentwoodCreekScraper
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_logger(logger : logging.Logger, filename_suffix : str, level : int):
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    logs_folder = "logs"
    log_filename = f"{logs_folder}/{current_time}_{filename_suffix}.log"

    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

add_logger(logger, "main", logging.INFO)

scrapers = [
    AntiochScraper(), 
    WalnutCreekScraper(),
    BrentwoodCreekScraper()
] 

if __name__ == "__main__":
    for scraper in scrapers:
        municipality = scraper.municipality
        logger.info("Processing Municipality: " + str(municipality.city))
        start = time.time()
        scraper.scrape()
        elapsed1 = (time.time() - start)
        logger.info("Scrape Time: " + str(elapsed1))
        write_to_csv(municipality, "assets/" + municipality.city + " " + get_timestamp() + ".csv")
        download_files(municipality)
        elapsed2 = (time.time() - start)
        logger.info("Download Time: " + str(elapsed2 - elapsed1))

