import requests
import json
import datetime

def dice_transmit(api_key, api_secret, json_file):
    api_key = api_key
    api_secret = api_secret
    json_file = json_file
    auth_values = (api_key, api_secret)
    url = "https://www.dicevm.com/api/businessmodel/json"
    headers = {
        "Content-Type": "application/json",
        "api_key": api_key,
        "api_secret": api_secret
        }

    with open('static/json/' + json_file, 'r') as j:
        json_payload = json.load(j)

    # response = requests.request("POST", url=url, headers=headers, auth=auth_values, data=json_payload, verify=False)

    return 'complete'
