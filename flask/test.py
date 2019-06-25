import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

url = "https://vrops.home.lab/suite-api/api/auth/token/acquire"

payload = "{\n    \"username\": \"admin\",\n    \"password\": \"Pa$$w0rd\"\n}"
headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    }
print(type(payload))

response = requests.request("POST", url, data=payload, headers=headers, verify=False)

print(response.text)