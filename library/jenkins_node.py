#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: jenkins_node_module

short_description: Manage jenkins node

version_added: "0.1"

description:
    - "This module to create, delete, enable, disable nodes in jenkins"
    - "Draft version"

requirements: python-jenkins

options:
    name:
        description:
            - Node name
        required: true
    url:
        description:
            - url address of the jenkins server, 
        default:
            - http://localhost:8080
        required: false
    url_password:
        description:
            - The password for use in HTTP basic authentication.
    url_username:
        description:
            - The username for use in HTTP basic authentication.
    state:
        description:
            - Desired node state.
            - Can be: present, absent
        default:
            - present
    enabled:
        description:
            - Online or offline node state.
        default:
            - yes
    remoteFS:
        description:
            - Remote root directory
    params:
        description:
            - Additional parameters for the launcher, dict
            - Can be: port, host, username, credentialsId, etc...

author:
    - Alexey Demidov (@ademidov)
'''

EXAMPLES = '''

# Add new node:
        name: new_node1
        state: present
        enabled: yes
        url_username: admin
        url_password: password123
        remoteFS: /data
        params:
                port: 22
                host: 192.168.0.1
                username: jenkins
                credentialsId: fa9efd77-94d5-4d01-9052-24c179e86e8d
                sshHostKeyVerificationStrategy: {"stapler-class": "hudson.plugins.sshslaves.verifiers.NonVerifyingKeyVerificationStrategy"}

'''
RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
message:
    description: The output message that the sample module generates
'''

from ansible.module_utils.basic import AnsibleModule
from time import sleep
import jenkins

def run_module():
        module_args = dict(
                name=dict(type='str', required=True),
                url=dict(type='str', required=False, default='http://localhost:8080'),
                url_password=dict(type='str', required=True, no_log=True),
                url_username=dict(type='str', required=True),
                state=dict(type='str', required=False, default='present'),
                enabled=dict(type='bool', required=False, default='yes'),
                remoteFS=dict(type='str', required=False, default='/opt'),
                params=dict(type='dict', required=False, default={})
        )     

        result = dict(changed=False, message='')

        module = AnsibleModule(
                argument_spec=module_args,
                supports_check_mode=True
        )

        server = jenkins.Jenkins(module.params['url'], username=module.params['url_username'], password=module.params['url_password'])
        if module.check_mode:
                return result

        if module.params['state'] == 'present'.lower():
                if server.node_exists(module.params['name']): 
                        result['changed'] = False
                        result['message'] += "Node already exists |"
                else:
                        server.create_node(
                                module.params['name'],
                                nodeDescription=module.params['name'],
                                remoteFS=module.params['remoteFS'],
                                labels=module.params['name'],
                                exclusive=False,
                                launcher=jenkins.LAUNCHER_SSH,
                                launcher_params=module.params['params'])
			result['message'] += "Node has been created |"
                        result['changed'] = True

                status=(False if server.get_node_info(module.params['name'], depth=0)['offline'] else True)
		sleep (10) # Delay to starting node
                if module.params['enabled'] > status:
			result['message'] +=" Node has been enabled |"
                        server.enable_node(module.params['name'])
                        result['changed'] = True
                elif module.params['enabled'] < status:
			result['message'] += " Node has been disabled |"
                        server.disable_node(module.params['name'])
                        result['changed'] = True
                else:
			result['changed'] = False

        if module.params['state'] == 'absent'.lower():
                if not server.node_exists(module.params['name']):
                        result['changed'] = False
                        result['message'] = "Node does not exists"
                else:
                        server.delete_node(module.params['name'])
			result['message'] = "Node has been removed"
                        result['changed'] = True

        module.exit_json(**result)

def main():
        run_module()

if __name__ == '__main__':
        main()
