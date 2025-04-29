# 04 Certificates

## mkcert

A self signed root certificate is automaticle generated eizj `mkcert` into the `.cert` folder, andautomaticle applied as a secret called `ca-key-pair`.

## Reflector

Automaticle copy secrets and configmaps for all namespaces. For example the CA certificates secret will be mirrored to all the namespaces. For this the fallowing annotation is neaded:

```yaml
apiVersion: v1
kind: Secret
metadata:
 name: source-secret
 annotations:
   reflector.v1.k8s.emberstack.com/reflection-allowed: "true"
   reflector.v1.k8s.emberstack.com/reflection-allowed-namespaces: "namespace-1,namespace-2,namespace-[0-9]*"
data:
 ...
```

## CA Trust

A Deployment named `node-custom-setup` Automaticle ads the root CA as trusted for the Kubernetes nodes.

## Cert Manager

Cert-Manager is an operator to automaticle generate certificates for Ingress hosts.

```yaml
# Generate certificate for ingress
cert-manager.io/cluster-issuer: ca-issuer

# cert-manager inject certificate for ValidatingWebhookConfiguration with the fallowing annotation
# form certificate object elastic-webhook in namesoace elastic-system
cert-manager.io/inject-ca-from: elastic-system/elastic-webhook
cert-manager.io/inject-ca-from-secret: elastic-webhook-secret
cert-manager.io/inject-apiserver-ca: "true"
```

## Cluster issuer

We will use a root CA secret `ca-key-pair` in the cluster-issuer for generating certificates for the apps.

## CA Injector

```yaml
# CA injector injects ca bundle in secret "public-bundle" t pod with label:
microcumul.us/injectssl: "public-bundle"
```

## Trust manager

Inject Trust CA bundle into pods

```yaml
# trust manager generates bundle from ca in secret "ca-key-pair" to "public-bundle" secret in namespace with label:
inject-trust: "enabled"
```

## Inject cert with Kyverno policy

```yaml
# Kyverno policy inject t pod with labels:
inject-trust-to-java: "enabled"
inject-trust: "enabled"
```
