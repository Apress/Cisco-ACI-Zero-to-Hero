import requests
import json
import ssl
import websocket
import threading
import time
import sys

requests.packages.urllib3.disable_warnings()

# APIC Credentials:
APIC = "10.17.87.60"
USER = "admin"
PASS = "cisco123"

AUTH_URL = "https://" + APIC + "/api/aaaLogin.json"
AUTH_BODY = {"aaaUser": {"attributes": {"name": USER, "pwd": PASS}}}

#Authentication to APIC
def apic_authenticate():
    login_response = requests.post(AUTH_URL, json=AUTH_BODY, verify=False).content
    response_body_dictionary = json.loads(login_response)
    token = response_body_dictionary["imdata"][0]["aaaLogin"]["attributes"]["token"]
    cookie = {"APIC-cookie": token}
    return cookie

# Subscribe to Apress Tenant
def subscribe(cookie):
    apress_tenant_url = "https://" + APIC + "/api/node/mo/uni/tn-Apress.json?subscription=yes&refresh-timeout=60"    
    apress_tenant_subscription = requests.get(apress_tenant_url, verify=False, cookies=cookie)
    json_dict = json.loads(apress_tenant_subscription.text)
    apress_tenant_subscription_id = json_dict["subscriptionId"]
    print("Subscription ID: ", apress_tenant_subscription_id)
    return apress_tenant_subscription_id

# Create Web Socket to APIC
def ws_socket(token):
    websocket_url = "wss://" + APIC + "/socket{}".format(token)
    ws = websocket.create_connection(websocket_url, sslopt={"cert_reqs": ssl.CERT_NONE})
    print("WebSocket Subscription Status Code: ", ws.status)
    return ws

#Thread definition and start
def thread_start(ws, subscription_id, cookie):
    thread1 = threading.Thread(target=print_ws, args=(ws,))
    thread2 = threading.Thread(target=refresh, args=(subscription_id, cookie, ))
    thread1.start()
    thread2.start()

#Print any new message in Subcription queue
def print_ws(ws):
    while True:
        print(ws.recv())

# Refresh subscription ID
def refresh(subscription_id, cookie):
    while True:
        time.sleep(30)
        refresh_id = "https://" + APIC + "/api/subscriptionRefresh.json?id={}".format(subscription_id)
        refresh_id = requests.get(refresh_id, verify=False, cookies=cookie)

#Main Function 
if __name__ == "__main__":
    cookie = apic_authenticate()
    token =  (cookie["APIC-cookie"])
    print ("*" * 10, "WebSocket Subscription Status & Messages", "*" * 10)
    wbsocket = ws_socket(token)
    subscription_id = subscribe(cookie)
    thread_start(wbsocket, subscription_id, cookie)