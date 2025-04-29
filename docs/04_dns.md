# 03 DNS

The KDEV Development environment use the `kdev.intra` as the witecard domain for oll theservices.

## Headless service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: custom-dns-service
  namespace: default # Optional: Specify namespace if not in "default"
spec:
  clusterIP: None # Makes it a headless service
```

```yaml
apiVersion: v1
kind: Endpoints
metadata:
  name: custom-dns-service # Must match the headless service name
  namespace: default # Ensure the namespace matches the service
subsets:
  - addresses:
      - ip: 192.168.1.100 # The custom IP address for the DNS record
```

```bash
kubectl exec -it <pod-name> -- nslookup custom-dns-service.default.svc.cluster.local

Server:    10.96.0.10
Address:   10.96.0.10#53
Name:      custom-dns-service.default.svc.cluster.local
Address:  192.168.1.100
```

## host file

By Default the KDEV will run in NAT mode so all the services will be avaiable rtout the ingress witch ports are NAT-id in the host. The easiest way to manage the DNS for this is the fostfile. KDEV use the `hosts` utility to manage the hostfile:

```bash
task add-hosts
```

## Pi-hole

## Custom CoreDNS

We created a new CoreDNS instance that is act as a local DNS server for the clients. It stores all its data in an etcd cluster.

## External-DNS

Generating DNS records for ingress hostnames in the Custom CoreDNS instance or Pi-hole.