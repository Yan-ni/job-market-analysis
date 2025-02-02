from scraper import Scraper
from database import ScrapeDB


class SearchPage:
    """A representation of (welcome to the jungle) search page.

    Attributes:
    - country_code (str): The country code of the search.
    - contract_type (str): The contract type of the search.
    - query (str): The query for the position we are looking for.
    - location (str): The location where we would like to search in.
    - page (int): The number of the page of the search result.
    """

    def __init__(
        self,
        *,
        db_cursor,
        page_number=1,
        country_code="FR",
        contract_type="FULL_TIME",
        query="data analyst",
        location="Ile-de-France, France",
    ):
        self.country_code = country_code
        self.contract_type = contract_type
        self.query = query
        self.location = location
        self.page_number = page_number

        self.__db_cur = db_cursor

    def save_scrape_to_db(self):
        self.__db_cur.execute(
            """UPDATE scrapes SET
      query = %(query)s,
      contract_type = %(contract_type)s,
      location = %(location)s,
      country_code = %(country_code)s
      WHERE id=%(scrape_id)s""",
            {
                "query": self.get_query(),
                "contract_type": self.get_contract_type(),
                "location": self.get_location(),
                "country_code": self.get_country_code(),
                "scrape_id": ScrapeDB.scrape_id,
            },
        )
        self.__db_cur.connection.commit()

    def get_country_code(self):
        return self.country_code

    def get_contract_type(self):
        return self.contract_type

    def get_query(self):
        return self.query

    def get_location(self):
        return self.location

    def get_page_number(self):
        return self.page_number

    def get_url(self) -> str:
        return f"https://www.welcometothejungle.com/en/jobs?refinementList[offices.country_code][]={self.get_country_code()}&refinementList[contract_type][]={self.get_contract_type()}&query={self.get_query()}&page={self.get_page_number()}&aroundQuery={self.get_location()}&searchTitle=true"

    def get_jobs_offers_urls(self) -> set[str]:
        """Return a set of job urls present in the current search page."""
        soup = Scraper.get_url_soup(self.get_url())
        elements = soup.select("li > div > div > a")
        jobs_urls = set()

        for element in elements:
            if "href" in element.attrs:
                jobs_urls.add(f"https://www.welcometothejungle.com{element['href']}")

        return jobs_urls

    def next_page(self):
        """Return next search page"""
        return SearchPage(
            page_number=(self.page_number + 1),
            db_cursor=self.__db_cur,
            country_code=self.country_code,
            contract_type=self.contract_type,
            query=self.query,
        )
