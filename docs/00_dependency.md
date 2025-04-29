# Dependencies

All the Dependencies are installed with brew because it is avaiable for linux and OSX.

```bash
BREW_HOME="${XDG_DATA_HOME:-${HOME}/}.homebrew"
if [ ! -d $BREW_HOME ];then
    git clone https://github.com/Homebrew/brew $BREW_HOME
fi
eval "$($BREW_HOME/bin/brew shellenv)"
brew update --force --quiet
```

The automatization for the Kubernetes cluster creation and installation of the apps is made with `Taskfile`. It is nececarry to be installed.

```bash
brew install go-task
```

All the other tolls can be automaticly installed by `task`:

```bash
cd ~/k8s-local-dev-env
task dependency
```

Or by manually with `brew`:

```bash
brew install kind
brew install minikube

brew install kubernetes-cli
brew install kubectx

brew install helm
brew install helmfile
helm plugin install https://github.com/databus23/helm-diff

brew install cilium-cli

brew install mkcert
brew install nss # if you use Firefox

sudo wget https://raw.github.com/xwmx/hosts/master/hosts -O /usr/local/bin/hosts && \
sudo chmod +x /usr/local/bin/hosts && \
hosts completions install --download
```

## OSX

On OSX The docker Deskto runs the container in a Virtual machine. So to making the Docker Network reachable In MacOS, we will create a tunel:

```bash
# Install via Homebrew
brew install chipmk/tap/docker-mac-net-connect

# Run the service and register it to launch at boot
brew services start chipmk/tap/docker-mac-net-connect
```
