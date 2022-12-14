#!/usr/bin/env python3
from __future__ import absolute_import, division, print_function
__metaclass__ = type
from orionsdk import SwisClient
from ansible.module_utils.basic import AnsibleModule
import requests
import urllib3


DOCUMENTATION = '''
---
module: sw_manage
short_description: Adds support for automatically updating Solarwinds custom properties
'''
EXAMPLES = '''
- name: add custom properties to solarwinds node
  sw_manage:
    hostname: "SWHOSTNAME"
    username: "SWUSERNAME"
    password: "SWPASSWORD"
    state: "update"
    caption: "node_hostname"
'''

__SWIS__ = None
urllib3.disable_warnings()

def main():
    global __SWIS__
    module = AnsibleModule(
        argument_spec=dict(
            hostname=dict(required=True),
            username=dict(required=True, no_log=True),
            password=dict(required=True, no_log=True),
            state=dict(required=True, choices=['update']),
            node_id=dict(required=False),
            caption=dict(required=False),
            env=dict(required=False),
            fisma=dict(required=False),
            project_lead=dict(required=False),
            sme=dict(required=False)
        )
    )

    options = {
        'hostname': module.params['hostname'],
        'username': module.params['username'],
        'password': module.params['password']
    }

    __SWIS__ = SwisClient(**options)

    try:
        __SWIS__.query('SELECT Uri FROM Orion.Environment')
    except Exception as e:
        module.fail_json(msg="Failed to query Orion. Check Hostname, Username, and Password : {0}".format(str(e)))

    if module.params['state'] == 'update':
        _custom_props(module)

def _find_node(module):
    node = {}
    if module.params['node_id'] is not None:
        results = __SWIS__.query(
            'SELECT NodeID, Caption, Unmanaged, UnManageFrom, UnManageUntil FROM Orion.Nodes WHERE NodeID = '
            '@node_id',
            node_id = module.params['node_id'])

    elif module.params['caption'] is not None:
        results = __SWIS__.query(
            'SELECT NodeID, Caption, Unmanaged, UnManageFrom, UnManageUntil FROM Orion.Nodes WHERE Caption = '
            '@host_caption',
            host_caption = module.params['caption'])

    else:
        module.fail_json(msg="Invalid node_id or hostname provided (FAILED)")

    if results['results']:
        node['nodeId'] = results['results'][0]['NodeID']
        node['caption'] = results['results'][0]['Caption']
        node['netObjectId'] = 'N:{}'.format(node['nodeId'])
    return node

def _custom_props(module):
    options = {
        'hostname': module.params['hostname'],
        'username': module.params['username'],
        'password': module.params['password']
    }

    swis = SwisClient(**options)
    node = _find_node(module)
    nodeid = "{0}".format(node['nodeId'])

    swis.update('swis://orion/Orion/Orion.Nodes/' + 'NodeID=' + nodeid + '/CustomProperties', Environment=module.params['env'])
    swis.update('swis://orion/Orion/Orion.Nodes/' + 'NodeID=' + nodeid + '/CustomProperties', FISSMA_System=module.params['fisma'])
    swis.update('swis://orion/Orion/Orion.Nodes/' + 'NodeID=' + nodeid + '/CustomProperties', Government_Contact_Information=module.params['project_lead'])
    swis.update('swis://orion/Orion/Orion.Nodes/' + 'NodeID=' + nodeid + '/CustomProperties', GSA_FISMA_System='GRACE')
    swis.update('swis://orion/Orion/Orion.Nodes/' + 'NodeID=' + nodeid + '/CustomProperties', Region='AWS - EAST')
    swis.update('swis://orion/Orion/Orion.Nodes/' + 'NodeID=' + nodeid + '/CustomProperties', Service_Group='GRACE')
    swis.update('swis://orion/Orion/Orion.Nodes/' + 'NodeID=' + nodeid + '/CustomProperties', SITE_ID='CAM - Amazon - Cloud Service Provider')
    swis.update('swis://orion/Orion/Orion.Nodes/' + 'NodeID=' + nodeid + '/CustomProperties', SME_Contact_Information=module.params['sme'])

    module.exit_json(changed=True)

if __name__ == '__main__':
    main()
