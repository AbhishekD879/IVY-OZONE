#!/usr/bin/env bash
docker run --rm --name=crlat_squid_proxy -p 3128:3128 crlat_squid_proxy /usr/local/bin/start-squid.sh