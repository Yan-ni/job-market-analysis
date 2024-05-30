from scraper import Scraper
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

  def __init__(self, page=1, country_code="FR", contract_type="FULL_TIME", query="data analyst", location="Ile-de-France, France"):
    self.country_code = urllib.parse.quote(country_code)
    self.contract_type = urllib.parse.quote(contract_type)
    self.query = urllib.parse.quote(query)
    self.location = urllib.parse.quote(location)
    self.page = page

  def get_url(self) -> str:
    """Returns the constructed url of the search page."""
    return f"https://www.welcometothejungle.com/en/jobs?refinementList%5Boffices.country_code%5D%5B%5D={self.country_code}&refinementList%5Boffices.state%5D%5B%5D=Ile-de-France&refinementList%5Bcontract_type%5D%5B%5D={self.contract_type}&query={self.query}&page={self.page}&aroundQuery={self.location}"
  
  def get_jobs_urls(self, scraper) -> set[str]:
    """Return the list of job urls present in the current search page."""
    soup = scraper.get_url_soup(self.get_url())
    elements = soup.select('li > div > a')
    jobs_urls = set()

    for element in elements:
      if 'href' in element.attrs:
        jobs_urls.add(f"https://www.welcometothejungle.com{element['href']}")

    return jobs_urls

  def next(self) -> None:
    """Sets the search page to the next search page."""
    self.page += 1

class JobOffer:
  """A representation of a welcome-to-the-jungle job offer.
  
  Attributes:
  - ulr (str): The url to the job offer.
  """

  def __init__(self, url: str):
    self.url = url

  def get_data(self, scraper) -> dict:
    """Returns the data of the job offer."""
    soup = scraper.get_url_soup(self.url)

    job_data = dict()

    job_data['job_url'] = self.url

    job_title = soup.select_one('h1')
    job_data['job_title'] = job_title.get_text(' ') if job_title else None

    company_name = soup.select_one('div + span')
    job_data['company_name'] = company_name.get_text(' ') if company_name else None

    company_description = soup.select_one('section#about-section > h2 + div')
    job_data['company_description'] = Scraper.get_soup_text(company_description) if company_description else None

    job_description = soup.select_one('section#description-section > h2 + div')
    job_data['job_description'] = Scraper.get_soup_text(job_description) if job_description else None

    preferred_experience = soup.select_one('section#profile-section > h2 + div')
    job_data['preferred_experience'] = Scraper.get_soup_text(preferred_experience) if preferred_experience else None

    recruitement_process = soup.select_one('section#recruitment-section > h2 + div')
    job_data['recruitement_process'] = Scraper.get_soup_text(recruitement_process) if recruitement_process else None

    return job_data
