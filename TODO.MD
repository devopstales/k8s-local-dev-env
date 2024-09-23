# TODOS

## Routing

```bash
# route podcidr to kind-controll-plain
sudo ip route add 10.0.0.0/16 via 172.18.0.2

# BGP ?
```

## Auth

https://medium.com/@charled.breteche/kind-keycloak-securing-kubernetes-api-server-with-oidc-371c5faef902

## Monitoring

```bash
PushProx ???
```

## Docs

* https://medium.com/@charled.breteche/securing-grafana-with-keycloak-sso-d01fec05d984
* https://medium.com/@charled.breteche/kind-fix-missing-prometheus-operator-targets-1a1ff5d8c8ad
* https://particule.io/en/blog/k8s-no-cloud/
* https://medium.com/@charled.breteche/kind-cluster-with-cilium-and-no-kube-proxy-c6f4d84b5a9d
* https://medium.com/@charled.breteche/kind-cilium-metallb-and-no-kube-proxy-a9fe66ddfad6
* https://medium.com/@charled.breteche/using-dnsmasq-with-a-local-kind-clusters-9a27c8987073
* registry
  * https://kind.sigs.k8s.io/docs/user/local-registry/
  * https://medium.com/@charled.breteche/caching-docker-images-for-local-kind-clusters-252fac5434aa
  * https://maelvls.dev/docker-proxy-registry-kind/


## Future

* Identity-based Security
  * SPIFFE
    * https://artifacthub.io/packages/helm/helm-spire/spire
  * SPIRE
  * https://cert-manager.io/docs/usage/csi-driver-spiffe/
  * https://docs.cilium.io/en/stable/network/servicemesh/mutual-authentication/mutual-authentication-example/

## Bugs

* cilium operator number [-]
* loadbalancer pool as string in double quots [?]
* loadbalancer static ip
* keycloak auto import realm [-]
* keycloak ingress certificate [-]
* keycloak monitoring [-]


8ZFWQojAUwIsgMWp8taYAuHkWutjP4fU
GZrYHf64WZWKBxnB0f2h6xlFwZOZJXyL
