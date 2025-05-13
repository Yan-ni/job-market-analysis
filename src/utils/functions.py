import logging
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--debug", help="sets logging level to debug", action="store_true"
    )
    parser.add_argument(
        "-q", "--query", help="the query you want to scrape", default=""
    )
    parser.add_argument(
        "-ud",
        "--update-deleted",
        help="only updates the deleted job offers",
        action="store_true",
    )

    args = parser.parse_args()

    return args


def config_logging(debug: bool):
    logging_level = logging.INFO

    if debug is True:
        logging_level = logging.DEBUG

    logging.basicConfig(
        level=logging_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
