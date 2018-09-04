import subprocess
import sys
import time
import argparse
from helpers.validator import Validator
from concurrent.futures import ThreadPoolExecutor
from helpers.db_helper import DBHelper
from models.start_config import StartConfig


def run_spider(args_arr):
    sp = subprocess.Popen(["python", "runMultipleSpiders.py"] + args_arr)
    sp.wait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runs 'booking-scraper' commands.")
    args = parser.parse_args()

    print("Enter <number of processes>, <number of spiders per process> and press 'Enter'\n"
          "To finish input enter blank line.")

    db = DBHelper()
    start_configs = db.select_run_configs().all()
    print(start_configs)

    for start_config in start_configs:
        print(start_config.id)
        print(start_config.country)
        print(start_config.city)
        print(start_config.checkin_date)
        print(start_config.checkout_date)
        print(start_config.vpn)
        print(start_config.concurrent_request_amount)
        print("\n")


    # with ThreadPoolExecutor(max_workers=3) as executor:
    #     for cmd in commands:
    #         executor.submit(run_spider, cmd)