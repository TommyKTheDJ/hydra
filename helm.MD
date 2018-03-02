# Installing Helm

1. Check kubectl config - ensure you're using the correct context that's pointing at the right cluster
`kubectl config view`

2. Install the Tiller pod
`helm init`

3. Verify the installation
`kubectl get pods --namespace kube-system`
