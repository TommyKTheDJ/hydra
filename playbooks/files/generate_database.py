#! /usr/bin/python2.7
# coding: utf-8
import pandas as pd
import yaml
import sys
import collections

INVENTORY = sys.argv[1]
OUTFILE = sys.argv[2]

def xls_to_dict(inventory_file=None,sheet_name=None):
    return pd.read_excel(inventory_file,sheet_name=sheet_name,index_col=0,encoding=sys.getfilesystemencoding()).to_dict(orient='index')

def is_empty(cell):
    return not cell or unicode(cell) in [u'missing', u'-', u'.nan',u'-\xa0', '-', u'nan', '.nan']

def clean_list (record):
    cleaned_list = [ x for x in record if x and not is_empty(x)]
    if len(cleaned_list)>0:
        return cleaned_list
    else:
        return None

def clean_dict (data):
    for key,record in data.items():
        if type(record) is dict:
            data[key] = clean_dict(record)
        elif type(record) is list:
            data[key] = clean_list(record)
        if is_empty(data[key]):
            del data[key]
    return data

master = xls_to_dict(inventory_file=INVENTORY, sheet_name="master")
console =  xls_to_dict(inventory_file=INVENTORY, sheet_name="console")
management =  xls_to_dict(inventory_file=INVENTORY, sheet_name="management")
subnets =  xls_to_dict(inventory_file=INVENTORY, sheet_name="subnets")
interfaces =  xls_to_dict(inventory_file=INVENTORY, sheet_name="interfaces")
power =  xls_to_dict(inventory_file=INVENTORY, sheet_name="power")

database = {}
database ['hosts'] = []
for hostname, data in master.iteritems():
    record = {}
    record['hostname'] = hostname
    record['manufacturer'] = data['manufacturer']
    record['rack'] = data['rack']
    record['model'] = data['model']
    record['type'] = data['type']
    record['os'] = data['os']
    record['resources'] = {}
    record['resources']['cpu'] = data['cpu']
    record['resources']['ram'] = data['ram']
    record['resources']['disk'] = data['disk']


    record['interfaces'] = {}
    # MANAGEMENT INTERFACE DATA
    record['interfaces']['management'] = {}
    record['interfaces']['management']['vlan_id'] = subnets['management']['vlan_id']
    record['interfaces']['management']['cable_id'] = management[hostname]['cable_id']
    record['interfaces']['management']['mac_address'] = management[hostname]['mac_address']
    record['interfaces']['management']['user'] = management[hostname]['user']


    if record['type'] == 'switch':
        record['interfaces']['management']['ip'] = interfaces[hostname]['switch_management']
        record['interfaces']['management']['netmask'] = subnets['switch_management']['netmask']
    elif record['type'] == 'host':
        record['interfaces']['management']['ip'] = interfaces[hostname]['ipxe']
        record['interfaces']['management']['netmask'] = subnets['ipxe']['netmask']
    else:
        record['interfaces']['management']['ip'] = interfaces[hostname]['management']
        record['interfaces']['management']['netmask'] = subnets['management']['netmask']

    if not record['type'] == 'vm':
        record['interfaces']['management']['neighbor'] = {}
        record['interfaces']['management']['neighbor']['hostname'] = management[hostname]['switch']
        record['interfaces']['management']['neighbor']['port'] = management[hostname]['port']

    # CONSOLE INTERFACE DATA
    if not record['type'] in [ 'vm', 'console']:
        record['interfaces']['console'] = {}
        record['interfaces']['console']['neighbor'] = {}
        record['interfaces']['console']['neighbor']['hostname'] = console[hostname]['console_server']
        record['interfaces']['console']['neighbor']['port'] = console[hostname]['port']
        record['interfaces']['console']['cable_id'] = console[hostname]['cable_id']
        record['interfaces']['console']['baud'] = console[hostname]['baud']

    # POWER SUPPLY DATA
    if not record['type'] == 'vm':
        record['psus'] = [None,None]
        if not is_empty(power[hostname]['pdu_1']):
            record['psus'][0] = {}
            record['psus'][0]['pdu_hostname'] = power[hostname]['pdu_1']
            record['psus'][0]['pdu_port'] = power[hostname]['pdu_port_1']

        if not is_empty(power[hostname]['pdu_2']):
            record['psus'][1] = {}
            record['psus'][1]['pdu_hostname'] = power[hostname]['pdu_2']
            record['psus'][1]['pdu_port'] = power[hostname]['pdu_port_2']

    database ['hosts'].append(clean_dict(record))


with open(OUTFILE, 'w') as outfile:
    yaml.safe_dump(database,outfile,allow_unicode = True,indent = 4,default_flow_style = False,encoding = 'utf-8')
