#!/bin/bash
set -x
sudo chmod 777 /mnt/reports
start_vnc.sh
start_noVNC.sh
start_go.sh
tail -f  /var/log/go-agent/go-agent-stderr.log
