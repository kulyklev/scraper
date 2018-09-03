import subprocess
import sys
from helpers.validator import Validator

print("Enter booking-scraper commands and press 'Enter'")

for line in sys.stdin:
    if len(line) is not 1:
        # TODO Convert string into array of args
        # TODO Validate array of args
        # TODO Add array of args to array of commands

    else:
        break



# TODO Create loop to loop through array of commands and start subprocesses

# subprocess.Popen(["python", "runner.py", "Украина", "Никополь", "2018-12-12", "2018-12-13"])