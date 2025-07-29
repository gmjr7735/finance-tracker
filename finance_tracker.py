import csv
from datetime import datetime
import calendar
import os
import matplotlib.pyplot as plt


def yes_or_no(prompt):
    """
    Prompt the user with a yes/no question and return True for 'yes' and False for 'no'.

    Repeats until the user enters a valid response.

    Args:
        prompt (str): The question to prompt the user.

    Returns:
        bool: True if user answers 'yes', False if 'no'.
    """
    while True:
        user_input = input(prompt + ", yes or no? ")
        if user_input.lower() == "yes":
            return True
        elif user_input.lower() == "no":
            return False
        else:
            print("Invalid response")


class Transaction:
    """
    Represents a financial transaction.

    Attributes:
        date (datetime): The date of the transaction.
        txn_type (str): Type of transaction ('income' or 'expense').
        amount (float): Amount of money for the transaction.
        category (str): Category of the transaction.
    """
    def __init__(self, date, txn_type, amount, category):
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.txn_type = txn_type.strip().lower()
        self.amount = amount
        self.category = category

    def __str__(self):
        """Returns a formatted string representation of the transaction."""
        return f"[{self.date.date()}] {self.txn_type} ${self.amount:.2f} (Category: {self.category})"

    def __repr__(self):
        """Returns the string representation of the transaction."""
        return self.__str__()


class FinanceTracker:
    """
    Tracks and manages financial transactions.

    Attributes:
        transactions (list): List of Transaction objects.
    """
    def __init__(self):
        """Initializes the FinanceTracker with an empty list of transactions."""
        self.transactions = []

    def add_transaction(self, transaction):
        """Adds a transaction object to a list.

        Args:
            transaction (Transaction): the transaction to add.
        """
        self.transactions.append(transaction)

    def calc_current_balance(self):
        """
        Calculates the net balance (income - expenses).

        Returns:
            str: Net balance formatted to 2 decimal places.
        """
        income = 0
        expense = 0
        for transaction in self.transactions:
            if transaction.txn_type == "income":
                income += transaction.amount
            elif transaction.txn_type == "expense":
                expense += transaction.amount
        return f"{income - expense:.2f}"

    def get_total_income(self):
        """
        Calculates the total income.

        Returns:
            str: Total income formatted to 2 decimal places.
        """
        income = 0
        for transaction in self.transactions:
            if transaction.txn_type == "income":
                income += transaction.amount
        return f"{income:.2f}"

    def get_total_expenses(self):
        """
        Calculates total expenses.

        Returns:
            str: Total expenses formatted as a string with two decimal places.
        """
        expense = 0
        for transaction in self.transactions:
            if transaction.txn_type == "expense":
                expense += transaction.amount
        return f"{expense:.2f}"

    def category_filter(self, category):
        """
        Filters transactions by category.

        Args:
            category (str): The category to filter by.

        Returns:
            list: Transactions matching the specified category.
        """
        category_list = []
        for transaction in self.transactions:
            if transaction.category == category:
                category_list.append(transaction)
        return category_list

    def date_filter(self, date1, date2=None):
        """
        Filters transactions by a specific date or a range of dates.

        Args:
            date1 (str): Start date in "YYYY-MM-DD" format.
            date2 (str, optional): End date in "YYYY-MM-DD" format.

        Returns:
            list: Filtered transactions sorted by date.
        """
        date_list = []

        for transaction in self.transactions:
            if date2 is None:
                if transaction.date == datetime.strptime(date1, "%Y-%m-%d"):
                    date_list.append(transaction)
            else:
                start = datetime.strptime(date1, "%Y-%m-%d")
                end = datetime.strptime(date2, "%Y-%m-%d")
                if start <= transaction.date <= end:
                    date_list.append(transaction)

        date_list = sorted(date_list, key=lambda txn: txn.date)
        return date_list

    def _date_filter_by_type(self, date1, date2, filter):
        """
        Internal method to filter transactions by type and date.

        Args:
            date1 (str): Start date.
            date2 (str): End date.
            filter (str): 'income' or 'expense'.

        Returns:
            list: Filtered transactions sorted by date.
        """
        date_list = []
        for transaction in self.transactions:
            if transaction.txn_type == filter:
                if date2 is None:
                    if transaction.date == datetime.strptime(date1, "%Y-%m-%d"):
                        date_list.append(transaction)
                else:
                    start = datetime.strptime(date1, "%Y-%m-%d")
                    end = datetime.strptime(date2, "%Y-%m-%d")
                    if start <= transaction.date <= end:
                        date_list.append(transaction)

        date_list = sorted(date_list, key=lambda txn: txn.date)
        return date_list

    def date_income_filter(self, date1, date2):
        """Returns income transactions within a date range."""
        return self._date_filter_by_type(date1, date2, "income")

    def date_expense_filter(self, date1, date2):
        """Returns expense transactions within a date range."""
        return self._date_filter_by_type(date1, date2, "expense")

    def date_category_filter(self, date1, date2, category):
        """
        Filters transactions by category and date range.

        Args:
            date1 (str): Start date.
            date2 (str): End date.
            category (str): Category to filter.

        Returns:
            list: Filtered and sorted transactions.
        """
        date_list = []
        for transaction in self.transactions:
            if transaction.category == category:
                if date2 is None:
                    if transaction.date == datetime.strptime(date1, "%Y-%m-%d"):
                        date_list.append(transaction)
                else:
                    start = datetime.strptime(date1, "%Y-%m-%d")
                    end = datetime.strptime(date2, "%Y-%m-%d")
                    if start <= transaction.date <= end:
                        date_list.append(transaction)

        date_list = sorted(date_list, key=lambda txn: txn.date)
        return date_list


class Storage:
    """
    Handles reading and writing transactions to/from files.

    Attributes:
        tracker (FinanceTracker): The tracker to which data is added.
    """
    def __init__(self, tracker):
        self.tracker = tracker

    def read_transaction(self, filename):
        """
        Reads transactions from a CSV or TSV file and adds them to the tracker.

        Args:
            filename (str): The name of the file to read.
        """
        if filename.lower().endswith(".csv"):
            with open(filename, "r") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")
                next(csv_reader)
                for line in csv_reader:
                    date = line[0]
                    txn_type = line[1]
                    amount = round(float(line[2]), 2)
                    category = line[3]
                    read_txn = Transaction(date, txn_type, amount, category)
                    self.tracker.add_transaction(read_txn)
        elif filename.lower().endswith(".tsv"):
            with open(filename, "r") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter="\t")
                next(csv_reader)
                for line in csv_reader:
                    date = line[0]
                    txn_type = line[1]
                    amount = round(float(line[2]), 2)
                    category = line[3]
                    read_txn = Transaction(date, txn_type, amount, category)
                    self.tracker.add_transaction(read_txn)

    def append_transaction(self, filename, transaction):
        """
        Appends a new transaction to a CSV or TSV file.

        Args:
            filename (str): The file to write to.
            transaction (Transaction): The transaction to append.
        """
        file_is_new = not os.path.exists(filename)
        if filename.lower().endswith(".csv"):
            with open(filename, "a", newline="", encoding="utf-8") as csv_file:
                csv_append = csv.writer(csv_file, delimiter=",")
                titlenames = ["Date", "Txn Type", "Amount", "Category"]

                if file_is_new:
                    csv_append.writerow(titlenames)

                csv_append.writerow(
                    [
                        transaction.date.strftime("%Y-%m-%d"),
                        transaction.txn_type,
                        f"{transaction.amount:.2f}",
                        transaction.category,
                    ]
                )

        elif filename.lower().endswith(".tsv"):
            with open(filename, "a", newline="", encoding="utf-8") as csv_file:
                csv_append = csv.writer(csv_file, delimiter="\t")
                titlenames = ["Date", "Txn Type", "Amount", "Category"]

                if file_is_new:
                    csv_append.writerow(titlenames)

                csv_append.writerow(
                    [
                        transaction.date.strftime("%Y-%m-%d"),
                        transaction.txn_type,
                        f"{transaction.amount:.2f}",
                        transaction.category,
                    ]
                )


class ReportingAndAnalysis:
    """
    Provides functionality for analyzing, filtering, exporting, and visualizing financial transaction data.
    """
    def __init__(self, filename, tracker, use_file):
        """
        Initialize the ReportingAndAnalysis instance.

        Args:
            filename (str): Path to the file containing transaction data.
            tracker (FinanceTracker): Instance of FinanceTracker holding transactions.
            use_file (bool): Whether to sync from a file.
        """
        self.filename = filename
        self.tracker = tracker
        self.use_file = use_file

    def _sync_transactions(self):
        """
        Sync transactions from the file into the tracker if use_file is True.
        """
        if self.use_file:
            self.tracker.transactions = []
            storage = Storage(self.tracker)
            storage.read_transaction(self.filename)

    def _monthly_basis(self, txn_type):
        """
        Aggregate monthly totals for the specified transaction type.

        Args:
            txn_type (str): Either 'income' or 'expense'.

        Returns:
            dict: {(year, month): total_amount}
        """
        self._sync_transactions()
        all_txn = self.tracker.transactions
        months_dict = {}

        for txn in all_txn:
            tuple_date = (txn.date.year, txn.date.month)
            if txn.txn_type == txn_type:
                if tuple_date in months_dict:
                    months_dict[tuple_date] += txn.amount
                else:
                    months_dict[tuple_date] = txn.amount

        months_dict = dict(sorted(months_dict.items()))
        return months_dict

    def monthly_income(self):
        """Return monthly income totals."""
        return self._monthly_basis("income")

    def monthly_expenses(self):
        """Return monthly expense totals."""
        return self._monthly_basis("expense")

    def monthly_net_savings(self):
        """
        Calculate net savings per month.

        Returns:
            dict: {(year, month): income - expenses}
        """
        income_dict = self.monthly_income()
        expenses_dict = self.monthly_expenses()
        months_dict = {}

        for tuple_1, income in income_dict.items():
            for tuple_2, expense in expenses_dict.items():
                if tuple_1 == tuple_2:
                    months_dict[tuple_1] = income - expense

        months_dict = dict(sorted(months_dict.items()))
        return months_dict

    def _monthly_categories_basis(self, txn_type):
        """
        Aggregate monthly totals by category for a given transaction type.

        Args:
            txn_type (str): Either 'income' or 'expense'.

        Returns:
            dict: {((year, month), category): total_amount}
        """
        self._sync_transactions()
        all_txn = self.tracker.transactions
        months_dict = {}

        for txn in all_txn:
            tuple_1 = (txn.date.year, txn.date.month)
            tuple_2 = (tuple_1, txn.category)

            if txn.txn_type == txn_type:
                if tuple_2 in months_dict:
                    months_dict[tuple_2] += txn.amount
                else:
                    months_dict[tuple_2] = txn.amount

        months_dict = dict(sorted(months_dict.items()))
        return months_dict

    def monthly_income_categories(self):
        """Return monthly income grouped by category."""
        return self._monthly_categories_basis("income")

    def monthly_expenses_categories(self):
        """Return monthly expenses grouped by category."""
        return self._monthly_categories_basis("expense")

    def _totals_each_txn_type_category(self, txn_type):
        """
        Aggregate totals for each category of a given transaction type.

        Args:
            txn_type (str): Either 'income' or 'expense'.

        Returns:
            dict: {category: total_amount}
        """
        self._sync_transactions()
        all_txn = self.tracker.transactions
        txn_dict = {}

        for txn in all_txn:
            if txn.txn_type == txn_type:
                if txn.category in txn_dict:
                    txn_dict[txn.category] += txn.amount
                else:
                    txn_dict[txn.category] = txn.amount

        txn_dict = dict(sorted(txn_dict.items()))
        return txn_dict

    def totals_each_income_category(self):
        """Return total income for each category."""
        return self._totals_each_txn_type_category("income")

    def totals_each_expense_category(self):
        """Return total expense for each category."""
        return self._totals_each_txn_type_category("expense")

    def export_analysis(self):
        """
        Export various financial summaries and analyses to 'analysis.tsv'.
        """
        self._sync_transactions()
        monthly_net_savings_txns = self.monthly_net_savings()
        monthly_income_txns = self.monthly_income()
        monthly_expenses_txns = self.monthly_expenses()
        monthly_income_categories_txns = self.monthly_income_categories()
        monthly_expenses_categories_txns = self.monthly_expenses_categories()
        totals_each_income_category_txns = self.totals_each_income_category()
        totals_each_expense_category_txns = self.totals_each_expense_category()

        with open("analysis.tsv", "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter="\t")
            csv_writer.writerow(
                ["Current Balance:", self.tracker.calc_current_balance()]
            )
            csv_writer.writerow(["Total Income:", self.tracker.get_total_income()])
            csv_writer.writerow(["Total Expenses:", self.tracker.get_total_expenses()])
            csv_writer.writerow([])
            csv_writer.writerow(["Monthly Net Savings"])

            for tuple_date, total in monthly_net_savings_txns.items():
                tuple_year = tuple_date[0]
                tuple_month = tuple_date[1]
                csv_writer.writerow(
                    [f"{calendar.month_name[tuple_month]} {tuple_year}:", total]
                )

            csv_writer.writerow([])
            csv_writer.writerow(["Monthly Income"])

            for tuple_date, total in monthly_income_txns.items():
                tuple_year = tuple_date[0]
                tuple_month = tuple_date[1]
                csv_writer.writerow(
                    [f"{calendar.month_name[tuple_month]} {tuple_year}:", total]
                )

            csv_writer.writerow([])
            csv_writer.writerow(["Monthly Expenses"])

            for tuple_date, total in monthly_expenses_txns.items():
                tuple_year = tuple_date[0]
                tuple_month = tuple_date[1]
                csv_writer.writerow(
                    [f"{calendar.month_name[tuple_month]} {tuple_year}", total]
                )

            csv_writer.writerow([])
            csv_writer.writerow(["Totals for Each Income Category"])

            for cat, total in totals_each_income_category_txns.items():
                csv_writer.writerow([cat, f"{total:.2f}"])

            csv_writer.writerow([])
            csv_writer.writerow(["Totals for Each Expense Category"])

            for cat, total in totals_each_expense_category_txns.items():
                csv_writer.writerow([cat, f"{total:.2f}"])

            csv_writer.writerow([])
            csv_writer.writerow(["Monthly Income by Category"])

            for combined_tuple, total in monthly_income_categories_txns.items():
                tuple_2 = combined_tuple[0]
                cat = combined_tuple[1]
                tuple_year = tuple_2[0]
                tuple_month = tuple_2[1]
                csv_writer.writerow(
                    [cat, f"{calendar.month_name[tuple_month]} {tuple_year}", total]
                )

            csv_writer.writerow([])
            csv_writer.writerow(["Monthly Expenses by Category"])

            for combined_tuple, total in monthly_expenses_categories_txns.items():
                tuple_2 = combined_tuple[0]
                cat = combined_tuple[1]
                tuple_year = tuple_2[0]
                tuple_month = tuple_2[1]
                csv_writer.writerow(
                    [cat, f"{calendar.month_name[tuple_month]} {tuple_year}", total]
                )

    def export_filters(self, category, date1, date2=None):
        """
        Export various filters based on category and/or date range to 'filter.tsv'.

        Args:
            category (str): Transaction category to filter.
            date1 (str): Start date in YYYY-MM-DD.
            date2 (str, optional): End date in YYYY-MM-DD.
        """
        self._sync_transactions()
        category_filter_txns = self.tracker.category_filter(category)
        date_filter_txns = self.tracker.date_filter(date1, date2)
        date_income_filter_txns = self.tracker.date_income_filter(date1, date2)
        date_expense_filter_txns = self.tracker.date_expense_filter(date1, date2)
        date_category_filter_txns = self.tracker.date_category_filter(
            date1, date2, category
        )

        with open("filter.tsv", "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter="\t")
            csv_writer.writerow([f"Transactions filter: {category}"])

            for txn in category_filter_txns:
                txn = [
                    txn.date.strftime("%Y-%m-%d"),
                    txn.txn_type,
                    f"{txn.amount:.2f}",
                    txn.category,
                ]
                csv_writer.writerow(txn)

            csv_writer.writerow([])

            if date2 is None:
                csv_writer.writerow([f"Transactions on {date1}"])
            else:
                csv_writer.writerow([f"Transactions from {date1} to {date2}"])

            for txn in date_filter_txns:
                txn = [
                    txn.date.strftime("%Y-%m-%d"),
                    txn.txn_type,
                    f"{txn.amount:.2f}",
                    txn.category,
                ]
                csv_writer.writerow(txn)

            csv_writer.writerow([])

            if date2 is None:
                csv_writer.writerow([f"Income transactions on {date1}"])
            else:
                csv_writer.writerow([f"Income transactions from {date1} to {date2}"])

            for txn in date_income_filter_txns:
                txn = [
                    txn.date.strftime("%Y-%m-%d"),
                    txn.txn_type,
                    f"{txn.amount:.2f}",
                    txn.category,
                ]
                csv_writer.writerow(txn)

            csv_writer.writerow([])

            if date2 is None:
                csv_writer.writerow([f"Expense transactions on {date1}"])
            else:
                csv_writer.writerow([f"Expense transactions from {date1} to {date2}"])

            for txn in date_expense_filter_txns:
                txn = [
                    txn.date.strftime("%Y-%m-%d"),
                    txn.txn_type,
                    f"{txn.amount:.2f}",
                    txn.category,
                ]
                csv_writer.writerow(txn)

            csv_writer.writerow([])

            capital_category = category.capitalize()
            if date2 is None:
                csv_writer.writerow([f"{capital_category} transactions on {date1}"])
            else:
                csv_writer.writerow(
                    [f"{capital_category} transactions from {date1} to {date2}"]
                )

            for txn in date_category_filter_txns:
                txn = [
                    txn.date.strftime("%Y-%m-%d"),
                    txn.txn_type,
                    f"{txn.amount:.2f}",
                    txn.category,
                ]
                csv_writer.writerow(txn)

    def _chart_basis(self, method):
        """
        Prepare data for plotting charts.

        Args:
            method (dict): Dictionary of {category: total}

        Returns:
            tuple: (list of categories, list of totals)
        """
        totals_each_category_txns = method
        category_list = []
        totals_list = []

        for cat, total in totals_each_category_txns.items():
            capital_cat = cat.capitalize()
            category_list.append(capital_cat)
            totals_list.append(total)

        return category_list, totals_list

    def totals_each_income_category_bar_chart(self):
        """Display a bar chart of total income by category."""
        tuple_1 = self._chart_basis(self.totals_each_income_category())
        categories = tuple_1[0]
        totals = tuple_1[1]
        positions = []

        for num in range(len(categories)):
            positions.append(num)

        plt.figure(figsize=(7, 7))
        plt.bar(positions, totals, width=0.5)
        plt.xticks(positions, categories)
        plt.xlabel("Categories")
        plt.ylabel("Dollars ($)")
        plt.title("Totals for Each Income Category")
        plt.show()
        plt.close()

    def totals_each_expense_category_bar_chart(self):
        """Display a bar chart of total expenses by category."""
        tuple_1 = self._chart_basis(self.totals_each_expense_category())
        categories = tuple_1[0]
        totals = tuple_1[1]
        positions = []

        for num in range(len(categories)):
            positions.append(num)

        plt.figure(figsize=(len(categories) * 1.67 + 4, 7))
        plt.bar(positions, totals, width=0.5)
        plt.xticks(positions, categories)
        plt.xlabel("Categories")
        plt.ylabel("Dollars ($)")
        plt.title("Totals for Each Expense Category")
        plt.show()
        plt.close()

    def totals_each_income_category_pie_chart(self):
        """Display a pie chart showing income category distribution."""
        tuple_1 = self._chart_basis(self.totals_each_income_category())
        categories = tuple_1[0]
        totals = tuple_1[1]
        explode = []
        num = 0
        for i in range(len(totals)):
            explode.append(num)
            num += 0.045
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.pie(
            totals, labels=categories, autopct="%.2f%%", startangle=90, explode=explode
        )
        ax.set_title("Percent for Each Income Category", y=1.07)
        plt.show()
        plt.close()

    def totals_each_expense_category_pie_chart(self):
        """Display a pie chart showing expense category distribution."""
        tuple_1 = self._chart_basis(self.totals_each_expense_category())
        categories = tuple_1[0]
        totals = tuple_1[1]
        explode = []
        num = 0
        increment = 0.075

        for i in range(len(totals)):
            explode.append(num)
            increment *= 0.7
            num += increment
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.pie(
            totals,
            labels=categories,
            autopct="%.2f%%",
            startangle=90,
            explode=explode,
        )
        ax.set_title("Percent for Each Expense Category", y=1.07)
        plt.show()
        plt.close()

    def monthly_income_and_expenses_line_graph(self):
        """Plot a line graph of monthly income, expenses, and net savings."""
        income_data = self.monthly_income()
        expenses_data = self.monthly_expenses()
        net_savings_data = self.monthly_net_savings()
        x_income = []
        y_income = []
        x_expense = []
        y_expense = []
        x_net = []
        y_net = []

        for tuple_date, value in income_data.items():
            year = tuple_date[0]
            month = tuple_date[1]
            month = calendar.month_name[month]
            month_year = f"{month} {year}"
            x_income.append(month_year)
            y_income.append(value)

        for tuple_date, value in expenses_data.items():
            year = tuple_date[0]
            month = tuple_date[1]
            month = calendar.month_name[month]
            month_year = f"{month} {year}"
            x_expense.append(month_year)
            y_expense.append(value)

        for tuple_date, value in net_savings_data.items():
            year = tuple_date[0]
            month = tuple_date[1]
            month = calendar.month_name[month]
            month_year = f"{month} {year}"
            x_net.append(month_year)
            y_net.append(value)

        plt.figure(figsize=(10, 7))
        plt.plot(
            x_income,
            y_income,
            label="Monthly Income",
            marker="o",
            markerfacecolor="red",
        )
        plt.plot(
            x_expense,
            y_expense,
            label="Monthly Expenses",
            marker="o",
            markerfacecolor="red",
        )
        plt.plot(x_net, y_net, label="Net Savings", marker="o", markerfacecolor="red")
        plt.xlabel("Months")
        plt.ylabel("Dollars ($)")
        plt.title("Monthly Incomes, Expenses, and Net Savings")
        plt.legend()
        plt.show()
        plt.close()


def main():
    """
    Main interactive loop for the finance tracking application.

    Workflow:
    - Ask user if they have an existing CSV/TSV file of transactions.
        - If yes, prompt for filename and load transactions using Storage.
        - If no, prepare to create new transactions without loading from file.
    - Optionally, ask user if they want to enter new transactions manually.
        - For each transaction, prompt for date, type, amount, and category.
        - Save entered transactions to the specified file (creating one if needed).
    - After input, optionally generate analysis TSV report.
    - Optionally export filtered transactions based on category and date range.
    - Optionally create and display charts of income/expense data.

    Assumes:
    - Storage, FinanceTracker, ReportingAndAnalysis classes exist and work as expected.
    - yes_or_no is a utility function that returns True/False from user input.
    - Dates are entered in 'YYYY-MM-DD' format.
    """
    tracker = FinanceTracker()
    storage = Storage(tracker)

    # Check if user has existing CSV/TSV file and load transactions if so
    while True:
        has_csv = yes_or_no("Do you have a CSV or TSV file")
        if has_csv:
            while True:
                filename = input("Enter file name (with .csv or .tsv at the end): ")
                if filename.lower().endswith(".csv") or filename.lower().endswith(".tsv"):
                    try:
                        storage.read_transaction(filename)
                    except FileNotFoundError:
                        print('File not found.')
                        continue
                    break
                else:
                    print("Invalid file name.")
            report = ReportingAndAnalysis(filename, tracker, use_file=True)
        else:
            filename = None
            report = ReportingAndAnalysis(filename, tracker, use_file=False)
        break

    i = 0
    inputting_txn = yes_or_no("Would you like to enter a transaction")
    if inputting_txn:
        i += 1
    # If entering transactions and no file was specified, prompt for filename
    if inputting_txn and filename is None:
        while True:
            filename = input(
                "Enter a file name to save your transactions (with .csv or .tsv at the end): "
            )
            if filename.lower().endswith(".csv") or filename.lower().endswith(".tsv"):
                break
            else:
                print("Invalid file name.")

     # Input transactions loop
    while inputting_txn:
        # Validate date input
        while True:
            try:
                date = input("Enter date of transaction (YYYY-MM-DD): ")
                datetime.strptime(date, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date.")

        # Validate transaction type input
        txn_type_input = True
        while txn_type_input:
            txn_type = input("Enter the type of transaction (income or expense): ")
            txn_type = txn_type.lower()
            if txn_type == "income" or txn_type == "expense":
                txn_type_input = False
            else:
                print("Invalid type of transaction.")

        # Validate amount input
        while True:
            try:
                amount = float(input("Enter amount of money: "))
                break
            except ValueError:
                print("Invalid amount.")

        category = input("Enter category of transaction: ")
        category = category.lower()
        new_txn = Transaction(date, txn_type, amount, category)
        tracker.add_transaction(new_txn)
        storage.append_transaction(filename, new_txn)
        inputting_txn = yes_or_no("Would you like to enter another transaction")

    # If any data was loaded or entered, prompt for analysis and filtering
    if has_csv or i > 0:
        inputting_analysis = yes_or_no("Would you like an analysis TSV file")

        if inputting_analysis:
            report.export_analysis()

        inputting_filter = yes_or_no("Would you like a filtered TSV file")

        if inputting_filter:
            category = input("Enter category of transaction: ")
            category = category.lower()
            # Validate start date
            while True:
                try:
                    date1 = input("Enter start date (YYYY-MM-DD): ")
                    datetime.strptime(date1, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Invalid date.")

            # Validate optional end date
            while True:
                try:
                    date2 = input(
                        "Enter end date (YYYY-MM-DD). Press enter if no end date. "
                    )
                    if date2 == "":
                        date2 = None
                        break
                    datetime.strptime(date2, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Invalid date.")

            report.export_filters(category, date1, date2)

        create_chart = yes_or_no("Would you like some charts")

        if create_chart:
            report.totals_each_income_category_bar_chart()
            report.totals_each_expense_category_bar_chart()
            report.totals_each_income_category_pie_chart()
            report.totals_each_expense_category_pie_chart()
            report.monthly_income_and_expenses_line_graph()


if __name__ == "__main__":
    main()
