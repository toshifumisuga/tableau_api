import pandas as pd
import xml.etree.ElementTree as et
import numpy as np

# 縦持ちのcsvの読み込み
inputFileName = "tag_file.csv"
df = pd.read_csv(inputFileName)

for i in range(len(df.index)):
    # XMLデータを生成
    rootXml = et.Element('tsRequest')
    # recordsXml = et.SubElement(rootXml, 'records')
    for iRow, row in df.iloc[[i],1:].iterrows():
        recordXml = et.SubElement(rootXml, 'tags')
        for iCol, column in df.iloc[[i],1:].iteritems():
            cellXml = et.SubElement(recordXml, iCol)

            # 文字列の場合はそのまま処理
            if type(row[iCol]) == str:
                cellXml.set('label', str(row[iCol]))
            # NULLの場合はスキップ
            elif np.isnan(row[iCol]) == True:
                pass
            # 数値の場合は、文字型に変換してセット
            else:
                cellXml.set('label', str(row[iCol]))

    #XMLとして出力
    outputFileName = f"file/tag_file_{df['view_wookbook_id'].at[i]}.xml"
    et.ElementTree(rootXml).write(outputFileName,encoding="unicode")
