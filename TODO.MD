# TODOS

## Routing

```bash
# route podcidr to kind-controll-plain
sudo ip route add 10.0.0.0/16 via 172.18.0.2

# BGP ?
docker run --rm -itd --privileged --network kind --name bird_router pierky/bird:2.15

# cloud provider
# https://console.cloud.google.com/gcr/images/k8s-staging-kind/GLOBAL/cloud-provider-kind
docker run --rm -itd --network kind -v /var/run/docker.sock:/var/run/docker.sock --name cloud-provider-kind gcr.io/k8s-staging-kind/cloud-provider-kind:v20240917-31dac43

docker um -itd cloud-provider-kind
```

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
  * https://docs.cilium.io/en/stable/network/servicemesh/mutual-authentication/mutual-authentication-example/

## SSO:

```bash
pomerium: y5q5jeEpEmL7aJh74Tgsb32aJz1LaKAh
kind:     1Y1BDvwweUiVL89VFePBe5zSMIpI54NM
grafana:  blLT7cqamLqR9CriDn40gDhChgtRkT4F
kubedash: nkBeJzvrBxzRfGNDJENrEvwtnqczGLzk
```
