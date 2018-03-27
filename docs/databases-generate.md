# Generating the lab database

1. Change the generate_database.yml file with the correct path to your lab .xls file

   i.e. `src: "{{ inventory_dir }}/shared/hydra_lab_inventory.xlsx`

2. Run the generation playbook

   `ansible-playbook -i inventory playbooks/databases-generate.yml`
