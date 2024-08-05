#!/usr/bin/env bash
sudo mkdir -p /var/go/influxdb
sudo docker stop crlat_influx
sudo docker rm -f crlat_influx
sudo docker run -d \
      --name=crlat_influx \
      -p 8083:8083 \
      -p 8086:8086 \
      --restart always \
      -v /var/go/grafana:/var/lib/influxdb \
      influxdb

sleep 5
