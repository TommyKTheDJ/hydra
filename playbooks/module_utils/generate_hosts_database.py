# from ansible.module_utils.common_functions import *
from common_functions import *

global subnets
global interfaces

def generate_hosts_database(inventory_filename = None):
    global subnets
    global interfaces

    master = xls_to_dict(inventory_filename=inventory_filename, sheet_name="master")
    console =  xls_to_dict(inventory_filename=inventory_filename, sheet_name="console")
    subnets =  xls_to_dict(inventory_filename=inventory_filename, sheet_name="subnets")
    interfaces =  xls_to_dict(inventory_filename=inventory_filename, sheet_name="interfaces",index_col=[0,1])
    power =  xls_to_dict(inventory_filename=inventory_filename, sheet_name="power")
    ilo =  xls_to_dict(inventory_filename=inventory_filename, sheet_name="ilo")

    database = {}
    database ['hosts'] = {}
    for hostname, data in master.iteritems():
        record = {}

        record['manufacturer'] = data['manufacturer']
        record['rack'] = data['rack']
        record['model'] = data['model']
        record['type'] = data['type']
        record['os'] = data['os']
        if hostname in ilo.keys(): record['ilo_password'] = ilo[hostname]['password']
        record['resources'] = {}
        record['resources']['cpu'] = data['cpu']
        record['resources']['ram'] = data['ram']
        record['resources']['disk'] = data['disk']
        record['user'] = data['user']
        if not is_empty_datum(data['onie_image']): record['onie_image'] = data['onie_image']
        if hostname in ilo.keys(): record['ilo_password'] = ilo[hostname]['password']
        record['interfaces'] = {}
        record['interfaces'].update(add_host_interfaces(hostname))

        # CONSOLE INTERFACE DATA
        if not record['type'] in [ 'vm', 'console','host']:
            record['interfaces']['console'] = {}
            record['interfaces']['console']['neighbor'] = {}
            record['interfaces']['console']['neighbor']['hostname'] = console[hostname]['console_server']
            record['interfaces']['console']['neighbor']['port'] = console[hostname]['port']
            record['interfaces']['console']['cable_id'] = console[hostname]['cable_id']
            record['interfaces']['console']['baud'] = console[hostname]['baud']

        # POWER SUPPLY DATA
        if not record['type'] in ['vm','pdu']:
            record['psus'] = []
            if not power[hostname]['pdu_1'] == u'-':
                psu = {}
                psu['pdu'] = {}
                psu['pdu']['hostname'] = power[hostname]['pdu_1']
                psu['pdu']['port'] = power[hostname]['pdu_port_1']
                record['psus'].append(psu)

            if not power[hostname]['pdu_2'] == u'-':
                psu = {}
                psu['pdu'] = {}
                psu['pdu']['hostname'] = power[hostname]['pdu_2']
                psu['pdu']['port'] = power[hostname]['pdu_port_2']
                record['psus'].append(psu)

        database ['hosts'][hostname] = record
    return clean_dict(database)

def add_host_interfaces(host):
    # Add interfaces
    host_interfaces = {}

    for (hostname, subnet_name), data in interfaces.items():
        if hostname == host:
            interface = {}
            if 'vlan_id' in subnets[subnet_name].keys(): interface['vlan_id'] = subnets[subnet_name]['vlan_id']
            if not is_empty_datum(data['cable_id']): interface['cable_id'] = data['cable_id']
            if not is_empty_datum(data['mac_address']): interface['mac_address'] = format_mac_address(data['mac_address'])
            if not is_empty_datum(data['ip']): interface['ip'] = "/".join(map(str,[data['ip'],subnets[subnet_name]['prefix_length']]))
            if not is_empty_datum(data['neighbor']):
                interface['neighbor'] = {}
                interface['neighbor']['hostname'] = data['neighbor']
                if not is_empty_datum(data['port']): interface['neighbor']['port'] = data['port']

            host_interfaces[subnet_name] = interface

    return host_interfaces




if __name__ == "__main__":
    import sys
    import yaml
    if len(sys.argv)>=2 and sys.argv[1]:  # Example usage.
        hosts_database_data = generate_hosts_database(sys.argv[1])
        print yaml.safe_dump(hosts_database_data,allow_unicode = True,indent = 4,default_flow_style = False,encoding = 'utf-8')
        # print hosts_database_data
    else:
        print ('No arguments passed')
        sys.exit(1)
