#!/bin/bash

cd $HOME
git clone https://github.com/devopstales/k8s-local-dev-env.git

export PATH="$HOME/k8s-local-dev-env/bin:$PATH"

if [ $SHELL == "/bin/bash"]; then
  echo 'export PATH="$HOME/k8s-local-dev-env/bin:$PATH"' >> $HOME/.bashrc
elif [ $SHELL == "/bin/zsh"]; then
  echo 'export PATH="$HOME/k8s-local-dev-env/bin:$PATH"' >> $HOME/.zshrc
fi
