import requests, json
from pathlib import Path

# NOTE! Substitute your own values for the following variables
# True = use personal access token for sign in, false = use username and password for sign in.
use_pat_flag = True

# Name or IP address of your installation of Tableau Server
server_name = "prod-apnortheast-a.online.tableau.com"
# API version of your server
version = "3.16"
# Site (subpath) to sign in to. An empty string is used to specify the default site.
site_url_id = "site id"

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
search APIを利用してworkbookの一覧を取得する
https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_concepts_filtering_and_sorting.htm
APIで一度に取得できる上限に限りがあるので注意

今回はワークブックのみを取得できれば良いので、フィルタの条件に加えています
"""
URI = f'https://{server_name}/api/-/search?filter=type:eq:workbook&limit=1000'
response = requests.get(URI, headers=headers)

f = open('file/wookbook_list_log.txt', 'w')
f.write(response.content.decode('utf-8'))

# Sign out
signout_url = f"https://{server_name}/api/{version}/auth/signout"

req = requests.post(signout_url, data=b'', headers=headers, verify=False)
req.raise_for_status()
print('Sign out successful!')