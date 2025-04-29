# TODO

* dependecy install [X]
* docker network [X]
  * kind start [X]
    * ingress port forward [X]
  * minikube start [ ]
  * caching docker registry [ ]
* CNI
  * cilium [X]
* CRD
  * prometheus [X]
  * gateway api [X] - 1.3.0
* DNS ???
  * add to hostfile [X]
  * external dns [ ]
    * https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/pihole.md
  * pihole [ ]
    * https://github.com/MoJo2600/pihole-kubernetes/tree/main/charts/pihole
  * coredns [ ]
  * etcd [ ]
* certificate [ ]
  * certgen [X]
    * cert secret [X]
  * cert-manager [X]
    * cluster issuer [X]
  * reflector [X]
    * cert annotate [X]
  * trust manager [x]
    * trust bundle [X]
* Ingress
  * Nginx-ingress [X]
  * traefik
    * gateway api [ ]
    * sso itegration [ ]
* observinility
  * grafana
  * grafana operator
  * grafana call
  * victoria metrics
  * alert dashboard
  * slack vs mattermost ???
* sso
  * keycloak [ ]
  * keycloak operator [ ]
  * kubedash [ ]
  * https://geek-cookbook.funkypenguin.co.nz/docker-swarm/traefik-forward-auth/
  * https://geek-cookbook.funkypenguin.co.nz/docker-swarm/traefik-forward-auth/dex-static/
  * https://dexidp.io/docs/connectors/local/
  * https://github.com/coderanger/traefik-forward-auth-dex
* app
  * dashboard
  * harbor registry ???
    * https://purushothamkdr453.medium.com/harbor-registry-setup-on-kind-kubernetes-cluster-96c13afdfaaa
    * https://k8s.co.il/kubernetes/deploying-harbor-kind-and-helm-charts/
    * https://kind.sigs.k8s.io/docs/user/private-registries/#use-a-certificate
  * auditlog
    * https://kind.sigs.k8s.io/docs/user/auditing/
  * OpenFGA