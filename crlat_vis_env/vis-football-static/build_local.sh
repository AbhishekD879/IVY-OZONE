#!/usr/bin/env bash
DIRECTORY=vis-football-widget-3d
docker_image_name=vis-football-widget-3d

MY_IP=$(/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}') || true
docker_images=$(docker images | grep $docker_image_name | awk '{print $1}')
if [ -n "$docker_images" ]; then docker rmi -f $docker_images; fi
if [ -d "$DIRECTORY" ]; then rm -rf $DIRECTORY; fi
git clone -b master git@bitbucket.org:symphonydevelopers/vis-football-widget-3d.git
cd $DIRECTORY
git submodule update --init --recursive --checkout
cd ..
docker build -t $docker_image_name -f Dockerfile .
