#!/usr/bin/env bash
unzip web/testrail-5.3.0.3603-ion53.zip -d web/
docker build -t crlat_testrail ./web/
