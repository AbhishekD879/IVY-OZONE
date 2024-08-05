#!/usr/bin/env bash


#
#recoders=$(ps aux | grep flvrec| awk 'NR==1 {print $2}')
#if [ -n $recoders ]; then
#    kill $recoders
#    rm -f ./video.flv
#fi
##vnc4server -geometry ${WIDTH}x${HEIGHT} $DISPLAY
#sleep 3
#/usr/local/bin/flvrec.py -q -P /var/go/.vnc/pass -o ./video.flv localhost:${DKR_ID} &
#avconv -f x11grab -r 25 -s 480x800  -i localhost$DISPLAY -ar 44100 -threads 1 -vf scale=360:600 /tmp/output.webm -y -loglevel panic &
#avconv -f x11grab -r 25 -s $SC_separator  -i localhost:3 -ar 44100 -threads 1 -vf scale=360:600 /tmp/output.webm -y -loglevel panic &
echo disabled
#exit 0