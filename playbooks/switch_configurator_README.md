This playbooks is in charge to crete configuration files for switches. Currently it creates configuration for management switchtes,
which are Cisco Nexus currently, but can be easy extended.

Prerequisits:
1) templates "step0.j2" and "nexus.j2" in templates folder
2) vars "vlans_subnets.yml" and "connectivity_matrix.yml" in "host_vars" folder

Tipp:
1) execute limited to management switches (i.e. "--limit hydra-mgmt-1")

Outcomes:
1) device abstraction (vendor-agnostic format) file in nodes/{{ inventory_hostname }}/base.yml
2) configuration file in output/{{ inventory_hostname }}.conf
