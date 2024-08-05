#!/usr/bin/env bash
set -x
TOTAL="${NUM_AGENTS:-2}"
DOCKER_NAME="${DOCKER_NAME_PATTERN:-crlat_selenium}"
for i in $(docker ps -a | grep ${DOCKER_NAME} |awk '{print $1}');
do
        docker rm -f $i
done