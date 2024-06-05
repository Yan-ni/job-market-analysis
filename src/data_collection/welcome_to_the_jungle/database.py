import psycopg2
import time

class ScrapeDB:
  """A representation of the database that holds the scraping data."""
  con = psycopg2.connect(user="postgres", password="password", host="localhost")
  cur = con.cursor()
  cur.execute("""CREATE TABLE IF NOT EXISTS scrapes(
      id SERIAL PRIMARY KEY,
      query TEXT,
      contract_type TEXT,
      location TEXT,
      country_code TEXT,
      started_at INTEGER,
      ended_at INTEGER)"""
    )

  cur.execute("""CREATE TABLE IF NOT EXISTS companies(
      id TEXT PRIMARY KEY,
      name TEXT,
      sector TEXT,
      office_location TEXT,
      website_url TEXT,
      presentation TEXT,
      looking_for TEXT,
      good_to_know TEXT,
      creation_year TEXT,
      number_employees TEXT,
      parity_percent_women TEXT,
      parity_percent_men TEXT,
      average_age TEXT,
      url TEXT)"""
    )

  cur.execute("""CREATE TABLE IF NOT EXISTS job_offers(
      id TEXT,
      company_id TEXT,
      title TEXT,
      url TEXT,
      description TEXT,
      preferred_experience TEXT,
      recruitment_process TEXT,
      contract TEXT,
      location TEXT,
      salary TEXT,
      starting_date TEXT,
      remote TEXT,
      experience TEXT,
      education TEXT,
      date TEXT,
      scrape_id INTEGER,
      PRIMARY KEY (id, company_id),
      FOREIGN KEY (scrape_id) REFERENCES scrapes(id))"""
    )

  cur.execute('INSERT INTO scrapes(started_at) VALUES(%s) RETURNING id', [int(time.time())])
  scrape_id = cur.fetchone()[0]
  
  con.commit()
  print('[INFO] database ready!')

  @classmethod
  def close(cls) -> None:
    """Updates the scrape end time in the data and closes the cursor and the database."""
    timestamp = int(time.time())
    cls.cur.execute('UPDATE scrapes SET ended_at=%s WHERE id=%s', [timestamp, cls.scrape_id])
    cls.con.commit()
    cls.cur.close()
    cls.con.close()
