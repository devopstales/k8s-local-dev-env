# TODOS

## Routing

```bash
# route podcidr to kind-controll-plain
sudo ip route add 10.0.0.0/16 via 172.18.0.2

# BGP ?
docker run --rm -itd --privileged --network kind --name bird_router pierky/bird:2.15
# https://github.com/metallb/frr-k8s
docker run --name frr_router \
-itd \
--privileged \
--network kind  \
-v $HOME/k8s-local-dev-env/mounts/frr/:/tmp/frr \
quay.io/frrouting/frr:10.2.0 \
bash -c /tmp/frr/frr-entrypoint.sh
# https://raw.githubusercontent.com/metallb/frr-k8s/main/config/all-in-one/frr-k8s.yaml
# https://github.com/ksator/frrouting_demo/tree/master

docker exec -it frr_router vtysh -c 'show bgp summary'
docker exec -it frr_router vtysh -c 'show ip bgp neighbors 172.50.0.2'
docker exec -it frr_router vtysh -c 'show ip bgp neighbors 172.50.0.2 advertised-routes'

keti cilium-thqr8 -- cilium bgp peers
keti cilium-thqr8 -- cilium bgp routes

#kubectl annotate node kind-control-plane bgp_enabled="true"
#kubectl annotate node kind-control-plane cilium.io/bgp-virtual-router.65001="router-id=172.50.0.2"
#kubectl annotate node kind-control-plane cilium.io/bgp-virtual-router.65002="local-port=3179"



# cloud provider
# https://console.cloud.google.com/gcr/images/k8s-staging-kind/GLOBAL/cloud-provider-kind
docker run --rm -itd --network kind -v /var/run/docker.sock:/var/run/docker.sock --name cloud-provider-kind gcr.io/k8s-staging-kind/cloud-provider-kind:v20240917-31dac43

docker um -itd cloud-provider-kind 

# sr-iov ???
```

## FRR

* https://allanjohn909.medium.com/harnessing-the-power-of-cilium-a-guide-to-bgp-integration-with-gateway-api-on-ipv4-7b0d058a1c0d
* https://allanjohn909.medium.com/integrating-cilium-with-gateway-api-ipv6-and-bgp-for-advanced-networking-solutions-5b41b0ca0090

## Monitoring

* https://medium.com/@giorgiodevops/kind-install-prometheus-operator-and-fix-missing-targets-b4e57bcbcb1f
* https://medium.com/@charled.breteche/securing-grafana-with-keycloak-sso-d01fec05d984
* https://medium.com/@charled.breteche/kind-fix-missing-prometheus-operator-targets-1a1ff5d8c8ad
* PushProx

## Docs

* https://particule.io/en/blog/k8s-no-cloud/

## Future

* Identity-based Security
  * SPIFFE
    * https://artifacthub.io/packages/helm/helm-spire/spire
  * SPIRE
  * https://cert-manager.io/docs/usage/csi-driver-spiffe/
  * https://www.kusari.dev/blog/spiffe-spire-csi-driver
  * https://docs.cilium.io/en/latest/network/servicemesh/mutual-authentication/mutual-authentication/
  * https://docs.cilium.io/en/stable/network/servicemesh/mutual-authentication/mutual-authentication-example/
  * https://github.com/accuknox/cilium-spire-tutorials
* kind lazy load

```bash
docker build -t stargz-kind-node https://github.com/containerd/stargz-snapshotter.git
kind create cluster --name stargz-demo --image stargz-kind-node
```

## containerlab

* https://containerlab.dev/manual/kinds/k8s-kind/#__tabbed_1_3
* https://github.com/martimy/clab-bgp-frr/blob/master/bgp-frr.clab.yml

