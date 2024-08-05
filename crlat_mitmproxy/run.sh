#!/usr/bin/env bash
docker run --name crlat_mitmproxy --rm -it -p 8080:8080 -p 8081:8081 -v $PWD/ca:/root/.mitmproxy crlat_mitmproxy
