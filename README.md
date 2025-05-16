# French Job Market Analysis 🌿

The goal of this project is to apply data engineering and analysis concepts to analyze the job market in France.

## Technologies Utilized

- Selenium & Beautiful Soup: For dynamic web page loading & scraping.
- Docker & Postgresql: For deployment and data storage.
- Cron jobs: for ELT orchestration.

## 🚀 Getting started

To install the required packages to run the project's scripts you should:

You need to [install uv](https://docs.astral.sh/uv/getting-started/installation/)

Run the scraping ELT for data analyst:

```shell
uv run src/main.py --query "data analyst"
```

## ⚙️ Data collection

The data collection is done on a daily basis my executing this script.

by scraping the search result for the job titles in the data sources below.

Data sources: [welcome to the jungle](https://www.welcometothejungle.com/en/jobs)
Job offers countries: France
Job offer titles: Data Analyst, Data Science

### Raw database schema

#### scrapes

| Column        | Type               |
| ------------- | ------------------ |
| id            | SERIAL PRIMARY KEY |
| query         | TEXT               |
| contract_type | TEXT               |
| location      | TEXT               |
| country_code  | TEXT               |
| started_at    | INTEGER            |
| ended_at      | INTEGER            |

#### job_offers

| Column               | Type |
| -------------------- | ---- |
| id                   | TEXT |
| company_id           | TEXT |
| title                | TEXT |
| url                  | TEXT |
| description          | TEXT |
| preferred_experience | TEXT |
| recruitment_process  | TEXT |
| scrape_id            | TEXT |
| contract             | TEXT |
| location             | TEXT |
| salary               | TEXT |
| starting_date        | TEXT |
| remote               | TEXT |
| experience           | TEXT |
| education            | TEXT |
| date                 | TEXT |

#### companies

| Column               | Type             |
| -------------------- | ---------------- |
| id                   | TEXT PRIMARY KEY |
| name                 | TEXT             |
| sector               | TEXT             |
| office_location      | TEXT             |
| website_url          | TEXT             |
| presentation         | TEXT             |
| looking_for          | TEXT             |
| good_to_know         | TEXT             |
| creation_year        | TEXT             |
| number_employees     | TEXT             |
| parity_percent_women | TEXT             |
| parity_percent_men   | TEXT             |
| average_age          | TEXT             |
| url                  | TEXT             |

### std data

The std (standardized) data is the raw data cleaned and prepared for analysis.
