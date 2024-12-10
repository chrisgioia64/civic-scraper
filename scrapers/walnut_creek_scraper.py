
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


def get_date(date_text):
    date_text = date_text.strip()
    date_object = get_date_format(date_text, "%m/%d/%y")
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


class WalnutCreekScraper(CivicScraper):
    def __init__(self):
        super().__init__(Municipality("Walnut Creek", "Contra Costa", "California"), 
                         "https://www.walnutcreekca.gov/government/public-meeting-agendas-and-videos"
                         )
    
    def __scrape_committee(self, committee : CommitteeData, committee_element : WebElement, committee_name : str):
        tabs = committee_element.find_elements(By.CLASS_NAME, "TabbedPanelsTab")
        for tab in tabs:
            try:
                tab.click()
                logger.info("   Clicking on " + str(tab.text))
            except Exception as e:
                logger.error("   Clicking on tab for committee " + str(committee.name) + " failed ")
                logger.error("   Tab text: " + str(e))
            time.sleep(1)
            TabbedPanelsContentVisible = committee_element.find_element(By.CLASS_NAME, "TabbedPanelsContentVisible")
            self.__scrape_committee_year_table(committee, TabbedPanelsContentVisible, committee_name)

        
    def __scrape_committee_year_table(self, committee : CommitteeData, content_element : WebElement, committee_name : str):
        table = content_element.find_element(By.TAG_NAME, "table")
        tbody = table.find_element(By.TAG_NAME, "tbody")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            tds = row.find_elements(By.TAG_NAME, "td")
            if len(tds) < 4:
                # Sometimes a year has no records and there is text that says "No records" or something similar
                continue
            date = tds[1].text
            parsed_date = get_date(date)
            
            try:
                link_element = tds[3].find_element(By.TAG_NAME, "a")
                committee_meeting = CommitteeMeeting(parsed_date)
                file = CommitteeFile(link_element.text, link_element.get_attribute("href"))
                if "agenda" in link_element.text.lower():
                    committee_meeting.addAgenda(file)
                if "minutes" in link_element.text.lower():
                    committee_meeting.addMinutes(file)

                committee.addMeeting(committee_meeting)

            except NoSuchElementException as e:
                logger.info("No link found")

    def scrape(self):
        try:
            self.driver = webdriver.getChromeDriver(headless=False)
            self.driver.get(self.url)
    
            time.sleep(3)

            # Scroll down the page
            self.driver.execute_script("window.scrollTo(0, 1700);")
            time.sleep(2)  # Wait for the page to load after scrolling

            # Switch to the iframe
            iframe = self.driver.find_element(By.ID, 'cvIframe')
            self.driver.switch_to.frame(iframe)

            time.sleep(2)

            elements = self.driver.find_elements(By.CLASS_NAME, "CollapsiblePanel")
            logger.info("# of elements: " + str(len(elements)))

            for element in elements:
                collapsiblePanelTab = element.find_element(By.CLASS_NAME, "CollapsiblePanelTab")
                element.click()
                # time.sleep(1)
                title = element.find_element(By.CLASS_NAME, "CollapsiblePanelTab").text
                logger.info("Title: " + title)

                committee = CommitteeData(title, self.url)
                content = element.find_element(By.CLASS_NAME, "CollapsiblePanelContent")
                self.__scrape_committee(committee, content, title)
                scroll_script = "window.scrollBy(0, 500);"
                # self.driver.execute_script(scroll_script)

                self.municipality.addCommittee(committee)
        finally:
            # Close the WebDriver
            self.driver.quit()