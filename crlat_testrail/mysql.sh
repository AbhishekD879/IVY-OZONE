#!/usr/bin/env bash
docker rm -f crlat_mysql
mkdir -p $PWD/mysql/data/
rm -rf $PWD/mysql/data/*
docker run -d --name crlat_mysql -e MYSQL_ROOT_PASSWORD=secret -v $PWD/mysql/data:/var/lib/mysql -p 3306:3306 crlat_mysql
