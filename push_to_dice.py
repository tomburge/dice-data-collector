import requests
import json
import datetime

def dice_transmit():
    api_key = ''
    api_secret = ''
    auth_values = (api_key, api_secret)
    url = "https://www.dicevm.com/api/businessmodel/json"
    headers = {
        "Content-Type": "application/json",
        "api_key": api_key,
        "api_secret": api_secret
        }

    dice_file = 'dice_vrops_output_' + str(datetime.date.today()) + '.json'

    with open('static/json/' + dice_file, 'r') as j:
        json_payload = json.load(j)

    # response = requests.request("POST", url=url, headers=headers, auth=auth_values, data=json_payload, verify=False)

    return 'complete'
