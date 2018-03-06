docker run -it --rm \
-v /Users/arnoldin/Projects/hydra/inventory/physical_inventory:/aos/physical_inventory \
-v /Users/arnoldin/Projects/hydra/playbooks/group_vars/cumulus/:/aos/group_vars/cumulus/ \
aos-device-installer \
install \
--inventory physical_inventory \
--limit cumulus
