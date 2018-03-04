New version of the mgmt_swithces config. The following working process:
1) Creates temporary config files based on info grom group_vars/all
2) Pushes config to switches
3) Deletes temporary files
'Imporant: pushes only incremental config, what means that existing config is only updated, not repaced'
