from abc import ABC, abstractmethod
from records import Municipality
import scrapers.webdriver

class CivicScraper(ABC):

    def __init__(self, municipality : Municipality, url : str):
        self.municipality = municipality
        self.url = url
        self.driver = scrapers.webdriver.getChromeDriver()
    
    @abstractmethod
    def scrape(self):
        pass