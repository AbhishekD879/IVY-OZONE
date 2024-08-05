#!/usr/bin/env bash
docker run --name bpp-redis --rm -p 6379:6379 redis redis-server --appendonly no --save ""