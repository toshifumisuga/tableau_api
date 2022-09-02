import json
import re
import pandas as pd
import numpy as np

'''
APIを叩いて取得したログから、workbook_idの辞書を作成する
'''
# 縦持ちのcsvの読み込み
inputFileName = "tag_file.csv"
df = pd.read_csv(inputFileName)

def get_workbook_id_dict():
    # APIを叩いて取得したログの整形を行う
    f = open('file/wookbook_list_log.txt', 'r')
    str_data = json.loads(f.read())
    str_data = json.dumps(str_data['hits'])
    str_data = json.loads(str_data).get('items')

    # workbook_idのログを取得するために、正規表現を利用する
    workbook_id = r'workbook:(.*)'

    # ループを利用するために空の辞書を用意する
    empty_dict = {}
    for loop_cnt in range(len(str_data)):
        # ログ上にはtag付けが必要ないファイルも多数含まれているので、必要なものだけを辞書にする
        if np.all(str_data[loop_cnt]['content']['id'] in df.values) == False:
            pass
        else:
            # GUI上で確認できるView workbook IDからAPI上に渡すためのworkbook IDの取得
            empty_dict[str_data[loop_cnt]['content']['id']] = re.search(workbook_id, str_data[loop_cnt]['uri']).group(1)
    return empty_dict