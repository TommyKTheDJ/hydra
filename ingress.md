# Run the playbook to deploy the ingress controller
```
export ANSIBLE_VAULT_PASSWORD_FILE=.vault_pass
ansible-playbook -i inventory/virtual_inventory ingress-controller.yml --
```

All information sourced here: https://github.com/kubernetes/ingress-nginx/tree/master/deploy
