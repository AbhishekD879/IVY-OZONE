#!/usr/bin/env bash
set -x
docker \
run -d \
-p 4444:4444 \
-p 5900:5900 \
-v /dev/shm:/dev/shm \
--dns=192.168.192.174 \
    --add-host="service.maxymiser.net: 127.0.0.1" \
    --add-host="at_mac_mini:172.23.78.17" \
    --add-host="at_ub_tv:172.23.78.18" \
    --add-host="at_ub_host:172.23.78.19" \
    --add-host="spark-br.symphony-solutions.eu:10.0.1.239" \
    --add-host="bp-stg-coral.symphony-solutions.eu:54.154.158.165" \
    --add-host="obbackoffice-stg2.gib1.egalacoral.com:10.5.26.159" \
    --add-host="google.com:127.0.0.1" \
--name=selenium-remote-debug selenium/standalone-chrome-debug