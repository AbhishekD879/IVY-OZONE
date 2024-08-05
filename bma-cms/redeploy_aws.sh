#!/bin/bash
INSTANCE=${1:-"test"}
REVISION=${2:-"latest"}
HOST=${3:-"jumphost"}
source ./prepare-deployment.sh ${INSTANCE} ${REVISION}
ssh -A ${HOST} "ssh ${INST}" <<< "${FINAL_SCRIPT}"
