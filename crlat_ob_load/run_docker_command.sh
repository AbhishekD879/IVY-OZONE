#!/usr/bin/env bash
set -x
command=${1:-"echo command undefined ; exit 1"}

docker run \
    --rm \
    --name=crlat_liveupdates_locustio \
    -v $PWD:/locust \
    docker-registry.crlat.net/crlat_locustio:py2 "${command}"
