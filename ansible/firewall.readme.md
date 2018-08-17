# Basic workflow

Generate an initial config for a group:

`kayobe playbook run $PWD/ansible/firewall-generate.yml --limit compute --extra-vars "debug=True"`

Check the generated output in `$KAYOBE_CONFIG_PATH/etc/firewallgen` to see differences between
the hosts in the group:

`diff -Nau etc/firewallgen/svn2-dr06-u7 etc/firewallgen/svn4-dr06-u7`

If you aren't happy with the rules you can adjust:

- `firewallgen_ipv4_input_allow_rewrite_rules`
- `firewallgen_ipv4_input_allow_custom_rules`

to alter the rules.

If the rules are consistent across the hosts you can place one
of the generated files as a group_var in the inventory:

`cp etc/firewallgen/svn4-dr06-u7  etc/kayobe/inventory/group_vars/compute/firewall`

otherwise you can use host_vars instead.

To apply the changes non-persistently use:

`kayobe playbook run $PWD/ansible/firewall-test.yml --limit storage`

Persist the firewall across reboots:

`kayobe playbook run $PWD/ansible/firewall-apply.yml --limit storage`

to delete the firewall and set the INPUT/OUTPUT chains to ACCEPT:

`kayobe playbook run $PWD/ansible/firewall-remove.yml --limit svn2-dr06-u7`

# Tips

- use `--extra-vars "debug=True"` to dump collected data. You can use this
  to prototype your rewrite rules
- delete the output in `$KAYOBE_CONFIG_PATH/etc/firewallgen` after each run
  so that you only have the hosts in group you are interested in


