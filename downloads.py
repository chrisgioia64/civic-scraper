import requests
import os
from records import Municipality, CommitteeData, CommitteeMeeting, CommitteeFile

def download_files(municipality : Municipality):
    print("Downloading files for " + str(municipality.city))
    for committee in municipality.committees:
        print("Downloading files for committee " + str(committee.name))
        for meeting in committee.meetings:
            download_meeting(municipality, committee, meeting)

def download_meeting(municipality : Municipality, committee : CommitteeData, 
                 meeting : CommitteeMeeting):
    committee_name = committee.name.replace("/","_")
    dir = "download/" + municipality.county + "/" + municipality.city + "/" + committee_name + "/"
    # print("meeting date " + str(meeting.date))
    s = dir + municipality.city + "_" + committee_name + "_" + meeting.date.strftime("%Y_%m_%d")
    
    os.makedirs(dir, exist_ok=True)
    if meeting.agenda is not None:
        filename = s + "_agenda." + file_extension(meeting.agenda.file_url)
        download_file(meeting.agenda.file_url, filename)
    if meeting.minutes is not None:
        filename = s + "_minutes." + file_extension(meeting.minutes.file_url)
        download_file(meeting.minutes.file_url, filename)

def download_file(url, local_filename):
    # Send a GET request to the URL
    with requests.get(url, stream=True) as response:
        try:
            response.raise_for_status()  # Check if the request was successful
            with open(local_filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
    
        except requests.HTTPError as e:
            print(f"Failed to download {url}: {e}")
        # Write the content to a local file
        
    # print(f"Downloaded {url} to {local_filename}")

def file_extension(url : str):
    local_filename = url.split('/')[-1]
    extension = local_filename.split('.')[-1]
    return extension

if __name__ == "__main__":
    url = 'https://www.antiochca.gov/fc/government/agendas/CityCouncil/2024/agendas/111224/111224a.pdf'
    local_folder = 'download'
    
    # Ensure the local folder exists
    os.makedirs(local_folder, exist_ok=True)
    
    download_file(url, local_folder)