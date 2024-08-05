#!/usr/bin/env sh
set -x
if [ -f "/locust/requirements.txt" ]; then
   pip install -r requirements.txt --trusted-host pypi.crlat.net
fi
if [ -f "/locust/setup.py" ]; then
    pip install -e . --trusted-host pypi.crlat.net
fi
sh -c "$1"