from google.cloud import language_v2
import csv
import os
import sys

rows = []

with open('./stock_codes.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    for row in reader:
        rows.append(row)
    number_of_rows = len(rows)
    for i in range(number_of_rows):
        file_name = str(rows[i])
        file_name = file_name.replace('[', '')
        file_name = file_name.replace(']', '')
        file_name_code = file_name.replace("'", '')
        file_name = './2023Q2text/' + file_name_code + '.txt'

        with open(file_name, 'r', encoding='utf-8-sig') as f:
            text = f.read()

            # 空白を削除
            text = text.replace(' ', '')

            # テキストを句点ごとに分割
            text_split = [s for s in text.split('。') if s]

            # １行目を削除
            text_split = text_split[1:]

            # テキストの感情分析
            for analyze_text in text_split:
                client = language_v2.LanguageServiceClient()
                document = language_v2.types.Document(
                    content=analyze_text, type_=language_v2.types.Document.Type.PLAIN_TEXT)
                sentiment = client.analyze_sentiment(
                    request={"document": document}).document_sentiment
                
                # 証券コードと数値化された感情を保存
                with open('2023Q2sentiment.csv', 'a', encoding='utf-8-sig', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(
                        [file_name_code, sentiment.score, sentiment.magnitude, analyze_text])
