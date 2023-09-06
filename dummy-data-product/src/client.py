from datetime import datetime

import dotenv
import sys

sys.path.append(
    "D:/Taiyo/TS/pt-mesh-pipeline-main/dummy-data-product/src/dependencies/scraping/egov.py"
)
from dependencies.scraping.egov import Scraper
from dependencies.scraping.scraper import WebScraper

import logging


# Importing scraping and data processing modules
# from dependencies.scraping.<file_name> import <class_name>
# from dependencies.scraping.<file_name> import <class_name>
# from dependencies.cleaning.<file_name> import <class_name>
# from dependencies.geocoding.<file_name> import <class_name>
# from dependencies.standardization.<file_name> import <class_name>

dotenv.load_dotenv(".env")
logging.basicConfig(level=logging.INFO)


# In each step create an object of the class, initialize the class with
# required configuration and call the run method
def step_1():
    logging.info("Scraped Metadata")


def step_2():
    logging.info("Scraped Main Data")
    egov_object = Scraper()
    egov_object.get_data()


def step_3():
    logging.info("Cleaned Main Data")
    egov_object = WebScraper()
    egov_object.scrape()


def step_4():
    logging.info("Geocoded Cleaned Data")


def step_5():
    logging.info("Standardized Geocoded Data")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--step", help="step to be choosen for execution")

    args = parser.parse_args()

    eval(f"step_{args.step}()")

    logging.info(
        {
            "last_executed": str(datetime.now()),
            "status": "Pipeline executed successfully",
        }
    )
