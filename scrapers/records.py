from scrapers.civic_logger import logger

class Municipality:
    def __init__(self, city, county, state):
        self.city = city
        self.county = county
        self.state = state
        self.committees = []
    
    def addCommittee(self, committee):
        self.committees.append(committee)
    
    def getJsonData(self):
        data = []
        for committee in self.committees:
            for meeting in committee.meetings:
                if meeting.agenda is not None:
                    data.append({
                        "place": self.city,
                        "place_name": self.county,
                        "state_or_province": self.state,
                        "meeting_date": meeting.date.strftime("%Y-%m-%d"),
                        "meeting_time": "",
                        "committee_name": committee.name,
                        "meeting_id" : "",
                        "asset_name" : "",
                        "asset_type" : "agenda",
                        "url" : meeting.agenda.file_url,
                        "scraped_by" : "Marc-Scraper",
                        'content-type' : '',
                        'content-length' : ''
                    })
                if meeting.minutes is not None:
                    data.append({
                        "place": self.city,
                        "place_name": self.county,
                        "state_or_province": self.state,
                        "meeting_date": meeting.date.strftime("%Y-%m-%d"),
                        "meeting_time": "",
                        "committee_name": committee.name,
                        "meeting_id" : "",
                        "asset_name" : "",
                        "asset_type" : "minutes",
                        "url" : meeting.minutes.file_url,
                        "scraped_by" : "Marc-Scraper",
                        'content-type' : '',
                        'content-length' : ''
                    })
        return data

class CommitteeData:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.meetings = []

    def addMeeting(self, meeting):
        self.meetings.append(meeting)
    
    def printInformation(self):
        logger.info("Committee: " + self.name)
        logger.info("URL: " + self.url)
        logger.info("Meetings:")
        for meeting in self.meetings:
            logger.info("   Date: " + str(meeting.date))
            if meeting.agenda is not None:
                logger.info("   Agenda: " + meeting.agenda.file_name + " URL: " + meeting.agenda.file_url)
            if meeting.minutes is not None:
                logger.info("   Minutes: " + meeting.minutes.file_name + " URL: " + meeting.minutes.file_url)
            print("")

class CommitteeMeeting:
    def __init__(self, date):
        self.date = date
        self.agenda = None
        self.minutes = None

    def addAgenda(self, agenda):
        self.agenda = agenda
    
    def addMinutes(self, minutes):
        self.minutes = minutes

class CommitteeFile:
    def __init__(self, file_name, file_url):
        self.file_name = file_name
        self.file_url = file_url