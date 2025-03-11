import csv
import os
import pandas_datareader.data as web
import datetime as dt

rows = []
with open('./stock_codes.csv', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    for row in reader:
        rows.append(row)
    number_of_rows = len(rows)
    for i in range(number_of_rows):
        file_name = str(rows[i])
        file_name = file_name.replace('[', '')
        file_name = file_name.replace(']', '')
        file_name = file_name.replace("'", '')
        print(file_name)

        start = '2023-07-03'  # 第二四半期の最初の営業日
        end = '2023-09-29'  # 第二四半期の最後の営業日

        # 終値の取得。
        ticker_symbol = file_name
        ticker_symbol_dr = ticker_symbol + '.JP'

        df_start = web.DataReader(
            ticker_symbol_dr, 'stooq', start=start, end=start)

        df_end = web.DataReader(ticker_symbol_dr, 'stooq', start=end, end=end)

        start_close = df_start['Close'][0]
        end_close = df_end['Close'][0]

        change_ratio = end_close / start_close  # 騰落率の計算

        with open('./2023Q2price.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([file_name, change_ratio])
