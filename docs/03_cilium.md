
# LoadBalancer

```bash
sudo apt install frr -y
```

## Cilium BGP

```bash
sudo vtysh -c 'show bgp summary'
sudo vtysh -c 'show ip bgp neighbors 198.18.254.2'
sudo vtysh -c 'show ip bgp neighbors 198.18.254.2 advertised-routes'
```

```bash
kubectl exec -it cilium-thqr8 -- cilium bgp peers
kubectl exec -it cilium-thqr8 -- cilium bgp routes
```

## Host FRR Config

```bash
task ???

cp ~/k8s-local-dev-env/config/frr/* /etc/frr/
```
