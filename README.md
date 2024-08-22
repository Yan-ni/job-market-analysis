# French Job Market Analysis 🌿

The goal of this project is to apply data analysis concepts to analyze the job market in France.

## Technologies Utilized

- Selenium & Beautiful Soup: For dynamic web page loading & scraping.
- Docker & Postgresql: For data storage.

## 🚀 Getting started

To install the required packages to run the project's scripts you should:

Create a virtual environment (venv):

```shell
python3 -m venv .venv
source .venv/bin/activate
```

Installing the project dependencies:

```shell
pip3 install -r requirements.txt
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
