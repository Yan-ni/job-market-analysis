from .scraper import Scraper
from .database import ScrapeDB

class Company:
  def __init__(self, id: str):
    self.id: str = id
    self.__soup: BeautifulSoup = Scraper.get_url_soup(self.get_url())

    self.name: str = self.__scrape_name()
    self.sector: str = self.__scrape_sector()
    self.office_location: str = self.__scrape_office_location()
    self.website_url: str = self.__scrape_website_url()
    self.presentation: str = self.__scrape_presentation()
    self.looking_for: str = self.__scrape_looking_for()
    self.good_to_know: str = self.__scrape_good_to_know()
    self.creation_year: str = self.__scrape_creation_year()
    self.number_employees: str = self.__scrape_number_employees()
    self.parity_percent_women: str = self.__scrape_parity_percent_women()
    self.parity_percent_men: str = self.__scrape_parity_percent_men()
    self.average_age: str = self.__scrape_average_age()

  def get_id(self) -> str:
    return self.id

  def get_url(self) -> str:
    return f'https://www.welcometothejungle.com/en/companies/{self.id}'

  def get_name(self) -> str:
    return self.name

  def __scrape_name(self) -> str:
    name_tag = self.__soup.select_one('h1')

    return name_tag.get_text(' ') if name_tag is not None else None

  def get_sector(self) -> str:
    return self.sector

  def __scrape_sector(self) -> str:
    sector_tag = self.__soup.select_one('div[data-testid="showcase-header-sector"]')

    return sector_tag.get_text() if sector_tag is not None else None

  def get_office_location(self) -> str:
    return self.office_location

  def __scrape_office_location(self) -> str:
    office_location_tag = self.__soup.select_one('div[data-testid="showcase-header-office"]')

    return office_location_tag.get_text() if office_location_tag is not None else None

  def get_website_url(self) -> str:
    return self.website_url

  def __scrape_website_url(self) -> str:
    website_url_tag = self.__soup.select_one('div[data-testid="showcase-header-website"] a')

    return website_url_tag.attrs.get('href') if website_url_tag is not None else None

  def get_presentation(self) -> str:
    return self.presentation

  def __scrape_presentation(self) -> str:
    text_block_tags = self.__soup.select('article > header + div')

    return Scraper.get_soup_text(text_block_tags[0]) if len(text_block_tags) >= 1 else None

  def get_looking_for(self) -> str:
    return self.looking_for

  def __scrape_looking_for(self) -> str:
    text_block_tags = self.__soup.select('article > header + div')

    return Scraper.get_soup_text(text_block_tags[1]) if len(text_block_tags) >= 2 else None

  def get_good_to_know(self) -> str:
    return self.good_to_know

  def __scrape_good_to_know(self) -> str:
    text_block_tags = self.__soup.select('article > header + div')

    return Scraper.get_soup_text(text_block_tags[2]) if len(text_block_tags) >= 3 else None

  def get_creation_year(self) -> str:
    return self.creation_year

  def __scrape_creation_year(self) -> str:
    creation_year_tag = self.__soup.select_one('span[data-testid="stats-creation-year"]')

    return creation_year_tag.get_text() if creation_year_tag is not None else None

  def get_number_employees(self) -> int:
    return self.number_employees

  def __scrape_number_employees(self) -> str:
    number_employees_tag = self.__soup.select_one('span[data-testid="stats-nb-employees"]')

    return number_employees_tag.get_text() if number_employees_tag is not None else None

  def get_parity_percent_women(self) -> str:
    return self.parity_percent_women

  def __scrape_parity_percent_women(self) -> str:
    parity_percent_women_tag = self.__soup.select_one('span[data-testid="stats-parity-women"]')

    return parity_percent_women_tag.get_text() if parity_percent_women_tag is not None else None

  def get_parity_percent_men(self) -> str:
    return self.parity_percent_men

  def __scrape_parity_percent_men(self) -> str:
    parity_percent_men_tag = self.__soup.select_one('span[data-testid="stats-parity-men"]')

    return parity_percent_men_tag.get_text() if parity_percent_men_tag is not None else None

  def get_average_age(self) -> str:
    return self.average_age

  def __scrape_average_age(self) -> str:
    average_age_tag = self.__soup.select_one('span[data-testid="stats-average-age"]')

    return average_age_tag.get_text() if average_age_tag is not None else None

  def to_dict(self) -> dict:
    return {
      'id': self.get_id(),
      'name': self.get_name(),
      'sector': self.get_sector(),
      'office_location': self.get_office_location(),
      'website_url': self.get_website_url(),
      'presentation': self.get_presentation(),
      'looking_for': self.get_looking_for(),
      'good_to_know': self.get_good_to_know(),
      'creation_year': self.get_creation_year(),
      'number_employees': self.get_number_employees(),
      'parity_percent_women': self.get_parity_percent_women(),
      'parity_percent_men': self.get_parity_percent_men(),
      'average_age': self.get_average_age(),
      'url': self.get_url()
    }

  def save_to_db(self) -> None:
    row_data: dict = self.to_dict()
    ScrapeDB.cur.execute("""INSERT INTO companies(
      id,
      name,
      sector,
      office_location,
      website_url,
      presentation,
      looking_for,
      good_to_know,
      creation_year,
      number_employees,
      parity_percent_women,
      parity_percent_men,
      average_age,
      url) VALUES (
      %(id)s,
      %(name)s,
      %(sector)s,
      %(office_location)s,
      %(website_url)s,
      %(presentation)s,
      %(looking_for)s,
      %(good_to_know)s,
      %(creation_year)s,
      %(number_employees)s,
      %(parity_percent_women)s,
      %(parity_percent_men)s,
      %(average_age)s,
      %(url)s) ON CONFLICT DO NOTHING""", row_data)
