#!/usr/bin/env bash
docker rm -f crlat_testrail
mkdir -p web/shared_folder
docker run -d \
  --link=crlat_mysql:crlat_mysql \
  --name=crlat_testrail \
  -v $PWD/web/shared_folder:/shared_folder \
  -p 80:80 \
  crlat_testrail

