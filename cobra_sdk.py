
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.model.fv import Tenant
from cobra.model.pol import Uni
from cobra.mit.request import ConfigRequest
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

USERNAME = "admin"
PASSWORD = "cisco123"
APIC_URL = "https://10.17.87.60"

def apic_authenticate():
    moDir = MoDirectory(LoginSession(APIC_URL, USERNAME, PASSWORD))
    moDir.login()
    return moDir

def query_class(modir, object_class):
    object_set = modir.lookupByClass(object_class)
    return object_set

def create_tenant(modir, name):
    uniMo = Uni('')
    fvTenantMo = Tenant(uniMo, name)
    cfgRequest = ConfigRequest()
    cfgRequest.addMo(fvTenantMo)
    return modir.commit(cfgRequest)

if __name__ == "__main__":
    mo = apic_authenticate()
    response = query_class(mo, "fvTenant")
    for tenants in response:
        print(tenants.name)
    response = create_tenant(mo, "Cobra_Tenant")
    print (response.status_code)
    mo.logout()