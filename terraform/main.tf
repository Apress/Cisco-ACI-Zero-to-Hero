terraform {
  required_providers {
    aci = {
      source = "ciscodevnet/aci"
    }
  }
}

#configure provider with your cisco aci credentials.
provider "aci" {
  # cisco-aci user name
  username = "admin"
  # cisco-aci password
  password = "cisco123"
  # cisco-aci APIC url
  url      = "https://10.17.87.60"
  insecure = true
}

# === TENANT POLICIES ===
# Create ACI Logical Application Policies - Tenant, VRF, BD, EPGs, Contracts and EPG to interface mapping

#Create Tenant Apress_Terraform
resource "aci_tenant" "Apress_Terraform_Tenant" {
  description = "Terraform Managed Tenant"
  name        = "Apress_Terraform"
  annotation  = "orchestrator:terraform"
}

resource "aci_vrf" "PROD" {
  tenant_dn              = aci_tenant.Apress_Terraform_Tenant.id
  name                   = "PROD"
  annotation             = "orchestrator:terraform"
}

resource "aci_bridge_domain" "Apress_FrontEnd_BD" {
  tenant_dn                   = aci_tenant.Apress_Terraform_Tenant.id
  description                 = "FrontEnd_BD"
  name                        = "FrontEnd_BD"
  optimize_wan_bandwidth      = "no"
  annotation                  = "orchestrator:terraform"
  arp_flood                   = "no"
  multi_dst_pkt_act           = "bd-flood"
  unicast_route               = "yes"
  unk_mac_ucast_act           = "flood"
  unk_mcast_act               = "flood"
}

resource "aci_subnet" "Apress_FrontEnd_BD_Subnet" {
  parent_dn        = aci_bridge_domain.Apress_FrontEnd_BD.id
  description      = "FrontEnd_BD_Subnet"
  ip               = "10.1.1.1/24"
  annotation       = "orchestrator:terraform"
  ctrl             = ["querier", "nd"]
  preferred        = "no"
  scope            = ["private", "shared"]
} 


resource "aci_application_profile" "Apress_AP" {
  tenant_dn    = aci_tenant.Apress_Terraform_Tenant.id
  name         = "Apress_AP"
  annotation   = "orchestrator:terraform"
  description  = "from terraform"
  name_alias   = "Apress_AP"
}

resource "aci_application_epg" "Apress_Frontend_EPG" {
    application_profile_dn  = aci_application_profile.Apress_AP.id
    name                    = "Apress_Frontend_EPG"
    description             = "from terraform"
    annotation              = "orchestrator:terraform"
    shutdown                = "no"
    relation_fv_rs_bd       = aci_bridge_domain.Apress_FrontEnd_BD.id
}
