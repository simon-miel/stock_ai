import requests
import csv
import unicodedata
import time
import os
import pandas as pd
from bs4 import BeautifulSoup

# 決算速報を保存するフォルダを直下に作成
new_dir_path = './2023Q3text'
# os.mkdir(new_dir_path)

# 二重リストを通常のリストにする関数


def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result += flatten(item)
        else:
            result.append(item)
    return result


path = './stock_codes.csv'  # 証券コードを保存しているファイル
with open(path, encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    for row in reader:
        stock_code = row
        stock_code_str = str(stock_code)
        stock_code_str = stock_code_str.replace('[', '')
        stock_code_str = stock_code_str.replace("'", '')
        stock_code_str = stock_code_str.replace(']', '')

        # 決算速報を取得
        url = "https://kabutan.jp/stock/news?code=" + stock_code_str + "&nmode=2"
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')
        h1 = soup.find(id="news_contents")

        # テーブル要素を取得
        table_elements = h1.find('table')

        # テーブルの内容をリストとして保存
        table_data = []

        for tr in table_elements.find_all('tr'):
            row_data = []
            for td in tr.find_all('td'):
                row_data.append(td.text)
                link = td.find("a")
                if link:
                    href = link.get("href")
                    row_data.append(href)
            table_data.append(row_data)
        df = pd.DataFrame(table_data)

        # 決算に関係する行を取得
        target_value = '決算'
        filtered_df = df[df[1] == target_value]

        # データフレームをリストに変換
        table_data = filtered_df.values.tolist()
        table_data_list = flatten(table_data)

        # 指定の決算シーズンの決算速報を検索
        empty_list = []
        search_value = "24/09"
        index_list = [i for i, e in enumerate(
            table_data_list) if search_value in e]
        if index_list == empty_list:
            search_value = "24/10"
            index_list = [i for i, e in enumerate(
                table_data_list) if search_value in e]
            if index_list == empty_list:
                search_value = "24/11"
                index_list = [i for i, e in enumerate(
                    table_data_list) if search_value in e]
                if index_list == empty_list:
                    search_value = "24/12"
                    index_list = [i for i, e in enumerate(
                        table_data_list) if search_value in e]

        # 指定の決算シーズンの決算速報のURLを生成
        target_url_number = index_list[0] + 3
        target_url = table_data_list[target_url_number]
        target_url = "https://kabutan.jp" + target_url

        # 決算速報を取得
        response = requests.get(target_url)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')
        article = soup.find_all("div", class_='body')
        article = article[0]

        # 全てのaタグを削除
        for a in article.find_all('a'):
            a.decompose()

        # タグを削除
        article = article.get_text()
        article = article.replace('\n', '')
        article = article.replace('<>', '')
        article = article.replace('株探ニュース', '')
        article = article.replace(' ', '')

        # 全角の数字や記号を全て半角に変換
        article = unicodedata.normalize('NFKC', article)

        # time.sleep(1)

        # 決算速報をテキストファイルとして保存
        path = './2024Q3text/' + stock_code_str + '.txt'
        with open(path, 'w', encoding='utf-8-sig') as f:
            f.write(article)
