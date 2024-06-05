# Imports
from welcome_to_the_jungle import SearchPage, JobOffer, ScrapeDB
import concurrent.futures

# Functions
def process_job_offer(job_offer_url):
  job_offer = JobOffer(job_offer_url)
  job_offer_company = job_offer.get_company()

  if job_offer.exists_in_db():
    print('job offer already exists in the Databse!')
    return None

  if not job_offer_company.exists_in_db():
    print('scraping the job offer company.')
    job_offer_company.scrape_all_attributes()
    print('saving company data in the database.')
    job_offer_company.save_to_db()

  print('scraping the job offer data.')
  job_offer.scrape_all_attributes()
  print('saving the job offer data in the database.')
  job_offer.save_to_db()

def main():
  total_job_offers_urls = set()

  # Scraping Welcome To The Jungle all search result pages
  search_page = SearchPage()

  print('[PROCESS] retrieving job offers list from search page.')
  print('{:<8} {:<8}'.format('Page', 'Job offers'))

  while True:
    page_job_offers_urls = search_page.get_jobs_offers_urls()

    print("{:<8} {:<8}".format(search_page.get_page_number(), len(page_job_offers_urls)))

    total_job_offers_urls = total_job_offers_urls.union(page_job_offers_urls)

    if len(page_job_offers_urls) < 30:
      break

    search_page = search_page.next_page()

  print('[PROCESS] retrieving job offers data.')

  with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(process_job_offer, total_job_offers_urls)

  ScrapeDB.close()

if __name__ == '__main__':
  main()