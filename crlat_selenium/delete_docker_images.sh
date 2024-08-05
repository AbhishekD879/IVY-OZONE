#!/usr/bin/env bash
set -x

for i in $(docker images | grep crlat_selenium | awk 'NR>1 {print $3}');
do
    docker rmi -f $i
done

for zombie_container in $(docker ps -aq -f status=exited);
do
    docker rm -v $zombie_container
done

docker image prune -af
docker volume rm $(docker volume ls -qf dangling=true)

sudo /etc/init.d/docker restart