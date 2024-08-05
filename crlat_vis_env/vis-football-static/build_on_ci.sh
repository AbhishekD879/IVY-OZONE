#!/usr/bin/env bash
CURR_DIR=$(PWD)
VIS_DIRECTORY_NAME=vis-football-widget-3d
VIS_DIRECTORY_PATH=../../
VIS_DIRECTORY=$VIS_DIRECTORY_PATH$VIS_DIRECTORY_NAME
docker_image_name=vis-football-widget-3d
docker_images=$(docker images | grep $docker_image_name | awk '{print $1}')
if [ -n "$docker_images" ]; then docker rmi -f $docker_images; fi
if [ -d "$VIS_DIRECTORY_NAME" ]; then rm -rf $VIS_DIRECTORY_NAME; fi
#enable below for local debug
set -e
[[ -d "$VIS_DIRECTORY" ]] || git clone -b master git@bitbucket.org:symphonydevelopers/vis-football-widget-3d.git $VIS_DIRECTORY
set +e
cd $VIS_DIRECTORY
git submodule update --init --recursive --checkout
cd $CURR_DIR
mv $VIS_DIRECTORY .
docker build -t $docker_image_name -f Dockerfile .
mv $VIS_DIRECTORY_NAME $VIS_DIRECTORY