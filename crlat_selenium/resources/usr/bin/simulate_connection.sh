#!/usr/bin/env bash
VERSION=0.2
device=eth0
bandwidth=100kbps
latency=350ms
packetloss=0%
command=slow
retcode=0
PATH=/sbin:/bin:/usr/sbin:/usr/bin

echorun() {
  echo -E '#' "$@"
  "$@"
}

if ! which tc > /dev/null; then
  echo "Aborting: No 'tc' iptables firewall traffic conditioner found" 1>&2
  echo "This requires the Linux iptables firewall." 1>&2
  exit 1
fi

if [ $EUID -ne 0 ]; then
  echo "Aborting: you must run this as root."
  exit 2
fi


while test $# -gt 0
do
  case $1 in

  # Normal option processing
    -h | --help)
      # usage and help
      command=help
      break
      ;;
    -v | --version)
      command=version
      break
      ;;
    -d | --device)
      shift
      device=$1
      ;;
    -b | --bandwidth)
      shift
      bandwidth=$1
      ;;
    -l | --latency)
      shift
      latency=$1
      ;;
    -p | --packetloss)
      shift
      packetloss=$1
      ;;
  # ...

  # Special cases
    --)
      break
      ;;
    --*)
      # error unknown (long) option $1
      ;;
    -?)
      # error unknown (short) option $1
      ;;

   # Shortcuts
       AMPS|amps)
         command=slow
         bandwidth=14kbps
         latency=250ms
         ;;
       EDGE|edge|2.5G|GPRS|gprs)
         command=slow
         bandwidth=50kbps
         latency=200ms
         ;;
       3G|3g)
         command=slow
         bandwidth=1000kbps
         latency=200ms
         ;;
       4G|4g)
         command=slow
         bandwidth=10000kbps
         latency=100ms
         ;;
       modem-0.1k|modem-110)
         command=slow
         bandwidth=110bps
         latency=350ms
         ;;
       modem-0.3k|modem-300)
         command=slow
         bandwidth=300bps
         latency=300ms
         ;;
       modem-1.2k|modem-1200)
         command=slow
         bandwidth=1200bps
         latency=280ms
         ;;
       modem-2.4k|modem-2400)
         command=slow
         bandwidth=2400bps
         latency=250ms
         ;;
       modem-9.6k|modem-9600)
         command=slow
         bandwidth=9600bps
         latency=200ms
         ;;
       modem-14.4k|modem-14400)
         command=slow
         bandwidth=14400bps
         latency=150ms
         ;;
       modem-28.8k|modem-28800)
         command=slow
         bandwidth=28800bps
         latency=150ms
         ;;
       modem-56k|modem-56000)
         command=slow
         bandwidth=56kbps
         latency=120ms
         ;;
       56k)
         command=slow
         bandwidth=56kbps
         latency=40ms
         ;;
       T1|t1)
         command=slow
         bandwidth=1500kbps
         latency=20ms
         ;;
       T3|t3)
         command=slow
         bandwidth=45mbps
         latency=10ms
         ;;
       DSL|dsl)
         command=slow
         bandwidth=2mbps
         latency=40ms
         ;;
       cablemodem)
         command=slow
         bandwidth=10mbps
         latency=20ms
         ;;
       wifi-a|wifi-g)
         command=slow
         bandwidth=54mbps
         latency=5ms
         ;;
       wifi-b)
         command=slow
         bandwidth=11mbps
         latency=10ms
         ;;
       wifi-n)
         command=slow
         bandwidth=110mbps
         latency=2ms
         ;;
       vsat)
         command=slow
         bandwidth=5mbps
         latency=500ms
         ;;
       clear|reset)
         command=clear
         ;;
       status)
         command=status
         break
         ;;

  # FUN STUFF HERE:
  # Split apart combined short options
    -*)
      split=$1
      shift
      set -- $(echo "$split" | cut -c 2- | sed 's/./-& /g') "$@"
      continue
      ;;

  # Done with options
    *)
      break
      ;;
  esac

  # for testing purposes:
  echo "param $1"

  shift
done

echo "command=$command"
echo "bandwidth=$bandwidth"
echo "latency=$latency"

case $command in
  help)
    echo $0
    echo 'Usage: slow <network-type> [-d device] [-b bandwidth] [-l latency] [-p drop]'
    echo '       slow reset'
    echo '       slow status'
    echo
    echo '"network-type" type can be:'
    echo '  GPRS'
    echo '  GSM'
    echo '  EDGE'
    echo '  2.5G'
    echo '  GPRS'
    echo '  3G'
    echo '  4G'
    echo '  modem-2.4k'
    echo '  modem-9.6k'
    echo '  modem-14.4k'
    echo '  modem-28.8k'
    echo '  modem-56k'
    echo '  56k'
    echo '  T1'
    echo '  T3'
    echo '  DSL'
    echo '  cablemodem'
    echo '  wifi-a'
    echo '  wifi-b'
    echo '  wifi-g'
    echo '  wifi-n'
    echo '  eth-10'
    echo '  eth-100'
    echo '  eth-1000'
    echo '  vsat'
    echo '  vsat-busy'
    ;;
  version)
    # version info
    echo "slow version $VERSION"
    echo "Copyright (c) 2012 Modus Create"
    ;;
  slow)
    if  tc qdisc show dev $device | fgrep -q "qdisc htb 1: root"; then
      verb=change
      echo "Changing existing queuing discipline"
    else
      verb=add
      echo "Adding new queuing discipline"
      echorun tc qdisc $verb dev $device root handle 1: htb default 12
    fi
    if ! lsmod | fgrep -q "sch_netem"; then
      modprobe sch_netem
    fi
    echorun tc class $verb dev $device parent 1:1 classid 1:12 htb rate $bandwidth ceil $bandwidth  &&
    echorun tc qdisc $verb dev $device parent 1:12 netem delay $latency loss $packetloss
    retcode=$?
    ;;
  clear)
    echo resetting queueing discipline
    echorun tc qdisc del dev $device root
    retcode=$?
    ;;
  status)
    echorun tc qdisc
    retcode=$?
    ;;
esac

exit $retcode
