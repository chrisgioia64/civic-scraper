A web scraper that is used to download assets (minutes, agenda) from committees of various municipalities. 

## Setup
Run the following to install the required dependencies:

`pip install -r requirements.txt`

## Usage

To runs the all web scrapers (see list of supported cities below), perform the following command:

`python scraper.py`

Result:
- writes out a timestamped csv file of all the assets to the `assets` directory
- downloads all assets to the `download` directory. replaces old files with new files.

Note: a few links are broken and do not point to a valid asset [Issue 5](https://github.com/chrisgioia64/civic-scraper/issues/5).

## How to add a scraper

1. Create a new file with the name of the city (e.g. ClaytonScraper).
2. Follow the template in `example_scraper.py` to create a class.
  * The class should inherit from `CivicScraper`
  * Initialize with the correct municipality and url
  * Implement the `scrape` method where your final result updates the `municipality` instance variable
3. In `scraper.py`, add the new scraper to the `scrapers` list variable.

Now, when you run `python scraper.py`, the new scraper will be included.

## Supported Cities

### [Antioch](https://www.antiochca.gov/government/agendas-and-minutes/)

* [Issue 1](https://github.com/chrisgioia64/civic-scraper/issues/3) : For `City Council`, years 2002 - 2004 are not getting picked up by Selenium (the rows are there but the text is empty) 
* [Issue 2](https://github.com/chrisgioia64/civic-scraper/issues/3) : For `Zoning Administrator` committee, years 2019 - 2010 not getting picked up by Selenium (the rows are there but the text is empty).
* [Issue 3](https://github.com/chrisgioia64/civic-scraper/issues/1): under the committee: "Processing Quality of Life Forum", there are multiple agendas on the same date. They appear as separate entities in the csv file. However, when they download these resources, they are given the same name and only one of them is saved.

Time taken:
* 6 minutes to scrape (TODO: update this value)
* 15 minutes to download files (TODO: update this value)

### [Walnut Creek](https://www.walnutcreekca.gov/government/public-meeting-agendas-and-videos)

Currently does not run to completion but is mostly working. 
* [Issue 8](https://github.com/chrisgioia64/civic-scraper/issues/8) : Stale Exception when clicking the year tab. Prevents scraper from finishing.

Time taken:
* (TODO: update this value)
* (TODO: update this value)

## Improvements

* Files are downloaded in parallel which provides an approximate 2X speedup for the file download time
* Walnut Creek blocks headless browsers so need to make the chrome driver not headless
* Support for downloading both html and pdf files based on content type of response rather than file extension
