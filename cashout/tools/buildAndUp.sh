#!/usr/bin/env bash
./gradlew clean build && docker-compose -f docker-compose.yaml build && docker-compose -f docker-compose.yaml up
