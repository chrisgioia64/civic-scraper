
from typing import List
from scrapers.civic_logger import logger
from scrapers.civic_scraper import CivicScraper
from scrapers.records import Municipality, CommitteeData, CommitteeMeeting, CommitteeFile
import scrapers.webdriver as webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime, date, timedelta
from selenium.common.exceptions import WebDriverException
import scrapers.utils as utils

def get_date_time(date_text):
    s = date_text.split("@")
    date = s[0].strip()
    print(f"date: {date}")
    return get_date(date)

def get_date(date_text):
    date_text = date_text.strip()
    s = "Monday, December 02, 2024 @ 5:00 PM"
    date_object = get_date_format(date_text, "%m/%d/%y")
    if date_object is None:
        date_object = get_date_format(date_text, "%A, %B %d, %Y")
    if date_object is None:
        date_object = get_date_format(date_text, "%b %d, %Y")
    if date_object is None:
        date_object = get_date_format(date_text, "%m/%d/%Y")
    if date_object is None:
        date_object = get_date_format(date_text, "%B %d, %Y")
    if date_object is None:
        logger.error("Could not parse date: " + date_text)
    return date_object

def get_date_format(date_text, format):
    try:
        date_object = datetime.strptime(date_text, format).date()
        # print("parsed date " + str(date_object))
        return date_object
    except ValueError:
        return None



class BrentwoodCreekScraper(CivicScraper):
    def __init__(self):
        super().__init__(Municipality("Brentwood", "Contra Costa", "California"), 
                         "https://www.brentwoodca.gov/government/meeting-information"
                         )
    def __scrape__link(self, links : List[WebElement]):
        logger.debug("   Scraping links " + str(len(links)))
        candidate_link = None
        candidate_link_type = None
        for link in links:
            content_type = utils.get_content_type(link.get_attribute("href"))
            logger.debug("        Link: " + link.text + ", content type: " + str(content_type))
            if content_type == "application/pdf" or  "text/html" in content_type:
                if candidate_link is None:
                    candidate_link = link
                    candidate_link_type = content_type
                elif "text/html" in candidate_link_type and content_type == "application/pdf":
                    candidate_link = link
                    candidate_link_type = content_type
                elif "text/html" in candidate_link_type and "text/html" in content_type:
                    candidate_link = link
                    candidate_link_type = content_type
        return candidate_link


    def __scrape_committee(self, committee : CommitteeData, committee_element : WebElement, committee_name : str):
        meetings = committee_element.find_elements(By.CLASS_NAME, "meeting-content")
        logger.info("Committee: " + str(committee.name))
        logger.debug("Number of meetings " + str(len(meetings)))
        for meeting in meetings:
            date_div = meeting.find_element(By.CLASS_NAME, "meeting-date")
            date_text = date_div.text
            parsed_date = get_date_time(date_text)
            logger.debug("   Meeting " + str(parsed_date))

            committee_meeting = CommitteeMeeting(parsed_date)

            links = meeting.find_elements(By.TAG_NAME, "a")
            link = self.__scrape__link(links)
            if link != None:
                committee_meeting.addAgenda(CommitteeFile(link.text, link.get_attribute("href")))
            else:
                logger.error("No link found for " + str(committee.name) + " on " + str(parsed_date))

            committee.addMeeting(committee_meeting) 

    def scrape(self):
        try:
            self.driver = webdriver.getChromeDriver(headless=False)
            self.driver.get(self.url)
    
            time.sleep(3)

            self.driver.execute_script("window.scrollTo(0, 1500);")

            time.sleep(2)

            frames = self.driver.find_elements(By.TAG_NAME, 'iframe')
            self.driver.switch_to.frame(frames[0])

            topElement = self.driver.find_element(By.ID, "PastMeetingTypesAccordian")
            accordionElements = topElement.find_elements(By.CLASS_NAME, "MeetingTypeList")

            for accordion in accordionElements:
                link = accordion.find_element(By.CLASS_NAME, "PastMeetingTypesName")
                committee_name = link.text
                link.click()
                time.sleep(2)

                committee = CommitteeData(committee_name, self.url)
                self.__scrape_committee(committee, accordion, committee_name)
                self.municipality.addCommittee(committee)

            
        finally:
            # Close the WebDriver
            self.driver.quit()