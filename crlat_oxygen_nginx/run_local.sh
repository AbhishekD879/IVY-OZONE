#!/usr/bin/env bash
docker run \
    --rm -it \
    -p 443:443 \
    -p 80:80 \
    -v $PWD/www:/var/www \
    -v $PWD/resources/etc/nginx/conf.d/:/etc/nginx/conf.d/ \
    --add-host="crlat_oxygen_bpp:172.23.99.29" \
    --name crlat_oxygen_nginx \
    crlat_oxygen_nginx
