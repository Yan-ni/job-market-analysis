from dotenv import load_dotenv
import logging
import argparse
import os

def check_env_var():
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
  parser.add_argument('-q', '--query', help="the query you want to scrape", default=None)
  
  args = parser.parse_args()
  
  return args

def config_logging(debug: bool):
  logging_level = logging.INFO

  if debug is True:
    logging_level = logging.DEBUG

  logging.basicConfig(
    level=logging_level,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
  )