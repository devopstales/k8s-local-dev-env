# TODO

* docker network [X]
  * caching docker registry [ ]
* DNS ???
  * add to hostfile [X]
  * external dns [ ]
    * https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/pihole.md
  * coredns [ ]
  * etcd [ ]
* Ingress
  * traefik
    * gateway api [ ]
    * sso itegration [ ]
* observinility
  * grafana [x]
    * dex integration [ ]
  * grafana call
  * victoria metrics
    * https://blog.ogenki.io/post/series/observability/metrics/
    * https://blog.ogenki.io/post/series/observability/alerts/gs
    * https://github.com/Smana/cloud-native-ref/tree/main/observability/base/victoria-metrics-k8s-stack
    * https://github.com/VictoriaMetrics/helm-charts/blob/master/charts/victoria-metrics-k8s-stack/values.yaml
  * exporters [ ]
    * kube-state-metrics [X]
    * kube-bench-metrics [X]
    * k8s-ephemeral-storage-metrics [X]
    * certificate-exporter [X]
    * helm-exporter [X]
    * pushprox-controller-manager [ ]
    * pushprox-kube-proxy [ ]
    * pushprox-kube-scheduler [ ]
  * alert dashboard
  * slack vs mattermost ???
* sso
  * dex [X]
  * keycloak [ ]
  * keycloak operator [ ]
  * kubedash [ ]
  * k8s sso integration [ ]
  * https://gawsoft.com/blog/kubernetes-auth-oidc/
* app
  * hajimari [ ]
  * harbor registry ???
    * https://purushothamkdr453.medium.com/harbor-registry-setup-on-kind-kubernetes-cluster-96c13afdfaaa
    * https://k8s.co.il/kubernetes/deploying-harbor-kind-and-helm-charts/
    * https://kind.sigs.k8s.io/docs/user/private-registries/#use-a-certificate
  * monitoring
    * victoriametrics
    * victorialogs
    * tempo vs jaeger
      * https://opentelemetry.io/blog/2023/k8s-runtime-observability/
      * https://github.com/isovalent/cilium-grafana-observability-demo
      * https://getindata.com/blog/running-getindata-observability-stack/
      * https://fenyuk.medium.com/kubernetes-observability-with-opentelemetry-and-jaeger-8e072b7a4846
      * https://www.massdriver.cloud/blogs/observability-in-kubernetes-with-jaeger
      * https://www.cloudthat.com/resources/blog/achieving-end-to-end-observability-with-jaeger-for-distributed-tracing
    * inspektor-gadget
      * https://inspektor-gadget.io/docs/latest/legacy/prometheus/
  * Security
    * trivy operoator
    * kubearmor
      * https://docs.kubearmor.io/kubearmor/quick-links/deployment_guide
      * https://seifrajhi.github.io/blog/kubearmor-k8s-runtime-security/
      * https://github.com/kubearmor/kubearmor-prometheus-exporter
    * auditlog
      * https://kind.sigs.k8s.io/docs/user/auditing/
    * spire
      * https://gawsoft.com/blog/spiffe-spire-tls-jwt-jwks-oidc/