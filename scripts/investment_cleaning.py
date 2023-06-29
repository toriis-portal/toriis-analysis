"""
This script is intended to clean CSV files resulting from FIOA request
for the University of Illinois Systems Office of Investments Annual Report
Appendix D. As such, the input CSV files are expected to have 6 lines of
header, and 6 columns: Account or Security, Coupon, Maturity Date,
Quantity, Cost Value, and Market Value. This script will clean this CSV
file and create an output CSV file called investment_fy<YEAR>
"""

from constants import COMPANY_NAMES 

import pandas as pd
import numpy as np
import yfinance as yf
import requests
import concurrent.futures

"""
Reading in Inputs from the Command Line
"""

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
for i in range (10):
    try:
        year_found = df.iloc[i][0].year
        break
    except:
        pass

if int(year) != int(year_found):
    print(f"Input Year {year} does not Match Year Found in Input CSV {year_found}")
    print(f"Would you like to update the year to {year_found}? (y/n)")
    if input().upper() == 'Y':
        print(f"Updating Year to {year_found}")
        year = year_found

output_file_path = f'../data/investments_fy{year}.csv'

"""
Processing Dataframe
"""
starting_index = -1
for i in range(10):
    try:
        if 'Account or Security' == df.iloc[i][0]:
            starting_index = i + 2
            break
    except:
        pass
if starting_index < 0:
    print("Could Not Find Entry 'Account or Security', Terminating the Script")
    quit()

df = pd.read_excel(input_file_path, parse_dates=True, skiprows=starting_index).dropna(how='all')

## Setting up the Operating Pool Dataframe
bank_i = df[df['Account or Security'].str.contains("9-200100", na=False)].index
op_i = df[df['Account or Security'].str.contains("Operating Funds Pool", na=False)].index
op_df = df.loc[bank_i[0]:op_i[1]-1]
op_df.insert(6, 'Bank', pd.NA)
op_df.insert(7, 'Asset Type', pd.NA)
op_df.insert(8, 'Company', pd.NA)
op_df.insert(9, 'Industry', pd.NA)
op_df.insert(10, 'Private Placement', False)
op_df.insert(11, 'Ticker', pd.NA)
op_df.insert(11, 'Info', object)

## Adding the bank and Asset Type to the Dataframe
bank_name = pd.NA
asset_type = pd.NA
for i in op_df.index:
    if np.isnan(op_df.loc[i]["Quantity"]):
        if "9-200100" in df.loc[i]["Account or Security"]:
            bank_name = df.loc[i]["Account or Security"]
        else:
            asset_type = df.loc[i]["Account or Security"]
    op_df.at[i,'Bank'] = bank_name
    op_df.at[i,'Asset Type'] = asset_type
op_df.head()

## Corporate Bonds Dataframe
cb_df = op_df[op_df['Asset Type'].str.contains("Corporate Bonds", na=False)]

## Clean Company Names
company_names = set()
for i in cb_df.index:
    # Set the Company to be cleaned
    cb_df.at[i,'Company'] = cb_df.at[i,'Account or Security']
    if not np.isnan(cb_df.at[i,'Quantity']):
        # clean private placement
        for prefix in ["PVTPL", "PVPTL", "PVYPL", "PVT PL", "PVPTL"]:
            if prefix in cb_df.loc[i]["Company"]:
                cb_df.at[i,'Private Placement'] = True
                cb_df.at[i,'Company'] = cb_df.at[i,'Company'][6:].strip()
        for end in [" CAP", " INC", " FDG", " CORP", " CO", " LLC", " CR", " SR", " A/S", " LP", " ASA", " LTD", ]:
            if end in cb_df.at[i, "Company"]:
                cb_df.at[i, "Company"] = cb_df.at[i, 'Company'].split(end)[0].strip()+" "+end
        for token in ['%']:
            if token in cb_df.at[i, "Company"]:
                # get everything before the token, then get everything before the last space
                cb_df.at[i, "Company"] = cb_df.at[i, "Company"].split(token)[0].rsplit(' ', 1)[0].strip()
        for key, value in COMPANY_NAMES.items():
            if key in cb_df.at[i, "Company"]:
                cb_df.at[i, "Company"] = value
        company_names.add(cb_df.at[i, "Company"])
    else:
        cb_df.drop(i, axis=0)


## Get Company Tickers
# taken from https://gist.github.com/bruhbruhroblox/dd9d981c8c37983f61e423a45085e063
def lookup_ticker(company_name):
    yfinance = "https://query2.finance.yahoo.com/v1/finance/search"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    params = {"q": company_name, "quotes_count": 1, "country": "United States"}

    res = requests.get(url=yfinance, params=params, headers={'User-Agent': user_agent})
    data = res.json()

    ticker = data['quotes'][0]['symbol']
    return ticker

def get_ticker(name):
    try:
        # try to get the ticker
        ticker = lookup_ticker(name)
    except:
        try:
            # shorten the name and try again
            short_name = name.split(' ')[0]
            ticker = lookup_ticker(short_name)
        except:
            # no ticker could be found, probably a private company, check by hand to make sure
            ticker = 'NO_TICKER_FOUND'
    return (name, ticker)

company_name_to_ticker = dict()
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(get_ticker, name) for name in company_names]
    for future in concurrent.futures.as_completed(futures):
        name, ticker = future.result()
        company_name_to_ticker[name] = ticker

## Match Company Name to Ticker in Dataframe
for i in cb_df.index:
    try:
        cb_df.at[i,'Ticker'] = company_name_to_ticker[cb_df.at[i,'Company']]
    except:
        assert cb_df.at[i,'Company'] == 'Corporate Bonds', f"Expected Cororate Bonds, got {cb_df.at[i,'Company']}"

## Get Company Info
def get_info_from_ticker(ticker):
    search_results = yf.Tickers(ticker)
    return search_results.tickers[ticker].info

def get_info(name):
    try:
        ticker = company_name_to_ticker[name]
        info = get_info_from_ticker(ticker)
    except:
        info = 'No Info Found'
    return (name, info)

## use parallelization to speed up this process
company_info_dict = dict()
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(get_info, name) for name in company_names]
    for future in concurrent.futures.as_completed(futures):
        name, info = future.result()
        company_info_dict[name] = info

"""
Output Results to File
"""
cb_df.to_csv(output_file_path)
print(f"Investment Processing are Done, Saving to File {output_file_path}")


"""
Investments Meta Information Output
"""
print("""Corporate Bond Totals""")
print("Cost Value\t",'${:,.2f}'.format(cb_df.sum(numeric_only=True)["Cost Value"]))
print("Market Value\t",'${:,.2f}'.format(cb_df.sum(numeric_only=True)["Market Value"]))