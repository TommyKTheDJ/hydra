#! /usr/bin/python2.7
# coding: utf-8

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: hydra_database

short_description: This is my sample module

version_added: "2.4"

description:
    - "This module generates the yml version of the database"

options:
    name:
        description:
            - This is the message to send to the sample module
        required: true
    new:
        description:
            - Control to demo if the result of this module is changed or not
        required: false

'''

EXAMPLES = '''
# Pass in a message
- name: Test with a message
  hydra_database:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  hydra_database:
    src: hello world
    dest: true

# fail the module
- name: Test failure of the module
  hydra_database:
    name: fail me
'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
message:
    description: The output message that the sample module generates
'''
import hashlib
import os
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.generate_hosts_database import *
from ansible.module_utils.generate_subnet_database import *
import sys
import yaml

def run_module():
    # define the available arguments/parameters that a user can pass to
    # the module
    module_args = dict(
        src=dict(type='str', required=True),
        hosts_database_dest=dict(type='str', required=False, default=None),
        subnets_database_dest=dict(type='str', required=False, default=None),
        force=dict(type='bool', required=False, default=False),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        error = '',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    hosts_database_filename = module.params['hosts_database_dest'] or "/tmp/database.yml"
    subnets_database_filename = module.params['subnets_database_dest'] or "/tmp/subnets.yml"

    # CHECK IF DATABASE DATA CHANGED
    try:
        with open(hosts_database_filename,'r') as destination_file:
            old_hosts_data = yaml.safe_load(destination_file)
    except:
        old_hosts_data = None

    try:
        hosts_database_data = generate_hosts_database(inventory_filename = module.params['src'])
    except Exception as e:
        result['error'] = e
        module.fail_json(msg='Database data generation failed', **result)

    try:
        subnets_database_data = generate_subnet_database(inventory_filename = module.params['src'])
    except Exception as e:
        result['error'] = e
        module.fail_json(msg='subnet database generation failed', **result)

    # new_file_hash = hashlib.md5().update(database_data)
    # yaml.safe_dump(database,allow_unicode = True,indent = 4,default_flow_style = False,encoding = 'utf-8')

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    # sys.stderr.write(str(old_file_content))
    # sys.stderr.write(str(database_data))

    if not old_hosts_data == hosts_database_data or not os.path.isfile(hosts_database_filename) \
    or not os.path.isfile(subnets_database_filename) or module.params['force']:
        result['changed'] = True
    else:
        result['changed'] = False


    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        return result

    if result['changed'] and not module.check_mode:
        # sys.stderr.write(str(type(database_data)))
        with open(hosts_database_filename, 'w') as hosts_database_file:
            try:
                yaml.safe_dump(hosts_database_data,hosts_database_file,allow_unicode = True,indent = 4,default_flow_style = False,encoding = 'utf-8')
                result['message'] = 'Database file correctly generated'
            except:
                module.fail_json(msg='Writing database data file failed', **result)
        with open(subnets_database_filename,'w') as subnets_database_file:
            try:
                yaml.safe_dump(subnets_database_data,subnets_database_file,allow_unicode = True,indent = 4,default_flow_style = False,encoding = 'utf-8')
                result['message'] = 'Subnet database file correctly generated'
            except:
                module.fail_json(msg='Writing subnet data file failed', **result)
    else:
            result['message'] = 'No changes required'

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    # if module.params['name'] == 'fail me':
    #     module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():

    run_module()

if __name__ == '__main__':
    main()
