from datetime import datetime


class Validator:
    def validate_input(self, checkin_date, checkout_date):
        if self.validate_date_format(checkin_date) and self.validate_date_format(checkout_date):
            if self.validate_after_today(checkin_date):
                if self.validate_dates(checkin_date, checkout_date):
                    return True
                else:
                    print("Check-out date must be after check-in date")
                    return False
            else:
                print("Check-in date must be after today or today")
                return False
        else:
            print("Incorrect data format, should be YYYY-MM-DD")
            return False

    def validate_date_format(self, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False
            # raise ValueError("Incorrect data format, should be YYYY-MM-DD")

    # Check if check in is today of after
    def validate_after_today(self, checkin):
        c_in = datetime.strptime(checkin, '%Y-%m-%d')
        td = datetime.today()
        if c_in.date() >= td.date():
            return True
        else:
            return False

    # Check if check-in is before check-out
    def validate_dates(self, checkin, checkout):
        c_in = datetime.strptime(checkin, '%Y-%m-%d')
        c_out = datetime.strptime(checkout, '%Y-%m-%d')
        if c_in.date() < c_out.date():
            return True
        else:
            return False

    # Check spelling of python word
    def validate_python(self, python_str):
        if python_str == "python":
            return True
        else:
            print("Incorrect spelling of 'python'")
            return False

    def validate_script_name(self, script_name):
        if script_name == "runner.py":
            return True
        else:
            print("Script name - 'runner.py'")
            return False