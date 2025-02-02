from welcome_to_the_jungle import SearchPage, JobOffer, ScrapeDB
import concurrent.futures
from datetime import datetime
import logging
import traceback

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

def scrape_jobs(args):
  total_job_offers_urls = set()

  ScrapeDB.insert_scrape_id()

  db_connection = ScrapeDB.get_con()
  db_cursor = db_connection.cursor()

  # Scraping Welcome To The Jungle all search result pages
  search_page = SearchPage(db_cursor=db_cursor, location='France', query=args.query)

  search_page.save_scrape_to_db()

  logging.info(f'retrieving job offers list from search page: {{query: {search_page.get_query()}, location: {search_page.get_location()}}}')
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

def update_deleted(args):
  db_conn = ScrapeDB.get_con()
  db_cur = db_conn.cursor()

  db_cur.execute("SELECT url FROM job_offers WHERE deleted_at IS NULL")

  job_offer_urls = [url[0] for url in db_cur.fetchall()]

  deleted_job_offers_ids = list()

  if len(job_offer_urls) == 0:
    logging.warning('database empty.')
    exit(0)

  for job_offer_url in job_offer_urls:
    jo = JobOffer(job_offer_url, db_cur)
    jo_company = jo.get_company()

    if jo.is_deleted():
      deleted_job_offers_ids.append((jo.get_id(), jo_company.get_id()))

  if len(deleted_job_offers_ids) == 0:
    logging.info('nothing to update.')
    exit(0)

  logging.info(f'updating {len(deleted_job_offers_ids)} rows.')

  db_cur.execute("""UPDATE job_offers
                  SET deleted_at = %(deleted_at)s
                  WHERE (id, company_id) IN %(deleted_job_offers_ids)s
                  """, {
                    "deleted_at": str(datetime.now().date()),
                    "deleted_job_offers_ids": tuple(deleted_job_offers_ids)
                  })

  db_conn.commit()

  logging.info('database updated successfully.')

  db_cur.close()
  db_conn.close()
