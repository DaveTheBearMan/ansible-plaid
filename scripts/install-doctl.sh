#!/bin/bash
# Snap install package
sudo snap install doctl

# Ensure config directory
sudo mkdir -p /root/.kube/
mkdir -p ~/.config
sudo snap connect doctl:kube-config

# Authenticate to doctl
doctl auth init --context 'Master'
doctl account get

# Connect to cluster
sudo doctl kubernetes cluster kubeconfig save $1
