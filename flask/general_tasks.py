import requests, json, fnmatch, os
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# disable ssl warnings for self signed certs
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


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

    response = requests.request(
        "POST",
        url=url,
        headers=headers,
        auth=auth_values,
        data=json.dumps(json_payload),
        verify=False
    )

    return response


def get_list_of_json_files():
    """ This function builds a list of JSON files """
    list_of_files = os.listdir('static/json')
    pattern = '*.json'
    json_list = []
    for files in list_of_files:
        if fnmatch.fnmatch(files, pattern):
            json_list.append(files)
    return json_list


def get_task_status():
    headers = {'Accept': 'application/json'}
    url = 'http://localhost:5555/api/tasks'
    response = requests.request("GET", url=url, headers=headers, verify=False)
    tasks = json.loads(response.text)

    bg_tasks = {}

    i = 0
    while i < len(tasks):
        for task in tasks:
            name = tasks[task]['name']
            state = tasks[task]['state']
            runtime = tasks[task]['runtime']
            trace = tasks[task]['traceback']
            err = tasks[task]['exception']
            if runtime is not None:
                runtime = round(int(runtime), 4)
            bg_tasks.update({i: {'name': name , 'state': state, 'runtime': runtime, 'trace': trace, 'exception': err}})
            i = i + 1
    
    return bg_tasks