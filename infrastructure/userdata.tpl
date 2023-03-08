#!/bin/bash

yum update -y &&
rpm --import https://yum.corretto.aws/corretto.key &&
curl -L -o /etc/yum.repos.d/corretto.repo https://yum.corretto.aws/corretto.repo &&
yum install -y java-16-amazon-corretto-devel &&

export MINECRAFT_SERVER_DIRECTORY="/opt/minecraft/server"
export MINECRAFT_PORT=25565
export MINECRAFT_MAX_MEMORY=2048
export MINECRAFT_MIN_MEMORY=1024

python scripts/src/run_administrator.py
