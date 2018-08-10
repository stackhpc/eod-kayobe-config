from ansible.module_utils.basic import AnsibleModule
from firewallgen import ssutils
from firewallgen import iputils
from firewallgen import dockerutils
from firewallgen import utils
from firewallgen import firewallgen
from firewallgen.firewallgen import (UDPDataCollector, TCPDataCollector, collect_open_sockets)
from jinja2 import Template

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}


class AnsibleVersionMixin:
    def get_version_flag(self):
        return ssutils.get_version_flag(self.module.params['ip_version'])


class AnsibleUDPCollector(UDPDataCollector, AnsibleVersionMixin):
    def __init__(self, module):
        super(AnsibleUDPCollector, self).__init__()
        self.module = module

    def get_ss_output(self):
        _, out, _ = self.module.run_command(["ss", "-nlpu", self.get_version_flag()])
        return out

class AnsibleTCPCollector(TCPDataCollector, AnsibleVersionMixin):
    def __init__(self, module):
        super(AnsibleTCPCollector, self).__init__()
        self.module = module

    def get_ss_output(self):
        _, out, _ = self.module.run_command(["ss", "-nlpt", self.get_version_flag()])
        return out

def transform_network_allocation(allocation):
    map = {}
    for label, host_to_ips in allocation.items():
        # strip off _ips suffix
        interface = "{}_interface".format(label[0:-4])
        for host, ip in host_to_ips.items():
            map[ip] = interface

    map['127.0.0.1'] = 'lo'
    return map

def process_to_dict(process):
    return vars(process)

def opensocket_to_dict(opensocket):
    result = vars(opensocket)
    result['processes'] = map(process_to_dict, result['processes'])
    return result

class AnsibleCmdRunner(utils.CmdRunner):
    def __init__(self, module):
        self.module = module

    def check_output(self, *args, **kwargs):
        return self.module.run_command(*args, **kwargs)[1]

def run_module():
    module_args = dict(
        ip_to_interface_map=dict(type='dict', required=True),
        # dest=dict(type='str', required=True)
        ip_version=dict(type='int', required=False, default=4)
    )

    result = dict(
        changed=False
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    tcp = collect_open_sockets(AnsibleTCPCollector(module),
                               module.params['ip_to_interface_map'])

    udp = collect_open_sockets(AnsibleUDPCollector(module),
                               module.params['ip_to_interface_map'])

    result['sockets'] = map(opensocket_to_dict, (tcp + udp))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()