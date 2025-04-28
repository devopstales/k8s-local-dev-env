
# LoadBalancer

## Cilium BGP

```bash
sudo vtysh -c 'show bgp summary'
sudo vtysh -c 'show ip bgp neighbors 172.50.0.2'
sudo vtysh -c 'show ip bgp neighbors 172.50.0.2 advertised-routes'
```

```bash
keti cilium-thqr8 -- cilium bgp peers
keti cilium-thqr8 -- cilium bgp routes
```

## Host FRR Config

```bash
sudo apt install frr -y

kdev --up all

cp ~/k8s-local-dev-env/mount/frr/* /etc/frr/
```
