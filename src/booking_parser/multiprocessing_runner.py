import subprocess
import sys
import argparse
from helpers.validator import Validator

print("Enter booking-scraper commands and press 'Enter'")

validator = Validator()

for line in sys.stdin:
    if len(line) is not 1:
        line = line .strip()
        command = line.split(" ")

        # TODO Delete all. save only country city c_in date, c_out date and args
        # TODO Add error handling
        if validator.validate_input(checkin_date=command[2], checkout_date=command[3]):
            print("OK")
        else:
            print("Command must be: <country> <city> <check_in_date> <check_out_date>")
        # TODO Validate command array
        # TODO Add command array to array of commands

    else:
        break



# TODO Create loop to loop through array of commands and start subprocesses

# subprocess.Popen(["python", "runner.py", "Украина", "Никополь", "2018-12-12", "2018-12-13"])