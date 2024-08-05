#!/usr/bin/env bash
py_version=${PY_VERSION:-py3}
docker build -t crlat_locustio:${py_version} -f Dockerfile.${py_version} .
