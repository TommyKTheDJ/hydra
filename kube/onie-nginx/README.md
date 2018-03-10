# Nginx-cluster with persistent volumes

This folder provides the files necessary to deploy an nginx cluster using a glusterfs persistent volume.

This requires having a functional kubectl working environment.

Adjust the parameters to reflect your environment such as the glusterfs endpoint IP addresses, volume sizes and TCP ports.

Then execute the following commands in order:

```
kubectl apply -f onie-namespace.yml
kubectl apply -f glusterfs-service.yml
kubectl apply -f glusterfs-endpoints.yml
kubectl apply -f gluster-persistentvolume.yml
kubectl apply -f gluster-persistentvolumeclaim.yml
kubectl apply -f nginx-service.yml
kubectl apply -f nginx-deployment.yml
```
