#!/usr/bin/env bash

MY_IP=$(hostname --ip-address)
docker run \
    -d \
    --name=crlat_oxygen_bpp \
    -p 8080:8080 \
    --link bpp-redis:bpp-redis \
    -e REDIS_HOST=bpp-redis \
    -e REDIS_PORT=6379 \
    -v $PWD/resources/web.xml:/usr/local/tomcat/webapps/Proxy/WEB-INF/web.xml \
    crlat_oxygen_bpp

echo "address=/crlat-oxygen-bpp.coral.co.uk/${MY_IP}" > /var/go/dnsmasq.d/crlatbpp.conf
