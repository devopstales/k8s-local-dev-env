# TODOS

## Routing

```bash
# route podcidr to kind-controll-plain
sudo ip route add 10.0.0.0/16 via 172.18.0.2

# BGP ?
```

## Auth

https://medium.com/@charled.breteche/kind-keycloak-securing-kubernetes-api-server-with-oidc-371c5faef902

```bash
k create ns auth-system

helm upgrade --install --wait --timeout 15m \
  --namespace auth-system --create-namespace \
  --repo https://charts.bitnami.com/bitnami keycloak keycloak \
  --reuse-values --values - <<EOF
auth:
  createAdminUser: true
  adminUser: admin
  adminPassword: admin
  managementUser: manager
  managementPassword: manager
proxyAddressForwarding: true
ingress:
  enabled: true
  hostname: keycloak.kdev.intra
  annotations:
    kubernetes.io/ingress.class: nginx
  tls: true
  extraTls:
  - hosts:
    - keycloak.kdev.intra
    secretName: keycloak-tls
postgresql:
  enabled: false
  postgresqlPassword: password
externalDatabase:
  host: "none"
extraEnvVars:
  - name: KEYCLOAK_DATABASE_VENDOR
    value: "dev-file"
EOF
```

## Monitoring

```bash
PushProx ???
```

##  Docs

* https://medium.com/@charled.breteche/securing-grafana-with-keycloak-sso-d01fec05d984
* https://medium.com/@charled.breteche/kind-fix-missing-prometheus-operator-targets-1a1ff5d8c8ad
* https://particule.io/en/blog/k8s-no-cloud/
* https://medium.com/@charled.breteche/kind-cluster-with-cilium-and-no-kube-proxy-c6f4d84b5a9d
* https://medium.com/@charled.breteche/kind-cilium-metallb-and-no-kube-proxy-a9fe66ddfad6
* https://medium.com/@charled.breteche/using-dnsmasq-with-a-local-kind-clusters-9a27c8987073


## Future

* Identity-based Security
  * SPIFFE
    * https://artifacthub.io/packages/helm/helm-spire/spire
  * SPIRE
  * https://cert-manager.io/docs/usage/csi-driver-spiffe/