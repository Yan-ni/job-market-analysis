from datetime import datetime, date, timedelta
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
import urllib
import os
import re


def str_date_to_timedelta(date_str: str) -> timedelta:
    if not isinstance(date_str, str):
        return None

    if len(date_str) == 0:
        return None

    if date_str == "yesterday":
        return timedelta(days=1)

    if date_str == "last month":
        return timedelta(days=30)

    date_parts = date_str.split(" ")

    if len(date_parts) != 3:
        raise Exception(f"an error occurred splitting '{date_str}' by space")

    (date_number, date_type, _) = date_parts

    if "day" in date_type:
        return timedelta(days=int(date_number))

    if "month" in date_type:
        return timedelta(days=int(date_number) * 30)

    if "hour" in date_type:
        return timedelta(hours=int(date_number))

    if "minute" in date_type:
        return timedelta(minutes=int(date_number))

    if "second" in date_type:
        return timedelta(seconds=int(date_number))


def starting_date_to_date(starting_date: str) -> date | None:
    if not isinstance(starting_date, str):
        return None

    if len(starting_date) == 0:
        return None

    starting_date_split = starting_date.split("  ")

    if len(starting_date_split) == 1:
        return None

    date_str = starting_date_split[1]

    return datetime.strptime(date_str, "%B %d, %Y").date()


def salary_to_min_max_salary(salary: str) -> tuple[int | None, int | None]:
    if not isinstance(salary, str):
        return (None, None)

    if len(salary) == 0:
        return (None, None)

    if salary == "Not specified" or salary == "Not specified0":
        return (None, None)

    # €60K to 100K
    match = re.search(
        "[\$€]?(?P<min>\d+([\.,]\d+)?)K? to (?P<max>\d+([\.,]\d+)?)K?", salary
    )

    if match:
        min = int(float(match.group("min").replace(",", ".")) * 1000)
        max = int(float(match.group("max").replace(",", ".")) * 1000)
        return (min, max)

    # €34K+
    match = re.search("[\$€](?P<min>\d+([\.,]\d+)?)K\+?", salary)

    if match:
        min = int(float(match.group("min").replace(",", ".")) * 1000)

        if "a month" in salary:
            min *= 12

        return (min, None)

    # < €70
    match = re.search("\< [\$€](?P<max>\d+)", salary)

    if match:
        max = int(float(match.group("max")) * 1000)
        return (None, max)

    raise Exception(f"could not match '{salary}' salary")


def clean_job_offers(raw_db_engine, std_db_engine):
    scrapes_df = pd.read_sql("SELECT * FROM scrapes", raw_db_engine).set_index("id")
    job_offers_df = pd.read_sql("SELECT * FROM job_offers", raw_db_engine)

    job_offers_df = job_offers_df.merge(
        scrapes_df[["started_at", "query"]],
        left_on="scrape_id",
        right_on="id",
        how="left",
    )

    job_offers_df = job_offers_df.rename(
        columns={
            "started_at": "scraped_at",
            "date": "created_date",
            "deleted_at": "deleted_date",
            "experience": "min_experience",
        }
    )

    # starting_date
    job_offers_df["starting_date"] = job_offers_df["starting_date"].apply(
        starting_date_to_date
    )

    # education
    job_offers_df["education"] = job_offers_df["education"].apply(
        lambda x: x[11:] if x is not None else None
    )

    # created_date
    job_offers_df["created_date"] = job_offers_df["created_date"].apply(
        str_date_to_timedelta
    )
    job_offers_df["scraped_at"] = job_offers_df["scraped_at"].apply(
        datetime.fromtimestamp
    )
    job_offers_df["created_date"] = pd.to_datetime(
        (job_offers_df["scraped_at"] - job_offers_df["created_date"])
    ).dt.date

    # min_experience
    job_offers_df["min_experience"] = job_offers_df["min_experience"].str[15:]

    # salary
    job_offers_df["salary"] = job_offers_df["salary"].str[9:]
    job_offers_df[["min_salary", "max_salary"]] = (
        job_offers_df["salary"]
        .apply(salary_to_min_max_salary)
        .apply(pd.Series)
        .astype("Int64")
    )

    job_offers_df = job_offers_df[
        [
            "id",
            "company_id",
            "title",
            "query",
            "contract",
            "location",
            "remote",
            "education",
            "min_experience",
            "min_salary",
            "max_salary",
            "created_date",
            "starting_date",
            "deleted_date",
        ]
    ]

    job_offers_df = job_offers_df.rename(columns={"query": "position"})

    save_df_to_std_db("std_job_offers", job_offers_df, std_db_engine)


def str_percent_to_float(percent_str: str) -> float | None:
    if not isinstance(percent_str, str):
        return None

    if len(percent_str) == 0:
        return None

    if "%" not in percent_str:
        raise Exception(f"'%' sign is not included in the percentage string")

    return int(percent_str[:-1]) / 100


def average_age_str_to_int(average_age_str: str) -> int:
    if not isinstance(average_age_str, str):
        return None

    if len(average_age_str) == 0:
        return None

    return int(average_age_str.split(" ")[0])


def clean_companies(raw_db_engine, std_db_engine):
    companies_df = pd.read_sql("SELECT * FROM companies", raw_db_engine)

    # creation_year
    companies_df["creation_year"] = companies_df["creation_year"].astype("Int64")

    # number_employees
    companies_df["number_employees"] = companies_df["number_employees"].astype("Int64")

    # parity_percent
    companies_df["parity_percent_women"] = companies_df["parity_percent_women"].apply(
        str_percent_to_float
    )
    companies_df["parity_percent_men"] = companies_df["parity_percent_men"].apply(
        str_percent_to_float
    )

    # average_age
    companies_df["average_age"] = (
        companies_df["average_age"].apply(average_age_str_to_int).astype("Int64")
    )

    companies_df = companies_df[
        [
            "id",
            "name",
            "creation_year",
            "number_employees",
            "parity_percent_women",
            "parity_percent_men",
            "average_age",
        ]
    ]

    save_df_to_std_db("std_companies", companies_df, std_db_engine)


def save_df_to_std_db(table_name: str, df: pd.DataFrame, std_db_engine):
    df.to_sql(table_name, std_db_engine, if_exists="replace", index=False)


if __name__ == "__main__":
    load_dotenv()
    POSTGRES_HOSTNAME = os.getenv("POSTGRES_HOSTNAME")
    POSTGRES_RAW_DB = os.getenv("POSTGRES_RAW_DB")
    POSTGRES_STD_DB = os.getenv("POSTGRES_STD_DB")
    POSTGRES_USER = urllib.parse.quote(os.getenv("POSTGRES_USER"))
    POSTGRES_PASSWORD = urllib.parse.quote(os.getenv("POSTGRES_PASSWORD"))

    raw_connection_string = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}:5432/{POSTGRES_RAW_DB}"
    std_connection_string = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}:5432/{POSTGRES_STD_DB}"
    raw_db_engine = create_engine(raw_connection_string)
    std_db_engine = create_engine(std_connection_string)

    clean_job_offers(raw_db_engine, std_db_engine)
    clean_companies(raw_db_engine, std_db_engine)
