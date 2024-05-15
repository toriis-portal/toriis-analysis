# Populating 2023 Data into a CSV

This is the (crude) first draft of documentation for the 2023 data pipeline!

How this works:

- All the input/output dataframes that the scripts operate with are located in the directory data-2023/in/ and data-2023/out/.
- To follow the pipeline, drag/drop the new year's investment portfolio .CSV file into data-2023/in/.
- Follow 01-clean.ipynb and 02-populate-tickers.ipynb respectively.
- The final dataframe, will be populated as 'data-2023/out/df*with_ticker*...csv'. Please replicate this process and compare your results with 'data-2023/out/master_df_with_ticker.csv', which is the final dataframe that I uploaded to MongoDB.
