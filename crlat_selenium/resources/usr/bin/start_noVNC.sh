#!/bin/bash
cd /var/noVNC
dkr_id=${DKR_ID:-1}
./utils/launch.sh --vnc localhost:590${dkr_id} --listen 608${dkr_id} &
