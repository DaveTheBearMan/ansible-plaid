#!/bin/bash
# Prompt for important information
echo -n "Kubernetes cluster GUID: "
read clusterGUID

# Install kubernetes
./install-kubectl.sh

# Install DOCTL
./install-doctl.sh $clusterGUID

# Verify connection
sudo kubectl cluster-info
sudo kubectl get nodes
