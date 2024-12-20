
# Root CA

A self signed root certificate is automaticle generated in teh `.cert` folder.

## CA Trust

A Deployment named `node-custom-setup` Automaticle ads the root CA as trusted for the Kubernetes nodes.

# Cert-Manager

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

We will use a root CA cluster issuer for certificate management.

# Trust Manager

Generating Trust CA bundle with self signed CA

```yaml
# trust manager generates bundle from ca in secret "ca-key-pair" to "public-bundle" secret in namespace with label:
inject-trust: "enabled"
```

# CA Injector

Inject Trust CA bundle into pods

```yaml
# CA injector injects ca bundle in secret "public-bundle" to pod with label:
microcumul.us/injectssl: "public-bundle"
```

# Kyverno Policy

```yaml
# Kyverno policy inject to pod with labels:
inject-trust-to-java: "enabled"
inject-trust: "enabled"
```

# Reflector

Automaticle copy secrets and configmaps for all namespaces. For example CA certificates. For this the fallowing annotation is neaded:

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
