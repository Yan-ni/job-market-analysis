from scraper import Scraper
from database import ScrapeDB
from .company import Company
from bs4 import BeautifulSoup
import re


class JobOffer:
    """A representation of a welcome-to-the-jungle job offer.

    Attributes:
    - ulr (str): The url to the job offer.
    """

    def __init__(self, url: str, db_cursor):
        self.__db_cur = db_cursor
        self.url: str = url

        regex_search_result = re.search(
            "companies\/(?P<company_id>[^\/]+)\/jobs\/(?P<job_id>[^\/?]+)", self.url
        )
        self.id: str = regex_search_result.group("job_id")
        company_id: str = regex_search_result.group("company_id")
        self.company: Company = Company(company_id, db_cursor=self.__db_cur)

    def exists_in_db(self) -> bool:
        self.__db_cur.execute(
            """Select 1 FROM job_offers WHERE id=%(id)s AND company_id=%(company_id)s""",
            {"id": self.get_id(), "company_id": self.get_company().get_id()},
        )

        return self.__db_cur.fetchone() is not None

    def load_from_db(self) -> None:
        if not self.exists_in_db():
            return None

        self.__db_cur.execute(
            """SELECT * FROM job_offers WHERE id=%(id)s""", {"id": self.get_id()}
        )

        row = self.__db_cur.fetchone()

        row_dict = dict(row) if row is not None else dict()

        self.title: str = row_dict.get("title")
        self.description: str = row_dict.get("description")
        self.preferred_experience: str = row_dict.get("preferred_experience")
        self.recruitment_process: str = row_dict.get("recruitment_process")
        self.contract: str = row_dict.get("contract")
        self.location: str = row_dict.get("location")
        self.salary: str = row_dict.get("salary")
        self.starting_date: str = row_dict.get("starting_date")
        self.remote: str = row_dict.get("remote")
        self.experience: str = row_dict.get("experience")
        self.education: str = row_dict.get("education")
        self.date: str = row_dict.get("date")

    def __get_soup(self):
        return Scraper.get_url_soup(self.get_url())

    def scrape_all_attributes(self) -> None:
        self.__soup: BeautifulSoup = self.__get_soup()
        self.title: str = self.__scrape_title()
        self.description: str = self.__scrape_description()
        self.preferred_experience: str = self.__scrape_preferred_experience()
        self.recruitment_process: str = self.__scrape_recruitment_process()
        self.contract: str = self.__scrape_contract()
        self.location: str = self.__scrape_location()
        self.salary: str = self.__scrape_salary()
        self.starting_date: str = self.__scrape_starting_date()
        self.remote: str = self.__scrape_remote()
        self.experience: str = self.__scrape_experience()
        self.education: str = self.__scrape_education()
        self.date: str = self.__scrape_date()

    def get_id(self) -> str:
        return self.id

    def get_company(self) -> Company:
        return self.company

    def get_url(self) -> str:
        return self.url

    def get_title(self) -> str:
        return self.title

    def __scrape_title(self) -> str:
        title_tag = self.__soup.select_one("h2")

        return title_tag.get_text(" ") if title_tag is not None else None

    def get_description(self) -> str:
        return self.description

    def __scrape_description(self) -> str:
        description_tag = self.__soup.select_one(
            'div[data-testid="job-section-description"] > div'
        )

        return (
            Scraper.get_soup_text(description_tag)
            if description_tag is not None
            else None
        )

    def get_preferred_experience(self) -> str:
        return self.preferred_experience

    def __scrape_preferred_experience(self) -> str:
        preferred_experience_tag = self.__soup.select_one(
            'div[data-testid="job-section-experience"] > div'
        )

        return (
            Scraper.get_soup_text(preferred_experience_tag)
            if preferred_experience_tag is not None
            else None
        )

    def get_recruitment_process(self) -> str:
        return self.recruitment_process

    def __scrape_recruitment_process(self) -> str:
        recruitment_process_tag = self.__soup.select_one(
            'div[data-testid="job-section-process"] > div'
        )

        return (
            Scraper.get_soup_text(recruitment_process_tag)
            if recruitment_process_tag is not None
            else None
        )

    def get_contract(self) -> str:
        return self.contract

    def __scrape_contract(self) -> str:
        contract_icon_tag = self.__soup.select_one('i[name="contract"]')

        return (
            contract_icon_tag.parent.get_text(" ")
            if contract_icon_tag is not None
            else None
        )

    def get_location(self) -> str:
        return self.location

    def __scrape_location(self) -> str:
        location_icon_tag = self.__soup.select_one('i[name="location"]')

        return (
            location_icon_tag.parent.get_text(" ")
            if location_icon_tag is not None
            else None
        )

    def get_salary(self) -> str:
        return self.salary

    def __scrape_salary(self) -> str:
        salary_icon_tag = self.__soup.select_one('i[name="salary"]')

        return (
            salary_icon_tag.parent.get_text(" ")
            if salary_icon_tag is not None
            else None
        )

    def get_starting_date(self) -> str:
        return self.starting_date

    def __scrape_starting_date(self) -> str:
        starting_date_icon_tag = self.__soup.select_one('i[name="clock"]')

        return (
            starting_date_icon_tag.parent.get_text(" ")
            if starting_date_icon_tag is not None
            else None
        )

    def get_remote(self) -> str:
        return self.remote

    def __scrape_remote(self) -> str:
        remote_icon_tag = self.__soup.select_one('i[name="remote"]')

        return (
            remote_icon_tag.parent.get_text(" ")
            if remote_icon_tag is not None
            else None
        )

    def get_experience(self) -> str:
        return self.experience

    def __scrape_experience(self) -> str:
        experience_icon_tag = self.__soup.select_one(
            'div[data-testid="job-metadata-block"] i[name="suitcase"]'
        )

        return (
            experience_icon_tag.parent.get_text(" ")
            if experience_icon_tag is not None
            else None
        )

    def get_education(self) -> str:
        return self.education

    def __scrape_education(self) -> str:
        education_icon_tag = self.__soup.select_one('i[name="education_level"]')

        return (
            education_icon_tag.parent.get_text(" ")
            if education_icon_tag is not None
            else None
        )

    def is_deleted(self) -> str:
        if hasattr(self, "__soup") is False:
            self.__soup = self.__get_soup()

        return self.__soup.select_one('svg[alt="Alert"]') is not None

    def get_date(self) -> str:
        return self.date

    def __scrape_date(self) -> str:
        date_icon_tag = self.__soup.select_one('i[name="date"]')

        return date_icon_tag.parent.get_text(" ") if date_icon_tag is not None else None

    def to_dict(self):
        return {
            "id": self.get_id(),
            "company_id": self.get_company().get_id(),
            "title": self.get_title(),
            "url": self.get_url(),
            "description": self.get_description(),
            "preferred_experience": self.get_preferred_experience(),
            "recruitment_process": self.get_recruitment_process(),
            "contract": self.get_contract(),
            "location": self.get_location(),
            "salary": self.get_salary(),
            "starting_date": self.get_starting_date(),
            "remote": self.get_remote(),
            "experience": self.get_experience(),
            "education": self.get_education(),
            "date": self.get_date(),
        }

    def save_to_db(self) -> None:
        """Saves the job data in the database."""
        row_data: dict = self.to_dict()
        row_data["scrape_id"] = ScrapeDB.scrape_id
        self.__db_cur.execute(
            """INSERT INTO job_offers(
            id,
            company_id,
            title,
            url,
            description,
            preferred_experience,
            recruitment_process,
            scrape_id,
            contract,
            location,
            salary,
            starting_date,
            remote,
            experience,
            education,
            date) VALUES (
            %(id)s,
            %(company_id)s,
            %(title)s,
            %(url)s,
            %(description)s,
            %(preferred_experience)s,
            %(recruitment_process)s,
            %(scrape_id)s,
            %(contract)s,
            %(location)s,
            %(salary)s,
            %(starting_date)s,
            %(remote)s,
            %(experience)s,
            %(education)s,
            %(date)s) ON CONFLICT DO NOTHING""",
            row_data,
        )

        self.__db_cur.connection.commit()
