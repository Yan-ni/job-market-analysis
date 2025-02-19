# Imports
from helper.functions import scrape_jobs, update_deleted
from dotenv import load_dotenv as load_env_var
from utils.functions import check_env_var, config_logging, parse_arguments


def main():
    args = parse_arguments()
    config_logging(args.debug)
    load_env_var()
    check_env_var()

    if args.update_deleted:
        update_deleted()
    else:
        scrape_jobs(args)


if __name__ == "__main__":
    main()
