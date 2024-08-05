#!/usr/bin/env bash
set -x
env

TOTAL="${NUM_AGENTS:-2}"
for i in `seq 1 ${TOTAL}`;
do
        ./run.sh $i
done