#!/bin/bash
HOST=${2:-"dev"}
REVISION=${1:-"latest"}
source ./prepare-deployment.sh test ${REVISION}
ssh ${HOST} <<< "${FINAL_SCRIPT}"
source ./restart_nginx.sh
ssh ${HOST} <<< "${RUN_SCRIPT}"
