import json
import subprocess
import argparse
import random
from concurrent.futures import ThreadPoolExecutor
from helpers.db_helper import DBHelper


def run_spider(command):
    filename = str(random.randint(1, 100)) + '.json'

    with open(filename, 'w') as outfile:
        json.dump(command, outfile)

    sp = subprocess.Popen("python runMultipleSpiders.py" + " " + filename)
    sp.wait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runs 'booking-scraper' commands.")
    parser.add_argument("processes", help="The number of processes", type=int)
    parser.add_argument("spiders", help="The number of spiders per process", type=int)
    args = parser.parse_args()

    print("Enter <country>, <city>, <checkin_date>, <checkout_date> and press 'Enter'\n"
          "To finish input enter blank line.")

    commands = []
    db = DBHelper()
    start_configs = db.select_run_configs().all()
    for conf in start_configs:
        c_in = conf.checkin_date
        c_out = conf.checkout_date
        d = {
            "city": conf.city,
            "country":conf.country,
            "checkin_monthday": c_in.day,
            "checkin_month": c_in.month,
            "checkin_year": c_in.year,

            "checkout_monthday": c_out.day,
            "checkout_month": c_out.month,
            "checkout_year": c_out.year,

            "use_vpn": conf.vpn,
        }
        commands.append(d)

    with ThreadPoolExecutor(max_workers=args.processes) as executor:
        executor.submit(run_spider, commands)
        # for cmd in commands:
        #     executor.submit(run_spider, cmd)
