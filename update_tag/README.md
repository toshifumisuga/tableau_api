## 概要
Tableau上にパブリッシュされたワークブックのtagを更新するためのファイルをまとめています

## 注意点
Tableau online側でサイト管理者権限を持っている  
or 
上記の方が発行したAccess Tokenを所持していることが前提です

詳細は下記を確認ください  
https://help.tableau.com/current/server/ja-jp/security_personal_access_tokens.htm#%E3%83%88%E3%83%BC%E3%82%AF%E3%83%B3%E3%81%AE%E6%9C%89%E5%8A%B9%E6%9C%9F%E9%99%90

>個人用アクセス トークン が 15 日連続で使用されない場合、そのトークンは期限切れになります。
>アクセス トークン が 15 日ごとよりも頻繁に使用される場合、トークンは 1 年後に期限切れになります。
>1 年後に新しいトークンを作成する必要があります。期限切れの個人用アクセス トークンは、[マイ アカウントの設定] ページには表示されません。

## tagの更新方法に関して
Tableu社のテクニカルサポートの方に確認しましたが、tag自体の上書き方法はありません  
よって、基本的にはtagを追加する、削除するという形でコードを書いています

## APIの詳細
tagの追加に関しては下記からご確認ください  
https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref.htm#add_tags_to_workbook

## 作業手順
1. tagを更新するためのCSVファイル(tag_file.csv)を作成してください  
tagを更新するためのworkbook idを取得する必要がありますが、API経由でしか取得できません  
そこでGUI上で確認できるView wookbook IDを取得してください  
例: https://prod-apnortheast-a.online.tableau.com/#/site/[site id]/workbooks/[View wookbook ID]]/views

2. get_wookbook_list_log.pyを実行してください
上記で示した通り、サイト上のworkbook idを取得するためのログファイルを取得します  
https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_concepts_filtering_and_sorting.htm  
APIで一度に取得できる上限に限りがあるので注意  
tagが付与されない場合、ワークブックの数が多すぎて一覧を取得できていない可能性があります

3. CSVファイルをxmlに変換します
TableauのAPIではxml形式で更新したいtag情報と、対象のworkbook idを渡す必要があります  
create_xml.pyを実行し、ファイルの整形を行ってください

4. add_tag_from_csv.pyを実行します
CSV内で指定されたワークブックに対して、記載されたtagが追加されます
