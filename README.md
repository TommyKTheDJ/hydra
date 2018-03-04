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
- Run the kubespray-install.yml playbook
```
export ANSIBLE_VAULT_PASSWORD_FILE=.vault_pass
ansible-playbook -i inventory kubespray-install.yml --
```
- Run the inventory generator with the four IPs of the nodes (check they're correct)
```
cd /tmp/kubespray/kubsespray
cp -r inventory/sample inventory/hydracluster
declare -a IPS=(10.60.3.25 10.60.3.26 10.60.3.27 10.60.3.28)
CONFIG_FILE=inventory/hydracluster/hosts.ini python3 contrib/inventory_builder/inventory.py ${IPS[@]}
```
- Choose the networking plugin you want (we're using the default, calico)
```
vi /inventory/sample/group_vars/k8s-cluster.yml (lines 65-67)

# Choose network plugin (cilium, calico, contiv, weave or flannel)
# Can also be set to 'cloud', which lets the cloud provider setup appropriate routing
kube_network_plugin: calico
```
- Enable the netchecker option in k8s-cluster.yml (for verification)
```
vi /inventory/sample/group_vars/k8s-cluster.yml (line 129)

# Deploy netchecker app to verify DNS resolve as an HTTP service
deploy_netchecker: true
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
