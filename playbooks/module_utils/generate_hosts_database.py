import netaddr
from ansible.module_utils.common_functions import *

def generate_hosts_database(inventory_filename = None):
    master = xls_to_dict(inventory_filename=inventory_filename, sheet_name="master")
    console =  xls_to_dict(inventory_filename=inventory_filename, sheet_name="console")
    management =  xls_to_dict(inventory_filename=inventory_filename, sheet_name="management")
    subnets =  xls_to_dict(inventory_filename=inventory_filename, sheet_name="subnets")
    interfaces =  xls_to_dict(inventory_filename=inventory_filename, sheet_name="interfaces")
    power =  xls_to_dict(inventory_filename=inventory_filename, sheet_name="power")

    database = {}
    database ['hosts'] = {}
    for hostname, data in master.iteritems():
      record = {}
      record['manufacturer'] = data['manufacturer']
      record['rack'] = data['rack']
      record['model'] = data['model']
      record['type'] = data['type']
      record['os'] = data['os']
      record['ilo_default_pwd'] = data['ilo_default_pwd']
      record['resources'] = {}
      record['resources']['cpu'] = data['cpu']
      record['resources']['ram'] = data['ram']
      record['resources']['disk'] = data['disk']


      record['interfaces'] = {}
      # MANAGEMENT INTERFACE DATA
      record['interfaces']['management'] = {}
      record['interfaces']['management']['vlan_id'] = subnets[management[hostname]['subnet_name']]['vlan_id']
      record['interfaces']['management']['cable_id'] = management[hostname]['cable_id']
      record['interfaces']['management']['user'] = management[hostname]['user']

      try:
          mac_address = netaddr.EUI(management[hostname]['mac_address'])
          mac_address.dialect = netaddr.mac_unix
      except:
          record['interfaces']['management']['mac_address'] = u'-'
      else:
          record['interfaces']['management']['mac_address'] = unicode(mac_address)

      if record['type'] == 'fabric':
          record['onie_url'] = data['onie_url']
          record['interfaces']['management']['ip'] = interfaces[hostname]['fabric_management']
          record['interfaces']['management']['prefix_length'] = subnets['fabric_management']['prefix_length']

      elif record['type'] == 'host':
          record['interfaces']['management']['ip'] = interfaces[hostname]['ipxe']
          record['interfaces']['management']['prefix_length'] = subnets['ipxe']['prefix_length']
      else:
          record['interfaces']['management']['ip'] = interfaces[hostname]['management']
          record['interfaces']['management']['prefix_length'] = subnets['management']['prefix_length']

      if not record['type'] == 'vm':
          record['interfaces']['management']['neighbor'] = {}
          record['interfaces']['management']['neighbor']['hostname'] = management[hostname]['switch']
          record['interfaces']['management']['neighbor']['port'] = management[hostname]['port']

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
