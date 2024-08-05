#!/usr/bin/env bash
docker run \
    -it \
    --rm \
    --shm-size=256M \
    -p 5050:5050 \
    --link crlat_mongo:crlat_mongo \
    --name crlat_harstorage \
    crlat_harstorage
