"""
This script is intended to clean CSV files resulting from FIOA request
for the University of Illinois Systems Office of Investments Annual Report
Appendix D. As such, the input CSV files are expected to have 6 lines of
header, and 6 columns: Account or Security, Coupon, Maturity Date,
Quantity, Cost Value, and Market Value. This script will clean this CSV
file and create an output CSV file called investment_fy<YEAR>
"""

import pandas as pd

print("Welcome to the Investment Cleaning Scripts. Please answer the following prompts so we may process your data.\n")
print("Investment CSV File to be Cleaned (make sure the file is in the data directory)")
input_file = input()
input_file_path = "../data/" + input_file
while 1:
    try:
        df = pd.read_excel(input_file_path, parse_dates=True).dropna(how='all')
        break
    except FileNotFoundError:
        print(f"No such file or directory: '../data/{input_file}'")
        print("Please enter a valid file path")
        input_file = input()
        input_file_path = "../data/" + input_file
print("Fiscal Year of Annual Report (in YYYY format)")
year = input()
year_found = df.iloc[2][0].year
if year != year_found:
    print(f"Input Year {year} does not Match Year Found in Input CSV {year_found}")
    print(f"Would you like to update the year to {year_found}? (y/n)")
    if input().upper() == 'Y':
        print(f"Updating Year to {year_found}")
        year = year_found
