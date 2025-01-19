import pandas as pd
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }
        df = pd.DataFrame([new_entry])
        df.to_csv(cls.CSV_FILE, mode="a", header=False, index=False)
        print("Entry added successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT)

        start_date = datetime.strptime(start_date, cls.FORMAT)
        end_date = datetime.strptime(end_date, cls.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transaction found in the given date range")
        else:
            print(
                f"\nTransactions from {start_date.strftime(cls.FORMAT)} to {end_date.strftime(cls.FORMAT)}:"
            )
            print(
                filtered_df.to_string(
                    index=False, formatters={"date": lambda x: x.strftime(cls.FORMAT)}
                )
            )

            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expenses = filtered_df[filtered_df["category"] == "Expenses"]["amount"].sum()
            print("\nSummary:")
            print(f"Total Income: {total_income: .2f}")
            print(f"Total Expenses: {total_expenses: .2f}")
            print(f"Net Savings: {total_income - total_expenses: .2f}")

        return filtered_df


def add():
    CSV.initialize_csv()
    date = get_date(
        "Enter the date of the transaction (dd-mm-yyyy or press Enter for today's date): ",
    )
    amount = get_amount("Enter the amount: ")
    category = get_category("What is the category? ")
    description = get_description("Enter a description : ")
    CSV.add_entry(date, amount, category, description)


def plot_transaction(df):
    df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)  # Ensure the date column is datetime
    df.set_index("date", inplace=True)

    # Resample income data by day and fill missing dates with 0
    income_df = (
        df[df["category"] == "Income"]
        .resample("D")  # Corrected: Use a valid frequency string
        .sum()
        .reindex(df.index, fill_value=0)
    )

    # Resample expenses data by day and fill missing dates with 0
    expenses_df = (
        df[df["category"] == "Expenses"]  # Ensure category matches exactly
        .resample("D")  # Corrected: Use a valid frequency string
        .sum()
        .reindex(df.index, fill_value=0)  # Fixed missing parentheses
    )

    # Plot the income and expenses data
    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expenses_df.index, expenses_df["amount"], label="Expenses", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            
            # After viewing transactions, ask if the user wants to see the plot
            show_plot = input("Do you want to see a plot? (y/n): ").lower()
            if show_plot == "y":
                plot_transaction(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2, or 3.")



if __name__ == "__main__":
    main()
