import requests
import csv
import time
from bs4 import BeautifulSoup

path = './stock_codes.csv'
with open(path, encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    for row in reader:

        # 証券コードを取得
        stock_code = row
        stock_code_str = str(stock_code)
        stock_code_str = stock_code_str.replace('[', '')
        stock_code_str = stock_code_str.replace("'", '')
        stock_code_str = stock_code_str.replace(']', '')

        # 取得したい企業のアドレスを生成
        url = 'https://www.nikkei.com/markets/kigyo/money-schedule/kessan/ResultFlag=3&kwd=' + stock_code_str

        # 決算日をスクレイピング
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        date_list = soup.select('th')
        print(date_list[8:])
        i = date_list[8:]
        date = str(i)

        # タグを削除
        date = date.replace('[', '')
        date = date.replace('<', '')
        date = date.replace('t', '')
        date = date.replace('h', '')
        date = date.replace('>', '')
        date = date.replace(']', '')
        with open('./2024Q3date.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([stock_code_str, date])
        time.sleep(1)
