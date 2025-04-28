# TODO

* dependecy install [X]
* docker network [X]
  * kind start [X]
    * ingress port forward [X]
  * caching docker registry [ ]
* CNI
  * cilium [X]
* CRD
  * prometheus [X]
  * gateway api [X] - 1.3.0
* DNS ???
  * add to hostfile [X]
  * external dns [ ]
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
  * pomerium
    * pomerium - gateway api [ ]
    * keycloak itegration [ ]
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
* app
  * dashboard
  * harbor registry ???
    * https://purushothamkdr453.medium.com/harbor-registry-setup-on-kind-kubernetes-cluster-96c13afdfaaa
    * https://k8s.co.il/kubernetes/deploying-harbor-kind-and-helm-charts/
    * https://kind.sigs.k8s.io/docs/user/private-registries/#use-a-certificate
  * auditlog
    * https://kind.sigs.k8s.io/docs/user/auditing/