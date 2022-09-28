import requests
import json

requests.packages.urllib3.disable_warnings()

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
    cookie = "APIC-cookie="+ token
    return cookie

def get_tenants(cookie):
   url = "https://"+ APIC + "/api/node/class/fvTenant.json"   
   headers = {
      "Cookie" : f"{cookie}", 
   }
   response = requests.get(url, headers=headers, verify=False)
   return response.json()

def create_tenant(cookie, tenant_name):
    url = "https://"+ APIC +"/api/node/mo/uni.json"
    headers = {
        "Cookie" : f"{cookie}", 
    }
    
    payload = {
        "fvTenant": {
            "attributes": {
                "name": f"{tenant_name}",
                },
            "children": []
        }
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
    return response

#Main Function 
if __name__ == "__main__":
    cookie = apic_authenticate()
    response = get_tenants(cookie)

    for tenants in response["imdata"]:
      print(f"Tenant name: {tenants['fvTenant']['attributes']['name']}")

    response = create_tenant(cookie, "Python_TENANT")
    print ("Status Code: " + str(response.status_code))
   