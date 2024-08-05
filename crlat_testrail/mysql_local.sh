#!/usr/bin/env bash
docker rm -f crlat_mysql
docker run -d --name crlat_mysql -e MYSQL_ROOT_PASSWORD=secret -p 3306:3306 crlat_mysql


