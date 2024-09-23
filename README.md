# k8s-local-dev-env

A píthon based script that starts a local kind based Kubernetes Developmant environment and Install apps.

## Features

* Generate self signed certificate authority
* Start kind Cluster
  * Import image to kind cluster
  * Run a separate dns server for ingress dns resolution
    * coredns and external-dns
* Start apps
  * Cilium CNI
  * LoadBalancer
    * Cilium L2 loadbalancer
  * Cert-Manager
    * Generate certs under self signed CA
  * Nginx INgress Controller
    * Nodeport
    * loadbalancer

## Required packages

### Ubuntu 20.04

```bash
apt update
apt-get install build-essential libtool pkgconf libzstd-dev liblzma-dev libssl-dev autoconf
apt-get install python3 python3-pip

pip3 install -r requirements.txt
```

* kind
* docker
* kubectl
* helm
* helmfile

### OSX

```bash
brew install autoconf automake libtool
brew install chipmk/tap/docker-mac-net-connect
sudo brew services start chipmk/tap/docker-mac-net-connect

pip3 install -r requirements.txt
```

Start docker dasktop

## Required Kernel modules:

```bash
sudo modprobe xt_socket -v

lsmod | grep xt_socket
```
