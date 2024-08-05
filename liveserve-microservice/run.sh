#!/bin/bash

SPRING_PROFILES_ACTIVE=$1 ./gradlew bootRun | tee live.log
