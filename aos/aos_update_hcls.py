import requests
import json
import sys
import os
import getpass
requests.packages.urllib3.disable_warnings()

DEBUG = True
AOS_HOST = 'aos.hydra.lab'
HCL_ENTRIES_FOLDER = 'hcl/'

API_AUTH_ENDPOINT = '/api/aaa/login'
API_HCL_ENDPOINT = '/api/hcl'

try:
    TOKEN = os.environ.get('AOS_TOKEN')
except:
    print ('AOS_TOKEN environment variable not found')

try:
    TOKEN_ID = os.environ.get('AOS_TOKEN_ID')
except:
    print ('AOS_TOKEN_ID environment variable not found')

def add_hcl_aos(u_token,u_id,hcl):
    url = 'https://{0}{1}'.format(AOS_HOST,API_HCL_ENDPOINT)
    headers = {'AUTHTOKEN': u_token, 'id': u_id, 'Content-type': 'application/json', 'Accept': 'application/json'}
    r = requests.post(url, headers=headers, json=hcl, verify=False)
    return r

def update_hcl_aos(u_token,u_id,hcl):
    url = 'https://{0}{1}/{2}'.format(AOS_HOST,API_HCL_ENDPOINT,hcl[u'id'])
    headers = {'AUTHTOKEN': u_token, 'id': u_id, 'Content-type': 'application/json', 'Accept': 'application/json'}
    r = requests.put(url, headers=headers, json=hcl, verify=False)
    return r

headers = {'AUTHTOKEN': TOKEN, 'id': TOKEN_ID}
url = 'https://{0}{1}'.format(AOS_HOST,API_HCL_ENDPOINT)
r = requests.get(url, headers=headers, verify=False)
json_data = json.loads(r.text)
aos_hcls_dict = {}
for item in json_data['items']:
    item.pop(u'last_modified_at')
    item.pop(u'created_at')
    aos_hcls_dict[item[u'id']] = item



local_hcl_json_data = []
added_counter = 0
updated_counter = 0
for fn in os.listdir(HCL_ENTRIES_FOLDER):
    filename = os.path.join(HCL_ENTRIES_FOLDER,fn)
    print "Reading file: {}".format(filename)
    f=open(filename,'r')
    json_data=f.read()
    hcl = json.loads(json_data)
    local_hcl_json_data.append(hcl)
    if hcl['id'] not in aos_hcls_dict.keys():
        print 'HCL {} needs to be added'.format(hcl['id'])
        r = add_hcl_aos(TOKEN,TOKEN_ID,hcl)
        if not r.status_code == requests.codes.ok:
            with open('body_{}.json'.format(hcl['id']), 'w') as dumpfile:
                json.dump(hcl, dumpfile, indent = 4, encoding = 'utf-8')
            raise Exception('HCL {} could not be added: response code = {}'.format(hcl['id'],r.status_code))
        else:
            added_counter +=1
    elif not hcl == aos_hcls_dict[hcl['id']]:
        print 'HCL {} needs to be updated'.format(hcl['id'])
        r = update_hcl_aos(TOKEN,TOKEN_ID,hcl)
        if not r.status_code == requests.codes.ok:
            with open('body_{}.json'.format(hcl['id']), 'w') as dumpfile:
                json.dump(hcl, dumpfile, indent = 4, encoding = 'utf-8')
            raise Exception('HCL {} could not be updated: response code = {}'.format(hcl['id'],r.status_code))
        else:
            updated_counter +=1

print "A Total of {} HCLs were added".format(added_counter)
print "A Total of {} HCLs were updated".format(updated_counter)
