import psycopg2
import time

class ScrapeDB:
  """A representation of the database that holds the scraping data."""

  con = psycopg2.connect(user="postgres", password="password", host="localhost")
  cur = con.cursor()
  cur.execute("""CREATE TABLE IF NOT EXISTS scrapes(
      id SERIAL PRIMARY KEY,
      started_at INTEGER,
      ended_at INTEGER)"""
    )

  self.cur.execute("""CREATE TABLE IF NOT EXISTS job_offers(
      id SERIAL PRIMARY KEY,
      job_url TEXT,
      job_title TEXT,
      company_name TEXT,
      company_description TEXT,
      job_description TEXT,
      preferred_experience TEXT,
      recruitment_process TEXT,
      scrape_id INTEGER,
      FOREIGN KEY (scrape_id) REFERENCES scrapes(id))"""
    )

  cur.execute('INSERT INTO scrapes(started_at) VALUES(%s)', [int(time.time())])
  con.commit()

  scrape_id = cur.lastrowid

  @classmethod
  def close(cls) -> None:
    """Updates the scrape end time in the data and closes the cursor and the database."""
    timestamp = int(time.time())
    self.cur.execute('UPDATE scrapes SET ended_at=%s WHERE id=%s', [timestamp, cls.scrape_id])
    self.con.commit()
    self.cur.close()
    self.con.close()
