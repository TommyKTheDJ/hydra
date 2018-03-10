import pandas as pd
import sys
from boltons.iterutils import remap

def xls_to_dict(inventory_filename=None,sheet_name=None):
    df = pd.read_excel(inventory_filename,sheet_name=sheet_name,index_col=0,encoding=sys.getfilesystemencoding())
    df = df.replace(['missing','Missing','MISSING'],'-')
    df = df.fillna('-')
    return df.to_dict(orient='index')

def clean_dict(d):
    drop_none_or_hyphen = lambda path, key, value: key is not None and value is not None and not value == u'-' and not value == '-'
    return remap(d, visit=drop_none_or_hyphen)
