stackhpc.firewallgen
=========================

Generates an iptables firewall by inspecting the target host for any open sockets

Requirements
------------

- `kayobe` is required for it's filters and variables
- `jq` is required for firewall rule rewriting
 
Role Variables
--------------

    # list of rules to accept in the filter chain
    firewallgen_ipv4_input_allow_rules: []
    
    # where to output the generated firewall rules
    firewallgen_output_path: "{{ kayobe_config_path | dirname ~ '/firewallgen' }}" 
    
    # location where the iptables-restore file is outputed prior to being loaded
    firewallgen_rules_path: /tmp/firewallgen-iptables.rules
    
    # where, on the target host, to output a backup of the iptables rules
    firewallgen_backup_path: /tmp/firewallgen-iptables.save
    
    # firewall must be explicitly enabled to be applied
    firewallgen_enable_firewall: False
    
    # modify the generated rules with `jq` expressions:
    # e.g to remove the rule generated for the process, `rpcbind`, you 
    # could use: '. | map(select(.processes[].name != "rpcbind"))'
    firewallgen_ipv4_input_allow_rewrite_rules: []


Dependencies
------------

No current dependencies.

Example Playbook
----------------

To generate a firewall:

    - name: gather firewall rules
      hosts: all
      roles:
        - name: stackhpc.firewallgen
      vars:
        firewall_action: "generate"

License
-------

GPLv3

Author Information
------------------

- Will Szumski (<will@stackhpc.com>)
