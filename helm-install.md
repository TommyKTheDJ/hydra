# Installing Helm

1. Run the installation playbooks

   `ansible-playbook -i inventory playbooks/helm-install.yml`

2. Check kubectl config - ensure you're using the correct context that's pointing at the right cluster

   `kubectl config view`

3. Install the Tiller pod

   `helm init`

4. Verify the installation

   `kubectl get pods --namespace kube-system`
