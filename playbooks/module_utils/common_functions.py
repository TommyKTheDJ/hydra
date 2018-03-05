import pandas as pd
import sys

def xls_to_dict(inventory_filename=None,sheet_name=None):
  df = pd.read_excel(inventory_filename,sheet_name=sheet_name,index_col=0,encoding=sys.getfilesystemencoding())
  df = df.replace(['missing','Missing','MISSING'],'-')
  df = df.fillna('-')
  return df.to_dict(orient='index')

# def is_empty(cell):
#     return not cell or unicode(cell) in []

def clean_list (record):
  cleaned_list = [ x for x in record if not x == u'-' ]
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
      if data[key] == u'-':
          data[key] = None
  return data
