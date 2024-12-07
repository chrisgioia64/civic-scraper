import time
from datetime import datetime, date, timedelta
from records import Municipality, CommitteeData, CommitteeMeeting, CommitteeFile
import logging

from scrapers.civic_scraper import CivicScraper
from scrapers.records import Municipality
import scrapers.webdriver as webdriver
import time
from selenium.webdriver.common.by import By

from scrapers.civic_logger import logger

class AntiochScraper(CivicScraper):

    def __init__(self):
        super().__init__(Municipality("Antioch", "Contra Costa", "California"), 
                         "https://www.antiochca.gov/government/agendas-and-minutes/")

    def scrape(self):
        try:
            self.driver.get(self.url)
            time.sleep(5)

            links = self.driver.find_elements(By.TAG_NAME, 'a')
            
            elements = self.driver.find_elements(By.CLASS_NAME, "vc_gitem-zone")
            
            links_map = {}
            for element in elements:
                inner_links = element.find_elements(By.TAG_NAME, 'a')
                for inner_link in inner_links:
                    if inner_link.text:
                        links_map[inner_link.text] = inner_link.get_attribute('href')
            
            idx = 0
            for key in links_map:
                idx += 1
                # if idx <= 15:
                #     continue
                logger.info("Processing " + str(key))
                committee = self.__scrape_committee(key, links_map[key])
                self.municipality.addCommittee(committee)
                
        finally:
            # Close the WebDriver
            self.driver.quit()
    
    def __scrape_committee(self, committee_name : str, committee_url : str) -> CommitteeData:
        commitee = CommitteeData(committee_name, committee_url)
        try:
            self.driver = webdriver.getChromeDriver()
            self.driver.get(committee_url)
            # time.sleep(5)
            
            # Special Case: for tabbed panes: this is only relevant for 
            # "Zoning Administrator" and the bottom of "City Council"
            # link_tabs_container = driver.find_elements(By.ID, "mk-tabs-9")
            link_tabs_container = self.driver.find_elements(By.CLASS_NAME, "mk-tabs")
            logger.info("link tabs " + str(len(link_tabs_container)))
            if len(link_tabs_container) == 1:
                tabs = link_tabs_container[0].find_elements(By.CLASS_NAME, "mk-tabs-tab")
                logger.info("Number of tabs " + str(len(tabs)))
                table_divs = link_tabs_container[0].find_elements(By.CLASS_NAME, "mk-fancy-table")    
                for idx, tab in enumerate(tabs):
                    tab.click()
                    table = table_divs[idx]
                    self.__scrape_table(table, commitee)
            
            # Normal Case -- Use the box-6 to find all panes
            box6s = self.driver.find_elements(By.ID, "box-6")
            if len(box6s) == 0:
                logger.info("No box-6 elements found")
                return commitee
            box6 = box6s[0]

            fancy_tables = box6.find_elements(By.CLASS_NAME, "mk-fancy-table")
            if len(fancy_tables) == 1:
                table = fancy_tables[0].find_elements(By.TAG_NAME, 'table')[0]
                # We only have a single table
                logger.info("single table")
                self.__scrape_table(table, commitee)
            elif len(fancy_tables) > 1:
                panels = self.driver.find_elements(By.CLASS_NAME, "vc_tta-panel")
                logger.info("Number of vc_tta-panel elements " + str(len(panels)))
                for idx, panel in enumerate(panels):
                    heading = panel.find_element(By.CLASS_NAME, "vc_tta-panel-heading")
                    if idx > 0:
                        heading.click()
                    else:
                        table = panel.find_element(By.CLASS_NAME, "mk-fancy-table")
                        if (table.text.strip() == ""):
                            heading.click()
                            time.sleep(1)
                        
                    logger.info("Processing panel " + str(idx))

                    tables = panel.find_elements(By.TAG_NAME, 'table')
                    for table in tables:
                        self.__scrape_table(table, commitee)

        finally:
            self.driver.quit()
        return commitee

    def __scrape_table(self, table, committee : CommitteeData) -> None:
        doc_keys = {}
        heading_keys = {'agenda', 'minutes', 'date', 'agenda-minutes'}
                
        rows = table.find_elements(By.TAG_NAME, 'tr')
        heading_row = rows[0]
        heading_tds = heading_row.find_elements(By.TAG_NAME, 'td')
        for idx, td in enumerate(heading_tds):
            for key in heading_keys:
                if 'agenda' in td.text.lower() and 'minutes' in td.text.lower():
                    doc_keys['agenda-minutes'] = idx
                    break
                elif key in td.text.lower():
                    doc_keys[key] = idx
                    break
                elif 'meeting' in td.text.lower():
                    doc_keys['date'] = idx

        if 'date' not in doc_keys:
            # Special case where we have no header row
            for idx, row in enumerate(rows):
                tds = row.find_elements(By.TAG_NAME, 'td')
                date = None
                for td in tds:
                    d = get_date(td.text.strip())
                    if d is not None:
                        date = d
                        break
                meeting = CommitteeMeeting(date)
                for td in tds:
                    links = td.find_elements(By.TAG_NAME, 'a')
                    if len(links) > 0:
                        if "agenda" in links[0].text.lower():
                            agenda_link = links[0].get_attribute('href')
                            agenda_file_name = links[0].text.strip()
                            file = CommitteeFile(agenda_file_name, agenda_link)
                            meeting.addAgenda(file)
                        if "minutes" in links[0].text.lower():
                            minutes_link = links[0].get_attribute('href')
                            minutes_file_name = links[0].text.strip()
                            file = CommitteeFile(minutes_file_name, minutes_link)
                            meeting.addMinutes(file)
                committee.addMeeting(meeting)

        else:
            # Normal case where we have a header row
            for idx, row in enumerate(rows[1:]):
                tds = row.find_elements(By.TAG_NAME, 'td')
                date = tds[doc_keys['date']]
                date_object = get_date(date.text.strip())
                if date_object is None:
                    continue

                meeting = CommitteeMeeting(date_object)

                if 'agenda' in doc_keys and doc_keys['agenda'] < len(tds):
                    agenda = tds[doc_keys['agenda']]
                    agenda_links = agenda.find_elements(By.TAG_NAME, 'a')
                    if len(agenda_links) > 0:
                        agenda_link = agenda_links[0].get_attribute('href')
                        agenda_file_name = agenda_links[0].text.strip()
                        file = CommitteeFile(agenda_file_name, agenda_link)
                        meeting.addAgenda(file)
                if 'minutes' in doc_keys and doc_keys['minutes'] < len(tds):
                    minutes = tds[doc_keys['minutes']]
                    minutes_links = minutes.find_elements(By.TAG_NAME, 'a')
                    if len(minutes_links) > 0:
                        minutes_link = minutes_links[0].get_attribute('href')
                        minutes_file_name = minutes_links[0].text.strip()
                        file = CommitteeFile(minutes_file_name, minutes_link)
                        meeting.addMinutes(file)
                if 'agenda-minutes' in doc_keys and doc_keys['agenda-minutes'] < len(tds):
                    agenda_minutes = tds[doc_keys['agenda-minutes']]
                    agenda_minutes_links = agenda_minutes.find_elements(By.TAG_NAME, 'a')
                    if len(agenda_minutes_links) > 0:
                        agenda_minutes_link = agenda_minutes_links[0].get_attribute('href')
                        agenda_minutes_file_name = agenda_minutes_links[0].text.strip()
                        file = CommitteeFile(agenda_minutes_file_name, agenda_minutes_link)
                        if 'agenda' in agenda_minutes_file_name.lower():
                            meeting.addAgenda(file)
                        if 'minutes' in agenda_minutes_file_name.lower():
                            meeting.addMinutes(file)
                committee.addMeeting(meeting)


def get_date(date_text):
    date_text = date_text.strip()
    date_object = get_date_format(date_text, "%m/%d/%y")
    if date_object is None:
        date_object = get_date_format(date_text, "%m/%d/%Y")
    if date_object is None:
        date_object = get_date_format(date_text, "%B %d, %Y")
    if date_object is None:
        print("Could not parse date: " + date_text)
    return date_object

def get_date_format(date_text, format):
    try:
        date_object = datetime.strptime(date_text, format).date()
        # print("parsed date " + str(date_object))
        return date_object
    except ValueError:
        return None


# if __name__ == "__main__":
#     start = time.time()
#     antioch = scrape_antioch()
#     elapsed1 = (time.time() - start)
#     print("Time to scrape: " + str(elapsed1))
#     write_to_csv(antioch, "assets/antioch " + get_timestamp() + ".csv")
#     download_files(antioch)
#     elapsed2 = (time.time() - start)
#     print("Time to download: " + str(elapsed2 - elapsed1))