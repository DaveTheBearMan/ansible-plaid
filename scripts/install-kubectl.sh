#!/bin/bash
# https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/
# Update packages and get dependancies
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg

# Get current kubectl version
version=$(curl "https://kubernetes.io/releases/" | grep "Release History</h2><h3 id=release-v[0-9]-[0-9][0-9]>" | grep -o ">[0-9]\.[0-9][0-9]<" | grep -o "[0-9]\.[0-9][0-9]")

# Get public signing key
# sudo mkdir -p -m 755 /etc/apt/keyrings # Distros older than Ubuntu 22.04 and Debian 12 do not have this folder
curl -fsSL "https://pkgs.k8s.io/core:/stable:/v$version/deb/Release.key" | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
sudo chmod 644 /etc/apt/keyrings/kubernetes-apt-keyring.gpg # allow unprivileged APT programs to read this keyring

# This overwrites any existing configuration in /etc/apt/sources.list.d/kubernetes.list
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.33/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo chmod 644 /etc/apt/sources.list.d/kubernetes.list   # helps tools such as command-not-found to work correctly

# Update apt index, then install
sudo apt-get update
sudo apt-get install -y kubectl
