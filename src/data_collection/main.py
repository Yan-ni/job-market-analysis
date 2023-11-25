# Imports
from db import ScrapeDB
from welcome_to_the_jungle import SearchPage, JobOffer
from scraper import Scraper

# Init
scraper = Scraper()
scrape_db = ScrapeDB()

# Variables
total_pages_jobs_urls = set()

# Scraping Welcome To The Jungle all search result pages
search_page = SearchPage(page=1)
while True:
  page_jobs_urls = search_page.get_jobs_urls(scraper)
  print("page {:<2} has {:<2} jobs".format(search_page.page, len(page_jobs_urls)))
  total_pages_jobs_urls = total_pages_jobs_urls.union(page_jobs_urls)

  if len(page_jobs_urls) < 30:
    break
  search_page.next()

# Scraping all job offers
for job_url in total_pages_jobs_urls:
  job_offer_data = JobOffer(job_url).get_data(scraper)
  scrape_db.save_job_offer_data(job_offer_data)

# closing connection to the database
scrape_db.close()