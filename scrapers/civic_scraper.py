from abc import ABC, abstractmethod
from scrapers.records import Municipality
import scrapers.webdriver
from scrapers.civic_logger import logger

class CivicScraper(ABC):

    def __init__(self, municipality : Municipality, url : str):
        self.municipality = municipality
        self.url = url
        self.driver = scrapers.webdriver.getChromeDriver()
        logger.info("Initialized scraper for " + str(municipality.city))
    
    @abstractmethod
    def scrape(self):
        pass