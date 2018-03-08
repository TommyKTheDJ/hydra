# Run the playbook to deploy the ingress controller
```
export ANSIBLE_VAULT_PASSWORD_FILE=.vault_pass
ansible-playbook -i inventory/virtual_inventory ingress-controller.yml --
```

All information sourced here: https://github.com/kubernetes/ingress-nginx/tree/master/deploy

# Create all the resources on the Kubernetes cluster
```
kuebctl apply -f /tmp/ingress/namespace.yaml
kuebctl apply -f /tmp/ingress/default-backend.yaml
kuebctl apply -f /tmp/ingress/configmap.yaml
kuebctl apply -f /tmp/ingress/tcp-services-configmap.yaml
kuebctl apply -f /tmp/ingress/udp-services-configmap.yaml
kuebctl apply -f /tmp/ingress/rbac.yaml
kuebctl apply -f /tmp/ingress/with-rbac.yaml
kuebctl apply -f /tmp/ingress/service-nodeport.yaml
```

## Verify that the default-backend is a ClusterIP and get the ingress nodePort details
```
kubectl get svc --namespace=ingress-nginx
NAMESPACE       NAME                   TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
ingress-nginx   default-http-backend   **ClusterIP**   10.233.28.120   <none>        80/TCP                       18h
ingress-nginx   ingress-nginx          NodePort    10.233.39.254   <none>        80:**30905**/TCP,443:**30666**/TCP   9s
```

## Verify which node the default-backend is running on
```
kubectl get pods --namespace=ingress-nginx
NAMESPACE       NAME                                        READY     STATUS             RESTARTS   AGE
ingress-nginx   default-http-backend-55c6c69b88-w77c2       1/1       Running            0          18h
ingress-nginx   nginx-ingress-controller-5c6698dfbf-m2jbq   1/1       Running            0          1h

kubectl describe pod default-http-backend-55c6c69b88-w77c2 --namespace=ingress-nginx
Name:           default-http-backend-55c6c69b88-w77c2
Namespace:      ingress-nginx
Node:           **castor/10.60.3.26**
```

## Browse to that nodePort (from outside the cluster) - you should receive a 200 response
```
curl -I http://10.60.3.26:30905
HTTP/1.1 404 Not Found
Server: nginx/1.13.9
Date: Thu, 08 Mar 2018 16:48:55 GMT
Content-Type: text/plain; charset=utf-8
Content-Length: 21
Connection: keep-alive
Strict-Transport-Security: max-age=15724800; includeSubDomains;

curl -I http://10.60.3.26:30905/healthz
HTTP/1.1 200 OK
Server: nginx/1.13.9
Date: Thu, 08 Mar 2018 16:48:47 GMT
Content-Type: text/html
Content-Length: 0
Connection: keep-alive
Strict-Transport-Security: max-age=15724800; includeSubDomains;
```
