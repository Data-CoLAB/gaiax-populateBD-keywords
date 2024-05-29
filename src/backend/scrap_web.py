from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

# Custom expected condition to wait until the div has at least 2 <p> elements
class element_has_at_least_number_of_children:
    def __init__(self, locator, number_of_children):
        self.locator = locator
        self.number_of_children = number_of_children

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        if len(element.find_elements(By.TAG_NAME, "p")) >= self.number_of_children:
            return True
        else:
            return False

def extract_content(url: str):
    # Set up Chrome options
    options = webdriver.ChromeOptions()

    # Set up the WebDriver using webdriver-manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Open a webpage
    driver.get(url)

    # Wait until the div with the specific class has at least two <p> elements inside
    try:
        WebDriverWait(driver, 20).until(
            element_has_at_least_number_of_children((By.CSS_SELECTOR, 'div.Markdown_markdown__3aZ4V.undefined'), 2)
        )
    except TimeoutException:
        print("Timed out waiting for the page to load")

    # Get the page source (HTML code)
    html_source = driver.page_source

    # Close the WebDriver
    driver.quit()

    return html_source
