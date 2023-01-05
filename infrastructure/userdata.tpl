#!/bin/bash

yum update -y &&

rpm --import https://yum.corretto.aws/corretto.key &&
curl -L -o /etc/yum.repos.d/corretto.repo https://yum.corretto.aws/corretto.repo &&
yum install -y java-16-amazon-corretto-devel &&

adduser minecraft &&
mkdir -p /opt/minecraft/server &&
cd /opt/minecraft/server/ &&

wget https://piston-data.mojang.com/v1/objects/c9df48efed58511cdd0213c56b9013a7b5c9ac1f/server.jar &&
chown -R minecraft:minecraft /opt/minecraft/server/

su minecraft


