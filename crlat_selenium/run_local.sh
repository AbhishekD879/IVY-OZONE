#!/usr/bin/env bash
set -x
DKR_ID=${1:-1}
echo "*** Starting Selenium docker id: $DKR_ID"

docker run \
    --rm \
    -it \
    --shm-size=1g \
    -p 590${DKR_ID}:590${DKR_ID} \
    -p 608${DKR_ID}:608${DKR_ID} \
    -e DKR_ID=$DKR_ID \
    -e MASTERHOST=$HOSTNAME \
    -e DISPLAY=:${DKR_ID} \
    -e MASTSER_AGENT_ENVIRONMENT=$GO_ENVIRONMENT_NAME \
    --add-host="service.maxymiser.net: 127.0.0.1" \
    --add-host="mob-push.coral.co.uk:127.0.0.1" \
    --add-host="at_mac_mini:172.23.78.17" \
    --add-host="at_ub_tv:172.23.78.18" \
    --add-host="at_ub_host:172.23.78.19" \
    --add-host="invictus.coral.co.uk:52.16.3.251" \
    --add-host="spark-br-tst.symphony-solutions.eu:10.0.1.239" \
    --env-file=env.list \
    --cap-add=SYS_ADMIN \
    -v $PWD/tmp:/stream \
    --name crlat_selenium_$DKR_ID \
    py3_crlat_selenium bash
