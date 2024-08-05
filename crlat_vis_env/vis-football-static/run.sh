#!/usr/bin/env bash
set -e
# OSX
#if [ -n "$MY_IP" ]; then MY_IP=$(/sbin/ifconfig en0 | grep 'inet ' | awk '{ print $2}') || true fi


## linux
MY_IP=$(/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}') || true
echo detected IP $MY_IP
container_name=vis-football-3d
container_found=$(docker ps -a | grep $container_name | awk '{print $1}')
if [ -n "$container_found" ]; then docker rm -f $container_name; fi
docker run \
    -d \
    -p 5000:5000 -p 5500:5500 \
    -e MY_IP=$MY_IP \
    --name $container_name \
    vis-football-widget-3d
