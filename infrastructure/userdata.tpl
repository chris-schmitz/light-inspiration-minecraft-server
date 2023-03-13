#!/bin/bash
yum update -y &&
rpm --import https://yum.corretto.aws/corretto.key &&
curl -L -o /etc/yum.repos.d/corretto.repo https://yum.corretto.aws/corretto.repo &&
yum install -y java-17-amazon-corretto-devel &&

echo 'MINECRAFT_SERVER_DIRECTORY="/opt/minecraft/server"' >> /etc/environment
echo 'MINECRAFT_PORT=25565' >> /etc/environment
echo 'MINECRAFT_MAX_MEMORY=2048' >> /etc/environment
echo 'MINECRAFT_MIN_MEMORY=1024' >> /etc/environment

sudo python3 /home/ec2-user/scripts/src/run_administrator.py
