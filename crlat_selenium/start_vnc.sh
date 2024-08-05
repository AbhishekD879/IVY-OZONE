#!/bin/bash
set -x
#export DISPLAY=:${DKR_ID}
sudo mkdir -p /var/lib/go-agent/config
/bin/rm -f /var/lib/go-agent/config/autoregister.properties

MASTERHOST="${MASTERHOST:-unknown}"
#AGENT_HOSTNAME=$HOSTNAME-ON-$MASTERHOST
AGENT_RESOURCES=$AGENT_RESOURCES,$MASTERHOST
AGENT_ENVIRONMENTS=OxygenUI_test_docker_$MASTSER_AGENT_ENVIRONMENT
AGENT_KEY="${AGENT_KEY:-123456789abcdef}"
sudo touch /var/lib/go-agent/config/autoregister.properties
echo "agent.auto.register.key=$AGENT_KEY" | sudo tee /var/lib/go-agent/config/autoregister.properties
if [ -n "$AGENT_RESOURCES" ]; then echo "agent.auto.register.resources=$AGENT_RESOURCES" | sudo tee -a /var/lib/go-agent/config/autoregister.properties; fi
if [ -n "$AGENT_ENVIRONMENTS" ]; then echo "agent.auto.register.environments=$AGENT_ENVIRONMENTS" | sudo tee -a /var/lib/go-agent/config/autoregister.properties; fi

sudo chown -R go:go /var/lib/go-agent/config
#Xvnc4 :3 -geometry $GEOMETRY -depth 24 -rfbwait 30000 -rfbauth /var/go/.vnc/passwd -pn -fp /usr/X11R6/lib/X11/fonts/Type1/,/usr/X11R6/lib/X11/fonts/Speedo/,/usr/X11R6/lib/X11/fonts/misc/,/usr/X11R6/lib/X11/fonts/75dpi/,/usr/X11R6/lib/X11/fonts/100dpi/,/usr/share/fonts/X11/misc/,/usr/share/fonts/X11/Type1/,/usr/share/fonts/X11/75dpi/,/usr/share/fonts/X11/100dpi/ -co /etc/X11/rgb &

sudo /etc/init.d/dbus start
#X_separator=$WIDTH
#X_separator+=x
#X_separator+=$HEIGHT
#Xvnc4 :3 -geometry $X_separator -rfbwait 30000 -rfbauth /var/go/.vnc/passwd -pn -fp /usr/X11R6/lib/X11/fonts/Type1/,/usr/X11R6/lib/X11/fonts/Speedo/,/usr/X11R6/lib/X11/fonts/misc/,/usr/X11R6/lib/X11/fonts/75dpi/,/usr/X11R6/lib/X11/fonts/100dpi/,/usr/share/fonts/X11/misc/,/usr/share/fonts/X11/Type1/,/usr/share/fonts/X11/75dpi/,/usr/share/fonts/X11/100dpi/ -co /etc/X11/rgb &
#Xvnc4 :1 -geometry $GEOMETRY -depth 24 -rfbwait 30000 -rfbauth /var/go/.vnc/passwd -rfbport 5901 -pn -fp /usr/X11R6/lib/X11/fonts/Type1/,/usr/X11R6/lib/X11/fonts/Speedo/,/usr/X11R6/lib/X11/fonts/misc/,/usr/X11R6/lib/X11/fonts/75dpi/,/usr/X11R6/lib/X11/fonts/100dpi/,/usr/share/fonts/X11/misc/,/usr/share/fonts/X11/Type1/,/usr/share/fonts/X11/75dpi/,/usr/share/fonts/X11/100dpi/ -co /etc/X11/rgb

echo -e "$VNC_PASSWD\n$VNC_PASSWD" |vnc4passwd
vnc4server $VNC_GEOMETRIES :${DKR_ID}
#sudo /etc/init.d/go-agent start &
#tail -f  /var/log/go-agent/go-agent.log
