
import requests
from bs4 import BeautifulSoup

def scrape_antioch_agendas_and_minutes():
    url = 'https://www.antiochca.gov/government/agendas-and-minutes/'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        file = open("example.txt", "wb")
        file.write(response.content)
        file.close()
        
        # Example: Find all links to agendas and minutes
        links = soup.find_all('a', href=True)
        print("number of links " + str(len(links)))

        divs = soup.find_all('div', class_='vc_grid-item')
        print("number of divs " + str(len(divs)))

        # links = soup.find_all('a', href=True, class_='vc_gitem-link')
        # print("number of links " + str(len(links)))


        for link in links:
            href = link['href']
            text = link.get_text(strip=True)
            print(f'Text: {text}, URL: {href}')
    else:
        print(f'Failed to retrieve the webpage. Status code: {response.status_code}')

if __name__ == "__main__":
    scrape_antioch_agendas_and_minutes()