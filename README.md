A web scraper that is used to download assets (minutes, agenda) from committees of various municipalities. 

## Setup
Run the following to install the required dependencies:

`pip install -r requirements.txt`

## Usage

Runs the Antioch web scraper:
`python scraper.py`

Result:
- writes out a timestamped csv file of all the assets to the `assets` directory
- downloads all assets to the `download` directory. replaces old files with new files.

Note: a few links are broken and do not point to a valid asset.

Time taken:
* 6 minutes to scrape
* 15 minutes to download files

## Supported Cities

### [Antioch](https://www.antiochca.gov/government/agendas-and-minutes/)

* [Issue 1](https://github.com/chrisgioia64/civic-scraper/issues/3) : For `City Council`, years 2002 - 2004 are not getting picked up by Selenium (the rows are there but the text is empty) 
* [Issue 2](https://github.com/chrisgioia64/civic-scraper/issues/3) : For `Zoning Administrator` committee, years 2019 - 2010 not getting picked up by Selenium (the rows are there but the text is empty).
* [Issue 3](https://github.com/chrisgioia64/civic-scraper/issues/1): under the committee: "Processing Quality of Life Forum", there are multiple agendas on the same date. They appear as separate entities in the csv file. However, when they download these resources, they are given the same name and only one of them is saved.

## Improvements

* Files are downloaded in parallel which provides an approximate 2X speedup