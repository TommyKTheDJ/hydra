# This playbook configures the DHCP server

1. Make sure the [dhcp_servers] group in lab_inventory is accurate

2. Make sure you have the group_vars/all/database.yml updated with the latest hosts/mac-addresses/IPs

3. Run the configuration playbook

   `export ANSIBLE_VAULT_PASSWORD_FILE=.vault_pass`
   `ansible-playbook -i lab_inventory playbooks/configure_dhcp.yml`
