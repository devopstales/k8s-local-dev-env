#!/bin/bash

unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Darwin;;
esac

if [ ${MACHINE} == "Linux" ]; then
    if [ -x "$(command -v brew)" ]; then
      binaries=(git kubectx helm helmfile mkcert cilium-cli hubble skopeo oras tilt)
      for bin in ${binaries[@]} ; do
        if ! [ -x "$(command -v $bin)" ]; then
            echo "##  Install $bin"
            brew install $bin
        fi
      done
      echo "##  Install helm diff plugin"
      helm plugin install https://github.com/databus23/helm-diff
    else
      echo "Please install the reqirements"
    fi
elif [ ${MACHINE} == "Darwin" ]; then
    binaries=(git kubectx helm helmfile mkcert cilium-cli hubble skopeo oras tilt)
    for bin in ${binaries[@]} ; do
      if ! [ -x "$(command -v $bin)" ]; then
          echo "##  Install $bin"
          brew install $bin
      fi
    done
    echo "##  Install helm diff plugin"
    helm plugin install https://github.com/databus23/helm-diff
else
    echo "Unknown MACHINE"
    exit 1
fi

if [ -x "$(command -v git)" ]; then
  cd $HOME
  git clone https://github.com/devopstales/k8s-local-dev-env.git
else
  echo "Missing package git"
fi

export PATH="$HOME/k8s-local-dev-env/bin:$PATH"

if [ $SHELL == "/bin/bash"]; then
  echo 'Add the bi directory to the PATH:
export PATH="$HOME/k8s-local-dev-env/bin:$PATH" >> $HOME/.bashrc'
elif [ $SHELL == "/bin/zsh"]; then
  echo 'Add the bi directory to the PATH:
export PATH="$HOME/k8s-local-dev-env/bin:$PATH" >> $HOME/.zshrc'
fi

