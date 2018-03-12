import pandas as pd
import sys
import netaddr
from boltons.iterutils import remap

def xls_to_dict(inventory_filename=None,sheet_name=None,index_col=0):
    df = pd.read_excel(inventory_filename,sheet_name=sheet_name,index_col=index_col,encoding=sys.getfilesystemencoding())
    df = df.replace(['missing','Missing','MISSING'],'-')
    df = df.fillna('-')
    return df.to_dict(orient='index')

def clean_dict(d):
    drop_none_or_hyphen = lambda path, key, value: key is not None and not is_empty_datum(value)
    return remap(d, visit=drop_none_or_hyphen)

def is_empty_datum(value):
    return value is None or value == u'-' or value == '-'

def format_mac_address(blob):
    mac_address = netaddr.EUI(blob)
    mac_address.dialect = netaddr.mac_unix
    return unicode(mac_address)
