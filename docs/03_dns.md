# 03 DNS

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

## Pi-hole

## Custom CoreDNS

## External-DNS

