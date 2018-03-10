# Deploy the kubernetes dashboard service

To deploy the dashboard execute this play

```
$ kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml
```

Then, on the host where the dashboard UI wants to be executed run
```
kubectl proxy&
```

This will launch the web GUI that is then accessible at:

[http://localhost:8001/ui](http://localhost:8001/ui)
