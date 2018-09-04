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
        is_valid_args = False

        try:
            arguments = command[4:]
            is_valid_dates = validator.validate_input(checkin_date=command[2], checkout_date=command[3])
            is_valid_args = validator.validate_args(arguments)
        except IndexError:
            print("To few arguments")

        if is_valid_dates: #and is_valid_args:
            commands.append(command)
            print("OK")
        else:
            print("Command must be: <country> <city> <check_in_date> <check_out_date>")

    else:
        break


# TODO Create loop to loop through array of commands and start subprocesses
for com in commands:
    sp = subprocess.Popen(["python", "runner.py"] + com)