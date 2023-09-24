# k8s-local-dev-env

This repository contains helmper scripts and kubernetes manifests for k3s and KinD (Kubernetes in Docker) developer environments on Linux and macOS.

# Table of contents

1. [Requirements](#Requirements)
2. [Installation](#installation)
3. [K3s](#k3s)
  1. [K3S Files to ZFS](#k3s-files-to-zfs-optional)
  2. [Local docker refistry](#local-docker-registry-on-zfs)
    1. [Local docker regisregistry as caching proxy](#local-docker-registry-as-caching-proxy)

# Requirements

* docker-ce or docker for macOS
* brew

> On macOS the install script automatically installs the necessary packages with brew.
> On Linux the install script automatically installs the necessary packages if you have brew.

Packages to install on Linux:

* git
* kubectx
* helm
* helmfile
* mkcert
* cilium-cli
* hubble
* skopeo
* oras
* tilt

## macOS

Unlike Docker on Linux, Docker-for-Mac does not expose container networks directly on the macOS host. Docker-for-Mac works by running a Linux VM under the hood (using [`hyperkit`](https://github.com/moby/hyperkit)) and creates containers within that VM.

Docker-for-Mac supports connecting to containers over Layer 4 (port binding), but not Layer 3 (by IP address).

To solwe this issue we will use [docker-mac-net-connect](https://github.com/chipmk/docker-mac-net-connect) That create a minimal network tunnel between macOS and the Docker Desktop Linux VM using WireGuard.

```bash
# Install via Homebrew
$ brew install chipmk/tap/docker-mac-net-connect

# Run the service and register it to launch at boot
$ sudo brew services start chipmk/tap/docker-mac-net-connect

# Restart the docker for mac services
```

# Installation

```bash
cd ~
git clone https://github.com/devopstales/k8s-local-dev-env.git

export PATH="$HOME/k8s-local-dev-env/bin:$PATH"

echo 'export PATH="$HOME/k8s-local-dev-env/bin:$PATH"' >> $HOME/.bashrc
# or
echo 'export PATH="$HOME/k8s-local-dev-env/bin:$PATH"' >> $HOME/.zshrc
```

# K3S

> The K3S environment is only tested on Linux, I used Ubuntu 22.04

## K3S Files to ZFS (Optional)

Ubuntu has the ability to manage the ZFS filesystem. So We can use it to separate the K3S files.

```bash
sudo zfs create -s -V 50GB zpool/k3s
sudo mkfs.ext4 /dev/zvol/zpool/k3s
sudo mount /dev/zvol/zpool/k3s /var/lib/rancher

echo "/dev/zvol/zpool/k3s /var/lib/rancher ext4 defaults 0 0" >> /etc/fstab
```

## Local docker-registry on ZFS

We can use ZFS to  separate the local docker registry's files.

```bash
sudo zfs create -s -V 50GB zpool/docker
sudo mkfs.ext4 /dev/zvol/zpool/docker-registry
sudo mount /dev/zvol/zpool/docker-registry /var/lib/docker-registry

echo "/dev/zvol/zpool/docker-registry /var/lib/docker-registry ext4 defaults,_netdev 0 0" >> /etc/fstab

chown -R docker-registry:docker-registry /var/lib/docker-registry

sudo apt install docker-registry -y
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
```

```bash
echo "127.0.1.1       registry.k3s.intra" >> /etc/hosts
systemctl restart docker-registry
```

Test the local registry

```bash
docker pull nginx:latest
docker push registry.k3s.intra:5000/nginx:latest
docker tag nginx:latest registry.k3s.intra:5000/nginx:latest

curl -X GET http://registry.k3s.intra:5000/v2/_catalog
{"repositories":["nginx"]}
```

### Local docker-registry as caching proxy

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