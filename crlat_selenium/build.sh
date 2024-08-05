#!/usr/bin/env bash
set -x
py_version=${PY_VERSION:-py3}
docker build -t crlat_selenium_base -f dockerfiles/selenium_base/Dockerfile .
docker build -t ${py_version}_crlat_selenium -f dockerfiles/${py_version}/Dockerfile .