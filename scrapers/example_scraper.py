from scrapers.civic_scraper import CivicScraper
from scrapers.records import Municipality, CommitteeData, CommitteeMeeting, CommitteeFile
from scrapers.webdriver import webdriver
from civic_logger import logger

class ExampleCityScraper(CivicScraper):
    def __init__(self):
        super().__init__(Municipality("City Name", "County Name", "State Name"), 
                         "https://www.someurl.com"
                         )
    
    def scrape(self):
        # TODO: Implement this method
        # At the end of this method, `self.municipality` should have all the data scraped