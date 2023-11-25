# Welcome To The Jungle Job Market Analysis 🌿

As a junior Data Analyst based in Ile-de-France, France, I aim to identify trending technologies demanded in my local job market. To address this, I've initiated a data analysis project.

## Project structure

This project follows the data analysis process:

1. Data Collection ⚙️.
2. Data Cleaning 🧼.
3. Data Analysis 🔍.
4. Data Visualization 📊.
5. Decision Making ✅.

Technologies Utilized:

- Selenium: For dynamic web page loading.
- Beautiful Soup: For web scraping.
- SQLite: For data storage.
- Pandas: For data cleaning and manipulation.
- Tableau: For data visualization.

## 🚀 Getting started

The requirements of the project are in `requirements.txt`

To install the required packages to run the project's scripts you should:

Create a virtual environement (venv):
> 💡 This step is optionnal but recommanded.

```shell
python3 -m venv .venv
source .venv/bin/activate
```

Installing the requirements:

```shell
pip3 install -r requirements.txt
```

## ⚙️ Data collection

### 🤖 Gathering the Data

Scraping job offers from [Welcome to the Jungle](https://www.welcometothejungle.com/en/jobs):

Difficulties faced scraping welcome to the jungle:

- The website is rendered on client side (CSR).
- The website uses dynamic class names.

| Challenge faced | Solution |
| ----------- | ----------- |
| Client-side rendered website (CSR) | Used Selenium to load the pages first |
| Usage of dynamic class names. | Used XPath and section id |

### 💾 Storing the Data

Utilizing SQLite for data storage due to its simplicity and efficiency.

Table Definitions:

```SQL
CREATE TABLE IF NOT EXISTS scrapes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  started_at INTEGER,
  ended_at INTEGER
);

CREATE TABLE IF NOT EXISTS job_offers(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  job_url TEXT,
  job_title TEXT,
  company_name TEXT,
  company_description TEXT,
  job_description TEXT,
  preferred_experience TEXT,
  recruitement_process TEXT,
  scrape_id INTEGER,
  FOREIGN KEY (scrape_id) REFERENCES scrapes(id)
);
```

You can find an example of resulted database [here](/example/)

## 🧼 Data cleaning

Cleaning the raw data in the database using Pandas:

1. Load job offers data.
1. Remove records without a job URL or title.
1. Trim URL parameters.
1. Eliminate duplicate records based on URL.

## 🔍 Data analysis

Post data cleaning, I focused on extracting insights about technology usage.

Using a predefined set of key technology names – 'Excel', 'VBA', 'R', 'Python', 'SQL', 'Power BI', 'Tableau', and 'Looker' – I analyzed job_descriptions and preferred_experience to quantify their frequency.

This transformed data serves as a foundation for upcoming visualizations.

---
You can find an example of the outputed excel file [here](/example/)

## 📊 Data Visualization

Utilizing Tableau to visualize the data extracted, creating comprehensive charts and dashboards for market demand insights.

You can review the Tableau workbook of this visualization [here](/example/)

!['Global view of keywords occurence'](docs/assets/Global%20keywords.jpg)

!['Excel and VBA insights'](docs/assets/Excel%20and%20VBA%20-%20Pie.jpg)

!['programming languages insights dashboard'](docs/assets/Prog%20Lang%20-%20Dashboard.jpg)

!['bi tools insights dashboard'](docs/assets/Bi%20Tools%20-%20Dashboard.jpg)

## ✅ Decision making

Upon visualizing the data insights, I've strategically prioritized refining my skills in key technologies:

- **SQL** emerges as an indispensable requirement across a majority of job offers, underscoring its significance in today's market.
- **Python** stands out as a powerful programming language within the data analysis realm, solidifying its dominance over R.
- **Tableau**, from the visualized data, exhibits more promising prospects compared to both **Power BI** and **Looker**.
- Incorporating **Excel** into my skill set is recognized as a valuable addition.

These insights derived from data visualization act as guiding principles, directing my focus towards acquiring expertise in technologies that hold relevance and demand in the job market of Ile-de-France, France.
