#!/usr/bin/env bash
set -x
DKR_ID=${1-1}
echo "*** Starting Selenium docker id: $DKR_ID"
py_version=${PY_VERSION:-py2}

agent_resources=${AGENT_RESOURCES_CONFIG:-"node, voltron"}
DKR_VMNAME=crlat_selenium_${DKR_ID}
docker run \
    -d \
    -v /dev/shm:/dev/shm \
    -p 590${DKR_ID}:590${DKR_ID} \
    -p 608${DKR_ID}:608${DKR_ID} \
    -e DKR_ID=$DKR_ID \
    -e MASTERHOST=$HOSTNAME \
    -e DOCKER_VM_NAME=${DKR_VMNAME} \
    -e DISPLAY=:${DKR_ID} \
    -e MASTSER_AGENT_ENVIRONMENT="$GO_ENVIRONMENT_NAME" \
    -e AGENT_RESOURCES="${agent_resources}" \
    --dns=192.168.192.174 \
    --add-host="service.maxymiser.net: 127.0.0.1" \
    --add-host="at_mac_mini:172.23.78.17" \
    --add-host="at_ub_tv:172.23.78.18" \
    --add-host="at_ub_host:172.23.78.19" \
    --add-host="google.com:127.0.0.1" \
    --env-file=env.list \
    --cap-add=NET_ADMIN \
    -v $PWD/tmp:/stream \
    -v /mnt/crlat-storage/allure:/mnt/reports \
    --tmpfs=/var/lib/go-agent/pipelines/ \
    --name ${DKR_VMNAME} \
    ${py_version}_crlat_selenium
