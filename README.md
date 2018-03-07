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
ansible-playbook -i inventory/virtual_inventory kubespray-install.yml --
```
- Run the deployment playbook
```
ansible-playbook -i inventory/virtual_inventory cluster.yml -b -v
```
- Connect to the first master and verify
```
ssh 10.60.30.25 'kubectl get nodes'
```
- Connect to each node and verify using netchecker
```
curl http://localhost:31081/api/v1/connectivity_check
```

# Install additional services
Helm install: [./helm-install.md]
