# Imports
from welcome_to_the_jungle import SearchPage, JobOffer, ScrapeDB

# Variables
total_job_offers_urls = set()

# Scraping Welcome To The Jungle all search result pages
search_page = SearchPage(page_number=1)

print('[PROCESS] retrieving job offers list from search page.')
print('{:<8} {:<8}'.format('Page', 'Job offers'))

while True:
  page_job_offers_urls = search_page.get_jobs_offers_urls()

  print("{:<8} {:<8}".format(search_page.get_page_number(), len(page_job_offers_urls)))

  total_job_offers_urls = total_job_offers_urls.union(page_job_offers_urls)

  if len(page_job_offers_urls) < 30:
    break

  search_page.next_page()

print('[PROCESS] retrieving job offers data.')

# Scraping all job offers
for job_offer_url in total_job_offers_urls:
  JobOffer(job_offer_url).save_to_db()

# closing connection to the database
ScrapeDB.close()