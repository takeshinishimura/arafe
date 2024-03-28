import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog

# ルートウィンドウを作成
root = tk.Tk()
root.withdraw()  # ルートウィンドウを表示しないように設定

# ファイルを選択してファイルパスを取得
file_path = filedialog.askopenfilename(title="ファイルを選択してください", filetypes=[("CSV files", "*.csv")])

# ファイルが選択されたかを確認
if file_path:
    # CSVファイルをデータフレームとして読み込む
    d1 = pd.read_csv(file_path, sep=",", dtype=str)
    print("ファイルが正常に読み込まれました。")
else:
    print("ファイルが選択されませんでした。")

# ルートウィンドウを破棄
root.destroy()

d1 = d1.iloc[:, 1:]
d2 = pd.DataFrame()

# 行ごとにデータを処理して新しいデータフレームに追加
for index, row in d1.iterrows():
    score_name = row[0]
    num_columns = len(row)
    data_to_add = []

    # 列ごとにデータを処理してリストに追加
    for i in range(0, num_columns, 5):
        if i + 5 < num_columns:
            report_number = row[i + 1]
            acceptance = row[i + 2]
            clarity = row[i + 3]
            significance = row[i + 4]
            achievement = row[i + 5]

            if pd.isna(report_number):
                break

            data_to_add.append([score_name, report_number, acceptance, clarity, significance, achievement])

    # 新しいデータフレームにデータを追加
    d2 = pd.concat([d2, pd.DataFrame(data_to_add, columns=['採点者名', '報告番号', '個別報告論文の採択の見込み', '報告の明解さ', '研究内容の意義', '研究内容の達成度'])], ignore_index=True)

# 合計列を追加
d2['合計'] = d2[['報告の明解さ', '研究内容の意義', '研究内容の達成度']].astype(float).sum(axis=1)

# 報告番号のユニークな値を取得
No = d2['報告番号'].unique()

# 平均列を持つデータフレームを作成
d3 = pd.DataFrame({'No': No, '平均': None})

for i in No:
    d3.loc[d3['No'] == i, '平均'] = round(d2[d2['報告番号'] == i]['合計'].mean(), 1)

d3 = d3.sort_values(by='平均', ascending=False)

# 集計結果のデータフレームを作成
result = pd.DataFrame(columns=d2.columns.tolist() + ['平均'])

for i in d3['No']:
    result = pd.concat([result, d2[d2['報告番号'] == i]], ignore_index=True)
result['平均'] = d3.set_index('No')['平均'].loc[result['報告番号'].values].values

result.to_html('result.html')
