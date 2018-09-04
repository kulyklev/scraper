import json
import subprocess
import sys
import time
import argparse
from helpers.validator import Validator
from concurrent.futures import ThreadPoolExecutor
from helpers.db_helper import DBHelper
from models.start_config import StartConfig
from datetime import datetime


def run_spider(command):
    sp = subprocess.Popen("python runMultipleSpiders.py" + " " + command)
    sp.wait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runs 'booking-scraper' commands.")
    parser.add_argument("processes", help="The number of processes", type=int)
    parser.add_argument("spiders", help="The number of spiders per process", type=int)
    args = parser.parse_args()

    print("Enter <country>, <city>, <checkin_date>, <checkout_date> and press 'Enter'\n"
          "To finish input enter blank line.")

    validator = Validator()

    commands = []
    db = DBHelper()
    start_configs = db.select_run_configs().all()
    for conf in start_configs:
        c_in = conf.checkin_date
        c_out = conf.checkout_date
        d = {
            "ss": conf.city + " " + conf.country,
            "checkin-monthday": c_in.day,
            "checkin-month": c_in.month,
            "checkin-year": c_in.year,

            "checkout-monthday": c_out.day,
            "checkout-month": c_out.month,
            "checkout-year": c_out.year,

            "use-vpn": conf.vpn,
        }
        commands.append(d)

    commands = json.dumps(commands, separators=(',', ':'))

    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(run_spider, commands)
        # for cmd in commands:
        #     executor.submit(run_spider, cmd)
