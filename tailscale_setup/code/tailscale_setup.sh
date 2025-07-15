#!/bin/bash

sudo apt update
sudo apt upgrade -y
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up