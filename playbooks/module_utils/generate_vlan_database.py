from ansible.module_utils.common_functions import *

def generate_vlan_database(inventory_filename = None):
    management =  xls_to_dict(inventory_filename=inventory_filename, sheet_name="management")
    subnets =  xls_to_dict(inventory_filename=inventory_filename, sheet_name="subnets")


    data = {}
    data ['vlans'] = []
    for name, values in subnets.iteritems():
        vlan = {}
        vlan['id'] = values['vlan_id']
        vlan['name'] = name
        vlan['notes'] = values['notes']
        vlan['network'] = values['network']
        vlan['prefix_length'] = values['prefix_length']
        vlan['dhcp'] = bool(values['requires_dhcp'])
        vlan['hosts'] = [x for x,host_data in management.iteritems() if host_data['subnet_name'] == name ]
        data ['vlans'].append(vlan)

    return data
