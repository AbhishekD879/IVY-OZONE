#!/usr/bin/env bash
#export MY_IP=192.168.99.100

./vis-redis/redis_start.sh
./vis-mapper/vis-rtc-tennis.sh

./vis-generic-endpoint/vis-endpoint.sh

cd ./vis-football-static/
./build_local.sh
./run.sh

cd ..

