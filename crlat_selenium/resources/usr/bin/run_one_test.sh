#!/bin/bash

set -v
platform=${PLATFORM:-chrome}
hostname=${OX_HOSTNAME:-invictus.coral.co.uk}
pytest_timeout=${PYTEST_TIMEOUT:-300}
mark=${MARK:-prod}
JOB_SELECTOR=${GO_JOB_RUN_INDEX:-1}
screen_resolution=${RESOLUTION:-540x1110}
device=${DEVICE_NAME:-Galaxy S9}
discovered_tests_file_name=${DISCOVERED_TESTS_FILENAME}
run_test=${RUN_TESTS:-True}
test=$(sed "${JOB_SELECTOR}q;d" ${discovered_tests_file_name})

kill_third_party_processes()
{
  echo "*** Executing ${FUNCNAME[0]}"
  killall chrome
  killall chromedriver
  killall avconv
}

publish_report()
{
  echo "*** Executing ${FUNCNAME[0]}"
  mkdir -p reports
  rm -rf reports/*
  mkdir -p reports/$GO_PIPELINE_NAME/$OX_HOSTNAME/$GO_PIPELINE_COUNTER
  mv -f report reports/$GO_PIPELINE_NAME/$OX_HOSTNAME/$GO_PIPELINE_COUNTER
  rsync -ar reports/$GO_PIPELINE_NAME go@services.crlat.net:/var/www/reports
}

run_py_test()
{
echo "*** Executing ${FUNCNAME[0]}"
py.test --timeout=$pytest_timeout --alluredir=report/ $test -m "$mark" --hostname=$hostname --platform=$platform  --device_name="$device" -v --junit-xml=results.xml
}

if [[ $run_test == True ]] && [[ $test ]]; then

  kill_third_party_processes
  xrandr -s $screen_resolution
  start_record_video.sh

  echo "*** RUNNING TEST $test"
  run_py_test
  result="$?"
  if [[ ${result} == 86 ]]; then
    echo "*** RE-RUNNING TEST $test"
    kill_third_party_processes
    stop_record_video.sh
    start_record_video.sh
    run_py_test
  fi
  publish_report

  stop_record_video.sh
  kill_third_party_processes

  exit 0
else echo "Test run skipped for $test"
fi
