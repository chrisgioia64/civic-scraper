import requests
import os
from records import Municipality, CommitteeData, CommitteeMeeting, CommitteeFile
import csv
import datetime
import logging

import requests
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def download_file(url, dest):
    response = requests.get(url, stream=True)
    with open(dest, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)

urls = [
    ('https://example.com/file1', 'file1.txt'),
    ('https://example.com/file2', 'file2.txt'),
]

with ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(lambda u: download_file(*u), urls)    


def download_files(municipality : Municipality):
    """
    Downloads all files associated with this municipality
    """
    logging.info("Downloading files for " + str(municipality.city))
    ls = []
    for committee in municipality.committees:
        logging.info("Downloading files for committee " + str(committee.name))
        for meeting in committee.meetings:
            # __download_meeting(municipality, committee, meeting)
            ls.append((municipality, committee, meeting))
    
    with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust `max_workers` as needed
        executor.map(lambda u: __download_meeting(*u), ls)

def __download_meeting(municipality : Municipality, committee : CommitteeData, 
                 meeting : CommitteeMeeting):
    """
    Downloads the files associated with a committee meeting which may include 
    agenda and minutes
    """
    committee_name = committee.name.replace("/","_")
    dir = "download/" + municipality.county + "/" + municipality.city + "/" + committee_name + "/"
    s = dir + municipality.city + "_" + committee_name + "_" + meeting.date.strftime("%Y_%m_%d")
    
    os.makedirs(dir, exist_ok=True)
    if meeting.agenda is not None:
        filename = s + "_agenda." + file_extension(meeting.agenda.file_url)
        download_file(meeting.agenda.file_url, filename)
    if meeting.minutes is not None:
        filename = s + "_minutes." + file_extension(meeting.minutes.file_url)
        download_file(meeting.minutes.file_url, filename)

def download_file(url, local_filename):
    """
    Downloads a file from a URL and saves it to the local file system
    """
    with requests.get(url, stream=True) as response:
        try:
            response.raise_for_status()  # Check if the request was successful
            with open(local_filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
    
        except requests.HTTPError as e:
            logging.error(f"Failed to download {url}: {e}")
        
def file_extension(url : str):
    local_filename = url.split('/')[-1]
    extension = local_filename.split('.')[-1]
    return extension

def write_to_csv(municipality : Municipality, filename):
    """ Writes the data for a municipality to a csv file"""
    logging.info("Writing csv for " + str(municipality.city))
    data = municipality.getJsonData()
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def get_timestamp():
    return datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

def is_date(text):
    try:
        datetime.datetime.strptime(text, "%m/%d/%y")
        return True
    except ValueError:
        return False

