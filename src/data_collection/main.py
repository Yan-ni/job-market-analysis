# Imports
from welcome_to_the_jungle import SearchPage, JobOffer, ScrapeDB
import concurrent.futures
from dotenv import load_dotenv
import os
import logging
import argparse
import traceback

# Functions
def process_job_offer(job_offer_url):
  try:
    db_pool = ScrapeDB.get_pool()
    logging.debug('getting DB connection from DB POOL.')
    db_connection = db_pool.getconn()
    db_cursor = db_connection.cursor()

    job_offer = JobOffer(url=job_offer_url, db_cursor=db_cursor)
    job_offer_company = job_offer.get_company()

    if not job_offer.exists_in_db():
      if not job_offer_company.exists_in_db():
        job_offer_company.scrape_all_attributes()
        job_offer_company.save_to_db()
        logging.debug(f'saving the "company":"{job_offer_company.get_name()}" data in the database.')

      job_offer.scrape_all_attributes()
      logging.debug(f'saving the "job offer":"{job_offer.get_title()}" data in the database.')
      job_offer.save_to_db()
    else:
      logging.debug(f'"job offer":"({job_offer.get_id()}, {job_offer_company.get_id()})" already exists!')
    logging.debug('putting away the DB connection.')
    db_cursor.close()
    db_pool.putconn(db_connection)
  except Exception as e:
    logging.error(f'An error occurred while processing job offer: {e}')
    logging.error(traceback.format_exc())

def check_environment_variables():
  load_dotenv()

  POSTGRES_DATABASE = os.environ.get('POSTGRES_DB')
  POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
  POSTGRES_USER = os.environ.get('POSTGRES_USER')
  POSTGRES_HOSTNAME = os.environ.get('POSTGRES_HOSTNAME')

  if POSTGRES_DATABASE is None:
    raise Exception(f"postgres database name can't be {POSTGRES_DATABASE}")
  
  if POSTGRES_PASSWORD is None:
    raise Exception(f"postgres user name can't be {POSTGRES_PASSWORD}")
  
  if POSTGRES_USER is None:
    raise Exception(f"postgres database name can't be {POSTGRES_USER}")
  
  if POSTGRES_HOSTNAME is None:
    raise Exception(f"postgres database name can't be {POSTGRES_HOSTNAME}")

def parse_arguments():
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--debug', help="sets logging level to debug", action="store_true")
  
  args = parser.parse_args()
  
  return args

def main():
  args = parse_arguments()

  logging_level = logging.INFO

  if args.debug is True:
    logging_level = logging.DEBUG

  logging.basicConfig(
    level=logging_level,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
  )
  check_environment_variables()

  total_job_offers_urls = set()

  ScrapeDB.init()

  db_connection = ScrapeDB.get_con()
  db_cursor = db_connection.cursor()

  # Scraping Welcome To The Jungle all search result pages
  search_page = SearchPage(db_cursor=db_cursor)

  logging.info('retrieving job offers list from search page...')
  logging.debug('{:<8} {:<8}'.format('Page', 'Job offers'))

  while True:
    page_job_offers_urls = search_page.get_jobs_offers_urls()

    logging.debug("{:<8} {:<8}".format(search_page.get_page_number(), len(page_job_offers_urls)))

    total_job_offers_urls = total_job_offers_urls.union(page_job_offers_urls)

    if len(page_job_offers_urls) < 30:
      break

    search_page = search_page.next_page()

  logging.info(f'retrieved {len(total_job_offers_urls)} job offers from {search_page.get_page_number()} pages.')

  db_cursor.close()
  db_connection.close()

  logging.info('retrieving job offers data...')

  with concurrent.futures.ProcessPoolExecutor() as executor:
    executor.map(process_job_offer, total_job_offers_urls)

if __name__ == '__main__':
  main()