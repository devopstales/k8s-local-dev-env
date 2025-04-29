# 04 Certificates

## mkcert

## Reflector

## Cert Manager

## CA Injector

```yaml
# CA injector injects ca bundle in secret "public-bundle" t pod with label:
microcumul.us/injectssl: "public-bundle"
```

## Trust manager

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
