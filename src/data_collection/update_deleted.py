# Imports
from welcome_to_the_jungle import SearchPage, JobOffer, ScrapeDB
from utils.functions import check_env_var, config_logging
from dotenv import load_dotenv as load_env_var
from datetime import datetime
import logging

# Functions
def main():
  load_env_var()
  check_env_var()
  config_logging()

  ScrapeDB.init()

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

if __name__ == '__main__':
  main()