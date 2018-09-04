import subprocess
import sys
import argparse
from helpers.validator import Validator


parser = argparse.ArgumentParser(description="Runs 'booking-scraper' commands.")
args = parser.parse_args()

print("Enter <country>, <city>, <checkin_date>, <checkout_date> and press 'Enter'\n"
      "To finish input enter blank line.")

validator = Validator()
commands = []

for line in sys.stdin:
    if len(line) is not 1:
        line = line .strip()
        command = line.split(" ")

        is_valid_dates = False

        try:
            arguments = command[4:]
            is_valid_dates = validator.validate_input(checkin_date=command[2], checkout_date=command[3])
        except IndexError:
            print("To few arguments")

        if is_valid_dates:
            commands.append(command)
            print("OK")
        else:
            print("Command must be: <country> <city> <check_in_date> <check_out_date>")

    else:
        break

for comm in commands:
    sp = subprocess.Popen(["python", "runner.py"] + comm)