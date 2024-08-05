#!/usr/bin/env bash
sudo mkdir -p /var/go/grafana
sudo docker stop crlat_grafana
sudo docker rm -f crlat_grafana
sudo docker pull grafana/grafana:latest
sudo docker run -d \
    --name=crlat_grafana \
    -p 3000:3000 \
    --restart always \
    -v /var/go/grafana:/var/lib/grafana \
    --link=crlat_influx:crlat_influx \
    -e GF_SERVER_ROOT_URL=http://localhost:3000/ \
    -e GF_SERVER_DOMAIN=localhost \
    -e GF_SECURITY_ADMIN_USER=admin \
    -e GF_SECURITY_ADMIN_PASSWORD=secret#1\
    -e GF_SMTP_ENABLED=true \
    -e GF_SMTP_HOST=smtp.gmail.com:587 \
    -e GF_SMTP_USER=crl.alerter@gmail.com \
    -e GF_SMTP_FROM_ADDRESS=crl.alerter@gmail.com \
    -e GF_SMTP_PASSWORD=secret#1 \
    -e GF_SMTP_FROM_NAME=crl.alerter \
    -e GF_SMTP_SKIP_VERIFY=true \
    grafana/grafana
