from datetime import datetime

date_format = "%d-%m-%y"
CATEGORIES = {"I": "Income", "E": "Expenses"}

def get_date(prompt, allow_default=True):
    while True:
        date_str = input(prompt)
        if allow_default and not date_str:
            return datetime.today().strftime(date_format)
        try:
            valid_date = datetime.strptime(date_str, date_format)
            return valid_date.strftime(date_format)
        except ValueError:
            print("Invalid date format. Please enter in 'dd-mm-yy' format.")

def get_amount(prompt):
    while True:
        try:
            amount = float(input(prompt))
            if amount <= 0:
                raise ValueError("Amount must be greater than 0.")
            return amount
        except ValueError as e:
            print(e)

def get_category(prompt):
    while True:
        category = input(prompt).upper()
        if category in CATEGORIES:
            return CATEGORIES[category]
        print("Invalid category. Please enter 'I' for income or 'E' for expenses.")

def get_description(prompt):
    return input(prompt)
