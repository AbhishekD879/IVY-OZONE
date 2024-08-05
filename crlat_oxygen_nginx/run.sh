#!/usr/bin/env bash
docker run \
    -d \
    -p 80:80 \
    -p 443:443 \
    -v /var/go/www:/var/www \
    -v $PWD/resources/etc/nginx/conf.d/:/etc/nginx/conf.d/ \
    --name crlat_oxygen_nginx \
    crlat_oxygen_nginx
