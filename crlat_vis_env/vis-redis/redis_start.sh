#!/usr/bin/env bash

container_name=vis-redis
docker_image_name=redis
container_found=$(docker ps -a | grep $container_name | awk '{print $1}')
if [ -n "$container_found" ]; then docker rm -f $container_name; fi
docker_images=$(docker images | grep $docker_image_name | awk '{print $1}')
if [ -n "$docker_images" ]; then docker rmi -f $docker_images; fi
docker rm -f `docker ps -a | grep vis-redis | awk '{print $1}'`
docker run --name $container_name -d -p 6379:6379 $docker_image_name