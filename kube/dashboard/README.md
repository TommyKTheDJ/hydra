# Nginx-cluster with persistent volumes

This folder provides the files necessary to deploy an nginx cluster using a glusterfs persistent volume.

This requires having a functional kubectl working environment.

Execute the following commands in order

```
kubectl apply -f onie-namespace.yml
kubectl apply -f glusterfs-service.yml
kubectl apply -f glusterfs-endpoints.yml
kubectl apply -f gluster-persistentvolume.yml
kubectl apply -f gluster-persistentvolumeclaim.yml
kubectl apply -f nginx-service.yml
kubectl apply -f nginx-deployment.yml
```
