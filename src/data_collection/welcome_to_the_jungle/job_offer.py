from .scraper import Scraper
import re

class JobOffer:
  """A representation of a welcome-to-the-jungle job offer.
  
  Attributes:
  - ulr (str): The url to the job offer.
  """

  def __init__(self, url: str):
    self.url: str = url
    self.__soup: BeautifulSoup = Scraper.get_url_soup(self.url)

    regex_search_result = re.search('https://www.welcometothejungle.com/en/companies/(?P<company_id>.*)/jobs/(?P<job_id>.*)\??.*', self.url)
    self.id: str = regex_search_result.group('job_id')
    self.company_id: str = regex_search_result.group('company_id')
    self.title: str = self.__scrape_title()
    self.description: str = self.__scrape_description()
    self.preferred_experience: str = self.__scrape_preferred_experience()
    self.recruitment_process: str = self.__scrape_recruitment_process()

  def get_url(self) -> str:
    return self.url

  def get_id(self) -> str:
    return self.id

  def get_title(self) -> str:
    return self.title

  def get_company_id(self) -> str:
    return self.company_id

  def get_description(self) -> str:
    return self.description

  def get_preferred_experience(self) -> str:
    return self.preferred_experience

  def get_recruitment_process(self) -> str:
    return self.recruitment_process

  def __scrape_title(self) -> str:
    title_tag = self.__soup.select_one('h2')

    return title_tag.get_text(' ') if title_tag is not None else None

  def __scrape_description(self) -> str:
    description_tag = self.__soup.select_one('div[data-testid="job-section-description"] > div')

    return Scraper.get_soup_text(description_tag) if description_tag is not None else None

  def __scrape_preferred_experience(self) -> str:
    preferred_experience_tag = self.__soup.select_one('div[data-testid="job-section-experience"] > div')

    return Scraper.get_soup_text(preferred_experience_tag) if preferred_experience_tag is not None else None

  def __scrape_recruitment_process(self) -> str:
    recruitment_process_tag = self.__soup.select_one('div[data-testid="job-section-process"] > div')

    return Scraper.get_soup_text(recruitment_process_tag) if recruitment_process_tag is not None else None

  def to_dict(self):
    return {
      'id': self.get_id(),
      'company_id': self.get_company_id(),
      'title': self.get_title(),
      'url': self.get_url(),
      'description': self.get_description(),
      'preferred_experience': self.get_preferred_experience(),
      'recruitment_process':  self.get_recruitment_process()
    }

  def save_to_db(self):
    pass
