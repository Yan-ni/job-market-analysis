import psycopg2
import psycopg2.extras
import psycopg2.pool
import logging
import time
from dotenv import load_dotenv
import os


class ScrapeDB:
    """A representation of the database that holds the scraping data."""

    __pool = None
    scrape_id = None

    @classmethod
    def init(cls):
        load_dotenv()

        cls.hostname = os.environ.get("POSTGRES_HOSTNAME")
        cls.database = os.environ.get("POSTGRES_DB")
        cls.user = os.environ.get("POSTGRES_USER")
        cls.password = os.environ.get("POSTGRES_PASSWORD")

        con = cls.get_con()
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute(
            """CREATE TABLE IF NOT EXISTS scrapes(
            id SERIAL PRIMARY KEY,
            query TEXT,
            contract_type TEXT,
            location TEXT,
            country_code TEXT,
            started_at INTEGER,
            ended_at INTEGER)"""
        )

        cur.execute(
            """CREATE TABLE IF NOT EXISTS companies(
            id TEXT PRIMARY KEY,
            name TEXT,
            sector TEXT,
            office_location TEXT,
            website_url TEXT,
            presentation TEXT,
            looking_for TEXT,
            good_to_know TEXT,
            creation_year TEXT,
            number_employees TEXT,
            parity_percent_women TEXT,
            parity_percent_men TEXT,
            average_age TEXT,
            url TEXT)"""
        )

        cur.execute(
            """CREATE TABLE IF NOT EXISTS job_offers(
            id TEXT,
            company_id TEXT,
            title TEXT,
            url TEXT,
            description TEXT,
            preferred_experience TEXT,
            recruitment_process TEXT,
            contract TEXT,
            location TEXT,
            salary TEXT,
            starting_date TEXT,
            remote TEXT,
            experience TEXT,
            education TEXT,
            date TEXT,
            deleted_at DATE DEFAULT NULL,
            scrape_id INTEGER,
            PRIMARY KEY (id, company_id),
            FOREIGN KEY (company_id) REFERENCES companies(id),
            FOREIGN KEY (scrape_id) REFERENCES scrapes(id))"""
        )

        con.commit()
        cur.close()
        con.close()

        # logging.info('database ready!')

    @classmethod
    def insert_scrape_id(cls):
        con = cls.get_con()
        cur = con.cursor()

        cur.execute("SELECT id FROM scrapes ORDER BY id DESC LIMIT 1")

        db_res = cur.fetchone()

        cls.scrape_id = db_res[0] + 1 if db_res is not None else 1

        cur.execute(
            "INSERT INTO scrapes(id, started_at) VALUES(%(id)s, %(started_at)s)",
            {"id": cls.scrape_id, "started_at": int(time.time())},
        )

        con.commit()
        cur.close()
        con.close()

    @classmethod
    def get_con(cls):
        return psycopg2.connect(
            database=cls.database,
            user=cls.user,
            password=cls.password,
            host=cls.hostname,
        )

    @classmethod
    def get_scrape_id(cls):
        return cls.scrape_id

    @classmethod
    def create_pool(cls):
        cls.__pool = psycopg2.pool.ThreadedConnectionPool(
            1,
            10,
            database=cls.database,
            user=cls.user,
            password=cls.password,
            host=cls.hostname,
        )

    @classmethod
    def get_pool(cls):
        if cls.__pool is None:
            cls.create_pool()

        return cls.__pool
