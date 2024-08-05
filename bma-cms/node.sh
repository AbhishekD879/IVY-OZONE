#!/bin/bash

iterator=0
trap "" HUP
action=$1

function main(){
  until node -p --trace-deprecation keystone.js >> server.log
  do
    ((iterator++))
    [ $iterator -ge 5 ] && break
    sleep 2s
  done

}

function stop(){
  #kill -KILL $(ps aux | grep 'node keystone.js' | awk '{print $2}')
  sptPid=$(ps aux | grep './[n]ode.sh [s]tart' | awk '{print$2}')
  ndPid=$(ps aux | grep '[k]eystone.js' | awk '{print$2}')
  if [[ $sptPid -eq '' && $ndPid -ne '' ]]; then
    sptPid=$(ps aux | grep './[n]ode.sh [r]estart' | awk '{print$2}')
  fi
  if [[ $sptPid ]]; then
    kill -KILL $sptPid
    kill -KILL $ndPid
  fi
}


case $action in
  'start')
    main > /dev/null 2&>1 &
    ;;
  'stop')
    stop
    ;;
  'restart')
    stop
    main &
    ;;
  *)
    #echo 'Usage: start|stop|restart'
    ;;
esac