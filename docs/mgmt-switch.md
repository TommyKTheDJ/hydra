# Deploying configuration to management switches

- Working process
```
1) Creates temporary config files based on info from group_vars/all
2) Pushes config to switches
3) Deletes temporary files
```

*Important: pushes only incremental config, what means that existing config is only updated, not replaced*
