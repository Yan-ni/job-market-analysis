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

  cur.execute("""CREATE TABLE IF NOT EXISTS job_offers(
      id SERIAL PRIMARY KEY,
      company_id TEXT,
      title TEXT,
      url TEXT,
      description TEXT,
      preferred_experience TEXT,
      recruitment_process TEXT,
      scrape_id INTEGER,
      FOREIGN KEY (scrape_id) REFERENCES scrapes(id))"""
    )

  cur.execute('INSERT INTO scrapes(started_at) VALUES(%s)', [int(time.time())])
  con.commit()

  scrape_id = cur.lastrowid
  print('[INFO] database ready!')

  @classmethod
  def close(cls) -> None:
    """Updates the scrape end time in the data and closes the cursor and the database."""
    timestamp = int(time.time())
    cls.cur.execute('UPDATE scrapes SET ended_at=%s WHERE id=%s', [timestamp, cls.scrape_id])
    cls.con.commit()
    cls.cur.close()
    cls.con.close()
