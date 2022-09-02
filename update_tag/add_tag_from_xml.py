import requests, json
import shutil
import os
import re
from modify_wookbook_list_log import get_workbook_id_dict

# NOTE! Substitute your own values for the following variables
use_pat_flag = True  # True = use personal access token for sign in, false = use username and password for sign in.

server_name = "prod-apnortheast-a.online.tableau.com"   # Name or IP address of your installation of Tableau Server
version = "3.16"     # API version of your server
site_url_id = "istyle"    # Site (subpath) to sign in to. An empty string is used to specify the default site.

# For username and password sign in
user_name = "USERNAME"    # User name to sign in as (e.g. admin)
password = "{PASSWORD}"

# For Personal Access Token sign in
# Name of the personal access token.
personal_access_token_name = "発行したトークン名を入力してください"
# Value of the token.
personal_access_token_secret = "パスワードを入力してください"

signin_url = "https://{server}/api/{version}/auth/signin".format(server=server_name, version=version)

if use_pat_flag:
	payload = { "credentials": { "personalAccessTokenName": personal_access_token_name, "personalAccessTokenSecret": personal_access_token_secret, "site": {"contentUrl": site_url_id }}}

	headers = {
		'accept': 'application/json',
		'content-type': 'application/json'
	}

else:
	payload = { "credentials": { "name": user_name, "password": password, "site": {"contentUrl": site_url_id }}}

	headers = {
		'accept': 'application/json',
		'content-type': 'application/json'
	}

# Send the request to the server
req = requests.post(signin_url, json=payload, headers=headers, verify=False)
req.raise_for_status()

# Get the response
response = json.loads(req.content)

# Get the authentication token from the credentials element
token = response["credentials"]["token"]

# Get the site ID from the <site> element
site_id = response["credentials"]["site"]["id"]

print('Sign in successful!')


headers = {
    'X-Tableau-Auth': token
}


"""
更新対象のworkbook_idの辞書を取得する関数は、modify_wookbook_list_log.pyで作成済み
その関数を利用して、作成されたxmlファイルを順に読み込み、tagとして更新させる

処理の完了後、今回コードによって作成したフォルダを削除する
"""
for key, value in get_workbook_id_dict().items():
    with open(f'file/tag_file_{key}.xml', 'r')as f:
        file_open = f.read().replace('\n', '')
        file_open = re.sub('<tag\.\d', '<tag ', file_open)

    URI = f'https://{server_name}/api/{version}/sites/{site_id}/workbooks/{value}/tags'
    response = requests.put(URI, headers=headers, data=file_open)

shutil.rmtree('file/')
"""
処理の完了後、サインアウトする
"""
signout_url = f"https://{server_name}/api/{version}/auth/signout"

req = requests.post(signout_url, data=b'', headers=headers, verify=False)
req.raise_for_status()
print('Sign out successful!')