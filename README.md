# Deploying Kubernetes using Kubespray
All information sourced here: https://github.com/kubernetes-incubator/kubespray

## Steps to run through
- Install Ansible
```
sudo apt-get update
sudo apt-get install software-properties-common
sudo apt-add-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install -y ansible
```
- Run the kubespray-prequisites.yml playbook
```
ansible-playbook -i "localhost," -c local kubespray-prerequisites.yml
```
- Run the inventory generator with the four IPs of the nodes (check they're correct)
```
cd /tmp/kubespray/kubsespray
cp -r inventory/sample inventory/hydracluster
declare -a IPS=(10.60.3.25 10.60.3.26 10.60.3.27 10.60.3.28)
CONFIG_FILE=inventory/hydracluster/hosts.ini python3 contrib/inventory_builder/inventory.py ${IPS[@]}
```
- Enable the netchecker option (for verification)
```
vi /inventory/sample/group_vars/k8s-cluster.yml
(set deploy_netchecker: true) - line 129
```
- Run the deployment playbook
```
ansible-playbook -i inventory/hydracluster/hosts.ini cluster.yml -b -v  --private-key=~/.ssh/id_rsa
```
- Connect to the first master and verify
```
ssh 10.60.30.25 'kubectl get all'
```
- Connect to each node and verify using netchecker
```
curl http://localhost:31081/api/v1/connectivity_check
```