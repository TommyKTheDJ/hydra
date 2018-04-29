from ansible.module_utils.common_functions import *

def generate_subnet_database(inventory_filename = None):
    interfaces =  xls_to_dict(inventory_filename=inventory_filename, sheet_name="interfaces",index_col=[0,1])
    subnets =  xls_to_dict(inventory_filename=inventory_filename, sheet_name="subnets")
    data = {}
    data['subnets'] = {}
    for subnet_name, values in subnets.iteritems():
        subnet = {}
        if not is_empty_datum(values['vlan_id']): subnet['vlan_id'] = values['vlan_id']
        subnet['name'] = subnet_name
        subnet['notes'] = values['notes']
        subnet['network'] = values['network']
        subnet['prefix_length'] = values['prefix_length']
        subnet['dhcp'] = False
        if not is_empty_datum(values['nic']): subnet['nic'] = values['nic']
        if not is_empty_datum(values['dhcp']):
            subnet['dhcp'] = True if values['dhcp'] == u'x' else False
        if not is_empty_datum(values['domain']):
            subnet['domain'] = values['domain']
            if not is_empty_datum(values['zone'])  :
                subnet['domain'] = ".".join([values['zone'],values['domain']])
        subnet['hosts'] = []


        for (hostname,interface_subnet_name),interface_data in interfaces.iteritems():
            if interface_subnet_name == subnet_name:
                host = {}
                host['hostname'] = hostname
                if not is_empty_datum(interface_data['mac_address']): host['mac_address'] = format_mac_address(interface_data['mac_address'])
                subnet['hosts'].append(host)

        data['subnets'][subnet_name] = subnet
    return data
