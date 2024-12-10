from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def getChromeDriver(headless=True):
    chrome_options = Options()
    # chrome_options.add_argument("--disable-logging") 
    # chrome_options.add_argument("--log-level=3")  # Suppress most Chrome logs
    # chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.headless = headless
    if headless:
        chrome_options.add_argument("--headless")

    # Set up the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver