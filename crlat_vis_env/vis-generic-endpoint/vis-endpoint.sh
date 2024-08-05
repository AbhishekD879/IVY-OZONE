#!/usr/bin/env bash

container_name=vis-football-endpoint
docker_image_name=vis-football-endpoint:latest-tst
docker_repository=registry-coral.symphony-solutions.eu
container_found=$(docker ps -a | grep $container_name | awk '{print $1}')
if [ -n "$container_found" ]; then docker rm -f $container_name; fi
docker_images=$(docker images | grep $docker_image_name | awk '{print $1}')
if [ -n "$docker_images" ]; then docker rmi -f $docker_images; fi

docker pull $docker_repository/$docker_image_name
docker run \
    -d \
    --link vis-redis:vis-redis \
    -e REDISES=vis-redis:6379 \
    -e NODE_ENV=tst \
    -p 8120:8120 \
    --name=$container_name \
    $docker_repository/$docker_image_name \
    npm start
