# Generating the configurations of lab devices (switches, pdus, console managers)

1. Run the generation playbook

   `export ANSIBLE_VAULT_PASSWORD_FILE=.vault_pass`

   `ansible-playbook -i inventory playbooks/devices-configs-generate.yml`
