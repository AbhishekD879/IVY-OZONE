#!/bin/sh

export spring_profiles_active=$1

mkdir log
./gradlew bootRun | tee log/run.log
