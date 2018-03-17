from ansible.module_utils.common_functions import *

def generate_vlan_database(inventory_filename = None):
    interfaces =  xls_to_dict(inventory_filename=inventory_filename, sheet_name="interfaces")
    subnets =  xls_to_dict(inventory_filename=inventory_filename, sheet_name="subnets")


    data = {}
    data['vlans'] = {}
    for name, values in subnets.iteritems():

        vlan = {}
        vlan['id'] = values['vlan_id']
        vlan['name'] = name
        vlan['notes'] = values['notes']
        vlan['network'] = values['network']
        vlan['prefix_length'] = values['prefix_length']
        vlan['dhcp'] = False
        if not is_empty_datum(values['nic']):
            vlan['nic'] = values['nic']
            vlan['dhcp'] = True
        if not is_empty_datum(values['domain']):
            vlan['domain'] = values['domain']
            if not is_empty_datum(values['zone'])  :
                vlan['domain'] = ".".join([values['zone'],values['domain']])
        vlan['hosts'] = []
        for hostname,interface_data in interfaces.iteritems():
            if interface_data['subnet'] == name:
                host = {}
                host['hostname'] = hostname
                if not is_empty_datum(interface_data['mac_address']): host['mac_address'] = format_mac_address(interface_data['mac_address'])
                vlan['hosts'].append(host)

        data['vlans'][name] = vlan
    return data
