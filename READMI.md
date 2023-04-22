# k8s-local-dev-env

```bash
cd ~
git clone https://github.com/devopstales/k8s-local-dev-env.git

export PATH="$HOME/k8s-local-dev-env/bin:$PATH"

echo 'export PATH="$HOME/k8s-local-dev-env/bin:$PATH"' >> $HOME/.bashrc
# or
echo 'export PATH="$HOME/k8s-local-dev-env/bin:$PATH"' >> $HOME/.zshrc
```

## Requirements

* git
* docker
* kubectl
* helm
* helmfile
* helm-diff plugin
* mkcert

```bash
brew install git
brew install kubectl
brew install kubectx
brew install helm
brew install helmfile
brew install cilium-cli
brew install skopeo
brew install mkcert
brew install oras
brew install tilt

helm plugin install https://github.com/databus23/helm-diff
```

## K3S Files to ZFS (Optional)

```bash
sudo zfs create -s -V 50GB zpool/k3s
sudo mkfs.ext4 /dev/zvol/zpool/k3s
sudo mount /dev/zvol/zpool/k3s /var/lib/rancher

echo "/dev/zvol/zpool/k3s /var/lib/rancher ext4 defaults 0 0" >> /etc/fstab
```

## docker-registry on ZFS

```bash
sudo zfs create -s -V 50GB zpool/docker
sudo mkfs.ext4 /dev/zvol/zpool/docker-registry
sudo mount /dev/zvol/zpool/docker-registry /var/lib/docker-registry

echo "/dev/zvol/zpool/docker-registry /var/lib/docker-registry ext4 defaults,_netdev 0 0" >> /etc/fstab

chown -R docker-registry:docker-registry /var/lib/docker-registry
```

```bash
echo "version: 0.1
log:
  fields:
    service: registry
storage:
  delete:
    enabled: true
  cache:
    blobdescriptor: inmemory
  filesystem:
    rootdirectory: /var/lib/docker-registry
http:
  addr: :5000
  headers:
    X-Content-Type-Options: [nosniff]
health:
  storagedriver:
    enabled: true
    interval: 10s
    threshold: 3
proxy:
  remoteurl: https://registry-1.docker.io
  username: [username]
  password: [password]" > /etc/docker/registry/config.yml
```

```bash
echo "127.0.1.1       registry.k3s.intra" >> /etc/hosts
systemctl restart docker-registry
```

```bash
docker pull nginx:latest
docker push registry.k3s.intra:5000/nginx:latest
docker tag nginx:latest registry.k3s.intra:5000/nginx:latest

curl -X GET http://registry.k3s.intra:5000/v2/_catalog
{"repositories":["nginx"]}
```
