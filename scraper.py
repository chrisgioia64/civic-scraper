from abc import ABC, abstractmethod
import time
from scrapers.utils import write_to_csv, download_files, get_timestamp
from scrapers.antioch_scraper import AntiochScraper
from scrapers.walnut_creek_scraper import WalnutCreekScraper
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scrapers = [
    AntiochScraper(), 
    WalnutCreekScraper()
] 

if __name__ == "__main__":
    for scraper in scrapers:
        start = time.time()
        scraper.scrape()
        elapsed1 = (time.time() - start)
        logger.info("Time to scrape: " + str(elapsed1))
        municipality = scraper.municipality
        logger.info("municipality: " + str(municipality))
        write_to_csv(municipality, "assets/" + municipality.city + " " + get_timestamp() + ".csv")
        download_files(municipality)
        elapsed2 = (time.time() - start)
        logger.info("Time to download: " + str(elapsed2 - elapsed1))

