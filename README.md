# k8s-local-dev-env ☸️ <!-- omit in toc -->

![kubernetes-localdev-cover](https://d33vo9sj4p3nyc.cloudfront.net/kubernetes-localdev/kubernetes-localdev-cover.png?dummy=null)

## Required packages <!-- omit in toc -->

#### 1. [Install docker](https://docs.docker.com/engine/install/ubuntu/) <!-- omit in toc -->

```bash
# update packages
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
 
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# run with sudo
sudo usermod -aG docker ${USER}
su - ${USER}
sudo chmod 666 /var/run/docker.sock
```

#### 2. [Install brew](https://brew.sh/) <!-- omit in toc -->

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew install kubernetes-cli
brew install kubectx
brew install helm
brew install helmfile
brew install minikube
brew install cilium-cli

helm plugin install https://github.com/databus23/helm-diff
```

#### 4. Instal frr (Optional) <!-- omit in toc -->

```bash
```
