#!/bin/bash

SCRIPT=$(cat <<- 'FILE'
	docker stop nginx &&\
	docker rm -v nginx &&\
	docker run -d --restart=on-failure --link bma-ui:bma-ui --link keystone:keystone -p 443:443 -v /home/core/Nginx/conf.d:/etc/nginx/conf.d -v /home/core/Nginx/ssl:/etc/nginx/ssl --name nginx nginx
FILE
)

RUN_SCRIPT=$(echo "$SCRIPT")

