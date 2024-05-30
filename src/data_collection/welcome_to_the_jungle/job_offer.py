from .scraper import Scraper

class JobOffer:
  """A representation of a welcome-to-the-jungle job offer.
  
  Attributes:
  - ulr (str): The url to the job offer.
  """

  def __init__(self, url: str):
    self.url = url

  def get_data(self) -> dict:
    """Returns the data of the job offer."""
    soup = Scraper.get_url_soup(self.url)

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
