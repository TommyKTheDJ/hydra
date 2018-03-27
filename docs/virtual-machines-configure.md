# Configuring ALL the VMs with basic networking, hostnames, ssh keys, and docker

1. Run the playbook

  `export ANSIBLE_VAULT_PASSWORD_FILE=.vault_pass`

  `ansible-playbook -i inventory playbooks/virtual-machines-configure.yml`


If it's the first configuration, run

  `ansible-playbook -i inventory playbooks/virtual-machines-configure.yml -e initial=yes`
