# this script has not been properly tested. use with care.

import sys
from _restobject import RestObject

def ex17_mount_virtual_media_iso(restobj, iso_url, boot_on_next_server_reset):
    sys.stdout.write("\nAdding .iso to boot order.\n")
    instances = restobj.search_for_type("Manager.")

    for instance in instances:
        rsp = restobj.rest_get(instance["href"])
        rsp = restobj.rest_get(rsp.dict["links"]["VirtualMedia"]["href"])

        for vmlink in rsp.dict["links"]["Member"]:
            response = restobj.rest_get(vmlink["href"])

            if response.status == 200 and "DVD" in response.dict["MediaTypes"]:
                body = {"Image": iso_url}
                
                if (iso_url is not None and \
                                        boot_on_next_server_reset is not None):
                    body["Oem"] = {"Hp": {"BootOnNextServerReset": \
                                                    boot_on_next_server_reset}}
    
                    response = restobj.rest_patch(vmlink["href"], body)
                    restobj.error_handler(response)
            elif response.status != 200:
                restobj.error_handler(response)
if __name__ == "__main__":
    iLO_https_url = "https://servername.oob.hydra.lab"
    iLO_account = "Administrator"
    iLO_password = "password"
    
    REST_OBJ = RestObject(iLO_https_url, iLO_account, iLO_password)
    ex17_mount_virtual_media_iso(REST_OBJ, "http://cluster.hydra.lab/pxe/images/ubuntu16-preseed.iso", True)
    
