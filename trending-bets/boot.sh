#!/bin/sh

mkdir -p log
gradle bootBuildImage && docker-compose up | tee log/boot.log
