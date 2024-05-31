from .scraper import Scraper
import urllib

class SearchPage:
  """A representation of (welcome to the jungle) search page.
  
  Attributes:
  - country_code (str): The country code of the search.
  - contract_type (str): The contract type of the search.
  - query (str): The query for the position we are looking for.
  - location (str): The location where we would like to search in.
  - page (int): The number of the page of the search result.
  """

  def __init__(self, *, page_number=1, country_code="FR", contract_type="FULL_TIME", query="data analyst", location="Ile-de-France, France"):
    self.country_code = urllib.parse.quote(country_code)
    self.contract_type = urllib.parse.quote(contract_type)
    self.query = urllib.parse.quote(query)
    self.location = urllib.parse.quote(location)
    self.page_number = page_number
    self.url = f'https://www.welcometothejungle.com/en/jobs?refinementList%5Boffices.country_code%5D%5B%5D={self.country_code}&refinementList%5Boffices.state%5D%5B%5D=Ile-de-France&refinementList%5Bcontract_type%5D%5B%5D={self.contract_type}&query={self.query}&page={self.page_number}&aroundQuery={self.location}'

  def get_country_code(self):
    return self.country_code

  def get_contract_type(self):
    return self.get_contract_type

  def get_query(self):
    return self.query

  def get_location(self):
    return self.location 

  def get_page_number(self):
    return self.page_number

  def get_url(self) -> str:
    return self.url
  
  def get_jobs_offers_urls(self) -> set[str]:
    """Return a set of job urls present in the current search page."""
    soup = Scraper.get_url_soup(self.get_url())
    elements = soup.select('li > div > div > a')
    jobs_urls = set()

    for element in elements:
      if 'href' in element.attrs:
        jobs_urls.add(f"https://www.welcometothejungle.com{element['href']}")

    return jobs_urls

  def next_page(self) -> None:
    """Sets the search page to the next search page."""
    self.page_number += 1
