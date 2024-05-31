# Imports
from welcome_to_the_jungle import SearchPage, JobOffer, ScrapeDB

# Init
scrape_db = ScrapeDB()

# Variables
total_job_offers_urls = set()

# Scraping Welcome To The Jungle all search result pages
search_page = SearchPage(page_number=1)
while True:
  page_job_offers_urls = search_page.get_jobs_offers_urls()
  print("page {:<2} has {:<2} job offers".format(search_page.page_number, len(page_job_offers_urls)))
  total_job_offers_urls = total_job_offers_urls.union(page_job_offers_urls)

  if len(page_job_offers_urls) < 30:
    break
  search_page.next_page()

# Scraping all job offers
for job_offer_url in total_job_offers_urls:
  job_offer_data = JobOffer(job_offer_url).get_data()
  scrape_db.save_job_offer_data(job_offer_data)

# closing connection to the database
scrape_db.close()