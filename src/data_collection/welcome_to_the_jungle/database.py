import psycopg2
import time

class ScrapeDB:
  """A representation of the database that holds the scraping data."""

  def __init__(self):
    self.con = psycopg2.connect(user="postgres", password="password", host="localhost")

    self.cur = self.con.cursor()

    self.cur.execute("""CREATE TABLE IF NOT EXISTS scrapes(
      id SERIAL PRIMARY KEY,
      started_at INTEGER,
      ended_at INTEGER
    )""")

    self.cur.execute("""CREATE TABLE IF NOT EXISTS job_offers(
      id SERIAL PRIMARY KEY,
      job_url TEXT,
      job_title TEXT,
      company_name TEXT,
      company_description TEXT,
      job_description TEXT,
      preferred_experience TEXT,
      recruitement_process TEXT,
      scrape_id INTEGER,
      FOREIGN KEY (scrape_id) REFERENCES scrapes(id)
      )""")

    timestamp = int(time.time())
    self.cur.execute('INSERT INTO scrapes(started_at) VALUES(%s)', [timestamp])
    self.con.commit()
    self.scrape_id = self.cur.lastrowid

  def save_job_offer_data(self, job_offer_data: dict) -> None:
    """Saves the job data in the database."""
    job_data = list(job_offer_data.values())
    job_data.append(self.scrape_id)
    self.cur.execute("""INSERT INTO job_offers(
      job_url,
      job_title,
      company_name,
      company_description,
      job_description,
      preferred_experience,
      recruitement_process,
      scrape_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""", job_data)
    self.con.commit()
    
    if len(job_data) >= 2:
      print('[SAVING] {:<80} @ {:<50}'.format(job_data[1], job_data[2]))

  def close(self) -> None:
    """Updates the scrape end time in the data and closes the cursor and the database."""
    timestamp = int(time.time())
    self.cur.execute('UPDATE scrapes SET ended_at=%s WHERE id=%s', [timestamp, self.scrape_id])
    self.con.commit()
    self.cur.close()
    self.con.close()
