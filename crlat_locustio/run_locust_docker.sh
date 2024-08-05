#!/usr/bin/env bash

docker run \
    --rm -it \
    --name=crlat_locustio \
    -p 8089:8089 \
    -v $PWD:/locust \
    crlat_locustio sh

