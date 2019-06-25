import requests
import ssl
import json
from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def test_vrops_connect(vropshost, vropsuser, vropspass):
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    new_url = "https://" + vropshost + '/suite-api/api/auth/token/acquire'
    payload = json.dumps({'username': vropsuser, 'password': vropspass})
    response = requests.request("POST", url=new_url, data=payload, headers=headers, verify=False)
    return response.status_code

def test_vcenter_connect(vchost, vcuser, vcpass):
    port = 443
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE
    service_instance = connect.SmartConnect(host=vchost, user=vcuser, pwd=vcpass, port=int(port), sslContext=context)
    if service_instance:
        return 200
    else:
        return 401



# vc_host = 'vc01.home.lab'
# vc_user = 'administrator@vsphere.local'
# vc_pwd = 'pass'

# test_vcenter_connect(vc_host, vc_user, vc_pwd)