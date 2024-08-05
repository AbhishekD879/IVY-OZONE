#!/usr/bin/env bash
docker run \
    -it \
    --rm \
    -p 80:80 \
    --name crlat_nginx \
    crlat_nginx
