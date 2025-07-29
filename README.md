# Finance Tracker

A command-line personal finance tracker with data analysis and visualization, built with Python. It supports transaction entry, file import/export (CSV/TSV), filtering, and the generation of charts and reports.

## Features

- Add income and expense transactions
- Load and save data from `.csv` or `.tsv` files
- Filter transactions by date and/or category
- View monthly summaries of income, expenses, and savings
- Export detailed analysis to `Analysis.tsv`
- Export filtered views to `Filter.tsv`
- Generate bar charts, pie charts, and line graphs of financial data

## Technologies Used

- Python 3
- `matplotlib`
- Built-in modules: `csv`, `datetime`, `os`, `calendar`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/finance-tracker.git
   cd finance-tracker

2. Install required dependencies:
    pip install -r requirements.txt

## Usage

Run the program from the command line:
    python main.py

You’ll be prompted to either load existing transactions from a file or manually input them. Afterward, you can choose to:
	•	Generate analysis reports
	•	Export filtered data
	•	Display charts (bar, pie, and line)

## File Format

Input files must be .csv or .tsv with the following header:
    Date,Txn Type,Amount,Category
or
    Date    Txn Type    Amount  Category

Example row:
    2025-07-01,expense,50.00,groceries

Output Files:
	•	Analysis.tsv: Summary of balances, income, expenses, and categorized monthly data.
	•	Filter.tsv: Filtered transactions based on date/category inputs.

## Sample Charts

The app includes:
	•	Bar chart of totals by category
	•	Pie chart of category proportions
	•	Line graph of income, expenses, and net savings over time

## File Structure

finance-tracker/
├── main.py                 # Main script (entry point)
├── README.md               # This file
└── requirements.txt        # Dependencies (matplotlib)
 
## Requirements

	•	Python 3.7+
	•	matplotlib
Install dependencies with:
    pip install matplotlib
Or use the provided requirements.txt.

## License

MIT License. See LICENSE for more information.

## Author

Gary Merisme Jr.
https://github.com/gmjr7735