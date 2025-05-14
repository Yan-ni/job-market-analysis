# Imports
from helper.functions import scrape_jobs, update_deleted
from utils.functions import config_logging, parse_arguments


def main():
    args = parse_arguments()
    config_logging(args.debug)

    if args.update_deleted:
        update_deleted()
    else:
        scrape_jobs(args)


if __name__ == "__main__":
    main()
