#!/bin/bash
set -x
export LC_ALL="en_US.UTF-8"
git pull origin
git checkout dev
git submodule update --init --recursive
npm install &&\
cd ./bma-betstone/ &&\
npm install &&\
cd ./public/js/lib/angular &&\
bower install &&\
cd ../../../../../ &&\
grunt build:remote &&\
echo "Done"
