A web scraper that is used to download assets (minutes, agenda) from committees of various municipalities. 

Currently have support for only Antioch, California located at : https://www.antiochca.gov/government/agendas-and-minutes/.

## Setup
Run the following to install the required dependencies:

`pip install -r requirements.txt`

## Usage

Runs the Antioch web scraper:
`python antioch_scraper_selenium.py`

Result:
- writes out a timestamped csv file of all the assets to the `assets` directory
- downloads all assets to the `download` directory. replaces old files with new files.

Note: a few links are broken and do not point to a valid asset.

Time taken:
* 6 minutes to scrape
* 15 minutes to download files

### Bugs
* For `City Council`, years 2002 - 2004 are not getting picked up by Selenium (the rows are there but the text is empty)
* For `Zoning Administrator` committee, years 2019 - 2010 not getting picked up by Selenium (the rows are there but the text is empty).
