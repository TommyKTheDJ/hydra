import pandas as pd
import sys

def xls_to_dict(inventory_filename=None,sheet_name=None):
  df = pd.read_excel(inventory_filename,sheet_name=sheet_name,index_col=0,encoding=sys.getfilesystemencoding())
  df = df.replace(['missing','Missing','MISSING'],'-')
  df = df.fillna('-')
  return df.to_dict(orient='index')

# def is_empty(cell):
#     return not cell or unicode(cell) in []

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
        vlan['netmask'] = values['netmask']
        vlan['hosts'] = [x for x,host_data in management.iteritems() if host_data['subnet_name'] == name ]
        data ['vlans'].append(vlan)

    return data
