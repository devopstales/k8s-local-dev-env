# Obesevibility

## VictoriaMetrics

* vmagent
  * metric collecting agentmv
  * VMPodScrape
  * VMServiceScrape
  * VMScrapeConfig
* vmsingle
  * main componet
* Grafana
  * dashboards for 
  * GrafanaDashboard
* vmalert
  * a service for processing Prometheus-compatible alerting and recording rules.
* alertmanager
  * managing alert sendings

* vmauth
  * authorization proxy and load balancer optimized for VictoriaMetrics products.
* vmgateway
  * authorization proxy with per-tenant rate limiting capabilities.

```bash
client -> vmagent -> vmsingle -> vmalert -> alertmanager
Grafana -----------> vmsingle
Grafana -----------> alertmanager
```

## Grafana