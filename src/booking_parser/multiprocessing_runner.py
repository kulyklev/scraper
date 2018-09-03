import subprocess
import sys
from helpers.validator import Validator

print("Enter booking-scraper commands and press 'Enter'")

validator = Validator()

for line in sys.stdin:
    if len(line) is not 1:
        line = line .strip()
        command = line.split(" ")

        # TODO Delete all. save only c_in date, c_out date and args
        if validator.validate_python(command[0]) and validator.validate_script_name(command[1]) and validator.validate_input(checkin_date=command[2], checkout_date=command[3]):
            print("OK")
        else:
            print("Not ok")
        # TODO Validate command array
        # TODO Add command array to array of commands

    else:
        break



# TODO Create loop to loop through array of commands and start subprocesses

# subprocess.Popen(["python", "runner.py", "Украина", "Никополь", "2018-12-12", "2018-12-13"])