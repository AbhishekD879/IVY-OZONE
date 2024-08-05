#!/bin/sh

mkdir -p log
gradle bootRun --debug-jvm | tee log/debug.log
