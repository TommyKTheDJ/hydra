# this script has not been properly tested. use with care

import sys
from _redfishobject import RedfishObject
from redfish.rest.v1 import ServerDownOrUnreachableError

def redfish_mount_virtual_media_iso(redfishobj, iso_url, boot_on_next_server_reset):
    sys.stdout.write("\nAdding .iso to boot order ...\n")
    instances = redfishobj.search_for_type("Manager.")

    for instance in instances:
        rsp = redfishobj.redfish_get(instance["@odata.id"])
        rsp = redfishobj.redfish_get(rsp.dict["VirtualMedia"]["@odata.id"])

        for vmlink in rsp.dict["Members"]:
            response = redfishobj.redfish_get(vmlink["@odata.id"])

            if response.status == 200 and "DVD" in response.dict["MediaTypes"]:
                body = {"Image": iso_url}
                
                if (iso_url is not None and \
                                        boot_on_next_server_reset is not None):
                    if redfishobj.typepath.defs.isgen9:
                        body["Oem"] = {"Hp": {"BootOnNextServerReset": \
                                                    boot_on_next_server_reset}}
                    else:
                        body["Oem"] = {"Hpe": {"BootOnNextServerReset": \
                                                    boot_on_next_server_reset}}

                    response = redfishobj.redfish_patch(vmlink["@odata.id"], body)
                    redfishobj.error_handler(response)
            elif response.status != 200:
                redfishobj.error_handler(response)


def redfish_reset_server(redfishobj, bios_password=None):
    sys.stdout.write("\nResetting the server ...\n")
    instances = redfishobj.search_for_type("ComputerSystem.")

    if redfishobj.typepath.defs.isgen9:
        for instance in instances:
            body = dict()
            body["Action"] = "Reset"
            body["ResetType"] = "ForceRestart"

            response = redfishobj.redfish_post(instance["@odata.id"], body)
            redfishobj.error_handler(response)
    else:
        for instance in instances:
            resp = redfishobj.redfish_get(instance['@odata.id'])
            if resp.status==200:
                body = dict()
                body["Action"] = "ComputerSystem.Reset"
                body["ResetType"] = "ForceRestart"
                path = resp.dict["Actions"]["#ComputerSystem.Reset"]["target"]
            else:
                sys.stderr.write("ERROR: Unable to find the path for reboot.")
                raise

            response = redfishobj.redfish_post(path, body)
            redfishobj.error_handler(response)


if __name__ == "__main__":
    iLO_https_url = "https://serverName.oob.hydra.lab"
    iLO_account = "Administrator"
    iLO_password = "password"


    try:
        REDFISH_OBJ = RedfishObject(iLO_https_url, iLO_account, iLO_password)
    except ServerDownOrUnreachableError as excp:
        sys.stderr.write("ERROR: server not reachable or doesn't support " \
                                                                "RedFish.\n")
        sys.exit()
    except Exception as excp:
        raise excp

    redfish_mount_virtual_media_iso(REDFISH_OBJ, "http://cluster.hydra.lab/pxe/images/ubuntu16-preseed.iso", True)
    REDFISH_OBJ.redfish_client.logout()


    try:
        REDFISH_OBJ = RedfishObject(iLO_https_url, iLO_account, iLO_password)
    except ServerDownOrUnreachableError as excp:
        sys.stderr.write("ERROR: server not reachable or doesn't support " \
                                                                "RedFish.\n")
        sys.exit()
    except Exception as excp:
        raise excp

    redfish_reset_server(REDFISH_OBJ)
    REDFISH_OBJ.redfish_client.logout()
  
