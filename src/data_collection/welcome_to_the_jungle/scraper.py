from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import time
import re

SLEEP_TIME=1

class Scraper:
  """A representation of the scraper that is a combination of selenium and beautiful soup."""
  
  def __init__(self):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    self.browser = Chrome(options=chrome_options) # Path to chromium argument is optional, if not specified will search path.

  def get_url_soup(self, url: str) -> BeautifulSoup:
    """Fetch the url and return its page source soup."""
    self.browser.get(url)
    time.sleep(SLEEP_TIME)
    return BeautifulSoup(self.browser.page_source, 'lxml')

  @staticmethod
  def get_soup_text(soup: BeautifulSoup) -> str:
    """Get text from a multi line text.
    This method prevents having randomly broken words or inconsistent returns.
    """
    text_list = list()
    soup_elements = soup.find_all(['p', 'li'])

    if len(soup_elements) == 0:
      return None

    for soup_element in soup_elements:
      if soup_element.p: # prevent having duplicate lines in case of: <li><p>...</p></li>
        continue

      for br in soup_element.find_all("br"):
        br.replace_with("\n")
      text_list.append(soup_element.get_text(''))

    text = "\n".join(text_list)
    text = re.sub(re.compile(r'\n{3,}'), '\n\n', text) # prevent having more than 2 line returns
    text = re.sub(re.compile(r':\n{2,}'), ':\n', text) # prevent having an empty line after a sentence ending with ":"
    text = re.sub(re.compile(r'([^\n])(\n.*:)'), r'\1\n\2', text) # prevent having empty lines before sentence ending with ":"

    return text