import requests
import ssl
import json, sys
from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def test_vrops_connect(vropshost, vropsuser, vropspass, vropsport):
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    new_url = "https://" + vropshost + ':' + vropsport + '/suite-api/api/auth/token/acquire'
    print(new_url)
    payload = json.dumps({'username': vropsuser, 'password': vropspass})
    response = requests.request("POST", url=new_url, data=payload, headers=headers, verify=False)
    return response.status_code

def test_vcenter_connect(vchost, vcuser, vcpass, vcport):
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE
    try:
        service_instance = connect.SmartConnect(host=vchost, user=vcuser, pwd=vcpass, port=int(vcport), sslContext=context)
        if service_instance:
            return 200
    except Exception:
        return 401
        
