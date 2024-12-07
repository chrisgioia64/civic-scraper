from abc import ABC, abstractmethod
import time
from utils import write_to_csv, download_files, get_timestamp
from scrapers.antioch_scraper import AntiochScraper
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    start = time.time()
    antiochScraper = AntiochScraper()
    antiochScraper.scrape()
    elapsed1 = (time.time() - start)
    logger.info("Time to scrape: " + str(elapsed1))
    
    antiochMunicipality = antiochScraper.municipality

    write_to_csv(antiochMunicipality, "assets/antioch " + get_timestamp() + ".csv")
    download_files(antiochMunicipality)
    elapsed2 = (time.time() - start)
    logger.info("Time to download: " + str(elapsed2 - elapsed1))
    