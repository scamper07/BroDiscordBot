# 1. make api call
# 2. update twitch_app_access file
# 3. update twitch_client_id

import requests
import os

api = "https://twitchtokengenerator.com/api/refresh/"
refresh_token = ""

api_url = api+refresh_token

resp = requests.get(api_url)
print(resp.status_code)
if resp.status_code == 200:
    data = resp.json()
    print(data)
    if data['success'] == True:
        cmd_access = "echo -n \"%s\" > twitch_app_access" % data['token']
        os.system(cmd_access)
        cmd_client = "echo -n \"%s\" > twitch_client_id" % data['client_id']
        os.system(cmd_client)


