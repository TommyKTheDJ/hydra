from ansible.module_utils.common_functions import *

def generate_dns_services_entries(inventory_filename = None):
    entries = xls_to_dict(inventory_filename=inventory_filename, sheet_name="dns_entries_services",index_col=[0,1,2,3])
    data = []
    for (host,domain,etype,value) in entries.iterkeys():
        data.append({'host':host,'domain':domain,'type':etype,'value':value})
    return {'dns_service_entries':data}
