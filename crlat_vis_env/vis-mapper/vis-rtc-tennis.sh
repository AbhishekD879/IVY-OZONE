#!/usr/bin/env bash

container_name=vis-rtc-tennis
docker_image_name=vis-rtc-tennis
container_found=$(docker ps -a | grep $container_name | awk '{print $1}')
if [ -n "$container_found" ]; then docker rm -f $container_name; fi
docker_images=$(docker images | grep $docker_image_name | awk '{print $1}')
if [ -n "$docker_images" ]; then docker rmi -f $docker_images; fi
docker pull registry-coral.symphony-solutions.eu/vis-rtc-tennis:latest-tst
set -e
# linux
MY_IP=$(/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}') || true
# OSX
if [ -n "$MY_IP" ]; then MY_IP=$(/sbin/ifconfig en0 | grep 'inet ' | awk '{ print $2}') || true; fi
docker run \
    -d \
    -p 8085:8085 -p 8110:8110 \
    --link vis-redis:vis-redis \
    -e REDIS_HOST=vis-redis \
    -e MY_IP=${MY_IP} \
    -e REDIS_PORT=6379 \
    -e NODE_ENV=tst \
    --name $container_name \
    registry-coral.symphony-solutions.eu/vis-rtc-tennis:latest-tst \
    sh -c "sed \"s/https:\/\/coral-vis-rtc-tst2.symphony-solutions.eu/http:\/\/$MY_IP/g\" \
        /opt/vis-tennis/ui/constants/tst.json > /opt/vis-tennis/ui/constants/tst.json.$ && \
        sed \"s/https:\/\/vis-tst2-coral.symphony-solutions.eu/http:\/\/$MY_IP:8120/g\" \
        /opt/vis-tennis/ui/constants/tst.json.$ > /opt/vis-tennis/ui/constants/tst.json.$$ && \
        mv /opt/vis-tennis/ui/constants/tst.json.$$ /opt/vis-tennis/ui/constants/tst.json && \
        /usr/local/bin/gulp tst:tennis"
