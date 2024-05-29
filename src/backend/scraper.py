import requests
import re
from bs4 import BeautifulSoup
# import PyPDF2
 
 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
 
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
 
class SeleniumScraper:
    def __init__(self):
        self.options = Options()
 
        # Maximize the window
        self.options.add_argument("--headless")
 
        # Set up WebDriver (example with Chrome)
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service,options=self.options)
 
 
    def get_content(self,url):
        self.driver.get(url)
        time.sleep(2)
        page_source = self.driver.page_source
 
        soup = BeautifulSoup(page_source, 'html.parser')
        content = soup.find('div', attrs={'class': 'AssetContent_content__1YKv5 Box_box__l77_J'})
        if content is not None:
            content = content.get_text()
        return content
 
def request_extractor(url):
    try:
        response = requests.get(url, stream=True)
        content_type = response.headers.get('Content-Type')
 
        # Check if the content is HTML
        if 'text/html' in content_type:
            print("Extracting from HTML")
            soup = BeautifulSoup(response.text, 'html.parser')
            for script_or_style in soup(['footer', 'link', 'style',
                       'noscript', 'iframe','header', 'script', 'meta', 'img', 'button', 'nav']):
                script_or_style.decompose()
            text = soup.get_text()
            text= re.sub(r'\n{2,}', '\n', text)
            return text
        else:
            return "Unsupported content type"

 
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
 
 
def extract_content(url: str,config: dict):
 
    extraction_type = config['extraction_type']
 
    if extraction_type== "requests":
 
        content_ext = request_extractor(url)
    elif extraction_type=="scraper":
        scraper = SeleniumScraper()
 
        content_ext = scraper.get_content(url)
 
    return content_ext